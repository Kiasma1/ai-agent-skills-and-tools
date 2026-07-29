#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EN SRT -> bilingual SRT + ASS (Chinese large on top, English smaller below)."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

SYSTEM_PROMPT = """\
You are a translator. Your ONLY job: translate the English lines below to Chinese (Simplified).
Output EXACTLY one Chinese line per input line. No English words in output. No explanations.
Rules: concise, natural spoken Chinese, consistent terminology, preserve tone."""


def parse_srt(text: str):
    blocks = re.split(r"\n\s*\n", text.strip())
    cues = []
    for b in blocks:
        lines = [ln.rstrip() for ln in b.splitlines() if ln.strip() != ""]
        if len(lines) < 3:
            continue
        times = lines[1].strip()
        body = " ".join(lines[2:]).strip()
        m = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            times,
        )
        if not m:
            continue
        cues.append({"start": m.group(1), "end": m.group(2), "en": body})
    return cues


def fix_en(s: str) -> str:
    s = s.strip()
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    return s


def srt_time_to_ass(t: str) -> str:
    t = t.replace(",", ".")
    h, m, rest = t.split(":")
    sec, ms = rest.split(".")
    cs = int(ms[:2])
    return f"{int(h)}:{m}:{sec}.{cs:02d}"


def ass_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def translate_cues_google(cues, sleep_s: float = 0.08):
    """Fallback: Google Translate (deep-translator), one cue at a time."""
    try:
        from deep_translator import GoogleTranslator
    except ImportError as e:
        raise SystemExit(
            "deep-translator required: pip install deep-translator"
        ) from e

    tr = GoogleTranslator(source="en", target="zh-CN")
    for i, c in enumerate(cues):
        c["en"] = fix_en(c["en"])
        for attempt in range(5):
            try:
                zh = tr.translate(c["en"]) or c["en"]
                c["zh"] = zh
                break
            except Exception as err:
                print(f"retry {attempt+1} #{i+1}: {err}")
                time.sleep(1.5 * (attempt + 1))
        else:
            c["zh"] = c["en"]
        if (i + 1) % 20 == 0 or i == 0:
            print(f"[{i+1}/{len(cues)}] {c['en'][:40]} -> {c['zh'][:30]}")
        time.sleep(sleep_s)
    return cues


def translate_cues_openai(cues, api_key, base_url, model, batch_size=20):
    """Batch-translate via OpenAI-compatible chat/completions API."""
    import requests

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    endpoint = f"{base_url.rstrip('/')}/chat/completions"

    for batch_start in range(0, len(cues), batch_size):
        batch = cues[batch_start:batch_start + batch_size]
        for c in batch:
            c["en"] = fix_en(c["en"])

        numbered = "\n".join(
            f"{i+1}. {c['en']}" for i, c in enumerate(batch)
        )
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Translate these {len(batch)} English subtitle lines "
                        f"to Chinese. Return ONLY {len(batch)} lines "
                        f"(one translation per line, same order):\n\n{numbered}"
                    ),
                },
            ],
            "temperature": 0.1,
            "max_tokens": 4000,
        }

        for attempt in range(3):
            try:
                resp = requests.post(
                    endpoint, headers=headers, json=payload, timeout=90
                )
                resp.raise_for_status()
                body = resp.json()
                content = body["choices"][0]["message"]["content"].strip()
                lines = [ln.strip() for ln in content.split("\n") if ln.strip()]

                # Strip leading numbers if present ("1. 中文" → "中文")
                cleaned = []
                for ln in lines:
                    ln = re.sub(r"^\d+[\.\、\s]+\s*", "", ln).strip()
                    cleaned.append(ln)

                if len(cleaned) != len(batch):
                    print(
                        f"WARNING: expected {len(batch)} translations, "
                        f"got {len(cleaned)} — falling back to raw split"
                    )
                    # Best-effort: pad or truncate
                    while len(cleaned) < len(batch):
                        cleaned.append(batch[len(cleaned)]["en"])
                    cleaned = cleaned[: len(batch)]

                for c, zh in zip(batch, cleaned):
                    c["zh"] = zh

                idx = batch_start + 1
                print(
                    f"[{idx}-{idx + len(batch) - 1}/{len(cues)}] "
                    f"batch OK ({len(batch)} cues)"
                )
                break
            except Exception as err:
                print(f"OpenAI attempt {attempt+1} failed: {err}")
                if attempt < 2:
                    time.sleep(2.0 * (attempt + 1))
        else:
            raise RuntimeError(
                f"OpenAI batch {batch_start}-{batch_start + batch_size} "
                f"failed after 3 attempts"
            )

    return cues


def translate_cues(cues, translator="google", sleep_s=0.08, **kwargs):
    """Dispatch to the selected translator.

    translator='google' uses deep-translator (Google Translate).
    translator='openai' uses OpenAI-compatible API.
    translator='local' uses local ollama (gemma3:1b by default).
    Falls back to google if openai/local is unavailable.
    """
    if translator in ("openai", "local"):
        if translator == "local":
            api_key = kwargs.get("api_key") or "ollama"
            base_url = kwargs.get("base_url") or os.environ.get(
                "OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1"
            )
            model = kwargs.get("model", "translategemma:4b-it-q8_0")
            batch_size = int(kwargs.get("batch_size", 15))
            # Check if ollama is reachable
            import requests as _r
            try:
                _r.get(base_url.rstrip("/") + "/models", timeout=3)
            except Exception:
                print(
                    "Local ollama not reachable at " + base_url +
                    " — falling back to Google Translate",
                    file=sys.stderr,
                )
                return translate_cues_google(cues, sleep_s=sleep_s)
        else:
            api_key = kwargs.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                print(
                    "OPENAI_API_KEY not set — falling back to Google Translate",
                    file=sys.stderr,
                )
                return translate_cues_google(cues, sleep_s=sleep_s)
            base_url = kwargs.get("base_url") or os.environ.get(
                "OPENAI_BASE_URL", "https://api.openai.com/v1"
            )
            model = kwargs.get("model", "gpt-4o-mini")
            batch_size = int(kwargs.get("batch_size", 20))

        try:
            print(f"Translating {len(cues)} cues with {model} @ {base_url}")
            return translate_cues_openai(
                cues, api_key=api_key, base_url=base_url,
                model=model, batch_size=batch_size,
            )
        except Exception as err:
            print(
                f"Translation failed: {err}\n"
                f"Falling back to Google Translate...",
                file=sys.stderr,
            )
            return translate_cues_google(cues, sleep_s=sleep_s)

    return translate_cues_google(cues, sleep_s=sleep_s)


def write_outputs(cues, out_dir: Path, cn_size: int, en_size: int):
    out_dir.mkdir(parents=True, exist_ok=True)
    en_path = out_dir / "english_clean.srt"
    bi_path = out_dir / "bilingual_subs.srt"
    ass_path = out_dir / "bilingual_subs.ass"

    en_lines, bi_lines = [], []
    for i, c in enumerate(cues, 1):
        en_lines.append(f"{i}\n{c['start']} --> {c['end']}\n{c['en']}\n")
        bi_lines.append(
            f"{i}\n{c['start']} --> {c['end']}\n{c['zh']}\n{c['en']}\n"
        )
    en_path.write_text("\n".join(en_lines), encoding="utf-8")
    bi_path.write_text("\n".join(bi_lines), encoding="utf-8")

    # PlayRes 1920x1080; burns fine on 4K
    header = f"""[Script Info]
Title: Bilingual CN+EN
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CN,Microsoft YaHei,{cn_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2.4,1.2,2,40,40,88,1
Style: EN,Arial,{en_size},&H00DDDDDD,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.6,0.8,2,40,40,28,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for c in cues:
        start, end = srt_time_to_ass(c["start"]), srt_time_to_ass(c["end"])
        events.append(
            f"Dialogue: 0,{start},{end},CN,,0,0,0,,{ass_escape(c['zh'])}"
        )
        events.append(
            f"Dialogue: 0,{start},{end},EN,,0,0,0,,{ass_escape(c['en'])}"
        )
    ass_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8-sig")
    print(f"Wrote {en_path}")
    print(f"Wrote {bi_path}")
    print(f"Wrote {ass_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--srt", required=True, help="English SRT path")
    ap.add_argument("--out-dir", default="subs")
    ap.add_argument("--cn-size", type=int, default=46)
    ap.add_argument("--en-size", type=int, default=24)
    ap.add_argument(
        "--layout",
        default="cn-top-en-bottom",
        choices=["cn-top-en-bottom"],
        help="Currently only cn-top-en-bottom",
    )
    ap.add_argument(
        "--translator",
        default="google",
        choices=["google", "openai", "local"],
        help="Translation engine (default: google). openai=OpenAI API, local=ollama @ 127.0.0.1:11434",
    )
    ap.add_argument(
        "--model",
        default=None,
        help="Model name (default: gpt-4o-mini for openai, translategemma:4b-it-q8_0 for local)",
    )
    ap.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Cues per API call for --translator openai (default: 20)",
    )
    ap.add_argument(
        "--no-translate",
        action="store_true",
        help="Skip translation entirely (zh field must already exist in cues)",
    )
    args = ap.parse_args()

    src = Path(args.srt)
    cues = parse_srt(src.read_text(encoding="utf-8"))
    print(f"Parsed {len(cues)} cues from {src}")
    if not args.no_translate:
        kwargs = {}
        if args.model:
            kwargs["model"] = args.model
        kwargs["batch_size"] = args.batch_size
        cues = translate_cues(
            cues,
            translator=args.translator,
            **kwargs,
        )
    write_outputs(cues, Path(args.out_dir), args.cn_size, args.en_size)


if __name__ == "__main__":
    main()
