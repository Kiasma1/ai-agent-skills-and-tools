#!/usr/bin/env python3
"""OpenRouter contextual JSON translation for bilingual subtitle generation."""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path

import requests

from build_bilingual_subs import parse_srt, write_outputs

GLOSSARY = {
    "Agent Harness": "智能体运行框架",
    "harness in AI-agent/code/runtime context": "智能体运行框架（禁止译为马具）",
    "Pi": "Pi", "tool calling": "工具调用", "prompt": "提示词",
    "context window": "上下文窗口",
}


def translate(cues, key, model, size):
    session, translated = requests.Session(), {}
    for start in range(0, len(cues), size):
        batch = cues[start:start + size]
        context = cues[max(0, start - 2):min(len(cues), start + size + 2)]
        source = {
            "glossary": GLOSSARY,
            "context_only": [{"id": i + 1, "en": c["en"]} for i, c in enumerate(context)],
            "cues_to_translate": [{"id": start + i + 1, "start": c["start"], "end": c["end"], "en": c["en"]} for i, c in enumerate(batch)],
            "output_schema": {"translations": [{"id": "integer", "zh": "string"}]},
        }
        system = (
            "Translate English technical-video subtitles into concise Simplified Chinese. "
            "Return ONLY valid JSON matching output_schema. Preserve every cue id; do not add, omit, merge, or split. "
            "Preserve timestamps, URLs, commands, flags, filenames, product names, and code exactly. Every zh must be nonempty, including sentence fragments. "
            "Use the glossary exactly. Every cue whose English contains 'harness' MUST include the exact Chinese string 智能体运行框架, even when it is a sentence fragment; never use 马具."
        )
        body = {"model": model, "temperature": 0, "reasoning_effort": "low", "max_tokens": 8000, "response_format": {"type": "json_object"},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(source, ensure_ascii=False)}]}
        expected = set(range(start + 1, start + len(batch) + 1))
        for attempt in range(3):
            try:
                response = session.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=body, timeout=45)
                response.raise_for_status()
                items = json.loads(response.json()["choices"][0]["message"]["content"])["translations"]
                if {x.get("id") for x in items} != expected:
                    raise ValueError("cue IDs do not match")
                for cue, item in zip(batch, sorted(items, key=lambda x: x["id"])):
                    zh = item["zh"].strip()
                    if re.search(r"\bharness\b", cue["en"], re.I) and "智能体运行框架" not in zh:
                        zh = zh.rstrip("，。 ") + "的智能体运行框架"
                    if not zh or "马具" in zh:
                        raise ValueError(f"glossary validation failed for cue {item['id']}: {zh}")
                    translated[item["id"]] = zh
                print(f"Translated {start + 1}-{start + len(batch)} / {len(cues)}", flush=True)
                break
            except Exception as error:
                if attempt == 2:
                    raise
                print(f"Retrying {start + 1}-{start + len(batch)}: {type(error).__name__}", flush=True)
                time.sleep(2 * (attempt + 1))
    for i, cue in enumerate(cues, 1):
        cue["zh"] = translated[i]
    return cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--out-dir", default="subs")
    ap.add_argument("--batch-size", type=int, default=30, choices=range(20, 41))
    ap.add_argument("--model", default="google/gemini-3.1-pro-preview")
    args = ap.parse_args()
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("OPENROUTER_API_KEY is required")
    cues = translate(parse_srt(Path(args.srt).read_text(encoding="utf-8")), key, args.model, args.batch_size)
    write_outputs(cues, Path(args.out_dir), 46, 24)


if __name__ == "__main__":
    main()
