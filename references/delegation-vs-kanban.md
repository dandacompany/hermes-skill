# Delegation Vs Kanban

Use this reference when deciding whether Hermes should use `delegate_task`, Kanban, tmux, cron, or a background terminal job.

## Operator Summary

`delegate_task` is a synchronous subagent call. The parent Hermes agent forks one or more isolated child agents, waits for them, then receives only their final summaries.

Kanban is a durable local work queue. Tasks are rows in the Hermes Kanban database, can be assigned to named profiles, can be retried or blocked, and remain visible after the current turn ends.

Use `delegate_task` for short, independent reasoning work the parent needs before continuing. Use Kanban for durable coordination, profile handoff, human-visible progress, dependencies, retries, or anything that should survive interruption.

## Decision Table

| Need | Prefer |
| --- | --- |
| Parent needs a short answer before continuing | `delegate_task` |
| Parallel research or review with isolated context | `delegate_task` |
| Keep intermediate tool calls out of the parent context | `delegate_task` |
| Task must outlive the current parent turn | Kanban, cron, or background terminal |
| Named profile identity, persistent memory, or role ownership | Kanban |
| Human can comment, unblock, or audit later | Kanban |
| Dependencies between tasks | Kanban |
| Recurring schedule | Cron |
| Long shell process that should continue while Hermes does other work | Background terminal or tmux |
| Interactive operator session that must stay observable | tmux |

## How `delegate_task` Works

A parent agent calls `delegate_task` with either a single task or a `tasks` batch. Each child gets:

- A fresh conversation with no parent history.
- The `goal` and `context` fields passed by the parent.
- Its own terminal session.
- Restricted toolsets chosen for the task.
- No direct user interaction.

Only the final child summary enters the parent context. Intermediate child tool calls and observations do not.

Single task shape:

```python
delegate_task(
    goal="Compare the local Hermes help output with official docs",
    context="Use hermes --help and the current docs. Return mismatches only.",
    toolsets=["terminal", "web"]
)
```

Batch task shape:

```python
delegate_task(tasks=[
    {
        "goal": "Check official Slack gateway docs",
        "context": "Focus on app tokens, channel IDs, and Socket Mode.",
        "toolsets": ["web"]
    },
    {
        "goal": "Check local Hermes Slack configuration",
        "context": "Do not print secrets. Report missing variables only.",
        "toolsets": ["terminal", "file"]
    }
])
```

Operators usually ask Hermes in natural language instead of calling Python directly:

```text
Use delegate_task to check the official docs and local help in parallel, then summarize only the differences.
```

## Bounds And Configuration

Useful config keys under `delegation`:

| Key | Purpose |
| --- | --- |
| `max_concurrent_children` | Maximum parallel children in a batch. Default is 3. Also configurable through `DELEGATION_MAX_CONCURRENT_CHILDREN`. |
| `max_spawn_depth` | Nested delegation depth, 1-3. Default is flat delegation. |
| `orchestrator_enabled` | Global switch for orchestrator children. |
| `child_timeout_seconds` | Idle timeout for child agents. Default is 600 seconds in current docs. |
| `max_iterations` | Maximum tool-calling turns per child. |
| `model`, `provider`, `base_url`, `api_key`, `reasoning_effort` | Optional child-agent model routing. |

Child roles:

- `role="leaf"` is the default. Leaf children cannot delegate further.
- `role="orchestrator"` allows nested delegation only when `max_spawn_depth` permits it.

Blocked or restricted child capabilities include `clarify`, shared `memory` writes, cross-platform `send_message`, and leaf-child `delegate_task`.

## Observability

Use `/agents` in the Hermes TUI to inspect running and recently finished subagents. `/tasks` is an alias in current docs. The classic CLI prints a text summary.

Timeout diagnostics can be written under `~/.hermes/logs/subagent-timeout-<session>-<timestamp>.log` when a child times out before making API calls.

`delegate_task` is not a durable queue. If the parent turn is interrupted by a new user message, `/stop`, or `/new`, active children are interrupted and in-progress work is discarded.

## How It Differs From Kanban

| Factor | `delegate_task` | Kanban |
| --- | --- | --- |
| Shape | Synchronous fork-join call | Durable queue and state machine |
| Parent behavior | Blocks until children finish | Can create tasks and return |
| Worker identity | Anonymous child agent | Named Hermes profile |
| Durability | Current turn only | SQLite-backed task rows |
| Human input | Not supported inside child | Comments, block, unblock, review |
| Retry/reclaim | No durable retry | Retry, block, reclaim, run history |
| Audit trail | Final summary in parent context | Board events, comments, logs, runs |
| Best use | Short reasoning subtasks | Cross-agent operational workflows |

They can be combined: a Kanban worker may use `delegate_task` internally for parallel research or review during its own run. Do not use `delegate_task` as a substitute for Kanban when the handoff itself must be visible, durable, or assigned to a named profile.

## Prompt Patterns

Parallel research:

```text
Use delegate_task to research these three independent questions in parallel. Give each child a precise scope and cite official sources in the final synthesis.
```

Fresh-context review:

```text
Delegate a fresh-context review of this setup plan. The child should only inspect the files and return risks, missing checks, and one recommended path.
```

Kanban instead:

```text
Create Kanban tasks for researcher, implementer, and reviewer profiles. Make the implementation task depend on research, and the review task depend on implementation.
```

## Safety Rules

- Pass complete context. Children know nothing except their `goal` and `context`.
- Restrict toolsets to the minimum needed.
- Keep delegated tasks independent unless the parent will coordinate results.
- Do not put secrets in goals, context, task titles, comments, or logs.
- Avoid shared file writes by multiple children unless ownership is explicit.
- Prefer Kanban for work that needs status, retry, dependencies, profile identity, or human review.
- Prefer tmux for live interactive Hermes sessions and background terminal or cron for long non-interactive jobs.
