#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Edit Bilibili archive title/desc via member web API + biliup show."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import requests


def load_cookies(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {c["name"]: c["value"] for c in raw["cookie_info"]["cookies"]}


def biliup_show(biliup: str, cookie: Path, bvid: str) -> dict:
    out = subprocess.check_output(
        [biliup, "-u", str(cookie), "show", bvid],
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    start = out.find("{")
    if start < 0:
        raise RuntimeError("no json in biliup show output")
    return json.loads(out[start:])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bvid", required=True)
    ap.add_argument("--title")
    ap.add_argument("--tid", type=int, help="Bilibili 二级分区 ID")
    ap.add_argument("--desc")
    ap.add_argument("--desc-file", type=Path)
    ap.add_argument(
        "--cookie",
        type=Path,
        default=Path.home() / ".bilibili" / "cookies.json",
    )
    ap.add_argument(
        "--biliup",
        default="biliup",
        help="path to biliup.exe",
    )
    args = ap.parse_args()

    if not args.cookie.exists():
        raise SystemExit(f"cookie not found: {args.cookie}")

    detail = biliup_show(args.biliup, args.cookie, args.bvid)
    archive, videos = detail["archive"], detail["videos"]

    title = args.title or archive.get("title")
    if args.desc_file:
        desc = args.desc_file.read_text(encoding="utf-8")
    elif args.desc is not None:
        desc = args.desc
    else:
        desc = archive.get("desc") or ""

    cookies = load_cookies(args.cookie)
    csrf = cookies["bili_jct"]
    sess = requests.Session()
    for k, v in cookies.items():
        sess.cookies.set(k, v, domain=".bilibili.com")

    vid_payload = []
    for v in videos:
        item = {
            "title": v.get("title") or "P1",
            "filename": v.get("filename"),
            "desc": v.get("desc") or "",
        }
        if v.get("cid"):
            item["cid"] = v["cid"]
        vid_payload.append(item)

    post_data = {
        "aid": archive["aid"],
        "copyright": archive.get("copyright", 2),
        "source": archive.get("source") or "",
        "tid": args.tid if args.tid is not None else archive.get("tid", 201),
        "cover": archive.get("cover") or "",
        "title": title,
        "desc": desc,
        "desc_format_id": archive.get("desc_format_id", 0),
        "dynamic": archive.get("dynamic") or "",
        "tag": archive.get("tag") or "",
        "videos": vid_payload,
        "no_reprint": archive.get("no_reprint", 0),
        "open_elec": 0,
        "interactive": archive.get("interactive", 0),
        "subtitle": {"open": 0, "lan": ""},
    }

    api = f"https://member.bilibili.com/x/vu/web/edit?csrf={csrf}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://member.bilibili.com/platform/upload/video/frame",
        "Origin": "https://member.bilibili.com",
        "Content-Type": "application/json",
    }
    r = sess.post(api, headers=headers, json=post_data, timeout=30)
    print(r.status_code, r.text[:500])
    j = r.json()
    if j.get("code") != 0:
        raise SystemExit(f"edit failed: {j}")
    print("OK", j.get("data"))


if __name__ == "__main__":
    main()
