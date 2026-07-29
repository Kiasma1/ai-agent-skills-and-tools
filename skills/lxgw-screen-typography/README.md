# LXGW Screen Typography Skill

一个面向 Codex 的语义化混排 Skill，固定使用以下字体角色：

| 内容角色 | 字体 |
| --- | --- |
| 中文正文 | 霞鹜新致宋 屏幕阅读版 |
| 中文界面 | 霞鹜新晰黑 屏幕阅读版 |
| 英文、拉丁词根与 ASCII 数字 | LXGW Bright |

本仓库只提供 Codex Skill、排版规则和 CSS 配置模板，**不包含字体文件、字形轮廓或由字体提取的数据**。

## 为什么不合并字体

霞鹜新晰黑／新致宋屏幕阅读版采用 IPA Font License 1.0；LXGW Bright 采用 SIL Open Font License 1.1。屏幕阅读版上游项目明确说明，这两种许可不兼容。

本项目因此不生成或分发合并后的 TTF/OTF，而是：

- 在网页中通过 `@font-face` 与 `unicode-range` 组成虚拟字体族；
- 在文档、演示稿和设计工具中按文字区段指定字体；
- 在系统字体方案中优先使用平台提供的字体角色映射。

这种方式让字体文件保持独立，也不会尝试改变任何上游字体的许可。

## 安装

将仓库克隆到 Codex 的个人 Skill 目录：

```powershell
git clone https://github.com/Kiasma1/lxgw-screen-typography.git "$env:USERPROFILE\.codex\skills\lxgw-screen-typography"
```

重新打开 Codex 任务后，使用：

```text
$lxgw-screen-typography
```

例如：

```text
使用 $lxgw-screen-typography 为这个中文知识库页面配置正文、界面及英文数字字体。
```

## 字体准备

请分别从上游项目获取字体，并遵守各自随附的许可：

- [霞鹜新晰黑＆霞鹜新致宋 屏幕阅读版](https://github.com/lxgw/LxgwNeoXiZhi-Screen)
- [LXGW Bright](https://github.com/lxgw/LxgwBright)

Skill 不会静默下载、复制或重新打包这些字体。网页模板默认同时尝试本机字体名称和 `./fonts/` 下的示例路径；实际使用时请根据项目调整 URL，并在获准分发字体时同时保留相应许可文件。

## 网页模板

复制 [`assets/lxgw-screen-typography.css`](assets/lxgw-screen-typography.css) 到项目中。模板提供：

- `--font-reading`：中文正文虚拟字体族；
- `--font-interface`：中文界面虚拟字体族；
- `--font-latin`：英文、词根和数字；
- `.reading`、`.prose`、`.interface`、`.latin`、`.number` 等辅助类。

中文通用标点默认跟随中文字体；英文排版标点可将完整英文区段标记为 `lang="en"` 或 `.latin`。

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── lxgw-screen-typography.css
└── references/
    └── licensing-and-platforms.md
```

## 许可与声明

本仓库自行编写的 Skill 文档与 CSS 模板采用 [MIT License](LICENSE)。

字体名称仅用于说明兼容与配置关系。本项目与霞鹜字体作者、IPA、Ysabeau 或其他上游项目没有隶属或背书关系。本仓库的 MIT License 不适用于任何字体文件，也不会替代上游字体的 IPA Font License、SIL OFL 或其他许可。

本项目提供的是保守的技术实现建议，不构成法律意见。准备嵌入、修改或分发字体前，请自行核对上游最新许可。
