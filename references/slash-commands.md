# Slash Commands

Use this reference when controlling an interactive Hermes session. Exact availability can vary by version and platform; run `/help` inside Hermes or inspect official docs if a command fails.

## When To Use Slash Commands

Use slash commands when already inside an interactive CLI or gateway conversation. Use `hermes <command>` CLI commands for deterministic scripting, setup, automation, or when no session is running.

After config, skill, or tool changes, prefer `/reset` or a fresh `hermes` process so the next session loads the new state.

## Session Control

| Command | Purpose |
| --- | --- |
| `/new` or `/reset` | Start a fresh session and reload tools/skills/config snapshots. |
| `/clear` | Clear the terminal view and start fresh in CLI. |
| `/retry` | Retry the previous user request. |
| `/undo` | Remove the last exchange. |
| `/title <name>` | Name the current session. |
| `/compress` | Manually compact context. |
| `/stop` | Stop background processes started by the agent. |
| `/rollback [N]` | Restore a filesystem checkpoint when checkpoints are enabled. |
| `/background <prompt>` | Run a prompt in the background. |
| `/queue <prompt>` | Queue work for the next turn. |
| `/resume [name]` | Resume a named session when supported. |

## Configuration

| Command | Purpose |
| --- | --- |
| `/config` | Show current config in CLI. |
| `/model [name]` | Show or change model. |
| `/personality [name]` | Set personality when enabled. |
| `/reasoning [level]` | Set or display reasoning level. |
| `/verbose` | Cycle verbosity modes. |
| `/voice on` | Voice-to-voice mode. |
| `/voice tts` | Always respond with voice when supported. |
| `/voice off` | Disable voice mode. |
| `/yolo` | Toggle approval bypass for the current context. Use sparingly. |
| `/skin [name]` | Change CLI theme. |
| `/statusbar` | Toggle CLI status bar. |

## Tools, Skills, Plugins

| Command | Purpose |
| --- | --- |
| `/tools` | Manage enabled tools interactively. |
| `/toolsets` | List toolsets. |
| `/skills` | Search, install, or manage skills. |
| `/skill <name>` | Load a specific skill into the session. |
| `/cron` | Manage cron jobs from a session. |
| `/reload-mcp` | Reload MCP servers. |
| `/plugins` | List plugins. |

## Gateway Commands

These are most useful from Slack, Discord, Telegram, or another gateway platform.

| Command | Purpose |
| --- | --- |
| `/approve` | Approve a pending command. |
| `/deny` | Deny a pending command. |
| `/restart` | Restart the gateway. |
| `/sethome` | Set the current chat/channel as the home delivery target. |
| `/update` | Update Hermes from a gateway context. Confirm before using. |
| `/platforms` or `/gateway` | Show platform connection status. |

## Utility And Info

| Command | Purpose |
| --- | --- |
| `/branch` or `/fork` | Branch the current session. |
| `/fast` | Toggle faster/priority processing when supported. |
| `/browser` | Open a CDP browser connection. |
| `/history` | Show conversation history in CLI. |
| `/save` | Save conversation to file. |
| `/paste` | Attach clipboard image in CLI. |
| `/image` | Attach a local image file. |
| `/help` | Show help. |
| `/commands [page]` | Browse gateway command pages. |
| `/usage` | Show token/cost usage. |
| `/insights [days]` | Show usage analytics. |
| `/status` | Show session or gateway status. |
| `/profile` | Show active profile information. |
| `/quit`, `/exit`, `/q` | Exit CLI. |

## Practical Rules

- Prefer `/sethome` from the actual Slack channel when configuring proactive cron or webhook delivery.
- Prefer `/approve` and `/deny` in gateway workflows instead of trying to approve from local CLI.
- Use `/reset` after changing tools, skills, config, or secret redaction settings.
- Use `/rollback` only after confirming checkpoints are enabled for the session.
