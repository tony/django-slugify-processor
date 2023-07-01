import django_extensions.db.fields
from django.db import models

from django_slugify_processor.text import slugify


class MyModel(models.Model):
    title = models.CharField(max_length=255)
    django_extensions_slug = django_extensions.db.fields.AutoSlugField(
        populate_from="title", slugify_function=slugify
    )
