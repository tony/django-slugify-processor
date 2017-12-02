# -*- coding: utf-8 -*-

from django.template.defaultfilters import register, stringfilter

from .text import slugify as _slugify


@register.filter(is_safe=True)
@stringfilter
def slugify(value):
    return _slugify(value)
