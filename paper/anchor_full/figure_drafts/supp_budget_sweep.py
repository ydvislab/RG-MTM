"""Supplementary Fig. S4 (v33): the merge budget sampled finely on Ring, Storms and Wildfires (2026-11-09).

Data (read only): paper/pvis2027/budget_tradeoff_20261105/planar_per_frame/<seq>/epsilon_<eps>.csv, the collaborator's
per-frame records of AnchorMTM at 14-21 budgets (columns NPE = worst displacement of the frame / L, SNS, topology_max =
attained merge error of the frame / scalar range). They reproduce Fig. 8 of the paper exactly at 0, 1, 2, 5, 10, 20%
(checked: frame means and shares of frames with positive merge error). Gaussian is omitted: no frame has a conflict.
TW is not drawn: it is defined on only 1, 4 and 11 frames of these sequences (k neighbours, see Table 1).
Rows: (a) NPE, (b) attained merge error (worst frame and mean over frames; the diagonal is the budget), (c) SNS.
Output: ../../pvis2027/latex_v30/figures/supp_budget_sweep.{pdf,png}
"""
import csv, glob
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import v23_figures as v

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'pvis2027/budget_tradeoff_20261105/planar_per_frame'
OUT = HERE.parents[1] / 'pvis2027/latex_v30/figures'
SEQ = [('Ring', 'Ring (2D)'), ('Storms', 'Storms (2D)'), ('Wildfires', 'Wildfires (2D)')]
BASE = {'Ring': (17.56, 24.63), 'Storms': (57.53, 45.79), 'Wildfires': (22.80, 31.80)}   # NPE (%) of TMTM, ST-MTM, Table 1
BLUE, GREY = '#0B5CAD', '#6B7680'
XMAX = 30


def nice_top(v):
    """Smallest 'round' number >= v, so that the top of an axis can carry a tick label."""
    import math
    e = 10 ** math.floor(math.log10(v))
    for c in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if c * e >= v * 1.0001: return c * e


def nice_bottom(v):
    import math
    e = 10 ** math.floor(math.log10(v))
    for c in (10, 8, 6, 5, 4, 3, 2.5, 2, 1.5, 1.2, 1):
        if c * e <= v * .9999: return c * e


def sweep(name):
    rows = []
    for f in glob.glob(str(DATA / name / 'epsilon_*.csv')):
        e = 100 * float(Path(f).stem.split('_')[1]); R = list(csv.DictReader(open(f)))
        top = np.array([float(r['topology_max']) for r in R]) * 100
        sns = [float(r['SNS']) for r in R if r['SNS'] not in ('', 'nan')]
        rows.append((e, 100 * np.mean([float(r['NPE']) for r in R]), top.max(), top.mean(), np.mean(sns)))
    return np.array(sorted(r for r in rows if r[0] <= XMAX))


def main():
    v.use_times()
    plt.rcParams.update({'font.size': 8})
    fig, axes = plt.subplots(3, 3, figsize=(7.05, 3.9), sharex=True)
    fig.subplots_adjust(left=.075, right=.99, top=.94, bottom=.1, hspace=.32, wspace=.26)
    for j, (n, title) in enumerate(SEQ):
        S = sweep(n); e = S[:, 0]
        a = axes[0, j]; a.step(e, S[:, 1], where='post', color=BLUE, lw=1.3); a.plot(e, S[:, 1], 'o', ms=3, color=BLUE)
        top = nice_top(S[:, 1].max() * 1.05); a.set_ylim(0, top); a.set_yticks([0, top / 2, top]); a.set_yticklabels(['0', f'{top / 2:g}', f'{top:g}'])
        a.set_title(title, fontsize=9, pad=3)
        t, s = BASE[n]; a.text(.97, .06, f'NPE of TMTM {t:.1f}%, ST-MTM {s:.1f}%', transform=a.transAxes, ha='right', va='bottom', fontsize=7.5, color=GREY)
        b = axes[1, j]; b.plot([0, XMAX], [0, XMAX], color='#BBB', lw=.8, ls=(0, (3, 2)))
        b.step(e, S[:, 2], where='post', color=BLUE, lw=1.3, label='worst frame'); b.plot(e, S[:, 3], '--', color=BLUE, lw=1, label='mean over frames')
        b.set_ylim(0, XMAX); b.set_yticks([0, 10, 20, 30])
        c = axes[2, j]; c.plot(e, S[:, 4], '-o', color=BLUE, ms=3, lw=1.1)
        lo, hi = S[:, 4].min(), S[:, 4].max(); pad = .08 * (hi - lo); lo, hi = round(lo - pad, 3), round(hi + pad, 3)
        c.set_ylim(lo, hi); c.set_yticks([lo, (lo + hi) / 2, hi]); c.set_yticklabels([f'{lo:.3f}', f'{(lo + hi) / 2:.3f}', f'{hi:.3f}'])
        c.set_xlabel(r'merge budget $\varepsilon$ (% of the scalar range)', fontsize=8, labelpad=1)
        for ax in (a, b, c):
            ax.set_xlim(-.5, XMAX + .5); ax.set_xticks([0, 5, 10, 15, 20, 25, 30]); ax.tick_params(labelsize=7.5, length=2, pad=1)
            ax.yaxis.grid(True, color='#EEF0F2', lw=.5); ax.set_axisbelow(True)
            for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
        
    axes[0, 0].set_ylabel('NPE (%)', fontsize=8.5)
    axes[1, 0].set_ylabel('merge error (%)', fontsize=8.5)
    axes[2, 0].set_ylabel('SNS', fontsize=8.5)
    axes[1, 0].legend(loc='upper left', fontsize=7.5, frameon=False, handlelength=1.6, borderaxespad=.1)
    axes[1, 0].text(22, 26, 'budget', fontsize=7.5, color='#999', rotation=33, ha='center', va='center')
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'supp_budget_sweep.{ext}', dpi=300)


if __name__ == '__main__':
    main()
