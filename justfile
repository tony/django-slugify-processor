# justfile for django-slugify-processor
# https://just.systems/

set shell := ["bash", "-uc"]

# File patterns
watch_files := "find . -type f -not -path '*/\\.*' | grep -i '.*[.]py$' 2> /dev/null"
py_files := "find . -type f -not -path '*/\\.*' -and -not -path '*/settings/*' -and -not -path '*/migrations/*' | grep -i '.*[.]py$'"

# List all available commands
default:
    @just --list

# Run tests with pytest
[group: 'test']
test *args:
    uv run py.test {{ args }}

# Run tests then start continuous testing with pytest-watcher
[group: 'test']
start:
    just test
    uv run ptw .

# Watch files and run tests on change (requires entr)
[group: 'test']
watch-test:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v entr > /dev/null; then
        ${{ watch_files }} | entr -c just test
    else
        just test
        just _entr-warn
    fi

# Build documentation
[group: 'docs']
build-docs:
    just -f docs/justfile html

# Watch files and rebuild docs on change
[group: 'docs']
watch-docs:
    just -f docs/justfile watch

# Start documentation server with auto-reload
[group: 'docs']
start-docs:
    just -f docs/justfile start

# Start documentation design mode (watches static files)
[group: 'docs']
design-docs:
    just -f docs/justfile design

# Format code with ruff
[group: 'lint']
ruff-format:
    uv run ruff format .

# Run ruff linter
[group: 'lint']
ruff:
    uv run ruff check .

# Watch files and run ruff on change
[group: 'lint']
watch-ruff:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v entr > /dev/null; then
        ${{ watch_files }} | entr -c just ruff
    else
        just ruff
        just _entr-warn
    fi

# Run mypy type checker
[group: 'lint']
mypy:
    uv run mypy $(${{ py_files }})

# Watch files and run mypy on change
[group: 'lint']
watch-mypy:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v entr > /dev/null; then
        ${{ py_files }} | entr -c just mypy
    else
        just mypy
        just _entr-warn
    fi

# Format markdown files with prettier
[group: 'format']
format-markdown:
    prettier --parser=markdown -w *.md docs/*.md docs/**/*.md CHANGES

[private]
_entr-warn:
    @echo "----------------------------------------------------------"
    @echo "     ! File watching functionality non-operational !      "
    @echo "                                                          "
    @echo "Install entr(1) to automatically run tasks on file change."
    @echo "See https://eradman.com/entrproject/                      "
    @echo "----------------------------------------------------------"
