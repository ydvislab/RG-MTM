# 全文叙述重构方案（11/7 晚，待用户确认）

用户 11/7："我感觉这个论文的完整思路还是存在重大问题。没有突出我们提出方法的创新性来，插图和叙述都没有让读者很清楚的明白我们提出思想还有整个论文的贡献。……能不能帮我重新梳理一下，整篇论文按照科学可视化论文应该怎么叙述更逻辑顺畅？"

对象：`paper/pvis2027/drafts/method_anchor_figures_updated_en.tex`（v15，分支 `paper/submit-1037`）。本方案只改叙述结构和图的组织，**不改任何实验数字和协议**。

## 一、诊断：读者为什么看不出创新

1. **三个想法并列，没有主线。** 锚定（新的可视编码）、三个下界（理论）、ε（拓扑放松）在摘要和引言里各占一句。读者不知道哪个是核心，也不知道三者是什么关系。
2. **顺序倒置。**
   - 引言把下界当主要贡献，但第 4 节先讲对应、方向、问题表述、构造、QP、重建，下界放在 4.3 最后。
   - 读起来像附加分析，读者读到时已经忘了为什么需要它。
3. **核心冲突图来得太晚。** A、C、D、B 冲突图是全文最重要的想法，却出现在第 3 页、4.1 节中段一大串定义之后。
4. **首页图看不出"新在哪"。**
   - 首页图只有我们的图。纵轴标的是 "Mapped position"，恰好把核心想法（纵轴 = 空间坐标）藏了起来。
   - TMTM 也能画出看起来差不多的图，读者没有对比。
5. **图 6 把贡献讲错了。**
   - 图中 "Improvement 1: + Spatial Awareness（TMTM→ST-MTM）"、"Improvement 2: + Topology Budget（ST-MTM→Ours）" 的意思是：我们的贡献是在 ST-MTM 上加了拓扑预算，"空间感知"是 ST-MTM 已有的。
   - 真正的核心（固定的空间轴、绝对位置）反而没出现。
   - ST-MTM 的空间是相对距离，我们的是绝对位置，两者不是一回事。这是最直接误导读者的地方。
6. **实现细节淹没方法。**
   - 第 4 节一半以上是对应、Hungarian、方向符号规则、ε0、Θ0、四项 QP、栅格取整、失败报告。
   - 正文符号 20 多个：NROE、τ、ν\*、B_w、C_η、C_{w,η}、δ\*、d_top、NMLE、NPE、SNS、TW、η、ε0、β0、ρ、g、Θ0、A(S)、B(S)、ω、E∂、P0、Pη。
7. **实验按数据和协议组织，不按论点组织。** 5.2 节第一句是 "ST-MTM reports higher TW than AnchorMTM on all four inputs"，以负面结果开头。
8. **免责句分散在每段和每个图注**（"schematic"、"not author binaries"、"not a controlled comparison" 等）。审稿人读完记住的是限制，不是贡献。
9. **缺少可视化论文最关键的"读图"部分。**
   - 没有任务和需求。
   - "从图里能读出什么"只有最后两段很短的案例。
   - 可视化论文的价值首先要在图上让人看见。

## 二、全文只讲一件事

> **A merge tree map can show where features are, not only how they nest, if its vertical axis is a fixed spatial direction. The hierarchy prevents doing this exactly; we compute how much position the hierarchy costs before any map is drawn, build maps that pay little more than that cost, and let one control, a declared merge-error budget, buy position back.**

大白话：让合并树图的纵轴变成真实的空间方向，这样就能从图上读出位置和运动；树结构让这件事不能完全做到，但代价可以事先算出来；我们的方法只付这个代价，想更准就用一个公开声明的拓扑误差 ε 去换。

四部分的逻辑链：

| 问题 | 回答 | 位置 |
|---|---|---|
| 想要什么（What） | 纵轴 = 空间方向：高度读位置，斜率读运动 | 第 3 节 设计 |
| 为什么难（Why hard） | 子树必须连续，投影顺序会交错 | 第 3 节 冲突图 |
| 难到什么程度（How much） | 三个下界：只由树和参考位置决定，画图前可算 | 第 4 节 |
| 怎么做（How） | AnchorMTM：从达到下界的顺序出发，用 ε 换位置 | 第 5 节 |
| 做到了吗（Does it work） | 能读、接近下界、ε 换得值 | 第 6 节 |

### 贡献改写（三条，各对应一节）

1. **Spatially anchored merge tree maps**, a design in which the vertical axis of a temporal merge tree map is one fixed spatial direction, so a feature's height reads as its projected location and its slope as its projected velocity, with a single declared control ε for the merge-level error the map may accept (Section 3).
2. **The position price of topology**: three lower bounds on the displacement that exact topology, finite feature widths and a bounded merge error force on any such map; they need only the tree and the projected positions, so they can be evaluated before a map is drawn and used to separate forced from chosen error in existing maps (Section 4).
3. **AnchorMTM**, a construction that starts from the bound-attaining order and trades merge error for position under ε, and an evaluation showing that it meets the bound on 606 of 614 real planar frames and places features 73–96% closer to their references than TMTM and ST-MTM (Sections 5–6).

## 三、新的章节结构（正文 9 页）

| 节 | 页 | 内容 | 图表 | 材料来源 |
|---|---|---|---|---|
| 1 Introduction | 1.0 | 任务 → 现有图的缺口 → 想法与障碍 → 关键洞见（代价可算）→ 结果 → 贡献 | 图 1（首页对比） | 重写 |
| 2 Related Work | 0.6 | 三组：空间时序概览；合并树图与地形；受约束的叶序和布局。每组最后一句写差别 | — | 现 §2 压缩 |
| 3 Spatially Anchored Merge Tree Maps | 1.2 | 3.1 合并树图背景（压缩）；3.2 任务与需求；3.3 把纵轴固定为空间方向；3.4 冲突与问题表述 | 图 2（概念图，贯穿全文的四叶例子） | 现 §3、§4.1 |
| 4 The Position Price of Topology | 1.2 | 4.1 精确拓扑（ν\*，中点顺序最优）；4.2 有宽度（B_w 只给结论和直观解释）；4.3 有预算（2ε 规则）；4.4 下界的用途 | — | 现 §4.3 |
| 5 AnchorMTM | 1.2 | 总览图；5.1 预算内的叶序（从中点顺序出发，最优屏障命题）；5.2 锚点放置；5.3 重建与核验 | 图 3（框架图简化） | 现 §4.1 后半、§4.2 |
| 6 Results | 3.0 | 6.1 设置（所有披露集中在这里）；6.2 位置变得可读；6.3 代价有多大：下界的准确性；6.4 ε 换来什么；6.5 三维数据与开销 | 图 4 Storms、表 1、图 5 受控、图 6 Ring | 现 §5 重排 |
| 7 Discussion and Limitations | 0.6 | 下界的用途；锚定与邻域保持回答不同问题；局限（集中写一次） | — | 现 §6 |
| 8 Conclusion | 0.2 | — | — | 重写 |

### 第 3 节的新内容：任务与需求（可视化论文必须有，现在没有）

- **T1** 识别特征及其嵌套（合并层次）：合并树图本来就能做。
- **T2** 在任一时刻读出特征沿选定空间方向的位置。
- **T3** 跟踪运动：沿该方向的方向和快慢，以及不同特征之间的比较。
- **R1 拓扑**：显示的合并层次等于树，或者偏差不超过声明的 ε。
- **R2 位置**：锚点靠近投影位置；所有帧用同一条轴，不逐帧平移或缩放。
- **R3 运动**：相邻帧的锚点位移跟随投影位移。
- **R4 可读**：每个特征保留与其大小成比例的可见区间，互不重叠。

接着用一句话点出：**R1 和 R2 冲突**（图 2）。由此得到问题表述：在合并误差 ≤ ε 的条件下最小化最坏位移，只需一个公式。这样后面的下界和构造都是在回答这个问题。

### 第 6 节按论点组织（每个论点"先给图，再给数"）

| 小节 | 论点 | 证据 |
|---|---|---|
| 6.2 Position becomes readable | 锚定后，高度就是位置，斜率就是运动；TMTM 和 ST-MTM 读不出 | Storms 三方法同窗口对比（图 4）；表 1 的 NPE（低 73–96% / 77–98%）；Hilbert/Morton；ST-MTM 的 TW 更高放在最后并解释原因（任务不同） |
| 6.3 How large is the price | 下界在受控树上等于穷举最优；真实帧上所选顺序达到下界；现有图的大部分顺序误差不是树造成的 | 图 5；606/614；31–95% |
| 6.4 What ε buys | ε 用公开声明的合并误差换位置；每张图都在预算内；并非每个指标都改善 | Exact 对 Balanced（16.2/11.6/64.9%）；Storms ε 扫描；Ring |
| 6.5 Volumes and cost | 三维也成立，但参数是逐个选的（如实写） | 体数据表；运行时间一句话 |

两套基准在 6.1 开头一次说清：**基准 A**（ST-MTM 的四个平面输入 + 两个体数据）用于方法比较；**基准 B**（早期七序列）用于下界分析。

## 四、图的方案

| 新编号 | 内容 | 要传达的一句话 | 来源 | 工作量 |
|---|---|---|---|---|
| 图 1（首页） | 同一个风暴、同一时间窗，TMTM / ST-MTM / AnchorMTM 三张图并排，上面配空间快照；我们的纵轴标物理方向（如 "west → east"，需核对 Storms 的 a\*） | "在别人的图里风暴是一条平线，在我们的图里它的高度就是位置、斜率就是速度" | 现图 1 + 图 6 的 TMTM/ST-MTM 局部面板（都有 PPT） | 中（组合面板，约半天） |
| 图 2（概念图） | (a) 特征与参考方向，投影顺序 A C B D；(b) 树要求 (A B)(C D) 连续；(c) 精确模式必须位移 14%，即下界；(d) ε = 半个父间隙时位移为 0，合并误差正好等于 ε | 整篇论文的想法浓缩在一张图里 | v12 现成的 `paper/anchor_full/figures/fig_concept_anchor.pdf`（就是第 6.3 节受控实验的那棵树，数字一致） | 低（已有）。替换现在的图 3、4、5 三张机制图，省出约 1/3 栏 |
| 图 3（框架） | 三步：参考 → 预算内叶序 → 放置与重建 | 方法怎么走 | 现图 2 简化（去掉 QP 四项名称等细节） | 低到中（PPT） |
| 图 4（Storms） | ε 扫描 + TMTM/ST-MTM | ε 换位置；别人的图读不出位置 | 现图 6，**去掉 "Improvement 1/2" 箭头**，改成按行标注 | 低（PPT） |
| 图 5（受控） | 现图 8 | 下界准确 | 已有 | 无 |
| 图 6（Ring） | 现图 7 | 扩张读作展开 | 已有 | 无 |

移到附录：算法 1、参数与运行时间表、体数据参数表、对应关系与方向估计的细节。这些移走大约能省出 1 栏，用来写任务与需求和读图段落。

全文用同一个四叶例子：引言（图 2）→ 第 4 节下界的直观解释 → 第 6.3 节受控实验。现在的文字用 A、C、D、B，v12 概念图用 A、C、B、D（与受控实验一致）；采用概念图后，文字统一改为 A、C、B、D。

## 五、写法规则

1. 每段第一句是结论，后面才是证据。
2. 免责只出现两次：6.1 设置一段、第 7 节局限一段。图注只写读图需要的信息。
3. 正文符号精简：保留 q、x、ε、δ\*、τ、ν\*、B_w、C_η、NPE、SNS、TW；A(S)、B(S)、ω、E∂、P0、Pη、Θ0、β0、ε0 移到附录。定理 2 用文字加一个式子陈述。
4. 负面结果放在正面结果之后，并给出原因。例如："ST-MTM's higher TW reflects a different goal: it preserves neighborhoods, we preserve positions."

## 六、引言骨架（英文主题句）

- **P1 任务**：Analysts who follow storms or fires through a time-varying field ask three questions at once: which features exist and how they nest, where they are, and how they move.
- **P2 缺口**：Temporal merge tree maps answer the first question but not the other two: their vertical axis is a layout coordinate chosen for the tree, so a storm that travels east can stay level on the map (Fig. 1). Hovmöller diagrams keep a physical axis but average away the hierarchy.
- **P3 想法与障碍**：We fix the vertical axis to one spatial direction, so height reads as projected location and slope as projected velocity. The merge tree resists: it keeps every subtree in one block, while the projections of sibling subtrees can interleave (Fig. 2).
- **P4 关键洞见**：This conflict has a computable price. From the tree and the projected positions alone, we derive the smallest displacement any exact-topology map must accept, and how far a declared merge-error budget ε lowers it.
- **P5 方法与结果**：AnchorMTM builds maps that pay little more than this price …（数字沿用 v15）。
- **贡献三条**（见第二部分）。

## 七、风险与时间

- 现在到 11/9 AoE 约两天。
- **文字重构约 1 天**：换序、新写第 3 节需求和问题表述、重写引言、压缩第 5 节、按论点重排第 6 节、集中免责。数字全部沿用，主要是移动和改写已有内容。
- **图**：
  - 概念图现成。
  - 图 6 去掉箭头是 PPT 小改。
  - 首页三方法对比图约半天。
  - 如果时间不够，首页图先只改纵轴标签，加一个 TMTM 小图。
- **合作者**：他是底稿作者，结构大改需要他知道。建议把本笔记第一到四部分先发给他，或者先在分支上改好再给他看。
- **标题和摘要**：摘要 11/2 已提交。PCS 通常允许截止前修改摘要，标题能否改要在 PCS 上确认。建议标题不变。

## 八、确认后的执行顺序

1. 新建第 3 节：需求、概念图、问题表述。下界提前为第 4 节。
2. 重写引言和贡献。
3. 压缩第 5 节，实现细节移到附录。
4. 按论点重排第 6 节，免责集中到 6.1 和第 7 节。
5. 图：概念图替换三张机制图；图 6 去掉 "Improvement" 箭头；首页对比图。
6. 页数检查、编译、附录同步、中文版同步。
