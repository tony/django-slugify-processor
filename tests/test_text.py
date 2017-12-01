# -*- coding: utf-8 -*-

from django_slugify_processor.text import slugify
from django.utils.text import slugify as django_slugify


def test_slugify_fallback_to_default():
    assert slugify('c++') == django_slugify('c++')


def slugify_programming(value):
    value = value.replace('c++', 'cpp')
    return value


def test_slugify_slugify_processors(settings):
    settings.SLUGIFY_PROCESSORS = ['tests.test_text.slugify_programming']
    assert slugify('c++') == 'cpp'
