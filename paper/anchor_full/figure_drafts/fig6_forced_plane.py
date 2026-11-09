"""v32 Fig. 6: forced and chosen order error, and the position-topology plane without the baselines (2026-11-09).

Why: in the v31 plane (fig_plane_her.py) the TMTM and ST-MTM markers set the y-range, so the bound and the AnchorMTM
curve were squeezed to the bottom of every panel (Wildfires: 0.16% against 8.4%), and the share of error not forced by
the tree was only a text label. Here
  (a) shows the zero-merge-error slice on a log axis: the hatched region below nu* (no exact map can be there), the
      AnchorMTM order at eps = 0, and TMTM / ST-MTM; the line from the bound to each baseline is the order error the
      tree does not force, and its share is printed per row;
  (b) shows the plane for the budget alone (bound envelope, AnchorMTM, projection), each panel scaled to its own
      bound, so the curves fill the panels.
Data: identical to fig_plane_her.py (series()); nothing is recomputed.
Output: ../../pvis2027/latex_v30/figures/forced_plane.{pdf,png}
"""
import json, os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import v23_figures as v
import plane_fig as pf
from fig_plane_her import series, OUT, FIG, PANELS, GREY, HATCH, BLUE, TM, ST
OUT = Path(os.environ.get('FIG6_OUT', OUT))
# Gaussian: its bound is zero, so it needs a separate '0' position on the log axis. The baselines' mean order error
# comes from the collaborator's package 01 (gaussian_plane_row.py writes this file on the Mac); without it the row is left out.
GAUSS = Path(os.environ.get('FIG6_GAUSS', FIG / 'plane_her20261109/gaussian.json'))
ZERO = .045   # where a value of 0 is drawn, left of an axis break
SHOW_GAUSSIAN = False   # v34: dropped. Its bound is 0 and the row said no more than the sentence in Section 6.2


def nice_top(v):
    """Smallest 'round' number >= v, so that the top of an axis can carry a tick label."""
    import math
    e = 10 ** math.floor(math.log10(v))
    for c in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if c * e >= v * 1.0001: return c * e

ROWS = ['Wildfires', 'Storms', 'Ring', 'PM25', 'Tangaroa', 'Cylinder']   # planar, then volumes; each by nu*
LAB = dict((n, t) for n, t in PANELS)


def gaussian():
    g = json.loads(GAUSS.read_text())
    return None, None, None, None, (0., g['anchor_nroe']), {'TMTM': g['TMTM'], 'ST-MTM': g['ST-MTM']}, None, g['nu_strict']


def forced(ax):
    xmin, xmax = .1, 60.
    rows = (['Gaussian'] if SHOW_GAUSSIAN and GAUSS.exists() else []) + ROWS
    data = {n: (gaussian() if n == 'Gaussian' else series(n)) for n in rows}
    at = lambda val: val if val > 0 else ZERO
    x0 = .07 if 'Gaussian' in rows else xmin   # hatching starts right of the axis break
    for r, n in enumerate(rows):
        be, bv, fx, fy, e0, base, proj, nu = data[n]; y = len(rows) - 1 - r
        if nu > 0:
            ax.add_patch(plt.Rectangle((x0, y - .32), nu - x0, .64, facecolor=GREY, edgecolor=HATCH, hatch='////', lw=0, zorder=1))
        ax.plot([at(nu)] * 2, [y - .32, y + .32], color='#333', lw=.6, zorder=2)
        hi = max(base.values())
        ax.plot([at(nu), hi], [y, y], color='#9AA3AB', lw=.8, zorder=3, solid_capstyle='butt')
        ax.plot(at(e0[1]), y, 'o', ms=3.6, color=BLUE, mec='white', mew=.4, zorder=6, clip_on=False)
        ax.plot(base['TMTM'], y, 's', ms=3.7, color=TM, mec='white', mew=.4, zorder=6)
        ax.plot(base['ST-MTM'], y, 'D', ms=3.4, color=ST, mec='white', mew=.4, zorder=7, clip_on=False)  # on top where they meet (PM2.5)
        share = sorted(100 * (b - nu) / b for b in base.values())
        rng = f'{share[0]:.0f}%' if round(share[0]) == round(share[1]) else f'{share[0]:.0f}–{share[1]:.0f}%'
        ax.text(1.02, y, rng, transform=ax.get_yaxis_transform(), ha='left', va='center', fontsize=8, color='#3F474F')
    ax.text(1.02, len(rows) - .35, 'not forced', transform=ax.get_yaxis_transform(), ha='left', va='bottom', fontsize=8, color='#3F474F')
    ax.set_xscale('log'); ax.set_ylim(-.6, len(rows) - .4)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([LAB.get(n, 'Gaussian (2D)') for n in rows][::-1], fontsize=8)
    if 'Gaussian' in rows:   # zero to the left of an axis break
        ax.set_xlim(.032, xmax); ax.set_xticks([ZERO, .1, 1, 10, xmax]); ax.set_xticklabels(['0', '0.1', '1', '10', f'{xmax:g}'])
        for dx in (.058, .064):
            ax.plot([dx * .97, dx * 1.03], [-.75, -.45], color='#333', lw=.6, clip_on=False, zorder=9)
    else:
        ax.set_xlim(xmin, xmax); ax.set_xticks([xmin, 1, 10, xmax]); ax.set_xticklabels([f'{xmin:g}', '1', '10', f'{xmax:g}'])
    ax.tick_params(labelsize=8, length=2, pad=1); ax.tick_params(axis='y', length=0)
    ax.xaxis.grid(True, color='#F0F2F4', lw=.5); ax.set_axisbelow(True)
    for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
    ax.set_xlabel('mean order error at zero\nmerge error (%, log scale)', fontsize=8, labelpad=1)
    ax.set_title('(a) Forced vs. chosen error', loc='left', fontsize=9, pad=3)


def plane(ax, n, first_row, first_col):
    be, bv, fx, fy, e0, base, proj, nu = series(n)
    top = nice_top(max(bv[0], e0[1]) * 1.08)
    ax.fill_between(be, 0, bv, step='pre', color=GREY, lw=0, zorder=1)
    ax.fill_between(be, 0, bv, step='pre', facecolor='none', edgecolor=HATCH, hatch='////', lw=0, zorder=1)
    ax.step(be, bv, where='pre', color='#333', lw=.6, zorder=2)
    ax.step(np.append(fx, 100), np.append(fy, fy[-1]), where='post', color=BLUE, lw=.9, zorder=3)
    ax.plot(pf.inv(0), e0[1], 'o', ms=3.2, color=BLUE, mec='white', mew=.4, zorder=8, clip_on=False)
    ax.plot(*proj, '*', ms=6, color='k', mec='white', mew=.3, zorder=8, clip_on=False)
    ax.set_xscale('function', functions=(pf.fwd, pf.inv)); ax.set_xlim(0, 65); ax.set_ylim(0, top)
    ax.set_xticks([0, 1, 5, 20, 65]); ax.set_xticklabels(['0', '1', '5', '20', '65'])
    ax.set_yticks([0, top / 2, top]); ax.set_yticklabels(['0', f'{top / 2:g}', f'{top:g}'])
    ax.spines['left'].set_position(('outward', 3))
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=8, length=2, pad=1); ax.yaxis.grid(True, color='#F0F2F4', lw=.5); ax.set_axisbelow(True)
    ax.set_title(LAB[n], loc='left', fontsize=8.5, pad=2)
    if first_col: ax.set_ylabel('order error (%)', fontsize=8, labelpad=1)
    if not first_row: ax.set_xlabel('worst merge error (%)', fontsize=8, labelpad=1)


def main():
    v.use_times()
    fig = plt.figure(figsize=(7.05, 2.95))
    ga = fig.add_gridspec(1, 1, left=.105, right=.325, bottom=.325, top=.915)
    forced(fig.add_subplot(ga[0, 0]))
    gb = fig.add_gridspec(2, 3, left=.45, right=.99, bottom=.325, top=.915, wspace=.42, hspace=.62)
    fig.text(.405, .958, '(b) What a merge budget releases', fontsize=9, ha='left', va='bottom')
    for k, n in enumerate(['Ring', 'Wildfires', 'Storms', 'PM25', 'Tangaroa', 'Cylinder']):
        plane(fig.add_subplot(gb[k // 3, k % 3]), n, k < 3, k % 3 == 0)
    h = [Patch(facecolor=GREY, edgecolor=HATCH, hatch='////', lw=0, label='unreachable: below the lower bound'),
         Line2D([], [], color='#9AA3AB', lw=.8, label='order error the tree does not force'),
         Line2D([], [], color=BLUE, marker='o', ms=3.4, ls='none', label=r'AnchorMTM order, $\varepsilon=0$'),
         Line2D([], [], color=BLUE, lw=.9, label=r'AnchorMTM order, $\varepsilon$ from 0 to 100%'),
         Line2D([], [], marker='s', ms=3.6, color=TM, ls='none', label='TMTM'),
         Line2D([], [], marker='D', ms=3.3, color=ST, ls='none', label='ST-MTM'),
         Line2D([], [], marker='*', ms=6, color='k', ls='none', label='projection (sorted by reference)')]
    fig.legend(handles=h, loc='lower center', bbox_to_anchor=(.5, -.02), ncol=3, fontsize=8, frameon=False,
               handlelength=1.6, columnspacing=1.3)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'forced_plane.{ext}', dpi=300)


if __name__ == '__main__':
    main()
