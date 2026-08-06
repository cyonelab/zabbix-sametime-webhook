#!/usr/bin/env python3
"""Validate the Zabbix media type export without contacting Sametime."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "zabbix-sametime-webhook.yaml"
EXPECTED_PARAMETERS = {
    "Channel",
    "ChannelId",
    "Group",
    "GroupPlaceId",
    "Host",
    "Message",
    "Password",
    "proxy",
    "Subject",
    "To",
    "Username",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    raw = EXPORT.read_text(encoding="utf-8")

    if re.search(r"[\u0400-\u04FF]", raw):
        fail("The export must contain English-only text")

    document = yaml.safe_load(raw)
    export = document.get("zabbix_export", {})

    if str(export.get("version")) != "7.0":
        fail("Expected Zabbix export version 7.0")

    media_types = export.get("media_types", [])
    if len(media_types) != 1:
        fail("Expected exactly one media type")

    media_type = media_types[0]
    if media_type.get("name") != "Sametime":
        fail("Expected media type name Sametime")
    if media_type.get("type") != "WEBHOOK":
        fail("Expected WEBHOOK media type")
    if media_type.get("timeout") != "20s":
        fail("Expected a 20-second webhook timeout")

    parameter_names = {item.get("name") for item in media_type.get("parameters", [])}
    if parameter_names != EXPECTED_PARAMETERS:
        fail(
            "Unexpected parameter set: "
            f"missing={sorted(EXPECTED_PARAMETERS - parameter_names)}, "
            f"extra={sorted(parameter_names - EXPECTED_PARAMETERS)}"
        )

    parameters = {
        item["name"]: item.get("value") for item in media_type.get("parameters", [])
    }
    if parameters.get("Password") != "{$ST_PASSWORD}":
        fail("Password must reference {$ST_PASSWORD}, not a literal value")

    script = media_type.get("script", "")
    if not script:
        fail("Webhook JavaScript is missing")

    version_match = re.search(r'scriptVersion:\s*"([0-9]+\.[0-9]+\.[0-9]+)"', script)
    if not version_match:
        fail("scriptVersion was not found")

    version = version_match.group(1)
    description = media_type.get("description", "")
    if f"Webhook version: {version}." not in description:
        fail("Media type description and scriptVersion do not match")

    required_fragments = [
        "/stwebapi/user/connect",
        "/sametime-auth/api/v1/check",
        "/sametime-auth/api/v1/refresh",
        "/sametime-chatrooms/api/v1/chatrooms/byName",
        "/stwebapi/chat/nway",
    ]
    for fragment in required_fragments:
        if fragment not in script:
            fail(f"Required API path is missing: {fragment}")

    compiler = (
        "let s='';"
        "process.stdin.on('data',d=>s+=d);"
        "process.stdin.on('end',()=>{"
        "new Function('value','Zabbix','HttpRequest',s);"
        "console.log('Embedded JavaScript compiled successfully');"
        "});"
    )
    subprocess.run(
        ["node", "-e", compiler],
        input=script,
        text=True,
        check=True,
    )

    print(f"Validated {EXPORT.name}: Zabbix 7.0, webhook {version}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, OSError, subprocess.CalledProcessError, yaml.YAMLError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
