(releasing)=

# Releasing

Releases are published to [PyPI](https://pypi.org/project/django-slugify-processor/)
via [OIDC trusted publishing](https://docs.pypi.org/trusted-publishers/) from
[GitHub Actions](https://github.com/features/actions).

## Steps

1. Update {data}`django_slugify_processor.__version__` in `src/django_slugify_processor/__about__.py` and `version` in `pyproject.toml`.

2. Commit the release:

```console
$ git commit -m 'Tag vX.Y.Z'
```

AI agents stop after the release commit. The human release maintainer handles
tag creation and tag pushes, because tags trigger the publishing workflow.

3. Push the release commit:

```console
$ git push
```

The CI workflow builds the package and publishes it to PyPI automatically.
