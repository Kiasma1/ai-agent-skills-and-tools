#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post a Bilibili video comment (timestamps like 00:01:23 are clickable)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bvid", required=True)
    ap.add_argument("--aid", type=int, help="稿件 AVID；审核中稿件可跳过公开播放接口")
    ap.add_argument("--message")
    ap.add_argument("--message-file", type=Path)
    ap.add_argument(
        "--cookie",
        type=Path,
        default=Path.home() / ".bilibili" / "cookies.json",
    )
    args = ap.parse_args()

    if args.message_file:
        message = args.message_file.read_text(encoding="utf-8")
    elif args.message:
        message = args.message
    else:
        raise SystemExit("need --message or --message-file")

    raw = json.loads(args.cookie.read_text(encoding="utf-8"))
    cookies = {c["name"]: c["value"] for c in raw["cookie_info"]["cookies"]}
    csrf = cookies["bili_jct"]

    sess = requests.Session()
    sess.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Referer": f"https://www.bilibili.com/video/{args.bvid}",
            "Origin": "https://www.bilibili.com",
        }
    )
    for k, v in cookies.items():
        sess.cookies.set(k, v, domain=".bilibili.com")

    if args.aid:
        aid = args.aid
    else:
        vr = sess.get(
            "https://api.bilibili.com/x/web-interface/view",
            params={"bvid": args.bvid},
            timeout=15,
        )
        vr.raise_for_status()
        aid = vr.json()["data"]["aid"]

    r = sess.post(
        "https://api.bilibili.com/x/v2/reply/add",
        data={
            "oid": aid,
            "type": 1,
            "message": message,
            "plat": 1,
            "csrf": csrf,
        },
        timeout=30,
    )
    print(r.status_code, r.text[:500])
    j = r.json()
    if j.get("code") != 0:
        raise SystemExit(f"comment failed: {j}")
    print("OK rpid", j["data"]["rpid"])


if __name__ == "__main__":
    main()
