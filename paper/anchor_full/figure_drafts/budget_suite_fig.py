"""v29 Fig. 7: where a budget acts, per frame, on the same seven-sequence suite as every other result (2026-11-09).

Per-frame worst displacement of AnchorMTM (default configuration, frontier pipeline, checked against the stored
frontier values) over eps in {0, 2, 5, 10, 20}% for Storms, daily PM2.5, Tangaroa and Cylinder; bottom row: share of
frames whose attained merge error is positive (above the numerical allowance).
Output: ../../pvis2027/latex_v21/figures/budget_suite.{pdf,png}; ../figdata/budget_suite20261109.json
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import volume_gallery_data as vg
import v23_figures as v

HERE = Path(__file__).resolve().parent; OUT = HERE.parents[1] / 'pvis2027/latex_v21/figures'
NAMES = [('Storms', 'Storms (2D, 118 frames)'), ('PM2.5', r'PM$_{2.5}$ daily (2D, 366 frames)'),
         ('Tangaroa', 'Tangaroa (3D, 201 frames)'), ('Cylinder', 'Cylinder (3D, 102 frames)')]
EPS = [0, .02, .05, .1, .2]


def data():
    vg.EPS = EPS; out = {}
    for n, _ in NAMES:
        if n in ('Tangaroa', 'Cylinder'):   # same frontier sweep, saved with checks by volume_gallery_data.py
            A = vg.read(vg.FIG / f'volume_gallery20261108/{n.lower()}.json')
        else:
            A = vg.anchor(n)
        L = A['canvas']; Q = A['q']; r = {}
        for e in EPS:
            m = A['maps'][f'eps={e:g}']
            w = [100 * float(np.max(np.abs(np.asarray(x) - np.asarray(q)))) / L for x, q in zip(m['x'], Q)]
            used = int(sum(dlt > 1e-6 for dlt in m['delta']))
            r[f'{e:g}'] = dict(worst=w, used=used, frames=len(w), merge_max=100 * max(m['delta']))
        out[n] = r
    return out


def main():
    v.use_times()
    D = data(); (HERE.parent / 'figdata/budget_suite20261109.json').write_text(json.dumps(D) + '\n')
    fig, axes = plt.subplots(1, 4, figsize=(7.05, 1.7), sharey=True)
    for ax, (n, title) in zip(axes, NAMES):
        xs = np.arange(len(EPS)); data_ = [np.clip(D[n][f'{e:g}']['worst'], 5e-3, None) for e in EPS]
        bp = ax.boxplot(data_, positions=xs, widths=.6, whis=(5, 95), showfliers=True, patch_artist=True,
                        flierprops=dict(marker='.', ms=1.8, mfc='#4A90D9', mec='none', alpha=.6), medianprops=dict(color='#0B3D6B', lw=.9))
        for k, b in enumerate(bp['boxes']): b.set_facecolor('#0B5CAD' if k == 0 else '#BFD8F2'); b.set_edgecolor('#0B3D6B'); b.set_linewidth(.6)
        ax.plot(xs, [np.mean(D[n][f'{e:g}']['worst']) for e in EPS], 'D', ms=3, mfc='white', mec='black', mew=.6, zorder=5)
        ax.set_yscale('log'); ax.set_ylim(.005, 100); ax.set_xticks(xs); ax.set_xticklabels([f'{100 * e:g}' for e in EPS], fontsize=6.5)
        ax.set_title(title, fontsize=7.2, pad=3); ax.tick_params(labelsize=6.5, length=2, pad=1)
        ax.yaxis.grid(True, color='#EEF0F2', lw=.5); ax.set_axisbelow(True)
        for k, e in enumerate(EPS):
            u = D[n][f'{e:g}']; ax.text(k, .0016, f"{100 * u['used'] / u['frames']:.0f}%", ha='center', va='top', fontsize=6, color='#444', clip_on=False)
        print(n, {e: (round(float(np.median(D[n][e]['worst'])), 2), round(float(np.percentile(D[n][e]['worst'], 90)), 2),
                      round(float(np.max(D[n][e]['worst'])), 2), D[n][e]['used'], round(D[n][e]['merge_max'], 2)) for e in ['0', '0.02', '0.05', '0.1', '0.2']})
    axes[0].set_ylabel('worst displacement per frame\n(% of axis length)', fontsize=6.8)
    axes[0].text(-.9, .0016, 'frames using it', ha='right', va='top', fontsize=6, color='#444')
    fig.text(.5, .1, r'merge budget $\varepsilon$ (%)', ha='center', fontsize=7)
    fig.subplots_adjust(left=.09, right=.995, top=.86, bottom=.3, wspace=.08)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'budget_suite.{ext}', dpi=300)


if __name__ == '__main__':
    main()
