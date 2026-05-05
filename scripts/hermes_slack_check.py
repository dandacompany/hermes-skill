#!/usr/bin/env python3
"""Read-only Slack gateway configuration checks for Hermes."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


SLACK_KEYS = ("SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "SLACK_ALLOWED_USERS", "SLACK_HOME_CHANNEL")
REQUIRED_MANIFEST_BOT_SCOPES = (
    "app_mentions:read",
    "assistant:write",
    "channels:history",
    "channels:read",
    "chat:write",
    "commands",
    "files:read",
    "files:write",
    "groups:history",
    "groups:read",
    "im:history",
    "im:read",
    "im:write",
    "users:read",
)


def run_cmd(args: list[str], timeout: int) -> dict:
    started = time.time()
    try:
        proc = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout, check=False)
        return {
            "cmd": args,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "duration_sec": round(time.time() - started, 3),
            "output": redact(proc.stdout.strip()),
        }
    except FileNotFoundError as exc:
        return {"cmd": args, "ok": False, "returncode": 127, "duration_sec": 0, "output": str(exc)}
    except subprocess.TimeoutExpired as exc:
        output = ""
        if exc.stdout:
            output += exc.stdout if isinstance(exc.stdout, str) else exc.stdout.decode(errors="replace")
        if exc.stderr:
            output += exc.stderr if isinstance(exc.stderr, str) else exc.stderr.decode(errors="replace")
        return {"cmd": args, "ok": False, "returncode": 124, "duration_sec": round(time.time() - started, 3), "output": redact(output.strip())}


def redact(text: str) -> str:
    return re.sub(r"(xox[baprs]-)[A-Za-z0-9-]+", r"\1***", text)


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            values[key] = value
    return values


def summarize_value(key: str, value: str | None) -> dict:
    if not value:
        return {"present": False}
    item = {"present": True, "length": len(value), "preview": value[:6] + "***"}
    if key == "SLACK_BOT_TOKEN":
        item["valid_prefix"] = value.startswith("xoxb-")
        item["warning"] = None if item["valid_prefix"] else "Expected xoxb- prefix."
    elif key == "SLACK_APP_TOKEN":
        item["valid_prefix"] = value.startswith("xapp-")
        item["warning"] = None if item["valid_prefix"] else "Expected xapp- prefix."
    elif key == "SLACK_ALLOWED_USERS":
        users = [u.strip() for u in value.split(",") if u.strip()]
        item["count"] = len(users)
        item["looks_like_user_ids"] = all(u.startswith("U") or u.startswith("W") for u in users) if users else False
        item["warning"] = None if users else "Expected one or more Slack member IDs."
    elif key == "SLACK_HOME_CHANNEL":
        item["looks_like_channel_id"] = value.startswith(("C", "G", "D"))
        item["warning"] = None if item["looks_like_channel_id"] else "Expected a Slack channel/conversation ID."
    return item


def output_path(result: dict) -> Path | None:
    if not result.get("ok"):
        return None
    lines = [line.strip() for line in result.get("output", "").splitlines() if line.strip()]
    return Path(lines[-1]).expanduser() if lines else None


def inspect_manifest(path: Path | None) -> dict:
    if not path:
        return {"path": None, "present": False}
    item: dict = {"path": str(path), "present": path.exists()}
    if not path.exists():
        return item
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        item["error"] = f"{type(exc).__name__}: {exc}"
        return item
    scopes = data.get("oauth_config", {}).get("scopes", {}).get("bot", [])
    missing = [scope for scope in REQUIRED_MANIFEST_BOT_SCOPES if scope not in scopes]
    item["bot_scopes"] = scopes
    item["missing_bot_scopes"] = missing
    item["ok"] = not missing
    return item


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Hermes Slack gateway check.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--timeout", type=int, default=30, help="Per-command timeout in seconds.")
    parser.add_argument("--env-path", type=Path, help="Override Hermes .env path.")
    parser.add_argument("--manifest-path", type=Path, help="Check a generated Slack manifest for required bot scopes.")
    args = parser.parse_args()

    hermes = shutil.which("hermes")
    report: dict = {
        "ok": False,
        "hermes_path": hermes,
        "env_path": None,
        "env": {},
        "manifest": {},
        "checks": {},
        "manual_checks": [
            "Slack app uses Socket Mode.",
            "Bot is invited to target public/private channels.",
            "Slack event subscriptions include app_mention and the relevant message.channels or message.groups events.",
            "Slack app was reinstalled after scope or event changes.",
            "Sender's Slack member ID is included in SLACK_ALLOWED_USERS.",
        ],
        "recommendations": [],
    }

    if not hermes:
        report["recommendations"].append("Install Hermes or add it to PATH.")
        print(json.dumps(report, indent=2) if args.json else "ERROR: hermes not found on PATH")
        return 1

    checks = report["checks"]
    checks["slack_manifest_help"] = run_cmd([hermes, "slack", "manifest", "--help"], args.timeout)
    checks["gateway_status"] = run_cmd([hermes, "gateway", "status"], args.timeout)
    checks["gateway_logs"] = run_cmd([hermes, "logs", "--component", "gateway", "--since", "1h", "-n", "50"], args.timeout)
    checks["error_logs"] = run_cmd([hermes, "logs", "errors", "-n", "50"], args.timeout)

    env_path = args.env_path
    if env_path is None:
        checks["env_path"] = run_cmd([hermes, "config", "env-path"], args.timeout)
        env_path = output_path(checks["env_path"])
    report["env_path"] = str(env_path) if env_path else None

    env_values = parse_env(env_path) if env_path else {}
    for key in SLACK_KEYS:
        report["env"][key] = summarize_value(key, env_values.get(key) or os.environ.get(key))

    missing = [key for key, value in report["env"].items() if not value.get("present")]
    if missing:
        report["recommendations"].append("Set missing Slack environment values: " + ", ".join(missing))

    for key, value in report["env"].items():
        if value.get("warning"):
            report["recommendations"].append(f"{key}: {value['warning']}")

    report["manifest"] = inspect_manifest(args.manifest_path)
    missing_scopes = report["manifest"].get("missing_bot_scopes") or []
    if missing_scopes:
        report["recommendations"].append("Patch Slack manifest missing bot scopes: " + ", ".join(missing_scopes))

    if checks["gateway_logs"].get("output"):
        lower = checks["gateway_logs"]["output"].lower()
        if "invalid_auth" in lower or "not_authed" in lower:
            report["recommendations"].append("Slack auth error appears in logs. Rotate/check xoxb/xapp tokens and restart gateway.")
        if "not_in_channel" in lower or "channel_not_found" in lower:
            report["recommendations"].append("Invite the bot to the target channel and verify SLACK_HOME_CHANNEL.")
        if "missing_scope" in lower and "groups:read" in lower:
            report["recommendations"].append("Slack app is missing groups:read. Patch the manifest, reinstall the app, then restart the profile gateway.")

    report["ok"] = not missing and all(not v.get("warning") for v in report["env"].values()) and not missing_scopes

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Hermes: {hermes}")
        print(f"Env path: {report['env_path']}")
        print("\n## Slack env")
        for key, value in report["env"].items():
            print(f"{key}: {value}")
        print("\n## Gateway status")
        print(checks["gateway_status"]["output"] or f"exit={checks['gateway_status']['returncode']}")
        print("\n## Manual checks")
        for item in report["manual_checks"]:
            print(f"- {item}")
        if report["manifest"].get("path"):
            print("\n## Manifest")
            print(report["manifest"])
        if report["recommendations"]:
            print("\n## Recommendations")
            for item in report["recommendations"]:
                print(f"- {item}")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
