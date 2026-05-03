# Hermes Skill

[![skills.sh](https://skills.sh/b/dandacompany/hermes-skill)](https://skills.sh/dandacompany/hermes-skill)

Agent skill for self-hosting, installing, configuring, operating, updating, troubleshooting, and learning to use [NousResearch Hermes Agent](https://github.com/NousResearch/hermes-agent).

This skill keeps `SKILL.md` lean and routes detailed procedures into references for:

- setup, updates, backups, and health checks
- first-run tutorials, self-hosted gateway setup, and daily usage flows
- read-only operations and Slack gateway checks
- exact local CLI discovery through `hermes --help` and `hermes <command> --help`
- official documentation link routing
- Slack gateway setup with Socket Mode
- tmux-managed Hermes sessions
- in-session slash commands
- providers, toolsets, config paths, security, and privacy toggles
- operator-level plugins, tools, skills, and MCP management
- voice, transcription, TTS, image input, and media troubleshooting
- self-improvement review after Hermes behavior or command changes are discovered
- profiles, cron, webhooks, skills, memory, MCP, dashboards, and logs
- troubleshooting known gateway, token, update, and stale-skill issues

## Install

```bash
npx skills add dandacompany/hermes-skill
```

To install only this skill from the repo when prompted by compatible CLIs:

```bash
npx skills add dandacompany/hermes-skill --skill hermes
```

## Usage

Ask your coding agent to use the `hermes` skill when working with Hermes Agent:

```text
Use the hermes skill and walk me through self-hosting Hermes with Slack gateway.
```

The skill begins every task by checking the local Hermes installation:

```bash
python3 scripts/hermes_check.py --json
```

Refresh the generated local command map after Hermes updates:

```bash
python3 scripts/hermes_check.py --write-help references/command-map.generated.md
```

Run read-only operations checks:

```bash
python3 scripts/hermes_ops_check.py
python3 scripts/hermes_slack_check.py
```

## What This Is

- A self-hosting and operator runbook for Hermes Agent.
- A setup and tutorial skill for users who want Hermes working locally or through gateways.
- A safety layer that checks local CLI behavior before trusting remembered commands.
- A practical guide for Slack, plugins, tools, skills, MCP, cron, profiles, and daily use.
- A Kanban operator guide for profile workers, isolated workspaces, dependencies, and task notifications.

## What This Is Not

- A source-code contribution guide for Hermes internals.
- A replacement for the official bundled `hermes-agent` skill when developing Hermes itself.
- A tool that updates Hermes or changes secrets without user approval.

## Keywords

Hermes Agent, Hermes Slack bot setup, Hermes gateway self hosting, Hermes install tutorial, Hermes operations runbook, Hermes plugins, Hermes tools, Hermes MCP, Hermes cron, Hermes profiles, Hermes Kanban.

## Why This Exists

Hermes Agent changes quickly. Third-party examples can become stale, especially around CLI commands. This skill treats the local Hermes executable as the source of truth and keeps long guidance outside `SKILL.md` so agents load only the references needed for the user's setup, operations, and learning task.

## Notes

- Do not print full API keys, Slack tokens, or OAuth credentials.
- Run `hermes update --check` before update decisions.
- Do not run `hermes update` without explicit approval.
- Prefer foreground `hermes gateway run` while debugging Slack, then install/start the gateway service after validation.

## Sources

- Official Hermes docs: https://hermes-agent.nousresearch.com/docs/
- Hermes GitHub: https://github.com/NousResearch/hermes-agent
- skills.sh docs: https://skills.sh/docs
