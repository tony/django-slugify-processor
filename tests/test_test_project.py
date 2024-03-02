"""Tests using django test app for django-slugify-processor."""

import typing as t

import pytest
from django.apps import apps


@pytest.mark.django_db
def test_models_passthrough(settings: t.Any) -> None:
    """django-slugify-processor defaults to django's behavior if not set."""
    MyModel = apps.get_model("test_app.MyModel")
    entered = "c++"
    expected = "c"

    m = MyModel(title=entered)
    m.save()

    assert m.django_extensions_slug == expected


@pytest.mark.django_db
def test_models(settings: t.Any) -> None:
    """django-slugify-processor uses SLUGIFY_PROCESSORS if set."""
    settings.SLUGIFY_PROCESSORS = ["test_app.coding.slugify_programming"]
    MyModel = apps.get_model("test_app.MyModel")
    entered = "c++"
    expected = "cpp"

    m = MyModel(title=entered)
    m.save()

    assert m.django_extensions_slug == expected
