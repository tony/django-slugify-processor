# Development

You need [git] and [uv] to work on django-slugify-processor. Install uv from the
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

## Codebase Map

The slugification behavior lives in `src/django_slugify_processor/text.py`.
Template integration lives in
`src/django_slugify_processor/templatetags/slugify_processor.py`, which delegates
to the same Python helper so templates and Python code do not diverge.

Tests live in `tests/`, with importable example processors in `test_app/`.
Documentation pages live in `docs/`; API pages are generated from docstrings,
and runnable docs examples are checked by the `docs/` doctest recipe.

## Tests

Run the test suite directly:

```console
$ uv run py.test
```

Or use the [just] helper:

```console
$ just test
```

## Automatically run tests on file save

Use [pytest-watcher]:

```console
$ just start
```

Or use [entr(1)]:

```console
$ just watch-test
```

## Documentation

Default preview server: http://localhost:8034

[sphinx-autobuild] will automatically build the docs, watch for file changes and launch a server.

From the repository root:

```console
$ just start-docs
```

From inside `docs/`:

```console
$ just start
```

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

### Manual documentation (the hard way)

Build from inside `docs/`:

```console
$ cd docs && just html
```

Start the documentation server from inside `docs/`:

```console
$ cd docs && just serve
```

Helpers:

```console
$ just build-docs
```

```console
$ just serve-docs
```

Rebuild docs on file change:

```console
$ just watch-docs
```

This requires [entr(1)].

Rebuild docs and run the server from one terminal:

```console
$ just dev-docs
```

## Formatting / Linting

### Linting and Formatting

The project uses [ruff] to handle formatting, sorting imports and linting.

````{tab} Command

uv:

```console
$ uv run ruff check .
```

If you setup manually:

```console
$ ruff check .
```

````

````{tab} just

```console
$ just ruff
```

````

````{tab} Watch

```console
$ just watch-ruff
```

requires [`entr(1)`].

````

````{tab} Fix files

uv:

```console
$ uv run ruff check . --fix
```

If you setup manually:

```console
$ ruff check . --fix
```

````

#### Formatting

[ruff format] is used for formatting.

````{tab} Command

uv:

```console
$ uv run ruff format .
```

If you setup manually:

```console
$ ruff format .
```

````

````{tab} just

```console
$ just ruff-format
```

````

### Type Checking

[mypy] is used for static type checking.

````{tab} Command

uv:

```console
$ uv run mypy .
```

If you setup manually:

```console
$ mypy .
```

````

````{tab} just

```console
$ just mypy
```

````

````{tab} Watch

```console
$ just watch-mypy
```

requires [`entr(1)`].
````

## Releasing

[uv] handles virtualenv creation, package requirements, versioning,
building, and publishing. Therefore there is no setup.py or requirements files.

See {ref}`releasing` for the release checklist. Update
{data}`django_slugify_processor.__version__` in
`src/django_slugify_processor/__about__.py` and `version` in `pyproject.toml`,
then commit the release:

```console
$ git commit -m 'Tag v0.1.1'
```

[git]: https://git-scm.com/
[installation documentation]: https://docs.astral.sh/uv/getting-started/installation/
[just]: https://just.systems/
[pytest-watcher]: https://github.com/olzhasar/pytest-watcher
[uv]: https://github.com/astral-sh/uv
[entr(1)]: http://eradman.com/entrproject/
[`entr(1)`]: http://eradman.com/entrproject/
[ruff format]: https://docs.astral.sh/ruff/formatter/
[ruff]: https://ruff.rs
[mypy]: http://mypy-lang.org/
