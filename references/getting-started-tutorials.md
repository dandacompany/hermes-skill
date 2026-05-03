# Getting Started Tutorials

Use this reference for user-facing setup and self-hosting walkthroughs. Keep the user in the loop for interactive prompts, secrets, platform app creation, and update decisions.

## Tutorial 1: First Local Setup

Goal: get a working local Hermes CLI.

Prerequisites:

- macOS, Linux, or WSL2.
- A terminal with network access.
- At least one model/provider credential or OAuth flow available.

Expected result:

- `hermes doctor` passes or reports only understood optional warnings.
- `hermes chat -q ...` returns a model response.

1. Install Hermes from the official installer:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

2. Confirm the executable and version:

```bash
hermes --version
```

3. Run the setup wizard:

```bash
hermes setup
```

4. Pick a model/provider:

```bash
hermes model
```

5. Diagnose:

```bash
hermes doctor
hermes config check
```

6. Try a single query:

```bash
hermes chat -q "Say hello and confirm the active model."
```

If it fails:

- Run `hermes doctor` and `hermes config check`.
- Confirm `.env` exists with `hermes config env-path`.
- Re-run `hermes model` if provider credentials are missing.

## Tutorial 2: Self-Hosted Gateway

Goal: run Hermes as a persistent messaging gateway.

Prerequisites:

- Local Hermes CLI already works.
- Gateway platform account/app is ready or can be created.
- A stable host such as a VPS, home server, always-on workstation, WSL2 with systemd, or macOS launchd.

1. Configure providers and API keys first.
2. Configure gateway platforms:

```bash
hermes gateway setup
```

3. Debug in foreground:

```bash
hermes gateway run
```

4. After the platform works, install and start the service:

```bash
hermes gateway install
hermes gateway start
hermes gateway status
```

5. Use logs for verification:

```bash
hermes logs --component gateway --since 1h
hermes logs errors
```

Prefer foreground mode until tokens, allowlists, channel membership, and replies are verified.

Verification:

```bash
python3 <skill-dir>/scripts/hermes_ops_check.py
```

If service mode fails, return to `hermes gateway run` and inspect logs before changing platform settings.

## Tutorial 3: Slack Channel Bot

Use `references/slack-gateway.md` for the detailed setup. The short flow:

1. Generate or inspect manifest: `hermes slack manifest`.
2. Create Slack app with Socket Mode.
3. Set bot token, app token, allowed users, and home channel.
4. Invite bot to the target channel.
5. Run `hermes gateway run` and test a mention.
6. Move to service mode after logs are clean.

Verification:

```bash
python3 <skill-dir>/scripts/hermes_slack_check.py
```

Manual checks still required:

- Bot is invited to the channel.
- App was reinstalled after scope/event changes.
- Public channels include `message.channels`; private channels include `message.groups`.
- Sender's Slack member ID is allowed.

## Tutorial 4: Daily CLI Use

Common patterns:

```bash
hermes
hermes chat -q "Summarize the current project."
hermes -z "Return only a compact status report."
hermes --continue
hermes sessions list
hermes sessions browse
```

Inside the session, use `/help`, `/tools`, `/skills`, `/usage`, `/reset`, and `/quit`.

Useful interaction habits:

- Use `Ctrl+C` to interrupt a run.
- Use `/title` to name important sessions.
- Use `hermes --continue` to resume the latest session.
- Use `hermes sessions browse` when you need an older session.

## Tutorial 5: Safe Automation

Build automation gradually:

1. Manual one-shot task:

```bash
hermes chat -q "Check the gateway health and summarize issues."
```

2. Add structured output or a file destination.
3. Add cron only after repeated successful manual runs:

```bash
hermes cron create "every 2h"
hermes cron list
hermes cron status
```

4. Deliver proactive messages only after `SLACK_HOME_CHANNEL` or another home target is verified.

Operator rule: automation should start read-only, then produce drafts, then request approval, and only later make changes unattended.

## Tutorial 6: Profiles For Separate Agents

Use profiles to isolate experiments, production gateways, and personal workflows:

```bash
hermes profile list
hermes profile create slack-prod
hermes -p slack-prod setup
hermes -p slack-prod gateway setup
```

Keep production gateways and experimental agents in separate profiles.

Verification:

```bash
hermes -p slack-prod doctor
hermes -p slack-prod gateway status
```

## Tutorial 7: Updating Safely

Check first:

```bash
hermes update --check
```

Back up and update only after approval:

```bash
hermes backup -l before-update
hermes update --backup
```

After update:

```bash
hermes doctor
hermes config check
python3 <skill-dir>/scripts/hermes_check.py --write-help <skill-dir>/references/command-map.generated.md
```

## Tutorial 8: Plugins, Tools, And MCP

Goal: add capabilities without exposing more power than needed.

1. Inspect current tools:

```bash
hermes tools list
```

2. Search or inspect skills/plugins/MCP docs before installing:

```bash
hermes skills search <query>
hermes plugins list
hermes mcp list
```

3. Add only one new capability at a time.
4. Restart or `/reset`.
5. Run a narrow test and inspect logs.

Use `references/plugins-and-tools.md` for detailed operator workflow.

## Tutorial 9: Kanban For Profile Workers

Goal: create durable tasks that named Hermes profiles can claim and execute.

1. Create or verify worker profiles:

```bash
hermes profile list
hermes profile create research
```

2. Initialize the board:

```bash
hermes kanban init
```

3. Create a task:

```bash
hermes kanban create "Research Hermes gateway health checks" \
  --assignee research \
  --workspace scratch \
  --body "Find official docs and summarize operator steps."
```

4. Preview dispatch:

```bash
hermes kanban dispatch --dry-run
```

5. Dispatch through the gateway or one pass:

```bash
hermes gateway start
hermes kanban dispatch --max 1
```

6. Watch progress:

```bash
hermes kanban watch
hermes kanban list
hermes kanban log <task_id>
hermes kanban runs <task_id>
```

Use `references/kanban-operations.md` before creating production task boards.
