# Development

[poetry] is a required package to develop.

`git clone https://github.com/tony/django-slugify-processor.git`

`cd g`

`poetry install -E "docs test coverage lint"`

Makefile commands prefixed with `watch_` will watch files and rerun.

## Tests

`poetry run py.test`

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

poetry:

```console
$ poetry run ruff
```

If you setup manually:

```console
$ ruff .
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

poetry:

```console
$ poetry run ruff . --fix
```

If you setup manually:

```console
$ ruff . --fix
```

````

#### ruff format

[ruff format] is used for formatting.

````{tab} Command

poetry:

```console
$ poetry run ruff format .
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

poetry:

```console
$ poetry run mypy .
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

[poetry] handles virtualenv creation, package requirements, versioning,
building, and publishing. Therefore there is no setup.py or requirements files.

Update `__version__` in `__about__.py` and `pyproject.toml`::

    git commit -m 'build(django-slugify-processor): Tag v0.1.1'
    git tag v0.1.1
    git push
    git push --tags
    poetry build
    poetry publish

[poetry]: https://python-poetry.org/
[entr(1)]: http://eradman.com/entrproject/
[`entr(1)`]: http://eradman.com/entrproject/
[ruff format]: https://docs.astral.sh/ruff/formatter/
[ruff]: https://ruff.rs
[mypy]: http://mypy-lang.org/
