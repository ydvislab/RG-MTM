# 最终叙述逻辑（2026-11-06，用户确认）

用户 11/6 确认："论文标号：1037，然后现在开始改写，更新我自己的私有仓库。另外就是当前实验帮我检查有没有有效支撑我们的结论和论文内容。"

工作分支：`paper/v8-narrative`（基于 v7 `40addbc`）。源文件仍是 `paper/anchor_full/main.tex`。

## 一、全文论点

> 合并树图可以有一条空间轴，而且代价比现有地图显示的小得多；不可避免的那部分，可以在画图之前算出来。

- 31–95% 的说法从 "could be avoided" 改为 **"is not forced by the tree"**：数字不变，避免被读成"用我们的参考挑别人的错"（Codex 第 2 轮指出的最大拒稿风险）。

## 二、投稿版本

- 投 `anchor_full`（七个序列、917 帧、三个下界、严格 ν\*）。
- 合作者 `pvis2027` 版只并入**方法框架图** `anchor_framework.pdf`（符号与 v7 一致：η=(ε0+ε)ΔF、τ(π)、δ\*(π)≤η、按 (τ, NROE) 选择、上限 τ+β0、四项 QP）。
- 合作者的四数据集评估、已发表 SNS/TW、Balanced 自动选预算、Cylinder 中心树变体、相关工作流程图**不并入**。理由见 `2026-11-05-reframing-and-metrics.md`。
- `\onlineid{1037}`。

## 三、相对 v7 的改动

1. 摘要与引言重写。引言 5 段：读者要同时读层次和位置 → TMTM/ST-MTM 的轴为树服务，Hovmöller 相反 → 锚定与层次冲突（四叶例子）→ 树到底迫使多大位移：下界、AnchorMTM、结论数字 → 贡献。
2. 贡献三条：① 问题表述与三个下界；② AnchorMTM；③ 917 帧评估（下界在受控树中达到、精确模式贴近下界、现有地图的大部分顺序误差不是树造成的）。
3. 第 4 节顺序：模型与度量 → 三个下界 → 空间参考 → 构造。构造从定理 1 的中点顺序出发，正好"到达下界"。
4. 新增图：方法框架图（第 4.4 节）。页数不够时把算法 1 移到附录。可选：Storms 基准地图（附录 S12）进正文，仅在省出空间时。
5. 文风：段首即结论；正文不写预防性免责，每条局限只在 Limitations 出现一次；第 5 节每段 2–3 个数字；小标题平实（"The price of a spatial axis is stated, not hidden." 与 "Stable is not faithful." 改写）；不用"X, not Y"式对照，除非读者确实会混淆。
6. Vortex 一段移到附录；5.6 运行时间压成一句。

## 四、实验支撑检查

另见 `2026-11-06-evidence-audit.md`（逐条论断对照结果文件）。

## 五、时间表

| 日期 | 工作 |
|---|---|
| 11/6 | 定稿叙述；重写摘要、引言、贡献；第 4 节换序；框架图；实验支撑检查 |
| 11/7 | 第 5–7 节按检查结果和文风改写；页数 |
| 11/8 | 改动数字复核；Codex 复审；中文版同步；匿名性 |
| 11/9 | 提交（AoE） |

## 六、本机环境

- 本机（用户 Mac）新 clone：`~/Research/RG-MTM`，`origin` = `ydvislab/RG-MTM`，`upstream` = `lelewang1109/RG-MTM`（push 已禁用）。
- `~/Desktop/RG-MTM` 是合作者公开仓库的 clone（`origin` 指向公开仓库），**不要在那里提交 paper/ 或 notes/**。
- 本机有 `tectonic`（`/opt/homebrew/bin/tectonic`），可直接编译：`cd paper/anchor_full && tectonic -X compile main.tex`。

## 七、执行记录（11/6，分支 `paper/v8-narrative`）

- 摘要、引言、贡献重写；`\onlineid{1037}`。
- 第 4 节换序：4.1 模型 → 4.2 下界 → 4.3 参考 → 4.4 构造；构造段落写明中点顺序（定理 1）是初始候选。
- 新增图：合作者的方法框架图 `figures/anchor_framework.pdf`（取自 upstream `a092db8`，宽 0.80\linewidth），放在 4.4。算法 1 保留。
- 按实验支撑检查（`2026-11-06-evidence-audit.md`）改写第 5–7 节：
  - 摘要、引言、结论的头条证据从"距下界 0.03 个百分点"改为"ε=0 时所选叶序在 606/614 个平面帧上达到宽度下界"；
  - 5.2 写出逐帧达到下界的计数（平面 606/614，ε=10% 时 596；Cylinder 81/102，Tangaroa 27/201）；
  - 5.3 运动误差改为"四组明显更低，三组相差 1–4 个事件"；"The price of a spatial axis…"改为 "Anchoring costs pairwise-distance fidelity."；
  - 5.4 机制改为"冲突子树合并得浅还是深"（定理 3）；Vortex 段移到附录 S15；
  - 5.5 OLR 改为"在合并树图中，只有锚定图……"；Storms 小标题改为 "an exact map along the west--east axis"；
  - 讨论小标题 "Stable is not faithful." 改为 "Stability and motion."；局限段补"ST-MTM 只用一个重排阈值"。
- 为放下框架图，删去相关工作、讨论、局限中与正文重复的句子。
- 编译：正文在第 9 页结束，参考文献占第 10–11 页，共 11 页（9+2）；附录 16 页。`paper/anchor_full_overleaf.zip` 已更新（39 个文件），解压后从零编译通过。
- PDF：`paper/anchor_full/AnchorMTM_draft_v8_en.pdf`、`AnchorMTM_supplement_v3.pdf`。
- **未做**：中文版 `main_zh.tex` 未同步；ST-MTM 阈值 r 的补充实验待用户决定。
