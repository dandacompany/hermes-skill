# Kanban Operations

Use this reference when coordinating durable Hermes tasks across profiles. Kanban is for operator-managed task boards, not for ad hoc one-turn prompts.

## Concept

Hermes Kanban is a SQLite-backed board shared across Hermes profiles. Tasks are durable, can depend on other tasks, and can be claimed atomically by named profiles. Workers execute tasks in isolated workspaces.

Use Kanban when work needs:

- Durable task state across sessions.
- Profile-specific workers.
- Dependencies between tasks.
- A log and run history.
- Gateway-visible progress.
- Safer parallel execution through isolated workspaces.

Do not use Kanban for simple one-shot questions; use `hermes chat -q` or `hermes -z` instead.

## Core Objects

| Object | Meaning |
| --- | --- |
| Board | Shared SQLite task board under Hermes home. |
| Task | A durable unit of work with title, body, status, assignee, tenant, priority, and workspace. |
| Assignee | A Hermes profile name that should execute the task. |
| Workspace | Where the worker runs: `scratch`, `worktree`, or `dir:<path>`. |
| Parent | Dependency relationship; children wait for parent completion. |
| Worker | Hermes process spawned for a task. |
| Event | Task lifecycle record, comment, heartbeat, or worker output event. |

## Lifecycle

Common statuses from local help:

- `triage`: parked for specification.
- `todo` / `ready`: waiting to be run.
- `running`: claimed or executing.
- `blocked`: paused due to failure or operator decision.
- `done`: completed.
- `archived`: hidden from normal lists.

Use:

```bash
hermes kanban list
hermes kanban list --status ready
hermes kanban show <task_id>
hermes kanban stats
```

## Setup

Initialize idempotently:

```bash
hermes kanban init
```

List worker profiles:

```bash
hermes kanban assignees
hermes profile list
```

Create profiles before assigning production work:

```bash
hermes profile create research
hermes profile create coding
```

## Creating Tasks

Basic task:

```bash
hermes kanban create "Summarize gateway logs" \
  --assignee research \
  --workspace scratch \
  --body "Inspect recent logs and produce an operator summary."
```

Worktree task for code changes:

```bash
hermes kanban create "Fix Slack gateway docs" \
  --assignee coding \
  --workspace worktree \
  --skill hermes \
  --max-runtime 30m
```

Task in a known directory:

```bash
hermes kanban create "Run app QA" \
  --assignee qa \
  --workspace dir:/path/to/project
```

Use `--idempotency-key` for tasks created by automation so retries do not duplicate work.

## Dependencies

Link parent and child tasks:

```bash
hermes kanban link <parent_id> <child_id>
hermes kanban unlink <parent_id> <child_id>
```

Print the context a worker will see:

```bash
hermes kanban context <task_id>
```

Use dependencies when one task produces information another task must consume.

## Dispatch

Preview first:

```bash
hermes kanban dispatch --dry-run
```

Run one dispatcher pass:

```bash
hermes kanban dispatch --max 1
```

Current local help says `hermes kanban daemon` is deprecated. The dispatcher now runs in the gateway; use:

```bash
hermes gateway start
hermes gateway status
```

Use `dispatch --dry-run` before enabling unattended dispatch.

## Worker Monitoring

Watch board events:

```bash
hermes kanban watch
hermes kanban tail <task_id>
```

Inspect worker logs and attempts:

```bash
hermes kanban log <task_id>
hermes kanban runs <task_id>
```

Workers can emit liveness signals:

```bash
hermes kanban heartbeat <task_id>
```

## Updating Tasks

Comment:

```bash
hermes kanban comment <task_id> "Need approval before changing production config."
```

Complete:

```bash
hermes kanban complete <task_id>
```

Block/unblock:

```bash
hermes kanban block <task_id>
hermes kanban unblock <task_id>
```

Archive:

```bash
hermes kanban archive <task_id>
```

## Gateway Notifications

Kanban can subscribe a gateway source to task terminal events:

```bash
hermes kanban notify-subscribe <task_id> \
  --platform slack \
  --chat-id <channel_id> \
  --user-id <user_id>
```

List and remove subscriptions:

```bash
hermes kanban notify-list
hermes kanban notify-list <task_id>
hermes kanban notify-unsubscribe <subscription_id>
```

Prefer gateway slash commands when the user is already in Slack/Telegram and Hermes supports them.

## Cleanup

Garbage-collect old archived workspaces, logs, and terminal events:

```bash
hermes kanban gc
hermes kanban gc --event-retention-days 30 --log-retention-days 30
```

Review before running cleanup on boards with compliance or audit requirements.

## Workspace Choice

| Workspace | Use when |
| --- | --- |
| `scratch` | Research, summarization, isolated temporary work. |
| `worktree` | Code changes in a git repo where parallel workers may edit files. |
| `dir:<path>` | The task must run in a specific existing project or data directory. |

Use `worktree` for concurrent coding. Avoid `dir:<path>` for multiple writing workers unless file ownership is clear.

## Safety Rules

- Create worker profiles before production dispatch.
- Use `--max-runtime` on tasks that might run long.
- Use `--dry-run` before dispatching unattended.
- Use `--skill` to force-load relevant operating instructions into workers.
- Keep task bodies explicit: goal, allowed files/systems, verification, and done criteria.
- Do not expose secrets in task titles, bodies, comments, or logs.
- Prefer separate profiles for different trust boundaries.

## Example Multi-Profile Flow

```bash
hermes profile create researcher
hermes profile create implementer
hermes kanban init

research_task=$(hermes kanban create "Research Slack gateway setup" \
  --assignee researcher \
  --workspace scratch \
  --json)

impl_task=$(hermes kanban create "Apply Slack gateway docs updates" \
  --assignee implementer \
  --workspace worktree \
  --skill hermes \
  --json)

hermes kanban link <research_task_id> <impl_task_id>
hermes kanban dispatch --dry-run
hermes gateway start
```

Extract task IDs from JSON output in real automation instead of copying placeholders.
