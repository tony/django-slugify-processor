"""Django settings module for django-slugify-processor tests."""

import os
import typing as t

SECRET_KEY: str = os.getenv("SECRET_KEY", "dummy")

DATABASES: t.Dict[str, t.Any] = {
    "default": {"NAME": ":memory:", "ENGINE": "django.db.backends.sqlite3"},
}

INSTALLED_APPS: t.List[str] = ["test_app"]

USE_TZ: bool = False
