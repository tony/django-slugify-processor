"""Example slug function for django-slugify-processor tests."""

from __future__ import annotations


def slugify_programming(value: str) -> str:
    """Replace c++ with cpp.

    Examples
    --------
    >>> slugify_programming("c++")
    'cpp'
    """
    return value.replace("c++", "cpp")


def slugify_programming_languages(value: str) -> str:
    """Replace common language names before Django finishes the slug.

    Examples
    --------
    >>> slugify_programming_languages("C++ and C#")
    'Cpp and CSharp'
    """
    return value.replace("C++", "Cpp").replace("C#", "CSharp")


def slugify_language_suffix(value: str) -> str:
    """Append a language suffix after the programming-language processor.

    Examples
    --------
    >>> slugify_language_suffix("Cpp Guide")
    'Cpp Language Guide'
    """
    return value.replace("Cpp", "Cpp Language").replace("cpp", "cpp language")
