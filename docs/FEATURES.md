# algo-zone features

Baseline inventory of what `algo-zone` ships. Update when a headline feature is added, removed, or materially reshaped.

## Harness

- `tasks.py` (invoke) - one uniform `invoke test <language> <script> <data_index>` entry point that runs any language's source file in docker against `data/` fixtures.
- `config.yml` - per-language docker image, script invoker, and special-case keys.

## Algorithms

- Sorting - `sort_builtin`, `sort_bubble_sort`, `sort_insertion_sort`, `sort_selection_sort`, `sort_merge_sort` across Python, Ruby, Go, JS, and Rust (coverage varies per language).
- SQL - a small `INSERT INTO` / query exercise in Python and Ruby.
- Tokenizer - a tokenizer script exercise in Python.

## Layout

- `src/<lang>/` - canonical per-language implementations.
- `snippets/<lang>/` - trimmed copies for sharing.
- `data/` - input fixtures; `data/output*` is generated and gitignored.

## See also

- [README.md](../README.md) - human-facing intro.
- [AGENTS.md](../AGENTS.md) - agent-facing operating rules.
- [.coily/coily.yaml](../.coily/coily.yaml) - allowlisted commands.

Cross-reference convention from [coilysiren/agentic-os#59](https://github.com/coilysiren/agentic-os/issues/59).
