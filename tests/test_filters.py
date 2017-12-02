# -*- coding: utf-8 -*-
from django.template import Context, Template


def test_slugify_engine_override(settings):
    settings.SLUGIFY_PROCESSORS = ['tests.test_text.slugify_programming']
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'builtins': [
                    'django_slugify_processor.templatetags.slugify_processor'
                ],
            },
        },
    ]

    template = Template("{{'c++'|slugify}}")
    assert template.render(Context({})) == 'cpp'


def test_slugify_via_load_tag(settings):
    settings.SLUGIFY_PROCESSORS = ['tests.test_text.slugify_programming']
    settings.INSTALLED_APPS = ['django_slugify_processor']
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ]

    template = Template('{% load slugify_processor %}{{"c++"|slugify}}')
    assert template.render(Context({})) == 'cpp'
