"""Example slug function for django-slugify-processor tests."""


def slugify_programming(value: str) -> str:
    """Replace c++ with cpp (URL safe)."""
    return value.replace("c++", "cpp")
