论文 1037（PacificVis 2027 会议论文轨道）LaTeX 源文件，当前为 v29（2026-11-09）
官方 VGTC 会议模板，preprint 选项：单盲，作者信息显示，页眉为 "Online Submission ID: 1037"。

v29：
  * 正文只用一套数据（7 个序列：Storms 12h、Wildfires、OLR、PM2.5 逐日、Ring、Tangaroa、Cylinder），同一管线、同一默认配置。
    表 1 = tables/table1_suite.tex（figure_drafts/table1_suite.py）；表 2 = tables/table_data_suite.tex。
  * 图：1 Storms 总览（逐小时，示意）；2 冲突；3 流程图（用户编辑的合作者 PPT 导出 figures/anchor_framework_user.pdf）；
    4 受控树；5 位置–拓扑平面；6 渲染地图 Storms/Ring（map_gallery_fig.py）；7 逐帧预算（budget_suite_fig.py）。
  * 原 layout 组（ST-MTM 基准重建、逐小时 PM2.5、调参体数据）移到补充材料 S4。
  * 三维标量地图待合作者提供树数组或渲染列（见 notes/2026-11-09-v29-restructure-plan.md）。

当前状态（2026-11-09，v25）
  v25：按用户意见通篇重写（逻辑框架见 notes/2026-11-09-v25-framework.md）：
    * 贡献按"我们提出……通过……来……"重写，不再写节号；明确 AnchorMTM 直接从数据计算，不是后处理。
    * 方法对照表（原表 1）和 PM2.5 案例图（原图 8）移入补充材料；表 3 去掉"小节"列；式 8 改为文字。
    * 图 5 重画（paper/anchor_full/figure_drafts/v25_fig5.py）：两行、"not forced"标注移到空白处、标记在线之上。
    * 补充材料按论文顺序重排：S1 记号，S2 证明，S3 构建细节，S4 对比方法、数据与设置，S5 补充结果，S6 按方法并列的完整结果表。
  PDF：paper/1037_v25.pdf、paper/1037_v25_supplement.pdf、paper/1037_v25_zh.pdf。

以下为 v23 及更早的记录。

当前状态（2026-11-09，v23）
  已完成：第 1–6 步，以及 v23 修订：
    * 图 4、5、7 用同一批保存数据重画（脚本 paper/anchor_full/figure_drafts/v23_figures.py）：
      图 4 插图移入坐标区内，不再压住横轴；图 5 所有标记画在实测坐标上（去掉原来为避开重叠而加的横向偏移），
      只标 ε=0 的点，Storms 标注改短；图 7 离群帧不再左右抖动，纵轴延伸到 0.004%，7 个低于 0.1% 的 Storms 帧按实际值画出，
      不再用三角形压在底线上。字体统一为 Times New Roman，字号加大。
    * 第 6 章各小节标题与开头段由问句改为陈述句；表 3 "Used in" 列改为对应小节号。
  通讯作者邮箱已填（liujun@sccas.cn）；不写致谢（用户决定，2026-11-09）。
  未完成：第一作者脚注中的 "E-mails: To be added."（其余作者邮箱）、最终 PDF 检查与上传。
  中文译稿：main_zh.tex（与 main.tex 逐段逐句对应、同一模板排版，图片沿用英文原图，图注和表格已译；
          XeLaTeX 编译，类文件 vgtc_zh.cls，表格 tables_zh/），PDF 为 paper/1037_v23_zh.pdf；
          main_zh.md 为同内容的 Markdown 版。预览：paper/1037_v23.pdf、paper/1037_v23_supplement.pdf。

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
