"""Slugify django template filter."""

from django import template
from django.template.defaultfilters import stringfilter

from django_slugify_processor.text import slugify as _slugify

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def slugify(value: str) -> str:
    """Template filter override for Django's :func:`django.utils.text.slugify()`.

    Can be installed via a builtin, or via ``{% load slugify_processor %}``.

    Parameters
    ----------
    value : str
        A value such as an article name or page title, to "slugify", (turn into a
        clean, URL-friendly short name)

    Returns
    -------
    str
        Clean, URL-friendly short name (a.k.a. "slug") of a string (e.g. a page or
        article name).

    Examples
    --------
    Usage in a Django template:

    .. code-block:: django

       {% load slugify_processor %}
       {{ variable|slugify }}
       {{ "C++"|slugify }}
    """
    return _slugify(value)
