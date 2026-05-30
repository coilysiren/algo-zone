# Agent instructions

Per-repo agent operating rules for `algo-zone`. Workspace-level conventions (git workflow, voice, safety) are inherited from Kai's global `AGENTS.md` chain.

## Scope

A workshop for figuring out algorithms and data-structure puzzles across many languages. Each algorithm is implemented per-language under `src/<lang>/` and exercised through one uniform `invoke test` harness.

## Project shape

`tasks.py` (invoke) is the harness: it reads `config.yml` for per-language docker images and script invokers, then runs each source file inside its language's container against fixtures in `data/`. `snippets/` holds trimmed copies used for sharing. There is no application server, just scripts.

## Repo boundaries

- Self-contained: no upstream pull, no downstream consumers.
- State lives only in `data/` fixtures and generated `data/output*` (gitignored).
- No Forgejo pushurl. Changes land via GitHub PR on `coilysiren/algo-zone`.

## Commands

Route every dev command through coily, which reads [`.coily/coily.yaml`](.coily/coily.yaml). Run algorithms with `invoke test <language> <script> <data_index>` (see [README.md](README.md)).

## Validation

`pre-commit` runs the agentic-os hook suite (see `.pre-commit-config.yaml`). Run it clean before landing. Never `--no-verify`. Algorithm runs themselves go through docker via `invoke test`.

## Safety

Inherited from the global `AGENTS.md` chain. Never `--no-verify`. Readonly git and shell commands run without confirmation.

## Cross-repo contracts

None. This repo exposes no API and shares no schema with other repos. Each language folder only has to satisfy `tasks.py`'s uniform "run one file, emit an output file" contract.

## Release

No release artifact. Merging to `main` is the only "ship". There is no tag, package, or formula bump.

## Agent rules

- Keep inline comments to at most two contiguous lines, each <= 90 chars (the `code-comments` hook). Move longer explanation into prose docs.
- When adding a language, follow the "New Languages" steps in [README.md](README.md): add it to `config.yml`, create `src/<lang>/`, handle special cases in `tasks.py`.

## See also

- [README.md](README.md) - human-facing intro and quick start.
- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [.coily/coily.yaml](.coily/coily.yaml) - allowlisted commands.

Cross-reference convention from [coilysiren/agentic-os#59](https://github.com/coilysiren/agentic-os/issues/59).
