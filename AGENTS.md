# AGENTS.md

This file provides guidance to AI agents (including Claude Code, Cursor, and other LLM-powered tools) when working with code in this repository.

## CRITICAL REQUIREMENTS

### Test Success
- ALL tests MUST pass for code to be considered complete and working
- Never describe code as "working as expected" if there are ANY failing tests
- Even if specific feature tests pass, failing tests elsewhere indicate broken functionality
- Changes that break existing tests must be fixed before considering implementation complete
- A successful implementation must pass linting, type checking, AND all existing tests

## Project Overview

gp-libs is a Python library of internal utilities for git-pull projects. In this repository it powers custom slugification for Django via `django-slugify-processor`, letting projects stack user-defined processors on top of Django's built-in `slugify` function and template filter to handle edge cases (e.g., C++ → cpp, US$ → usd).

Key features:
- Plug-in pipeline of slugify processors defined via `SLUGIFY_PROCESSORS` in Django settings
- Drop-in replacement for Django's `slugify` utility and template filter
- Keeps default Django behavior when no processors are configured
- Compatible with Django 4.2–5.2; tested on Python 3.10+
- Sphinx docs and doctest-friendly examples powered by gp-libs extensions

## Development Environment

This project uses:
- Python 3.10+
- Django 4.2+ (tested through 5.2)
- [uv](https://github.com/astral-sh/uv) for dependency management
- [ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://github.com/python/mypy) for type checking
- [pytest](https://docs.pytest.org/) with [pytest-django](https://pytest-django.readthedocs.io/) for testing
  - [pytest-watcher](https://github.com/olzhasar/pytest-watcher) for continuous testing

## Common Commands

### Setting Up Environment

```bash
# Install dependencies
uv pip install --editable .
uv pip sync

# Install with development dependencies
uv pip install --editable . -G dev
```

### Running Tests

```bash
# Run all tests
just test
# or directly with pytest
uv run py.test

# Run a single test file
uv run py.test tests/test_text.py

# Run a specific test
uv run py.test tests/test_text.py::test_slugify_pipeline

# Run tests with test watcher
just start
# or
uv run ptw .

# Run tests with doctests
uv run ptw . --now --doctest-modules
```

### Linting and Type Checking

```bash
# Run ruff for linting
just ruff
# or directly
uv run ruff check .

# Format code with ruff
just ruff-format
# or directly
uv run ruff format .

# Run mypy for type checking
just mypy
# or directly
uv run mypy `find src tests -name "*.py"`

# Watch mode for linting (using entr)
just watch-ruff
just watch-mypy
```

### Documentation

```bash
# Build documentation
just build-docs

# Start documentation server with auto-reload
just start-docs

# Update documentation CSS/JS
just design-docs
```

## Code Architecture

django-slugify-processor is intentionally small and focused. Core pieces live in `src/django_slugify_processor/`:

1. **text** (`text.py`)
   - Defines `slugify(value, allow_unicode=False)`
   - Loads callables listed in `settings.SLUGIFY_PROCESSORS` (via `import_string`) and runs them in order before delegating to Django's `slugify`
   - Keeps behavior identical to Django when no processors are configured

2. **templatetags** (`templatetags/slugify_processor.py`)
   - Registers a template filter `slugify` that wraps the custom `text.slugify`
   - Can be loaded via `{% load slugify_processor %}` or configured as a builtin filter

3. **Package metadata** (`__about__.py`, `__init__.py`, `py.typed`)
   - Exposes version info and typing support

## Testing Strategy

Tests live in `tests/` and rely on `pytest` + `pytest-django` with `DJANGO_SETTINGS_MODULE=tests.settings` (configured in `pyproject.toml`). Doctests are enabled for modules and documentation files.

Guidelines:
1. Prefer real processor functions and Django settings fixtures over heavy mocking.
2. Keep slugify processor examples minimal and deterministic.
3. When adding docs examples, ensure they work with `pytest --doctest-modules`.
4. Use `uv run ptw .` for tight feedback during iteration.

### Example Fixture Usage

```python
def test_custom_processor(settings):
    settings.SLUGIFY_PROCESSORS = [
        "tests.examples.slugify_programming_languages",
    ]

    from django_slugify_processor.text import slugify

    assert slugify("C++") == "cpp"
```

## Coding Standards

### Imports

- Prefer namespace imports (e.g., `import typing as t`), avoiding `from module import *`
- Include `from __future__ import annotations` at the top of Python files

### Docstrings

Use NumPy-style docstrings for functions and methods:

```python
"""Short description.

Parameters
----------
value : str
    Description.
"""
```

### Doctests

**All functions and methods MUST have working doctests.** Doctests serve as both documentation and tests.

**CRITICAL RULES:**
- Doctests MUST actually execute - never comment out function calls or similar
- Doctests MUST NOT be converted to `.. code-block::` as a workaround (code-blocks don't run)
- If you cannot create a working doctest, **STOP and ask for help**

**Available tools for doctests:**
- `doctest_namespace` fixtures: `tmp_path`
- Django `settings` fixture (from pytest-django)
- Ellipsis for variable output: `# doctest: +ELLIPSIS`
- Update `conftest.py` to add new fixtures to `doctest_namespace`

**`# doctest: +SKIP` is NOT permitted** - it's just another workaround that doesn't test anything. Use fixtures properly.

**Using fixtures in doctests:**
```python
>>> from django_slugify_processor.text import slugify
>>> slugify("Hello World")
'hello-world'
>>> slugify("C++ Programming")  # With processor configured
'cpp-programming'
```

**When output varies, use ellipsis:**
```python
>>> from django.conf import settings
>>> hasattr(settings, 'SLUGIFY_PROCESSORS')  # doctest: +ELLIPSIS
...
```

### Dev Loop (from `.cursor/rules/dev-loop.mdc`)
- Format first: `uv run ruff format .`
- Run tests: `uv run py.test` (or `uv run ptw .` for watch / doctests)
- Lint + auto-fix: `uv run ruff check . --fix --show-fixes`
- Type check: `uv run mypy`
- Re-run tests before finalizing changes

### Git Commit Standards (from `.cursor/rules/git-commits.mdc`)
```
Component/File(commit-type[scope]): Concise description

why: reason
what:
- bullet of concrete change
- bullet of tests/tooling touched
```
Commit types: feat, fix, refactor, docs, chore, test, style, py(deps), py(deps[dev]). Keep subject ≤50 chars; body ≤72 chars/line; imperative mood.

## Debugging Tips (from `.cursor/rules/avoid-debug-loops.mdc`)
- If fixes loop without progress, pause and state the loop.
- Minimize to a smallest reproducible example and drop debugging cruft.
- Document error, reproduction, failed attempts, and hypothesis clearly (quad-backtick block if sharing).

## Notes Formatting (from `.cursor/rules/notes-llms-txt.mdc`)
- Keep notes concise and well-structured with headings/lists.
- Use fenced code blocks for code; avoid repetition; follow llms.txt style when applicable.

## Django-Specific Considerations

- Respect `allow_unicode` flag when extending functionality; do not force ASCII unless intended.
- Processor functions should be pure and idempotent; avoid database or network access.
- Keep template filter behavior aligned with `text.slugify` to prevent divergence between Python and template usage.

## References

- Documentation: https://django-slugify-processor.git-pull.com
- PyPI: https://pypi.org/project/django-slugify-processor/
- Django slugify docs: https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.text.slugify
- gp-libs docs (extensions used in this project): https://gp-libs.git-pull.com
