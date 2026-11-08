论文 1037（PacificVis 2027 会议论文轨道）LaTeX 源文件，v21 草稿（2026-11-08 中午）
官方 VGTC 会议模板（vgtc_conference_latex-2024.02.14），单盲，作者信息已加入。

当前状态（2026-11-09）
  已完成：第 1–5 步（骨架与统一表述、结果图、摘要/引言/相关工作重写、实验按 Q1–Q4 重排、
          合入合作者流程图与逐小时 PM2.5）；第 6 步逻辑与数字核对（正文百分比与表 1、体数据表逐项复算一致；
          统一了"下界组/布局组"在摘要、贡献、结论中的说法；图 5 标明 daily PM2.5；Balanced 明确为预算模式）。
  未完成：第 7 步——两处邮箱 "To be added"、是否在致谢中披露生成式 AI（IEEE 政策）、最终 PDF 检查与上传。
  中文全文对照：main_zh.md。

新的论文思路（一句话）
  把合并树地图的轴锚定到空间，位置上必然要付出代价；我们算出任何地图都逃不掉的这份代价，
  做出一个只比它多付一点的地图（AnchorMTM），并用它说明现有地图的大部分误差并不是这份代价。

结构
  1 引言（待重写）  2 相关工作（待重写）
  3 空间锚定的合并树地图：合并树与剖面；统一表述（Eq. 3）——TMTM、ST-MTM 是"合并误差为 0、
    没有参考项"的两个特例（表 1）；空间参照；冲突在哪（图 2）
  4 保住树的代价：三个与布局无关的下界（定理 1–3）；"树逼的 vs 画法选的"
  5 AnchorMTM：统一表述的一个实例，逼近下界（叶序、放置、重建）
  6 实验（待按 Q1 下界紧不紧 / Q2 现有方法误差有多少是树逼的 / Q3 是否更准、守预算 / Q4 预算买到什么 重排）
  7 讨论与局限  8 结论

与 v20 相比的主要改动
  * 编号公式 23 个 → 9 个；新增统一表述公式和方法族表（表 1）。
  * 新图 4：位置–拓扑平面（七个序列，含二维和三维，所有方法在同一平面上，灰色为不可达区）。
  * 新图 6：三维效果对比（Tangaroa、Cylinder；参考位置 / TMTM / ST-MTM / AnchorMTM ε=0、5%、20%）。
  * 新图 7：逐帧分布（三个二维 + 两个三维数据集，ε=0/2/5/10/20%）。
  * Ring 案例（原图 7 与 5.6 节）和两张参数表移到补充材料末尾（图 S8、表 S3–S4）。
  * 贡献改为三条短句。
  * 篇幅：正文 9 页（17.5 栏，上限 18 栏）+ 参考文献 1 页；补充材料 13 页。

文件
  main.tex、supplement.tex、refs.bib、vgtc.cls、abbrv-doi-narrow.bst、tables/、figures/
  新图同时有可编辑的 SVG（文字为文本）：figures/plane_compact.svg、volume_gallery.svg、budget_per_frame.svg

编译
  Overleaf（pdfLaTeX）：上传整个压缩包，主文件选 main.tex；补充材料把主文件切换为 supplement.tex。
  本地：pdflatex main && bibtex main && pdflatex main && pdflatex main

作者信息
  两份文件里 "E-mails: To be added." 和 "Corresponding author. E-mail: To be added." 要填。

新图的数据来源（都是已保存结果，没有新实验）
  * 图 3：合作者提供的流程图（PPTX 导出），可编辑源文件 figures/anchor_framework.pptx。
  * 图 5：早期七序列基准的下界与 AnchorMTM 前沿；TMTM/ST-MTM/OLO 取与参考更一致的镜像。
  * 图 6：AnchorMTM 位置由 frontier 管线重算，与存档结果及体数据预算扫描逐项一致；
    TMTM、ST-MTM 为仓库中按原文实现保存的锚点，同一特征。若要换成标量地图，需要
    output/current_method_parameter_sweep_20261029/{tangaroa,cylinder}/epsilon_*.npz（合作者机器上）。
  * 图 7（11-09 重画：一行四面板 Storms、PM2.5、Tangaroa、Cylinder，对数纵轴，底行为用到预算的帧比例）：
    Storms 用 budget_tradeoff_20261105/planar_per_frame/Storms（0% 与 10% 与表 2 逐值一致）；
    PM2.5 用 pm25_hourly_20261107/six_budgets_20261108/PM25_six_budgets_per_frame.csv（0% 与 5% 均值等于表 2）；
    体数据用 budget_tradeoff_20261105/volume_per_frame_audit.csv。
  作图脚本在仓库 paper/anchor_full/figure_drafts/（plane_fig.py compact、volume_gallery_fig.py、budget_distribution.py v22）。
  * 图 9 与表 2 的 PM2.5 行、补充表 S3 的 PM2.5 列：合作者的逐小时 PM2.5 结果
    （仓库 paper/pvis2027/pm25_hourly_20261107/：comparison_metrics.csv、timing.json、eps_*_summary.json）；
    图 9 的可编辑版本是 figures/pm25_hourly.svg。
