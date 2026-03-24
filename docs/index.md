---
hide-toc: true
---

(index)=

# django-slugify-processor

Custom slug processors for Django's `slugify()`.

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install, configure processors, and start slugifying.
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
$ pip install django-slugify-processor
```

```console
$ uv add django-slugify-processor
```

## At a glance

Define a processor function:

```python
def my_processor(value):
    value = value.replace("++", "pp")
    return value
```

Register it in your Django settings:

```python
SLUGIFY_PROCESSORS = [
    "myapp.processors.my_processor",
]
```

Use the drop-in replacement for Django's `slugify`:

```python
from django_slugify_processor.text import slugify

slugify("C++")  # 'cpp'
```

```{toctree}
:hidden:

quickstart
api
project/index
history
GitHub <https://github.com/tony/django-slugify-processor>
```
