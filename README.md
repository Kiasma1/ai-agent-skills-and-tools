# AI Agent Skills 与生态工具清单

> 最后更新：2026-07-28（中国标准时间）
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

| 场景 | Skills |
|---|---|
| 路由与实现 | `ask-matt`、`implement` |
| 交接与规格 | `handoff`、`claude-handoff`、`to-spec`、`to-tickets` |
| 分析与规划 | `triage`、`wayfinder`、`improve-codebase-architecture` |
| 决策压力测试 | `grill-me`、`grill-with-docs`、`grilling` |

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
