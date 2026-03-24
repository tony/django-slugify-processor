(releasing)=

# Releasing

Releases are published to [PyPI](https://pypi.org/project/django-slugify-processor/) via OIDC-trusted publishing from GitHub Actions.

## Steps

1. Update `__version__` in `src/django_slugify_processor/__about__.py` and `version` in `pyproject.toml`.

2. Commit and tag:

```console
$ git commit -m 'build(django-slugify-processor): Tag vX.Y.Z'
```

```console
$ git tag vX.Y.Z
```

3. Push:

```console
$ git push
```

```console
$ git push --tags
```

The CI workflow builds the package and publishes it to PyPI automatically.
