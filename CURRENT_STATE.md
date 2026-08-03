# 当前 Codex 状态快照

> 采集时间：2026-08-04 00:05（中国标准时间）
>
> 此文件只记录可公开的名称、版本和启用状态。用户目录统一写成 `~`，不保存令牌、Cookie 或环境变量值。

## 摘要

| 项目 | 当前状态 |
|---|---|
| Codex CLI | `0.144.2` |
| Codex 用户 skills | 21 个，位于 `~/.codex/skills/` |
| 共享 Agent skills | 94 个，位于 `~/.agents/skills/` |
| Codex 系统 skills | 5 个，位于 `~/.codex/skills/.system/` |
| 直接 skills 去重后 | 101 个 |
| 已启用插件提供的 skills | 19 个（去重） |
| 当前可见 skills 总数 | 120 个（去重） |
| 已安装并启用插件 | 12 个 |
| 已启用 MCP 服务 | 4 个 |

## Skills

<details>
<summary>Codex 用户 skills（21）</summary>

- `animation-vocabulary`
- `apple-design`
- `atomic-html-normalizer`
- `codex-model-routing-team`
- `distill-books`
- `emil-design-eng`
- `find-animation-opportunities`
- `gc-minimal-zine-poster-v0-1`
- `hatch-pet`
- `improve-animations`
- `leader`
- `luban`
- `lxgw-screen-typography`
- `minimal-diff`
- `pick-ui-library`
- `prototype`
- `research`
- `review-animations`
- `translate-book`
- `ui-ux-pro-max`
- `unpack-upxs`

</details>

<details>
<summary>共享 Agent skills（94）</summary>

- `animation-vocabulary`, `apple-design`, `ask-matt`, `atomic-html-normalizer`, `atomic-ooux-tokens`
- `banner-design`, `batch-grill-me`, `brand`, `cangjie-skill`, `check-work`
- `chinese-code-review`, `chinese-commit-conventions`, `chinese-documentation`, `chinese-git-workflow`, `claude-handoff`
- `code-review`, `codebase-design`, `codebase-memory`, `codex-model-routing-team`, `coding-discipline`
- `create-skill`, `darwin-skill`, `design`, `design-an-interface`, `design-system`
- `diagnosing-bugs`, `disk-cleaner`, `disk-cleaner-mcp`, `distill-books`, `domain-modeling`, `edit-article`
- `emil-design-eng`, `find-animation-opportunities`, `git-guardrails-claude-code`, `grill-me`, `grill-with-docs`
- `grilling`, `handoff`, `hatch-pet`, `help`, `huashu-nuwa`
- `imagine`, `implement`, `improve-animations`, `improve-codebase-architecture`, `leader`
- `liquid-glass-design`, `loop-me`, `luban`, `lxgw-screen-typography`, `lzc-explain-words`
- `mcp-builder`, `migrate-to-shoehorn`, `nuwa-skill`, `obsidian-vault`, `ooux-atomic-tokens`
- `pick-ui-library`, `prototype`, `qa`, `request-refactor-plan`, `research`
- `resolving-merge-conflicts`, `review-animations`, `sansheng-distill`, `scaffold-exercises`, `setup-matt-pocock-skills`
- `setup-pre-commit`, `setup-ts-deep-modules`, `slides`, `steve-jobs-perspective`, `steve-jobs-skill`
- `tdd`, `teach`, `to-issues`, `to-prd`, `to-questionnaire`
- `to-spec`, `to-tickets`, `translate-book`, `triage`, `ubiquitous-language`
- `ui-styling`, `ui-ux-pro-max`, `understand-learn`, `unpack-upxs`, `video-downloader`
- `wayfinder`, `wizard`, `workflow-runner`, `writing-beats`, `writing-fragments`
- `writing-great-skills`, `writing-shape`, `youtube-bilibili-bilingual`

</details>

<details>
<summary>Codex 系统 skills（5）</summary>

- `imagegen`
- `openai-docs`
- `plugin-creator`
- `skill-creator`
- `skill-installer`

</details>

### 插件提供的 skills（19 个，去重）

| 来源 | Skills |
|---|---|
| `ponytail@ponytail` | `ponytail`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`, `ponytail-review` |
| `i-have-adhd@i-have-adhd` | `i-have-adhd` |
| `openai-bundled` | `control-in-app-browser`, `control-chrome`, `computer-use`, `sites-building`, `sites-hosting`, `visualize` |
| `openai-primary-runtime` | `documents`, `pdf`, `Presentations`, `Spreadsheets`, `excel-live-control`, `template-creator` |

## 已安装插件

全部插件状态均为 `installed, enabled`。

| Marketplace | 插件 | 版本 |
|---|---|---|
| `openai-primary-runtime` | `documents` | `26.802.11031` |
| `openai-primary-runtime` | `pdf` | `26.802.11031` |
| `openai-primary-runtime` | `spreadsheets` | `26.802.11031` |
| `openai-primary-runtime` | `presentations` | `26.802.11031` |
| `openai-primary-runtime` | `template-creator` | `26.802.11031` |
| `openai-bundled` | `sites` | `0.1.27` |
| `openai-bundled` | `browser` | `26.707.62119` |
| `openai-bundled` | `chrome` | `26.707.62119` |
| `openai-bundled` | `computer-use` | `26.707.62119` |
| `openai-bundled` | `visualize` | `1.0.11` |
| `i-have-adhd` | `i-have-adhd` | `0.1.0` |
| `ponytail` | `ponytail` | `4.8.4` |

## MCP 服务

| 名称 | 状态 | 作用 |
|---|---|---|
| `codebase-memory-mcp` | enabled | 代码库知识图谱与持久化记忆 |
| `codegraph` | enabled | 代码语义搜索、调用链与影响分析 |
| `node_repl` | enabled | Browser / Chrome 控制所需的 JavaScript 运行时 |
| `sites-design-picker` | enabled | Sites 设计方案选择器 |

## Agent 指令状态

- 当前有效指令已保存到 [AGENTS.md](./AGENTS.md)。
- 本仓库没有 `.codegraph/`，因此按规则跳过 CodeGraph 索引。
- `AGENTS.md` 引用了 `@RTK.md`，但采集时在工作区、用户目录及 Codex 配置目录均未找到该文件。
- `codebase-memory-mcp` 优先级规则与 ADHD 输出格式规则均处于有效状态。

## 复查命令

```powershell
codex --version
codex plugin list
codex mcp list
```
