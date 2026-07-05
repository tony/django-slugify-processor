(api)=

# API Reference

## Processor Pipeline

`SLUGIFY_PROCESSORS` is a Django setting containing dotted import strings. Each
string must resolve through {func}`django.utils.module_loading.import_string` to
a callable that accepts a `str` and returns a `str`.

Processors run in list order for every {func}`~django_slugify_processor.text.slugify`
call. Each processor receives the previous processor's output, then the final
value passes to {func}`django.utils.text.slugify` with the caller's
`allow_unicode` value.

Keep processors pure and inexpensive. A processor should not depend on request
state, database writes, or network calls because slugification can run inside
model-field saves, template rendering, and bulk import jobs.

## Slugify function

```{eval-rst}
.. autofunction:: django_slugify_processor.text.slugify
```

## Template filter

The template filter delegates to {func}`~django_slugify_processor.text.slugify`
with its default `allow_unicode=False` behavior. Load it explicitly with
`{% load slugify_processor %}`, or install
`django_slugify_processor.templatetags.slugify_processor` as a template builtin
when the whole template engine should shadow Django's built-in `slugify` filter.

```{eval-rst}
.. autofunction::
    django_slugify_processor.templatetags.slugify_processor.slugify
```

## Package metadata

```{eval-rst}
.. autodata:: django_slugify_processor.__version__
```
