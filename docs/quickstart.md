(quickstart)=

# Quickstart

## Installation

For latest official version:

```console
$ pip install --user django-slugify-processor
```

Or using uv:

```console
$ uv tool install django-slugify-processor
```

Upgrading:

```console
$ pip install --user --upgrade django-slugify-processor
```

Or with uv:

```console
$ uv tool upgrade django-slugify-processor
```

(developmental-releases)=

### Developmental releases

New versions of django-slugify-processor are published to PyPI as alpha, beta, or release candidates.
In their versions you will see notification like `a1`, `b1`, and `rc1`, respectively.
`1.10.0b4` would mean the 4th beta release of `1.10.0` before general availability.

- [pip]\:

  ```console
  $ pip install --user --upgrade --pre django-slugify-processor
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@next 'django-slugify-processor' --pip-args '\--pre' --force
  // Usage: django-slugify-processor@next [args]
  ```

- [uv tool install][uv-tools]\:

  ```console
  $ uv tool install --prerelease=allow django-slugify-processor
  ```

- [uv]\:

  ```console
  $ uv add django-slugify-processor --prerelease allow
  ```

- [uvx]\:

  ```console
  $ uvx --from 'django-slugify-processor' --prerelease allow django-slugify-processor
  ```

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install --user -e git+https://github.com/tony/django-slugify-processor.git#egg=django-slugify-processor
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@master 'django-slugify-processor @ git+https://github.com/tony/django-slugify-processor.git@master' --force
  ```

- [uv]\:

  ```console
  $ uv tool install django-slugify-processor --from git+https://github.com/tony/django-slugify-processor.git
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
[uv]: https://docs.astral.sh/uv/
[uv-tools]: https://docs.astral.sh/uv/concepts/tools/
[uvx]: https://docs.astral.sh/uv/guides/tools/

## Usage

For usage instructions, please refer to the [README](https://github.com/tony/django-slugify-processor#readme).
