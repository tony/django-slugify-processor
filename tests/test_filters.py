from django.template import Context, Template


def test_slugify_via_builtin_override(settings):
    settings.SLUGIFY_PROCESSORS = ["test_app.coding.slugify_programming"]
    settings.TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "builtins": ["django_slugify_processor.templatetags.slugify_processor"]
            },
        }
    ]

    template = Template("{{'c++'|slugify}}")
    assert template.render(Context({})) == "cpp"


def test_slugify_via_load_templatetags(settings):
    settings.SLUGIFY_PROCESSORS = ["test_app.coding.slugify_programming"]
    settings.INSTALLED_APPS = ["django_slugify_processor"]
    settings.TEMPLATES = [
        {"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}
    ]

    template = Template('{% load slugify_processor %}{{"c++"|slugify}}')
    assert template.render(Context({})) == "cpp"
