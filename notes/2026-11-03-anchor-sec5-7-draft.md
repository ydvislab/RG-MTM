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
