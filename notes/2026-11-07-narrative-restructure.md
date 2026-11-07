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

## 二、主线（11/8 第二稿，替换第一稿）

用户 11/8："感觉你的主线说的不是很流畅……大概意思是对的，但是讲的不通顺，需要把主线说清楚之后再改。"

第一稿的问题：几句话之间没有因果衔接。"树结构让这件事不能完全做到"没有说为什么；"代价可以事先算出来"没有说算它有什么用；ε 和锚定、下界并列出现，看不出它是在回答哪个问题。第二稿改为一条问答链：每一步都是上一步自然引出的问题。

### 两句话版

> 现有的合并树图能看出特征怎样嵌套，却看不出它们在哪里、往哪走。我们把图的纵轴固定为一个空间方向，让每个特征尽量靠近它沿该方向的真实位置；保持合并树时偏离不可避免，我们算出它的下限，并给出一个方法：以严格保持合并树为起点，把偏离压到这个下限附近，再只在能减少偏离的地方、用不超过 ε 的合并误差换取更小的偏离。

> Temporal merge tree maps show how features nest, but not where they are or where they move. We fix the map's vertical axis to a spatial direction and place each feature as close to its location along it as the merge tree allows; we prove how close that is, and AnchorMTM starts from the exact tree, comes close to this bound, and relaxes the tree only where a merge error of at most ε reduces the displacement.

### 问答链（全文的骨架）

| 步 | 读者此时的问题 | 回答 | 位置 |
|---|---|---|---|
| 1 | 分析风暴、火点这类时变场时想看什么？ | 一张图里同时看到：有哪些特征、怎样嵌套；它们在哪里、往哪走 | 引言 P1 |
| 2 | 现有方法缺什么？ | 合并树图把每帧的树画成一条剖面、按时间排开，嵌套看得很清楚；但剖面上的位置是为排版服务的，不对应任何空间方向。向东移动的风暴在图上可以是一条平线 | 引言 P2，图 1 |
| 3 | 我们怎么做？ | 把这条轴固定为一个空间方向（由特征运动估计，或由用户指定），每个特征画在尽量靠近它投影位置的地方。高度近似位置，轨迹走向反映沿该方向的运动。位置是近似的，但每帧最坏偏离有上限（τ+β0）并随图报告：四个数据上平均为全域的 0.9–4.7%（精确模式），TMTM、ST-MTM 为 11–58% | 引言 P3，第 3 节 |
| 4 | 为什么不能直接这样画？ | 合并树要求同一子树的特征挨在一起，否则合并层次会画错；按空间排序时，不同子树的特征可能交错。例：A、B 同属一棵子树，C、D 属于另一棵，从西到东却是 A、C、B、D。要保持层次，就必须把 B 或 C 挪离真实位置 | 引言 P3，图 2(a–c)，第 3 节 |
| 5 | 那偏离是谁造成的？ | 读者看到一个特征偏离了位置，需要知道这是树逼出来的，还是算法做得不好。我们证明：只看树和投影位置，就能算出保持层次时最坏偏离的下限（考虑特征宽度后也能算）。它不依赖任何画法，所以画图前就能算，也能用来检查别人的图 | 引言 P4，第 4 节 |
| 6 | 我们的方法离这个下限多远？ | 精确模式严格保持合并树（实测合并矩阵误差 0），从达到点模型下限的中点叶序出发，再处理宽度和时间连贯。在 614 个真实平面帧中，有 606 帧恰好达到下限 | 第 5 节，6.3 |
| 7 | 下限本身太大怎么办？ | 以严格的合并树为起点放松：精确树始终是候选；只释放造成偏离的那对兄弟子树（或压平高度差不超过 2ε 的父子间隙）；每个放松后的叶序都按原始合并树计算误差，超过 ε 的淘汰，剩下的选偏离最小的。所以放松只在能减少偏离时发生，显示的合并高度偏离原树不超过 ε（实测 0、0.98%、4.42%、9.99%） | 图 2(d)，4.3，5.1，6.4 |
| 8 | 实际效果如何？代价是什么？ | 在 ST-MTM 的四个平面数据上，位置误差比 TMTM、ST-MTM 低 73–96%（ε=0）；在早期七序列基准上，它们的顺序误差有 31–95% 不是树逼出来的。代价：ST-MTM 保持邻域关系更好，因为它优化的是相对距离，我们优化的是绝对位置 | 6.2，6.3，第 7 节 |

与第一稿相比：

1. 加了第 5 步"偏离是谁造成的"。这一步说明了为什么要证明下界，第一稿缺这一环。
2. ε 从和锚定、下界并列，改为第 7 步：在下界之后，作为"下限太大怎么办"的回答出现。

### 贡献（按问答链的顺序）

1. **一种新的图**：合并树图的纵轴是固定的空间方向，特征的高度近似它沿该方向的位置，最坏偏离有上限并随图报告（第 3 节）。
2. **偏离的下界**：保持层次、或允许 ε 合并误差时，特征至少要偏离多远。下界只依赖树和投影位置，能把树逼出的偏离与布局造成的偏离分开（第 4 节）。
3. **AnchorMTM 及其验证**：保持层次时达到下界（606/614 帧），用 ε 换取位置；与 TMTM、ST-MTM 比较（第 5–6 节）。

English:

1. A spatially anchored merge tree map, whose vertical axis is one fixed spatial direction, so that a feature's height approximates its location along that direction, with a per-frame worst deviation that is bounded and reported (Section 3).
2. Lower bounds on how far features must leave their locations when the map keeps the merge tree exactly or within a merge-error budget ε; they depend only on the tree and the projected locations, so they separate displacement forced by the hierarchy from displacement caused by the layout (Section 4).
3. AnchorMTM, which keeps the merge tree exactly and attains the exact-topology bound on 606 of 614 real planar frames, and relaxes the tree only where a merge error of at most ε reduces displacement, with an evaluation against TMTM and ST-MTM (Sections 5–6).

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

## 六、引言骨架（英文主题句，按第二部分问答链 1–8）

- **P1（步 1）**：Analysts who follow storms or fires through a time-varying field want one picture of which features exist, how they nest, where they are and where they move.
- **P2（步 2）**：Temporal merge tree maps show the nesting well, but their vertical axis serves the layout and has no spatial meaning, so a storm that travels east can appear as a level band (Fig. 1). Hovmöller diagrams keep a spatial axis but average the hierarchy away.
- **P3（步 3–4）**：We fix the vertical axis to one spatial direction, so a feature's height is its location and the slope of its track is its speed. The merge tree resists: features of one subtree must stay together, yet along the direction they can interleave with another subtree (Fig. 2), so some features must leave their locations.
- **P4（步 5–7）**：A reader who sees a displaced feature needs to know whether the hierarchy forced it. We show that the tree and the projected locations alone determine the smallest worst displacement of any exact-topology map, and how far a merge-error budget ε lowers it.
- **P5（步 6、8）**：AnchorMTM meets this bound on 606 of 614 real planar frames … ST-MTM preserves neighborhoods better（数字沿用 v15）。
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

## 九、11/8 用户追问与修正（主线第三稿）

用户："我们的方法能让位置和运动可以直接读出？不是有误差吗？我们的方法是不是也是近似值？我们的方法是不是严格遵循了拓扑结构再进行的放松？"

1. **位置是近似的。** "直接读出"说过头了，改为"近似，误差有上限并随图报告"。依据：
   - 放置有上限 ‖x−q‖∞ ≤ τ(π)+β0。
   - 主表 NPE（每帧最坏偏离 / 全域长度，取平均）：精确模式 0.89%、4.71%、1.31%、3.99%；Balanced 0.89%、3.95%、1.16%、1.40%；TMTM 11.2–57.5%，ST-MTM 11.5–45.8%。
   - 卖点从"能直接读出"改为：TMTM 的轴没有空间含义，位置误差无从谈起；我们的轴有固定含义，偏离有界、已知，并且接近树允许的最小值。
2. **运动没有单独度量。** 合作者的主表里没有运动误差。早期基准（anchor_full）里有，结果是多数序列明显更低，但不是全部。正文只能说"轨迹走向反映沿该方向的运动"，不能说"斜率就是速度"。
3. **放松以严格拓扑为起点。** 核对合作者代码 `code/src/rgmtm/order_certificate.py` 的 `budget_order`、`selective_order`，以及 `interval_order.py` 的 `width_order`：
   - 精确树始终是候选，注释写明 "the exact tree, which always qualifies"。
   - 阈值放松：把高度差 ≤2ε 的父子间隙压平。
   - 选择性放松：从精确树出发，每次只释放造成最大偏离的那对兄弟子树，并要求满足 2ε 链条件。
   - 宽度细化：保留的结构总包括精确树。
   - 所有候选都按原始合并矩阵计算 δ\*，超过 ε 的淘汰，按 (τ, NROE) 选最小。
   - 这不是"先画严格的图再修改"，而是逐帧在同一组候选里选；概念上可以讲成"以严格拓扑为起点，按需、有上限地放松"。
   - 放松不会让所选叶序的 τ 比精确树更差（精确树在候选中）。但最终 QP 有 β0 余量和其他目标项，所以不是每个指标都改善：Gaussian 不变，Wildfires 的 SNS 上升。
