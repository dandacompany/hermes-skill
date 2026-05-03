# Getting Started Tutorials

Use this reference for user-facing setup and self-hosting walkthroughs. Keep the user in the loop for interactive prompts, secrets, platform app creation, and update decisions.

## Tutorial 1: First Local Setup

Goal: get a working local Hermes CLI.

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

## Tutorial 2: Self-Hosted Gateway

Goal: run Hermes as a persistent messaging gateway.

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

## Tutorial 3: Slack Channel Bot

Use `references/slack-gateway.md` for the detailed setup. The short flow:

1. Generate or inspect manifest: `hermes slack manifest`.
2. Create Slack app with Socket Mode.
3. Set bot token, app token, allowed users, and home channel.
4. Invite bot to the target channel.
5. Run `hermes gateway run` and test a mention.
6. Move to service mode after logs are clean.

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

## Tutorial 6: Profiles For Separate Agents

Use profiles to isolate experiments, production gateways, and personal workflows:

```bash
hermes profile list
hermes profile create slack-prod
hermes -p slack-prod setup
hermes -p slack-prod gateway setup
```

Keep production gateways and experimental agents in separate profiles.

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
