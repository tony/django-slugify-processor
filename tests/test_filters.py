# -*- coding: utf-8 -*-
from django.template import Context, Template


def test_slugify_engine_override(settings):
    settings.SLUGIFY_PROCESSORS = ['tests.test_text.slugify_programming']
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'builtins': [
                    'django_slugify_processor.filters'
                ],
                'context_processors': [
                    'django.template.context_processors.request',
                ]
            },
        },
    ]

    template = Template("{{'c++'|slugify}}")
    assert template.render(Context({})) == 'cpp'
