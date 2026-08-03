#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find first SRT timestamp for each keyword (for Bilibili jump comments)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_srt(text: str):
    blocks = re.split(r"\n\s*\n", text.strip())
    cues = []
    for b in blocks:
        lines = [ln for ln in b.splitlines() if ln.strip()]
        if len(lines) < 3:
            continue
        m = re.match(r"(\d{2}:\d{2}:\d{2}),(\d{3})\s*-->", lines[1])
        if not m:
            continue
        body = " ".join(lines[2:]).strip()
        cues.append((m.group(1), body))
    return cues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--srt", required=True)
    ap.add_argument(
        "--keyword",
        action="append",
        required=True,
        help="keyword:label  e.g.  'platinum 950:铂金950 / Platinum 950'",
    )
    args = ap.parse_args()

    cues = parse_srt(Path(args.srt).read_text(encoding="utf-8"))
    for item in args.keyword:
        if ":" in item:
            kw, label = item.split(":", 1)
        else:
            kw, label = item, item
        kw_l = kw.lower()
        hit = None
        for t, body in cues:
            if kw_l in body.lower():
                hit = t
                break
        if hit:
            print(f"{hit} {label}")
        else:
            print(f"# NOT FOUND: {label} ({kw})")


if __name__ == "__main__":
    main()
