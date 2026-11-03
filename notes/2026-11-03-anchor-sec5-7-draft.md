# AnchorMTM 第 5–7 节草稿（2026-11-03）

## 背景

- 合作者 11 月 2 日的 AnchorMTM 新稿（`paper/pvis2027/drafts/method_anchor_figures_updated_en.tex`，提交 `6f0f2dc`）只写完了第 1–4 节，第 5–7 节（实验、讨论、结论）是占位标题。
- 10 月 30 日的完整版（提交 `91e1fb8`，`paper/pvis2027/main.tex`）有全部实验：917 帧、七个序列，结果经 `validate.py` 核验。
- 用户决定由我起草第 5–7 节。

## 产物

- `paper/anchor_full/main.tex`：第 1–4 节为合作者 11 月 2 日的原文，**未改动**；第 5–7 节为新写的内容。导言区只加了 `booktabs`，图片路径改为本地的 `figures/`。
- 图和表取自两处：
  - `91e1fb8` 的 `fig_compare`、`fig_controlled_conflict`、`fig_frontier`、`fig_direction`、`fig_dataset_overview_extended`，以及 `tables/tab_volume.tex`；
  - 11 月 2 日新稿的首页图和对应关系图。
- Overleaf 包：`paper/anchor_full_overleaf.zip`。主文件为 `main.tex`，用 pdfLaTeX 编译。

## 写法

- 第 5–7 节的数字全部沿用 10 月 30 日版的原文。我没有重新计算，也没有新增数字。
- 术语按新框架统一：
  - 精确模式（Exact Mode，ε=0）、预算模式（Budgeted Mode，ε>0）；
  - 定理 1–3 分别对应 `thm:order`、`thm:width`、`thm:chain`；
  - 旧的 R20 改称 "uncapped κ construction"；
  - 投影基线即 ε=∞。
- 第 5 节按合作者的小节标题组织：
  - 5.1 设置：数据表、方法、指标、对 TMTM/ST-MTM 的复现核验；
  - 5.2 跨方法对比（Fig. compare）；
  - 5.3 界与权衡：可控冲突、权衡曲线、局部预算响应、大树上界的紧度、三维参考方向；
  - 5.4 案例：118 帧 Storms 基准与首页图的解读、五组数据快照；
  - 5.5 消融与性能：宽度感知排序（表 volume）、搜索覆盖与误差上限、运行时间。
- 第 6 节覆盖合作者 TODO 里列的四点：投影损失、候选覆盖、栅格效应、可读性验证；另加"预算改变了什么"和"可复现性"。
- 删去了 10 月 30 日版里新稿已不再成立的说法，例如"Supplement S4"、"68 unit tests"。我凭图读出、未经核实的描述也删掉了。

## 风险 / 待确认

1. **页数**：第 1–4 节约 5.1 页，新章节正文约 3000 词，另有 5 张图和 2 张表，估计正文会略超 9 页。可以把 `fig_direction` 或 `fig_dataset_overview_extended` 移到附录。
2. **首页图案例**：逐小时 Storms 的定量数字（Track 260，帧 363–452）不在已拿到的结果里，所以案例段只做定性描述，定量部分用 118 帧基准。
3. 附录引用都写成 "the supplement"，需要和合作者 11 月 2 日的附录章节核对。
4. 合作者 10 月 23 日之后的提交还没合并进私有仓库：拉取约 1 GB 时连接被断开，正在重试。

## 第 3 版（2026-11-03 晚）：按用户要求和交叉评审修改

**用户要求**
- 通篇围绕我们自己的方法写；
- 旧的 κ 构造（即先前的 RG-MTM-R）全部删除；
- TMTM、ST-MTM 写成我们公式的特例。

**交叉评审**
- Codex 额度用完（11 月 4 日 15:49 恢复），改用两个独立子代理：
  - PacificVis 审稿评审员：给 6/10。指出"特例"一说在第 1–4 节没有落脚点；有几处引导句说得比证据更满；正文约超 1 页。
  - 证据审计员：所有数字都与来源一致，约 30 处措辞超出来源。

**修改内容**
1. 新增 4.4 节 "Existing Merge Tree Maps as Special Cases"：
   - 统一公式 Eq. general，来自 10 月 30 日版的 eq:problem，含 E_O、E_G、E_M、E_R、E_C、E_W；
   - 特例表（TMTM、ST-MTM、投影、AnchorMTM）；
   - 各定理的适用范围：定理 1 适用于任何精确拓扑图；定理 2 只适用于区间模型（ST-MTM 和我们）；定理 3 适用于合并误差不超过 η 的图。
2. 摘要和贡献 2 各加一句"已有合并树图是该公式的特例"。**这是对合作者第 1–4 节仅有的改动。**
3. 删除全部 κ：
   - 用 `make_figs_anchor.py` 从保存的结果（`figdata/`，即 `91e1fb8` 的 `code/results`）重画了 `fig_compare` 和 `fig_frontier`，与原图相比只去掉了 κ 和"旧候选池"两组数据；
   - `tab_volume` 不再使用。
4. 新数字：七个序列上，TMTM/ST-MTM 的顺序误差有 54–95% / 57–95% 高于 ν\*，即可以避免。由已保存的 NROE 和 nu_mean 计算得到。
5. 按审计意见收紧措辞，主要几处：
   - "定理对所有图成立" → 写明各自的适用范围；
   - "精确位置" → "参考顺序"；
   - 删掉"最多三倍"；
   - 删掉"Theta0 对所有序列相同"；
   - 栅格标签覆盖 → "在 Ring 和 OLR 的 200 个渲染列上验证"；
   - "ST-MTM 距离保持更好" → "TW 更好，SNS 在多数序列上更好"。
6. 讨论部分新增"使用 AnchorMTM 的流程"三步；局限部分补充了对应关系质量、Θ0 未做敏感性分析、ST-MTM 为复现实现。

**待确认（问合作者）**
- Wildfires、OLR、PM2.5、Ring 的参考方向是自动估计的，还是另外给定的？10 月 30 日版只写了：Storms 东西向、Tangaroa 估计方向、Cylinder 顺流方向。
- 审计员发现的两处数据疑点：
  - Cylinder 的 N1 NROE 为 8.01，高于 ν\*=7.72；
  - tab_direction 中 z 轴的 ν\* 落在"400 个采样方向"的范围之外，说明坐标轴不在采样集中。正文已改为"400 个采样方向"。
- 页数：第 4.4 节约 450 词，加一张表；第 5–7 节约 2900 词，加 5 张图和 2 张表。估计超出约 1 页。建议优先把 `fig_dataset_overview_extended` 或 `fig_direction` 移到附录。

## 第 4 版（2026-11-03 夜）：本机编译，压到 9 页

- 本机已装 tectonic（Homebrew），可以直接编译：在 `paper/anchor_full/` 下运行 `tectonic -X compile main.tex`。
- 全文中文翻译放在 `main_zh.tex`（ctexart 单栏，系统字体 STSong / Hiragino Sans GB / STHeiti）。PDF 为 `AnchorMTM_draft_v4_zh.pdf`，英文为 `AnchorMTM_draft_v4_en.pdf`。
- 压缩前：正文文字在第 9 页结束，但两张大图被排到第 10–11 页，共 12 页。
- 按顺序做的压缩：
  1. `fig_dataset_overview_extended` 移到附录，"跨领域"一段压成两句。
  2. `fig_direction` 换成单栏版 `fig_direction_col`（`make_figs_anchor.py` 从 `figdata/reference_direction20261027` 重画，数据和编码不变）。
  3. 第 4.2.1 节"Helpers inherit…"整段和第 4.2.4 节栅格失败细节压成一句，指向附录。这是合作者第 4 节的改动。
  4. 第 5–7 节删约 300 词，主要是重复表述和可放附录的细节；`fig_frontier` 改到 5.3 节开头定义，图号按讨论顺序排列。
- 结果：正文和全部图表在第 9 页内结束，参考文献占第 10 页，**全文 10 页**。
- **附录需要补上**：五组数据快照图、OLR/Ring 地图对比、Tangaroa 前 30 步的逐帧 τ 图，以及第 4 节移出的失败处理细节。
