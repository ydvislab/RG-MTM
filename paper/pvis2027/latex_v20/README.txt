论文 1037（PacificVis 2027 会议论文轨道）LaTeX 源文件，版本 v20（2026-11-08）
底稿：用户加入作者信息后的版本（Overleaf 导出），在其上修改。格式与 v19 相同，按官方 VGTC 会议模板
（vgtc_conference_latex-2024.02.14）。

文件
  main.tex          正文
  supplement.tex    补充材料（与正文同一模板、同一选项，两栏）
  figures/          全部图（v20 新增 budget_distribution.pdf 和 budget_supp_*.pdf 四张）
  tables/           正文 \input 的四张表
  refs.bib          参考文献
  vgtc.cls, abbrv-doi-narrow.bst   官方模板文件

编译
  Overleaf（pdfLaTeX）：上传整个压缩包，主文件选 main.tex；补充材料把主文件切换为 supplement.tex。
  本地：pdflatex main && bibtex main && pdflatex main && pdflatex main

v20 相对用户版本的改动
  1. 作者块（两份文件相同）：
     - Lele Wang 的标记改为 1,2,*，与 Yu Dong 的 1,* 一致（* 即共同一作脚注）；
     - 脚注先写 "Lele Wang and Yu Dong contributed equally"，再写单位；
     - 删去第一条脚注里重复的 "Jun Liu is the corresponding author."（已有 † 脚注）；
     - 补充材料加上与正文相同的 † 通讯作者脚注；Jun Liu 的标记写成 1,2,†，与其他人格式一致；
     - \hypersetup 的 pdfauthor 改为七位作者（原来仍是 First Author, Second Author）。
  2. 正文新增图 8（单栏）：AnchorMTM 在合并预算 ε=0–10% 下的逐帧分布（三组平面数据，完整序列，
     与主对比表同一配置）。上：每帧最大位移；下：每帧实际合并误差与预算线。5.4 节加一段解读。
  3. 补充材料新增 S10 节和图 S1–S4：扩展扫描（到 30%，Ring 到 100%，含 SNS）、帧×预算矩阵、
     体数据默认配置扫描、Balanced 预算选择过程。原图 S1、S2（位置–拓扑平面、方向）顺延为 S5、S6，
     正文引用已同步。补充材料调了浮动体放置参数（不改字号、行距），共 12 页。
  4. 两处小错：体数据段 "continuous direction in Section 4.2" 改为 4.1（方向定义在 4.1）；
     Wildfires 相对 ST-MTM 的 NPE 降低 96.367% 原写 96.3%，改为 96.4%。

需要你处理
  * 作者脚注里 "E-mails: To be added." 和 "Corresponding author. E-mail: To be added." 两处要填。
  * 篇幅（9 页 = 18 栏；按参考文献标题位置测量，含真实作者块和新图 8）：
        v20 原样                                  20.2 栏
        算法框 Algorithm 1 移到补充材料           19.9 栏
        两张参数表（表 1、表 3）移到补充材料      19.6 栏
        Ring 案例（图 7 与 5.6 节）移到补充材料   19.4 栏
        图 5（选择性放松示意图）删去或移走         19.9 栏
        算法框 + 参数表 + Ring                     18.6 栏
        算法框 + 参数表 + Ring + 图 5              18.2 栏（再删约 13 行文字即为 9 页）
    注意：正文里表号按出现顺序编排，参数表（表 1）移走后主对比表会变成表 1。新图图例不写表号，不受影响。
  * 模板建议在正文末尾加 "Supplemental Materials" 和 "Figure Credits" 两个不编号小节，视篇幅决定。
  * 正式提交前请在 PacificVis 2027 征稿说明中确认评审方式（单盲或双盲）。

作图脚本：仓库 paper/anchor_full/figure_drafts/budget_distribution.py（只读已保存结果，不重跑算法；
数据来自 paper/pvis2027/budget_tradeoff_20261105/ 与 experiments_ratio_p_20261104/，并逐值核对
ε=0 与所选 ε 的结果与主表 Exact、Balanced 运行完全一致）。
