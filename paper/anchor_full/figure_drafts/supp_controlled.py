"""Supplementary Fig. S2 (v33): controlled four-leaf trees, redrawn so that no legend covers a curve (2026-11-09).

Data (read only): code/results/controlled_conflict20261030/{overlap,budget}.json, the saved records behind the
collaborator's figure (43 overlaps x 4 widths; 4 parent gaps x 91 budgets = 364 runs).
(a) displacement against the sibling overlap d: interval LP optimum (width 6%), point bound nu* (width 0), width bound.
(b) displacement against the merge budget for the four parent gaps h; the conflict is released at 2*eps = h.
Legends sit below the axes. Output: ../../pvis2027/latex_v30/figures/supp_controlled.{pdf,png}
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import v23_figures as v

HERE = Path(__file__).resolve().parent
RES = HERE.parents[2] / 'code/results/controlled_conflict20261030'
OUT = HERE.parents[1] / 'pvis2027/latex_v30/figures'
BLUE, LBLUE, ORANGE, GREEN = '#0B5CAD', '#56B4E9', '#D55E00', '#009E73'


def main():
    v.use_times()
    rows = json.loads((RES / 'overlap.json').read_text()); runs = json.loads((RES / 'budget.json').read_text())
    point = sorted((r for r in rows if r['width'] == 0), key=lambda r: r['overlap'])
    wide = sorted((r for r in rows if r['width'] == .06), key=lambda r: r['overlap'])
    assert len(point) == len(wide) == 43 and len(runs) == 364
    fig = plt.figure(figsize=(3.45, 1.95))
    ga = fig.add_gridspec(1, 2, left=.13, right=.985, top=.88, bottom=.43, wspace=.32)
    ax = fig.add_subplot(ga[0, 0])
    d = 100 * np.array([r['overlap'] for r in wide])
    ax.plot(d, [100 * r['nu'] for r in point], '--', color=LBLUE, lw=1.0, label=r'point bound $\nu^*$')
    ax.plot(d, [100 * r['exact_tau'] for r in wide], '-', color=ORANGE, lw=1.3, label='LP optimum')
    ax.plot(d[::4], [100 * r['width_lower'] for r in wide][::4], 'o', ms=3.2, mfc='white', mec=BLUE, mew=.9, label='width bound')
    ax.set_xlim(-13, 31); ax.set_ylim(-.6, 18); ax.set_xticks([-10, 0, 10, 20, 30]); ax.set_yticks([0, 5, 10, 15])
    ax.set_xlabel('sibling overlap $d$ (%)', fontsize=7, labelpad=1); ax.set_ylabel('displacement (%)', fontsize=7, labelpad=1)
    ax.set_title('(a) Forced displacement', fontsize=7.6, pad=3)
    ax.legend(loc='upper center', bbox_to_anchor=(.5, -.36), ncol=1, fontsize=6.2, frameon=False, handlelength=1.6, labelspacing=.25)
    bx = fig.add_subplot(ga[0, 1])
    for gap, col in [(.2, BLUE), (.4, LBLUE), (.6, ORANGE), (.8, GREEN)]:
        b = sorted((r for r in runs if abs(r['parent_gap'] - gap) < 1e-9), key=lambda r: r['epsilon'])
        e = 100 * np.array([r['epsilon'] for r in b]); t = 100 * np.array([r['tau'] for r in b])
        bx.step(e, t, where='post', color=col, lw=1.1, label=f'$h$ = {100 * gap:.0f}%')
        keep = np.isclose(np.mod(e, 4), 0) | np.isclose(np.mod(e, 4), 4)
        bx.plot(e[keep], t[keep], 'o', ms=2.6, mfc='white', mec=col, mew=.8)
        print(gap, 'released at eps =', e[np.argmax(t < 1e-9)], '%')
    bx.set_xlim(-1, 46); bx.set_ylim(-.6, 18); bx.set_xticks([0, 10, 20, 30, 40]); bx.set_yticks([0, 5, 10, 15])
    bx.set_xlabel(r'merge budget $\varepsilon$ (%)', fontsize=7, labelpad=1)
    bx.set_title('(b) Release threshold', fontsize=7.6, pad=3)
    bx.legend(loc='upper center', bbox_to_anchor=(.5, -.36), ncol=2, fontsize=6.2, frameon=False, handlelength=1.6,
              labelspacing=.25, columnspacing=1.0)
    for a in (ax, bx):
        a.tick_params(labelsize=6.5, length=2, pad=1); a.yaxis.grid(True, color='#EEF0F2', lw=.5); a.set_axisbelow(True)
        for sp in ('top', 'right'): a.spines[sp].set_visible(False)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'supp_controlled.{ext}', dpi=300)


if __name__ == '__main__':
    main()
