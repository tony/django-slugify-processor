(code-style)=

# Code Style

## ruff

The project uses [ruff](https://ruff.rs) for linting and formatting.

Lint:

```console
$ uv run ruff check .
```

Auto-fix:

```console
$ uv run ruff check . --fix
```

Format:

```console
$ uv run ruff format .
```

## mypy

[mypy](http://mypy-lang.org/) is used for static type checking.

```console
$ uv run mypy .
```

See `pyproject.toml` `[tool.mypy]` for the full configuration.
