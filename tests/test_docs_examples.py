"""Regression tests for documentation examples and commands."""

from __future__ import annotations

import pathlib
import subprocess
import typing as t

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]


class DocsInstallCase(t.NamedTuple):
    """Documentation install-command test case."""

    test_id: str
    path: pathlib.Path
    section_marker: str | None
    forbidden_commands: tuple[str, ...]


DOCS_INSTALL_CASES = (
    DocsInstallCase(
        test_id="quickstart-library-install",
        path=PROJECT_ROOT / "docs" / "quickstart.md",
        section_marker=None,
        forbidden_commands=("$ uv tool", "$ pipx", "$ uvx"),
    ),
    DocsInstallCase(
        test_id="unreleased-changelog-library-install",
        path=PROJECT_ROOT / "CHANGES",
        section_marker="## django-slugify-processor 1.10.0 (2025-11-01)",
        forbidden_commands=("$ pipx", "$ uvx"),
    ),
)


@pytest.mark.parametrize(
    "case",
    DOCS_INSTALL_CASES,
    ids=[case.test_id for case in DOCS_INSTALL_CASES],
)
def test_library_install_docs_do_not_recommend_tool_installers(
    case: DocsInstallCase,
) -> None:
    """Assert library install docs do not use Python tool-runner commands."""
    text = case.path.read_text()
    if case.section_marker is not None:
        assert case.section_marker in text
        text = text.split(case.section_marker, maxsplit=1)[0]

    for forbidden_command in case.forbidden_commands:
        assert forbidden_command not in text


def test_sphinx_doctest_builder_runs() -> None:
    """Assert docs/ doctest examples run without requiring external just."""
    completed = subprocess.run(
        [
            "uv",
            "run",
            "sphinx-build",
            "-b",
            "doctest",
            "-d",
            "_build/doctrees",
            ".",
            "_build/doctest",
        ],
        check=False,
        cwd=PROJECT_ROOT / "docs",
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stdout
