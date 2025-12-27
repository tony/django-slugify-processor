# Development

[uv] is a required package to develop.

Install and [git] and [uv]

Clone:

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

[installation documentation]: https://docs.astral.sh/uv/getting-started/installation/
[git]: https://git-scm.com/

## Tests

`uv run py.test`

Helpers: `just test`

## Automatically run tests on file save

1. `just start` (via [pytest-watcher])
2. `just watch-test` (requires installing [entr(1)])

[pytest-watcher]: https://github.com/olzhasar/pytest-watcher

## Documentation

Default preview server: http://localhost:8034

[sphinx-autobuild] will automatically build the docs, watch for file changes and launch a server.

From home directory: `just start-docs`
From inside `docs/`: `just start`

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

### Manual documentation (the hard way)

`cd docs/` and `just html` to build. `just serve` to start http server.

Helpers:
`just build-docs`, `just serve-docs`

Rebuild docs on file change: `just watch-docs` (requires [entr(1)])

Rebuild docs and run server via one terminal: `just dev-docs`

## Formatting / Linting

### ruff

The project uses [ruff] to handle formatting, sorting imports and linting.

````{tab} Command

uv:

```console
$ uv run ruff
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

#### ruff format

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

### mypy

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

Update `__version__` in `__about__.py` and `pyproject.toml`::

    git commit -m 'build(django-slugify-processor): Tag v0.1.1'
    git tag v0.1.1
    git push
    git push --tags

[uv]: https://github.com/astral-sh/uv
[entr(1)]: http://eradman.com/entrproject/
[`entr(1)`]: http://eradman.com/entrproject/
[ruff format]: https://docs.astral.sh/ruff/formatter/
[ruff]: https://ruff.rs
[mypy]: http://mypy-lang.org/
