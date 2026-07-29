# Agent 兼容与能力降级

## 适用范围

本 Skill 的唯一事实源是当前目录中的 `SKILL.md`、`references/`、`scripts/` 和 `templates/`。Claude Code、Codex Desktop 与 Grok 必须执行同一条 Step0-Step7 管线,不得维护三份分叉提示词。

## 运行时约定

1. 将当前 `SKILL.md` 所在目录解析为 `$SKILL`;不要写死 `~/.claude`、`~/.codex` 或 `~/.grok`。
2. 将 `DISTILL_DATA_DIR` 解析为 `$DATA`;未设置时使用当前任务目录下的 `distill-data`。
3. 使用当前 Agent 已提供的文件、Shell、网页搜索、浏览器和任务委派能力;不要按供应商名称猜工具。
4. 不强制具体模型名。需要高质量长文推理时使用当前 Agent 可用的高推理能力档。

## 一等支持

| Agent | 发现方式 | 并行方式 | 网页增补 |
|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` + 插件 `skills/` | Agent/Task 能力可用时 fan-out | 已配置的搜索 MCP、WebSearch 或浏览器 |
| Codex Desktop | `.codex-plugin/plugin.json` 指向 `skills/`;接口清单另见 `skills/sansheng-distill/agents/openai.yaml` | 多 Agent 工具可用时 fan-out | 连接器/MCP、内置网页搜索或浏览器 |
| Grok | 原生读取 Claude Code 插件,也可从 `.grok/plugins/` 或 `--plugin-dir` 加载(仓内无独立 Grok 清单,依赖其 Claude Code 插件兼容) | Grok 任务委派可用时 fan-out | Grok 搜索/浏览工具或已配置 MCP |

## 必需能力与可选能力

- 必需:读写本地文件、运行 Python、读取完整原文。
- 可选:网页搜索、浏览器、子 Agent、视频理解工具、第三方搜索 MCP。
- 缺网页搜索:将 `enrich.json` 对应联网块置 `null`,继续完成主体。
- 缺子 Agent:按同样分组在主 Agent 中串行执行,不得跳章或降低质量门禁。
- 缺浏览器/Playwright:先完成静态校验,明确报告渲染冒烟未完成;不得声称 Step7 已通过。
- 缺视频理解工具:仅处理已有字幕/转写稿;需要画面语义时停下请求可用转写或工具。

## 搜索能力选择

按以下顺序选择首个可用能力,不要反复重试同一失败提供器:

1. 适合目标站点或语种的专用搜索连接器/MCP。
2. 当前 Agent 的内置网页搜索。
3. 浏览器直接访问权威页面。
4. 全部不可用时按 `enrich.md` 整块降级。

任何外部事实都必须保留可点击 URL。搜索工具名称只属于运行环境,不得写入产物契约。
