# Contributing

Thanks for looking. A bug report with a minimal reproduction — the input
string, the `SLUGIFY_PROCESSORS` configured (if any), and the slug you
expected — is the most useful thing to send.

How this project writes prose — README, `CHANGES`, commit messages,
docstrings, and source comments — is set out separately in
[WRITING.md](WRITING.md). Read that before changing any of it. The
constraints every change is held to, and the map of what is where, are in
[AGENTS.md](../AGENTS.md).

## Getting set up

You need [git] and [uv]. Install uv from the
[installation documentation] if it is not already available.

Clone the repository:

```console
$ git clone https://github.com/tony/django-slugify-processor.git
```

```console
$ cd django-slugify-processor
```

Install packages:

```console
$ uv sync --all-extras --dev
```

[git]: https://git-scm.com/
[installation documentation]: https://docs.astral.sh/uv/getting-started/installation/
[uv]: https://github.com/astral-sh/uv

## The gates

Run them in this order: format, test, lint with fixes, type-check, then
test again before finalizing a change.

Format:

```console
$ uv run ruff format .
```

Lint:

```console
$ uv run ruff check . --fix --show-fixes
```

Type-check:

```console
$ uv run mypy
```

Test:

```console
$ uv run py.test
```

Or use the [just][just-systems] helper for the same four:

```console
$ just ruff-format
```

```console
$ just ruff
```

```console
$ just mypy
```

```console
$ just test
```

Documentation is a gate, not a courtesy. Docstring examples under `src/`,
and `>>> ` sessions on `docs/` pages, are executed by `pytest`; the doctest
flags live in `pyproject.toml`, so there is no separate doctest step and a
green `uv run py.test` is the proof. Which blocks qualify, and the one
mistake that silently removes a test, are in
[WRITING.md](WRITING.md#documented-examples-that-run).

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

CI (`.github/workflows/tests.yml`) is the order of record: it runs
`ruff check .`, `ruff format . --check`, `mypy .`, and
`py.test --cov=./ --cov-report=xml` across the Python/Django matrix. Every
gate it runs has to pass before a change is done.

### Code style

[ruff] handles linting, formatting, and import sorting; [mypy] runs in
`strict` mode (`pyproject.toml`, `[tool.mypy]`). Namespace imports
(`import typing as t`) are preferred over `from module import *`, and every
module opens with `from __future__ import annotations` — ruff's isort
config (`required-imports`) enforces the latter automatically. Docstrings
follow one enforced dialect (NumPy, via `ruff`'s `pydocstyle` rules); see
[WRITING.md](WRITING.md#docstrings) for what to put in them.

[ruff]: https://ruff.rs
[mypy]: http://mypy-lang.org/
[just-systems]: https://just.systems/

## Tests

Tests live in `tests/` and run under `pytest` with `pytest-django`, using
`DJANGO_SETTINGS_MODULE=tests.settings` (set in `pyproject.toml`; the
module itself is `tests/settings.py`). There is no `conftest.py` anywhere
in this repository, so there are no project-specific fixtures — tests use
pytest-django's built-in `settings` fixture directly to set
`SLUGIFY_PROCESSORS`, `INSTALLED_APPS`, or `TEMPLATES` per test, and
`@pytest.mark.django_db` on tests that touch a model.

`test_app/` at the repository root is an example Django app — `models.py`
has a model with an `AutoSlugField`, `coding.py` has the example processor
functions (`slugify_programming`, `slugify_programming_languages`,
`slugify_language_suffix`) that both `tests/` and the `docs/` examples
import. `pythonpath = ". tests"` in `pyproject.toml` puts the repository
root and `tests/` on `sys.path`, which is what makes
`test_app.coding.slugify_programming_languages` and `tests.settings`
importable.

Run the full suite directly:

```console
$ uv run py.test
```

Run one file:

```console
$ uv run py.test tests/test_text.py
```

Automatically rerun tests on save with [pytest-watcher]:

```console
$ just start
```

Or with [entr(1)]:

```console
$ just watch-test
```

If a fix loops without progress, stop and say so. Minimize to the smallest
reproduction, drop debugging cruft, and document the error, the
reproduction, what you already tried, and your current hypothesis before
continuing.

[pytest-watcher]: https://github.com/olzhasar/pytest-watcher
[entr(1)]: http://eradman.com/entrproject/

## Documentation

Default preview server: http://localhost:8030. [sphinx-autobuild] builds
the docs, watches for file changes, and serves them.

From the repository root:

```console
$ just start-docs
```

From inside `docs/`:

```console
$ just start
```

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

Build once without a server:

```console
$ just build-docs
```

Rebuild on file change (requires [entr(1)]):

```console
$ just watch-docs
```

Two pages are generated and must not be hand-edited: `docs/history.md`
`{include}`s `CHANGES` directly — edit `CHANGES`. The signatures and
docstring bodies on `docs/api.md` come from `autofunction`/`autodata`
directives reading `src/` — edit the docstring, not the page, for
anything under one of those directives; the surrounding prose on that page
is hand-written and stays hand-written.

`just build-docs` catches a broken cross-reference; running the tests does
not — build the docs before committing a change that touches one. See
[WRITING.md](WRITING.md#cross-references) for the MyST roles this project
uses.

## Releasing

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow. See
[Release commits](WRITING.md#release-commits).

Releases publish to [PyPI](https://pypi.org/project/django-slugify-processor/)
via [OIDC trusted publishing](https://docs.pypi.org/trusted-publishers/)
from the `release` job in `.github/workflows/tests.yml`, triggered by a
pushed tag. Update
`__version__` in `src/django_slugify_processor/__about__.py` and `version`
in `pyproject.toml`, then commit:

```console
$ git commit -m 'Tag vX.Y.Z'
```

The owner pushes the commit and the tag; CI builds and publishes from
there. The full checklist is in
[docs/project/releasing.md](../docs/project/releasing.md).

## Pull requests

One subject per pull request. Unrelated cleanup found along the way
belongs in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

A pull request merges once it has the sign-off of one other developer. If
you do not have merge permission, ask a maintainer to merge it for you.

Commit format is in [WRITING.md](WRITING.md#commits).

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on [Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).

## Security

Please do not open a public issue for a vulnerability. This repository has
no `SECURITY.md`; report privately through GitHub's security advisories
for this repository, or reach the maintainer through the contact listed in
`pyproject.toml`.
