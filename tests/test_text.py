from django.utils.text import slugify as django_slugify

from django_slugify_processor.text import slugify


def test_slugify_fallback_to_default():
    assert slugify("c++") == django_slugify("c++")


def test_slugify_slugify_processors(settings):
    settings.SLUGIFY_PROCESSORS = ["test_app.coding.slugify_programming"]
    assert slugify("c++") == "cpp"
