"""Slugify django template filter."""

from __future__ import annotations

from django import template
from django.template.defaultfilters import stringfilter

from django_slugify_processor.text import slugify as _slugify

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def slugify(value: str) -> str:
    """Template filter override for Django's :func:`django.utils.text.slugify`.

    Install via a template builtin, or load with ``{% load slugify_processor %}``.

    Parameters
    ----------
    value : str
        A value such as an article name or page title to turn into a clean,
        URL-friendly short name.

    Returns
    -------
    str
        Clean, URL-friendly short name.

    Examples
    --------
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
    ...         '{% load slugify_processor %}{{ "C++ Guide"|slugify }}',
    ...     ).render(Context({}))
    'cpp-guide'
    """
    return _slugify(value)
