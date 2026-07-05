"""Tests for django-slugify-processor's text utilities."""

from __future__ import annotations

import typing as t

import pytest
from django.utils.text import slugify as django_slugify

from django_slugify_processor.text import slugify


class SlugifyCase(t.NamedTuple):
    """Slugify behavior test case."""

    test_id: str
    value: str
    processors: tuple[str, ...]
    allow_unicode: bool
    expected: str


SLUGIFY_CASES = (
    SlugifyCase(
        test_id="fallback-ascii",
        value="c++",
        processors=(),
        allow_unicode=False,
        expected=django_slugify("c++"),
    ),
    SlugifyCase(
        test_id="single-processor",
        value="c++",
        processors=("test_app.coding.slugify_programming",),
        allow_unicode=False,
        expected="cpp",
    ),
    SlugifyCase(
        test_id="processor-order",
        value="C++ Guide",
        processors=(
            "test_app.coding.slugify_programming_languages",
            "test_app.coding.slugify_language_suffix",
        ),
        allow_unicode=False,
        expected="cpp-language-guide",
    ),
    SlugifyCase(
        test_id="unicode-pass-through-without-processors",
        value="東京 c++",
        processors=(),
        allow_unicode=True,
        expected=django_slugify("東京 c++", allow_unicode=True),
    ),
    SlugifyCase(
        test_id="unicode-pass-through-with-processor",
        value="東京 c++",
        processors=("test_app.coding.slugify_programming",),
        allow_unicode=True,
        expected="東京-cpp",
    ),
)


@pytest.mark.parametrize(
    "case",
    SLUGIFY_CASES,
    ids=[case.test_id for case in SLUGIFY_CASES],
)
def test_slugify_pipeline_cases(settings: t.Any, case: SlugifyCase) -> None:
    """Assert slugify() applies processors before Django's final slugifier."""
    settings.SLUGIFY_PROCESSORS = list(case.processors)
    assert slugify(case.value, allow_unicode=case.allow_unicode) == case.expected
