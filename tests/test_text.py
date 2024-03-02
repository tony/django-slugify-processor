"""Tests for django-slugify-processor's text utilities."""

import typing as t

from django.utils.text import slugify as django_slugify

from django_slugify_processor.text import slugify


def test_slugify_fallback_to_default() -> None:
    """Assert slugify() falls back to django's behavior."""
    assert slugify("c++") == django_slugify("c++")


def test_slugify_slugify_processors(settings: t.Any) -> None:
    """Assert slugify() follows SLUGIFY_PROCESSORS."""
    settings.SLUGIFY_PROCESSORS = ["test_app.coding.slugify_programming"]
    assert slugify("c++") == "cpp"
