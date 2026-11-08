# v21 图设计方案（2026-11-08 晚，内容已定，明天改图）

用户反馈：带指标的 xy 图难读。本文件先确定每张图的内容、编码和文字，明天按此改图。对应稿件：`paper/pvis2027/latex_v21/`。

## 0. 原则

1. 一张图只回答一个问题；读者只看图和图注，就能读出结论。
2. 坐标轴写白话、单位和好坏方向，例如 `Worst displacement per frame (% of axis length, lower is better)`。不用只有作者懂的缩写。
3. 不用平方根刻度：范围跨数量级的用对数，其余用线性。
4. 直接在数据旁标名字，少用图例。全文只用一套方法配色和标记（见第 1 节）。
5. 印刷尺寸下：刻度 ≥6 pt，轴标题和面板标题 7 pt，字体 Times。
6. 同一个量全文同名：每帧最坏位移的帧平均就是表中的 NPE；面板注释写 "NPE"，不写 "worst"。
7. 我画的图都输出 PDF 和 SVG（`svg.fonttype: none`），方便用户手调。

## 1. 统一配色、标记和名称

| 对象 | 颜色 | 标记 |
|---|---|---|
| AnchorMTM Exact（ε=0） | 深蓝 `#08519c` | 实心圆 |
| AnchorMTM ε>0 | 蓝色渐浅：ε 越大越浅（`#2171b5`→`#9ecae1`） | 实心圆 |
| 表中采用的预算（Storms 10%、Ring 1%、PM2.5 5%） | 橙色描边 `#e6550d` | 同上，加橙边 |
| TMTM | 灰 `#636363` | 方块 |
| ST-MTM | 品红 `#c51b7d` | 菱形 |
| OLO | 土黄 `#a6761d` | 三角 |
| Hilbert / Morton | 绿 `#1b9e77` | + / × |
| 投影 | 黑 | 五角星 |
| 参考位置 q | 浅灰 `#969696` | 小点 |
| 下界以下（不可达）区域 | 浅灰斜线 | — |

旧图 7 的 Exact 用灰色，和 TMTM 撞色，改成深蓝。

指标名称：
- **每帧最坏位移** = max_i |x_i − q_i| / L，"% of axis length"。它的帧平均就是 NPE。
- **顺序误差 NROE**，"% of axis length"。
- **合并误差 NMLE**，"% of value range"。

## 2. 正文各图

### 图 1 Storms 首页图（她）
保持不变。

### 图 2 冲突示意（她）
保持不变。四个叶子的参考顺序 A,C,D,B 是全文的标准例子。

### 图 3 流程图（她，PPTX：`latex_v21/figures/anchor_framework.pptx`）
内容不变，要改的地方：
- 输入 `F(x, t)` 改为 `f_t`（与正文一致）；方向 `d` 改为 `a*`。图注目前写"d 即 a*"，图改好后删掉这句。
- 第 (2) 块示例的参考顺序 A,C,B,D 改成与图 2 一致的 A,C,D,B（Exact 行：x 顺序 A,B,C,D；Budgeted 行：x 顺序 A,C,D,B）。如果改动太大，可以保留，但要在图注里说明是另一个例子。
- 第 (2) 块可在 x 轴旁加一行小字 "anchors within cap τ + β₀"，让"选序 + 带上限放置"两步都出现在图里（可选）。
- 印刷尺寸下最小字号 ≥5 pt，主要是 "t+1"…"t+7" 和 x、q 行标签。

### 图 4 受控树验证（我，单栏，两个面板）
- **问题**：下界准不准？**结论**：(a) 下界、我们的搜索和穷举最优三者重合；(b) 预算恰好在 2ε = h 处解除冲突，与定理 3 的预测一致。
- **数据**：她的 `code/results/controlled_conflict20261030`（43 个重叠值 × 4 种宽度，4152 次独立 LP）。脚本：`paper/anchor_full/figure_drafts/make_figure_drafts.py`（改为 Times 字体）。
- **(a)**
  - x：`Overlap d of the two subtrees (%)`，−12 到 30。d<0 一段浅底色并标 "no overlap"。
  - y：`Worst displacement (% of axis length)`。
  - 三条线直接在线旁标名，不用图例框："point bound ν*"（虚线）、"width bound (Thm. 2)"（空心圆）、"optimum over all 24 orders"（实线）。
  - 小树和 q=(.2,.5,.5−d,.8−d) 移到左上空白处，不压坐标轴。
- **(b)**
  - x：`Merge budget ε (%)`。y 同 (a)。
  - 四个父节点间隙 h=20/40/60/80% 用同一色系的四条阶梯线。
  - 在 ε=h/2 处画空心圆，标 "predicted by Thm. 3"，让人一眼看到预测与实测重合。

### 图 5 位置–拓扑平面（我，通栏，重画）
- **问题**：现有方法的误差有多少是树强迫的？**结论**：保持树的方法（TMTM、ST-MTM、OLO）都在 x=0 上、远高于下界；投影和空间填充曲线顺序误差小，但破坏了树；AnchorMTM 贴着下界走。
- **面板**：正文只留 Q2 文中引用的四个序列：Storms、Wildfires、Tangaroa (3D)、Cylinder (3D)，1×4，每个面板放大。OLR、PM2.5（逐日）、Ring 和七个序列全图放补充材料（现有 S5 更新）。
- **x 轴**：`Merge error (% of value range)`。
  - 0–20% 线性。
  - 右侧加一条窄的"off-scale"带：超过 20% 的点（投影 5.6–59%、部分曲线 8–40%）画在带里，旁边标数值，例如 "Projection 59%"。
  - 去掉平方根刻度。
- **y 轴**：`Order error (% of axis length)`，各面板独立线性刻度。
- **编码**：
  - 灰色斜线区域 = 任何地图都到不了的区域。第一个面板里写 "unreachable (Thm. 1–3)"。
  - AnchorMTM：蓝线，ε 网格点为圆点，在线旁标 "AnchorMTM, ε = 0 → 20%"。
  - TMTM、ST-MTM、OLO：x=0 处的三个点，第一个面板里直接标名字，其余面板只用标记。
- **Storms 面板的注释**：在 x=0 处用竖向括号把 0 到 ν* 标为 "forced by the tree"，把 ν* 到基线标为 "chosen by the layout (76–79%)"。
- **数据**：`plane_fig.py compact` 的现有数据，不重算。基线镜像沿用"与参考更一致的全局镜像"，图注里写明。
- **图注**：只写一次三句话：每个点是什么、灰区是什么、怎么读。

### 图 6 体数据位置图（我，通栏，小改）
- **问题**：各方法把体数据的特征画在哪里？**结论**：TMTM、ST-MTM 把 Cylinder 的涡集中在轴中部；Exact 已经呈现参考的脱落图样；Tangaroa 要到 20% 才接近参考。
- 结构保持 2×6。要改的地方：
  - 面板下注释改为 "mean x%, NPE y%"（与表同名）。数字字号 6 pt。正预算面板加 "merge error z%"。
  - 第一列标题改为 "Reference q (target)"。
  - 列标题按第 1 节方法配色着色。
  - 色标标签改为 "signed displacement (x − q), % of axis length"。
- 不重算，数据在 `figdata/volume_gallery20261108/`。

### 图 7 逐帧预算分布（我，通栏，重画）
- **问题**：预算买到了什么？**结论**：在 Storms 上预算只削掉困难的尾部（35% 的帧用到预算）；在 PM2.5 和两个体数据上，几乎每一帧都用到预算，整个分布下移。
- **面板**：Storms、PM2.5（逐小时）、Tangaroa (3D)、Cylinder (3D)，1×4，只保留一行。
  - Wildfires 只有 7 帧受预算影响，移到补充材料；Ring 也移到补充材料。
- **x**：`Merge budget ε (%)`，按类别排列。平面数据 0, 1, 2, 5, 10, 20；体数据 0, 2, 5, 10, 20（没有 1%）。
- **y**：`Worst displacement per frame (% of axis length)`，对数刻度，刻度 0.1, 0.3, 1, 3, 10, 30。Storms 有极小值（最小 0.006%），低于 0.1% 的点画在 0.1% 处，用三角标记，并在图注里说明。
- **编码**：
  - 箱：四分位；须：5–95 百分位；须外画点；菱形是均值，即表中 NPE。
  - Exact 深蓝，ε>0 浅蓝，表中采用的预算加橙边（Storms 10%、PM2.5 5%）。
- **每个箱下的一行小字**："帧中用到预算的比例"（合并误差 >0 的帧）。这一行替代原来的合并误差那一行。参考值：

  | 序列 | ε | 用到预算的帧 |
  |---|---|---|
  | Storms | 10% | 262/744 = 35% |
  | PM2.5 | 5% | 724/744 = 97% |
  | Tangaroa | 正预算 | 200/201 |
  | Cylinder | 正预算 | 98/102 |

- **合并误差**：原来的合并误差一行移到补充材料。图注写一句 "no frame exceeds its budget"，并给出各档的最大合并误差。
- **数据**：
  - Storms：`budget_tradeoff_20261105/planar_per_frame/Storms/epsilon_*.csv`；
  - PM2.5：`pvis2027/pm25_hourly_20261107/six_budgets_20261108/PM25_six_budgets_per_frame.csv`（她 11-08 提供，6×744 帧，已核对：0% 与 5% 的均值等于表 2 的 0.1390 和 0.0468）；
  - 体数据：`budget_tradeoff_20261105/volume_per_frame_audit.csv`。
- **备注**：PM2.5 的 2% 那档有一次同目标 QP 备用求解记录，补充材料里如实写一句。

### 图 8 Storms 多预算对比（她，PPT）
要改的地方：
- "Improvement 1: + Spatial Awareness"（TMTM → ST-MTM）和 "Improvement 2: + Topology Budget"（ST-MTM → Ours）这套框架，会让读者以为 AnchorMTM = ST-MTM + 预算，漏掉了核心的空间参考，也和正文"TMTM、ST-MTM 是统一表述的特例"矛盾。改为：TMTM、ST-MTM（同一行，标 "exact topology, no spatial reference"）→ 箭头 "+ spatial reference" → AnchorMTM ε=0 → 箭头 "+ merge budget" → ε=2…20%。
- 给地图加坐标轴提示：横向 "time →"，纵向 "position along a*"。加 [−35, 35] hPa 色标，图注里的色标说明可以删掉。
- 图注最后一句 "Module connections summarize design differences rather than exact algebraic equivalence" 改图后可以删。

### 图 9 PM2.5 案例（她，matplotlib：`pm25_hourly_20261107/draw.py`）
要改的地方：
- 字体从 DejaVu Serif 改为 Times；日期标签由 3.6 pt 放大到 ≥5 pt。
- 纵轴 "Mapped position" 改为 "Position along a* (fraction of extent)"。
- 在第一张快照上画一个箭头表示参考方向 a*，让地图上的高低和地理方向对应起来。
- 可编辑版本：`latex_v21/figures/pm25_hourly.svg`。

## 3. 补充材料的图

- **S1–S4**（预算相关，我）：沿用第 1 节配色和对数刻度。新增两样：
  - Ring、Wildfires 的逐帧分布；
  - 所有序列的合并误差行，即原图 7 下半。
- **S5 平面全图**（我）：七个序列，用新图 5 的画法。
- **S6 方向**（我）：只改配色和字体。
- **Cylinder、Ring、方向和松弛示意图**（她）：不动。

## 4. 正文要跟着改的地方

- 图 5 图注：改为"七个下界序列中的四个；全部见补充图 S5"。Q2 文中的数字不变，引用的四个序列都在图里。
- 图 7 图注与 Q4：
  - 写 Storms 削尾（中位数 1.10% → 0.84%，90 分位 10.7% → 2.5%，35% 的帧用到预算）；
  - 写 PM2.5 与体数据整体下移（PM2.5 中位数 14.5% → 2.1%（5%），97% 的帧用到预算）；
  - 删掉"Gaussian 省略"之外不再需要的说明。
- 图 4 图注：去掉线型说明，因为线旁已直接标名。
- 6.1 Measures：图 5、6 的镜像规则保持现有一句。

## 5. 篇幅

当前正文正好 18.0 栏，没有余量。
- 新图 7 只剩一行，高度约从 178 pt 降到约 115 pt，省约 0.1 栏。
- 新图 5 面板少了，但每个更大，高度维持约 140 pt。
- 改完后目标 ≤17.9 栏。

## 6. 明天的顺序

1. **我**：重画图 7 → 图 5 → 图 4 → 图 6，以及补充材料 S1–S5，并同步图注和 Q4 文字。编译、量栏数、提交。约 3 小时。
2. **她**：图 3、8、9 的修改（第 7 节的意见可以直接转给她）。
3. **然后**：第 6 步全文核对（每个数字对到结果文件、交叉引用、补充材料），之后定稿。

## 7. 给合作者的修改意见（可直接转发）

> 图 3（流程图）：
> - 输入 F(x,t) 改为 f_t，方向 d 改为 a*，与正文记号一致；
> - 第 (2) 块示例的参考顺序请改成和图 2 一样的 A,C,D,B；
> - 小字（t+1…t+7、x、q）在印刷尺寸下请不小于 5 pt。
>
> 图 8（Storms 对比）：
> - "Improvement 1: + Spatial Awareness / Improvement 2: + Topology Budget" 会让读者以为我们的方法 = ST-MTM + 预算，漏掉了空间参考这个核心。请改为：TMTM、ST-MTM 放在同一侧，标 "exact topology, no spatial reference"，箭头 "+ spatial reference" 指向 ε=0，再箭头 "+ merge budget" 指向 ε=2–20%；
> - 地图请加 "time →" 和 "position along a*" 的轴提示，并加 [−35, 35] hPa 色标。
>
> 图 9（PM2.5）：
> - 字体改为 Times，日期标签放大到 5 pt 以上；
> - 纵轴改为 "Position along a* (fraction of extent)"；
> - 第一张快照上加一个箭头表示参考方向 a*。
>
> 另外：PM2.5 的镜像规则、六档预算数据和表 1 的描述都已按你的说明写进稿子，谢谢。

## 8. 执行记录

### 2026-11-09 图 7 已重画（第 1 张）
- 脚本：`paper/anchor_full/figure_drafts/budget_distribution.py v22`，输出 `latex_v21/figures/budget_per_frame.{pdf,svg}`（SVG 文字可编辑），预览 `figure_drafts/preview_v20/budget_per_frame.png`。旧的 `budget_distribution_2d3d.*` 已从 figures/ 删除（git 历史里有）。
- 按第 2 节方案做到的：
  - 一行四面板：Storms、PM2.5 逐小时、Tangaroa、Cylinder；平面 0/1/2/5/10/20%，体数据 0/2/5/10/20%。
  - 纵轴对数，刻度 0.1–30，所有面板共用；Storms 有 7 帧低于 0.1%，画在 0.1% 处，用三角表示。
  - 配色：Exact 深蓝实心；ε>0 浅蓝；表 2 用的预算（Storms 10%、PM2.5 5%）加橙边，并标 "Table 2"。
  - 底行"frames using it"取代原来的合并误差行。
  - 印刷宽 6.9 英寸，最小字号约 6 pt；高度约 107 pt（原约 178 pt）。
- 脚本里的核对（断言）：
  - Storms 的 0% 和 10% 逐值等于表 2 的运行；
  - PM2.5 的 0% 和 5% 均值等于表 2（0.1390、0.0468）；
  - 所有帧的合并误差都不超过预算（Cylinder 在 ε=0 有 1e-7 的渲染残差，容差 1e-6）。
- 数字（用到预算的帧）：

  | 序列 | 各档用到预算的帧（括号内为预算） |
  |---|---|
  | Storms | 80 (1%)、120 (2%)、197 (5%)、262 (10%)、294 (20%)，共 744 |
  | PM2.5 | 620、680、724、730、731，共 744 |
  | Tangaroa | 200、200、201、201，共 201 |
  | Cylinder | 各档都是 98，共 102 |

- 中位数：
  - Storms 1.10% → 0.84%（10%）；90 分位 10.74% → 2.49%；最大 44.84% → 11.55%。
  - PM2.5 14.48% → 2.10%（5%）。
  - Cylinder 6.76% → 1.04%（2%）。
  - Tangaroa 11.32% → 1.20%（20%）。
- 正文：
  - 图注改为对数刻度、底行含义、"no frame exceeds its budget"，以及 Wildfires、Ring 和逐帧合并误差在补充图 S1–S3。
  - Q4 重写为"预算买到什么，取决于多少帧含有可释放的冲突"：
    - Storms：35% 的帧用到预算，削掉尾部；
    - Wildfires、Ring：指向 S1；
    - PM2.5：97% 的帧用到预算，整体下移，中位数 14.5% → 2.1%；
    - 体数据：同样整体下移。
- 篇幅：正文 17.7 栏（原 18.0 栏），11 页。
- 留给补充材料那一步：S1 目前只有 Storms、Wildfires、Ring 的逐帧合并误差，要加 PM2.5 一列，图注第二句才完全落实；PM2.5 2% 那档的 QP 备用求解在补充材料里写一句。
