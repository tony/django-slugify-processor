# justfile for django-slugify-processor
# https://just.systems/

set shell := ["bash", "-uc"]

# File patterns
watch_files := "find . -type f -not -path '*/\\.*' | grep -i '.*[.]py$' 2> /dev/null"
py_files := "find . -type f -not -path '*/\\.*' -and -not -path '*/settings/*' -and -not -path '*/migrations/*' | grep -i '.*[.]py$'"

# List all available commands
default:
    @just --list

# ============================================================================
# Testing
# ============================================================================

# Run tests with pytest
test *args:
    uv run py.test {{ args }}

# Run tests then start continuous testing with pytest-watcher
start:
    just test
    uv run ptw .

# Watch files and run tests on change (requires entr)
watch-test:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v entr > /dev/null; then
        ${{ watch_files }} | entr -c just test
    else
        just test
        just _entr-warn
    fi

# ============================================================================
# Documentation
# ============================================================================

# Build documentation
build-docs:
    just -f docs/justfile html

# Watch files and rebuild docs on change
watch-docs:
    just -f docs/justfile watch

# Start documentation server with auto-reload
start-docs:
    just -f docs/justfile start

# Start documentation design mode (watches static files)
design-docs:
    just -f docs/justfile design

# ============================================================================
# Linting & Formatting
# ============================================================================

# Format code with ruff
ruff-format:
    uv run ruff format .

# Run ruff linter
ruff:
    uv run ruff check .

# Watch files and run ruff on change
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
mypy:
    uv run mypy $(${{ py_files }})

# Watch files and run mypy on change
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
format-markdown:
    prettier --parser=markdown -w *.md docs/*.md docs/**/*.md CHANGES

# ============================================================================
# Private helpers
# ============================================================================

[private]
_entr-warn:
    @echo "----------------------------------------------------------"
    @echo "     ! File watching functionality non-operational !      "
    @echo "                                                          "
    @echo "Install entr(1) to automatically run tasks on file change."
    @echo "See https://eradman.com/entrproject/                      "
    @echo "----------------------------------------------------------"
