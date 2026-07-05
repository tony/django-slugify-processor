# django-slugify-processor

Custom slug processors for Django's
[`slugify()`](https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.text.slugify).

[![Python Package](https://img.shields.io/pypi/v/django-slugify-processor.svg)](https://pypi.org/project/django-slugify-processor/)
[![Build Status](https://github.com/tony/django-slugify-processor/workflows/tests/badge.svg)](https://django-slugify-processor.git-pull.com/)
[![Docs](https://github.com/tony/django-slugify-processor/workflows/docs/badge.svg)](https://github.com/tony/django-slugify-processor/actions?query=workflow%3Adocs)
[![Code Coverage](https://codecov.io/gh/tony/django-slugify-processor/branch/master/graph/badge.svg)](https://codecov.io/gh/tony/django-slugify-processor)
[![License](https://img.shields.io/github/license/tony/django-slugify-processor.svg)](https://github.com/tony/django-slugify-processor/blob/master/LICENSE)

## Why

Django's slugifier is intentionally generic. That means terms such as `C++` and
`C#` both collapse to `c`, which can produce duplicate or unhelpful slugs.
django-slugify-processor lets a project run its own small processors before
Django performs the final slugification step.

With no `SLUGIFY_PROCESSORS` setting, the package behaves like Django's
`slugify()`.

## Install

```console
$ python -m pip install django-slugify-processor
```

```console
$ uv add django-slugify-processor
```

## Configure

Create a processor that accepts a string and returns a string:

```python
def slugify_programming_languages(value: str) -> str:
    return value.replace("C++", "Cpp").replace("C#", "CSharp")
```

Register the processor's import string in Django settings:

```python
SLUGIFY_PROCESSORS = [
    "myapp.slugify_processors.slugify_programming_languages",
]
```

Processors run in list order. The result then passes through Django's own
`slugify()`, including its `allow_unicode` handling.

## Use

Use the Python helper anywhere you would use Django's slugifier:

```python
from django_slugify_processor.text import slugify

slugify("C++ Programming")  # "cpp-programming"
```

Load the template filter in a template that needs the same pipeline:

```django
{% load slugify_processor %}
{{ "C++ Programming"|slugify }}
```

For projects that want every template to use this filter, install it as a
template builtin:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "builtins": [
                "django_slugify_processor.templatetags.slugify_processor",
            ],
        },
    },
]
```

Model-field packages usually accept a slugify callback. For django-extensions:

```python
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_slugify_processor.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", slugify_function=slugify)
```

For django-autoslug, pass the same function to its `slugify` option.

## Links

- Documentation: https://django-slugify-processor.git-pull.com
- API reference: https://django-slugify-processor.git-pull.com/api.html
- Changelog: https://django-slugify-processor.git-pull.com/history.html
- Source: https://github.com/tony/django-slugify-processor
- Issues: https://github.com/tony/django-slugify-processor/issues
- PyPI: https://pypi.org/project/django-slugify-processor/

## Development

```console
$ git clone https://github.com/tony/django-slugify-processor.git
```

```console
$ cd django-slugify-processor
```

```console
$ uv sync --all-extras --dev
```

```console
$ just test
```
