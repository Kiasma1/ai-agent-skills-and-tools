#!/usr/bin/env python3
"""Check sansheng-distill agent discovery and runtime dependencies."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

# Windows 管道默认 cp936,打印中文检查结果前强制 UTF-8。
# pytest 直接 import 本模块时 sys.stdout 可能是不带 reconfigure 的捕获对象,故 guard 防 import 崩。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


PYTHON_DEPS = {
    "ebooklib": "ebooklib",
    "beautifulsoup4": "bs4",
    "pymupdf": "fitz",
    "pillow": "PIL",
    "playwright": "playwright",
}
OPTIONAL_COMMANDS = ("ebook-convert", "yt-dlp")
AGENT_COMMANDS = ("claude", "codex", "grok")


def _present_module(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def inspect_environment() -> dict:
    skill_root = Path(__file__).resolve().parents[1]
    repo_root = skill_root.parents[1]
    return {
        "skill_root": str(skill_root),
        "layout": {
            "skill": (skill_root / "SKILL.md").is_file(),
            "references": (skill_root / "references").is_dir(),
            "templates": (skill_root / "templates").is_dir(),
            "claude_plugin": (repo_root / ".claude-plugin" / "plugin.json").is_file(),
            "codex_plugin": (repo_root / ".codex-plugin" / "plugin.json").is_file(),
            "codex_metadata": (skill_root / "agents" / "openai.yaml").is_file(),
        },
        "python": {
            package: _present_module(module)
            for package, module in PYTHON_DEPS.items()
        },
        "commands": {
            command: shutil.which(command) is not None
            for command in OPTIONAL_COMMANDS
        },
        "agents": {
            agent: shutil.which(agent) is not None
            for agent in AGENT_COMMANDS
        },
    }


def _ok(report: dict) -> bool:
    return all(report["layout"].values()) and all(report["python"].values())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查多 Agent 插件布局与书籍蒸馏运行依赖"
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="缺少核心布局或 Python 依赖时返回非零退出码",
    )
    args = parser.parse_args()
    report = inspect_environment()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for section in ("layout", "python", "commands", "agents"):
            print(f"[{section}]")
            for name, present in report[section].items():
                print(f"  {'OK' if present else '--'} {name}")
        print(f"skill_root: {report['skill_root']}")
        if not all(report["python"].values()):
            print(
                "安装核心依赖: pip install ebooklib beautifulsoup4 pymupdf pillow playwright",
                file=sys.stderr,
            )
        if not any(report["agents"].values()):
            print("未在 PATH 中发现 Claude Code、Codex 或 Grok CLI。", file=sys.stderr)

    return 1 if args.strict and not _ok(report) else 0


if __name__ == "__main__":
    raise SystemExit(main())
