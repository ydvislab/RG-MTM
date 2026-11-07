# 改为"代价分析"框架：ST-MTM 核对、相关方法、统一框架、主线第五稿、图的方案（11/8）

用户 11/8：

> 可以，下载 ST-MTM 预印本核对一下。而且我们并不是说要提出一种新的方法来，而是想表明这一种体系的下限计算出来，告诉读者代价发生在哪里是多少。你在确认 ST-MTM 的方法之后，帮我再查一下有没有别的类似的方法，我们也需要对比的，另外想一下我们的方法能否成为一个体系去包括当前问题下所有的计算方式。如果这一切都顺利的话，帮我按照主线推进一下新论文的写作，帮我出一稿，图也要按照优秀 TVCG 论文的标准构思，要说明清楚每一个图想代表什么，当前如果没有图的话，你可以告诉我、构思清楚这个图想表达什么，我们一点一点谨慎推进。

## 一、ST-MTM 原文核对

**来源**
- SSRN 页面有机器人验证，没有下载成功。
- 本机微信文件夹里有用户 9 月收到的 `ssrn-6604235.pdf`，SHA-256 与 `references/provenance.json` 的 `paper2_sha256`（9f9da0e8…）一致，就是同一份预印本。
- 稿件信息：13 页，投 Computers & Graphics（2026 年 4 月 18 日收稿），未经同行评审。

**逐条核对**

| 问题 | 原文 | 结论 |
|---|---|---|
| 保持合并树吗 | 摘要："preserve the hierarchical structure"；贡献："maintains the hierarchy induced by merge trees"；§4.1.1 在树允许的叶序里做 OLO；§4.2.2 按层次填充空隙 | **严格保持层次** |
| 轴上的位置表示什么 | §4.1.2 Eq. (1)：锚点距离拟合质心距离（加权 stress），可加上一帧锚定项 λ；§4.1.3："interval coordinates are derived only from pairwise distances"，按全序列极值统一缩放，并按质心包围盒加对称 padding | **相对距离**：有共同尺度，没有固定原点和方向 |
| 方向（镜像） | §4.1.1：OLO 与其反序空间代价相同，按与上一帧的一致性选一个 | 东西方向不固定，所以我们量 NPE 时要镜像 |
| 叶序参数 | §4.1.1、§7.3：阈值 r，当 Cost(π_olo)/Cost(π_curr) ≤ r 时才换序；λ 控制时间锚定；起始帧 Start | 与合作者复现一致 |
| 指标 | §5.2：SNS（尺度归一化 stress）、TW（邻域）、TD（相邻帧位移和） | 都是相对几何或稳定性，没有绝对位置 |
| 对失真的态度 | §7.1：压缩一处必然拉长另一处（"spring" 比喻）；§7.2："A fundamental limitation of any projection to 1D …"，所以 stress 大于零是 "an expected consequence of the projection process"，不是某个方法的失败 | **承认失真不可避免，但没有回答其中多少是不可避免的、来自哪里** |

**对我们最重要的一点：ST-MTM §7.2 正好留下了我们要回答的问题。** 它承认一维布局必然牺牲空间关系，但没有给出"必然的那部分有多大"。我们对"沿固定方向的位置"这一种空间读法给出答案，并且能区分"由树造成的"和"由布局选择造成的"。引言可以直接从这里切入（需要转述，不能长段引用）。

ST-MTM 的动机图（Fig. 2）也说明了 TMTM 的问题：一个特征在空间里移动，TMTM 图上却静止不动；层次一变，图上就出现突跳。ST-MTM 用相对距离部分解决了这个问题。

## 二、类似方法与对比

两轮查新（9/26 共 42 篇已核实，见 `RA-MTM/notes/related-work-map.md`；10/27 合作者查漏，见 `references/LITERATURE_CHECK_20261027.md`）加上今天补查 2025–2026 的新工作，**没有发现给合并树图的位置失真算下界的工作**。今天的检索没有找到 2025–2026 年新的合并树一维布局论文。

需要正面对比、并且能放进同一框架的方法：

| 类 | 方法 | 叶序规则 | 轴上位置的含义 | 拓扑 | 现有对比数据 |
|---|---|---|---|---|---|
| 合并树图 | TMTM | 每个内部结点按相邻帧重叠贪心选左右 | 树遍历中的位置（样本线性化） | 精确 | 有（早期七序列 + ST-MTM 四数据） |
| 合并树图 | ST-MTM | 受层次约束的 OLO、时间一致、阈值 r | 相对距离 + 上一帧锚定 | 精确 | 有（同上，阈值 r 全扫描） |
| 树约束叶序 | OLO（Bar-Joseph 2001） | 相邻质心距离和最小 | 只有顺序 | 精确 | 有（七序列，只比顺序误差） |
| 空间填充曲线 | Hilbert、Morton | 曲线顺序 | 曲线秩 | 不保持（最坏合并误差 8–40%） | 有 |
| 投影 | 按参考排序 | 按参考排序 | 绝对位置（x=q） | 不保持（最高 59%） | 有 |
| 物理轴 | Hovmöller 图 | 无（沿参考方向平均） | 绝对位置 | 特征被平均掉 | 有（OLR） |
| 锚定 | AnchorMTM（我们的参照构造） | 预算内 τ 最小 | 绝对位置 | 误差 ≤ ε | 有 |

只在文字里比较（数据或问题不同）：

- MotionRugs、GroupRugs、Stable PCA、MoReVis：轨迹的一维摘要，没有层次。
- Geophylogenies（Klawitter 2025）、Bulteau 2022、单侧 tanglegram：树约束叶序贴合外部顺序。组合结构最接近，但目标是交叉数或位移之和，没有宽度和最大位移的闭式下界。
- Spatially Ordered Treemaps、Data-Spatial Grid Maps：层次布局中的位置一致性和渐变权衡，没有下界。
- 拓扑地形（Weber、Beketayev、Oesterling 剖面、Herick 时间连贯版本）：没有位置目标。
- 合并树距离（Munch & Stefanou、Morozov、Gasparovic）：这是我们拓扑误差的理论依据，不是竞争方法。

## 三、能否成为"一个体系"包含所有计算方式

**能，但只针对一种忠实度**：沿一个选定空间方向的位置。

**能包含的部分**

1. **统一模型。** 任何方法在每一帧给出的都是"叶序 + 区间 + 剖面"。每张图都可以用两个数定位：
   - 合并误差：用固定标签量显示剖面与原树的差，等于带标签的交错距离；
   - 相对参考的位置偏差：顺序误差 NROE，或区间模型中的最坏位移 τ。

   所以 TMTM、ST-MTM、OLO、曲线、投影、AnchorMTM 都是"位置–拓扑平面"上的点。
2. **下界就是这个平面的下边界。** ν\*、B_w、C_η 只依赖树、参考和宽度，与方法无关，所以对平面上每个点都成立。
   - 下边界以下的区域，任何方法都到达不了。
   - 一张图离下边界多远，就是它自己选择的代价。
3. **代价分解（"代价在哪、是多少"）。** 任何一张图的位置偏差都可以分成三部分：
   - 树造成的（ν\* 或 C_η）；
   - 宽度造成的（B_w − ν\*L）；
   - 布局选择造成的（实际值 − B_w）。

   下界的取值点给出"在哪"：哪个结点的哪两个兄弟子树，它们在参考方向上的范围重叠了多少。下界还给出"多少钱能消除"：合并误差达到该父间隙的一半时，这对子树就可以交错（2ε 规则）。
4. **方向也是变量。** 下界随方向变化。不同方向下必然代价可以差 2–5 倍（Tangaroa 4.70–10.14%，Cylinder 5.49–28.15%），所以画图前就可以选代价小的方向。

**不能包含的部分（如实写进局限）**

- **相对距离（SNS、TW）。** 二维到一维本身就无法保持所有距离（ST-MTM §7.2），我们的下界不量化这部分。
- **数值位移（τ）需要宽度模型。** TMTM、ST-MTM 的原生宽度语义不同（TMTM 用样本数，ST-MTM 用固定总长 K 的比例），只能在同一区间模型里比较，或者只比顺序误差。顺序误差（NROE 对 ν\*）与尺度无关，对所有方法都适用。
- **时间连贯、感知可读性。** 不在下界范围内。
- **一个方向只给一个坐标。** 要读二维位置需要两张图（x、y 各一张），每张有自己的下界。这是 RA-MTM 最初的设想，可以写进展望。

## 四、主线第五稿

> 把时变标量场压成一张静态图时，空间只能占一条轴。合并树图（TMTM、ST-MTM）在这条轴上严格保持合并树，并各自为别的目标安排位置：TMTM 为了时间连贯，ST-MTM 为了特征之间的相对距离。ST-MTM 指出，一维布局必然牺牲一些空间关系，失真是投影的必然结果，而不是某个方法的失败；但其中多少是必然的、发生在哪里，还没有人回答。我们对最直接的空间读法——沿一个固定空间方向的位置——回答这个问题：只要保持合并树，特征至少要离开它的投影位置多远？这个下限只由树和投影位置决定，画图前就能算出；它指出是哪一次合并造成了偏离，也给出要放松多少合并高度才能消除它。用它衡量现有的图，大部分位置偏差不是树造成的；用它指导构造，可以得到恰好达到下限的图。

英文：

> A static overview of a time-varying scalar field gives space a single axis. Temporal merge tree maps keep the merge tree on this axis and place features for other goals, temporal coherence or relative distances; ST-MTM notes that any such layout must distort spatial relationships, as an expected consequence of the projection rather than a failure of a method. How much distortion is expected, and where it arises, has not been answered. We answer it for the most direct spatial reading, position along a fixed direction: given the merge tree and the projected locations alone, we compute how far any topology-preserving map must move its features, which merges force it, and how much merge error releases it. Measured against these bounds, most of the positional error of existing maps is not forced by the tree, and a construction that follows them attains the bound on almost every frame.

**贡献三条**

1. A common model that places merge tree maps and other one-dimensional linearizations in one position–topology plane, measured by the merge error of the displayed profile and the displacement of features from a fixed spatial reference.
2. Lower bounds on this plane, computable from the tree and the reference alone: exact topology (closed form), finite widths, and a bounded merge error. Each bound names the merge that forces the displacement and the merge error that releases it, and splits the error of any map into a part forced by the hierarchy and a part chosen by the layout.
3. A characterization on seven sequences and the four inputs of the ST-MTM benchmark:
   - how large the forced cost is and where it arises;
   - how far existing maps exceed it;
   - how strongly it depends on the direction;
   - and a construction that attains the bound on 606 of 614 planar frames, so the bounds are tight and anchored maps carry a known error.

**AnchorMTM 的定位**：不再是"我们提出的新方法"，而是"达到下界的参照构造"，用来证明下界是紧的，并给出误差已知的锚定图。正文只占约 0.8 页，实现细节移到附录。

**标题候选**（PCS 上标题能否改需确认；如果不能改，保留现标题，只改副标题以外的内容）：

1. The Positional Cost of Topology in Temporal Merge Tree Maps（推荐）
2. How Far Must Features Move? Position Bounds for Topology-Preserving Merge Tree Maps
3. AnchorMTM: The Positional Cost of Topology in Temporal Merge Tree Maps（保留名字）

## 五、新论文结构（9 页）

| 节 | 页 | 内容 |
|---|---|---|
| 1 Introduction | 1.0 | 静态概览只有一条空间轴 → 现有图保拓扑、为别的目标排位置 → ST-MTM 承认失真必然，但多少、在哪没人回答 → 我们的问题与回答 → 发现 → 贡献 |
| 2 Related Work | 0.7 | 合并树图与地形；一维线性化与运动摘要；受约束的叶序与有保证的布局；合并树距离 |
| 3 A Common Model | 1.0 | 剖面；地图 = 叶序 + 区间 + 剖面；两种忠实度；现有方法在模型中的位置（表 1）；四叶例子（图 2） |
| 4 The Positional Cost of Topology | 1.5 | 精确拓扑（ν\*，在哪、多少）；宽度（B_w）；有界合并误差（C_η，2ε 规则）；代价分解；计算成本 |
| 5 Attaining the Bounds | 0.7 | 参照构造：从精确树出发的预算内叶序、最优屏障、有上限的放置、渲染后核验 |
| 6 Characterizing the Cost | 3.0 | 设置（所有披露集中在这里）；下界是紧的；现有图的偏差有多少是被迫的；代价在哪、放松换来多少（位置–拓扑平面）；方向的影响；读图（OLR、Storms、ST-MTM 基准表） |
| 7 Discussion and Limitations | 0.6 | 下界的用途；位置与相对距离回答不同问题；局限 |
| 8 Conclusion | 0.2 | |

## 六、图的方案（按优秀 TVCG 论文的标准：每张图只讲一句话，图注第一句就是这句话）

| 图 | 这张图要读者记住的一句话 | 内容 | 状态 |
|---|---|---|---|
| **图 1 首页** | 现有的合并树图把特征放得离它们的位置很远，其中大部分不是树造成的 | OLR 60 天：Hovmöller、TMTM 式、ST-MTM 式、锚定精确图、锚定 ε=10%，黑点是参考位置。每个面板下加一条代价条：树造成的（ν\*）和布局选择的部分 | **改造**：`fig_olr_maps.pdf` 已有，需加代价条（数据在 `orientation20261106` / 表 supp_stmtm_threshold） |
| **图 2 概念** | 代价来自一对兄弟子树在参考方向上的重叠；精确拓扑必须付一半重叠，合并误差达到半个父间隙就能免除 | 四叶例子：(a) 场与参考顺序 A C B D；(b) 树，标出冲突的结点；(c) 精确拓扑，位移 14%（点 12%）；(d) ε = h/2，位移为 0、合并误差正好为 ε | **已有**：`fig_concept_anchor.pdf`。只需把 "Exact Mode / Budgeted Mode" 改成 "exact topology / merge error ε"，在 (b) 中高亮造成代价的结点 |
| **图 3 位置–拓扑平面**（核心新图） | 每张图都是平面上的一个点；下边界以下任何方法都到不了；现有图离下边界很远，参照构造贴着它 | 七个序列各一个小面板：横轴合并误差，纵轴位移；灰色区域是下界以下的不可达区；蓝线是 AnchorMTM ε=0–50%；星是投影；方块和菱形是 TMTM 式、ST-MTM 式；叉是 Hilbert/Morton | **新做**，数据已有：`order_width20261027/*.json` 的 `width_lower_mean/max`（ε=0、2、5、10%）、`frontier20261027/*.json`（ε=0–50% 与投影）。替换 `fig_frontier_v2` |
| **图 4 代价分解** | 现有图的顺序误差中，树强加的只占一小部分 | 七个序列的堆叠柱：黑色是 ν\*，其上是 OLO、TMTM、ST-MTM 各自的超出部分，标注比例 | **已有**：`fig_compare_v2.pdf` (a)。(b)–(e) 移到附录，或缩成一行 |
| **图 5 受控实验** | 下界与穷举最优完全一致；放松恰好在半个父间隙处生效 | 四叶受控树 | **已有**：`anchor_controlled_bounds.pdf` |
| **图 6 方向** | 同一数据换个方向，必然代价可以差几倍；画图前就能选方向 | 400 个方向上的下界（球面图）+ 主要方向的柱状对比 | **已有**：`fig_direction_col.pdf` |
| **图 7 读锚定图** | 误差已知的锚定图可以读出位置：风暴沿西–东轴推进，放松只用在少数帧 | Storms 预算扫描 + TMTM/ST-MTM 同窗口 | **改造**：合作者图 6，去掉 "Improvement 1/2" 箭头；或用 Tangaroa 位置图 `fig_tangaroa_positions.pdf` |
| 表 1 | 现有方法在统一模型中的位置 | 叶序规则 / 位置含义 / 拓扑 / 宽度语义 | **新写**（文字表） |
| 表 2 | ST-MTM 自己的基准上，锚定图的位置偏差低 73–96%；ST-MTM 的邻域保持更好 | 合作者表 1 | **已有** |

可选新分析（在哪发生的定量证据）：各序列"决定下界的那次合并"的父间隙分布，也就是消除它所需的 ε。数据和代码在本机都有（`RA-MTM/data/real`、`code/data/public_scalar`、`order_certificate.py`），约半天。现在用前沿曲线的形状（深合并 vs 浅合并）和 Storms 预算只用在 31/118 帧来间接说明。

## 七、风险与时间

- 截止 11/9 AoE，相当于北京时间 11/10 晚 8 点。英文初稿今天出（`paper/pvis2027/drafts/framework_v16_en.tex`）。图 3 数据已有，约 2–3 小时；图 1 加代价条约 1–2 小时；图 2、图 7 是小改。
- **这次改的是论文的性质**：从"方法论文"改成"分析论文"，AnchorMTM 降为参照构造。合作者是底稿作者，必须先让他知道并同意。
- 摘要已提交（11/2）。PCS 是否允许改标题和摘要需要确认。
- 证据主要来自早期七序列基准（我们自己的测量，同输入），合作者四数据集只作为 ST-MTM 自己基准上的交叉验证。这一点在设置里一次说清。
