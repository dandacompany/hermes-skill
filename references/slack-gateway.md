# Slack Gateway

Use this reference for Hermes Slack channel setup. Hermes uses modern Slack Bolt with Socket Mode, not deprecated Classic RTM apps.

## Recommended Setup Shape

1. Check local Hermes state:

```bash
python3 /Users/dante/.agents/skills/hermes/scripts/hermes_check.py --json
hermes slack manifest --help
hermes gateway setup --help
```

2. Generate a Slack app manifest when possible:

```bash
hermes slack manifest
```

If the command supports output flags in local help, write the manifest to a file and use it in Slack app creation.

3. Create or update the Slack app at `https://api.slack.com/apps`.
4. Enable Socket Mode.
5. Create tokens:
   - Bot Token: starts with `xoxb-`.
   - App-Level Token: starts with `xapp-`.
6. Subscribe to events and add scopes.
7. Configure Hermes through the interactive wizard:

```bash
hermes gateway setup
```

8. Start in foreground for debugging:

```bash
hermes gateway run
```

9. After successful messages, install/start as a service:

```bash
hermes gateway install
hermes gateway start
hermes gateway status
```

## Required Slack Details

Official docs call out these essentials:

- Use Socket Mode so no public HTTP endpoint is required.
- Classic Slack Apps are deprecated; create a modern app.
- Set `SLACK_ALLOWED_USERS` with authorized Slack member IDs.
- Store tokens in `~/.hermes/.env` with restrictive permissions.
- Invite the bot to every channel where it should respond.

Important channel items:

- Public channels need `message.channels` event and `channels:history` scope.
- Private channels need `message.groups` event and `groups:history` scope.
- App mentions need `app_mention` event.
- Reinstall the Slack app after changing scopes or event subscriptions.
- Use `/invite @Hermes Agent` in the target channel.

## Home Channel

Set a home channel for cron results and proactive notifications:

```bash
SLACK_HOME_CHANNEL=C01234567890
```

Find the channel ID in Slack channel details. Verify the bot is invited to that channel.

## Common Config Values

Token environment variables commonly used by Hermes Slack:

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_ALLOWED_USERS=U012ABCDEF,U034GHIJKL
SLACK_HOME_CHANNEL=C01234567890
```

Do not duplicate prefixes. If a wizard field already shows `xoxb-` or `xapp-`, paste only the portion it asks for. If it asks for the full token, paste the full token exactly once.

## Channel Behavior

Use channel-level controls when needed:

```yaml
slack:
  require_mention: true
  unauthorized_dm_behavior: "pair"
  channel_prompts:
    "C01RESEARCH": |
      Focus on academic sources and concise synthesis.
platforms:
  slack:
    reply_to_mode: "first"
    extra:
      reply_in_thread: true
      reply_broadcast: false
```

Before editing config directly, prefer `hermes gateway setup` and `hermes config edit`. Validate with `hermes config check`.

## Debug Checklist

If Slack does not respond in a channel:

1. Check gateway is running: `hermes gateway status`.
2. Check logs: `hermes logs --component gateway --since 1h` or `hermes logs errors`.
3. Confirm bot is invited to the channel.
4. Confirm `SLACK_ALLOWED_USERS` includes the sender's Slack member ID.
5. Confirm events and scopes are present.
6. Reinstall the app after scope/event changes.
7. Restart gateway: `hermes gateway restart` or stop/start foreground `gateway run`.
8. Confirm the App-Level token is `xapp-` and the Bot token is `xoxb-`.

Community reports commonly mention invalid token loops caused by pasting token prefixes twice, missing channel events, or assuming public-channel access works without inviting the bot.
