#!/usr/bin/env python3
"""Create or update the Codex personal marketplace entry for this plugin."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

# Windows 管道默认 cp936,displayName 等字段可能含非 GBK 字符,打印前强制 UTF-8。
# pytest 直接 import 本模块时 sys.stdout 可能是不带 reconfigure 的捕获对象,故 guard 防 import 崩。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


PLUGIN_NAME = "sansheng-distill"


def build_marketplace(current: dict | None = None) -> dict:
    doc = dict(current or {})
    doc.setdefault("name", "personal")
    interface = doc.setdefault("interface", {})
    interface.setdefault("displayName", "Personal")
    plugins = [
        item
        for item in doc.get("plugins", [])
        if isinstance(item, dict) and item.get("name") != PLUGIN_NAME
    ]
    plugins.append(
        {
            "name": PLUGIN_NAME,
            "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
    )
    doc["plugins"] = plugins
    return doc


def write_atomic(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(doc, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="更新 Codex 个人 marketplace 中的 sansheng-distill 条目"
    )
    parser.add_argument("--marketplace", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    current = None
    if args.marketplace.is_file():
        current = json.loads(args.marketplace.read_text(encoding="utf-8"))
        if not isinstance(current, dict):
            raise ValueError("marketplace 根节点必须是 JSON object")
    result = build_marketplace(current)
    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        write_atomic(args.marketplace, result)
        print(args.marketplace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
