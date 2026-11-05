# 11/5 晚：叙事调整 + Codex 第 2 轮修改（已执行）

用户 11/5 晚确认："都按你推荐的改，用 31–95%，中文同步。另外看一下最新的 github 进展。"

本文件记录做了什么、新算的数字和合作者 GitHub 的最新进展。方案见 `2026-11-05-reframing-and-metrics.md`，评审见 `2026-11-05-codex-review-run02.md`。

## 一、决定

| 项 | 决定 |
|---|---|
| 可避免比例口径 | **严格口径**：TMTM、ST-MTM 严格保树，用定理 1 的 ν\* 衡量；精确模式保留 ε0=1e-7 的数值允许量，用新记号 c0 = C_η(η=ε0ΔF) 衡量。两者只在 Cylinder 上不同（12.24% 对 8.01%）。摘要、5.3、结论改为 **TMTM 54–95%、ST-MTM 31–95%**（合称 31–95%） |
| (a) 叙事 | TMTM、ST-MTM 只作为对比方法出现，不再写成统一式的"特例"。删去式 general（含 E_O、E_W）和表 1（实例表） |
| (b) NPE | 采用。定义为"每帧最大 \|x−q\|/L 对各帧的平均"，用于 Storms 案例 |
| (c) Hilbert/Morton | 在我们的五个平面序列上重算（同一输入），正文 5.3 一句话 + 附录 S10 新表 |
| (d) ST-MTM 已发表的 SNS/TW | 不用。附录 S10 说明理由：输入不同，不能与本地测量值并列 |
| 同模型基线命名 | "TMTM objective / ST-MTM objective" 改为 **TMTM-style / ST-MTM-style**，并在 5.1 写明它们只是仿照两种方法的目标（时间对齐；质心距离 + 时间对齐），不复现原方法。依据：`code/experiments/unified/README.md` 写明是 "TMTM-inspired / ST-MTM-inspired" 代理 |

## 二、正文修改（main.tex，中文 main_zh.tex 同步）

- 摘要：删去"统一表述、TMTM/ST-MTM 为特例"；界"只依赖布局约束，与算法无关"；结论顺序改为"精确模式贴近下界 → TMTM/ST-MTM 31–95% 高于下界，不改变树也可避免"。
- 首页图注：加一句"纵轴是归一化参考坐标，不是经度"。
- 贡献 1：改为空间锚定合并树图的层次约束区间布局表述（参考、合并值容许量、位置上限），不再说统一已有方法。贡献 3：界对满足约束的所有布局成立；精确模式贴近界，TMTM/ST-MTM 大部分误差高于界。
- 4.1 改名"Layout Model and Fidelity Measures"。用"可接受的地图"定义替换式 general 和表 1：区间在 L(π) 中、ψ(x_i)=V_ii、d_top(ψ,T)≤η（Codex 问题 4）。
- Exact Mode 定义统一（Codex 问题 5）：4.1 写明 ε0 只处理近乎并列的鞍点，严格精确拓扑为 η=0；4.3.1 写"精确模式取 ε=0，只保留 η=ε0ΔF，平面序列上渲染合并误差为零"。
- 定理 3 后的错误说法（"至少与展平证书一样强"）改为：两个证书互不占优，报告两者较大者（与代码 `interval_order.py:161` 一致）（Codex 问题 2）。
- Scope 段改为只依赖可接受性，不提 TMTM/ST-MTM。
- 5.1 "Instances" 改为 "Compared methods"：TMTM（官方实现移植，平面序列 3127 个弧区间和锚点一致）、ST-MTM（按描述实现，KKT 残差 <1e-6，统一参数）、投影、TMTM-style/ST-MTM-style 目标（只用于图 5、图 6 和 Storms 案例）、Hilbert/Morton（Codex 问题 3、7）。
- 5.1 Measures：加 NPE；ν\* 与 c0 分开（Codex 问题 1）。
- 5.2：C 项改为"所选叶序的 τ 在每个测试的预算下达到宽度界"；"余量在下界一侧"改为"不能区分下界余量和搜索不足"。
- 5.3 改名 "Comparison with Existing Merge Tree Maps"，加 Hilbert/Morton 句；"沿参考移动的特征在图上也移动"改为"运动项鼓励显示运动跟随投影运动"；SNS/TW 段补一句曲线在每个平面序列上两项都不如 ST-MTM。
- 图 4 图注改为"原生输出"，黑色部分写明 ν\* 与 c0。图 5、图 6 图注和正文改为 -style。
- 5.6 方向研究：ν\* 改为 c0（这里比较的是 ε0 下的界）。
- 讨论第 1 段 "One formulation" 改为 "What the bounds are for"。"Stable is not faithful" 里 TD/ME 是原生输出，去掉 "objectives"。持续性简化阈值 2ε 改为 2η。局限段写明是"点模型阶段"与穷举一致。
- 结论同步 31–95%。
- 删去 4.4 两处重复句，放宽 `\dbltopfraction` 到 0.85（不改字号和页边距）。

## 三、附录（supplement.tex）

- S1：精确模式与严格精确的关系；原 "ME 是 RMS 残差" 改名为 motion residual，并注明不同于正文的事件 ME（Codex 问题 6）。
- S5：展平证书与链式证书互不占优，附两叶反例，报告较大者。
- S10：标题改为 Method Comparison；TMTM 移植的验证说明（体数据 TMTM 用另一个简化实现，未与官方核心比较）；不引用 ST-MTM 已发表 SNS/TW 的理由；新增 Hilbert/Morton 段和表 S4。表 S1 增加 ν\* 与 c0 两列。
- S11：写明 TMTM-style / ST-MTM-style 的具体设置（权重、无参考项、无上限）以及它们不是原方法。
- S12：steps 改为 frames，NPE。
- S13：去掉"上界"说法；未分辨的情况补上"被更近的相邻极小值先匹配"（与 B 项一致）。
- S14：图和图注 ν\* 改为 c0。
- S16 表注：TMTM/ST-MTM 用严格 ν\*（Cylinder 可避免 54%、31%），精确模式用 c0。

## 四、Hilbert/Morton（新算，同一输入）

脚本 `paper/anchor_full/figure_drafts/space_filling_baselines.py`，输出 `figdata/space_filling20261105/metrics.json`。方法：每个极值落到覆盖全序列极值的最小 2 的幂方格的单位网格中，用曲线序号作显示坐标；对八种轴对齐朝向取平均。δ\* 是该叶序下任何剖面的最小合并误差（命题 1），对曲线有利。

| 序列 | 曲线 | NROE % | δ\* 最坏 % | δ\* 平均 % | SNS | TW |
|---|---|---:|---:|---:|---:|---:|
| Storms | Hilbert / Morton | 18.2 / 17.9 | 36.5 / 38.6 | 3.0 / 2.9 | 0.142 / 0.144 | 0.71 / 0.70 |
| Wildfires | | 23.4 / 21.3 | 32.3 / 31.9 | 5.9 / 7.1 | 0.200 / 0.188 | 0.89 / 0.86 |
| OLR | | 18.4 / 17.8 | 21.5 / 20.5 | 2.4 / 2.2 | 0.101 / 0.088 | 0.85 / 0.86 |
| PM2.5 | | 8.6 / 8.6 | 19.2 / 20.0 | 0.3 / 0.3 | 0.072 / 0.078 | 0.70 / 0.67 |
| Ring | | 8.6 / 8.3 | 33.9 / 34.5 | 5.5 / 6.0 | 0.167 / 0.160 | 0.85 / 0.75 |

对照（NROE %，TMTM / ST-MTM / 精确模式）：Storms 19.2/16.3/3.8，Wildfires 29.3/24.0/5.8，OLR 19.3/17.2/0.9，PM2.5 12.9/11.6/1.0，Ring 7.2/10.4/2.7。结论：曲线的顺序误差与 TMTM/ST-MTM 同量级，最坏合并误差 19–39%，SNS/TW 在每个序列上都不如 ST-MTM。与精确模式相比，曲线并非处处更差：TW 在 Wildfires（0.89 对 0.88）和 Ring（0.85 对 0.69）上 Hilbert 更高，Ring 上 Morton 的 SNS 略低（0.160 对 0.164）。正文没有声称曲线在距离指标上不如 AnchorMTM。

## 五、严格口径下的可避免比例

| | Storms | Wildfires | OLR | PM2.5 | Ring | Tangaroa | Cylinder |
|---|---:|---:|---:|---:|---:|---:|---:|
| TMTM | 80 | 80 | 95 | 92 | 63 | 54 | 54 |
| ST-MTM | 77 | 76 | 95 | 92 | 74 | 57 | 31 |

## 六、图与排版

- 图 4（严格 ν\*/c0）、图 3、图 5、图 6、S14 方向图、S12 Storms 图重新生成；最小字号从约 4.6–5 pt 提到约 5.5–6 pt。
- 英文：共 10 页，正文结束于第 9 页（`\label{body:end}` 检查），参考文献从第 9 页右栏开始。附录 16 页，中文 17 页。
- Overleaf 包 `paper/anchor_full_overleaf.zip` 已更新（38 个文件），解压后从零编译通过。
- 新 PDF：`paper/anchor_full/AnchorMTM_draft_v7_en.pdf`、`AnchorMTM_draft_v7_zh.pdf`、`AnchorMTM_supplement_v2.pdf`。

## 七、合作者 GitHub 11/5 新进展（upstream 到 a092db8，只读未合并）

1. **2b65826（16:27）五数据集预算曲线**：Storms、Wildfires、Ring（他们重建的输入）加 Tangaroa、Cylinder，画 E_inf/E_pool 对渲染最坏 NMLE，共 59 个配置。Ring 补到 100% 预算，枚举出释放阈值 62.0013877%。体数据 1,515 列逐列复核，无预算超限。Gaussian 不画。
2. **d76bb9e（17:59）**：新 Fig 6（744 帧定性 Storms 档案，0/2/5/10/20% 预算的同帧剖面与事件图）；Fig 7–8 改为只画 NROE 和 NMLE（去掉事件 ME），附 CSV（`order_scalar_budget_20261105/metrics.csv`）；Fig 9 Cylinder 中心树变体（探索性，轴不是物理 x）。
3. **a092db8（21:52）**：Fig 2 完整方法框架图（双栏，第 3 页），可编辑 PPT。
4. 他们的 README 写"PDF 共 11 页（含参考文献），最后一张 Cylinder 图在第 10 页"。如果第 10 页的图属于正文，**正文已超过 9 页**，需要提醒。
5. 他们的数和我们一致的地方：Cylinder ε=0 的 NROE 均值为 0.0801，即我们的 c0。他们的图 7–8 只用 NROE/NMLE，与我们的指标一致。

**两版仍未统一**：合作者 `pvis2027` 用 ST-MTM 论文的四组重建输入、Balanced 自动选预算、引用已发表 SNS/TW；我们 `anchor_full` 用七组同一输入、三个下界、严格 ν\*、不引用已发表值。他们的新框架图（Fig 2）和 Storms 预算剖面图（Fig 6）可以考虑并入我们的版本，但页数已满（我们第 9 页无余量），需要删减才能放。

## 八、待办

- 与合作者商定交哪一版（11/9 AoE 截止）。
- 向合作者要 PCS 投稿号填 `\onlineid{0}`；告知 Cylinder 的 ν\*/c0 处理和 31–95%。
- 11/8 终检：中英文一致、页数、Overleaf 包、匿名性。
