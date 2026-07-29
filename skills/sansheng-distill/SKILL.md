---
name: sansheng-distill
description: >
  书籍/视频系列蒸馏引擎 -- 输入一本书的电子全文(epub/pdf/txt/azw3/mobi),或一组视频
  (YouTube/B站,单视频按 1 集系列处理),产出单文件交互 HTML 蒸馏页(浏览型):
  五板块(全书速览/逐章精读/批判与评价/行动清单/延伸阅读)= 凝练地图 + 详实正文 + 页内二级视图;
  书魂可视化并入①,金句墙并入②,同类书内联板块⑤。
  四源融合方法论(李继刚三轮压缩 + 决策规则 + 心智模型 + 批判段)两遍蒸馏(Pass1 压缩骨架 + Pass2 详实转述)
  + 可交互脑图(点节点跳章节/集数)+ 联网增补两张页内子视图(作者页/观点对照页,全带来源;同类书内联板块⑤)
  + 跨书跨作品知识索引互链(越蒸越富)。
  Triggers on 蒸馏这本书 / 书籍蒸馏 / 拆书 / 拆这本书 / 蒸一本书 / 把这本书做成蒸馏页 / book distill
  / 蒸馏这个系列 / 视频蒸馏 / 蒸馏这个UP主 / 蒸馏这几个视频 / 把这个系列做成蒸馏页。
  批量多本先抽样 1 本验收再并行铺量(6本/批串行)。
  Do not use for: 写文章、做口播视频成片、只要视频字幕/摘要而不做蒸馏、网站页面维护。
---

# sansheng-distill -- 多 Agent 书籍/视频蒸馏引擎(v3 浏览型)

输入一本书的电子全文(或一组视频),跑完 Step0-Step7 管线(Step2 分两遍),产出一个可 `file://` 直开的**单文件交互 HTML 蒸馏页**。

**v3 页型 = 浏览型「凝练地图 + 详实正文 + 页内二级视图」**,五板块按读者逻辑链「全局 → 细节 → 反思 → 循环 → 延伸」:

| Tab | 装什么 |
|---|---|
| ① 全书速览 | 刊头(真封面 + 作者名胶囊链)+ hero(核心问题 + 标语)+ 餐巾纸四件套(公式/公式读法/一句话/因果草图)+ 可点跳脑图 + 核心观点卡(pillar 分组)+ 书魂可视化(给 3 分钟扫读的人) |
| ② 逐章精读 | 概念筹码条 + 章目录(默认收起 + 手风琴多开 + 全部展开逃生门)+ 逐章 800-1500 字详实转述(论点式标题)+ 全书金句墙(给愿读 30 分钟的人) |
| ③ 批判与评价 | 裁决条 + 立论复述(论证链胶囊)+ 内在张力 + 批判四分区 + 正反书评 + 观点对照入口(别急着全信) |
| ④ 行动清单 | 行动路线图(4-5 环因果链)+ 情境决策卡 + 心智模型抽屉 + 第二人称自检问句(纯浏览,无打分) |
| ⑤ 延伸阅读 | 同类书卡 + 阅读路径 + 作者书架 + 跨域命名 + 跨书互链 + 两张页内子视图入口(作者页/观点对照页) |

交互:脑图可点跳章节、②章节目录态默认收起 + 手风琴多开(配「全部展开」逃生门)、书魂可视化(①内)、2 个页内全屏子视图(hash 路由开合)、7 套主题换肤。

**这是入口编排文件。** 先读本文对齐管线,再在每一步按下表**读对应 reference / 跑对应 script**;references 是各步的执行细则,不要凭记忆做。开始前读取 `references/agent-compat.md`,按当前 Agent 解析路径、搜索、浏览器和并行能力;不得假定 Claude 专属目录、工具名或模型名。

## 路径与变量约定(全文只定义一次)

| 占位符 | 展开为 |
|---|---|
| `$SKILL` | 当前 `SKILL.md` 所在目录;运行时解析,不得硬编码某个 Agent 的安装路径 |
| `$DATA` | 书数据根目录,由环境变量 `DISTILL_DATA_DIR` 指定(默认 `./distill-data`) |
| `{slug}` | 书的 ASCII kebab 短名(如 `jinqian-xinlixue`);全站唯一,别撞投资 `NN`/育儿 `pNN` |
| `{书目录}` | 本书数据目录,**纯 `{slug}`**(如 `jinqian-xinlixue`);不含书名,避免中文目录名、git/Windows 友好 |

命令里的占位符替成实值再执行。单书目录首次运行 Step0 时自动建。

## 数据目录约定(单书产物布局)

```
$DATA\
  knowledge-index.json          # 跨书概念索引(全库共享,Step4 维护,自动 .bak)
  {书目录}\
    book.txt                    # 全文(书=Step0-B;视频=Step0-V 组装的转写语料)  -- gitignore
    _converted.epub             # 仅 azw3/mobi:convert_book 转出的中间 epub      -- gitignore
    diagnose.json               # 入书诊断(书=Step0-B;视频=Step0-V 的 video_series 变体)
    raw\                        # 仅视频:各集原始转写 srt/txt(Step0-V)             -- gitignore
    series-input.json           # 仅视频:手写 manifest(Step0-V 输入)
    series.json                 # 仅视频:规范化 manifest(Step0-V 产物,下游只读它)
    comments.json               # 仅视频:观众评论(Step0-V,供 Step3 enrich.reviews)
    distill.json                # 蒸馏主对象(Step2 两遍产:Pass1 骨架 + Pass2 narrative/excerpts)
    _pass2_g*.json              # Pass2 分块中间态(长书按章 fan-out 各组产物,合并回 distill) -- gitignore
    enrich.json                 # 联网增补(Step3:author_page/similar_page/views_page + reviews + cross_book_external,带来源 URL,可整块降级)
    index-merge.json            # 5-tag 合并清单(Step4 中间产物)
    {slug}.html                 # 单文件交互蒸馏页(Step6 产物,最终交付,≤3MB;真封面 base64 内联,无独立 cover 文件)
    _verify.png                 # Step7 验证全页截图                                  -- gitignore
```

> gitignore(建议在数据目录加 `.gitignore`):`book.txt` / `_converted.epub` / `raw/` / `_verify.png` / `_pass2_*.json` / `*.bak` 不入库(版权原文 / 临时产物);其余(distill / enrich / HTML / index-merge / series / comments / diagnose)可入库。

---

## 管线表(Step0-Step7,Step2 分两遍)

每一步:**做什么 / 读哪个 reference / 跑哪条命令 / 产物 / 失败降级**。逐步照做,上一步产物是下一步输入。

| 步 | 做什么 | 读哪个 reference | 跑哪条命令 | 产物 | 失败降级 |
|---|---|---|---|---|---|
| **Step0-B** 入书诊断 + 转 txt(蒸**书**走此行) | 电子书 → 全文 txt + 诊断(格式/可提取/扫描版/乱码率/目录识别) | 脚本自足;分流规则见 `method.md §0` | `python $SKILL\scripts\convert_book.py "<书文件>" --outdir "$DATA\{书目录}"`(重转加 `--force`) | `book.txt` / `diagnose.json` | exit 2 = 缺依赖/格式不支持/拒覆盖 → 装 calibre(azw3·mobi)或补 pip 依赖或加 `--force`;**exit 3 = 需OCR / 需人工确认 → 停下问用户(见硬门禁①),不硬读、不编内容** |
| **Step0-V** 视频系列入库(蒸**视频**走此行) | 每个视频取材转写 → 手写 manifest → 组装语料 + 抓评论。章节=集数 | **`method.md §V.0`(取材 cascade,固定流程,先读)** + `§V`。分流:YouTube 优先抓字幕(**认准人工字幕**,可用 `video-to-subtitle-summary` 或 `yt-dlp`)/ 无字幕或需画面语义 → 当前 Agent 可用的 Gemini 视频分析工具/ 非 YouTube 先下载再解析 | ① 按 §V.0 取每视频**干净转写**(YouTube 人工字幕 `subtitle.{lang}.vtt` 可直喂 build_series;⚠️ 别用滚动重复 3× 的 `text.txt`/自动字幕),存 `$DATA\{书目录}\raw\{NN}_{id}\`;② 手写 `series-input.json`(`transcript` 指向选定的**干净**字幕文件);③ `python $SKILL\scripts\build_series.py --manifest "<series-input.json>" --outdir "$DATA\{书目录}"`;④ `python $SKILL\scripts\fetch_comments.py --series "$DATA\{书目录}\series.json" --out "$DATA\{书目录}\comments.json"`;⑤ 逐条 `yt-dlp --skip-download --print` 抓热度元数据(播放/赞/评论数/日期,供热度条;`--flat-playlist` 拿不到须逐条 full extract) | `book.txt` / `series.json` / `diagnose.json` / `comments.json` | build exit 3 = **全部视频缺转写** → 停下问用户(见硬门禁①);**乱码率>2% 不触发 exit 3**,仅置 `diagnose.recommendation=需人工确认` -- 同样停下问用户(补转写/换视频),不拿可疑语料硬蒸;fetch exit 2 = 全失败或抖音不支持 → 评论整块降级(enrich.reviews 置 null),不阻塞蒸馏 |
| **Step1** 书型判定 | 读诊断 + 全书抽样(首/中/末章),判 论说/叙事/人物/工具 型,定加重字段与硬门槛 | `method.md §1` | 无(读 `diagnose.json` + `book.txt` 抽样) | `book_type`(写入 distill.json) | 边界模糊按 §1.2 顺序裁决,命中即停;传记重思维 → 人物(不判叙事) |
| **Step2·Pass1** 压缩骨架(凝练地图) | 三轮认知压缩 + 四嫁接件(决策规则/心智模型/内在张力/批判段)+ v2 延展字段(生活类比/主次/金句点评/概念误读/书魂/因果链/自检)+ 逐条补锚点与证据等级 | `method.md §2-§5`(§3 三轮 + §4 四嫁接件 + **§4.5 延展字段** + §5 锚点) | 无(内化方法蒸馏,产出 JSON) | `distill.json` 骨架层(**除 `chapters[].narrative`/`.excerpts` 外全部字段**) | diagnose=分组蒸馏 → 走 `method.md §8` 分组再合成(禁一次性硬吞);产出后过 §7 门禁 G1-G21(+G4 扩展)自查(见硬门禁②) |
| **Step2·Pass2** 详实转述(详实正文) | 逐章两级检索(先读 Pass1 骨架保结构,再回 book.txt 该章原文 grep 案例/数字/原话保血肉)→ 讲书稿式 narrative(坡道开场 → 观点+完整案例故事+数据 → 一句接主线)+ 挑 excerpts。**长书按章 fan-out 并行**(每组≤5 章;当前 Agent 支持任务委派时派高推理能力 worker,否则主 Agent 组间串行;组内始终串行,最后统一合并) | `method.md §3.5`(两级检索 / 讲书稿模板 / 版权线 / fan-out) | 无(内化;长书分组各产 `_pass2_g*.json` 中间态,主控回填 distill.json) | 回填 `distill.json` 的 `chapters[].narrative`(书 800-1500 字/章·视频段 ≥400)+ `chapters[].excerpts`(书每章 ≥1,原文 ≤150 字) | grep 不到支撑就降级不写该点,**禁凭印象编案例/编数字**;主控做 G9 字数 / G14 excerpts 机械核对 + **标志性案例保全抽检**(招牌故事必须整段完整出现,不得压成标签) |
| **Step3** 联网增补(两页内子视图 + 内联) | 三个增补块各起一轮专门搜索:作者页 / 同类书(内容内联板块⑤,不再做独立子视图)/ 观点对照页(国内外赞同方/质疑方);另产内联 `reviews`(书评正反)+ `cross_book_external`(跨书外部立场),全带来源 URL。**视频系列:`reviews`/`views_page` 数据源含 Step0-V 的 `comments.json`,`author_page` 改频道页,详见 `enrich.md §V`** | `enrich.md`(§3 三块搜索 pass;§4 豆瓣反爬;视频看 §V) | 使用当前 Agent 可用的专用搜索连接器/MCP → 内置网页搜索 → 浏览器抓取降级链;视频 reviews/views 读 comments.json | `enrich.json`(五顶层键:`author_page`/`similar_page`/`views_page`/`reviews`/`cross_book_external`) | 某块全档抓不到 → 该键置 `null` 整块隐藏(子视图/内联块 + 入口一并删);蒸馏主体不依赖网络,联网失败不阻塞 |
| **Step4** 跨书索引登记 + 互链 | `distill.concepts` 逐个与现有索引语义匹配,赋 5-tag(SUPPORTS/REFINES/CONTRADICTS/NEW_SUB_ASPECT/NEW_CONCEPT),登记本书 entry + 渲染 ⑤ `.crossbook` 已蒸书互链 | `cross-book.md`(§2 精确四步 + §3 tag 判定) | ① `python $SKILL\scripts\update_index.py query --index "$DATA\knowledge-index.json" --names-only` → ② 写 `index-merge.json` → ③ `... register --index "$DATA\knowledge-index.json" --merge "$DATA\{书目录}\index-merge.json" --dry-run`(exit 0)→ ④ 去 `--dry-run` 真跑 | `index-merge.json` / 更新 `knowledge-index.json`(+.bak) / ⑤ 互链数据 | register exit 1 = 校验错 → 按 stderr 逐条修 `index-merge.json` 回 ③ 重校验(**禁用 `--force` 绕 exit 1**);exit 2 = 同书 slug 冲突 → 确为重蒸才加 `--force`,slug 撞车则换唯一 slug |
| **Step5** 设计两遍工作法 | 为这本书出 token plan + signature 决策,过对抗自审;品牌锁八成、书魂放两成 | `design-craft.md`(两遍工作法)+ `brand-tokens.md`(主题 token 契约) | 无(设计决策,内化到 Step6 填槽) | token/signature 定调(不落独立文件,直接指导 Step6) | signature 命中反 slop 黑名单(蓝紫渐变/emoji 图标/圆角+左边框卡滥用/凑数数据)→ 改;衬线模式必配 CJK 衬线兜底 |
| **Step6** 生成单文件 HTML | 复制骨架填**五板块 31 个 SLOT + 2 页内子视图(SUB-AUTHOR/SUB-VIEWS)**的槽,删干净 dummy 与模板占位(`(dummy)`/`(示例)`/`{书名}`/`{作者}`/`SLUG_PLACEHOLDER`/`{{`),可降级区块(concept-chips/reviews/观点对照入口/⑤各块/子视图)数据为 null 时连同 SLOT 注释对整块删 | `html-spec.md`(§1 五板块 + 区块规格表 / §3 生成流程 / §4 章码传送门与目录态 / §5 脑图数据契约 / §6 体积 + extract 兼容) | 复制 `$SKILL\templates\page-skeleton.html` 到 `$DATA\{书目录}\{slug}.html` 后逐槽填充(骨架交互脚本已内联,勿动) | `$DATA\{书目录}\{slug}.html`(单文件,**≤3MB**) | 超体积预算按 `html-spec.md §6` 先删 dummy 再压 excerpts 再压封面(WebP data URI/降尺寸);禁删骨架交互脚本/必需区块/data-source,禁压 narrative 跌破 G9 |
| **Step7** 出厂验证 | 静态 lint + 契约门禁 + Playwright 冒烟:体积≤3MB / 必需区块齐 / 五 tab 文案+panel id 对(禁 v2 旧名)/ ②目录态默认收起+「全部展开」逃生钮 / 章标题论点式(黑名单+长度)/ 书籍真封面 `img.cb-cover[src^="data:image"]` / 2 子视图与入口·返回一致(含 `.subpage-from` 归属语境)/ 金句唯一归宿 ②`.quote-wall`(无 quote-inline/featured-quotes 遗留)/ 无「显示出处」开关且 `.src-note` 常显 / 零外链 / lang="zh" / data-source≥20 / token 块外零 hex(含内联 style 与 SVG 属性)/ 主题切换 body 背景变化;传 `--distill` 追加契约门禁 G8-G21 + G4 扩展 + 模板占位残留 | `html-spec.md §3`(违规修复优先级) | `python $SKILL\scripts\verify_page.py "$DATA\{书目录}\{slug}.html" --distill "$DATA\{书目录}\distill.json" --screenshot "$DATA\{书目录}\_verify.png"; echo "退出码=$?"` | 退出码 + `_verify.png` 全页截图 | **exit 1 = 有违规,按输出逐条修后重跑;exit 2 = 输入问题(页面/JSON 缺失或损坏、缺 playwright/chromium),补齐后重跑;exit 0 才算 Step7 / 本书完成(见硬门禁③)。绝不放宽 verify 或删检查项来「过关」** |

> ⚠ **视频路径现状**:骨架 / `method.md §V` / `html-spec.md §V` / `enrich.md §V` / `verify_page.py` 的视频分支已随 v3/v4 更新到位,**v4-D 已用 Dan Koe 视频系列试点完整跑通并固化**(双语引用 / 热度条 / 概念中英 + 去书味,见 `method.md §6.2` 尾注与 `html-spec.md §V.3`);书样本《金钱心理学》亦已 E2E 通过。视频样本量仍小:蒸视频系列时按 §V 照做,遇到骨架/门禁与视频不吻合的坑先记录再修。
> 跑判成败的脚本别用 `\| tail` / `\| head` 取摘要(管道退出码取最后一段,`tail` 永远成功会吞失败);看完整结尾行或补 `; echo "退出码=$?"`。

## StepA · 作者演变聚合(可选,同一作者 ≥2 部已蒸时)

某作者在 `$DATA` 下已蒸 **≥2 部**作品时,可选做「思想演变专题」聚合页;单书蒸馏不涉及,**<2 部不生成**。

- **做什么**:只读各书 `distill.json`(**绝不重蒸**)聚合成 `author.json` → 渲染作者演变页 `author.html`(4 视图:时间线 / 母题 ribbon / 思想转向 / 概念演化图)。每书蒸馏页顶部「演变入口卡」(SLOT:AUTHOR-ENTRY)链到它。
- **读哪个 reference**:`author-craft.md`(§0 事实 vs 叙事铁律 / §2 author.json schema / §4 四视图数据契约 / §5 板块骨架 / §6 转向证伪层 / §7 入口卡)。
- **跑哪条命令**:`python $SKILL\scripts\build_author.py --author "<作者名>" --data-root "$DATA" --manual "$DATA\authors\{author_slug}\author.manual.json" --enrich "$DATA\authors\{author_slug}\author.enrich.json" --out "$DATA\authors\{author_slug}\author.json"`(已有 author.json 且 manual 缺失时防覆盖栏拒跑 exit 2,确需重建加 `--force`;<2 部 exit 3 不生成;**≥2 部但全部缺 pub_year、排不出时间线同样 exit 3**;`--inputs` glob 匹配为空 / manual·enrich JSON 损坏 exit 2);再复制 `templates\author-page-skeleton.html`、把 `#author-data` 槽替换为该 `author.json` 生成 `author.html`。
- **产物**:`$DATA\authors\{author_slug}\author.json` + `author.html`。
- **触发门槛 / 降级**:该作者 <2 部已蒸(或已蒸全部缺 pub_year)→ `build_author.py` exit 3 不生成、连网搜(enrich)不启、每书页入口卡整卡删。
- **出厂验证**:`python $SKILL\scripts\verify_page.py "$DATA\authors\{author_slug}\author.html"; echo "退出码=$?"`(自动识别作者页走独立门禁:4 视图齐 / 零外链 / Zero-Hex / lang=zh / 破折号 / 深链格式 / 转向 verdict 一致;exit 0 才算完成)。

---

## 硬门禁(三处,不过不许往下走)

1. **Step0 exit 3 → 停下问用户**:诊断判「需OCR」(扫描版纯图)或「需人工确认」(gb18030 疑似假字/乱码率>2%)时,**不启动蒸馏、不硬读、不编内容**,把 diagnose 结论报给用户定夺(补 OCR / 换文件 / 人工核编码)。**视频系列同理**:`build_series.py` exit 3(全部视频都缺转写,一个都没抓到)→ 停下问用户(补转写 / 换视频 / 核 manifest),不拿空语料硬蒸;`diagnose.recommendation=需人工确认`(乱码率>2%)同样照此办理。
2. **Step2 两遍质量门禁自查(G1-G21,+G4 扩展 a/b)**:Pass1 骨架 + Pass2 详实转述产出后,按 `method.md §7` 逐条自查(通用 G1-G7 + 书型专项 + 浏览层 G8-G21 + G4 扩展)。空洞夸赞 / 无锚点论断 / 硬门槛未达 / 公式含糊(含 formula_read/sketch 越界,G4 扩展)/ 叙事压成标签 / **章标题非论点式(G8)/ narrative 详实度不足(书<800·视频<400 字·G9)/ layman_analogy 有空(G10)/ soul_module 不合规(G11)/ self_check·action_chain 越界(G12/G13)/ excerpts 缺或超 150 字版权红线(G14)/ primary·featured 越界(G15)/ cover_intro 不合规(G16)/ action_chain detail 过薄(G17)/ credibility_verdict 缺(G18)/ core_question 缺或非疑问句(G19)/ chain_steps 越界(G20)/ hook 超长(G21)** = 打回重蒸 / 回补,不带病进 Step6。
3. **Step7 verify exit 0 才算完成**:`verify_page.py`(传 `--distill` 追加契约门禁)退出码非 0 就不是成品。按输出修数据/样式后重跑,直到 exit 0。**绝不放宽验证阈值或删检查项来假过关**。

## 铁律(每步都守)

- **锚点**:蒸馏内容必须锚定原文,`method.md §5.1` **六类字段**(core_ideas / decision_rules / quotes / mental_models.evidence / chapters.excerpts / self_check)每条带 `anchor`,上站进 `data-source`;无锚点论断 = 门禁打回。
- **论点式标题**:`chapters[].title` / `.bd-chapter` `<h3>` 一律**可反驳的判断句**,禁「第N章 / 视频N」式纯章号、禁通用容器词(章节脉络/全书脉络/金句墙/总结/概述…),有效长度 ≥8 字(G8;verify 机拦黑名单+长度,判断句语义靠蒸馏自查)。**脑图二级节点(v4 批 A 双层化)例外**:`topic` 改概念关键词 ≤10 字做扫读层、**取消 ≥8 字下限**(仍守黑名单+禁容器词);可反驳判断句下沉到 `tags[0]`(≥8 字,verify 机拦缺失/过短),`tags[1]` 放「第N章」章码 chip(见 method §4.6 / html-spec §5)。
- **详实度下限**:每章 `narrative` 书 ≥800 字 / 视频段 ≥400 字(G9);宁可少论点讲透,不注水;**标志性案例 / 故事必须整段完整讲**(时间·人物·动作·转折·结果),禁压成一句标签。
- **真封面(书)**:书籍刊头封面(`img.cb-cover`)必须**真封面 base64**(`data:image`),禁外链、禁纯色占位;联网拿不到才退占位 SVG。视频用系列封面(首集缩略图 `data:` URI)。
- **URL**:外部信息(作者/书评/同类书/观点对照/跨书外部)必须带可点击 http(s) 来源 URL;拿不到就降级隐藏,不臆造。
- **不编造**:金句 `<blockquote>` / `excerpts` 原文照录不改写(直接照录单段 **≤150 字**,blockquote 明示引用,连续 30 字与原文雷同即版权红线须改写);拿不到的数据(评分/年份)据实留空,不制造假精度。
- **破折号一律 `--`**:所有给读者看的文字里用两个英文连字符,禁全角 `——`。
- **底部「回原书」声明**:页面底部固定 AI 拆书当地图、别当目的地的收口声明(骨架已带,别删)。

## 批量模式(蒸多本)

- **先抽样 1 本人工验收再铺量**:多本任务先完整跑通 1 本(Step0-7 + 浏览器过一遍),你/审校者确认质量与 signature 成立,**通过才并行铺其余**。
- **6 本/批、批内串行**:小批次防服务端 529 Overloaded;一次性高并发会大面积失败。
- **Pass2 fan-out 是本轮最大成本**:v2 蒸馏成本约为 v1 的 2.5-3 倍(第二遍详实转述 per-chapter 分组并行 + 三页搜索);使用当前 Agent 的高推理能力档,不绑定具体供应商或模型名。批量铺量时把每本内部的 Pass2 fan-out 也算进并发预算,别一次性起太多。
- **以盘上文件为准**:部分「失败」的 agent 其实已写盘、只是返回元数据时被限流 → 核对 `$DATA\{书目录}\` 实际产物,别只信 workflow 的 succeeded 计数。
- **索引串行登记**:Step4 的 `update_index.py register` 会写同一个 `knowledge-index.json`,批量时**串行**登记(逐本 dry-run→真跑),避免并发写盘互相覆盖;每次写前自动 `.bak`。

## 环境依赖

- 安装/诊断:从插件仓库运行 `install.ps1 -Agent all`(Windows)或 `./install.sh --agent all`(macOS/Linux);运行 `python $SKILL\scripts\doctor.py` 检查依赖,运行 `python $SKILL\scripts\agent_smoke.py` 验证三端清单与确定性输入管线。安装器不得自动启动模型任务或暗中消耗额度。
- Python:`pip install ebooklib beautifulsoup4 pymupdf pillow pytest playwright` + `playwright install chromium`(Step7 需 chromium;`pillow` 用于真封面 / 缩略图的压缩与 base64 内联)。
- azw3 / mobi 输入需 calibre 的 `ebook-convert`(`winget install calibre.calibre`);epub/pdf/txt 不需要。
- **视频系列**(取材 cascade 见 `method.md §V.0`):`yt-dlp`(YouTube 抓字幕 + 抓评论;B站评论走公开 API 免依赖)。B站/抖音的转写需一个字幕/ASR 上游工具(如 `video-to-subtitle-summary`,读其 `AI_DOUYIN_API_KEY`);fetch_comments 的 B站评论无需 key。**无字幕 / 需画面语义**走一个 Gemini 视频分析工具:本仓兄弟 skill [`sansheng-gemini-video`](https://github.com/sandypoli-boop/sansheng-gemini-video)(读 env `GOOGLE_API_KEY`),装上即可;不装不影响书籍蒸馏与有字幕视频。
