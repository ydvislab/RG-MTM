# 合作者新仓库 RG-MTM 与我们 RA-MTM 的对比（2026-10-23）

来源：https://github.com/lelewang1109/RG-MTM（13 个提交，2026-10-08 至 10-18，最新提交 `8148498`），本地克隆在 `~/Research/RG-MTM`。它与 RA-MTM 的 git 历史没有关联，是一个独立的新仓库，项目先叫 CD-MTM，后来改名为 RG-MTM。

## RG-MTM 里有什么

- **论文**：`publications/RG-MTM-latest.pdf`，题为 "Reference-Guided Merge Tree Maps: Quantifying Position–Topology Trade-offs"，2026-10-16 版，8 页，**纯文字，没有图**。附录 `RG-MTM-supplement.pdf` 共 22 页。**LaTeX 源码和写作笔记没有放进仓库**，留在合作者本地。
- **代码**：
  - `src/rgmtm/`：合作者原来的 `src/ramtm`，改了名；
  - `analysis/`：**我们 `prototypes/` 的全部脚本**，包括 theory、relax_hierarchy、era5_expanded、attainable、filling 等，外加新增脚本；
  - `experiments/publication2027/`：run / build / validate 流水线，有 25 个测试。
- **数据**：ERA5 用的正是我们 9 月 27 日的扩大窗口文件（SHA 相同）。新增：
  - NOAA OLR（2024 年 6–7 月，热带印度洋–太平洋，60 帧）；
  - 中国 PM2.5（2000 年 1 月，30 帧）。
  - **ERA5 2013/14 不再计入主结果**，OISST 已弃用。
- **新增实验**：
  - 原生 Hilbert / Morton 空间填充曲线基线；
  - packed reference sorting 对照；
  - 公共指标 SNS / TW / TD（与 ST-MTM 可比）；
  - 垂直平分线控制实验；
  - 三维扩展：官方 Tangaroa，300×180×120 原网格，201 帧，TTK 0.9.9，持久性 10%。

## 论文框架的变化

| | 我们（RA-MTM，`paper/pacificvis2027/main.tex`） | 合作者（RG-MTM PDF） |
|---|---|---|
| 题目和定位 | "层次约束的一维布局能有多忠实？"——以理论刻画为主，并推广到树状图显示 | 以方法为主：RG-MTM-P（保持层次）和 RG-MTM-R（放松层次）两种模式 |
| 理论 | 证书、动态规划（定理）、γ/2 拓扑代价及其交错距离解释、最优画法、精确前沿 | 基本相同，但篇幅更短；动态规划降为一段说明 |
| 数据 | ERA5×2、山火、Ring、Gaussians，外加树状图（RQ4） | ERA5、山火、OLR、PM2.5、Ring、Gaussians，共 342 帧；树状图部分删除 |
| 主指标 | 读者代理中的读反率（另报漏判和错误） | NROE（不依赖宽度的标定顺序误差，即我们的 pointcert）、锚点误差、NMLE、ME（读反 + 漏判） |
| 结论口径 | 冲突占 24–63%，读反下降，有权衡 | 冲突占 12–63%，所有序列上 NROE 都下降；运动代理的收益不一致（OLR 没有收益） |
| 图 | 8 张 | 当前 PDF 中没有图（图在 `results/figures/`） |

## 我注意到的风险（供讨论）

1. "339/342 帧在精确前沿上"把未放松的帧也算进去了，而这些帧本来就在前沿上。我们之前用的是只算放松帧的 99/102，更诚实。
2. PM2.5 的月份是在看过四个月之后选的，只有 7 个明确事件；OLR 只有 7/60 帧有冲突。正文已披露，但证据偏弱。
3. 正文没有图，审稿人很难一眼看懂。我们已有的首页图、流程图、概念图、案例图可以直接补进去。
4. 我们论文里的读反分析、ERA5 2013/14、树状图（RQ4）、交错距离解释都被删掉了；需要决定要不要放回去。

## 决定（2026-10-24）

用户选择以 RG-MTM 为新工作仓库：
- 私有仓库 `ydvislab/RG-MTM`（本地 `~/Research/RG-MTM`）；upstream 为 `lelewang1109/RG-MTM`，已禁止 push。
- 我们的 `paper/`、`notes/`、`.aris/` 和 `references/provenance.json` 已拷贝过去并纳入跟踪；为此在私有仓库的 `.gitignore` 里取消了对 `/paper/`、`/notes/` 的忽略。
- 本地 `data/real` 软链接到 RA-MTM 的数据目录。
- 验证：新环境里单元测试通过，`experiments/publication2027/validate.py` 全部一致。
- RA-MTM 从此作为存档，不再修改。
