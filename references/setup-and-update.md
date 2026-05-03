# Hermes Setup And Update

Use this reference for installation state, update checks, backup policy, health checks, and local configuration.

## Sources Of Truth

- Local command behavior: `hermes --help` and `hermes <command> --help`.
- Official docs: `https://hermes-agent.nousresearch.com/docs/`.
- Official releases: `https://github.com/NousResearch/hermes-agent/releases`.
- Local source tree is usually under `~/.hermes/hermes-agent`.

## First Probe

Run the deterministic probe:

```bash
python3 <skill-dir>/scripts/hermes_check.py --json
```

For a fuller health pass:

```bash
python3 <skill-dir>/scripts/hermes_check.py --json --health --skills-check
```

Interpretation:

- `hermes --version` prints installed version and may mention commits behind.
- `hermes update --check` checks update availability without applying changes.
- GitHub release info is advisory; local CLI output wins for installed command behavior.

## Safe Update Workflow

1. Run `hermes update --check`.
2. Inspect `hermes doctor` and `hermes config check` if behavior is inconsistent.
3. Confirm whether the user wants a release-level update or latest-main update.
4. Run a backup before risky updates:

```bash
hermes backup -l before-update
```

5. Apply update only after approval:

```bash
hermes update --backup
```

For non-interactive migration prompts:

```bash
hermes update --backup --yes
```

Use `--no-backup` only when the user explicitly accepts that risk.

## Installation And Setup

Official baseline install is:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Then validate:

```bash
hermes --version
hermes setup
hermes model
hermes doctor
```

Use `hermes setup <section>` for targeted setup when supported by local help:

```bash
hermes setup model
hermes setup terminal
hermes setup gateway
hermes setup tools
hermes setup agent
```

## Configuration Paths

Find paths deterministically:

```bash
hermes config path
hermes config env-path
```

Common files:

- `~/.hermes/config.yaml`: main configuration.
- `~/.hermes/.env`: API keys and platform tokens.
- `~/.hermes/skills/`: Hermes skills loaded by Hermes itself.
- `~/.hermes/logs/`: gateway and agent logs.
- `~/.hermes/auth.json`: OAuth and credential pools.

Do not print full secrets. When showing config, redact token-like values.

## Skill Updates

Hermes bundled skills sync on install/update. If a bundled skill was edited locally, Hermes can skip future upstream updates for that skill. Use:

```bash
hermes skills check
hermes skills update
hermes skills reset <skill-name>
hermes skills reset <skill-name> --restore --yes
```

Use reset only after explaining that restore replaces the local skill copy with the bundled upstream version.
