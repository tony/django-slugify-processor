SECRET_KEY = "dummy"

DATABASES = {"default": {"NAME": ":memory:", "ENGINE": "django.db.backends.sqlite3"}}

INSTALLED_APPS = ["test_app"]

USE_TZ = False
