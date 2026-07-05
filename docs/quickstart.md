(quickstart)=

# Quickstart

django-slugify-processor lets you run small text processors before Django's
{func}`slugify() <django.utils.text.slugify>` finishes a slug. If you do not
configure `SLUGIFY_PROCESSORS`, {func}`~django_slugify_processor.text.slugify`
behaves like Django's function, so you can swap imports first and add processors
only when a term needs special handling.

## Installation

Add django-slugify-processor to the Python environment that runs your Django
project.

With [pip]:

```console
$ python -m pip install django-slugify-processor
```

With [uv]:

```console
$ uv add django-slugify-processor
```

Upgrade an existing environment with [pip]:

```console
$ python -m pip install --upgrade django-slugify-processor
```

Upgrade an existing [uv] dependency:

```console
$ uv add \
    --upgrade-package django-slugify-processor \
    django-slugify-processor
```

## Usage

A processor is a function that takes a string and returns a string. Each
function in `SLUGIFY_PROCESSORS` runs in order, then Django's
{func}`~django.utils.text.slugify` turns the final value into a slug.

Start with the term you need to preserve. This processor makes `C++` become
`Cpp` before Django strips punctuation:

```{doctest}
>>> def slugify_programming_languages(value: str) -> str:
...     return value.replace("C++", "Cpp").replace("C#", "CSharp")
>>> slugify_programming_languages("C++ Programming")
'Cpp Programming'
```

Add the processor's import string to your [Django settings]. Django resolves the
string with {func}`django.utils.module_loading.import_string`.

```python
SLUGIFY_PROCESSORS = [
    "myapp.slugify_processors.slugify_programming_languages",
]
```

Use {func}`~django_slugify_processor.text.slugify` anywhere you would use
Django's function. This tested example uses the repository's `test_app`
processor; in an application, point `SLUGIFY_PROCESSORS` at your own module.

```{doctest}
>>> from django.test import override_settings
>>> from django_slugify_processor.text import slugify
>>> with override_settings(
...     SLUGIFY_PROCESSORS=["test_app.coding.slugify_programming_languages"],
... ):
...     slugify("C++ Programming")
'cpp-programming'
```

Processors should stay pure and fast. The list is read for each slugification
call, each import string is resolved with Django's import helper, and each
processor receives the previous processor's output.

## Templates

For templates, load the
{func}`template filter <django_slugify_processor.templatetags.slugify_processor.slugify>`
when you want this pipeline in one template:

```{doctest}
>>> from django.template import Context, Template
>>> from django.test import override_settings
>>> with override_settings(
...     INSTALLED_APPS=[
...         "django.contrib.contenttypes",
...         "django.contrib.auth",
...         "test_app",
...         "django_slugify_processor",
...     ],
...     TEMPLATES=[
...         {
...             "BACKEND": "django.template.backends.django.DjangoTemplates",
...             "APP_DIRS": True,
...         },
...     ],
...     SLUGIFY_PROCESSORS=["test_app.coding.slugify_programming_languages"],
... ):
...     Template(
...         '{% load slugify_processor %}{{ "C++ Programming"|slugify }}',
...     ).render(Context({}))
'cpp-programming'
```

For the rarer cases where every template should use this filter, install
`django_slugify_processor.templatetags.slugify_processor` as a template builtin.
That shadows Django's `slugify` filter across the configured template engine, so
reserve it for projects that want the same slug rules everywhere.

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

## Model Fields

For model fields, pass {func}`~django_slugify_processor.text.slugify` to a field
option such as django-extensions'
[AutoSlugField `slugify_function`](https://django-extensions.readthedocs.io/en/latest/field_extensions.html)
or [django-autoslug](https://pypi.org/project/django-autoslug/)'s
`AutoSlugField` `slugify` argument.

```python
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_slugify_processor.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", slugify_function=slugify)
```

(developmental-releases)=

## Advanced: Developmental Releases

New versions of django-slugify-processor are published to [PyPI] as alpha, beta,
or release candidates. In their versions you will see labels like `a1`, `b1`,
and `rc1`; `1.10.0b4` means the fourth beta release of `1.10.0` before general
availability.

Install the latest prerelease with [pip]:

```console
$ python -m pip install --upgrade --pre django-slugify-processor
```

Or allow prereleases in a [uv] project dependency:

```console
$ uv add \
    --prerelease allow \
    django-slugify-processor
```

Use trunk only when you need unreleased changes; it can break without notice.

With [pip]:

```console
$ python -m pip install \
    --upgrade \
    'django-slugify-processor @ git+https://github.com/tony/django-slugify-processor.git'
```

With [uv]:

```console
$ uv add \
    'django-slugify-processor @ git+https://github.com/tony/django-slugify-processor.git'
```

[django settings]: https://docs.djangoproject.com/en/4.2/topics/settings/
[pip]: https://pip.pypa.io/en/stable/
[pypi]: https://pypi.org/project/django-slugify-processor/
[uv]: https://docs.astral.sh/uv/
