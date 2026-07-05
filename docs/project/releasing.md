(releasing)=

# Releasing

Releases are published to [PyPI](https://pypi.org/project/django-slugify-processor/) via OIDC-trusted publishing from [GitHub Actions](https://github.com/features/actions).

## Steps

1. Update `__version__` in `src/django_slugify_processor/__about__.py` and `version` in `pyproject.toml`.

2. Commit the release:

```console
$ git commit -m 'Tag vX.Y.Z'
```

AI agents stop after the release commit. The human release maintainer creates
and pushes tags, because tags trigger the publishing workflow.

```console
$ git tag vX.Y.Z
```

3. Push the release commit and tag:

```console
$ git push
```

```console
$ git push --tags
```

The CI workflow builds the package and publishes it to PyPI automatically.
