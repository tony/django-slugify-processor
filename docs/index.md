---
hide-toc: true
---

(index)=

# django-slugify-processor

Custom slug processors for Django's {func}`slugify() <django.utils.text.slugify>`.
With no `SLUGIFY_PROCESSORS` setting, django-slugify-processor keeps Django's
default slug behavior, so you can add processors only when a term needs special
handling.

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install, learn the pipeline, and start slugifying.
:::

:::{grid-item-card} API Reference
:link: api
:link-type: doc
Every public function and template filter.
:::

:::{grid-item-card} Contributing
:link: project/index
:link-type: doc
Development setup, code style, release process.
:::

::::

## Install

```console
$ python -m pip install django-slugify-processor
```

```console
$ uv add django-slugify-processor
```

## At a glance

Define a processor function that rewrites the text before Django finishes the
slug:

```{doctest}
>>> def my_processor(value: str) -> str:
...     return value.replace("C++", "Cpp")
>>> my_processor("C++")
'Cpp'
```

Register the processor's import string in your
[Django settings](https://docs.djangoproject.com/en/4.2/topics/settings/):

```python
SLUGIFY_PROCESSORS = [
    "myapp.processors.my_processor",
]
```

Use the drop-in {func}`~django_slugify_processor.text.slugify` replacement:

```{doctest}
>>> from django.test import override_settings
>>> from django_slugify_processor.text import slugify
>>> with override_settings(
...     SLUGIFY_PROCESSORS=["test_app.coding.slugify_programming_languages"],
... ):
...     slugify("C++")
'cpp'
```

```{toctree}
:hidden:

quickstart
api
project/index
history
GitHub <https://github.com/tony/django-slugify-processor>
```
