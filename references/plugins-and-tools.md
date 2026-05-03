# Plugins And Tools

Use this reference for operator-level plugin, toolset, skill, and MCP management. This is not a developer guide for writing Hermes source code.

## Mental Model

- **Tools** are capabilities exposed to the agent, grouped into toolsets.
- **Toolsets** control which tools are available in CLI or gateway contexts.
- **Skills** are reusable instruction packages Hermes can load.
- **Plugins** extend Hermes with additional integrations, memory providers, platforms, tools, or commands.
- **MCP servers** expose external tool providers through Model Context Protocol.

Always verify current command syntax:

```bash
hermes tools --help
hermes skills --help
hermes plugins --help
hermes mcp --help
```

## Toolset Operations

Inspect:

```bash
hermes tools
hermes tools list
```

Enable or disable:

```bash
hermes tools enable <toolset>
hermes tools disable <toolset>
```

Rules:

- Enable only the toolsets needed for a workflow.
- For gateway channels, avoid broad terminal/file/browser access unless the channel is trusted and allowlisted.
- Start a new session or use `/reset` after tool changes.
- Use `hermes config check` and `hermes doctor` when tools fail to appear.

Common toolsets are summarized in `references/providers-tools-security.md`.

## Skills Operations

Search, inspect, install, and update:

```bash
hermes skills browse
hermes skills search <query>
hermes skills inspect <id>
hermes skills install <id>
hermes skills list
hermes skills config
hermes skills check
hermes skills update
```

Operational rules:

- Inspect before installing unknown skills.
- Use `hermes skills config` to control platform enablement.
- If a bundled skill stops updating because it was modified locally, use `hermes skills check` first and only reset after explaining the replacement risk.

## Plugin Operations

List and manage plugins:

```bash
hermes plugins list
hermes plugins install <source>
hermes plugins enable <name>
hermes plugins disable <name>
hermes plugins update <name>
hermes plugins remove <name>
```

Recommended plugin workflow:

1. Confirm the plugin source and trust boundary.
2. Read plugin README or docs before install.
3. Install the plugin.
4. Enable it.
5. Restart or `/reset` if the plugin affects runtime tools or commands.
6. Run `hermes doctor`, `hermes status --all`, and a minimal functional test.

Security rules:

- Treat plugins like code execution.
- Avoid installing plugins from untrusted sources on production profiles.
- Use separate profiles for experimental plugins.
- Keep API keys in `.env`, not in prompts or plugin docs.

## MCP Operations

Inspect and add MCP servers:

```bash
hermes mcp list
hermes mcp add <name> --command <command>
hermes mcp add <name> --url <url>
hermes mcp test <name>
hermes mcp configure <name>
hermes mcp remove <name>
```

Operator workflow:

1. Add the server.
2. Test the connection.
3. Configure which MCP tools are enabled.
4. Start a fresh session.
5. Ask Hermes to list or use the new tools in a narrow test.

## Troubleshooting

Tool/plugin does not appear:

```bash
hermes tools list
hermes plugins list
hermes mcp list
hermes config check
hermes doctor
```

Then restart the relevant process:

```bash
hermes gateway restart
```

or use `/reset` in CLI.

Plugin breaks the gateway:

1. Stop gateway: `hermes gateway stop`.
2. Disable or remove the plugin.
3. Run `hermes doctor`.
4. Start foreground: `hermes gateway run`.
5. Move back to service mode only after logs are clean.

MCP server fails:

1. Run `hermes mcp test <name>`.
2. Check env vars and command paths.
3. Confirm the MCP server works outside Hermes.
4. Review logs with `hermes logs errors`.
