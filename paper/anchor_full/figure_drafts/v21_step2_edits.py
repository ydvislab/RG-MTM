"""v21 step 2: insert the 2D+3D distribution figure and the compact plane, move the Ring case and the parameter tables
to the supplement. Applied to the step-1 versions of main.tex and supplement.tex; every cut is bounded and checked."""
import re, sys
from pathlib import Path
D = Path(__file__).resolve().parents[2] / 'pvis2027/latex_v21'
s = (D / 'main.tex').read_text(); t = (D / 'supplement.tex').read_text()
n0 = len(s)


def block(text, start, end):
    """Exact block from start marker through the first end marker after it (inclusive)."""
    i = text.index(start); j = text.index(end, i) + len(end); return i, j


def replace_once(text, old, new):
    assert text.count(old) == 1, old[:80]; return text.replace(old, new)


# 1. distribution figure (single column) and its paragraph -> 2D+3D figure* and new paragraph
i, _ = block(s, "\\begin{figure}[t]\n\\centering\n\\includegraphics[width=\\columnwidth]{figures/budget_distribution.pdf}", "\\end{figure}\n")
j = s.index("\\subsection{Accuracy of the Position Bounds}", i)
assert j - i < 2500, j - i
s = s[:i] + (D.parent.parent / 'anchor_full/figure_drafts/v21_dist_block.tex').read_text() + "\n" + s[j:]

# 2. compact plane before the Real trees paragraph; main-text pointer
s = replace_once(s, "\\emph{Real trees.} We also evaluate",
                 (D.parent.parent / 'anchor_full/figure_drafts/v21_plane_block.tex').read_text() + "\\emph{Real trees.} We also evaluate")
s = replace_once(s, "Supplementary Fig.~S5 places all maps against the bounds.", "Figure~\\ref{fig:plane} places every map of these sequences against the bounds.")

# 3. Ring figure (one float), Ring subsection, parameters subsection and the two parameter tables -> supplement
i, j = block(s, "\\begin{figure}[!t]\n\\centering\n\\includegraphics[width=\\columnwidth]{figures/anchor_ring_result.pdf}", "\\end{figure}\n")
ringfig = s[i:j]; assert len(ringfig) < 1500, len(ringfig); s = s[:i] + s[j:]
i = s.index("\\subsection{Ring Case Study: Temporal Overview and Source Snapshots}"); j = s.index("\\subsection{Storms Case Study", i)
ringsec = s[i:j]; assert len(ringsec) < 1600, len(ringsec); s = s[:i] + s[j:]
i = s.index("\\subsection{Parameters and Computational Cost}"); j = s.index("\\section{Discussion and Limitations}", i)
params = s[i:j]; assert len(params) < 1200, len(params); s = s[:i] + s[j:]
for old in ["\\input{tables/table2_parameters_runtime.tex}\n", "\\input{tables/table_volume_parameters.tex}\n"]:
    s = replace_once(s, old, "")
s = replace_once(s, "\\section{Discussion and Limitations}", """\\paragraph{Parameters and runtime.}
The Balanced budgets are 1, 1, 5 and 10\\% on Gaussian, Ring, Wildfires and Storms. One cold Balanced run takes 0.5--63\\,s on an Apple M4, of which ordering and placement take 0.15--3.3\\,s; the rest is preprocessing, tree extraction, matching, rasterization and checks. Supplementary Tables~S3 and~S4 list all settings, and Supplementary Fig.~S8 shows a joint guidance--topology sweep on Ring with source snapshots.

\\section{Discussion and Limitations}""")
s = replace_once(s, "Table~\\ref{tab:volume-parameters} reports their different weights and budgets.", "Supplementary Table~S4 reports their different weights and budgets.")
assert not re.search(r'ref\{(fig:ring-result|tab:anchor-parameters-final|tab:volume-parameters)\}', s)

ringsec = ringsec.replace("\\subsection{Ring Case Study: Temporal Overview and Source Snapshots}\n", "").replace(
    "its $\\alpha=0$ panel is not the Exact Mode of Table~\\ref{tab:quantitative-final}", "its $\\alpha=0$ panel is not the Exact Mode of the paper's comparison table").strip()
params = params.replace("\\subsection{Parameters and Computational Cost}\n", "").strip()
sec = ("\\section{Ring Case Study, Parameters and Runtime}\\label{sec:supp_ring_params}\n" + ringfig + ringsec +
       "\n\n\\input{tables/table2_parameters_runtime.tex}\n\\input{tables/table_volume_parameters.tex}\n" + params + "\n\n")
t = replace_once(t, "\\FloatBarrier\n\\bibliographystyle{abbrv-doi-narrow}", "\\FloatBarrier\n" + sec + "\\FloatBarrier\n\\bibliographystyle{abbrv-doi-narrow}")
t = replace_once(t, "and an exploratory volumetric case.}", "an exploratory volumetric case, and the Ring case study with all parameter settings and runtimes (Fig.~S8, Tables~S3 and S4).}")
(D / 'main.tex').write_text(s); (D / 'supplement.tex').write_text(t)
print('main chars', n0, '->', len(s), '| moved', len(ringfig), len(ringsec), len(params))
