# 叙事调整与合作者新指标（2026-11-05，方案，待用户确认）

## 用户要求

论文只讲我们自己的方法 AnchorMTM；TMTM、ST-MTM 只在实验对比时作为别人的方法出现，不再写成我们框架的"特例"。同时看合作者 11/4–11/5 更新的评价指标，决定如何放进论文。

## 现状：TMTM/ST-MTM 在正文中被写进框架的地方

| 位置 | 现在的写法 |
|---|---|
| 摘要第 2 句 | "We formulate merge tree maps as one constrained layout problem …; TMTM and ST-MTM are exact-topology instances." |
| 贡献 1 | "… of which TMTM, ST-MTM, the reference projection and AnchorMTM are instances." |
| 第 4 节开头、4.1 节 | Eq. general 含 TMTM 的 E_O 和 ST-MTM 的 E_W；表 1 "Merge tree maps as instances of Eq. general" |
| 4.4 节 Scope 段 | "hence for TMTM and ST-MTM" |
| 5.3 节 | 标题 "Most Displacement of Existing Maps Is Avoidable"；"Because TMTM and ST-MTM are exact-topology instances …"；图 4 标题 "Instances of Eq. general" |
| 讨论第 1 段 | "One formulation for merge tree maps" |
| 结论 | "Because existing merge tree maps are instances of the same formulation, the bounds measure them too" |

## 调整方案

- 问题表述只写 AnchorMTM 自己的：参考、合并值容许量 η、位置上限、目标（即现有 Eq. qp 的四项）。去掉 E_O、E_W 和表 1（实例表），省出约 1/4 栏。
- 三个界保留"只依赖约束"这一性质，但只在实验中用一句话说明：因此也能用来衡量对比方法的地图。
- 实验 5.1 新增 "Compared methods"：TMTM（官方实现输出）、ST-MTM（按论文重新实现，统一参数，见 S10）、参考投影（作为不保拓扑的参照）。
- 5.3 改为"与已有合并树图的比较"，结论顺序改为：精确模式贴近下界 → 对比方法有 54–95% 的顺序误差高于下界。
- 讨论第 1 段改为"界的用途"（选参考、判断余量），不再说"统一表述"。
- 结论同步。中文版同步。

## 合作者的新评估（`paper/pvis2027/experiments_ratio_p_20261104`、`section5_revision_20261105`、`space_filling_baselines_20261105`）

- 数据：ST-MTM 论文的四组（Gaussian、Ring、Wildfires、Storms 744 帧），按重建的预处理。
- 指标：SNS、TW（k=1,3,5,3，要求 0<k<n/2）、NPE（每帧最坏 |x−q|/L 的时间平均）、TD。
- 方法：Hilbert、Morton（默认方向）、TMTM、ST-MTM（SNS/TW 直接引用 ST-MTM 论文表 1，NPE 本地测）、AnchorMTM Exact 和 Balanced（ε 由前 1/4 帧验证选出）。

### 评估意见

1. **NPE 可以直接采用**：我们 Storms 案例里的 37.3 / 50.7 / 5.1 / 2.7 就是 NPE，只是没命名。
2. **Hilbert / Morton 有价值**：能回答"为什么不直接用空间填充曲线"。但合作者的数是在他们重建的四组输入上，和我们的七组不是同一输入。
3. **引用 ST-MTM 已发表的 SNS/TW 有公平性问题**：合作者表中"Balanced 的 SNS 在四组上都低于 ST-MTM"是拿本地值和别人输入上的已发表值比。在我们同一输入的测量中，ST-MTM（重新实现）在 7 组中 5 组 SNS 最好、7 组 TW 都最好（如 Storms SNS 0.030，AnchorMTM 约 0.11）。两者放进同一篇论文会自相矛盾，审稿人容易发现。
4. **TW 覆盖太少**：k=(1,3,5,3) 时 Ring、Wildfires、Storms 只有 1/40、4/32、11/744 帧有效；我们 k=1 的覆盖为 27/32、30/30、88/115 等。
5. **Balanced 的 ε 选择规则**（J=0.5 NPE+0.5 SNS）引入一个打分规则；我们的权衡曲线已经给出全部预算。

### 两版分叉

合作者的 pvis2027 版（四组、Hilbert/Morton、已发表值、Balanced）和我们的 anchor_full 版（七组、界的评估、权衡曲线）现在评估部分不同，11/9 只能交一版，需要和合作者商定。
