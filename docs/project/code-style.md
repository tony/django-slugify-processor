(code-style)=

# Code Style

## Linting and Formatting

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

## Type Checking

[mypy](http://mypy-lang.org/) is used for static type checking.

```console
$ uv run mypy .
```

See `pyproject.toml` `[tool.mypy]` for the full configuration.
