---
name: hermes
description: This skill should be used when self-hosting, installing, configuring, operating, updating, troubleshooting, or learning to use NousResearch Hermes Agent, including CLI usage, gateway and Slack setup, plugins, tools, skills, profiles, memory, MCP, cron, Kanban, delegate_task subagents, dashboards, and tmux-managed Hermes sessions.
---

# Hermes

## Use First

Use this skill for Hermes Agent self-hosting and day-to-day operation: install, setup, model/provider selection, gateway platforms, Slack channel setup, command discovery, updates, plugins, tools, skills, memory, profiles, MCP, cron, Kanban, `delegate_task` subagents, logs, dashboards, tutorials, and long-running tmux sessions.

Do not rely on stale remembered commands. Hermes changes quickly. At the start of each Hermes task, resolve `scripts/hermes_check.py` relative to this skill directory and run:

```bash
python3 <skill-dir>/scripts/hermes_check.py --json
```

If command behavior matters, also refresh the generated local command snapshot:

```bash
python3 <skill-dir>/scripts/hermes_check.py --write-help <skill-dir>/references/command-map.generated.md
```

Report update availability before changing configuration. Do not run `hermes update` without explicit user approval unless the user already asked to update.

## Decision Flow

1. Verify local state with `scripts/hermes_check.py`.
2. Use `hermes --help` and `hermes <command> --help` as the source of truth for executable commands.
3. Load only the needed reference file:
   - `references/setup-and-update.md` for install, versioning, updates, config health, backups, and safe update policy.
   - `references/getting-started-tutorials.md` for first-run setup, self-hosting paths, guided usage flows, and user-facing tutorials.
   - `references/command-catalog.md` for command categories and common CLI patterns.
   - `references/official-links.md` for official docs, release, reference, and troubleshooting links.
   - `references/slack-gateway.md` for Slack app, channel, Socket Mode, manifest, gateway, and allowlist setup.
   - `references/operations-runbook.md` for tmux sessions, one-shot execution, profiles, cron, webhooks, memory, skills, and autonomy guardrails.
   - `references/kanban-operations.md` for durable task boards, profile workers, dependencies, isolated workspaces, dispatch, and task notifications.
   - `references/delegation-vs-kanban.md` for `delegate_task`, subagent delegation, and choosing between delegation, Kanban, tmux, cron, and background terminal work.
   - `references/slash-commands.md` for in-session `/...` commands, gateway slash commands, and when to prefer CLI commands.
   - `references/providers-tools-security.md` for key paths, config sections, providers, toolsets, approval modes, redaction, and privacy.
   - `references/plugins-and-tools.md` for user/operator plugin installation, tool enablement, MCP connections, and safe verification.
   - `references/voice-and-media.md` for STT, TTS, voice mode, image input, and media-related troubleshooting.
   - `references/self-improvement.md` for updating this skill after new Hermes behavior, command changes, or operational lessons are discovered.
   - `references/troubleshooting.md` for logs, Slack failures, token problems, stale skills, gateway issues, and community-known pitfalls.
   - `references/command-map.generated.md` only when exact local help output is needed.
4. For interactive Hermes or `tmux` work, read the current pane before sending keys. Explain prompts and recommend a choice before sending input.
5. Prefer deterministic commands and scripts for inspection. Keep non-deterministic guidance in reference docs or in the Hermes conversation itself.
6. At the end of each Hermes task, run the self-improvement review in `references/self-improvement.md`.

## Common Request Routing

- "Install Hermes" or "self-host Hermes" -> `getting-started-tutorials.md`, `setup-and-update.md`, then `official-links.md`.
- "Set up Slack channel" -> `slack-gateway.md`, run `scripts/hermes_slack_check.py`, then `troubleshooting.md`.
- "Check if my Hermes is healthy" -> run `scripts/hermes_ops_check.py`, then `setup-and-update.md`.
- "Enable a plugin/tool/MCP server" -> `plugins-and-tools.md`, `providers-tools-security.md`.
- "Teach me how to use Hermes" -> `getting-started-tutorials.md`, `slash-commands.md`, `command-catalog.md`.
- "Use Kanban", "dispatch workers", or "coordinate profiles" -> `kanban-operations.md`, `operations-runbook.md`.
- "Use delegate_task", "delegate this", "spawn subagents", or "parallel subtasks" -> `delegation-vs-kanban.md`; use Kanban instead when the work must be durable, human-visible, restartable, or assigned to named profiles.

## Current CLI Baseline

As of Hermes Agent v0.12.0, prefer:

```bash
hermes
hermes chat -q "single query"
hermes -z "script-friendly one-shot"
hermes setup
hermes model
hermes doctor
hermes config check
hermes update --check
hermes gateway setup
hermes gateway status
hermes slack manifest
```

Avoid old third-party examples built around `hermes run`; current Hermes does not expose `run` as a root command in v0.12.0.

## Safety Rules

- Treat `~/.hermes/.env`, Slack tokens, OAuth tokens, and `~/.hermes/auth.json` as secrets. Never print full token values.
- Set or verify allowlists before enabling Slack or other gateways.
- Use `hermes update --check` before update decisions; use `hermes backup` or the update backup flags for risky changes.
- For automation, start with read-only/reporting workflows, add verification, then schedule with cron/webhooks only after repeated successful manual runs.
- Prefer files over chat for durable Hermes behavior: `config.yaml`, `.env`, `SOUL.md`, `AGENTS.md`, skills, and runbooks.
