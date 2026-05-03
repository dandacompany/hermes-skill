# Developer Reference

Use this reference when extending Hermes itself, reviewing a Hermes PR, adding tools or slash commands, or debugging source-level behavior.

## Source Locations

Find local source with:

```bash
hermes --version
```

Common source layout in a git-installed Hermes tree:

| Path | Purpose |
| --- | --- |
| `run_agent.py` | Core conversation loop and agent orchestration. |
| `model_tools.py` | Tool discovery and dispatch path. |
| `toolsets.py` | Toolset definitions. |
| `cli.py` | Interactive CLI behavior. |
| `hermes_state.py` | SQLite session store. |
| `agent/` | Prompt building, compression, memory, routing, credentials, skill dispatch. |
| `hermes_cli/commands.py` | Slash command registry. |
| `hermes_cli/config.py` | Default config and env var definitions. |
| `hermes_cli/main.py` | CLI entry point and argparse. |
| `tools/` | Built-in tool implementations. |
| `tools/registry.py` | Tool registry. |
| `gateway/` | Messaging gateway. |
| `gateway/platforms/` | Platform adapters. |
| `cron/` | Scheduler and cron jobs. |
| `tests/` | Pytest suite. |
| `website/` | Documentation site. |

Use `rg` in the source tree rather than assuming filenames are unchanged.

## Adding A Tool

Typical flow:

1. Create a module under `tools/`.
2. Register the tool with the central registry.
3. Associate it with a toolset.
4. Provide a requirement check so unavailable tools do not appear.
5. Add tests.

Implementation rules:

- Return JSON strings from tool handlers.
- Use Hermes path helpers such as `get_hermes_home()` instead of hardcoding `~/.hermes`.
- Put config in `config.yaml` and secrets in `.env`.
- Keep tool schemas precise and small.
- Do not add side-effecting tools to broad/default toolsets without a reason.

## Adding A Slash Command

Typical flow:

1. Add a command definition to the central command registry.
2. Add CLI handling.
3. Add gateway handling if the command should work from Slack/Discord/etc.
4. Verify help, autocomplete, and platform command mappings derive from the registry.
5. Add tests for both CLI and gateway behavior where relevant.

Run:

```bash
hermes --help
hermes <command> --help
```

after changes to confirm public command shape.

## Agent Loop Model

High-level loop:

1. Build system prompt and context.
2. Call the selected model with messages and tool schemas.
3. Dispatch tool calls through the registry.
4. Append tool results.
5. Continue until final text response or max iterations.
6. Compress context as thresholds are reached.

Important invariants:

- Do not break message role alternation.
- Avoid changing system prompt/tool definitions mid-conversation because it can break prompt caching.
- Start a new session when changing tools, skills, or core config.

## Testing

From the Hermes source tree:

```bash
python -m pytest tests/ -o 'addopts=' -q
python -m pytest tests/tools/ -q
python -m pytest tests/gateway/ -q
```

Testing rules:

- Tests should redirect `HERMES_HOME` to temp directories.
- Do not touch real `~/.hermes` in tests.
- Run focused tests first, then broader tests before pushing.
- Include migration/config tests for schema or default changes.

## Commit And Review Rules

Use concise conventional prefixes such as `fix:`, `feat:`, `refactor:`, `docs:`, and `chore:`.

Before landing:

```bash
hermes config check
python -m pytest tests/ -o 'addopts=' -q
```

When reviewing changes, prioritize:

- Backward compatibility of config and env vars.
- Prompt/tool schema stability.
- Gateway platform regressions.
- Secret/PII handling.
- Provider routing and fallback behavior.
- Tests for migrations and new tool availability checks.

## When To Use Official Developer Docs

Use official docs for source-level work:

- Developer guide: `https://hermes-agent.nousresearch.com/docs/developer-guide/`
- CLI reference: `https://hermes-agent.nousresearch.com/docs/reference/cli-commands`
- Tools reference: `https://hermes-agent.nousresearch.com/docs/reference/tools-reference`
- Slash commands: `https://hermes-agent.nousresearch.com/docs/reference/slash-commands`
