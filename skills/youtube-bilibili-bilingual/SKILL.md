---
name: youtube-bilibili-bilingual
description: >
  YouTube 视频转 B 站双语硬字幕投稿全流程：yt-dlp 下载、Whisper 转写、中英双语字幕
  （默认中上英下、英文更小）、FFmpeg 烧录、简介/标签/排名总结、biliup 转载上传、带时间戳评论。
  Use when the user runs /youtube-bilibili-bilingual, or asks to 转B站, 双语字幕投稿, YouTube to Bilibili,
  硬字幕, 烧录字幕, biliup 上传, 转载投稿, 中上英下, bilingual subtitles for Bilibili.
license: MIT
tags:
  - youtube
  - bilibili
  - subtitles
  - bilingual
  - video
  - whisper
  - ffmpeg
  - translation
metadata:
  short-description: "YouTube → 双语硬字幕 → B站转载投稿"
  version: "1.0.0"
  platform: "Windows / Linux"
  runtime: "Claude Code / Codex / OpenClaw"
---

# YouTube → Bilibili 双语硬字幕投稿

把 YouTube 视频做成 **B 站可投稿成片**（默认硬字幕），并准备/执行转载投稿与带跳转的排名/要点评论。

## 默认约定（可被用户覆盖）

| 项 | 默认 |
|----|------|
| 字幕 | **硬字幕烧录** |
| 布局 | **中上英下**；中文大字，英文小字 |
| 分辨率 | **最高可用**（常为 4K） |
| 版权 | **转载非原创** `copyright=2`，必须填 `source` |
| 标题 | **不要**写「中上英下」等制作参数 |
| 上传 | 需 cookie；无 cookie 时引导扫码，**禁止编造已上传** |
| 工作目录 | `~/bilibili-workflow/<youtube_id>/` |

## 触发后先收集

1. YouTube URL（必填）
2. B 站标题（可选；否则用原标题中文化改写，**不含**字幕样式说明）
3. 原频道名（简介署名）
4. 字幕偏好（默认中上英下硬字幕）
5. 是否自动上传 / 是否发排名评论（默认：做成片后询问再上传）

## 工具依赖

检查并缺啥装啥（Windows 优先）：

- `yt-dlp`、`ffmpeg`、`ffprobe`
- Python + `openai-whisper`（或 `faster-whisper`）；有 CUDA 用 GPU
- 翻译：`deep-translator`（或 agent 自行高质量翻译）
- 投稿：`biliup-rs` 的 `biliup.exe`（推荐）或 `pip install biliup`
- 字体：`Microsoft YaHei` + `Arial`（或 Noto Sans SC）

Cookie 默认路径：`%USERPROFILE%\.bilibili\cookies.json`

登录（需用户本机交互终端）：

```powershell
& "<path-to>\biliup.exe" -u "$env:USERPROFILE\.bilibili\cookies.json" login
```

## 流水线（严格按序）

### 1. 工作区与下载

```text
~/bilibili-workflow/<id>/
  original_video.mp4
  original_video.jpg          # cover
  original_video.info.json
  audio.wav
  subs/
  final_bilibili_video.mp4
  bilibili_description.txt
```

```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 \
  --write-thumbnail --convert-thumbnails jpg --write-info-json \
  -o "original_video.%(ext)s" "YOUTUBE_URL"
```

记录：`title`、`channel`、`id`、`duration`、分辨率。

### 2. 抽音频 + STT

```bash
ffmpeg -y -i original_video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

Whisper（推荐）：

```bash
python -m whisper audio.wav --model large-v3 --language en --task transcribe \
  --output_format srt --output_dir ./subs --device cuda --fp16 True \
  --condition_on_previous_text False --temperature 0
```

要点：

- 无 CUDA 则 `--device cpu`，可降到 `medium`
- 若出现**重复幻觉**，立刻停掉，加 `--condition_on_previous_text False` 重跑
- 输出：`subs/audio.srt` 或 `subs/english_clean.srt`

### 3. 双语字幕（中上英下 + 英文更小）

**必须用 ASS 双 Style**（SRT 的 force_style 无法让两行字号不同）。

- Style `CN`：微软雅黑，大字号，更大 `MarginV`（更靠上）
- Style `EN`：Arial，小字号，较小 `MarginV`（更靠下）
- 每个 cue 两条 `Dialogue`：先中后英

可用本 skill 脚本：

```bash
# 默认 Google Translate（免费，逐句翻译）
python scripts/build_bilingual_subs.py --srt subs/audio.srt --out-dir subs \
  --layout cn-top-en-bottom

# 或使用本地 LLM（ollama + translategemma:4b-it-q8_0，需先 `ollama pull translategemma:4b-it-q8_0`）
python scripts/build_bilingual_subs.py --srt subs/audio.srt --out-dir subs \
  --translator local

# 或使用远程 OpenAI 兼容 API（需 OPENAI_API_KEY 环境变量）
python scripts/build_bilingual_subs.py --srt subs/audio.srt --out-dir subs \
  --translator openai --model gpt-4o-mini
```

Agent 也可自行翻译后写 ASS。专有名词、品牌名、金属/术语保持中英一致。

### 4. 烧录硬字幕

优先 `h264_nvenc`；驱动过旧则 `libx264`。

```bash
ffmpeg -y -i original_video.mp4 \
  -vf "ass='SUBS/bilingual_subs.ass'" \
  -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  final_bilibili_video.mp4
```

Windows 路径在 `ass=` 里要正确转义。完成后 `ffprobe` 确认分辨率与音视频流。

### 5. 简介 / 标签 / 封面

写 `bilibili_description.txt`：

1. 中文 3–5 句看点摘要  
2. 若内容是排行/清单：**中英对照总结**（见下）  
3. 转载声明 + 原频道 + 原标题 + 原链接  
4. 标签建议；封面用 `original_video.jpg`

**标题规则：** 吸引点击 + 主题；**禁止**塞入「中上英下」「硬字幕」等工艺词。

转载声明模板：

```text
本视频转载自 YouTube 原作者 [Channel] 的视频《[Title]》
原视频链接：https://www.youtube.com/watch?v=ID
感谢原作者的精彩内容！仅供学习交流，版权归原作者所有。
```

### 6. 排名/要点 + 时间戳（高价值内容必做）

从英文字幕对齐每个条目的**首次出现时间**，生成可点击跳转列表。

B 站评论中 `00:01:23` / `00:32` 形式可被点跳：

```text
【本视频排名总结 · 点击时间可跳转】
■ S 级 · S Tier
00:05:29 铂金950 / Platinum 950
...
```

- 中英文物体名都要有：`中文 / English`
- 时间从 SRT 提取，宁早一点进入话题，勿指错章节
- 可用 `scripts/post_bilibili_comment.py`

### 7. 上传 B 站

**无 cookie 禁止声称已上传。** 先检查：

`%USERPROFILE%\.bilibili\cookies.json`

```bash
biliup -u "%USERPROFILE%\.bilibili\cookies.json" upload final_bilibili_video.mp4 \
  --copyright 2 \
  --source "https://www.youtube.com/watch?v=ID" \
  --tid 201 \
  --cover original_video.jpg \
  --title "中文标题（无工艺词）" \
  --desc "完整简介" \
  --tag "双语字幕,英语,转载,..." \
  --no-reprint 0
```

- `copyright 2` = **转载/非原创**（自制是 1）
- `tid` 按内容选：科普常用 `201`（科学科普）；不确定则问用户
- 成功后记录 `bvid`、链接、审核状态
- 改标题/简介：member 编辑 API（见 `scripts/edit_bilibili_archive.py`）
- 验证：`biliup show BVxxxx` 看 `copyright`、`source`、`title`、`state_desc`

### 8. 交付清单

向用户汇报：

1. `final_bilibili_video.mp4` 路径与分辨率  
2. 双语 SRT/ASS 路径  
3. 简介全文 + 标签 + 封面  
4. 若已上传：`https://www.bilibili.com/video/BVxxxx`、是否转载、审核状态  
5. 若已评论：评论已带时间戳跳转  

## 故障速查

| 现象 | 处理 |
|------|------|
| Windows 弹「选择应用打开 cbm-…」 | 与本流程无关；Grok 侧关 Claude hooks |
| Whisper 循环重复句 | `--condition_on_previous_text False` 重跑 |
| NVENC 报 driver API | 改 `libx264` |
| biliup login `not a terminal` | 用户本机真实终端扫码 |
| 上传成功但仍像自制 | `show` 查 `copyright` 是否为 2 |
| 中文乱码（控制台） | 文件用 UTF-8；用 Python 读验证，勿信 GBK 终端 |

## 版权与安全

- 一律按**转载**处理并署名；不绕过权限/付费墙  
- 不在 skill 或日志里打印完整 cookie  
- 上传前若用户未明确要求，先确认再投稿  

## 本 skill 脚本

均在 `scripts/`（相对 skill 根目录）：

| 脚本 | 用途 |
|------|------|
| `build_bilingual_subs.py` | EN SRT → 翻译 → bilingual SRT + ASS（中上英下） |
| `burn_hardsubs.py` | FFmpeg 烧录 ASS → `final_bilibili_video.mp4` |
| `edit_bilibili_archive.py` | 改标题/简介（web edit API） |
| `post_bilibili_comment.py` | 发评论（含时间戳排名） |
| `extract_topic_timestamps.py` | 从 SRT 抽关键词首次时间，辅助写跳转评论 |

执行时用 skill 的绝对路径调用，例如：

```powershell
python "$env:USERPROFILE\.grok\skills\youtube-bilibili-bilingual\scripts\build_bilingual_subs.py" --help
```
