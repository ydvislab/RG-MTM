# 对比地图的朝向口径（2026-11-06，分析与建议，待用户决定）

用户问："这个朝向修改不修改会带来什么问题？最好怎么确定？"

## 一、问题在哪

- 一维合并树图本身没有方向：把整张图上下镜像，得到的仍是同一方法的合法输出。TMTM（时间对齐）、ST-MTM（两两距离 + 时间）以及 TMTM-style / ST-MTM-style 目标都对镜像不变，镜像图是同一目标下同样最优的解。
- 我们的 NROE 和位移是相对**有方向的**参考轴 q 计算的，所以对比方法的朝向会直接进入它们的分数。
- AnchorMTM 不受影响：它的轴由 q 定义，没有朝向选择。下界、NMLE、ME、TD、SNS、TW 也都与朝向无关。

## 二、现有协议

`code/experiments/era5.py` 第 258–265 行：TMTM、ST-MTM 按第一帧锚点与**质心 x 坐标**的相关性做一次全局翻转。规则事先固定、只用第一帧，但它对照的是 x 轴，不是参考方向 q。

## 三、实测（脚本：`figure_drafts/stmtm_threshold.py`、`volume_orientation.py`；均先逐帧复现保存值）

原生地图 NROE（%）与"不是树造成的"比例：

| 序列 | ν\* | TMTM 协议 | TMTM 镜像 | ST-MTM 协议 | ST-MTM 镜像 | 协议是否与 q 反向 |
|---|---:|---|---|---|---|---|
| Storms | 3.77 | 19.23（80%） | 18.31（79%） | 16.28（77%） | 17.10（78%） | 否 |
| Wildfires | 5.80 | 29.30（80%） | 19.65（70%） | 24.02（76%） | 18.72（69%） | **是** |
| OLR | 0.89 | 19.31（95%） | 24.07（96%） | 17.21（95%） | 16.59（95%） | **是** |
| PM2.5 | 0.97 | 12.87（92%） | 4.44（78%） | 11.60（92%） | 5.21（81%） | **是** |
| Ring | 2.66 | 7.18（63%） | 9.78（73%） | 10.39（74%） | 4.47（41%） | 否 |
| Tangaroa | 9.24 | 20.09（54%） | 19.50（53%） | 21.34（57%） | 15.80（41%） | — |
| Cylinder | 12.24 | 26.62（54%） | 28.24（57%） | 17.77（31%） | 28.75（57%） | — |

- 协议与参考方向在 5 个平面序列中的 3 个上相反（Wildfires、OLR、PM2.5）。
- 按"第一帧对照 q"定朝向（方案 B）也会选错：OLR 上 TMTM 被翻到整体更差的一侧（19.31→24.07）；OLR 第一帧只有 3 个叶子。
- 同模型目标（`unified20261025`，画布镜像 x' = 2·origin + L − x）：大多已在较优朝向；**OLR 的 ST-MTM-style 例外：平均位移 42.7%→19.3%，NPE 66.4%→30.7%**。图 6 中这一列目前是相对参考倒置的。
- 空间填充曲线（8 种轴对齐朝向）：正文报告的是 8 种朝向的平均（NROE 8.3–23.4%）；最优朝向下降到 0.3–12.6%（OLR Morton 0.91%，PM2.5 Morton 0.27%，低于 ν\*，因为曲线不保树），代价是合并误差 19–39%。

## 四、三个方案

| 方案 | 做法 | 好处 | 问题 |
|---|---|---|---|
| A 保持协议 | 第一帧对照质心 x | 不用改图；事先固定 | 3/5 平面序列与参考相反，对对比方法不利；附录 S10 已公开镜像数值，审稿人一对照就能看出（如 PM2.5 TMTM 12.87 对 4.44）；图 6 的 ST-MTM-style 一列是倒置的 |
| B 第一帧对照 q | 同样只用第一帧，但对照参考方向 | 规则因果、简单 | 第一帧叶子少时会选错（OLR TMTM） |
| C 最有利镜像 | 每张对比地图取与参考更一致的那个全局镜像（原生图按平均 NROE，同模型图按平均位移；曲线取 8 种朝向中最优） | 镜像是同一方法同样最优的输出；只对对比方法有利，结论最保守；通用规则，无逐数据集选择 | 用到了整段序列（但只朝有利于对比方法的方向）；要重算图 4a、图 5 灰框、图 6 的 ST-MTM-style 列和 S10 表 |

## 五、建议：方案 C

判断标准：我们的主张是"对比方法的大部分顺序误差不是树造成的"。这类主张应在**对对比方法最有利**的设定下成立，否则结论可以被归因于我们的约定。方案 C 正好满足，而且是通用规则。

方案 C 下的变化：

- 摘要和引言的 **31–95% 不变**：TMTM 53–95%（原 54–95%），ST-MTM 31–95%。
- TMTM 在七组上都是"大部分不是树造成的"（≥53%）；ST-MTM 在 Storms、Wildfires、OLR、PM2.5 上是（69–95%），在 Ring（41%）、Tangaroa（41%）、Cylinder（31%）上不是。5.3 小标题和贡献 3 的"most"需要改为分组表述。
- 图 4a：Wildfires、PM2.5、Storms（TMTM）、OLR（ST-MTM）、Ring（ST-MTM）、Tangaroa（ST-MTM）的柱子变化。
- 图 6 与 5.5：ST-MTM-style 的平均位移 42.7%→19.3%（仍远高于精确模式的 1.0%）；图中该列需镜像重画。
- 曲线：改写为"最优朝向下顺序误差可降到 0.3–12.6%，但只能靠破坏树（合并误差 19–39%），与投影同类"。需要按朝向重算 δ\*（脚本 `space_filling_baselines.py` 已有）。
- ME、TD、SNS、TW、NMLE 和所有 AnchorMTM 数值不变。

工作量：约半天（改 `make_figure_drafts.py`、`make_olr_hovmoller.py`、`make_supplement.py` 的取值，重画三张图，改正文约 6 处数字）。

## 六、Wildfires 补跑（已完成）

- 输入 `data/real/wildfire/wildfire.json` 从 Zenodo records/11234747 下载（64,795,452 字节，SHA-256 `2a8dd31bf6d222d7de673c7e7b2af94550660f1996b0a5db256d97f2b9c2ed9f`），已加入 `.git/info/exclude`，不入库。
- 输入场哈希与 `framework20261025` 一致；r=0.95 时 ST-MTM 与 TMTM 逐帧复现保存值。
- 所有 r 和两种朝向下：ST-MTM 53–82%，TMTM 70–80%。已写入 5.3 和附录 S10。

## 七、用户决定与执行（11/6）

用户选择 "Adopt most favorable"：所有对比地图取对其最有利的朝向。

- 实现：`figure_drafts/best_mirror.py`（输出 `figdata/orientation20261106/best_mirror.json`）。原生 TMTM/ST-MTM 取平均 NROE 较低的全局镜像；同模型 TMTM-style/ST-MTM-style 取平均位移较低的画布镜像 x' = 2o + L − x；空间填充曲线取 8 种朝向中平均 NROE 最低者（`space_filling_baselines.py` 现保存逐朝向数值，均值/最小/最大不变）。
- 一致性：三维参考方向实验（`experiments/reference_direction/run.py`）本来就按"对其有利的一次全局翻转"计算原生地图，新规则与之一致。
- 改动的图：图 4（`fig_compare_v2`）、图 5 灰框（`fig_frontier_v2`）、图 6（`fig_olr_maps`，ST-MTM-style 一列镜像）。附录表：S10 位置表、曲线表、阈值表；S11 位移与跳动表。
- 正文：5.1 写明规则；5.3 小标题改为 "The tree forces only part of the order error of TMTM and ST-MTM"，TMTM 53–95%（每组），ST-MTM 69–95%（四个真实平面序列）、31–41%（Ring 与两组体数据）；Storms 例子 18.3%；曲线改为"最优朝向下 NROE 0.3–12.6%，有时低于 ν\*，但最坏帧合并误差 8–40%"；5.5 OLR 的 ST-MTM-style 平均位移 42.7%→19.3%；贡献 3 改为 31–95%；图 4–6 图注注明朝向。摘要、引言、结论的 31–95% 不变。
- 为放下新句子，删去 5.6 的复杂度句和软件版本、Cylinder 宽度感知句、讨论中的重复句。正文第 9 页结束，全文 11 页；附录 18 页；Overleaf 包 42 个文件从零编译通过。
- PDF：`AnchorMTM_draft_v10_en.pdf`、`AnchorMTM_supplement_v5.pdf`。

## 八、中文版同步（11/6）

- `paper/anchor_full/main_zh.tex` 按英文 v10 逐段重译：摘要与引言（606/614 帧、31--95%）、第 4 节新顺序（模型 → 下界 → 参考 → 构造，含框架图）、第 5--7 节全部改写内容（最有利朝向规则、53--95% / 69--95% / 31--41% 分组表述、曲线 0.3--12.6%、OLR 19.3%、Θ0 敏感性 578--608、局限中的配置一句）。
- 旧中文稿中英文已删去的内容（Vortex 段、复杂度与软件版本句等）一并删去。
- 编译：`tectonic -X compile main_zh.tex`，17 页，无未定义引用。PDF：`AnchorMTM_draft_v10_zh.pdf`。

## 九、加入 OLO 并按两类方法重组对比（11/6，v11）

用户担心只和 TMTM、ST-MTM 比"有针对性"，决定："Add OLO and reframe"。

- **OLO 基线**：Bar-Joseph 2001 的最优叶序，代价是支撑质心的相邻距离，每帧取与前一帧一致的镜像。它就是 ST-MTM 在 r=1 时的排序。少数帧上时间一致叶序的代价不高于 SciPy 的 OLO，此时保留该叶序：平面 5/614，Tangaroa 51/201，Cylinder 10/102。OLO 没有锚点，只比较 NROE。
  - 平面数据：`stmtm_threshold20261106/results.json`，取 `thresholds['1']`。
  - 体数据：新脚本 `figure_drafts/olo_volume.py`，输出 `figdata/stmtm_threshold20261106/olo_volume.json`。
    - 本机没有 Tangaroa 的原始 TTK 树，所以从 features.json 保存的 hierarchy 重建二叉树，按 Adapter 的右链方式细化。
    - 核验：同一代码在 r=0.95 时逐帧复现保存的 ST-MTM 叶序，Tangaroa 201/201，Cylinder 102/102。
    - 解释器：`~/Desktop/RG-MTM/.venv/bin/python`。
- **OLO 结果**：取最有利镜像，括号内为不是树迫使的比例。

  | 序列 | NROE |
  |---|---|
  | Storms | 15.60（76%） |
  | Wildfires | 19.06（70%） |
  | OLR | 16.27（95%） |
  | PM2.5 | 5.17（81%） |
  | Ring | 4.23（37%） |
  | Tangaroa | 15.44（40%） |
  | Cylinder | 18.03（32%） |

  与 ST-MTM 很接近（两者叶序相差很小）。
- **合起来的结论**：
  - 四个真实平面序列上，三种保层次排序均为 69--95%；
  - Ring 和体数据上，TMTM 为 53--63%，OLO 和 ST-MTM 为 31--41%；
  - 摘要和结论中的 31--95% 不变，主语改为"三种保层次排序（OLO、TMTM、ST-MTM）"。
- **正文改动**：
  - 摘要、引言、贡献和结论的主语改为三种排序；引言加一句"下界也能衡量已有的排序"。
  - 相关工作加入 Temporal Treemaps 和 Nested Tracking Graphs（按少交叉排列嵌套特征带，坐标无物理方向），并说明把 OLO 当作通用排序规则来评估。
  - 5.1 对比方法分为两类："保层次的排序"（OLO、TMTM、ST-MTM）和"位置优先的显示"（投影、曲线、Hovmöller）。
  - 5.3 小标题改为 "...of hierarchy-preserving orderings"，按两类数据分组陈述，加一句"未被树迫使的误差是这些排序规则共有的"。
  - 图 4a 加 OLO 柱，图注同步修改；附录表 S6（`supp_stmtm_threshold`）加 OLO 两列。
- **为保持正文 9 页而删去的内容**：
  - 5.3 的 Storms 18.3%/3.8% 例句；
  - "与中点初始化相符"；
  - 运行时间句合并为 94--137 s；
  - 讨论中的 Hovmöller 互补句；
  - 结论的下一步缩短。
- **产出**：
  - PDF：`AnchorMTM_draft_v11_en.pdf`（正文到第 9 页，共 11 页）、`AnchorMTM_supplement_v6.pdf`（18 页）、`AnchorMTM_draft_v11_zh.pdf`（17 页，已同步）；
  - Overleaf 包 42 个文件，从零编译通过。
