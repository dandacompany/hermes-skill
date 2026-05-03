# Hermes Troubleshooting

Use this reference when Hermes commands, gateway, Slack, tools, skills, or updates behave unexpectedly.

## First Triage

```bash
hermes --version
hermes update --check
hermes doctor
hermes config check
hermes status --all
hermes logs errors
```

When a command fails, immediately run:

```bash
hermes <command> --help
```

Do not assume old blog or third-party examples are still valid.

## Logs

Use:

```bash
hermes logs
hermes logs errors
hermes logs --since 1h
hermes logs -f
```

For gateway:

```bash
hermes gateway status
hermes logs --component gateway --since 1h
```

Redact tokens, email addresses, phone numbers, channel IDs if needed, and auth payloads before sharing.

## Slack Issues

No response in channel:

- Bot not invited to channel.
- Missing `message.channels` or `message.groups` event.
- Missing history scope.
- App not reinstalled after scope/event changes.
- Sender not included in `SLACK_ALLOWED_USERS`.
- Gateway not running or running old config.
- Mention required but message did not mention the bot.

Invalid token:

- Bot token must start with `xoxb-`.
- App-Level token must start with `xapp-`.
- Do not paste `xoxb-` or `xapp-` twice into setup fields.
- Rotate and reinstall tokens if Slack app settings changed.

Debug:

```bash
hermes gateway run
hermes logs errors
hermes config env-path
```

## Skills Not Updating

Hermes protects user-modified bundled skills. If an upstream bundled skill is stale:

```bash
hermes skills check
hermes skills update
hermes skills reset <skill-name>
```

Use `--restore --yes` only when replacing the local copy is intended.

## Tools Missing

```bash
hermes tools
hermes tools list
hermes tools enable <name>
```

Start a new session after changing toolsets. Some tools require `.env` keys.

## Gateway Service Problems

Foreground debug first:

```bash
hermes gateway run
```

Then service mode:

```bash
hermes gateway install
hermes gateway restart
hermes gateway status
```

If service startup fails, inspect OS service logs plus `~/.hermes/logs/`.

## Update Problems

Check without changing:

```bash
hermes update --check
```

Before applying:

```bash
hermes backup -l before-update
```

Apply:

```bash
hermes update --backup
```

If local source has changes, do not discard them blindly. Inspect `~/.hermes/hermes-agent` git status and ask before destructive cleanup.
