# AI Agent Skills 与生态工具清单

> 最后更新: 2026-07-06 中国标准时间
> wsqzlzc

本清单按 **来源仓库** 分组,方便溯源与更新。覆盖 Claude Code / Codex / OpenClaw / Cursor / Gemini CLI / Hermes 等多端共用的 skills,及与这些 agent 深度配合的外部生态工具(MCP 服务、CLI、桌面 App)。

---

## 一、来自 superpowers-zh (jnMetaCode)

> 源仓库: https://github.com/jnMetaCode/superpowers-zh
> License: MIT(源自 obra/superpowers)
> 数量: **14 个翻译 skill + 6 个中文原创 skill = 20 个**
> 安装: `npx superpowers-zh` 或 `cp -r`

| # | Skill 名 | 用途 |
|---|---------|------|
| 1 | `brainstorming` | 需求分析 → 设计规格,写代码前先想清楚 |
| 2 | `writing-plans` | 把规格拆成可执行的实现步骤,落到 `docs/superpowers/plans/` |
| 3 | `executing-plans` | 逐步执行计划,每步校验后推进;子代理可用时优先走 subagent-driven |
| 4 | `test-driven-development` | 严格 TDD 红绿重构循环,一个垂直切片一个切片做 |
| 5 | `systematic-debugging` | 定位→分析→假设→修复四阶段,防 AI 瞎猜 |
| 6 | `requesting-code-review` | 派出 review 代理按"标准 + 规格"两轴审 diff |
| 7 | `receiving-code-review` | 收到 review 反馈后技术严谨地处理,拒绝敷衍 |
| 8 | `verification-before-completion` | 声称完成前必须跑验证命令,证据先行 |
| 9 | `dispatching-parallel-agents` | 2 个以上无依赖任务并行跑 |
| 10 | `subagent-driven-development` | 一个任务一个子 agent,两轮 review,隔关注点 |
| 11 | `using-git-worktrees` | 用 git worktree 隔离功能开发,防分支污染 |
| 12 | `finishing-a-development-branch` | 收尾期 merge/PR/keep/discard 决策树 |
| 13 | `writing-skills` | 创建新 skill 的方法论,让 skill 可复现 |
| 14 | `using-superpowers` | 元技能:何时该调哪个 skill 的优先级矩阵 |
| 15 | `chinese-code-review` `/chinese-code-review` | 中文 review 话术 + 必须修复/建议修改/仅供参考三档 |
| 16 | `chinese-commit-conventions` `/chinese-commit-conventions` | Conventional Commits 中文适配 + husky/commitizen 模板 |
| 17 | `chinese-documentation` `/chinese-documentation` | 中文排版指北:中英空格、全半角标点、术语保留 |
| 18 | `chinese-git-workflow` `/chinese-git-workflow` | Gitee/Coding/极狐 GitLab/CNB 的 SSH/凭据/CI 接入差异 |
| 19 | `mcp-builder` | 生产级 MCP 工具构建方法论,扩展 AI 能力边界 |
| 20 | `workflow-runner` | 在 Claude Code / OpenClaw / Cursor 内直接跑 YAML 多角色工作流 |

---

## 二、来自 mattpocock/skills (Matt Pocock)

> 源仓库: https://github.com/mattpocock/skills
> License: MIT
> 数量: **16 个**(部分与 superpowers 重叠,此处仅列独家)
> 安装: `npx skills add mattpocock/skills` → `/setup-matt-pocock-skills`

| # | Skill 名 | 调用类型 | 用途 |
|---|---------|---------|------|
| 1 | `ask-matt` | 用户主动 | Router:诊断当前场景该用哪个 flow |
| 2 | `grill-with-docs` | 用户主动 | 压力测试方案 + 同步建域模型/术语表/ADR |
| 3 | `triage` | 用户主动 | Issue/PR 状态机分流:分类→核实→grill→写 agent-ready brief |
| 4 | `improve-codebase-architecture` | 用户主动 | 扫代码库找 deepening 机会,出 HTML 可视化报告 |
| 5 | `setup-matt-pocock-skills` | 一次性 | 配置 issue tracker/triage 标签/doc 布局,每 repo 跑一次 |
| 6 | `to-issues` | 用户主动 | 把 plan/PRD 切成可独立领取的 issue(垂直切片) |
| 7 | `to-prd` | 用户主动 | 从当前会话直接合成 PRD 发到 issue tracker |
| 8 | `prototype` | 模型触发 | 做一次性原型验证 design 问题 |
| 9 | `domain-modeling` | 模型触发 | 术语对照 + 边界压力测试 + 更新 CONTEXT.md/ADR |
| 10 | `codebase-design` | 模型触发 | Deep module 词汇表:大行为、小接口、干净 seam、可测试 |
| 11 | `code-review` | 模型触发 | Standards × Spec 两轴审 diff,并行子 agent |
| 12 | `grill-me` | 用户主动 | 非代码场景的压力测试访谈 |
| 13 | `handoff` | 用户主动 | 把当前会话压缩成跨 agent 交接文档 |
| 14 | `teach` | 用户主动 | 在多会话内教一个新概念/新 skill |
| 15 | `writing-great-skills` | 参考 | skill 写法参考 — 词汇与原则 |
| 16 | `grilling` | 模型触发 | grill-me / grill-with-docs 的底层可复用访谈循环 |

---

## 三、来自其他源

### 3.1 拆书产出 — 《系统之美》by Donella Meadows (经 cangjie-skill 蒸馏)

> 这些 skill 的 `source_book` 字段都指向同一本书,由 `cangjie-skill` 蒸馏生成。

| Skill | 核心用途 |
|-------|---------|
| `feedback-loop-id` | 识别反馈回路,分调节(趋稳)与增强(指数/崩溃) |
| `stock-flow-thinking` | 拆存量 vs 流量,增流入 vs 减流出 |
| `leverage-points-12` | 梅多斯 12 杠杆点定位 |
| `system-traps-8` | 梅多斯 8 大系统陷阱,反馈结构 + 结构性对策 |

### 3.2 角色扮演 / 人物 skill (nuwa-skill 产出)

| Skill | 素材来源 |
|-------|---------|
| `nuwa-skill` (女娲) | 通用人物 skill 制造器 — 输入人名/主题,自动调研→生成 |
| `cangjie-skill` | 蒸馏一本书的框架为一套 atomic skill(上述系统之美系列由此生) |
| `steve-jobs-skill` | Isaacson 授权传记 + Stanford 演讲 + Lost Interview 等 30+ 一手来源 |

### 3.3 独立工具 / 方法论

| Skill | 源 / 用途 |
|-------|----------|
| `darwin-skill` | https://github.com/alchaincyf/darwin-skill — 9 维 SkillLens + SkillOpt 自动优化器,hill-climbing + git 版本控制 |
| `coding-discipline` | Karpathy 行为准则 + 终极 token 优化(diff-only,不废话) |
| `video-downloader` | 支持抖音/B站/YouTube/小红书/微信视频号的视频、字幕、音频、元数据一键归档 |

---

## 四、Agent 生态工具(MCP / 桌面 / 独立 CLI)

这些不是 skills,但跟 Claude Code / Codex / OpenClaw / Cursor / Gemini CLI 等 agent 深度绑定,增强或扩展其工作流。

| 工具 | 源 | 定位 | 关键能力 |
|------|----|------|---------|
| **agent-reach** | https://github.com/Panniantong/agent-reach | 全网平台接入层(统一入口) | 一键装 mcporter/Exa/yt-dlp 核心 + 15 个平台渠道(Twitter/Reddit/Facebook/Instagram/小红书/B站/小宇宙/雪球/LinkedIn/V2EX/RSS/GitHub/YouTube/全网搜索/任意网页);多后端路由(OpenCLI 浏览器会话 / 平台 CLI / 公开 API);`agent-reach doctor` 查渠道状态;`--channels=all` 一键拉满;Skill 同时装在 `~/.claude/skills/` 和 `~/.agents/skills/`;v1.5.0 已装;MIT(请独立审阅上游工具各自的 license) |
| **cc-switch** | https://github.com/farion1231/cc-switch | AI coding 全能助手(Tauri 2,跨平台) | 7 种 coding agent(Claude Code/Codex/Gemini CLI/OpenCode/OpenClaw/Hermes 等)的 API 提供商统一管理;一键切换 + 50+ 预设;本地代理热切 + 自动 failover;Dropbox/OneDrive/iCloud/WebDAV 云同步;MCP server/Skill 双向同步;113k stars;MIT |
| **headroom** | https://github.com/headroomlabs-ai/headroom | AI Agent 上下文压缩层 | 工具输出/RAG/日志在送达 LLM 前压 60-95% token;Kompress-v2-base 自定义模型;CCR 可逆压缩;跨 agent 共享记忆;`headroom wrap <agent>` 即装即用;Apache 2.0 |
| **last30days-skill** | https://github.com/mvanhorn/last30days-skill | 最近 30 天舆情研究引擎 | Reddit/X/YouTube(全字幕)/TikTok/Instagram/HN/Polymarket/GitHub 并行检索;人/公司/产品竞对 vs 对比;招聘信号;可分享 HTML report;v3.8.3 已装;48.7k stars;MIT |
| **codebase-memory-mcp** | https://github.com/DeusData/codebase-memory-mcp | 代码知识图谱索引(MCP 服务) | 158 种 tree-sitter + Hybrid LSP;Cypher-like 查询;14 MCP 工具;SQLite WAL 持久化;单静态二进制零依赖;团队共享 zstd graph artifact;v0.8.1 已装;~25.3k stars;MIT |

---

## 五、汇总

| 类别 | 数量 | 位置 |
|------|------|------|
| superpowers-zh skills | 20 | `~/.claude/skills/` |
| mattpocock/skills (独家) | 16 | `~/.claude/skills/` |
| 其他(拆书、角色扮演、独立) | ~12 | `~/.claude/skills/` |
| **已安装 skills 合计** | **48** | `~/.claude/skills/` |
| 已安装 Claude Code 插件 | 1 | `last30days@3.8.3` |
| 已注册 Marketplace | 2 | last30days-skill, karpathy-skills |
| 会话内置 skills | 44 | Claude Code 启动自动加载 |
| 生态工具(MCP / CLI) | 5 | agent-reach / cc-switch / headroom / last30days / codebase-memory-mcp |
| agent-reach 已激活渠道 | 6 | GitHub / YouTube / V2EX / RSS/Atom / 任意网页 / B站(基础) |
| agent-reach 待配置渠道 | 9 | Twitter / Reddit / Facebook / Instagram / 小红书 / 小宇宙 / 雪球 / LinkedIn / 全网搜索(Exa 配置路径偏差,见备注) |

---

## 备注

- 拆书系列(§3.1)的"源"是原书,cangjie-skill 做的是蒸馏,归在独立来源是因为它无法追溯回一个上游 skill 仓库。
- **agent-reach(§4) 安装偏差说明**:文档写配置目录 `~/.agent-reach/`,但本仓实际 Python venv 建在 `~/.agent-reach-venv/`,mcporter 配置被写到 `<repository_root>/config/mcporter.json`(mcporter 默认读 cwd)。两个路径 Agent Reach 都能识别,但跨目录跑命令时建议 `export MCPORTER_CONFIG=<仓库>/config/mcporter.json` 显式指定。
- agent-reach 装好后,本仓 `~/.claude/skills/agent-reach/` 和 `~/.agents/skills/agent-reach/` 自动出现,下次 Claude Code / 任意 agent 会话即自动加载。
