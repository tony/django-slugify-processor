# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, `CHANGES`, commit messages, docstrings, source comments, and
documentation pages under `docs/` — every surface a reader reaches.

For environment setup, the gates, and the release process, see
[CONTRIBUTING.md](CONTRIBUTING.md). The constraints every change is held to,
and the map of what is where, are in [AGENTS.md](../AGENTS.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on; a
`CHANGES` entry says what changed; prose says what happens. All three are
present tense, lead with the thing being described, and stop. Why it was
built that way belongs in the commit message, which is timestamped and
attached to the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks.
Prefer short declarative sentences, one operational fact each. Do not
explain Python or Django to a Django developer; do explain this project's
semantics.

Type annotations describe shape. Documentation describes meaning. A sentence
that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                                |
| --------------------------------- | -------------------------------------- |
| "We added…"                      | "`slugify()` now accepts…"            |
| "New and improved"               | "`SLUGIFY_PROCESSORS` now…"           |
| "powerful", "seamless"           | state the capability                  |
| "easily", "simply", "just"       | omit                                  |
| "simple", "obvious", "intuitive" | omit                                  |
| "robust"                         | name the failure that is handled      |
| "comprehensive"                  | name what is covered                  |
| "production-ready"               | state the guarantee                   |
| "optimized", "blazingly fast"    | give the magnitude                    |
| "various fixes"                  | name the components                   |
| "under the hood"                 | omit unless observable                |
| "please note that", "note that"  | state the fact                        |
| "leverage", "utilize"            | "use"                                 |
| "delve into"                     | "read", or omit                       |
| "best practices"                 | name the practice                     |
| "in order to"                    | "to"                                  |

## Who you are writing for

The default reader is a Django developer whose slugs come out wrong — `C++`
collapses to `c`, `New York City` should be `nyc`. They know Django well: the
settings module, `django.utils.text.slugify`, template filters,
`INSTALLED_APPS`. They cannot be assumed to know this package's internals:
that `SLUGIFY_PROCESSORS` is a list of import strings resolved with
`import_string`, that processors run in order before Django's own
`slugify`, or that the template filter deliberately shadows the built-in
one.

A second, smaller reader integrates deeper: installing the filter as a
template builtin, pointing django-autoslug's or django-extensions'
`AutoSlugField` at this package's `slugify`, or contributing. Serve them
too, but mark their material opt-in — "for the rarer cases", "advanced" — so
the default reader knows they can stop. Never make the common case pay a
comprehension tax for the advanced one.

Rules that follow:

- **Second person, present tense, active.** "You register a processor", not
  "A processor is registered". Address the reader who is doing the thing.
- **Concept before configuration.** Open by saying what the thing *is* and
  what it does for the reader — a processor is a function that takes a
  string and returns a string. The settings key and the dotted import path
  are the last details they need, not the first. A page that opens with
  "add this to settings" has buried the idea under its mechanics.
- **Say when they can stop.** Lead with the default and the reassurance:
  with no `SLUGIFY_PROCESSORS` configured, `slugify()` behaves exactly like
  Django's. Let a skimmer leave after one paragraph.
- **Grant permission, do not demand attention.** "Reach for this when…",
  "for the rarer cases" — tell readers they are in the right place without
  implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  drop-in `slugify` import, then one processor in settings, then the
  template filter, then wiring a model field. Each step is for a smaller
  audience than the last.
- **Lean on the pipeline.** The reader thinks value → each function in
  `SLUGIFY_PROCESSORS`, in order → Django's `slugify`. Reinforce that chain
  when explaining ordering or why one processor sees another's output. It
  is the mental model the whole package hangs on.
- **Name the trade-off.** If a choice costs something — processors run on
  every call, so they should stay pure and fast; installing the filter as a
  builtin shadows Django's `slugify` filter in every template — say so, and
  say what it buys. State it; do not sell it.
- **Frame by concept, not by mechanism.** Do not headline a feature by its
  settings key or dotted path in prose; that names the implementation
  surface, which is the reader's last concern. Name the concept. The
  mechanics vocabulary — the import string, the `slugify_function=` field
  option — belongs in a code block or the API reference, and only there.

## README

A README is the shortest path from "what is this?" to competent use, not
the project's autobiography.

The first sentence is a contract. It says what abstraction the reader has
been handed, concretely enough to tell this package apart from the
neighbouring one.

Get to a runnable command or snippet before anything the reader can skip. A
logo, a mission statement, a comparison matrix, and three paragraphs of
history in front of the install line all cost the same thing.

State the supported Django and Python combinations precisely, not just a
floor. `requires-python` in `pyproject.toml` sets the Python floor; the
Django trove classifiers there set the Django range; the matrix in
`.github/workflows/tests.yml` states which pairs actually run, including
any exclusion that raises the Python floor for part of the Django range.
Read all three before writing a compatibility claim — a bare "Django 5.2+"
can hide a real per-version Python constraint.

Name the distribution, the import, and the executable separately wherever
they differ. That distinction prevents a Python-specific class of
confusion. (This package has no console script — there is nothing to
distinguish here, so skip a CLI section entirely rather than invent one.)

Examples are executable, not illustrative fiction. Never
`your-command <some-options>`. See
[Documented examples that run](#documented-examples-that-run) for which
blocks are executed and how to write one that qualifies.

Document the semantic model, not the flag list. Say what a setting does to
behavior, what the pipeline order means, and what a caller can rely on —
not just that a setting "exists".

State defaults explicitly — defaults are API. State negative guarantees
where they exist: "does not modify your configuration file", "no network
access", "never writes outside the destination". They establish boundaries
faster than any amount of description.

Headings stay conventional and stable, because people deep-link them.
Badges are few and load-bearing.

## Settings

A Django setting this package reads is public API, held to the same
documentation bar as a function parameter: name it in backticks, state its
default, and say what happens when a project leaves it unset.

`SLUGIFY_PROCESSORS` is this package's only setting: a list of dotted
import strings resolved with
`django.utils.module_loading.import_string`. Left unset,
`getattr(settings, "SLUGIFY_PROCESSORS", [])` falls back to an empty list,
and `django_slugify_processor.text.slugify` behaves exactly like Django's
own `django.utils.text.slugify`. State that fallback explicitly at the
first mention of the setting on any page — a reader who has not configured
anything needs to know they are already covered.

A new setting gets the same treatment before it ships: name, default, and
the unset behavior, in the docstring of the code that reads it and in
whichever `docs/` page a reader would find it from.

## Documented examples that run

Examples in this project are tests. This section is the contract for
writing one the test suite can actually see.

**A fence tag is cosmetic. Only a `>>> ` prompt executes.** A block written
as

    ```python
    slugify("C++")
    ```

is prose that looks like a test. Nothing collects it, nothing runs it, and
it can be wrong for years. The same block written with a prompt is a test:

    ```python
    >>> slugify("C++")
    ```

This is the single most expensive mistake available when editing
documentation, because removing the prompts leaves a green test suite and a
silently deleted test. When editing a file that contains examples, count
the prompts before and after.

**Where examples run, concretely.** `testpaths` in `pyproject.toml` lists
`src/django_slugify_processor`, `tests`, and `docs`. `addopts` includes
`--doctest-modules`, so every docstring example under `src/` runs on every
`pytest` invocation. `README.md` is **not** in `testpaths` — a `>>> ` prompt
placed there would not run, which is why the README currently has none and
should not gain any; keep its blocks illustrative and unprompted.

Markdown pages under `docs/` are collected by `pytest_doctest_docutils` (a
plugin `gp-libs` registers under pytest's `sphinx` entry point). It reads
`.md` files reachable from `testpaths` and executes any `>>> ` prompt it
finds, including one nested inside a MyST directive.

**This project's docs pages use the `{doctest}` MyST directive, not a bare
`python` fence, for `>>> ` sessions:**

    ```{doctest}
    >>> slugify("C++")
    'c'
    ```

That is a deliberate choice, worth stating explicitly since a plain
prompted `python` fence would also be collected. A `{doctest}` block runs
twice: once through the `pytest_doctest_docutils` collector above, and again
through Sphinx's own doctest builder
(`sphinx-build -b doctest`, wired up as `just -f docs/justfile doctest` and
exercised by `tests/test_docs_examples.py::test_sphinx_doctest_builder_runs`).
A plain prompted `python` fence would only get the first of those two runs.
Reach for `{doctest}` on any docs page; reserve a bare `python` fence for
illustration that must not execute (config snippets, `TEMPLATES` blocks).

**No `doctest_namespace` fixture exists in this repository.** There is no
`conftest.py` anywhere in the tree, and the package ships no pytest plugin
of its own. Every name a block uses — `slugify`, `override_settings`,
`Template`, `test_app.coding.slugify_programming_languages` — must be
imported in that block or an earlier block on the same page; nothing is
pre-injected. Sphinx's own doctest builder is configured separately, via
`doctest_global_setup` in `docs/conf.py`, which calls `django.setup()`
before any `{doctest}` block runs — that only makes Django's app registry
ready, it does not inject names.

**`# doctest: +SKIP` is not permitted.** It is a workaround that tests
nothing. Configure the example with `django.test.override_settings` instead
of skipping it.

**Do not downgrade a doctest to a non-executed block to make it pass.** A
`.. code-block::` or an unprompted fence does not run. If an example cannot
pass, fix the example or fix the code.

**Option flags.** `ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled
globally via `doctest_optionflags` in `pyproject.toml`, so `...` elides
variable output and whitespace differences do not fail a comparison. Reach
for an inline `# doctest: +FLAG` only for the block that needs one beyond
those two.

**Docstring examples** use the NumPy `Examples` section:

    Examples
    --------
    >>> from django_slugify_processor.text import slugify
    >>> slugify("c++")
    'c'

## Cross-references

Link the first prose mention of any symbol that has a useful destination on
that page: Python objects, this package's own API, Django settings and
utilities (intersphinx covers Python and Django, so a `func` role
reference to `django.utils.text.slugify` resolves into Django's own docs),
other docs pages, and external tools or projects. Use the most specific
MyST role available, written as `` {rolename}`target` ``:

```
{func}`~django_slugify_processor.text.slugify`
{data}`django_slugify_processor.__version__`
{ref}`quickstart`
```

- `func` — module-level functions. The role actually in use today, for
  `django_slugify_processor.text.slugify` and the template filter.
- `data` — module-level data. Used for
  `django_slugify_processor.__version__`.
- `ref` — an anchor declared with `(label)=`. Used for cross-page targets
  such as the `quickstart` example above.
- `doc` — a doc-path link where no explicit anchor exists.
- `class`, `meth`, `attr`, `exc`, `mod` — standard Sphinx/MyST roles,
  available the day this package grows a class, exception, or submodule
  worth linking; none exist yet, so none of these are in use.

Plain backticks are correct for code syntax, environment variables,
parameter names, and file paths that are not a doc destination — never for
something with its own rendered page.

Do not rely on a later reference section to satisfy the first-mention rule.
If the first occurrence would be a heading, grid-card teaser, or
introductory sentence, link that occurrence or retitle the heading so the
first prose mention can carry the link. Leave command examples, code
blocks, and literal configuration values as code; link the surrounding
prose instead.

Point the deeper integrator at the detail page rather than inlining it, and
put the link where their interest peaks — on the phrase that made them
curious ("wire it into a model field") — not as a standalone footnote the
eye skips.

`just build-docs` catches a broken cross-reference; the doctests do not —
so build the docs before committing a change that touches one.

## The changelog

`CHANGES` is the changelog, rendered directly as the project's changelog
page (`docs/history.md` includes it). Not `CHANGELOG.md`.

A ledger, not a narrative. It is scanned, and the question a reader is
asking is whether an entry affects them.

Lead with the identifier and a concrete verb — add, fix, remove, deprecate,
support, requires, `now`, `no longer`. Name identifiers literally. Do not
sell a fix: "no longer raises on an empty string", not "improves
reliability". Do not describe effort. Give the old behaviour only where it
explains a break, and mention mechanism only where a caller can observe
it — a refactor that changes nothing observable is not an entry.

**Release entry boilerplate.** Every release header is
`## django-slugify-processor X.Y.Z (YYYY-MM-DD)`. The file opens with a
`## django-slugify-processor X.Y.Z (unreleased)` placeholder block fenced
by `<!-- KEEP THIS PLACEHOLDER ... -->` and
`<!-- END PLACEHOLDER ... -->` HTML comments — new entries land immediately
below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open
with the version as sentence subject ("django-slugify-processor X.Y.Z
ships…") so the lead is self-contained when excerpted. Two to four
sentences telling the reader what shipped and who cares — user-visible
takeaways, not internal mechanism. Cross-reference detail docs with
`{ref}` to keep the lead compact.

**Unreleased entries carry no lead paragraph and no version summary.**
Speaking for a release — what the version "is", "ships", or "focuses on" —
is presumptuous before its scope is final. Only the person cutting the
release writes that, and only when they are actually cutting it. Never
write or edit a lead paragraph from a feature branch, and never ask or
imply that a release should happen.

**Each deliverable is a section, not a bullet.** Inside `### What's new`,
every distinct deliverable gets a `#### Deliverable title (#NN)` heading
naming it in user vocabulary, followed by one to three prose paragraphs.
Do not wrap a paragraph in `- ` — bullets are for enumerable lists, not
paragraph containers.

**The deliverable test.** Before writing an entry, ask: "What's the
deliverable, in user vocabulary?" If that cannot be answered in one
sentence, the entry is not ready. Mechanism belongs in the pull request
description and code comments, not the changelog.

**A deprecation entry states four things:** what is deprecated, its
replacement (or that there is none), the release the deprecation began in,
and the earliest release that may remove it. This project's precedent, from
`## django-slugify-processor 1.7.0`:

> The 1.7.x series is the last branch intended for Django 3.2 users. The
> next feature line, 1.8.x, removes Django 3.2 support after Django 3.2's
> extended support ended on April 1, 2024.

That names the subject (Django 3.2 support), the release it survives
through (1.7.x), and the release that removes it (1.8.x) in two sentences.
A symbol-level deprecation follows the same shape: name the symbol, name
its replacement, state the version the deprecation started in, and state
the version that may remove it — never "in a future release".

**Fixed subheadings**, in this order when present: `### Breaking changes`,
`### Upcoming deprecations`, `### Dependencies`, `### What's new`,
`### Fixes`, `### Documentation`, `### Development`. Dev tooling (helper
scripts, internal automation) lives under `### Development`. For breaking
changes, show the migration path with concrete inline code (a `# Before` /
`# After` fenced block). Dependency floor bumps use the form
``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`,
occasionally `### Documentation`) with three or more genuinely small items
use bullets — one line each, never paragraphs. If a bullet swells past two
lines, promote it to a `#### Title (#NN)` heading with a prose body.

**Anti-patterns.** Fragile metrics that go stale silently — token
ceilings, third-party version pins, percent benchmarks, exact byte counts.
Describe the capability, not the math. Private symbols and internal
jargon. Walls of text dressed up as bullets. Breaking changes buried
mid-entry instead of given their own subheading at the top.

**Always link autodoc'd APIs**, per [Cross-references](#cross-references) —
never with plain backticks. Plain backticks stay correct for code syntax,
environment variables, parameter names, and file paths that are not a doc
destination.

## Docstrings

The prime directive: never restate the type. The annotation is the source
of truth; the docstring carries what the annotation cannot.

This is documentation debt wearing a docstring:

    def slugify(value: str, allow_unicode: bool = False) -> str:
        """Slugify a value.

        Parameters
        ----------
        value : str
            The value.
        allow_unicode : bool
            Whether to allow unicode.

        Returns
        -------
        str
            The slug.
        """

Document instead the dimensions the type system cannot encode: what a call
mutates, what it owns, what order results come back in, what has finished
by the time it returns, which exceptions it raises and what triggers each,
whether calling twice does anything the second time, what a number's units
and range are, what the boundary values do, and what differs by platform
or dependency version. For this package specifically: which setting a
function reads, and what happens when that setting is unset.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an
introspectable signature.

**Classes with fields** — `NamedTuple`, dataclasses — document every field
in an `Attributes` section:

    class SlugifyCase(t.NamedTuple):
        """Slugify behavior test case.

        Attributes
        ----------
        test_id : str
            Identifier used for the parametrized test id.
        value : str
            Input string handed to ``slugify``.
        """

Autodoc renders every field whether or not it is described, so an
undocumented `NamedTuple` field ships to the API docs as "Alias for field
number 0" and a dataclass field ships bare. Document all of them — a class
with three fields and two documented still ships a stub for the third.

One docstring dialect per repository, enforced by the linter rather than
relitigated in review: `ruff`'s `pydocstyle` rules run with
`convention = "numpy"` (`pyproject.toml`, `[tool.ruff.lint.pydocstyle]`).

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real
time rediscovering intent, an invariant, a constraint, or a failure mode
the code and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and
stop. They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that
hand-syncs a value the code owns — a count, an offset, a line reference, a
duplicated constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several
facts, in which case split it, or arguing, in which case cut it to the
fact.

Rationale, alternatives weighed, and the story of how the code got here
belong in the commit message: timestamped, attached to the exact diff, and
free to maintain.

A comment often holds both a constraint and the deliberation that found
it. Keep the constraint, cut the deliberation. "Runs at most once per
second" survives; "this is the right trade for now" does not.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency
  requirements that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not
  reintroduce the bug.
- A high-level sketch of an algorithm whose local operations do not
  reveal the whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves. Unfinished work goes in the
  tracker, not the source.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen
external facts.

Bad (Delete):

    # There are 321 tests to complete for servers.

Good (Keep):

    # CPython < 3.11 has no ExceptionGroup, so this branch stays.

### Documentation exception

Minimal usage examples, and parameter, return, and raises entries on
public API are exempt from the loss gate — they serve the caller, not the
maintainer. They are exempt from nothing else. Ceiling: a good man page
entry.

NumPy-style `Parameters`, `Returns`, and `Attributes` sections and
executable doctests fall under this exception — autodoc ships every field
whether or not it is described, and a doctest that runs is also a test.

## Terminology and capitalization

Pick the domain noun and keep it. This package's pipeline step is a
"processor" — not a "handler", "transform", or "hook" — everywhere: prose,
docstrings, and the `SLUGIFY_PROCESSORS` name it comes from. If the code
calls something a slug, do not call it a "URL segment" in one paragraph
and a "handle" in the next.

Stable vocabulary is what makes search, deep links, and an agent's
retrieval work at all.

Python and PyPI keep their own capitalisation. Distribution names are
written as they are published.

Do not write counts into prose — how many symbols exist, how many tests
there are. They go stale silently and no reader needs them.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are
exempt, because breaking them harms rendering. A pull request or issue
body does not wrap at all: GitHub renders a single newline as a space in a
file and as a line break in a comment, so a wrapped comment body arrives
as ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document. Write the sentence so it carries the fact on its own, and a
renderer that drops the marker loses nothing.

Do not use a local absolute path or an email address in anything
published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Executed examples are exempt — the test suite runs them,
nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments
  inside it.
- **Command menus are per-command blocks with prose lead-ins**, not
  tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware
  copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing
`(#NN)` pull request reference, and wrap body lines at 72. Separate the
`why:` and `what:` blocks with a blank line.

Routine maintenance commits drop the colon and take a capitalised
description, which is what distinguishes them at a glance in
`git log --oneline`. Both forms are real in this project's history:

```
py(deps[dev]) Bump dev packages
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types, drawn from this project's own history:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **py(deps[docs])**: Documentation-build dependencies
- **ai(rules[AGENTS])**: AI rule updates

Example:

```
Text(feat[slugify]): Add an `allow_unicode` passthrough

why: Let callers preserve unicode without a second processor pass.

what:
- Forward allow_unicode to Django's slugify after processors run
- Document the passthrough in the docstring's Examples section
```

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

### Release commits

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow.

A release commit subject is plain and short: `Tag v<version>`. The
detailed why and what go in the body. Do not use the
`Scope(type[detail]):` format for a release — it buries the lede.

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file
  counts, dated "as of" claims, bare SHAs, or local absolute paths —
  unless they are strict evidentiary artefacts such as a benchmark log.
- **Diff narration.** Do not restate what moved, was renamed, or was
  removed in anything the reader holds alongside the diff: code,
  docstrings, README, `CHANGES`, or a pull request description. The diff
  and commit message already carry it.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of a
  published release actually experienced the old state (the
  Published-Release Test, below).
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No
  `[R1]`, `Option B`, or any index a reader has to decode.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those
are the facts [Source comments](#source-comments) keeps, and every other
comment is judged by it. Preserve exact counts, dates, and SHAs that serve
as evidence — a benchmark result, a stack trace, a lockfile entry. A
useful description explains what changed for the system or the user; it
does not inventory the files or functions the diff already shows.

### Durable source links

Link to a pinned revision, never to trunk. A pinned permalink is not a
brittle reference; an unlinked SHA dropped into prose is. `blob/master/…`
links rot silently — the file moves, lines shift, and the anchor lands on
unrelated code while still resolving.

- Prefer a release tag (`blob/v1.11.0/…`). Most durable, and it tells the
  reader which released version the claim held for.
- Otherwise use a 7-character commit ref (`blob/9a29b1a/…`) reachable
  from trunk. Use when there is no tag or the claim is about unreleased
  code. Never a pull-request-head SHA — it can be rebased or
  garbage-collected.
- Reserve `blob/master/…` for living documents meant to always show the
  latest state, such as this contributing guide.
- Line anchors (`#L120-L145`) are only safe on a pinned ref.

### The Published-Release Test

Long-running branches accumulate tactical decisions — renames, refactors,
attempts then reverts. When deciding what counts as branch-internal, use
trunk or the parent branch as the baseline, not an intermediate state
inside the current branch. Ask:

> Did users of the most recently published release ever experience this
> old name, old behavior, or bug?

If the answer is no, it is branch-internal narrative. Move it to the
commit message and describe only the final state in the artifact.

Keep in shipped artifacts: deprecations and migration guides for symbols
that actually shipped, `### Fixes` entries for bugs that affected a
published release, and comments explaining why the current code looks
this way that make sense to a reader who never saw the previous version.

### Cleanup in hindsight

When applying these rules retroactively inside a feature branch, first
diff against the parent branch or trunk to see which commits the branch
actually introduced. For in-branch commits, either `fixup!` each one and
`git rebase --autosquash`, or fold the cleanup into one commit at the
branch tip. Leave trunk or parent commits alone by default; touch them
only on explicit instruction, and never rewrite shared history to do it.
