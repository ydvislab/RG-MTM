论文 1037（PacificVis 2027 会议论文轨道）LaTeX 源文件，版本 v19（2026-11-08）
按官方 VGTC 会议模板（vgtc_conference_latex-2024.02.14）检查并改正格式。

文件
  main.tex          正文
  supplement.tex    补充材料（与正文同一模板、同一选项，两栏）
  figures/          全部图
  tables/           正文 \input 的四张表
  refs.bib          参考文献
  vgtc.cls, abbrv-doi-narrow.bst   官方模板文件（与官方压缩包中的文件逐字节相同）

编译
  Overleaf（pdfLaTeX）：上传整个压缩包，主文件选 main.tex；补充材料把主文件切换为 supplement.tex。
  本地：pdflatex main && bibtex main && pdflatex main && pdflatex main

与 v18 相比的格式改动
  1. 文档类：\documentclass[review]{vgtc} 改为 \documentclass{vgtc}。官方模板说明 review 选项只用于双盲评审；
     单盲评审用默认（final）样式，作者信息正常显示。如果最后确认是双盲，改回 [review] 即可
     （作者自动隐藏，页眉显示 Online Submission ID）。
  2. 删除不符合模板的排版压缩：\linespread{0.90}（行距压缩 10%），以及 \textfloatsep、\floatsep、
     \dbltextfloatsep 的缩小。
  3. 作者：改为官方会议格式 \author{姓名\thanks{e-mail: ...}\\ \scriptsize 单位 \and ...}，
     电子邮件以脚注形式出现在首页左栏底部。v18 里为 review 模式加的作者补丁已删除。
  4. 标题：AnchorMTM: Spatially Anchored Merge Tree Maps with Position Bounds，一行排下
     （485pt，可用宽度 504pt）。原标题 "... with Displacement Bounds" 在模板字号下要两行。
  5. 首页大图（teaser）图注：\caption 放在 \teaser 里时，只要 \vgtcinsertpkg 加载了 hyperref，
     图注就会打印成空白（用官方 vgtc.cls 做最小例子也能复现）。所以保留手写图注，
     字体、"Figure 1:" 前缀、两端对齐和段前间距都与 vgtc.cls 中 \@makecaption 的定义一致。
  6. 前导区顺序按模板排列：\onlineid、\vgtccategory、\vgtcinsertpkg、\title、\author、\teaser、
     \abstract、\keywords。
  7. 补充材料由 article 类改为 vgtc 类：同样的标题、作者和摘要格式；宽表和宽图改用 table*/figure*；
     一个超出栏宽的公式改为两行；图、表、节、公式、定理都用 S 编号。

需要你处理
  * 作者：main.tex 和 supplement.tex 中的 \author 与 \hypersetup{pdfauthor=...}，两处都要改，且保持一致。
  * 篇幅：去掉行距压缩后，正文超出 9 页约 0.8 页（参考文献从第 10 页右栏中部开始）。
    按"栏"测得的正文长度（9 页 = 18 栏）：
        只修格式                                 19.6 栏
        算法框 Algorithm 1 移到补充材料          19.3 栏（省 0.34 栏）
        两张参数/耗时表移到补充材料              19.1 栏（省 0.54 栏）
        Ring 案例（图 7 与 5.6 节）移到补充材料  18.8 栏（省 0.81 栏）
        算法框 + 参数表                          18.8 栏
        三项都移                                 18.1 栏（再删约 3 行即为 9 页）
    以上是两位占位作者时的结果；作者和单位更多时标题区会更高。
  * 编译有一条 1.2pt 的 Overfull \vbox 警告（某栏高出 1.2pt，肉眼不可见），删减后通常会消失。
  * 模板建议在正文末尾加 "Supplemental Materials"（说明补充材料内容和存放位置）和
    "Figure Credits"（转载或改编他人图片时注明来源）两个不编号小节，可视篇幅决定是否加。
  * 正式提交前请在 PacificVis 2027 征稿说明中确认评审方式（单盲或双盲）。
