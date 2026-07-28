# AI Agent Skills 与生态工具清单

> 最后更新：2026-07-28 12:55（中国标准时间）
> 维护者：[@Kiasma1](https://github.com/Kiasma1)

这是我的 Agent 能力索引：记录我拥有的项目、当前可用的 skills，以及支撑它们的工具。按任务取用，而不是追求安装数量。

> **当前原则**：优先使用轻量 skill、合适工具和明确验收标准。~~superpowers~~ 仅保留为历史参考，不再是默认工作流或新机复刻项。

---

## 我的资产

| 项目 | 状态 | 用途 |
|---|---|---|
| [ai-agent-skills-and-tools](https://github.com/Kiasma1/ai-agent-skills-and-tools) | 创建 | 本仓库：Agent skills 与工具的索引。 |
| [lzc-explain-words](https://github.com/Kiasma1/lzc-explain-words) | 创建 | 英文词源、语义辨析、词卡与离线 HTML 渲染。 |
| [lxgw-screen-typography](https://github.com/Kiasma1/lxgw-screen-typography) | 创建 | Codex 中文屏幕排版与字体混排。 |
| [understand-learn](https://github.com/Kiasma1/understand-learn) | 创建 | 预测—验证式交互代码学习。 |
| [youtube-bilibili-bilingual](https://github.com/Kiasma1/youtube-bilibili-bilingual) | 创建 | YouTube 下载、双语硬字幕与 B 站投稿工作流。 |
| [sansheng-distill](https://github.com/Kiasma1/sansheng-distill) | 维护 / 社区复刻 | 多 Agent 书籍、视频蒸馏与交互式 HTML 输出；原项目作者为叁笙。 |

---

## Skills

### 自建与维护

| Skill / 项目 | 适用场景 |
|---|---|
| `lzc-explain-words` | 深入解释英文词汇并生成可阅读、可保存的词卡。 |
| `lxgw-screen-typography` | 为网页或界面建立舒适、统一的中西文排版。 |
| `understand-learn` | 以练习和反馈驱动的方式理解代码库或技术概念。 |
| `youtube-bilibili-bilingual` | 将公开视频处理为可发布的 B 站双语内容。 |
| `sansheng-distill` | 将书籍、视频或播客蒸馏成有来源的可执行知识。 |

### 设计与动效 · Emil Kowalski

来源：[emilkowalski/skills](https://github.com/emilkowalski/skills/tree/main/skills)（Skills for Design Engineers）。

| Skill | 适用场景 |
|---|---|
| `emil-design-eng` | 打磨 UI、组件、动画与产品细节。 |
| `apple-design` | 构建或审查手势、弹簧、拖拽、半透明与空间层次交互。 |
| `animation-vocabulary` | 将模糊的动效描述对应到准确术语。 |
| `find-animation-opportunities` | 找出界面中值得动、以及不该动的地方。 |
| `improve-animations` | 审视既有动效并产出优先级改进方案。 |
| `review-animations` | 按高标准审查动画与运动代码。 |
| `pick-ui-library` | 为输入、图表、拖拽、状态管理等选择合适的 UI 库。 |
| `prototype` | 并列构建多种 UI 方案，供视觉挑选。 |

### 工程与协作 · Atom

来源：[mattpocock/atom](https://github.com/mattpocock/atom)。只在任务需要时调用相应 skill。

| Skill | 用途 |
|---|---|
| `ask-matt` | 根据任务描述，建议应使用哪个 skill 或工作流。 |
| `implement` | 基于已有 spec 或 ticket，实现一个小范围、可验证的改动。 |
| `handoff` | 将当前对话和进度整理成可由另一位 agent 继续执行的交接文档。 |
| `claude-handoff` | 将当前任务交接给新的后台 agent，保留必要的上下文与下一步。 |
| `to-spec` | 把讨论沉淀为结构化规格，明确目标、范围和验收条件。 |
| `to-tickets` | 将计划或规格拆成有依赖关系、可独立执行的 tickets。 |
| `triage` | 分类并核验 issue 或外部 PR，形成可执行的处理 brief。 |
| `wayfinder` | 为跨多个会话的大型工作建立调查地图、拆解路线与阻塞关系。 |
| `improve-codebase-architecture` | 扫描代码库的架构改进机会，产出分析报告和下一步建议。 |
| `setup-matt-pocock-skills` | 一次性初始化 Atom skills 所需的 tracker、标签与领域文档布局。 |
| `grill-me` | 以访谈式追问压力测试一个设计、计划或决策。 |
| `grill-with-docs` | 在压力测试的同时产出 ADR 和术语表等配套文档。 |
| `grilling` | 对任意计划或方案进行通用的反问与风险检验。 |

### 其他专项

| Skill | 用途 | 来源 |
|---|---|---|
| `cangjie-skill` | 将中文扫描书蒸馏为 skill 或 Markdown Handbook。 | [Kiasma1/cangjie-skill](https://github.com/Kiasma1/cangjie-skill)（fork） |
| `darwin-skill` | 用 SkillLens 与 hill-climbing 优化 `SKILL.md`。 | [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) |
| `nuwa-skill` | 从人物或模糊需求生成可运行的视角 skill。 | [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) |
| `steve-jobs-perspective` | 用乔布斯视角审视产品与设计。 | [alchaincyf/steve-jobs-skill](https://github.com/alchaincyf/steve-jobs-skill) |
| `dataviz` | 生成一致、易读的图表与数据可视化。 | 平台内置 |

---

## 当前工具

| 类型 | 工具 | 作用 |
|---|---|---|
| 插件 | [caveman](https://github.com/JuliusBrussee/caveman) | 高密度、简洁的技术沟通。 |
| 插件 | [ponytail](https://github.com/DietrichGebert/ponytail) | YAGNI、库优先与最小 diff 的工程约束。 |
| MCP | `codegraph` | 代码语义搜索、调用链与影响分析。 |
| MCP | `codebase-memory-mcp` | 本地代码库知识图谱与持久化记忆。 |

使用路径：`任务 → 选择一项 skill 或工具 → 执行 → 按验收标准验证`。

---

## 为什么不再推荐 ~~superpowers~~

这不是否定其中的工程原则，而是改变默认使用方式：从“先装一套固定流程”改为“按问题取用一项能力”。

- **流程成本高于默认收益**：对多数小改动、排查和问答，强制经历规划、子代理、评审等固定阶段会增加往返、上下文与维护成本。
- **与现代 LLM 能力重叠**：规划、代码理解、工具调用、调试与自检已是当前模型的基础能力；将它们再包装成通用强制流程，往往只会增加提示词和操作层级。
- **专用 skill 更精确**：设计、排版、动画、词汇学习、视频处理等任务有明确领域语义。单项 skill 的触发条件、输出和验收标准更清晰，也更容易替换和维护。
- **验证应由结果驱动**：测试、构建、lint、视觉检查和用户验收是可观察证据；比“执行过某个流程”更可靠。

仍可借鉴其 TDD、系统化调试、代码审查和完成前验证等原则；当任务复杂或风险高时，手动选择这些做法即可，无需启用整套框架。

---

## 历史归档

<details>
<summary>~~superpowers~~（仅供溯源，不推荐安装）</summary>

来源：[obra/superpowers](https://github.com/obra/superpowers)。曾使用的 skills：

| 类别 | Skills |
|---|---|
| 规划与质量 | `brainstorming`、`writing-plans`、`executing-plans`、`test-driven-development`、`systematic-debugging`、`verification-before-completion` |
| 评审与协作 | `code-review`、`requesting-code-review`、`receiving-code-review`、`dispatching-parallel-agents`、`subagent-driven-development`、`using-git-worktrees`、`finishing-a-development-branch` |
| 编程实践 | `coding-discipline`、`diagnosing-bugs`、`domain-modeling`、`prototype`、`research`、`teach`、`writing-great-skills`、`codebase-design` |

其中的单项方法可以按需借鉴，但不再通过整套框架强制执行。

</details>

---

## 使用与维护

- 安装或配置以各项目自身 README 为准；不再维护“一键装齐”的长命令清单。
- 先从“我的资产”和 Emil 的设计工程 skills 中选，再按需添加外部能力。
- 自有资产以 [Kiasma1 的公开仓库](https://github.com/Kiasma1?tab=repositories) 为准；私有项目不在此列。
