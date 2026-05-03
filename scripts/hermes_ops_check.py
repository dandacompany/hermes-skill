#!/usr/bin/env python3
"""Read-only Hermes operations health report."""

from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


TOKEN_PATTERNS = [
    re.compile(r"(?i)xox[baprs]-[A-Za-z0-9-]+"),
    re.compile(r"(?i)sk[-_][A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)gh[opsu]_[A-Za-z0-9_]{12,}"),
    re.compile(r"(?i)nvapi-[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}:[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)[=:]\s*[^\s]+"),
]
STATUS_SECRET_RE = re.compile(r"(✓\s+)([A-Za-z0-9][A-Za-z0-9_:\-]{18,})")


def redact(text: str) -> str:
    redacted = text
    for pattern in TOKEN_PATTERNS:
        redacted = pattern.sub(lambda m: m.group(0)[:8] + "***", redacted)
    redacted = STATUS_SECRET_RE.sub(lambda m: m.group(1) + m.group(2)[:6] + "***", redacted)
    return redacted


def run_cmd(args: list[str], timeout: int) -> dict:
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
        return {
            "cmd": args,
            "ok": False,
            "returncode": 124,
            "duration_sec": round(time.time() - started, 3),
            "output": redact(output.strip() or f"Timed out after {timeout}s"),
        }


def path_from_output(result: dict) -> str | None:
    if not result.get("ok"):
        return None
    lines = [line.strip() for line in result.get("output", "").splitlines() if line.strip()]
    return lines[-1] if lines else None


def file_status(path: str | None) -> dict:
    if not path:
        return {"path": None, "exists": False}
    p = Path(path).expanduser()
    status = {"path": str(p), "exists": p.exists()}
    if p.exists():
        status["is_file"] = p.is_file()
        status["is_dir"] = p.is_dir()
        try:
            status["mode"] = oct(p.stat().st_mode & 0o777)
        except OSError:
            pass
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Hermes operations health check.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--timeout", type=int, default=30, help="Per-command timeout in seconds.")
    parser.add_argument("--skip-gateway", action="store_true", help="Skip gateway status/log checks.")
    parser.add_argument("--log-lines", type=int, default=50, help="Error log lines to request.")
    args = parser.parse_args()

    hermes = shutil.which("hermes")
    report: dict = {
        "ok": False,
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "hermes_path": hermes,
        "checks": {},
        "paths": {},
        "recommendations": [],
    }

    if not hermes:
        report["recommendations"].append("Install Hermes or add it to PATH.")
        print(json.dumps(report, indent=2) if args.json else "ERROR: hermes not found on PATH")
        return 1

    checks = report["checks"]
    checks["version"] = run_cmd([hermes, "--version"], args.timeout)
    checks["update_check"] = run_cmd([hermes, "update", "--check"], args.timeout)
    checks["doctor"] = run_cmd([hermes, "doctor"], args.timeout)
    checks["config_check"] = run_cmd([hermes, "config", "check"], args.timeout)
    checks["status_all"] = run_cmd([hermes, "status", "--all"], args.timeout)
    checks["config_path"] = run_cmd([hermes, "config", "path"], args.timeout)
    checks["env_path"] = run_cmd([hermes, "config", "env-path"], args.timeout)

    report["paths"]["config"] = file_status(path_from_output(checks["config_path"]))
    report["paths"]["env"] = file_status(path_from_output(checks["env_path"]))

    if not args.skip_gateway:
        checks["gateway_status"] = run_cmd([hermes, "gateway", "status"], args.timeout)
        checks["gateway_logs"] = run_cmd(
            [hermes, "logs", "--component", "gateway", "--since", "1h", "-n", str(args.log_lines)],
            args.timeout,
        )
        checks["error_logs"] = run_cmd([hermes, "logs", "errors", "-n", str(args.log_lines)], args.timeout)

    if checks["update_check"]["ok"] and "Update available" in checks["update_check"]["output"]:
        report["recommendations"].append("Update is available. Back up first and ask for approval before running `hermes update`.")
    if not checks["doctor"]["ok"]:
        report["recommendations"].append("Run `hermes doctor --fix` only after reviewing doctor output.")
    if not checks["config_check"]["ok"]:
        report["recommendations"].append("Review `hermes config check` output and migrate config if needed.")
    if not report["paths"]["env"]["exists"]:
        report["recommendations"].append("Configure provider and gateway secrets in the env path reported by `hermes config env-path`.")

    report["ok"] = all(
        checks[name]["ok"]
        for name in ("version", "update_check", "doctor", "config_check")
        if name in checks
    )

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Hermes: {hermes}")
        for name in ("version", "update_check", "doctor", "config_check", "gateway_status"):
            if name in checks:
                print(f"\n## {name}")
                print(checks[name]["output"] or f"exit={checks[name]['returncode']}")
        print("\n## paths")
        for key, value in report["paths"].items():
            print(f"{key}: {value}")
        if report["recommendations"]:
            print("\n## recommendations")
            for item in report["recommendations"]:
                print(f"- {item}")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
