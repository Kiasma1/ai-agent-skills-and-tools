# AI Agent Skills 与生态工具清单

> 最后更新：2026-07-28 22:12（中国标准时间）
> 维护者：[@Kiasma1](https://github.com/Kiasma1)

这是我的 Agent 能力索引：记录我拥有的项目、当前可用的 skills，以及支撑它们的工具。按任务取用，而不是追求安装数量。

> **当前原则**：优先使用轻量 skill、合适工具和明确验收标准。~~superpowers~~ 仅保留为历史参考，不再是默认工作流或新机复刻项。

---

## 我的资产

| 项目 | 状态 | 用途 |
|---|---|---|
| [skills](https://github.com/Kiasma1/skills) | 创建 | 本仓库：Agent skills 与工具的索引。<br><strong>大白话：</strong>我的 AI 工具箱目录，想找什么能力先来这里看。 |
| [lzc-explain-words](https://github.com/Kiasma1/lzc-explain-words) | 创建 | 英文词源、语义辨析、词卡与离线 HTML 渲染。<br><strong>大白话：</strong>查一个词不只给翻译，还讲它从哪来、怎么用、和近义词差在哪。 |
| [lxgw-screen-typography](https://github.com/Kiasma1/lxgw-screen-typography) | 创建 | Codex 中文屏幕排版与字体混排。<br><strong>大白话：</strong>让中文网页和软件界面更耐看，不再像默认字体随便堆出来的。 |
| [understand-learn](https://github.com/Kiasma1/understand-learn) | 创建 | 预测—验证式交互代码学习。<br><strong>大白话：</strong>让 AI 像老师一样边问边教，而不是直接把答案甩给你。 |
| [youtube-bilibili-bilingual](https://github.com/Kiasma1/youtube-bilibili-bilingual) | 创建 | YouTube 下载、双语硬字幕与 B 站投稿工作流。<br><strong>大白话：</strong>给它一个 YouTube 视频，尽量一路处理成能发到 B 站的双语成品。 |
| [sansheng-distill](https://github.com/Kiasma1/sansheng-distill) | 维护 / 社区复刻 | 多 Agent 书籍、视频蒸馏与交互式 HTML 输出；原项目作者为叁笙。<br><strong>大白话：</strong>让多个 AI 分工读完长内容，提炼重点并做成方便浏览的知识页面。 |

---

## Skills

仓库内可直接使用的 Skill 位于 [`skills/`](./skills/)；每个子目录都以 `SKILL.md` 作为入口。第三方 Skill 仍通过下方“来源”链接访问，避免重复分发和许可证混淆。

### 自建与维护

| Skill / 项目 | 适用场景 |
|---|---|
| [`lzc-explain-words`](./skills/lzc-explain-words/) | 深入解释英文词汇并生成可阅读、可保存的词卡。<br><strong>大白话：</strong>把普通词典的一行释义，升级成一张真正能把词学明白的卡片。 |
| [`lxgw-screen-typography`](./skills/lxgw-screen-typography/) | 为网页或界面建立舒适、统一的中西文排版。<br><strong>大白话：</strong>帮界面选对字体、字号和间距，让中文阅读更舒服。 |
| [`understand-learn`](./skills/understand-learn/) | 以练习和反馈驱动的方式理解代码库或技术概念。<br><strong>大白话：</strong>AI 不替你做题，而是一步步带你真正学会。 |
| [`youtube-bilibili-bilingual`](./skills/youtube-bilibili-bilingual/) | 将公开视频处理为可发布的 B 站双语内容。<br><strong>大白话：</strong>自动处理下载、字幕、压制和投稿这条流水线。 |
| [`sansheng-distill`](./skills/sansheng-distill/) | 将书籍、视频或播客蒸馏成有来源的可执行知识。<br><strong>大白话：</strong>替你啃长内容，最后交付一份有出处、能复用的精华。 |
| [`leader`](./skills/leader/) | 先实测代码库并补充必要调研，再把一句话想法写成不超过 4000 字符、可直接交给 agent 独立执行的目标任务书，包含边界、验收、防作弊与断点续跑。<br><strong>大白话：</strong>你只管说想做什么，它负责查清情况、问几个关键问题，再写出一份可以直接复制给 AI 开工并用来验收的任务书。 |

### 设计与动效 · Emil Kowalski

来源：[emilkowalski/skills](https://github.com/emilkowalski/skills/tree/main/skills)（Skills for Design Engineers）。

| Skill | 适用场景 |
|---|---|
| `emil-design-eng` | 打磨 UI、组件、动画与产品细节。<br><strong>大白话：</strong>把“能用”的界面继续磨到顺手、精致、有高级感。 |
| `apple-design` | 构建或审查手势、弹簧、拖拽、半透明与空间层次交互。<br><strong>大白话：</strong>让网页的操作手感更像 Apple 产品，自然、有重量、跟手。 |
| `animation-vocabulary` | 将模糊的动效描述对应到准确术语。<br><strong>大白话：</strong>说不出动画叫什么没关系，描述“那个弹一下的效果”，它帮你找到专业名称。 |
| `find-animation-opportunities` | 找出界面中值得动、以及不该动的地方。<br><strong>大白话：</strong>帮你判断哪里加动画会更好用，哪里乱动只会添堵。 |
| `improve-animations` | 审视既有动效并产出优先级改进方案。<br><strong>大白话：</strong>给现有动画做体检，列出先改什么、怎么改。 |
| `review-animations` | 按高标准审查动画与运动代码。<br><strong>大白话：</strong>请一位严格的动效审稿人挑出卡顿、突兀和不自然。 |
| `pick-ui-library` | 为输入、图表、拖拽、状态管理等选择合适的 UI 库。<br><strong>大白话：</strong>告诉你该用哪个现成轮子，避免重复造轮子。 |
| `prototype` | 并列构建多种 UI 方案，供视觉挑选。<br><strong>大白话：</strong>一次做出几个不同版本，直接看效果再选，不靠脑补。 |

### Apple Liquid Glass · ECC

来源：[affaan-m/ECC · liquid-glass-design](https://github.com/affaan-m/ECC/blob/main/docs/zh-CN/skills/liquid-glass-design/SKILL.md)。

| Skill | 适用场景 |
|---|---|
| `liquid-glass-design` | 面向 iOS 26 的 Liquid Glass 设计与实现指南，覆盖 SwiftUI、UIKit 和 WidgetKit 中的玻璃材质、交互变形、容器、性能及可访问性。<br><strong>大白话：</strong>想给 iPhone 应用做苹果新的“液态玻璃”效果时，它会告诉你按钮、卡片、工具栏和小组件该怎么写，既有玻璃感又不会乱用或拖慢界面。 |

### 工程与协作 · Atom

来源：[mattpocock/atom](https://github.com/mattpocock/atom)。同一行表示概念相近、经常连用，或后者是更进一步的版本；不代表必须全部使用。

| 相关 Skills | 说明 |
|---|---|
| `ask-matt` → `implement` | `ask-matt` 先判断该走哪个 skill 或工作流，`implement` 再根据已有 spec / ticket 完成一项小改动。<br><strong>大白话：</strong>不知道用哪个就先问，选好以后再让它动手干活。 |
| `handoff` → `claude-handoff` | `handoff` 把上下文和进度写成交接文档；`claude-handoff` 更进一步，直接把任务交给新的后台 agent。<br><strong>大白话：</strong>前者是写交接班说明，后者是连说明带工作一起转给另一个 AI。 |
| `to-spec` → `to-tickets` | `to-spec` 把讨论整理成目标、范围和验收条件；`to-tickets` 再拆成可独立执行、有先后关系的任务。<br><strong>大白话：</strong>先把“到底要做什么”说清楚，再切成一张张能完成的工单。 |
| `triage` → `wayfinder` | `triage` 适合给单个 issue / PR 分类、核验并确定下一步；`wayfinder` 面向跨多个会话的大工程，绘制任务、依赖和阻塞地图。<br><strong>大白话：</strong>小问题先分诊，大工程先画路线图。 |
| `improve-codebase-architecture` | 扫描代码库中的架构问题和改进机会，输出分析与行动建议。<br><strong>大白话：</strong>给整个代码库做一次体检，告诉你哪里最值得先改。 |
| `setup-matt-pocock-skills` | 初始化 Atom skills 使用的 tracker、标签和领域文档布局。<br><strong>大白话：</strong>首次安装向导，通常只需要运行一次。 |
| `grilling` → `grill-me` → `grill-with-docs` | `grilling` 通用挑刺，`grill-me` 通过连续追问深入压力测试，`grill-with-docs` 还会把结论整理成 ADR、术语表等文档。<br><strong>大白话：</strong>从“帮我找漏洞”，升级到“追问到底”，最后再把结论写成正式文件。 |

### 其他专项

| Skill | 用途 | 来源 |
|---|---|---|
| `cangjie-skill` | 将中文扫描书蒸馏为 skill 或 Markdown Handbook。<br><strong>大白话：</strong>把一本厚书拆解、提炼，变成 AI 能照着执行的知识手册。 | [Kiasma1/cangjie-skill](https://github.com/Kiasma1/cangjie-skill)（fork） |
| `darwin-skill` | 用 SkillLens 与 hill-climbing 优化 `SKILL.md`。<br><strong>大白话：</strong>让 skill 给自己做体检，并一轮轮改得更好用。 | [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) |
| `nuwa-skill` | 从人物或模糊需求生成可运行的视角 skill。<br><strong>大白话：</strong>研究一个人的思考方式，再做成可以调用的“思维分身”。 | [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) |
| `steve-jobs-perspective` | 用乔布斯视角审视产品与设计。<br><strong>大白话：</strong>请一个“乔布斯式产品顾问”帮你砍掉平庸方案、聚焦核心体验。 | [alchaincyf/steve-jobs-skill](https://github.com/alchaincyf/steve-jobs-skill) |
| `dataviz` | 生成一致、易读的图表与数据可视化。<br><strong>大白话：</strong>把枯燥数据画成一眼能看懂、风格统一的图。 | 平台内置 |

---

## 当前工具

| 类型 | 工具 | 作用 |
|---|---|---|
| 插件 | [caveman](https://github.com/JuliusBrussee/caveman) | 高密度、简洁的技术沟通。<br><strong>大白话：</strong>让 AI 少说套话，用更少的字把重点讲清楚。 |
| 插件 | [ponytail](https://github.com/DietrichGebert/ponytail) | YAGNI、库优先与最小 diff 的工程约束。<br><strong>大白话：</strong>提醒 AI 别过度设计，能少写代码就少写，能用成熟库就别重造。 |
| MCP | `codegraph` | 代码语义搜索、调用链与影响分析。<br><strong>大白话：</strong>快速查清一段代码是谁调用的、改了会影响哪里。 |
| MCP | `codebase-memory-mcp` | 本地代码库知识图谱与持久化记忆。<br><strong>大白话：</strong>让 AI 更容易记住整个项目的结构和模块关系。 |

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

| 类别 | Skills | 说明 |
|---|---|---|
| 规划与质量 | `brainstorming`、`writing-plans`、`executing-plans`、`test-driven-development`、`systematic-debugging`、`verification-before-completion` | 从需求、计划、实现到验证的一整套约束。<br><strong>大白话：</strong>先想清楚再写，出错按步骤查，做完必须拿证据证明。 |
| 评审与协作 | `code-review`、`requesting-code-review`、`receiving-code-review`、`dispatching-parallel-agents`、`subagent-driven-development`、`using-git-worktrees`、`finishing-a-development-branch` | 用评审、子代理和 Git 隔离来组织多人或多任务开发。<br><strong>大白话：</strong>把活分开干、互相检查，最后再安全地合到一起。 |
| 编程实践 | `coding-discipline`、`diagnosing-bugs`、`domain-modeling`、`prototype`、`research`、`teach`、`writing-great-skills`、`codebase-design` | 覆盖编码纪律、诊断、建模、原型、研究和教学。<br><strong>大白话：</strong>一组开发方法工具箱，遇到不同问题就拿对应的方法出来用。 |

其中的单项方法可以按需借鉴，但不再通过整套框架强制执行。

</details>

---

## 使用与维护

- 安装或配置以各项目自身 README 为准；不再维护“一键装齐”的长命令清单。
- 先从“我的资产”和 Emil 的设计工程 skills 中选，再按需添加外部能力。
- 自有资产以 [Kiasma1 的公开仓库](https://github.com/Kiasma1?tab=repositories) 为准；私有项目不在此列。
