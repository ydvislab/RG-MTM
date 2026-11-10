"""Assemble the v37 submission package (local only, not pushed): compiled PDFs, the LaTeX source needed to rebuild them,
and the editable figures (one native PowerPoint file per figure, paper/figures_editable_v34, Figs. 4-6 regenerated for v37).
Usage (repository root):  python paper/anchor_full/figure_drafts/make_submission_package_v37.py MAIN.pdf SUPPLEMENT.pdf
Output: paper/1037_v37_submission.zip
"""
import re, shutil, sys, zipfile
from pathlib import Path

PAPER = Path(__file__).resolve().parents[2]; SRC = PAPER / 'pvis2027/latex_v30'; EDIT = PAPER / 'figures_editable_v34'
OUT = PAPER / '1037_v37_submission.zip'
README = """Paper 1037 (PacificVis 2027, Conference Paper Track), version v37, 2026-11-09

1037_paper.pdf        main paper (9 pages + references on pages 10-11)
1037_supplement.pdf   supplementary material
latex/                source of both documents (only the figures they use)
figures_editable/     one PowerPoint file per figure (Figs. 1-7, S1-S7); see figures_editable/README.md.
                      Figs. 4-6 were regenerated for v37.

Build (from latex/):  pdflatex main; bibtex main; pdflatex main; pdflatex main  (same for supplementary)
or: tectonic -X compile main.tex / supplementary.tex
"""


def used_figures():
    names = set()
    for f in [SRC / 'main.tex', SRC / 'supplementary.tex', *SRC.glob('sections/*.tex'), *SRC.glob('supplementary/*.tex'), *SRC.glob('tables/*.tex')]:
        t = f.read_text(encoding='utf-8')
        names |= set(re.findall(r'includegraphics(?:\[[^\]]*\])?\{(figures/[^}]+)\}', t))
        names |= set(re.findall(r'paperfigure(?:\[[^\]]*\])?\{(figures/[^}]+)\}', t))
    return sorted(names)


def main(main_pdf, supp_pdf):
    figs = used_figures(); missing = [f for f in figs if not (SRC / f).exists()]
    assert not missing, missing
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('1037_v37_submission/README.txt', README)
        z.write(main_pdf, '1037_v37_submission/1037_paper.pdf'); z.write(supp_pdf, '1037_v37_submission/1037_supplement.pdf')
        for f in ['main.tex', 'supplementary.tex', 'references.bib', 'vgtc.cls', 'abbrv-doi-narrow.bst', *figs]:
            z.write(SRC / f, f'1037_v37_submission/latex/{f}')
        for d in ('sections', 'supplementary', 'tables'):
            for f in sorted((SRC / d).glob('*.tex')):
                z.write(f, f'1037_v37_submission/latex/{d}/{f.name}')
        for f in sorted(EDIT.iterdir()):
            z.write(f, f'1037_v37_submission/figures_editable/{f.name}')
    print(OUT, f'{OUT.stat().st_size / 1e6:.1f} MB', len(figs), 'figures')


if __name__ == '__main__':
    main(*sys.argv[1:3])
