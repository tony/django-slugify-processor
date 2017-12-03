# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter

from ..text import slugify as _slugify

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def slugify(value):
    """Template filter intended to override django 1.11+'s default slugify.

    This can be installed via a builtin, or via
    ``{% load slugify_processor %}``.

    Usage in a Django template:

    .. code-block:: django

       {% load slugify_processor %}  {# unless you added it to builtins %}
       {{variable|slugify}}  {# assuming "variable" is in context %}
       {{"C++"|slugify}}
    """

    return _slugify(value)
