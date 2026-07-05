(quickstart)=

# Quickstart

django-slugify-processor lets you run small text processors before Django's
{func}`slugify() <django.utils.text.slugify>` finishes a slug. If you do not
configure `SLUGIFY_PROCESSORS`, {func}`~django_slugify_processor.text.slugify`
behaves like Django's function, so you can swap imports first and add processors
only when a term needs special handling.

## Installation

Install the latest official version from [PyPI]:

```console
$ pip install --user django-slugify-processor
```

Or use [uv]:

```console
$ uv tool install django-slugify-processor
```

Upgrade with [pip]:

```console
$ pip install --user --upgrade django-slugify-processor
```

Or with [uv]:

```console
$ uv tool upgrade django-slugify-processor
```

(developmental-releases)=

### Developmental releases

New versions of django-slugify-processor are published to [PyPI] as alpha, beta,
or release candidates. In their versions you will see labels like `a1`, `b1`,
and `rc1`; `1.10.0b4` means the fourth beta release of `1.10.0` before general
availability.

- [pip]\:

  ```console
  $ pip install --user --upgrade --pre django-slugify-processor
  ```

- [pipx]\:

  ```console
  $ pipx install \
      --suffix=@next \
      --pip-args '\--pre' \
      --force \
      'django-slugify-processor'
  ```

- [uv tool install][uv-tools]\:

  ```console
  $ uv tool install --prerelease=allow django-slugify-processor
  ```

- [uv]\:

  ```console
  $ uv add django-slugify-processor --prerelease allow
  ```

- [uvx]\:

  ```console
  $ uvx \
      --from 'django-slugify-processor' \
      --prerelease allow \
      django-slugify-processor
  ```

Use trunk only when you need unreleased changes; it can break without notice.

- [pip]\:

  ```console
  $ pip install \
      --user \
      -e git+https://github.com/tony/django-slugify-processor.git#egg=django-slugify-processor
  ```

- [pipx]\:

  ```console
  $ pipx install \
      --suffix=@master \
      --force \
      'django-slugify-processor @ git+https://github.com/tony/django-slugify-processor.git@master'
  ```

- [uv]\:

  ```console
  $ uv tool install \
      django-slugify-processor \
      --from git+https://github.com/tony/django-slugify-processor.git
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
[pypi]: https://pypi.org/project/django-slugify-processor/
[uv]: https://docs.astral.sh/uv/
[uv-tools]: https://docs.astral.sh/uv/concepts/tools/
[uvx]: https://docs.astral.sh/uv/guides/tools/

## Usage

A processor is a function that takes a string and returns a string. Each
function in `SLUGIFY_PROCESSORS` runs in order, then Django's
{func}`~django.utils.text.slugify` turns the final value into a slug.

Create a processor for the term you need to preserve:

```python
def slugify_programming_languages(value: str) -> str:
    return value.replace("C++", "Cpp").replace("C#", "CSharp")
```

Add the processor's import string to your [Django settings]. Django resolves the
string with {func}`django.utils.module_loading.import_string`.

```python
SLUGIFY_PROCESSORS = [
    "myapp.slugify_processors.slugify_programming_languages",
]
```

Use {func}`~django_slugify_processor.text.slugify` anywhere you would use
Django's function:

```python
from django_slugify_processor.text import slugify

slugify("C++ Programming")
```

For templates, load the
{func}`template filter <django_slugify_processor.templatetags.slugify_processor.slugify>`
when you want this pipeline in one template:

```django
{% load slugify_processor %}
{{ "C++ Programming"|slugify }}
```

For the rarer cases where every template should use this filter, install
`django_slugify_processor.templatetags.slugify_processor` as a template builtin.
That shadows Django's `slugify` filter across the configured template engine, so
reserve it for projects that want the same slug rules everywhere.

For model fields, pass {func}`~django_slugify_processor.text.slugify` to a field
option such as django-extensions'
[AutoSlugField `slugify_function`](https://django-extensions.readthedocs.io/en/latest/field_extensions.html)
or [django-autoslug](https://pypi.org/project/django-autoslug/)'s
`AutoSlugField` `slugify` argument.

[django settings]: https://docs.djangoproject.com/en/4.2/topics/settings/
