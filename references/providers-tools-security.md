# Providers, Tools, Config, And Security

Use this reference for Hermes configuration paths, providers, toolsets, approvals, redaction, and privacy controls.

## Key Paths

Find paths with:

```bash
hermes config path
hermes config env-path
```

Common paths:

| Path | Purpose |
| --- | --- |
| `~/.hermes/config.yaml` | Main user configuration. |
| `~/.hermes/.env` | API keys, platform tokens, provider secrets. |
| `$HERMES_HOME/skills/` | Hermes-installed skills. |
| `~/.hermes/sessions/` | Session transcripts and history. |
| `~/.hermes/logs/` | Agent, gateway, and error logs. |
| `~/.hermes/auth.json` | OAuth tokens and credential pools. |
| `~/.hermes/hermes-agent/` | Git-installed source tree. |
| `~/.hermes/profiles/<name>/` | Isolated profile homes. |

Never print full contents of `.env` or `auth.json`.

## Config Sections

Edit with `hermes config edit` or narrow changes with `hermes config set KEY VALUE`.

| Section | Common keys |
| --- | --- |
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length`. |
| `agent` | `max_turns`, `tool_use_enforcement`. |
| `terminal` | `backend`, `cwd`, `timeout`. |
| `compression` | `enabled`, `threshold`, `target_ratio`. |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost`. |
| `stt` | `enabled`, `provider`, local STT model settings. |
| `tts` | `provider`, voice provider settings. |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider`. |
| `security` | `redact_secrets`, website/tool safety settings. |
| `privacy` | `redact_pii` for gateway context. |
| `delegation` | Delegate model/provider/base URL/API key/max iterations/reasoning, child timeout, concurrency, and nested orchestration limits. |
| `checkpoints` | `enabled`, `max_snapshots`. |
| `approvals` | `mode` for command approval behavior. |

Run `hermes config check` after manual edits.

## Providers

Select providers interactively:

```bash
hermes model
hermes login
hermes auth add
hermes auth list
```

Common provider secrets:

| Provider | Auth style | Common env/config |
| --- | --- | --- |
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| OpenAI / Codex | OAuth or API key | `hermes login --provider openai-codex`, `OPENAI_API_KEY` |
| Nous Portal | OAuth | `hermes login --provider nous` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| DashScope / Qwen | API key or OAuth | `DASHSCOPE_API_KEY`, `hermes login` where supported |
| Vercel AI Gateway | API key | `AI_GATEWAY_API_KEY` |
| Custom endpoint | config | `model.base_url`, `model.api_key`, `model.provider` |

Use `hermes doctor` when provider routing fails. Use `hermes fallback list/add/remove` to define fallback providers.

## Toolsets

Use:

```bash
hermes tools
hermes tools list
hermes tools enable <name>
hermes tools disable <name>
```

Common toolsets:

| Toolset | Provides |
| --- | --- |
| `web` | Search and web content extraction. |
| `search` | Search-only subset where available. |
| `browser` | Browser automation. |
| `terminal` | Shell/process tools. |
| `file` | File read/write/search/patch tools. |
| `code_execution` | Sandboxed code execution. |
| `vision` | Image analysis. |
| `image_gen` | Image generation. |
| `tts` | Text-to-speech. |
| `skills` | Skill browse/install/manage tools. |
| `memory` | Persistent memory access. |
| `session_search` | Search previous sessions. |
| `delegation` | Synchronous subagent delegation through `delegate_task`; see `references/delegation-vs-kanban.md` before using it for multi-agent work. |
| `cronjob` | Scheduled jobs. |
| `messaging` | Cross-platform message sending. |
| `clarify` | Ask user clarifying questions. |
| `todo` | In-session task tracking. |
| `rl`, `moa`, `homeassistant` | Specialized optional toolsets. |

Tool changes usually require `/reset` or a new Hermes process.

For delegation, keep child toolsets narrow. Leaf children cannot delegate further and cannot use user-clarification, shared-memory, or cross-platform message-sending tools. Use Kanban rather than `delegate_task` when work needs durable status, retry, human comments, or named profile identity.

## Security And Privacy

### Secret Redaction

Secret redaction can mask token-like strings before they enter context and logs. It is not a substitute for avoiding secret exposure.

```bash
hermes config set security.redact_secrets true
hermes config set security.redact_secrets false
```

Restart Hermes or `/reset` after changing it.

### Gateway PII Redaction

PII redaction is separate from secret redaction and is useful for Slack/Discord/Telegram context.

```bash
hermes config set privacy.redact_pii true
hermes config set privacy.redact_pii false
```

### Command Approval Modes

Common approval modes:

| Mode | Behavior |
| --- | --- |
| `manual` | Prompt for risky commands. Conservative default. |
| `smart` | Use an auxiliary model for low-risk auto-approval and prompt on risk. |
| `off` | Skip approvals. Equivalent in spirit to `--yolo`; avoid for unattended agents. |

```bash
hermes config set approvals.mode smart
hermes config set approvals.mode manual
```

Per invocation:

```bash
hermes --yolo
```

### Shell Hooks

Shell hooks may require allowlisting before execution. If hooks do not fire, inspect:

```bash
hermes hooks list
hermes hooks doctor
```

### Tool Risk Reduction

Disable tools that a workflow does not need:

```bash
hermes tools disable browser image_gen terminal
```

For Slack/gateway agents, enable only the minimum toolsets needed for the channel's workflow.
