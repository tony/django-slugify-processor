# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.text import slugify as django_slugify


def slugify(value, allow_unicode=False):
    """Override default slugify in django to handle programming symbols.

    :param value: string to slugify
    :type value: string
    :param allow_unicode: whether or not to allow unicode (e.g. chinese)
    :type allow_unicode: bool

    How to slugify filters:

        def slugify_programming_languages(value):
            value = value.lower()

            value = value.replace('c++', 'cpp')
            value = value.replace('c#', 'c-sharp')
            return value

    Settings:

        SLUGIFY_PROCESSORS = [
            'develtech.path.to.slugify_programming_languages'
        ]
    """
    if hasattr(settings, 'SLUGIFY_PROCESSORS'):
        for slugify_fn_str in settings.SLUGIFY_PROCESSORS:
            slugify_fn_ = import_string(slugify_fn_str)
            value = slugify_fn_(value)

    return django_slugify(value, allow_unicode)
