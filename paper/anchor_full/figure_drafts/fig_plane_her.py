"""v30 position-topology plane on the collaborator's sequences (2026-11-09).

Planar panels (Ring, Wildfires, Storms, PM2.5): bound envelope and AnchorMTM construction from plane_her.py (inputs of
her package 01; the strict bound equals her point bound frame by frame); TMTM and ST-MTM at zero merge error with mean
NROE = nu* / (1 - excess share) from her Table 2 (orientations as in her primary measurements); projection from the
reference-sorted order. Gaussian is omitted: its bound is zero and every map attains it.
Volumetric panels (Tangaroa, Cylinder): the same trees as in her volume figure; plane20261108 and best_mirror.
Style: thin lines, light hatch; markers at zero merge error drawn over the outward-shifted axis.
Output: ../../pvis2027/latex_v30/figures/plane_her.{pdf,png}
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import v23_figures as v
import plane_fig as pf

HERE = Path(__file__).resolve().parent; FIG = HERE.parent / 'figdata'
OUT = HERE.parents[1] / 'pvis2027/latex_v30/figures'
EXCESS = {'Ring': (.645, .257), 'Wildfires': (.925, .981), 'Storms': (.910, .830), 'PM25': (.564, .597)}   # her Table 2
PANELS = [('Ring', 'Ring (2D)'), ('Wildfires', 'Wildfires (2D)'), ('Storms', 'Storms (2D)'), ('PM25', r'PM$_{2.5}$ (2D)'),
          ('Tangaroa', 'Tangaroa (3D)'), ('Cylinder', 'Cylinder (3D)')]
GREY = '#E6E9EC'; HATCH = '#BCC3CA'; BLUE = '#0072B2'; TM = '#7B8790'; ST = '#CC79A7'


def series(n):
    if n in EXCESS:
        d = json.loads((FIG / f'plane_her20261109/{n.lower()}.json').read_text())
        be = 100 * np.array(d['bound']['epsilon']); bv = 100 * np.array(d['bound']['envelope'])
        c = sorted((100 * b['NMLE_max'], 100 * b['NROE_mean'], b['epsilon']) for b in d['construction'])
        fx, fy = [], []
        for x, y, e in c:
            if not fy or y < fy[-1] - 1e-12: fx.append(x); fy.append(y)
        nu = 100 * d['nu_strict']; a, b = EXCESS[n]
        base = {'TMTM': nu / (1 - a), 'ST-MTM': nu / (1 - b)}
        proj = (100 * d['projection']['NMLE_max'], 0.)
        e0 = next(b for b in d['construction'] if b['epsilon'] == 0.)
        return be, bv, np.array(fx), np.array(fy), (100 * e0['NMLE_max'], 100 * e0['NROE_mean']), base, proj, nu
    be, bv, fx, fy, pts = pf.series(n); nb = pf.BM['native'][n]
    e0 = next((x, y) for x, y, e in pts if e == 0.)
    return be, bv, fx, fy, e0, {'TMTM': nb['TMTM']['best'], 'ST-MTM': nb['ST-MTM']['best']}, (100 * pf.FR[n]['NMLE_max'], 0.), bv[0]


def main():
    v.use_times()
    fig = plt.figure(figsize=(7.05, 2.75))
    g = fig.add_gridspec(2, 4, left=.065, right=.99, bottom=.12, top=.93, wspace=.32, hspace=.55)
    for k, (n, title) in enumerate(PANELS):
        ax = fig.add_subplot(g[k // 3, k % 3] if False else g[k // 4, k % 4])
        be, bv, fx, fy, e0, base, proj, nu = series(n)
        top = max(list(base.values()) + [bv[0]]) * 1.3
        ax.fill_between(be, 0, bv, step='pre', color=GREY, lw=0, zorder=1)
        ax.fill_between(be, 0, bv, step='pre', facecolor='none', edgecolor=HATCH, hatch='////', lw=0, zorder=1)
        ax.step(be, bv, where='pre', color='#333', lw=.6, zorder=2)
        ax.step(np.append(fx, 100), np.append(fy, fy[-1]), where='post', color=BLUE, lw=.9, zorder=3)
        dx = 0.   # all tree-keeping maps at zero merge error; their values differ, so markers do not overlap
        ax.plot(pf.inv(0), e0[1], 'o', ms=3.4, color=BLUE, mec='white', mew=.4, zorder=8, clip_on=False)
        ax.plot(pf.inv(dx), base['TMTM'], 's', ms=3.6, color=TM, mec='white', mew=.4, zorder=8, clip_on=False)
        ax.plot(pf.inv(2 * dx), base['ST-MTM'], 'D', ms=3.3, color=ST, mec='white', mew=.4, zorder=8, clip_on=False)
        ax.plot(*proj, '*', ms=6.5, color='k', mec='white', mew=.3, zorder=8, clip_on=False)
        share = [100 * (b - nu) / b for b in base.values() if b > 0]
        lo_s, hi_s = round(min(share)), round(max(share)); rng = f'{lo_s}%' if lo_s == hi_s else f'{lo_s}–{hi_s}%'
        ax.text(.97, .95, f'not forced: {rng}', transform=ax.transAxes, ha='right', va='top', fontsize=6.5, color='#3F474F')
        ax.set_xscale('function', functions=(pf.fwd, pf.inv)); ax.set_xlim(0, 65); ax.set_ylim(0, top)
        ax.set_xticks([0, 1, 5, 20, 60]); ax.set_xticklabels(['0', '1', '5', '20', '60'])
        ax.spines['left'].set_position(('outward', 5))
        for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
        ax.tick_params(labelsize=6.5, length=2, pad=1); ax.yaxis.grid(True, color='#F0F2F4', lw=.5); ax.set_axisbelow(True)
        ax.set_title(title, loc='left', fontsize=7.6, pad=2.5)
        if k % 4 == 0: ax.set_ylabel('mean order error (%)', fontsize=6.8)
        if k // 4 == 1 or k == 3: ax.set_xlabel('worst merge error (%)', fontsize=6.6, labelpad=1)
        print(n, f'nu*={nu:.2f}', {m: round(x, 2) for m, x in base.items()}, 'proj NMLE', round(proj[0], 1), 'share', [round(s, 1) for s in share])
    lg = fig.add_subplot(g[1, 2:]); lg.axis('off')
    h = [Patch(facecolor=GREY, edgecolor=HATCH, hatch='////', lw=0, label='unreachable (below the bound)'),
         Line2D([], [], color=BLUE, lw=.9, label=r'AnchorMTM, $\varepsilon$ from 0 to 100%'),
         Line2D([], [], color=BLUE, marker='o', ms=3.4, ls='none', label=r'AnchorMTM, $\varepsilon=0$'),
         Line2D([], [], marker='s', ms=3.6, color=TM, ls='none', label='TMTM'),
         Line2D([], [], marker='D', ms=3.3, color=ST, ls='none', label='ST-MTM'),
         Line2D([], [], marker='*', ms=6.5, color='k', ls='none', label='projection (sorted by reference)')]
    lg.legend(handles=h, loc='center', ncol=2, fontsize=6.8, frameon=False, handlelength=1.6, columnspacing=1.4)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'plane_her.{ext}', dpi=300)


if __name__ == '__main__':
    main()
