#!/usr/bin/env python3
"""Patch a Hermes-generated Slack manifest for current gateway requirements."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_BOT_SCOPES = (
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
    "mpim:read",
    "users:read",
)

APP_HOME = {
    "home_tab_enabled": False,
    "messages_tab_enabled": True,
    "messages_tab_read_only_enabled": False,
}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"manifest not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise SystemExit(f"manifest root must be a JSON object: {path}")
    return data


def patch_manifest(data: dict[str, Any]) -> dict[str, Any]:
    changes: dict[str, Any] = {
        "added_bot_scopes": [],
        "updated_app_home": False,
    }

    oauth_config = data.setdefault("oauth_config", {})
    scopes_cfg = oauth_config.setdefault("scopes", {})
    bot_scopes = scopes_cfg.setdefault("bot", [])
    if not isinstance(bot_scopes, list):
        raise SystemExit("oauth_config.scopes.bot must be a list")

    for scope in REQUIRED_BOT_SCOPES:
        if scope not in bot_scopes:
            bot_scopes.append(scope)
            changes["added_bot_scopes"].append(scope)
    bot_scopes.sort()

    features = data.setdefault("features", {})
    current_app_home = features.get("app_home")
    if current_app_home != APP_HOME:
        features["app_home"] = dict(APP_HOME)
        changes["updated_app_home"] = True

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Patch a Hermes Slack manifest with required scopes and writable App Home DMs."
    )
    parser.add_argument("manifest", type=Path, help="Path to a Slack manifest JSON file.")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Write patched manifest to this path instead of overwriting the input file.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 0 if no patch is needed, 1 if changes would be made. Do not write.",
    )
    args = parser.parse_args()

    source = args.manifest.expanduser()
    target = args.output.expanduser() if args.output else source
    data = load_manifest(source)
    changes = patch_manifest(data)
    changed = bool(changes["added_bot_scopes"] or changes["updated_app_home"])

    if args.check:
        print(json.dumps({"ok": not changed, "changed": changed, **changes}, indent=2))
        return 1 if changed else 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(target), "changed": changed, **changes}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
