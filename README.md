# AI Agent Skills 与生态工具清单

> 最后更新: 2026-07-10 中国标准时间
> wsqzlzc

清单按 **来源仓库** 分组,覆盖本机 `.claude/skills/` 下已安装的全部 skill、`.claude/plugins/` 下 Plugin(Marketplace) 暴露的 hook + skill,以及全局 MCP 服务。附 GitHub 地址与用途,方便溯源与复装。

---

## 一、本地已安装 Skills(~/.claude/skills/)

按作者/来源分 5 组。每组下列 `SKILL.md` 文件名、用途、来源仓库。

### 1. obra / superpowers(Jesse Vincent, Prime Radiant)
> 源仓库: https://github.com/obra/superpowers
> License: MIT
> 安装方式:
> ```
> /plugin marketplace add obra/superpowers-marketplace
> /plugin install superpowers@superpowers-marketplace
> ```

| # | Skill 文件 | 用途 |
|---|-----------|------|
| 1 | `brainstorming` | 需求调研 + 设计规格,动手写代码前先想清楚(「12 因子产品」路径) |
| 2 | `writing-plans` | 把规格拆成可执行步骤计划,落到 `docs/superpowers/plans/` |
| 3 | `executing-plans` | 逐步执行计划,每步校验;支持 subagent-driven |
| 4 | `test-driven-development` | 严格 TDD 红绿重构循环,未写失败测试不许写实现代码 |
| 5 | `systematic-debugging` | 定位→分析→假设→修复四阶段,防瞎猜 |
| 6 | `verification-before-completion` | 声称完成前必须跑验证命令,证据先行 |

### 2. obra / superpowers — 代码评审与协作组(同上源 13 个核心技能中的)
> 源仓库: https://github.com/obra/superpowers

| # | Skill 文件 | 用途 |
|---|-----------|------|
| 7 | `code-review` | 沿「标准 + 规格」两轴审 diff,并行 subagent,审 branch/PR/「review since X」|
| 8 | `requesting-code-review` | 派 review 代理审 diff |
| 9 | `receiving-code-review` | 收到 review 反馈后技术性处理,拒绝敷衍 |
| 10 | `dispatching-parallel-agents` | 2+ 无依赖任务并行跑 |
| 11 | `subagent-driven-development` | 一个任务一个子 agent + 两轮 review |
| 12 | `using-git-worktrees` | git worktree 隔离功能开发 |
| 13 | `finishing-a-development-branch` | 收尾期 merge/PR/keep/discard 决策树 |

### 3. obra / superpowers — 编程实践组
> 源仓库: https://github.com/obra/superpowers

| # | Skill 文件 | 用途 |
|---|-----------|------|
| 14 | `coding-discipline` | Karpathy 风格 + 终极 token 优化,产出 diff-only、无废话输出 |
| 15 | `diagnosing-bugs` | 硬 bug / 性能回退的命令式诊断循环;关键词 diagnose/debug/debug this |
| 16 | `domain-modeling` | 建立 / 锐化项目领域模型,术语表、通用语言、ADR |
| 17 | `prototype` | 搭 throwable 原型回答设计问题(Lo-fi HTML 渲染)
| 18 | `research` | 派 background agent 调研,抓一手源留 Markdown 到仓库 |
| 19 | `teach` | 在工作区内教用户新技能/概念 |
| 20 | `writing-great-skills` | 写 / 改 skill 的参考(vocabulary + 原则) |
| 21 | `codebase-design` | 共享 deep-module 词汇:接口、接缝、可测性、AI 可导航 |

### 4. Isaac Matt Pocock / Atom Skills(`setup-matt-pocock-skills` 拉取的一组工程 skill,以及 `ask-matt`)
> 源仓库:
> - https://github.com/mattpocock/atom (Atom 系列 skill)
> - `ask-matt` 是上面 router,定位「当前用哪个 skill/flow 合适」
> 安装方式(Auto 已配):
> ```
> /setup-matt-pocock-skills
> ```

| # | Skill 文件 | 用途 |
|---|-----------|------|
| 22 | `ask-matt` | 路由入口,根据描述建议应走哪个 skill/flow |
| 23 | `handoff` | 把当前对话压成 handoff 文档,另一 agent 即刻接手 |
| 24 | `claude-handoff` | 把对话交接给一个新的后台 agent(任务级交接,非通用 handoff) |
| 25 | `implement` | 基于 spec / ticket 实现一小块工作 |
| 26 | `to-spec` | 把当前对话合成为 spec 并发布到 issue tracker(纯整理,不访谈) |
| 27 | `to-tickets` | 把计划/spec 拆成 tracer-bullet tickets(带阻塞边),落到本地/真实 tracker |
| 28 | `triage` | 把 issue / 外部 PR 过「分类 → 核验 → grill → 写 agent-ready brief」状态机 |
| 29 | `wayfinder` | 海量工作(超一个 session)画调查 tickets 共享地图,逐张清出路线 |
| 30 | `improve-codebase-architecture` | 扫仓库找 deep-module 机会,可视化 HTML 报告 → grill 选定的一个 |
| 31 | `setup-matt-pocock-skills` | **一次性初始化**:配设 tracker、triage label 词汇、domain doc 布局 |
| 32 | `grill-me` | 硬审设计/计划的访谈(interview 式 stress-test) |
| 33 | `grill-with-docs` | 同上 hard,顺手生成 ADR 与 glossary |
| 34 | `grilling` | 通用的「grill」触发 stress-test,任意计划/设计 |

### 5. 个性作者 / 专项 skill(独立 GitHub 仓库各自一个)

| # | Skill 文件 | 用途 | 源仓库 |
|---|-----------|------|--------|
| 35 | `cangjie-skill` | **拆书**:把中文扫描书蒸馏成可复用 skill 或 MARKDOWN HANDBOOK(RapidOCR + 硬选型) | https://github.com/Kiasma1/cangjie-skill |
| 36 | `darwin-skill` | **Skill 自优化器 v2.0**:SkillLens 9 维 rubric + SkillOpt + hill-climbing 自动优化 SKILL.md | https://github.com/alchaincyf/darwin-skill |
| 37 | `nuwa-skill`(huashu-nuwa) | **造人**:输入人名或模糊需求 → 调研 → 思维框架 → 可运行的人物视角 skill | https://github.com/alchaincyf/nuwa-skill |
| 38 | `steve-jobs-skill`(steve-jobs-perspective) | 以乔布斯视角审视产品/设计,6 心智模型 + 8 启发式,传记/访谈一手提炼 | https://github.com/alchaincyf/steve-jobs-skill |
| 39 | `dataviz` | 任何图表 / 可视化(HTML SVG / Recharts / matplotlib 等)的风格系统配色 | (来自 c7179cdb9 / c2a91c7d7 — 平台内置 skill) |

> 注:本机 `~/.claude/skills/` 共 32 个 skill 目录。上表把 superpowers 13 + atom 12 + 专项 4 + 内置 = 全部覆盖。

---

## 二、Plugins(Marketplace,全局启用)

本机 `~/.claude/settings.json` 启用 3 个全局 Plugin,都带 **SessionStart / UserPromptSubmit** 钩子,会话级强制模式。

### 1. caveman (Julius Brussee)
- 仓库: https://github.com/JuliusBrussee/caveman
- 市场 key: `caveman@caveman`
- 用途 — **超压缩交流模式**:像 smart caveman 一样输出,实测砍 ~65% token 同时保留全部技术准确性;几乎每条消息响应
- 钩子:
  - `SessionStart` → `caveman-activate.js`
  - `UserPromptSubmit` → `caveman-mode-tracker.js`
- 级别:`full`(自动 — 关掉用 `stop caveman`)
- 自带 agents:`cavecrew-builder / investigator / reviewer`(1–2 文件的小改动/只读定位)
- 路径:`~/.claude/plugins/marketplaces/caveman/`

### 2. ponytail (Dietrich Gebert)
- 仓库: https://github.com/DietrichGebert/ponytail
- 市场 key: `ponytail@ponytail`
- 用途 — **Lazy senior dev 模式**:强制 YAGNI、库优先、最短 diff;先问「这段代码需要存在吗?」再写;bug 修在 root-cause 一处而非 all callers
- 级别:`full`(默认,`stop ponytail` 关)
- 路径:`~/.claude/plugins/cache/ponytail/ponytail/4.8.4/`

### 3. superpowers-marketplace (obra)
- 仓库: https://github.com/obra/superpowers-marketplace(市场);插件本身 https://github.com/obra/superpowers
- 市场 key: `superpowers@superpowers-marketplace`
- 用途 — 承载上文 13 个核心 skill + 若干 chrome / elements-of-style 扩展(本机当前启用核心 skill)
- 路径:`~/.claude/plugins/cache/superpowers-marketplace/superpowers/6.1.1/`

> 本机当前激活模式:**caveman full + ponytail full + superpowers 全部 skill**(叠加)`— 会话里表现:极简输出、YAGNI 行为、TDD/debug 严谨性同步生效。

---

## 三、全局 MCP Servers

本机 `~/.claude.json`(user) 层配置 2 个 MCP 服务:

| # | MCP 服务 | 传输 | 启动命令 | 用途 |
|---|---------|------|---------|------|
| 1 | `codegraph` | stdio | `codegraph serve --mcp` | 跨文件 / 跨服务的代码图语义搜索、调用链、影响分析(codegraph CLI) |
| 2 | `codebase-memory-mcp` | 本地 exe | `C:/Users/wsqzlzc/AppData/Local/Programs/codebase-memory-mcp/codebase-memory-mcp.exe` | 本地代码库 → 知识图谱 + GraphRAG 索引,给 agent 提供持久化代码记忆 |

配置源文件:`~/.claude.json` → `mcpServers.mcpServers` 节点。
> 注:`codegraph` 服务需先 `codegraph init` 索引仓库;本机 cc-switch-headroom 当前 **未索引**(inactivate,SKIP 收拢)。

---

## 四、复装命令速查

```bash
# 市场注册
/plugin marketplace add JuliusBrussee/caveman
/plugin marketplace add DietrichGebert/ponytail
/plugin marketplace add obra/superpowers-marketplace

# 启 3 大插件
/plugin install caveman@caveman
/plugin install ponytail@ponytail
/plugin install superpowers@superpowers-marketplace

# 个性 skill(直接 clone 到 ~/.claude/skills/)
git clone https://github.com/Kiasma1/cangjie-skill.git      ~/.claude/skills/cangjie-skill
git clone https://github.com/alchaincyf/darwin-skill.git   ~/.claude/skills/darwin-skill
git clone https://github.com/alchaincyf/nuwa-skill.git     ~/.claude/skills/nuwa-skill
git clone https://github.com/alchaincyf/steve-jobs-skill.git ~/.claude/skills/steve-jobs-skill

# MCP:改 ~/.claude.json → mcpServers 块(见第三节表)
```

## 五、新电脑复刻指南

把这套环境搬到另一台机器,按下面 4 步依次跑完即得(假设已装好 Claude Code CLI)。

### 5.1 注册 3 个 marketplace + 启插件

```bash
/plugin marketplace add JuliusBrussee/caveman
/plugin marketplace add DietrichGebert/ponytail
/plugin marketplace add obra/superpowers-marketplace

/plugin install caveman@caveman
/plugin install ponytail@ponytail
/plugin install superpowers@superpowers-marketplace
```

完成后 `~/.claude/settings.json` 的 `enabledPlugins` 应含上述三条 `true`。

### 5.2 装本地 skill(全部 clone 到 ~/.claude/skills/)

```bash
# 专项 skill(各自独立仓库)
git clone https://github.com/Kiasma1/cangjie-skill.git      ~/.claude/skills/cangjie-skill
git clone https://github.com/alchaincyf/darwin-skill.git   ~/.claude/skills/darwin-skill
git clone https://github.com/alchaincyf/nuwa-skill.git     ~/.claude/skills/nuwa-skill
git clone https://github.com/alchaincyf/steve-jobs-skill.git ~/.claude/skills/steve-jobs-skill

# + ~ 13 个 superpowers 工程 skill(随 superpowers@superpowers-marketplace 启用而可用,
#   不用单独 clone;本机的 tdd / code-review / research / teach / implement 等都在这里)

# + ~ 12 个 Atom / ask-matt 工程 skill(本机已装,由 setup-matt-pocock-skills 拉取;
#   在新机先 clone superpowers 后按 /setup-matt-pocock-skills 引导安装)
```

> 校验:`~/.claude/skills/` 下应当 ≥ 30 个目录。

### 5.3 装两个 MCP server

编辑 `~/.claude.json`(顶层 `mcpServers` 块),加入:

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

- `codegraph`:需先 `npm i -g codegraph`(或按官方文档装 CLI)
- `codebase-memory-mcp`:先装对应 exe 后把绝对地址写进 `command`

装完重启 Claude Code,会话里出现 `[mcp]` 工具槽即生效。

### 5.4 状态栏脚本(本机自制,复刻必需)

1. 建目录并写脚本 `~/.claude/plugins/cache/cp-statusline/combined-statusline.ps1`(内容见下方)
2. 把 `~/.claude/settings.json` 加节点:

```json
"statusLine": {
  "type": "command",
  "command": "powershell -ExecutionPolicy Bypass -File \"<HOME>\\.claude\\plugins\\cache\\cp-statusline\\combined-statusline.ps1\""
}
```

(把 `<HOME>` 换成实际用户目录;Cygwin/Git Bash 路径写法不同于 Windows 绝对路径,按所用终端调整转义。)

3. 重启 Claude Code → 终端底部多出状态行。

**脚本内容**(`combined-statusline.ps1`,本机成形版本):

```powershell
$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME ".claude" }
function Get-FlagLevel($Name) {
    $p = Join-Path $ClaudeDir $Name
    if (-not (Test-Path $p)) { return $null }
    try { $r = (Get-Content $p -ErrorAction Stop | Select-Object -First 1).Trim(); if ([string]::IsNullOrEmpty($r)) { return $null }; return $r } catch { return $null }
}
$caveman = Get-FlagLevel ".caveman-active"
$pony    = Get-FlagLevel ".ponytail-active"
if ($null -eq $caveman -and $null -eq $pony) { exit 0 }
$Esc = [char]27
function Render($Label,$Level,$Color) {
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

### 5.5 复刻后checklist

- [ ] `~/.claude/settings.json` → 3 个 enabledPlugins 全 true
- [ ] `/plugin list` 显示 caveman + ponytail + superpowers-marketplace 均已装载
- [ ] `~/.claude/skills/` ≥ 30 个目录(cangjie / darwin / nuwa / steve-jobs + superpowers 全套)
- [ ] `~/.claude.json` mcpServers含 codegraph + codebase-memory-mcp → 会话里 `[mcp]` 槽出现
- [ ] 重启后终端底部状态行:双开 `[CAVEMAN & PONYTAIL]` /单色单显
- [ ] 模式验证:`/caveman`、`/ponytail` 各自可切换 lite/full/ultra

---

## 六、状态栏(Statusline)配置

两个 mode 插件(caveman、ponytail)各自写 `~/.claude/.caveman-active` / `~/.claude/.ponytail-active` 标记文件。本机改用**合一脚本**,按两个标记的有无渲染单条状态:

| 状态 | 显示 |
|------|------|
| 双开 | `[CAVEMAN & PONYTAIL]`(amber 173) |
| 仅 caveman | `[CAVEMAN]`(蓝 33) |
| 仅 ponytail | `[PONYTAIL]`(绿 108) |
| 都关 | 静默(无输出) |

脚本路径:`~/.claude/plugins/cache/cp-statusline/combined-statusline.ps1`(非插件自带,本机自制)。

`~/.claude/settings.json` 已配 `statusLine` 指向该脚本(需重启 Claude Code 生效)。

逻辑:读两个标记文件 → 全无 `exit 0` → 双开写 amber `[CAVEMAN & PONYTAIL]` → 单写对应单色标签。

---

## 六、附:skill 个数汇总

| 类别 | 数量 |
|------|------|
| 本地 SKILL.md | 32 个(skill 目录) |
| Plugin(Marketplace) | 3 个全局启用 |
| MCP server | 2 个(stdio) |
| 涉及 GitHub 仓库 | 约 8 个(marketplace/skill 不同源) |

---

*本机实际信息源:*
- *skills 目录:`~/.claude/skills/`* — 32 个
- *市场:JuliusBrussee/caveman、DietrichGebert/ponytail、obra/superpowers-marketplace*
- *settings:~/.claude/settings.json + ~/.claude.json(MCP)*
- *激活模式:`~./caveman-active`, `~./ponytail-active` 标记存在*