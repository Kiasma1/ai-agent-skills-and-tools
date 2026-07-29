---
name: lxgw-screen-typography
description: "Apply a fixed LXGW screen-typography system in websites, interfaces, documents, presentations, and other designed artifacts: LXGW Neo ZhiSong Screen for Chinese reading text, LXGW Neo XiHei Screen for Chinese interface text, and LXGW Bright for English, Latin word roots, and ASCII numbers. Use when the user names these fonts, requests this exact Chinese body/UI/Latin pairing, asks for a reusable typography system, or wants mixed-script typography without merging incompatible font binaries."
---

# LXGW Screen Typography

Apply the user's three-font mapping by semantic role while keeping the source font files separate.

## Canonical mapping

| Content role | Font |
| --- | --- |
| Chinese reading text | `LXGW Neo ZhiSong Screen` / 霞鹜新致宋 屏幕阅读版 |
| Chinese interface text | `LXGW Neo XiHei Screen` / 霞鹜新晰黑 屏幕阅读版 |
| English, Latin word roots, ASCII numbers | `LXGW Bright` |

Treat “word roots” as Latin-script letter sequences. Keep Chinese punctuation with the surrounding Chinese role unless the user requests another convention.

## Workflow

1. Confirm that the three fonts are installed or available as user-supplied files. Do not silently substitute another typeface.
2. Classify text by semantic role:
   - Use the reading face for articles, descriptions, essays, long captions, quotations, and other sustained Chinese prose.
   - Use the interface face for navigation, buttons, form labels, tabs, metadata, badges, table headers, controls, and application chrome.
   - Keep editorial headings inside a reading surface in the reading face unless they function as navigation.
   - Apply Bright to English runs, Latin roots, abbreviations, ASCII digits, and ASCII punctuation adjoining those runs.
3. Implement the mapping with separate font resources:
   - For HTML/CSS, copy and adapt `assets/lxgw-screen-typography.css`. Use its Unicode-ranged virtual families.
   - For DOCX, PPTX, PDF, or rich-text output, split mixed text into script runs and assign fonts per run.
   - For design tools, create separate text styles for Chinese body, Chinese UI, and Latin/numeric runs.
4. Preserve readability:
   - Do not synthesize bold or italic unless the target font has the requested face.
   - Prefer size, color, spacing, or hierarchy over fake bolding when only Regular is available.
   - Test representative Chinese-English-number mixtures at the actual target size.
5. Verify the artifact:
   - Chinese prose resolves to Neo ZhiSong Screen.
   - Chinese controls resolve to Neo XiHei Screen.
   - Latin letters and ASCII digits resolve to Bright.
   - Missing font files fail visibly or are reported; do not conceal them with an unrelated fallback.

## Licensing guardrail

Read `references/licensing-and-platforms.md` before downloading, embedding, packaging, merging, or redistributing fonts.

Do not produce or describe a merged TTF/OTF as redistribution-safe. The screen-reading fonts use IPA Font License 1.0, while LXGW Bright uses SIL OFL 1.1, and the upstream projects identify those licenses as incompatible. Prefer CSS Unicode ranges, rich-text runs, or platform font-role configuration.

If the user explicitly asks for a private local merge, explain the conflict first and keep any experiment local and clearly marked non-redistributable. Do not bundle source font binaries in this skill.

## Platform notes

- Web: use the virtual composite families in the bundled CSS; package each original font and its required license separately when redistribution is authorized.
- Documents and slides: set East Asian and Latin fonts independently where the format supports it; otherwise split runs.
- Figma and similar tools: use separate character styles because semantic script switching is not automatic.
- Android or desktop system replacement: map roles in the platform configuration when possible; do not assume one static TTF can detect “body” versus “interface.”
