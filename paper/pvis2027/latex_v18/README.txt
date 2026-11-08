论文 1037（PacificVis 2027 会议论文轨道）LaTeX 源文件，版本 v18（2026-11-08）

文件
  main.tex          正文（VGTC 模板，review 选项，正文 9 页 + 参考文献 1 页）
  supplement.tex    补充材料（图 S1 位置–拓扑平面，图 S2 方向影响）
  figures/          正文和补充材料用到的全部图
  tables/           正文 \input 的四张表
  refs.bib          参考文献
  vgtc.cls, abbrv-doi-narrow.bst   模板文件

编译
  Overleaf：上传整个压缩包，主文件选 main.tex（补充材料另建项目或切换主文件为 supplement.tex）。
  本地：pdflatex main && bibtex main && pdflatex main && pdflatex main

作者信息（单盲）
  main.tex 中 "AUTHORS (single-blind review)" 一段：修改 \author{...}，作者之间用 \and。
  vgtc 的 review 选项本来不显示作者，这里用一个小补丁把作者印在标题下面，页眉仍保留 Online Submission ID。
  如果最后要求双盲，把 \showauthorstrue 改成 \showauthorsfalse 即可。
  pdfauthor 在上面一行的 \hypersetup 里，也请一并修改。
  supplement.tex 的 \author{...} 也要改。

注意
  正文现在正好写满 9 页，参考文献从第 10 页顶部开始。作者和单位较多时，标题区会变高，可能把正文挤到第 10 页；请编译后检查。
  标题备选见下，改 \title 和 \hypersetup 的 pdftitle 两处（补充材料的 \title 也要改）。
    当前：AnchorMTM: Spatially Anchored Merge Tree Maps with Displacement Bounds
    备选：AnchorMTM: Spatially Anchored Merge Tree Maps with Layout-Independent Displacement Bounds
    备选：How Far Must Topology Move Features? Spatially Anchored Merge Tree Maps
