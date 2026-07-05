# Documentation voice

This file covers the *voice* of prose under `docs/` — how to frame a
page so a reader meets the idea before its configuration. It
complements the repository-root `AGENTS.md`, which already governs
code blocks, shell-command formatting, doctests, changelog
conventions, and MyST roles. When the two overlap, the root file
wins; this one only answers the question it leaves open: how should
the prose sound?

## Who you are writing for

The default reader is a Django developer whose slugs come out wrong —
"C++" collapses to "c", "New York City" should be "nyc". They know
Django well: the settings module, `django.utils.text.slugify`,
template filters, `INSTALLED_APPS`. You cannot assume they know this
package's internals: that `SLUGIFY_PROCESSORS` is a list of import
strings resolved with `import_string`, that processors run in order
before Django's own `slugify`, or that the template filter
deliberately shadows the built-in one.

A second, smaller reader integrates deeper: installing the filter as
a template builtin, pointing django-autoslug's or django-extensions'
`AutoSlugField` at this package's `slugify`, or contributing. Serve
them too, but mark their material opt-in ("for the rarer cases",
"advanced") so the default reader knows they can stop. Never make the
common case pay a comprehension tax for the advanced one.

## Voice

- **Second person, present tense, active.** "You register a
  processor", not "A processor is registered". Address the reader who
  is doing the thing.
- **Concept before configuration.** Open by saying what the thing
  *is* and what it does for the reader — a processor is a function
  that takes a string and returns a string. The settings key and the
  dotted import path are the last details they need, not the first. A
  page that opens with "add this to settings" has buried the idea
  under its mechanics.
- **Say when they can stop.** Lead with the default and the
  reassurance: with no `SLUGIFY_PROCESSORS` configured, `slugify()`
  behaves exactly like Django's. Let a skimmer leave after one
  paragraph.
- **Grant permission, don't demand attention.** "Reach for this
  when…", "for the rarer cases" — tell readers they're in the right
  place without implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  drop-in `slugify` import → one processor in settings → the template
  filter → wiring a model field. Each step is for a smaller audience
  than the last.
- **Lean on the pipeline.** The reader thinks value → each function
  in `SLUGIFY_PROCESSORS`, in order → Django's `slugify`; reinforce
  that chain when you explain ordering or why one processor sees
  another's output. It is the mental model the whole package hangs
  on.
- **Name the trade-off.** If a choice costs something — processors
  run on every call, so they should stay pure and fast; installing
  the filter as a builtin shadows Django's `slugify` filter in every
  template — say so, and say what it buys. State it; don't sell it.
- **Frame by concept, not by mechanism.** Don't headline a feature by
  its settings key or dotted path in prose; that names the
  implementation surface, which is the reader's last concern. Name
  the concept. The mechanics vocabulary — the import string, the
  `slugify_function=` field option — belongs in a code block or the
  API reference, and only there.

## Examples that run

Doctests on pages under `docs/` execute through
`just -f docs/justfile doctest`, and pytest runs Python docstrings
through `--doctest-modules`. A wrong example should fail loudly before
the docs are considered complete.

- There are no `doctest_namespace` fixtures in this repo — import
  what you use (`from django_slugify_processor.text import slugify`).
- Doctests run under the test project's settings (`tests.settings`),
  which set no `SLUGIFY_PROCESSORS` — a bare example shows the
  pass-through default. An example that needs a processor must
  configure one itself, e.g. with `django.test.override_settings`.
- Use a ```` ```{doctest} ```` directive for docs-page `>>>`
  sessions that must run through Sphinx. `ELLIPSIS` and
  `NORMALIZE_WHITESPACE` are already on via `doctest_optionflags` in
  `pyproject.toml`. Use a ```` ```console ```` block for shell commands
  at a `$` prompt.

## What stays precise

Warm the framing, never the facts. The term → default slug → desired
slug tables, processor ordering, exact settings lists, error strings,
and function cross-references carry meaning in their exact form —
leave them alone. The friendly voice belongs in the sentences
*around* a precise block, introducing it, not inside it paraphrasing
it into vagueness.

## Cross-references

Point the deeper integrator at the detail page rather than inlining
it, and put the link where their interest peaks — on the phrase that
made them curious ("wire it into a model field") — not as a
standalone footnote the eye skips. Use the MyST roles listed in the
root `AGENTS.md` (`{func}`, `{class}`, `{meth}`, `{attr}`, `{exc}`,
`{ref}`, `{doc}`). Pages declare explicit anchors — `(quickstart)=`,
`(api)=`, `(developmental-releases)=` — and a `{ref}` must match its
target exactly. Intersphinx covers Python and Django, so a `{func}`
reference to `django.utils.text.slugify` resolves into Django's own
docs. `just build-docs` catches a broken cross-reference; the
doctests do not — so build the docs before you commit.

Link the first prose mention of any symbol that has a useful
destination on that page. This includes Python objects, this
package's APIs, Django settings and utilities with intersphinx
destinations, other docs pages, and external tools or projects. Use
the most specific target available: `{func}`, `{class}`, `{meth}`,
`{mod}`, `{exc}`, or `{attr}` for API objects; `{ref}` or `{doc}` for
documentation pages and section anchors; and a Markdown link or
reference link for external projects. After the first linked mention
on a page, later mentions can stay plain unless the distance or
context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention
rule. If the first occurrence would be a heading, grid-card teaser,
or introductory sentence, link that occurrence or retitle the heading
so the first prose mention can carry the link. Leave command
examples, code blocks, and literal configuration values as code; link
the surrounding prose instead.

## Before you commit

- Does the page open with what the feature *is*, or with how to
  configure it?
- Can a reader who needs only the pass-through default stop after the
  first paragraph?
- Is anything framed by its settings key or dotted path that should
  be named by concept instead?
- Are the template-builtin and model-field parts clearly marked
  opt-in?
- Do `just test` and `just -f docs/justfile doctest` pass, and did you
  leave every code block, table, and cross-reference exact?
- Did `just build-docs` stay clean — no new warning, no broken
  cross-reference?
