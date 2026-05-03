# Hermes Skill

[![skills.sh](https://skills.sh/b/dandacompany/hermes-skill)](https://skills.sh/dandacompany/hermes-skill)

Agent skill for configuring, operating, updating, troubleshooting, and extending [NousResearch Hermes Agent](https://github.com/NousResearch/hermes-agent).

This skill keeps `SKILL.md` lean and routes detailed procedures into references for:

- setup, updates, backups, and health checks
- exact local CLI discovery through `hermes --help` and `hermes <command> --help`
- Slack gateway setup with Socket Mode
- tmux-managed Hermes sessions
- in-session slash commands
- providers, toolsets, config paths, security, and privacy toggles
- voice, transcription, TTS, image input, and media troubleshooting
- Hermes source-level developer/contributor reference
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
Use the hermes skill and configure Slack gateway step by step.
```

The skill begins every task by checking the local Hermes installation:

```bash
python3 scripts/hermes_check.py --json
```

Refresh the generated local command map after Hermes updates:

```bash
python3 scripts/hermes_check.py --write-help references/command-map.generated.md
```

## Why This Exists

Hermes Agent changes quickly. Third-party examples can become stale, especially around CLI commands. This skill treats the local Hermes executable as the source of truth and keeps long guidance outside `SKILL.md` so agents load only the references needed for the task.

## Notes

- Do not print full API keys, Slack tokens, or OAuth credentials.
- Run `hermes update --check` before update decisions.
- Do not run `hermes update` without explicit approval.
- Prefer foreground `hermes gateway run` while debugging Slack, then install/start the gateway service after validation.

## Sources

- Official Hermes docs: https://hermes-agent.nousresearch.com/docs/
- Hermes GitHub: https://github.com/NousResearch/hermes-agent
- skills.sh docs: https://skills.sh/docs
