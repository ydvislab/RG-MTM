# 正文数字核对（2026-11-05）

范围：摘要、贡献、第 4 节概念图、第 5–7 节中所有带数字的陈述（约 65 条）。逐条用保存的结果重新计算，不依赖论文旧稿。路径相对 `RG-MTM/`；`figdata/` 指 `paper/anchor_full/figdata/`。

## 结论

- 绝大多数数字与记录一致。
- **需要改的 6 处**（见下表），其中 2 处是数字错误，4 处是措辞超出了记录支持的范围。
- **需要补的 1 处披露**：ST-MTM 的参数是统一参数，不是原论文逐数据集的参数。合作者的核验报告明确要求这样标注，但正文和附录都没有写。

## 需要修改的地方

| # | 位置 | 原文 | 记录显示 | 建议改法 |
|---|---|---|---|---|
| A | 5.6 方向实验 | "only 3 of the 400 sampled directions have a higher bound" | 有 4 个方向更高（`reference_direction20261027/tangaroa.json` 的 `stored_nu_rank`=396，`bound_allowance20261105` 同） | 改为 4。合作者 10/30 原稿就是 3，是沿用下来的计数错误。中文版同改 |
| B | 5.5 OLR 案例 | "Exact Mode shows 94% (97%) of the minima at their exact values" | 2% 内有凹槽的是 94.3%，5% 内是 96.6%；但其中有 4 个（5% 时 9 个）匹配到的是相邻极小值的凹槽（两个靠近的极小值互换）。真正以精确值显示的是 92.8%（2%）和 93.2%（5%） | "Exact Mode has a dip within 2% (5%) of the reference for 94% (97%) of the minima; 93% are shown at their exact values, and the rest are displaced by more than 2%" |
| C | 5.2 真实树 | "The width bound is attained on most planar frames and on the worst Tangaroa and Cylinder frames" | Cylinder 最坏帧在 ε=0/2/5/10% 都达到；Tangaroa 只有 ε=2% 达到（ε=0：14.27 对 13.74；5%：13.40 对 12.77；10%：12.24 对 12.10）（`code/results/order_width20261027/*.json`） | "…on most planar frames and on the worst Cylinder frame at every budget, but not uniformly: on Tangaroa the worst frame meets it only at ε=2%, on Wildfires at ε>0 …" |
| D | 5.4 权衡 | "whereas no point of the AnchorMTM curves exceeds 27% and 4.2%" | 只对平面数据成立（最坏 26.19%、平均 4.19%）；图 5 也画了 Cylinder，其平均位移最高 5.01%，最坏 27.00% | "…whereas on these sequences no point of the AnchorMTM curves exceeds 26.2% and 4.2%" |
| E | 5.6 运行与覆盖 | "On all 637 frames with at most eight leaves, the selected order equals the exhaustive optimum at nine budgets" | 637 帧、9 个预算都对，但比较的是**点模型叶序的 NROE 最优**（`order_budget20261027` 的 `enumerated_frames_optimal`）。算法 1 最终按 τ 选叶序（Tangaroa 上最终 NROE 9.67% 高于 ν\*） | "…the point-model order search attains the exhaustive NROE optimum at nine budgets…"；局限段"it matched exhaustive enumeration"同样加"in NROE" |
| F | 5.1 数据 | "on Storms the estimated direction lies within 1.1° of west–east" | 记录为 −1.108°（`code/results/framework20261025/era5.json`），严格说比 1.1° 大 | "lies 1.1° from west–east" |

**需要补的披露（G）**：ST-MTM 在本文中用的是统一协议参数（W uniform、r=0.95、λ=0.5，K 由画布确定），而原论文对 Storms 用的是 inverse / K=135 / r=0.65 / λ=0.05，对 Wildfires 用的是 K=10 / r=0.85（`code/results/baseline_audit_20261019/REPORT_zh.md`）。合作者的报告写明比较应标注为 "ST-MTM reimplementation under the shared-input protocol"。建议在 5.1 Instances 加半句话，并在附录 S10 前加一段参数表。

## 已核对一致的数字（按出现顺序）

| 陈述 | 记录值 | 来源 |
|---|---|---|
| 917 帧；各数据帧数和叶子数范围（表 2） | 118/30/60/366/40/201/102；1–8, 6–11, 2–8, 1–7, 1–7, 18–93, 4–75 | `figdata/order_budget20261027/*.json` |
| 54–95%（摘要、结论）；TMTM 54–95%、ST-MTM 55–95% | TMTM 54.0–95.4；ST-MTM 54.9–94.8 | 同上 + `figdata/stmtm_completion20261026/unified_metrics.csv` |
| Storms：19.2% 中 3.8% 被迫；16.3% 中 12.5% 可避免 | 19.23 / 3.77 / 16.28 / 12.51 | 同上 |
| 精确模式在平面数据上距下界 0.03 个百分点以内，合并误差为 0 | 最大 0.006；NMLE_max 全为 0 | `figdata/frontier20261027` |
| 每张渲染图都在允许量以内 | 0 违反 | 同上 |
| ν\* 在 917 帧上达到；Cylinder 12.24% → 8.01% | 917/917；12.24、8.01 | `figdata/order_budget20261027`、`bound_allowance20261105` |
| 概念图：14%、12%、ε=30%、屏障 0.7 | 0.14、0.12、0.3 | `code/results/controlled_conflict20261030/summary.json` |
| 受控树：43 个重叠 × 4 种宽度，24 个叶序；τ=max(0,(d+0.04)/2)；四个父间隙都在 2ε=h 时消失 | 一致（误差 < 1e-16） | `controlled_conflict20261030/overlap.json`、`budget.json` |
| Tangaroa ε=5%：0.38% / 7.40% / 8.10% | 一致 | `order_width20261027/REPORT_zh.md`、`tangaroa.json` |
| 投影最大合并误差 59%；58.66 / 52.58 / 33.56 / 31.02%；Tangaroa 没有一帧保持树 | 一致；Tangaroa 0/201 | `figdata/frontier20261027` |
| Tangaroa 9.67% 对 9.24% | 一致 | 同上 |
| 精确模式的运动误差在七组上都低于 TMTM 和 ST-MTM；OLR 5.4 对 21.4，Tangaroa 52.2 对 70.0；投影在多数数据上更低 | 一致（投影在 5/7 上更低） | `figdata/metrics_n1c20261027`、`unified_metrics.csv` |
| ST-MTM 的 TW 在七组上最好，SNS 在五组上最好；Cylinder SNS 0.041 对 0.135 | 一致 | 同上 |
| Cylinder ε=1%：27.00 → 5.27，投影 5.73；Wildfires 20.48 → 8.71；PM2.5 5% 达到投影 | 一致 | `figdata/frontier20261027` |
| Storms 到 ε=20% 仍高于 18%；OLR 到 10% 仍 17.14% | 18.46；17.14 | 同上 |
| Storms 10%：平均 0.90%，最坏 8.51% | 一致 | 同上 |
| 同一模型：48–76 / 61–99 / 17–27 / 14–43% | 47.5–76.0 / 60.5–99.2 / 16.7–27.4 / 13.9–42.7 | `code/results/unified20261025`（`make_figure_drafts.baseline_displacement`） |
| Vortex：8.79 → 4.27；12,446 个中 30.91% 变差，24.72% 至少 0.5 个百分点 | 一致 | `code/results/local_redistribution20261030/results.json` |
| OLR 图：171°，2024 年 6–7 月，印度洋和西太平洋 | 170.9°；2024-06-01 至 07-30；60–150°E，15°S–20°N | `framework20261025/olr.json`、`protocol_olr.json` |
| OLR：同一模型平均位移 24.4% / 42.7%，精确模式 1.0% | 一致 | `unified20261025`、`frontier20261027` |
| OLR P1：264 个极小值；Hovmöller 59%（5% 内 77%），浅 32 W m⁻² | 58.7 / 77.3 / 31.7 | `figdata/olr_hovmoller/checks_p1_p2.json` |
| OLR P2：每对相邻日都有极小值出现或消失；列变化 9.0% 对 4.1% | 59/59；0.090 / 0.041 | 同上 |
| Storms 案例：37.3 / 50.7 / 5.1（中位 0.8，峰值 26.2）/ 2.7；31/118；8.51；0.90；89 个屏障 | 一致 | `figdata/maps20261030/storms_case.json` |
| 首页图：744 帧逐小时，1999 年 12 月，快照 16–19 日 | 图中时间 12-01 00:00 至 12-31 23:00，快照 12-16 03:00 至 12-19 20:00 | `figures/anchor_storms_overview.pdf`、`local_redistribution20261030`（744 帧） |
| 方向：Tangaroa 4.70–10.14%，x 轴 6.09%；Cylinder 5.49–28.15%，顺流轴 8.01%；关键方向 0.6 个百分点以内（Tangaroa z 2.6） | 一致 | `bound_allowance20261105/*_direction.json` |
| 宽度感知：Tangaroa 20.69 → 15.10（ε=0）、14.55（ε=2%），跳动 2.82 对 2.73；Cylinder 5.73 → 5.27 | 一致 | `order_width20261027` |
| 637 帧、9 个预算 | 一致（但见 E） | `order_budget20261027` |
| 运行时间：边界 0.6 / 5.5 ms，排序 3.7 / 103 ms，二次规划 2.3–9.0 ms / 0.25–0.50 s，总计 94 s / 137 s；M2 Pro、NumPy 2.0、SciPy 1.13 | 0.62 / 5.48；3.71 / 103.2；2.25–8.99 / 0.247–0.504；93.6 / 136.9 | `code/results/runtime20261027/runtime.json`（"QP 时间"含指标计算，偏保守） |
| Storms TD 23.1 / 10.1 / 7.2；运动误差 47 / 41 / 14 / 24% | 一致 | `metrics_n1c20261027`、`unified_metrics.csv` |
| OLR 跳动 1.0% 对锚点运动 5.9%；Tangaroa 2.8% | 1.01 / 5.94；2.82 / 2.80 | `figdata/frontier20261027` |
| TMTM 复现 3127 个区间和锚点；ST-MTM KKT 残差 < 1e-6 | 687 + 431 + 463 + 1257 + 289 = 3127，0 差异；最大 9.64e-7 | `code/results/baseline_audit_20261019/REPORT_zh.md`、`instance_reproduction20261027` |
| Ring 和 OLR 200 个渲染列 | 两种预算 × (40 + 60) 列，每列极值数等于叶子数，0 例外（今天重验） | `figdata/maps20261030/maps_{ring,olr}.npz` |

## 小的措辞建议（不影响数字）

- Storms 案例中"per step""31 of 118 steps"实际是逐帧（118 帧），可改成"per frame""31 of 118 frames"。
- 5.6 "where the worst frame meets the lower bound"：达到下界的是叶序的 τ（13.72%），显示的最坏位移 14.55% 还加上了位置松弛 β0；可写成"where the worst frame's order meets the width bound"。
- 运行时间里的"二次规划时间"含指标计算，是偏保守的上界，可以不改。

## 11/5 已按上表修改（用户确认后）

A–G 和两条小措辞都已改进 `paper/anchor_full/main.tex` 和 `main_zh.tex`，G 的参数说明加在 `supplement.tex` S10 开头（"ST-MTM setting" 段），没有新增附录节，S 编号不变。

| # | 实际改法 |
|---|---|
| A | "only 4 of the 400 sampled directions"；中文"只有 4 个" |
| B | "By the same test, Exact Mode has a dip within 2% (5%) for 94% (97%) of the minima, and 93% are shown at their exact values within 2%; the others are displaced farther or swapped with a neighbouring minimum. Their nesting is kept." 保留与 Hovmöller 同一检验的对比，同时写出更严格的 93% |
| C | "…on most planar frames and on the worst Cylinder frame at every budget, but not uniformly: on Tangaroa the worst frame meets it only at ε=2%, and on Wildfires at ε>0 and on one OLR frame at ε=10%, a worst-frame gap remains." |
| D | "whereas on these sequences no point of the AnchorMTM curves exceeds 26.2% and 4.2%" |
| E | 5.6："the point-model order search attains the exhaustive NROE optimum"；局限段："matched exhaustive enumeration in NROE" |
| F | "lies 1.1° from west–east" |
| G | 5.1 Instances 加 "with one untuned setting on all sequences rather than the original per-dataset settings (Supplement S10)"；S10 新段写明 uniform / r=0.95 / λ=0.5 / K=AnchorMTM 首帧总叶宽，原论文 Storms 为 inverse / K=135 / r=0.65 / λ=0.05、Wildfires 为 K=10 / r=0.85，并说明直接替换参数也不能复现原图，因此不是原结果的复现 |
| 小措辞 | Storms 案例 "per frame, averaged over frames""in a few frames""31 of 118 frames"；5.6 "where the worst frame's order meets the width bound" |

编译检查：正文仍在第 9 页结束，参考文献从第 9 页底开始，共 10 页；补充材料 16 页（原 15 页）；中文版 18 页。Overleaf 包已更新（37 个文件不变）。
