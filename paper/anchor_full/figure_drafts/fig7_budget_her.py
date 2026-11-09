"""v30 Fig. 7: where a merge budget acts, per frame (2026-11-09).

Data: the collaborator's recomputed per-frame records (package 01: planar_per_frame_recomputed.csv,
volume_per_frame_recomputed.csv): worst displacement E_max per frame and the attained merge error, for every budget.
Encoding (replaces the box plots, whose median and mean markers overlapped): for each sequence, the median, the 90th
percentile and the worst frame of E_max over the budget, plus the mean (= NPE) as a dashed line; the bar row gives
the share of frames whose attained merge error is positive. Every frame stays within its budget (checked).
Output: ../../pvis2027/latex_v30/figures/budget_response_v30.{pdf,png}
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import v23_figures as v

PKG = Path('/Users/yudong/Downloads/老师所需四项材料_20261109/01_七序列下界与AnchorMTM输入')
OUT = Path(__file__).resolve().parents[2] / 'pvis2027/latex_v30/figures'
SEQ = [('Ring', 'Ring (2D)'), ('Storms', 'Storms (2D)'), ('PM2.5', r'PM$_{2.5}$ (2D)'), ('Tangaroa', 'Tangaroa (3D)'), ('Cylinder', 'Cylinder (3D)')]
BLUE = '#0B5CAD'; LIGHT = '#9EC3E6'; GREY = '#555555'


def main():
    v.use_times()
    d = pd.concat([pd.read_csv(PKG / 'planar_per_frame_recomputed.csv'), pd.read_csv(PKG / 'volume_per_frame_recomputed.csv')])
    assert (d['NMLE_max'] <= d['epsilon'] + 1e-6).all() and d['rendered_budget_ok'].all()
    fig = plt.figure(figsize=(7.05, 2.15)); g = fig.add_gridspec(2, 5, height_ratios=[3.2, 1], hspace=.12, wspace=.28,
                                                                 left=.075, right=.995, top=.80, bottom=.19)
    for k, (n, title) in enumerate(SEQ):
        s = d[d.dataset == n]; E = sorted(s.epsilon.unique()); x = np.arange(len(E))
        st = {e: 100 * s[s.epsilon == e].E_max.values for e in E}
        p50 = [np.median(st[e]) for e in E]; p90 = [np.percentile(st[e], 90) for e in E]; mx = [st[e].max() for e in E]; mean = [st[e].mean() for e in E]
        ax = fig.add_subplot(g[0, k])
        ax.fill_between(x, p50, p90, color=LIGHT, alpha=.55, lw=0)
        ax.plot(x, mx, '-', color=GREY, lw=.8, marker='^', ms=2.6)
        ax.plot(x, p90, '-', color=BLUE, lw=1.1, marker='o', ms=2.6, mfc='white', mew=.8)
        ax.plot(x, p50, '-', color=BLUE, lw=1.6, marker='o', ms=2.8)
        ax.plot(x, mean, '--', color='#C25A00', lw=1.0)
        ax.set_yscale('log'); ax.set_ylim(.5, 70); ax.set_xticks(x); ax.set_xticklabels([])
        ax.set_title(title, fontsize=7.6, pad=3); ax.tick_params(labelsize=6.5, length=2, pad=1)
        ax.yaxis.grid(True, color='#EEF0F2', lw=.5); ax.set_axisbelow(True)
        for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
        if k == 0: ax.set_ylabel('worst displacement\nper frame (%)', fontsize=6.8)
        b = fig.add_subplot(g[1, k]); used = [100 * (s[s.epsilon == e].NMLE_max > 1e-5).mean() for e in E]
        b.bar(x, used, width=.6, color=LIGHT, edgecolor=BLUE, lw=.5); b.set_ylim(0, 100); b.set_yticks([0, 100])
        b.set_xticks(x); b.set_xticklabels([f'{100 * e:g}' for e in E], fontsize=6.5); b.tick_params(labelsize=6.2, length=2, pad=1)
        for sp in ('top', 'right'): b.spines[sp].set_visible(False)
        if k == 0: b.set_ylabel('frames\nusing (%)', fontsize=6.5)
        print(n, {f'{100 * e:g}': (round(p50[i], 2), round(p90[i], 2), round(mx[i], 2), round(mean[i], 2), round(used[i], 1)) for i, e in enumerate(E)})
    fig.text(.535, .02, r'merge budget $\varepsilon$ (%)', ha='center', fontsize=7.2)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    h = [Line2D([], [], color=BLUE, lw=1.6, marker='o', ms=2.8, label='median'), Patch(color=LIGHT, alpha=.55, label='median–90th pct.'),
         Line2D([], [], color=BLUE, lw=1.1, marker='o', ms=2.6, mfc='white', label='90th percentile'),
         Line2D([], [], color=GREY, lw=.8, marker='^', ms=2.6, label='worst frame'), Line2D([], [], color='#C25A00', lw=1, ls='--', label='mean (NPE)')]
    fig.legend(handles=h, ncol=5, loc='upper center', bbox_to_anchor=(.535, 1.0), fontsize=6.6, frameon=False, handlelength=1.6, columnspacing=1.2)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'budget_response_v30.{ext}', dpi=300)


if __name__ == '__main__':
    main()
