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

Helpers: `make test`

## Automatically run tests on file save

1. `make start` (via [pytest-watcher])
2. `make watch_test` (requires installing [entr(1)])

[pytest-watcher]: https://github.com/olzhasar/pytest-watcher

## Documentation

Default preview server: http://localhost:8034

[sphinx-autobuild] will automatically build the docs, watch for file changes and launch a server.

From home directory: `make start_docs`
From inside `docs/`: `make start`

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

### Manual documentation (the hard way)

`cd docs/` and `make html` to build. `make serve` to start http server.

Helpers:
`make build_docs`, `make serve_docs`

Rebuild docs on file change: `make watch_docs` (requires [entr(1)])

Rebuild docs and run server via one terminal: `make dev_docs` (requires above, and a
`make(1)` with `-J` support, e.g. GNU Make)

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

````{tab} make

```console
$ make ruff
```

````

````{tab} Watch

```console
$ make watch_ruff
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

````{tab} make

```console
$ make ruff_format
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

````{tab} make

```console
$ make mypy
```

````

````{tab} Watch

```console
$ make watch_mypy
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
