from django_slugify_processor.text import slugify
from django.utils.text import slugify as django_slugify


def test_slugify_fallback_to_default():
    assert slugify('c++') == django_slugify('c++')
