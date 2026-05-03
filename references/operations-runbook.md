# Hermes Operations Runbook

Use this reference for operating Hermes over time, especially with tmux, profiles, recurring jobs, and bounded autonomy.

## tmux Managed Hermes Sessions

For an existing tmux session:

```bash
tmux capture-pane -t hermes -p | tail -40
tmux send-keys -t hermes -l -- "message"
tmux send-keys -t hermes Enter
```

Always capture before sending input. If Hermes shows an interactive prompt, explain what it asks, recommend an option, and wait for the user's decision before sending keys.

For a new interactive session:

```bash
tmux new-session -d -s hermes -x 120 -y 40 'hermes'
```

Use `hermes -w` for isolated worktree mode when multiple Hermes agents edit code in parallel.

## One-Shot And Background Work

Use `chat -q` for normal single queries:

```bash
hermes chat -q "Inspect this project and summarize risks"
```

Use `-z` for scripts and pipes that require only final answer text:

```bash
hermes -z "Return a JSON checklist for today's gateway health"
```

For long-running autonomous work, prefer tmux so the process stays observable.

## Profiles

Profiles isolate config, sessions, skills, and memory:

```bash
hermes profile list
hermes profile create slack-prod
hermes profile use slack-prod
hermes -p slack-prod
```

Use profiles for distinct agents, workspaces, or safety domains.

## Bounded Autonomy

Community practice is consistent: do not start with "run everything." Start with one narrow workflow.

Good autonomy ladder:

1. Read-only inspection with citations/logs.
2. Draft recommendations.
3. Human-approved changes.
4. Scheduled read-only report.
5. Scheduled changes only after repeated clean manual runs.

Every recurring workflow should define:

- Inputs it may read.
- Outputs it must write.
- Actions it may never take.
- Verification evidence required before "done."
- Log path or delivery channel.
- Escalation condition for human approval.

Use files for durable behavior. Put stable operating rules in `AGENTS.md`, `SOUL.md`, skills, runbooks, `config.yaml`, and `.env`; do not rely on chat memory alone.

## Cron And Webhooks

Use cron for recurring jobs:

```bash
hermes cron list
hermes cron create "every 2h"
hermes cron status
```

Use webhooks for event-driven work:

```bash
hermes webhook subscribe <name>
hermes webhook list
hermes webhook test <name>
```

Route proactive messages to a configured home channel, such as `SLACK_HOME_CHANNEL`.

## Kanban Boards

Use Kanban when work should be durable, assigned to profiles, dependency-aware, and resumable across gateway or CLI sessions.

```bash
hermes kanban init
hermes kanban create "Draft weekly report" --assignee research --workspace scratch
hermes kanban list
hermes kanban dispatch --dry-run
```

Use `references/kanban-operations.md` for worker profiles, isolated workspaces, dispatch behavior, notifications, and cleanup.

## Delegation Vs Durable Work

Use `delegate_task` for short isolated subagent work that the current parent turn must wait for, such as parallel research or fresh-context review. Use Kanban, cron, background terminal, or tmux when work should outlive the current turn.

Use `references/delegation-vs-kanban.md` before designing multi-agent workflows, especially when choosing between anonymous subagents and named profile workers.

## Memory And Skills

Use:

```bash
hermes memory status
hermes memory setup
hermes skills list
hermes skills config
hermes skills check
hermes skills update
```

Keep skills focused. Avoid one giant skill that tries to run a full business process end to end. Split repeated deterministic actions into scripts and keep guidance in references.

## MCP And Tools

Use:

```bash
hermes tools list
hermes tools enable <toolset>
hermes mcp list
hermes mcp test <name>
hermes mcp configure <name>
```

After tool or MCP changes, start a fresh session or use the relevant Hermes slash command to reload if available in current help.
