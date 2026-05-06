# Changelog

## v0.1.4 - 2026-05-06

- Corrected the Slack manifest checker so assistant UI settings are treated as removable for normal DM bot setups.
- Removed `assistant:write` from the documented minimum bot-scope baseline.

## v0.1.3 - 2026-05-06

- Updated the Slack manifest patch helper to remove assistant UI fields for normal DM bot setups.
- Documented that Slack Agents & AI Apps mode can replace the normal Messages tab.

## v0.1.2 - 2026-05-06

- Added `scripts/patch_slack_manifest.py` so agents can patch Hermes-generated Slack manifests without modifying Hermes Agent source.
- Updated Slack gateway guidance to use the manifest patch helper before pasting into Slack.

## v0.1.1 - 2026-05-06

- Added Slack App Home DM message settings to the Slack gateway guide so app DMs are writable.
- Extended `scripts/hermes_slack_check.py` to detect missing or read-only Slack App Home message settings in generated manifests.

## v0.1.0 - 2026-05-04

- Initial public operator-focused Hermes skill.
- Added read-only update and CLI help probing with `scripts/hermes_check.py`.
- Added self-hosting, setup, Slack gateway, tmux, profiles, cron, MCP, tools, plugins, voice, troubleshooting, and self-improvement references.
- Added read-only operations health check with `scripts/hermes_ops_check.py`.
- Added read-only Slack gateway configuration check with `scripts/hermes_slack_check.py`.
- Added official documentation link map.
- Added Kanban operations guide for durable profile-worker task boards.
- Added `delegate_task` subagent guidance and a decision guide for delegation vs Kanban, tmux, cron, and background work.
