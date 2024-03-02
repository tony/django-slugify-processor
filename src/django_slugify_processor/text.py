"""Core functionality for django-slugify-processor."""

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.text import slugify as django_slugify


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Override default slugify in django to handle custom scenarios.

    Run value through functions declared in ``SLUGIFY_PROCESSORS`` setting. The value is
    then passed-through to Django's :func:`django.utils.text.slugify()`.

    Parameters
    ----------
    value : str
        A value such as an article name or page title, to "slugify", (turn into a
        clean, URL-friendly short name)
    allow_unicode : bool
        Whether or not to allow unicode (e.g. chinese).

    Returns
    -------
    str
        Clean, URL-friendly short name (a.k.a. "slug") of a string (e.g. a page or
        article name).

    Examples
    --------
    Examples of slugify processors, assume *project/app/slugify_processors.py*:

    .. code-block:: python

        def slugify_programming_languages(value):
            value = value.lower()

            value = value.replace('c++', 'cpp')
            value = value.replace('c#', 'c-sharp')
            return value

        def slugify_geo_acronyms(value):
            value = value.lower()

            value = value.replace('New York City', 'nyc')
            value = value.replace('United States', 'usa')
            return value

        def slugify_us_currency(value):
            value = value.lower()

            value = value.replace('$', 'usd')
            value = value.replace('US$', 'usd')
            value = value.replace('US Dollar', 'usd')
            value = value.replace('U.S. Dollar', 'usd')
            return value

    Settings:

    .. code-block:: python

        SLUGIFY_PROCESSORS = [
            'project.app.slugify_programming_languages',
            'project.app.slugify_geo_acronyms',
            'project.app.slugify_us_currency',
        ]
    """
    slugify_processors = getattr(settings, "SLUGIFY_PROCESSORS", [])
    for slugify_fn_str in slugify_processors:
        slugify_fn_ = import_string(slugify_fn_str)
        value = slugify_fn_(value)

    return django_slugify(value, allow_unicode)
