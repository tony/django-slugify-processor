# AGENTS.md

django-slugify-processor runs a Django project's own text processors ahead
of Django's `slugify()`, so terms like `C++` or `US$` produce the slug a
project wants instead of Django's generic default.

Follow the conventions already in the tree, and keep a change scoped to
what was asked for.

## What is here

| Path | What it is |
| ---- | ---------- |
| `src/django_slugify_processor/text.py` | `slugify()`: runs `SLUGIFY_PROCESSORS`, then Django's own `slugify` |
| `src/django_slugify_processor/templatetags/slugify_processor.py` | Template filter wrapping `text.slugify` |
| `src/django_slugify_processor/__about__.py` | Package metadata: version, title, URLs |
| `test_app/` | Example Django app (model, processors) used by tests and docs |
| `tests/` | pytest + pytest-django suite; `tests/settings.py` is the Django settings module |
| `docs/` | Sphinx site (MyST Markdown) |
| `CHANGES` | Changelog; rendered as `docs/history.md` |
| `pyproject.toml` | Metadata, dependencies, ruff/mypy/pytest config |
| `justfile`, `docs/justfile` | Task runner recipes |

## Which policy applies

- Documentation, user-facing text, `CHANGES`, commit messages, docstrings,
  and source comments: [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, documentation builds, releases, and pull
  requests: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a
  single-use helper or a one-line re-export.
- Add a test for every user-visible behaviour change, and a `CHANGES`
  entry for every change to the public API, settings, or output.
- A passing gate is evidence only once it has been shown capable of
  failing. Pair a new test with a deliberate break that proves it bites.

Processors must stay pure and idempotent — no database or network access,
since slugification can run inside model-field saves, template rendering,
and bulk imports. The template filter must keep delegating to `text.slugify`
rather than reimplementing it, so Python and template usage cannot diverge.
Respect the `allow_unicode` flag wherever it is threaded through; do not
force ASCII unless a caller asked for it.

## References

- Documentation: https://django-slugify-processor.git-pull.com
- PyPI: https://pypi.org/project/django-slugify-processor/
- Django `slugify`: https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.text.slugify
- gp-libs (docs and test tooling used here): https://gp-libs.git-pull.com
