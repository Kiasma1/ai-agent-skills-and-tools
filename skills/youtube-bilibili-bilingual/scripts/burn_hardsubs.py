#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Burn ASS hardsubs into video with ffmpeg (libx264 fallback)."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def escape_ass_path(p: Path) -> str:
    # FFmpeg ass filter on Windows: C\:/path/to/file.ass
    s = p.resolve().as_posix()
    if len(s) >= 2 and s[1] == ":":
        s = s[0] + "\\:" + s[2:]
    return s


def has_nvenc() -> bool:
    try:
        out = subprocess.check_output(
            ["ffmpeg", "-hide_banner", "-encoders"],
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        )
        return "h264_nvenc" in out
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--video", required=True)
    ap.add_argument("--ass", required=True)
    ap.add_argument("--out", default="final_bilibili_video.mp4")
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--prefer-nvenc", action="store_true")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found")

    video, ass, out = Path(args.video), Path(args.ass), Path(args.out)
    ass_esc = escape_ass_path(ass)
    vf = f"ass='{ass_esc}'"

    use_nvenc = args.prefer_nvenc and has_nvenc()
    if use_nvenc:
        vcodec = [
            "-c:v",
            "h264_nvenc",
            "-preset",
            "p5",
            "-rc",
            "vbr",
            "-cq",
            str(args.crf),
            "-b:v",
            "0",
        ]
    else:
        vcodec = [
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            str(args.crf),
            "-threads",
            "0",
        ]

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-vf",
        vf,
        *vcodec,
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "high",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-movflags",
        "+faststart",
        str(out),
    ]
    print(" ".join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0 and use_nvenc:
        print("NVENC failed, retrying libx264...")
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            str(args.crf),
            "-threads",
            "0",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(out),
        ]
        r = subprocess.run(cmd)
    raise SystemExit(r.returncode)


if __name__ == "__main__":
    main()
