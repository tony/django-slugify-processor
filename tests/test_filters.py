"""Test package for django-slugify-processor filters."""

import typing as t

from django.template import Context, Template


def test_slugify_via_builtin_override(settings: t.Any) -> None:
    """Tests for overriding of django template builtins."""
    settings.SLUGIFY_PROCESSORS = ["test_app.coding.slugify_programming"]
    settings.TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "builtins": ["django_slugify_processor.templatetags.slugify_processor"],
            },
        },
    ]

    template = Template("{{'c++'|slugify}}")
    assert template.render(Context({})) == "cpp"


def test_slugify_via_load_templatetags(settings: t.Any) -> None:
    """Tests for using django-slugify-processor via loading template tag."""
    settings.SLUGIFY_PROCESSORS = ["test_app.coding.slugify_programming"]
    settings.INSTALLED_APPS = ["django_slugify_processor"]
    settings.TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        },
    ]

    template = Template('{% load slugify_processor %}{{"c++"|slugify}}')
    assert template.render(Context({})) == "cpp"
