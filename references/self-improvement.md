# Self Improvement

Use this reference at the end of every Hermes task. The goal is to keep this skill current without bloating `SKILL.md` or making unsafe autonomous changes.

## End-Of-Task Review

Ask whether the task revealed any of these:

- New or changed Hermes CLI syntax.
- New `hermes --help` or `hermes <command> --help` output.
- Official docs, release notes, or source behavior that contradicts this skill.
- A Slack/gateway setup step that was missing or misleading.
- A provider, toolset, security, voice, profile, cron, MCP, or dashboard behavior not covered.
- A reproducible troubleshooting pattern.
- A safer operating rule, approval boundary, or secret-handling requirement.
- A scriptable check that would prevent future mistakes.

If none apply, do not edit the skill.

## Update Rules

When an update is useful:

1. Edit the smallest relevant `references/*.md` file.
2. Add a new reference file only if the topic does not fit an existing one.
3. Keep `SKILL.md` under roughly 700 words; add only routing instructions there.
4. Put deterministic checks in `scripts/`.
5. Do not copy large official docs verbatim; summarize and link.
6. Redact secrets and account-specific values.
7. Preserve portability: avoid absolute local paths in public docs; use `<skill-dir>` placeholders.

## CLI Snapshot Refresh

Refresh the generated command map whenever Hermes updates or CLI behavior matters:

```bash
python3 <skill-dir>/scripts/hermes_check.py --write-help <skill-dir>/references/command-map.generated.md
```

Also run:

```bash
python3 <skill-dir>/scripts/hermes_check.py --json
```

Report update availability, but do not run `hermes update` unless the user approved it or explicitly asked for an update.

## Validation

After editing the skill, validate it:

```bash
python3 /Users/dante/.agents/skills/skill-creator/scripts/quick_validate.py <skill-dir>
npx skills add <skill-dir> -l
```

For repo-maintained copies, also check:

```bash
git status --short
git diff --check
```

## Local And Public Repo Sync

If this skill is maintained from `dandacompany/hermes-skill`:

1. Apply edits in the repo working tree.
2. Sync to the local installed skill directory if needed.
3. Validate both copies.
4. Commit with a concise message.
5. Push after validation.

Recommended sync shape:

```bash
rsync -a --delete \
  --exclude='.git' \
  --exclude='.gitignore' \
  --exclude='README.md' \
  --exclude='LICENSE' \
  --exclude='__pycache__' \
  <repo-dir>/ <installed-skill-dir>/
```

Do not push unvalidated changes.

## What To Capture

Good additions are specific and operational:

- "For Slack public channels, subscribe to `message.channels` and reinstall the app."
- "`hermes run` is stale in v0.12.0; use `hermes chat -q` or `hermes -z`."
- "Tool changes require `/reset` or a fresh process."

Avoid vague additions:

- "Be careful."
- "Check docs."
- "Use best practices."

## Escalation

Ask the user before:

- Running `hermes update`.
- Replacing user-modified Hermes skills with `hermes skills reset --restore`.
- Editing files outside this skill or the Hermes config the user asked to change.
- Pushing a public repo update when the change includes organization-specific policy.
