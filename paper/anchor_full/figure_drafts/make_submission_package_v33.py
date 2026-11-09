"""Assemble the v33 submission package: compiled PDFs, the minimal LaTeX source needed to rebuild them, and the
editable figures (combined SVG deck plus the original PPT sources)."""
import shutil, subprocess, zipfile
from pathlib import Path

REPO = Path('C:/Users/ASUS/Desktop/RG-MTM/paper')
SRC = REPO / 'pvis2027/latex_v30'
BUILD = Path('C:/Users/ASUS/AppData/Local/Temp/claude/dc8d4bc441ce0d46/33aac687-2417-4db3-a17a-436fbacc9efb/scratchpad/build')
STAGE = BUILD.parent / 'pkg/1037_v33_submission'
FIGS = ['anchor_storms_overview', 'anchor_related_work_mapping', 'anchor_related_work_panel_d', 'anchor_node_mapping',
        'anchor_framework', 'anchor_relaxation_open', 'forced_plane', 'volume_gallery', 'budget_response_v30',
        'anchor_storms_budget_maps', 'anchor_cylinder_centered_blue', 'anchor_leaf_correspondence',
        'supp_budget_sweep', 'supp_cylinder_compare', 'supp_pm25_compare']
TABLES = ['table1_comparison', 'table2_parameters_runtime']
SOURCES = [('fig01_storms.pptx', 'Fig01_storms_overview.pptx'), ('fig02_related_work.pptx', 'Fig02abc_related_work.pptx'),
           ('node_mapping_updated.pptx', 'Fig03_node_mapping.pptx'), ('framework_requested.pptx', 'Fig04_framework.pptx'),
           ('fig06_relaxation.pptx', 'Fig05_selective_flattening.pptx'), ('fig10_storms_v30.pptx', 'Fig09_storms_budget_maps.pptx'),
           ('fig11_cylinder.pptx', 'Fig10_cylinder.pptx'), ('leaf_correspondence_updated.pptx', 'FigS1_leaf_correspondence.pptx')]
README = """Paper 1037 (PacificVis 2027, Conference Paper Track), version v33, 2026-11-09

1037_paper.pdf        main paper (9 pages + 2 pages of references)
1037_supplement.pdf   supplementary material (5 pages)
latex/                source of both documents
figures_editable/     1037_v33_figures_editable.pptx: every figure (Figs. 1-10, S1-S4), one per slide, as SVG.
                      In PowerPoint 365, right-click a picture > Convert to Shape to edit lines and labels; the
                      overlays LaTeX adds to Figs. 1 and 9 are native shapes. Speaker notes name each source file.
                      source_pptx/ holds the original PPT sources, renamed to the current figure numbers.

Build (from latex/):
  tectonic -X compile main.tex
  tectonic -X compile supplementary.tex
or pdflatex + bibtex + pdflatex x2 for each document.
"""
SRC_README = """Original PowerPoint sources, renamed to the v33 figure numbers.
Fig. 1: the W-E arrow and a* are drawn by LaTeX on top of this figure; Fig. 9: the two white boxes and their text likewise.
Fig. 2: panel (d) is drawn by paper/anchor_full/figure_drafts/fig2_panel_d.py (it is in the combined deck).
Figs. 6, 7, 8, S2, S3 and S4 are drawn by Python scripts (fig6_forced_plane.py, volume_gallery_fig.py, fig7_budget_her.py,
supp_budget_sweep.py, supp_cylinder_compare.py, supp_pm25_compare.py) and have no PPT source; use the combined deck.
Fig. 4: if A, B, C, D have been reordered since v31, the newer file is the one on the author's machine.
"""

if STAGE.parent.exists(): shutil.rmtree(STAGE.parent)
lat = STAGE / 'latex'
for d in ('sections', 'supplementary', 'tables', 'figures'): (lat / d).mkdir(parents=True)
for f in ('main.tex', 'supplementary.tex', 'references.bib', 'vgtc.cls', 'abbrv-doi-narrow.bst'): shutil.copy(SRC / f, lat / f)
for f in (SRC / 'sections').glob('*.tex'): shutil.copy(f, lat / 'sections' / f.name)
shutil.copy(SRC / 'supplementary/content.tex', lat / 'supplementary/content.tex')
for t in TABLES: shutil.copy(SRC / f'tables/{t}.tex', lat / f'tables/{t}.tex')
for g in FIGS: shutil.copy(SRC / f'figures/{g}.pdf', lat / f'figures/{g}.pdf')
ed = STAGE / 'figures_editable'; (ed / 'source_pptx').mkdir(parents=True)
shutil.copy(REPO / '1037_v33_figures_editable.pptx', ed / '1037_v33_figures_editable.pptx')
for src, dst in SOURCES: shutil.copy(SRC / 'figure_sources' / src, ed / 'source_pptx' / dst)
(ed / 'source_pptx' / 'README.txt').write_text(SRC_README, encoding='utf-8')
shutil.copy(BUILD / 'main.pdf', STAGE / '1037_paper.pdf')
shutil.copy(BUILD / 'supplementary.pdf', STAGE / '1037_supplement.pdf')
(STAGE / 'README.txt').write_text(README, encoding='utf-8')

# the staged source must rebuild on its own
chk = BUILD.parent / 'pkgcheck'
if chk.exists(): shutil.rmtree(chk)
shutil.copytree(lat, chk)
for doc in ('main', 'supplementary'):
    run = lambda: subprocess.run(['pdflatex', '-interaction=nonstopmode', f'-jobname={doc}', '\\pdfmapfile{+cm-super-t1.map}\\input{' + doc + '}'],
                                 cwd=chk, capture_output=True)
    run(); subprocess.run(['bibtex', doc], cwd=chk, capture_output=True); run(); run()
    log = (chk / f'{doc}.log').read_text(encoding='latin-1')
    bad = [l for l in log.splitlines() if 'not found' in l or l.startswith('!') or ('undefined' in l.lower() and 'Font' not in l)]
    print(doc, [l for l in log.splitlines() if 'Output written' in l], 'problems:', bad[:5])

out = REPO / '1037_v33_submission.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(STAGE.rglob('*')):
        if f.is_file(): z.write(f, f.relative_to(STAGE.parent))
print(out, round(out.stat().st_size / 1e6, 2), 'MB')
with zipfile.ZipFile(out) as z: print(len(z.namelist()), 'files'); print('\n'.join(n for n in z.namelist() if '/latex/' not in n))
