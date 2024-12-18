"""Django settings module for django-slugify-processor tests."""

import os
import typing as t

SECRET_KEY: str = os.getenv("SECRET_KEY", "dummy")

DATABASES: dict[str, t.Any] = {
    "default": {"NAME": ":memory:", "ENGINE": "django.db.backends.sqlite3"},
}

INSTALLED_APPS: list[str] = ["test_app"]

USE_TZ: bool = False
