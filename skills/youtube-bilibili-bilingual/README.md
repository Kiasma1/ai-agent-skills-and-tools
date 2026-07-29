<sub>🌐 <b>中文</b></sub>

<div align="center">

# youtube-bilibili-bilingual 🎬

> *「发现了一个很棒的 YouTube 英文视频想搬到 B 站？一句话，Agent 帮你从头跑到尾。」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-youtube--bilibili--bilingual-blueviolet)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)]()

**YouTube → Whisper 转写 → 中上英下硬字幕 → biliup 上传 → 时间戳排名评论，全流程 Agent 执行。**

[看看效果](#效果示例) · [安装](#快速开始) · [触发方式](#触发方式) · [它和同类有什么不同](#它和同类有什么不同) · [安全边界](#安全边界)

</div>

---

## 它解决什么问题

事情是这样的：你在 YouTube 上看到一个很棒的英文视频——可能是珠宝排行、技术讲解、设计分析——你想把它搬到 B 站，但接下来的事情让人头大：

1. **下载视频**，要最高画质，还得顺手拿封面
2. **Whisper 转写**，参数不对就容易陷入循环重复句（幻觉）
3. **翻译成中文**，还得做成**中上英下**的双语字幕——这不是 SRT 能搞定的，必须上 ASS 双 Style
4. **FFmpeg 烧录硬字幕**，Windows 上路径转义又是一个坑
5. **写简介**，转载声明、中英排名总结、标签建议——每条都得手工敲
6. **biliup 上传**，`copyright=2`（转载）别忘了，不然会被判定自制
7. 如果是排名类内容，还得在评论区发**带时间戳的中英对照排名**——让观众能点时间直接跳转

每一步都有坑。Whisper 幻觉、ASS 布局、FFmpeg 路径、biliup cookie、B 站时间戳格式……临时拼凑非常容易翻车。

**这个 Skill 把以上全部固化成一条流水线。** 你只需要给一个 YouTube 链接，Agent 按序执行，每步完成后汇报，最终交付：成片视频 + 双语字幕文件 + B站简介 + 时间戳排名评论 + BV 链接。

---

## 效果示例

### 最终产物：硬字幕烧录成品

三个真实案例的产物可在 [`examples/`](examples/) 查看：

| 案例 | YouTube 原片 | 成品 | 亮点 |
|---|---|---|---|
| 26种宝石排行 | [UEvbYcc0p9Q](https://www.youtube.com/watch?v=UEvbYcc0p9Q) | [description](examples/example1_gemstone_description.txt) · [comment](examples/example1_gemstone_comment.txt) | 8级排名中英对照 + 时间戳跳转 |
| 原子设计科普 | [Yi-A20x2dcA](https://www.youtube.com/watch?v=Yi-A20x2dcA) | [description](examples/example2_atomic_design_description.txt) · [comment](examples/example2_atomic_design_comment.txt) | 已上传 B站 BV1ktNR6gExm |
| 珠宝金属排行 | [tcpz2UTVihg](https://www.youtube.com/watch?v=tcpz2UTVihg) | [description](examples/example3_metal_description.txt) | 4K 3840×2160 硬字幕烧录 |

### 评论区时间戳排名（独有功能）

发到 B 站评论区后，时间戳可点击跳转：

```text
【本视频排名总结 · 点击时间可跳转】

■ God 级 · God Tier
00:15:59 刚玉（红宝石/蓝宝石） / Corundum (Ruby / Sapphire)

■ S 级 · S Tier
00:10:14 莫桑石 / Moissanite
00:12:22 培育钻石 / Lab Diamonds
...
```

B 站用户非常吃这个——排名类视频的评论区时间戳是天然的互动入口。

---

## 快速开始

### 1. 安装 Skill

```bash
# 克隆到你的 skills 目录
git clone https://github.com/<your-username>/youtube-bilibili-bilingual.git
```

### 2. 装依赖

```bash
pip install -r requirements.txt
```

需要系统工具 + 翻译引擎（三选一）：

- **yt-dlp**：`pip install yt-dlp` 或 `winget install yt-dlp`
- **ffmpeg**：`winget install ffmpeg`（Windows）或 `apt install ffmpeg`（Linux）
- **biliup**（上传用）：从 [biliup-rs releases](https://github.com/biliup/biliup-rs/releases) 下载 `biliup.exe`（Windows）或 `pip install biliup`
- **翻译引擎**（三选一，详见下方）

### 3. 选翻译引擎（三选一）

| 引擎 | 命令 | 成本 | 质量 |
|---|---|---|---|
| 🏠 本地 Ollama | `ollama pull translategemma:4b-it-q8_0` | 零 | ⭐⭐⭐⭐ |
| ☁️ OpenAI/DeepSeek | `export OPENAI_API_KEY=sk-xxx` | 按量 | ⭐⭐⭐⭐⭐ |
| 🔄 Google Translate | 无需配置（默认） | 零 | ⭐⭐⭐ |

### 4. B 站登录（仅上传时需要）

```powershell
biliup.exe -u "$env:USERPROFILE\.bilibili\cookies.json" login
```

### 4. 装完第一句话

对 Agent 说：

```text
把这个视频做成中上英下双语硬字幕投B站：https://www.youtube.com/watch?v=UEvbYcc0p9Q
```

---

## 触发方式

以下任意一句话都能触发：

- `/youtube-bilibili-bilingual https://www.youtube.com/watch?v=...`
- 「把这个 YouTube 视频转成双语字幕投 B 站」
- 「帮我做双语硬字幕，中上英下，然后上传 B 站」
- 「转载这个视频到 B 站，加双语字幕」
- 「YouTube to Bilibili bilingual subtitles」
- 「烧录字幕 + biliup 上传」
- 「做中上英下硬字幕，再发排名评论」

---

## 它能交付什么

| 步骤 | 交付物 | 说明 |
|---|---|---|
| 1. 下载 | `original_video.mp4` + 封面 + info.json | yt-dlp 最高画质 |
| 2. 转写 | `subs/audio.srt` | Whisper large-v3，防幻觉参数 |
| 3. 翻译+字幕 | `subs/bilingual_subs.srt` + `.ass` | 中上大字 / 英下小字，ASS 双 Style |
| 4. 烧录 | `final_bilibili_video.mp4` | FFmpeg 硬字幕，优先 NVENC |
| 5. 简介 | `bilibili_description.txt` | 中文看点 + 转载声明 + 标签分区建议 |
| 6. 评论 | 时间戳排名/要点列表 | B站 `HH:MM:SS` 可点击跳转 |
| 7. 上传 | BV 链接 | biliup `copyright=2` 转载投稿 |

---

## 它和同类有什么不同

| 维度 | 本 Skill | yt2bb | vorojar/bilingual-subtitle | zarazhangrui/bilingual-subtitles |
|---|---|---|---|---|
| YT→B站一条龙 | ✅ 下载→烧录→上传→评论 | ✅ 下载→字幕 | ❌ 只做字幕烧录 | ❌ 只做字幕烧录 |
| B站上传集成 | ✅ biliup + copyright=2 | ❓ | ❌ | ❌ |
| 时间戳排名评论 | ✅ 独有 | ❌ | ❌ | ❌ |
| 转载声明模板 | ✅ 内置 | ❓ | ❌ | ❌ |
| ASS 双语布局 | ✅ 中上英下双Style | ✅ | ✅ 卡拉OK逐词 | ✅ PNG overlay |
| Whisper 防幻觉 | ✅ 参数内置 | ❓ | ✅ 硬件加速检测 | ✅ |
| 真实案例 | ✅ 3个完整案例 | ❓ | ❓ | ❓ |
| 翻译方案 | Google / 本地LLM / OpenAI 三引擎 | ❓ | translate-shell | 无（外部） |

**一句话：同类做烧录，我们做闭环。** 从 YouTube 链接到 B 站 BV 号 + 时间戳评论，中间的每一步都固化了。

---

## 安全边界

这个 Skill **不会**做以下事情：

- ❌ **不会绕过付费墙或权限**下载受限内容
- ❌ **不会在未确认的情况下自动上传**——默认先做片，上传前询问
- ❌ **不会声称视频为自制**——一律按 `copyright=2` 转载处理并署名原作者
- ❌ **不会在日志或输出中打印完整 cookie**
- ❌ **不会修改用户本机除工作目录外的任何文件**

**何时会停下来问用户：**

- 上传前（除非用户明确说"自动上传"）
- B 站分区不确定时（如科普 vs 生活）
- 标题改写有多种选择时
- Whisper 出现幻觉需要重跑时

---

## 文件结构

```
youtube-bilibili-bilingual/
├── SKILL.md                  # Skill 主文件（Agent 读这个）
├── README.md                 # 你正在看
├── LICENSE                   # MIT
├── requirements.txt          # Python 依赖
├── test-prompts.json         # 测试用例与期望输出
├── examples/                 # 真实运行产物
│   ├── example1_gemstone_description.txt
│   ├── example1_gemstone_comment.txt
│   ├── example2_atomic_design_description.txt
│   ├── example2_atomic_design_comment.txt
│   └── example3_metal_description.txt
├── references/
│   └── workflow-checklist.md # 步骤检查清单
└── scripts/                  # 可独立运行的 Python 脚本
    ├── build_bilingual_subs.py    # EN SRT → 翻译 → 双语 SRT + ASS
    ├── burn_hardsubs.py           # FFmpeg 烧录 ASS → mp4
    ├── edit_bilibili_archive.py   # 修改 B站标题/简介（web API）
    ├── post_bilibili_comment.py   # 发 B站评论
    └── extract_topic_timestamps.py # 从 SRT 抽关键词时间戳
```

---

## 验证与测试

参见 [`test-prompts.json`](test-prompts.json)。核心验证：

```text
# 验收 prompt
把这个视频做成中上英下双语硬字幕投B站：
https://www.youtube.com/watch?v=UEvbYcc0p9Q
标题用「26种宝石排行：有些真的贵得离谱」
原频道：Mason Mignanelli
先做成片，上传前问我
```

**合格表现：**
1. `subs/bilingual_subs.ass` 包含 CN（46px, MarginV=88）和 EN（24px, MarginV=28）两个 Style
2. `bilibili_description.txt` 含转载声明 + 排名总结 + 标签建议
3. `final_bilibili_video.mp4` 分辨率 ≥ 1920×1080
4. 标题不含「中上英下」「硬字幕」等工艺词
5. 排名评论含 `HH:MM:SS` 格式时间戳 + 中英对照

---

## 致谢

- [Whisper](https://github.com/openai/whisper) by OpenAI — 语音转写
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 视频下载
- [biliup-rs](https://github.com/biliup/biliup-rs) — B站上传工具
- [ollama](https://ollama.com) — 本地 LLM 运行时
- [translategemma](https://ollama.com/library/translategemma) — 本地翻译模型
- [deep-translator](https://github.com/nidhaloff/deep-translator) — Google Translate 后端
- 同类 Skill 参考：[yt2bb](https://github.com/Agents365-ai/yt2bb)、[vorojar/bilingual-subtitle-skill](https://github.com/vorojar/bilingual-subtitle-skill)、[zarazhangrui/bilingual-subtitles](https://github.com/zarazhangrui/bilingual-subtitles)、[jianshuo/claude-skills](https://github.com/jianshuo/claude-skills)

## License

[MIT](LICENSE)

---

<div align="center">

*YouTube → 双语硬字幕 → B站投稿 + 时间戳评论，一句话，Agent 从头跑到尾。*

</div>
