#!/usr/bin/env python3
"""Probe the local Hermes installation and optionally refresh CLI help docs."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


TIMEOUT = 30
GITHUB_LATEST = "https://api.github.com/repos/NousResearch/hermes-agent/releases/latest"


def run_cmd(args: list[str], timeout: int = TIMEOUT) -> dict:
    started = time.time()
    try:
        proc = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        return {
            "cmd": args,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "duration_sec": round(time.time() - started, 3),
            "output": proc.stdout.strip(),
        }
    except FileNotFoundError as exc:
        return {
            "cmd": args,
            "ok": False,
            "returncode": 127,
            "duration_sec": round(time.time() - started, 3),
            "output": str(exc),
        }
    except subprocess.TimeoutExpired as exc:
        output = ""
        if exc.stdout:
            output += exc.stdout if isinstance(exc.stdout, str) else exc.stdout.decode(errors="replace")
        if exc.stderr:
            output += exc.stderr if isinstance(exc.stderr, str) else exc.stderr.decode(errors="replace")
        return {
            "cmd": args,
            "ok": False,
            "returncode": 124,
            "duration_sec": round(time.time() - started, 3),
            "output": output.strip() or f"Timed out after {timeout}s",
        }


def github_latest(timeout: int = 10) -> dict:
    req = urllib.request.Request(
        GITHUB_LATEST,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "hermes-skill-check",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            data = json.loads(res.read().decode("utf-8"))
        return {
            "ok": True,
            "name": data.get("name"),
            "tag_name": data.get("tag_name"),
            "published_at": data.get("published_at"),
            "html_url": data.get("html_url"),
        }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"ok": False, "error": str(exc)}


def parse_commands(help_text: str) -> list[str]:
    matches = re.findall(r"\{([^}\n]+)\}", help_text)
    if not matches:
        return []
    commands = []
    for part in matches[0].split(","):
        cmd = part.strip()
        if cmd and re.fullmatch(r"[a-z][a-z0-9_-]*", cmd):
            commands.append(cmd)
    return commands


def first_usage(help_text: str) -> str:
    lines = help_text.splitlines()
    usage_lines = []
    collecting = False
    for line in lines:
        if line.startswith("usage:"):
            collecting = True
            usage_lines.append(line.strip())
            continue
        if collecting:
            if not line.startswith(" ") or not line.strip():
                break
            usage_lines.append(line.strip())
    return " ".join(usage_lines)


def subcommands(help_text: str) -> list[str]:
    usage = first_usage(help_text)
    matches = re.findall(r"\{([^}\n]+)\}", usage)
    if not matches:
        return []
    return [x.strip() for x in matches[-1].split(",") if x.strip()]


def refresh_help_doc(hermes: str, output_path: Path, timeout: int = TIMEOUT) -> dict:
    root = run_cmd([hermes, "--help"], timeout=timeout)
    if not root["ok"]:
        return {"ok": False, "error": root["output"]}

    commands = parse_commands(root["output"])
    sections = [
        "# Hermes CLI Help Snapshot",
        "",
        "Generated from local `hermes --help` and `hermes <command> --help`.",
        "Regenerate with `scripts/hermes_check.py --write-help references/command-map.generated.md`.",
        "",
        "## Root",
        "",
        "```text",
        first_usage(root["output"]),
        "```",
        "",
        "## Commands",
        "",
        "| Command | Usage | Subcommands |",
        "| --- | --- | --- |",
    ]

    for cmd in commands:
        help_result = run_cmd([hermes, cmd, "--help"], timeout=timeout)
        if help_result["ok"]:
            usage = first_usage(help_result["output"]).replace("|", "\\|")
            subs = ", ".join(subcommands(help_result["output"])) or "-"
        else:
            usage = f"failed: {help_result['output'][:160]}".replace("|", "\\|")
            subs = "-"
        sections.append(f"| `{cmd}` | `{usage}` | {subs} |")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return {"ok": True, "commands": commands, "path": str(output_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Hermes version/update state and CLI help.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a text report.")
    parser.add_argument("--write-help", type=Path, help="Write a generated markdown command map.")
    parser.add_argument("--skip-network", action="store_true", help="Do not query GitHub releases.")
    parser.add_argument("--skills-check", action="store_true", help="Run `hermes skills check` too.")
    parser.add_argument("--health", action="store_true", help="Run `hermes config check` and `hermes doctor`.")
    parser.add_argument("--timeout", type=int, default=TIMEOUT, help="Per-command timeout in seconds.")
    args = parser.parse_args()

    hermes = shutil.which("hermes")
    report: dict = {
        "hermes_path": hermes,
        "cwd": os.getcwd(),
        "checks": {},
    }
    if not hermes:
        report["ok"] = False
        report["error"] = "hermes executable not found on PATH"
        print(json.dumps(report, indent=2) if args.json else "ERROR: hermes executable not found on PATH")
        return 1

    report["checks"]["version"] = run_cmd([hermes, "--version"], timeout=args.timeout)
    report["checks"]["update_check"] = run_cmd([hermes, "update", "--check"], timeout=args.timeout)
    if not args.skip_network:
        report["github_latest_release"] = github_latest(timeout=min(args.timeout, 15))
    if args.skills_check:
        report["checks"]["skills_check"] = run_cmd([hermes, "skills", "check"], timeout=args.timeout)
    if args.health:
        report["checks"]["config_check"] = run_cmd([hermes, "config", "check"], timeout=args.timeout)
        report["checks"]["doctor"] = run_cmd([hermes, "doctor"], timeout=args.timeout)
    if args.write_help:
        report["help_snapshot"] = refresh_help_doc(hermes, args.write_help, timeout=args.timeout)

    report["ok"] = all(check.get("ok") for check in report["checks"].values())

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Hermes: {report['hermes_path']}")
        version = report["checks"]["version"]["output"].splitlines()
        if version:
            print(version[0])
        update = report["checks"]["update_check"]
        print("\nUpdate check:")
        print(update["output"] or f"exit={update['returncode']}")
        latest = report.get("github_latest_release")
        if latest:
            print("\nGitHub latest release:")
            if latest.get("ok"):
                print(f"{latest.get('name')} ({latest.get('tag_name')}) {latest.get('published_at')}")
                print(latest.get("html_url"))
            else:
                print(f"unavailable: {latest.get('error')}")
        if args.write_help:
            print(f"\nHelp snapshot: {report['help_snapshot']}")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
