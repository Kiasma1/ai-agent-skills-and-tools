#!/usr/bin/env python3
"""Deterministic plugin discovery and input-pipeline smoke test."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Windows 管道默认 cp936,中转 agent CLI 的中文 stderr 前强制 UTF-8。
# pytest 直接 import 本模块时 sys.stdout 可能是不带 reconfigure 的捕获对象,故 guard 防 import 崩。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


PLUGIN_NAME = "sansheng-distill"


def run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def cli_command(name: str, *arguments: str) -> list[str] | None:
    """Resolve a CLI, including PowerShell and cmd shims on Windows."""
    executable = shutil.which(name)
    if not executable:
        return None
    suffix = Path(executable).suffix.lower()
    if suffix == ".ps1":
        return [
            "powershell.exe",
            "-NoLogo",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            executable,
            *arguments,
        ]
    if suffix in {".cmd", ".bat"}:
        invocation = subprocess.list2cmdline([executable, *arguments])
        return ["cmd.exe", "/d", "/s", "/c", invocation]
    return [executable, *arguments]


def _load_manifest(path: Path) -> dict | None:
    """读插件清单 JSON;缺失/损坏返回 None(由调用方记成失败检查项,不抛裸栈)。"""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def validate_layout(repo_root: Path) -> dict:
    skill_root = repo_root / "skills" / PLUGIN_NAME
    claude = _load_manifest(repo_root / ".claude-plugin" / "plugin.json")
    codex = _load_manifest(repo_root / ".codex-plugin" / "plugin.json")
    marketplace = _load_manifest(repo_root / ".claude-plugin" / "marketplace.json")
    versions = {(claude or {}).get("version"), (codex or {}).get("version")}
    market_item = next(
        (item for item in (marketplace or {}).get("plugins", []) if item.get("name") == PLUGIN_NAME),
        None,
    )
    checks = {
        "skill": (skill_root / "SKILL.md").is_file(),
        "references": (skill_root / "references").is_dir(),
        "scripts": (skill_root / "scripts").is_dir(),
        "templates": (skill_root / "templates").is_dir(),
        "openai_metadata": (skill_root / "agents" / "openai.yaml").is_file(),
        "claude_manifest": claude is not None,
        "codex_manifest": codex is not None,
        "marketplace_manifest": marketplace is not None,
        "claude_name": (claude or {}).get("name") == PLUGIN_NAME,
        "codex_name": (codex or {}).get("name") == PLUGIN_NAME,
        "codex_skill_path": (codex or {}).get("skills") == "./skills/",
        "version_match": len(versions) == 1 and None not in versions,
        "marketplace_match": bool(
            market_item and market_item.get("version") in versions
        ),
    }
    return checks


def smoke_inputs(repo_root: Path) -> dict:
    scripts = repo_root / "skills" / PLUGIN_NAME / "scripts"
    with tempfile.TemporaryDirectory(prefix="sansheng-distill-smoke-") as tmp:
        work = Path(tmp)
        source = work / "sample.txt"
        paragraph = (
            "知识不是把结论堆在一起，而是保留问题、证据、推理和可以反驳的边界。"
            "一个可靠的阅读地图必须让读者能够回到原文，重新检查每一步判断。"
        )
        source.write_text(
            "第一章 为什么需要证据\n" + paragraph * 180 +
            "\n第二章 如何保留分歧\n" + paragraph * 180,
            encoding="utf-8",
        )
        book_out = work / "book"
        converted = run(
            [
                sys.executable,
                str(scripts / "convert_book.py"),
                str(source),
                "--outdir",
                str(book_out),
            ],
            cwd=repo_root,
        )
        if converted.returncode != 0:
            raise RuntimeError(f"convert smoke failed: {converted.stderr}\n{converted.stdout}")

        series_out = work / "series"
        raw = series_out / "raw"
        raw.mkdir(parents=True)
        (raw / "01.txt").write_text(paragraph * 20, encoding="utf-8")
        (raw / "02.txt").write_text(paragraph * 20, encoding="utf-8")
        manifest = {
            "slug": "smoke-series",
            "series_title": "Smoke Series",
            "author": "sansheng-distill",
            "platform": "youtube",
            "videos": [
                {
                    "no": 1,
                    "title": "证据",
                    "url": "https://example.com/1",
                    "transcript": "raw/01.txt",
                },
                {
                    "no": 2,
                    "title": "分歧",
                    "url": "https://example.com/2",
                    "transcript": "raw/02.txt",
                },
            ],
        }
        manifest_path = series_out / "series-input.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        assembled = run(
            [
                sys.executable,
                str(scripts / "build_series.py"),
                "--manifest",
                str(manifest_path),
                "--outdir",
                str(series_out),
            ],
            cwd=repo_root,
        )
        if assembled.returncode != 0:
            raise RuntimeError(f"series smoke failed: {assembled.stderr}\n{assembled.stdout}")

        expected = [
            book_out / "book.txt",
            book_out / "diagnose.json",
            series_out / "book.txt",
            series_out / "series.json",
            series_out / "diagnose.json",
        ]
        if not all(path.is_file() for path in expected):
            raise RuntimeError("input smoke did not create every expected artifact")
        return {
            "convert": "passed",
            "series": "passed",
            "artifacts": [path.name for path in expected],
        }


def validate_agents(repo_root: Path, agents: list[str]) -> dict:
    results: dict[str, str] = {}
    if "claude" in agents:
        command = cli_command("claude", "plugin", "validate", str(repo_root))
        if command:
            proc = run(command, cwd=repo_root)
            results["claude"] = "passed" if proc.returncode == 0 else proc.stderr.strip()
        else:
            results["claude"] = "not installed"
    if "grok" in agents:
        command = cli_command("grok", "plugin", "validate", str(repo_root))
        if command:
            proc = run(command, cwd=repo_root)
            results["grok"] = "passed" if proc.returncode == 0 else proc.stderr.strip()
        else:
            results["grok"] = "not installed"
    if "codex" in agents:
        results["codex"] = "passed (manifest + skill structure)"
    failures = [value for value in results.values() if value not in {
        "passed", "passed (manifest + skill structure)", "not installed"
    }]
    if failures:
        raise RuntimeError(f"agent validation failed: {results}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="验证 Claude Code、Codex Desktop、Grok 插件布局和确定性输入管线"
    )
    parser.add_argument(
        "--agents",
        default="all",
        help="all 或逗号分隔的 claude,codex,grok",
    )
    parser.add_argument("--skip-inputs", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    agents = ["claude", "codex", "grok"] if args.agents == "all" else [
        item.strip() for item in args.agents.split(",") if item.strip()
    ]
    unknown = set(agents) - {"claude", "codex", "grok"}
    if unknown:
        raise ValueError(f"unknown agents: {sorted(unknown)}")
    layout = validate_layout(repo_root)
    if not all(layout.values()):
        # 布局检查失败:报告失败项后干净退出(exit 1),不再继续跑后续冒烟
        if args.json:
            print(json.dumps({"layout": layout}, ensure_ascii=False, indent=2))
        print(f"plugin layout validation failed: {layout}", file=sys.stderr)
        return 1
    report = {
        "layout": layout,
        "agents": validate_agents(repo_root, agents),
    }
    if not args.skip_inputs:
        report["inputs"] = smoke_inputs(repo_root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("sansheng-distill smoke: passed")
        for agent, status in report["agents"].items():
            print(f"  {agent}: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
