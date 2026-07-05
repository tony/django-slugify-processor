"""Core functionality for django-slugify-processor."""

from __future__ import annotations

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.text import slugify as django_slugify


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Override Django's default slugify behavior with custom processors.

    Run ``value`` through functions declared in ``SLUGIFY_PROCESSORS``. The
    value then passes to Django's :func:`django.utils.text.slugify`.

    Parameters
    ----------
    value : str
        A value such as an article name or page title to turn into a clean,
        URL-friendly short name.
    allow_unicode : bool
        Whether to allow Unicode characters in Django's final slugification
        step.

    Returns
    -------
    str
        Clean, URL-friendly short name.

    Examples
    --------
    With no processors configured, this matches Django's slugifier:

    >>> from django_slugify_processor.text import slugify
    >>> slugify("c++")
    'c'

    Processors run before Django's final slugification:

    >>> from django.test import override_settings
    >>> with override_settings(
    ...     SLUGIFY_PROCESSORS=["test_app.coding.slugify_programming"],
    ... ):
    ...     slugify("c++")
    'cpp'

    The ``allow_unicode`` flag is passed to Django after processors run:

    >>> with override_settings(
    ...     SLUGIFY_PROCESSORS=["test_app.coding.slugify_programming"],
    ... ):
    ...     slugify("東京 c++", allow_unicode=True)
    '東京-cpp'
    """
    slugify_processors = getattr(settings, "SLUGIFY_PROCESSORS", [])
    for slugify_fn_str in slugify_processors:
        slugify_fn_ = import_string(slugify_fn_str)
        value = slugify_fn_(value)

    return django_slugify(value, allow_unicode)
