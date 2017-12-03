# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.text import slugify as django_slugify


def slugify(value, allow_unicode=False):
    """Override default slugify in django to handle custom scenarios.

    Run value through functions declared in SLUGIFY_PROCESSORS. The value is
    then passed-through to django's slugify.

    :param value: string to slugify
    :type value: string
    :param allow_unicode: whether or not to allow unicode (e.g. chinese)
    :type allow_unicode: bool

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
    if hasattr(settings, 'SLUGIFY_PROCESSORS'):
        for slugify_fn_str in settings.SLUGIFY_PROCESSORS:
            slugify_fn_ = import_string(slugify_fn_str)
            value = slugify_fn_(value)

    return django_slugify(value, allow_unicode)
