# django-slugify-processor

Custom-[`slugify()`](https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.text.slugify)
support for django.

[![Python Package](https://img.shields.io/pypi/v/django-slugify-processor.svg)](https://pypi.org/project/django-slugify-processor/)
[![Build Status](https://github.com/tony/django-slugify-processor/workflows/tests/badge.svg)](https://django-slugify-processor.git-pull.com/)
[![Docs](https://github.com/tony/django-slugify-processor/workflows/docs/badge.svg)](https://github.com/tony/django-slugify-processor/actions?query=workflow%3Adocs)
[![Code Coverage](https://codecov.io/gh/tony/django-slugify-processor/branch/master/graph/badge.svg)](https://codecov.io/gh/tony/django-slugify-processor)
[![License](https://img.shields.io/github/license/tony/django-slugify-processor.svg)](https://github.com/tony/django-slugify-processor/blob/master/LICENSE)

# What are slugs?

_Slugs_ are URL's, typically generated from post titles, that you want to be both human readable and
a valid URL. They are SEO friendly.

Django provides a
[slugify function](https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.text.slugify) in
`django.utils.text.slugify` which is also made available as a
[default filter](https://github.com/django/django/blob/4.0.0/django/template/defaultfilters.py#L247-255).

Django slugs can be automatically generated in django models via packages such as:

- [django-autoslug](https://pypi.python.org/pypi/django-autoslug)
  ([docs](https://pythonhosted.org/django-autoslug/))
  ([github](https://github.com/neithere/django-autoslug))
- [django-extensions](https://pypi.python.org/pypi/django-extensions) via
  [AutoSlugField](https://django-extensions.readthedocs.io/en/latest/field_extensions.html)
  ([docs](https://django-extensions.readthedocs.io/en/latest/))
  ([github](https://github.com/django-extensions/django-extensions))

# The problem

This project is based on an article from [devel.tech](https://devel.tech) covering
[django's import strings](https://devel.tech/tips/n/djms3tTe/how-django-uses-deferred-imports-to-scale/).

Corner cases exist with slugification. For instance: Corner cases exist with slugification. For
instance:

| Term | [`django.utils.text.slugify`] | What you want |
| ---- | ----------------------------- | ------------- |
| C    | c (correct)                   | n/a           |
| C++  | c                             | cpp           |
| C#   | c                             | c-sharp       |

To make matters worse, if using a specialized model field like `AutoSlugField` from django-autoslug
or django-extensions, the default behavior may be to name the slugs for C++ and C# to "c-1", "c-2"
after "c" is taken.

Here's another case, acronyms / shorthands:

| Term              | [`django.utils.text.slugify`] | What you (may) want |
| ----------------- | ----------------------------- | ------------------- |
| New York City     | new-york-city                 | nyc                 |
| Y Combinator      | y-combinator                  | yc                  |
| Portland          | portland                      | pdx                 |
| Texas             | texas                         | tx                  |
| $                 | '' (empty)                    | usd, aud, etc?      |
| US$               | us                            | usd                 |
| A$                | a                             | aud                 |
| bitcoin           | bitcoin                       | btc                 |
| United States     | united-states                 | usa                 |
| League of Legends | league-of-legends             | league              |
| Apple® iPod Touch | apple-ipod-touch              | ipod-touch          |

Each website and niche has its own edge cases for slugs. So we need a solution that can scale, where
you can craft your own functions.

# How django-slugify-processor helps

This builds on top of [`django.utils.text.slugify`] to handle your django project's edgecases. By
default, django-slugify-processor will be a pass through to django's default behavior. Adding
slugification functions via your Django project's settings file allows you to adjust.

[`django.utils.text.slugify`]:
  https://github.com/django/django/blob/4.0/django/template/defaultfilters.py#L232

# Installation

```console
$ pip install django-slugify-processor
```

# Configure

To create a processor, create a function that accepts a string, and returns a string. Assume this is
_project/app/slugify_processors.py_:

```python
def my_processor(value):
   value = value.replace('++', 'pp')
   return value
```

Inside of your settings, add a `SLUGIFY_PROCESSORS` list of strings that points to the function.
Anything that's compatible with
[import_string](https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.module_loading.import_string),
in your settings file:

```python
SLUGIFY_PROCESSORS = [
   'project.app.slugify_processors.my_processor'
]
```

# Usage

## In normal django code

Import `slugify` from `django_slugify_processor.text`:

```python
from django_slugify_processor.text import slugify

print(slugify('C++'))
> 'cpp'
```

## Template code

django-slugify-processor is designed to override the built-in`slugify` filter.

### via load

You can load by default via `{% load django_slugify_processor %}` in your template.

In your settings `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django_slugify_processor'
]
```

In your template:

```django
{% load slugify_processor %}
{{"C++"|slugify}}
```

### via built-in

To make this available in all templates, in the `OPTIONS` of your template engine, add
`django_slugify_processor.template_tags`:

```python
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'builtins': [
            'django_slugify_processor.templatetags.slugify_processor',
        ],
    },
}]
```

From within the template file:

```django
{{"C++"|slugify}}
```

Output should be: cpp

## Models

For the most up to date documentation, view the documetation for the plugin you're using (e.g.
django-autoslug or django-extensions).

To use django-slugify-processor's `slugify` instead of django's default, there will be a field
option to use the function.

### django-extensions

Tested with 1.9.7 (2017-11-26):

```python
from django.db import models

from django_extensions.db.fields import AutoSlugField
from django_slugify_processors.text import slugify

class MyModel(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from='title',
        slugify_function=slugify
    )
```

### django-autoslug

Tested with 1.9.3 (2017-11-26):

```python
from django.db import models

from autoslug import AutoSlugField
from django_slugify_processors.text import slugify

class MyModel(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from='title',
        slugify=slugify
    )
```

# Credits

- tox.ini based off DRF's (BSD 2-clause licensed)
- yapf configuration based off RTD / devel.tech's (MIT-licensed)

# Project details

- python support >= 3.7, pypy3
- django support 2.2, > 3.1,
- Source https://github.com/tony/django-slugify-processor
- Docs https://django-slugify-processor.git-pull.com
- API https://django-slugify-processor.git-pull.com/api.html
- Changelog https://django-slugify-processor.git-pull.com/history.html
- Issues https://github.com/tony/django-slugify-processor/issues
- Test Coverage https://codecov.io/gh/tony/django-slugify-processor
- pypi https://pypi.python.org/pypi/django-slugify-processor
- Open Hub https://www.openhub.net/p/django-slugify-processor
- License MIT
- git repo

  ```bash
  $ git clone https://github.com/tony/django-slugify-processor.git
  ```

## Development

Install stable:

```console
$ pip install django-slugify-processor
```

Local installation:

```console
$ git clone https://github.com/tony/django-slugify-processor.git
```

```console
$ cd ./django-slugify-processor
```

```console
$ poetry shell
```

```console
$ pipenv install
```

Test:

```console
$ make test
```
