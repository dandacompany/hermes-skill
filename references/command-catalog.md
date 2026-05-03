# Hermes Command Catalog

Use this reference for choosing the right command family. Regenerate exact local help with `scripts/hermes_check.py --write-help references/command-map.generated.md`.

## High-Use Commands

| Task | Command |
| --- | --- |
| Interactive CLI | `hermes` or `hermes chat` |
| Single non-interactive query | `hermes chat -q "..."` |
| Script-friendly final-answer-only query | `hermes -z "..."` |
| Select model/provider | `hermes model` |
| Initial or targeted setup | `hermes setup [model|terminal|gateway|tools|agent]` |
| Diagnose | `hermes doctor`, `hermes config check`, `hermes status --all` |
| Check update | `hermes update --check` |
| Apply update | `hermes update --backup` |
| Gateway config | `hermes gateway setup` |
| Gateway service | `hermes gateway install/start/stop/restart/status` |
| Slack manifest | `hermes slack manifest` |
| Tools | `hermes tools`, `hermes tools list/enable/disable` |
| Skills | `hermes skills browse/search/inspect/install/list/check/update/config` |
| Logs | `hermes logs`, `hermes logs errors`, `hermes logs -f` |
| Profiles | `hermes profile list/create/use/show/alias/export/import` |
| Sessions | `hermes sessions list/browse/rename/export/delete/prune/stats` |

## Command Families

### Chat

Use for local interaction and one-shot calls:

```bash
hermes chat -q "Hello"
hermes chat --provider openrouter --model "anthropic/claude-sonnet-4" -q "Summarize this repo"
hermes chat --toolsets "web,terminal,skills"
hermes -z "Return only the final answer"
```

Use `-Q/--quiet` with `chat -q` when a cleaner programmatic output is enough. Use `-z` when only final text should be printed.

### Model, Auth, Fallback

Use:

```bash
hermes model
hermes login --provider nous
hermes auth add
hermes auth list
hermes fallback list
hermes fallback add
```

Prefer the interactive picker for provider-specific OAuth flows.

### Gateway And Messaging

Use:

```bash
hermes gateway setup
hermes gateway run
hermes gateway install
hermes gateway start
hermes gateway status
hermes gateway restart
```

Use foreground `gateway run` while debugging; use installed service only after the platform works.

### Skills

Use:

```bash
hermes skills browse
hermes skills search <query>
hermes skills inspect <id>
hermes skills install <id>
hermes skills list
hermes skills check
hermes skills update
hermes skills config
```

Inside Hermes chat, the same skills operations are also available through `/skills ...` slash commands.

### Tools And MCP

Use:

```bash
hermes tools
hermes tools list
hermes tools enable <name>
hermes tools disable <name>
hermes mcp list
hermes mcp add <name> --command ...
hermes mcp test <name>
hermes mcp configure <name>
```

Tool changes may require a new Hermes session or `/reset`.

### Cron, Webhooks, Kanban

Use for bounded automation after manual runs are reliable:

```bash
hermes cron list
hermes cron create "every 2h"
hermes cron status
hermes webhook subscribe <name>
hermes webhook list
hermes kanban init
```

Keep prompts narrow, log outputs, and route proactive delivery to a configured home channel.

### Dashboard, Logs, Debug

Use:

```bash
hermes dashboard --status
hermes dashboard --port 3000
hermes logs errors
hermes logs --since 1h
hermes debug share
hermes dump
```

Redact secrets before sharing dumps or logs.
