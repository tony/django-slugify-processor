# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter

from ..text import slugify as _slugify

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def slugify(value):
    return _slugify(value)
