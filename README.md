# AI Agent Skills 与生态工具清单

> 最后更新：2026-07-28（中国标准时间）
> 维护者：[@Kiasma1](https://github.com/Kiasma1)

这是我的 Agent 能力资产索引：优先记录我自己创建或维护的项目，再列出当前采用的工具栈与外部 skill。它不是“装得越多越好”的清单，而是一份按任务选择能力的地图。

> **当前立场**：~~superpowers~~ 已成为历史记录，不再是默认工作流或新机复刻项。LLM 已能承担大量规划、编码、调试与验证；默认选择轻量 skill、合适工具和清晰验收标准，只在任务确有需要时增加约束。

---

## 导览

| 想找什么 | 去哪里 |
|---|---|
| 我自己拥有、创建或维护的能力 | [自有与自创资产](#一自有与自创资产) |
| 当前推荐的运行时、插件与 MCP | [当前推荐栈](#二当前推荐栈) |
| 可按需安装的外部 skill | [外部 skill](#三外部-skill按需使用) |
| 旧环境与 ~~superpowers~~ 记录 | [历史归档](#四历史归档) |
| 新电脑的最小复刻步骤 | [新电脑复刻](#五新电脑最小复刻) |

---

## 一、自有与自创资产

以下项目来自 [Kiasma1](https://github.com/Kiasma1) 的公开仓库。`创建` 表示原创项目；`维护/改造` 明确表示并非原始作者。

| 项目 | 身份 | 能力与适用场景 |
|---|---|---|
| [ai-agent-skills-and-tools](https://github.com/Kiasma1/ai-agent-skills-and-tools) | 创建 | 本仓库：跨 Claude Code、Codex、OpenClaw、Cursor、Hermes 的 Agent skill 与工具资产索引。 |
| [lzc-explain-words](https://github.com/Kiasma1/lzc-explain-words) | 创建 | 博物馆级双语英文词卡：词源、细微语义、Mermaid 语义拓扑、离线 HTML 渲染。 |
| [lxgw-screen-typography](https://github.com/Kiasma1/lxgw-screen-typography) | 创建 | Codex 排版 skill：霞鹜新致宋正文、新晰黑界面与 LXGW Bright 西文混排。 |
| [understand-learn](https://github.com/Kiasma1/understand-learn) | 创建 | 交互式代码导师：预测—验证循环、练习与跨会话学习进度。 |
| [youtube-bilibili-bilingual](https://github.com/Kiasma1/youtube-bilibili-bilingual) | 创建 | YouTube 下载、双语硬字幕、B 站投稿与时间戳评论的端到端 Agent 工作流。 |
| [sansheng-distill](https://github.com/Kiasma1/sansheng-distill) | 维护/社区复刻 | 多 Agent 书籍与视频蒸馏，输出带来源的交互式 HTML；原项目作者为叁笙。 |

### 使用原则

- 优先从自有项目中选择与任务直接匹配的 skill，而不是套用一整套通用流程。
- 每个项目的安装方式、依赖与平台兼容性以其自身 README 为准。
- 私有仓库与个人配置不在公开清单中展开。

---

## 二、当前推荐栈

### 2.1 工作方式

`任务 → 选择单项 skill / 工具 → 执行 → 用验收标准验证`。

不默认叠加流程框架；需要更严格的测试、研究、代码审查或并行协作时，再按需引入对应能力。

### 2.2 已启用插件

| 插件 | 作用 | 备注 |
|---|---|---|
| [caveman](https://github.com/JuliusBrussee/caveman) | 高密度、简洁的技术沟通 | 可用 `stop caveman` 关闭。 |
| [ponytail](https://github.com/DietrichGebert/ponytail) | YAGNI、库优先、最小 diff 的工程约束 | 可用 `stop ponytail` 关闭。 |

### 2.3 MCP 服务

| MCP 服务 | 作用 | 前置条件 |
|---|---|---|
| `codegraph` | 跨文件语义搜索、调用链与影响分析 | 项目内先执行 `codegraph init`。 |
| `codebase-memory-mcp` | 本地代码库知识图谱与持久化记忆 | 在配置中填写本机可执行文件的绝对路径。 |

### 2.4 可选状态栏

<details>
<summary>查看 caveman / ponytail 合一状态栏配置</summary>

两个插件分别写入 `~/.claude/.caveman-active` 与 `~/.claude/.ponytail-active` 标记。可将 `~/.claude/settings.json` 的 `statusLine` 指向下面脚本：

```json
"statusLine": {
  "type": "command",
  "command": "powershell -ExecutionPolicy Bypass -File \"<HOME>\\.claude\\plugins\\cache\\cp-statusline\\combined-statusline.ps1\""
}
```

```powershell
$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME ".claude" }
function Get-FlagLevel($Name) {
    $p = Join-Path $ClaudeDir $Name
    if (-not (Test-Path $p)) { return $null }
    try { $r = (Get-Content $p -ErrorAction Stop | Select-Object -First 1).Trim(); if ([string]::IsNullOrEmpty($r)) { return $null }; return $r } catch { return $null }
}
$caveman = Get-FlagLevel ".caveman-active"
$pony = Get-FlagLevel ".ponytail-active"
if ($null -eq $caveman -and $null -eq $pony) { exit 0 }
$Esc = [char]27
function Render($Label, $Level, $Color) {
    if ([string]::IsNullOrEmpty($Level) -or $Level -eq "full") { return "${Esc}[38;5;${Color}m[${Label}]${Esc}[0m" }
    return "${Esc}[38;5;${Color}m[${Label}:$($Level.ToUpperInvariant())]${Esc}[0m"
}
if ($null -ne $caveman -and $null -ne $pony) {
    [Console]::Write("${Esc}[38;5;173m[CAVEMAN & PONYTAIL]${Esc}[0m")
} elseif ($null -ne $caveman) {
    [Console]::Write((Render "CAVEMAN" $caveman "33"))
} else {
    [Console]::Write((Render "PONYTAIL" $pony "108"))
}
```

</details>

---

## 三、外部 Skill（按需使用）

### 3.1 工程与协作：Atom / ask-matt

来源：[mattpocock/atom](https://github.com/mattpocock/atom)。适合已有明确工程问题时选择性调用，而非作为每次对话的固定流程。

| Skill | 用途 |
|---|---|
| `ask-matt` | 根据任务描述路由到合适的 skill 或流程。 |
| `handoff` / `claude-handoff` | 将当前工作沉淀为可继续执行的交接内容。 |
| `implement` | 基于 spec 或 ticket 实现一个小范围改动。 |
| `to-spec` / `to-tickets` | 将对话整理为规格或可执行 ticket。 |
| `triage` / `wayfinder` | 分类问题、梳理长周期工作与依赖。 |
| `improve-codebase-architecture` | 扫描架构改进机会并生成报告。 |
| `grill-me` / `grill-with-docs` / `grilling` | 压力测试设计、计划或决策。 |

### 3.2 专项能力

| Skill / 项目 | 用途 | 来源 |
|---|---|---|
| `cangjie-skill` | 将中文扫描书蒸馏为可复用 skill 或 Markdown Handbook。 | [Kiasma1/cangjie-skill](https://github.com/Kiasma1/cangjie-skill)（fork） |
| `darwin-skill` | 用 SkillLens rubric 与 hill-climbing 优化 `SKILL.md`。 | [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) |
| `nuwa-skill` | 从人名或模糊需求出发，生成可运行的人物视角 skill。 | [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) |
| `steve-jobs-perspective` | 以乔布斯视角审视产品和设计。 | [alchaincyf/steve-jobs-skill](https://github.com/alchaincyf/steve-jobs-skill) |

---

## 四、历史归档

<details>
<summary>展开 ~~superpowers~~ 历史记录（仅供溯源，不推荐安装）</summary>

来源：[obra/superpowers](https://github.com/obra/superpowers) 与 [superpowers-marketplace](https://github.com/obra/superpowers-marketplace)。以下能力曾安装在本机，但不再是推荐配置：

| 类别 | 历史 skill |
|---|---|
| 规划与质量 | `brainstorming`、`writing-plans`、`executing-plans`、`test-driven-development`、`systematic-debugging`、`verification-before-completion` |
| 评审与协作 | `code-review`、`requesting-code-review`、`receiving-code-review`、`dispatching-parallel-agents`、`subagent-driven-development`、`using-git-worktrees`、`finishing-a-development-branch` |
| 编程实践 | `coding-discipline`、`diagnosing-bugs`、`domain-modeling`、`prototype`、`research`、`teach`、`writing-great-skills`、`codebase-design` |

其方法中的个别原则仍可被任务需要时采用，但不再通过整套插件或固定流程强制执行。

</details>

---

## 五、新电脑最小复刻

只安装当前任务真正需要的部分；不要为了“完整”而恢复历史栈。

### 5.1 安装当前推荐插件

```bash
/plugin marketplace add JuliusBrussee/caveman
/plugin marketplace add DietrichGebert/ponytail

/plugin install caveman@caveman
/plugin install ponytail@ponytail
```

### 5.2 选择并安装 skill

先从上方“自有与自创资产”选择，再按需补充外部 skill。以各仓库的 README 为准；无需安装 ~~superpowers~~ 全套。

### 5.3 配置 MCP

在 `~/.claude.json` 的顶层 `mcpServers` 中配置本机实际路径：

```json
"mcpServers": {
  "codegraph": {
    "type": "stdio",
    "command": "codegraph",
    "args": ["serve", "--mcp"]
  },
  "codebase-memory-mcp": {
    "command": "C:/路径/到/codebase-memory-mcp.exe"
  }
}
```

### 5.4 验收清单

- [ ] 仅启用实际需要的插件与 skill。
- [ ] 若使用 `codegraph`，目标仓库已经初始化索引。
- [ ] MCP 服务能在会话中正常出现并调用。
- [ ] 用一个真实任务验证当前配置，而不是按数量检查安装目录。

---

## 维护说明

- 自有项目清单以 [Kiasma1 的公开仓库](https://github.com/Kiasma1?tab=repositories) 为准；私有项目不在此列。
- 外部工具、插件与 skill 的安装状态会变化；更新本页时优先更新“当前推荐栈”和“自有与自创资产”。
- 历史条目保留其来源链接和能力摘要，方便追溯，但不应被误解为当前建议。
