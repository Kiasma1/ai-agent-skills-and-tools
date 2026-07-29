#!/usr/bin/env python3
"""Mini-book smoke: convert original demo txt + static showcase verify.

Does NOT run LLM distillation (Step1-7). Proves installable input pipeline + contract lint.

exit 0 all pass / 1 check failed / 2 environment or input error
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REPO_ROOT = SKILL_ROOT.parent.parent
MINI_DIR = REPO_ROOT / "examples" / "mini-book"
SOURCE = MINI_DIR / "source.txt"
SHOWCASE = MINI_DIR / "showcase.html"
CONVERT = SCRIPT_DIR / "convert_book.py"
VERIFY = SCRIPT_DIR / "verify_page.py"
BUILD_SHOWCASE = MINI_DIR / "_build_showcase.py"


def run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="sansheng-distill mini-book smoke")
    ap.add_argument(
        "--outdir",
        type=Path,
        help="Where to write convert_book outputs (default: temp dir)",
    )
    ap.add_argument(
        "--keep",
        action="store_true",
        help="Keep temp outdir (print path); ignored if --outdir set",
    )
    args = ap.parse_args()

    failures: list[str] = []

    if not SOURCE.is_file():
        print(f"[输入] missing {SOURCE}", file=sys.stderr)
        return 2
    if not CONVERT.is_file() or not VERIFY.is_file():
        print("[输入] convert_book.py / verify_page.py missing", file=sys.stderr)
        return 2

    # 1) layout essentials
    for rel in (
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "templates" / "page-skeleton.html",
        SKILL_ROOT / "references" / "method.md",
    ):
        if not rel.is_file():
            failures.append(f"[layout] missing {rel.relative_to(REPO_ROOT)}")

    # 2) ensure showcase exists and rebuild if builder present
    if BUILD_SHOWCASE.is_file():
        built = run([sys.executable, str(BUILD_SHOWCASE)])
        if built.returncode != 0:
            failures.append(f"[showcase-build] exit {built.returncode}: {built.stdout}\n{built.stderr}")
        else:
            print(built.stdout.strip())
    if not SHOWCASE.is_file():
        failures.append(f"[showcase] missing {SHOWCASE}")

    # 3) convert mini book
    tmp: tempfile.TemporaryDirectory[str] | None = None
    if args.outdir:
        outdir = args.outdir
        outdir.mkdir(parents=True, exist_ok=True)
    else:
        tmp = tempfile.TemporaryDirectory(prefix="sansheng-mini-")
        outdir = Path(tmp.name)

    conv = run(
        [sys.executable, str(CONVERT), str(SOURCE), "--outdir", str(outdir), "--force"],
    )
    print("--- convert_book ---")
    if conv.stdout:
        print(conv.stdout.rstrip())
    if conv.stderr:
        print(conv.stderr.rstrip(), file=sys.stderr)
    if conv.returncode != 0:
        failures.append(f"[convert] exit {conv.returncode}")
    else:
        book_txt = outdir / "book.txt"
        diagnose = outdir / "diagnose.json"
        if not book_txt.is_file():
            failures.append("[convert] book.txt not written")
        else:
            text = book_txt.read_text(encoding="utf-8", errors="replace")
            if "第1章" not in text or "第2章" not in text:
                failures.append("[convert] chapter markers missing in book.txt")
            if len(text) < 200:
                failures.append("[convert] book.txt too short")
        if not diagnose.is_file():
            failures.append("[convert] diagnose.json not written")
        else:
            try:
                diag = json.loads(diagnose.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                failures.append(f"[convert] diagnose.json invalid: {e}")
            else:
                rec = str(diag.get("recommendation") or diag.get("status") or "")
                print(f"[convert] diagnose keys={list(diag.keys())[:12]} recommendation={rec!r}")
                # exit 0 path should not demand OCR
                if "OCR" in rec.upper() and "需" in rec:
                    failures.append(f"[convert] unexpected OCR recommendation: {rec}")

    # 4) static verify showcase (no playwright)
    if SHOWCASE.is_file():
        ver = run(
            [sys.executable, str(VERIFY), str(SHOWCASE), "--skip-interact"],
        )
        print("--- verify_page (showcase, --skip-interact) ---")
        print((ver.stdout or ver.stderr or "").rstrip())
        if ver.returncode != 0:
            failures.append(f"[verify] exit {ver.returncode}")

    # report
    print("--- summary ---")
    if failures:
        for f in failures:
            print("FAIL", f)
        if tmp and args.keep:
            kept = REPO_ROOT / "examples" / "mini-book" / "_last-smoke-outdir"
            if kept.exists():
                shutil.rmtree(kept)
            shutil.copytree(outdir, kept)
            print(f"kept convert outputs at {kept}")
            tmp = None  # noqa: avoid cleanup before copy - actually tmp cleans on exit
        if tmp:
            print(f"(temp convert dir was {outdir})")
        return 1

    print("PASS mini-book smoke")
    print(f"  source:   {SOURCE}")
    print(f"  showcase: {SHOWCASE}")
    print(f"  convert:  {outdir}")
    if args.keep and tmp:
        kept = REPO_ROOT / "examples" / "mini-book" / "_last-smoke-outdir"
        if kept.exists():
            shutil.rmtree(kept)
        shutil.copytree(outdir, kept)
        print(f"  kept:     {kept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
