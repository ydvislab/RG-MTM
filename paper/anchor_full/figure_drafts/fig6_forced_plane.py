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
from fig_plane_her import series as series_v33, OUT, FIG, PANELS, GREY, HATCH, BLUE, TM, ST
V35 = FIG / 'volumes_v35'   # v35: Tangaroa along the streamwise x axis (volumes_v35.py figs Tangaroa x)


def series(n):
    f = V35 / f'{n.lower()}_x_plane.json'
    if n != 'Tangaroa' or not f.exists(): return series_v33(n)
    d = json.loads(f.read_text()); be = 100 * np.array(d['bound']['epsilon']); bv = 100 * np.array(d['bound']['envelope'])
    pts = sorted((100 * b['NMLE_max'], 100 * b['NROE_mean'], b['epsilon']) for b in d['construction']); fx, fy = [], []
    for x, y, e in pts:
        if not fy or y < fy[-1] - 1e-12: fx.append(x); fy.append(y)
    e0 = next((x, y) for x, y, e in pts if e == 0.)
    base = {m: 100 * v['best'] for m, v in d['baselines_NROE'].items()}
    return be, bv, np.array(fx), np.array(fy), e0, base, (100 * d['projection_NMLE_max'], 0.), bv[0]
_series = series


def series(n):
    # v36: the bound at the data resolution eps0, as the maps use (only Cylinder differs: 12.2% strict, 7.7% at eps0)
    r = _series(n)
    if n != 'Cylinder': return r
    be, bv, fx, fy, e0, base, proj, nu = r
    nu0 = 100 * json.loads((FIG / 'reference_direction20261027/cylinder.json').read_text())['key_directions']['stored']['nu_mean']
    return be, np.minimum(bv, nu0), fx, np.minimum(fy, nu0), (e0[0], min(e0[1], nu0)), base, proj, nu0


# Final worst displacement NPE (% of the axis, Table 1): TMTM, ST-MTM, AnchorMTM Exact
NPE = {'Ring': (17.56, 24.63, 4.71), 'Wildfires': (22.80, 31.80, 1.31), 'Storms': (57.53, 45.79, 3.99), 'PM25': (52.41, 55.77, 13.90),
       'Tangaroa': (38.66, 32.86, 8.61), 'Cylinder': (47.69, 51.60, 9.18)}
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
    xmin, xmax = .1, 60.; rows = ROWS; data = {n: series(n) for n in rows}; dy = .2
    trans = ax.get_yaxis_transform()
    span = lambda v: f'{v[0]:.0f}%' if round(v[0]) == round(v[1]) else f'{v[0]:.0f}\u2013{v[1]:.0f}%'
    for r, n in enumerate(rows):
        be, bv, fx, fy, e0, base, proj, nu = data[n]; y = len(rows) - 1 - r; yo, yp = y + dy, y - dy
        ax.add_patch(plt.Rectangle((xmin, y - .4), nu - xmin, .8, facecolor=GREY, edgecolor=HATCH, hatch='////', lw=0, zorder=1))
        ax.plot([nu] * 2, [y - .4, y + .4], color='#333', lw=.6, zorder=2)
        ax.plot([nu, max(base.values())], [yo, yo], color='#9AA3AB', lw=.8, zorder=3, solid_capstyle='butt')
        ax.plot(e0[1], yo, 'o', ms=3.6, color=BLUE, mec='white', mew=.4, zorder=6, clip_on=False)
        ax.plot(base['TMTM'], yo, 's', ms=3.7, color=TM, mec='white', mew=.4, zorder=6)
        ax.plot(base['ST-MTM'], yo, 'D', ms=3.4, color=ST, mec='white', mew=.4, zorder=7, clip_on=False)
        t, st, a = NPE[n]
        ax.plot([nu, max(t, st)], [yp, yp], color='#9AA3AB', lw=.8, ls=(0, (1.5, 1.2)), zorder=3)
        ax.plot(a, yp, 'o', ms=3.6, mfc='white', mec=BLUE, mew=.8, zorder=6)
        ax.plot(t, yp, 's', ms=3.5, mfc='white', mec=TM, mew=.8, zorder=6)
        ax.plot(st, yp, 'D', ms=3.3, mfc='white', mec=ST, mew=.8, zorder=7, clip_on=False)
        so = sorted(100 * (b - nu) / b for b in base.values()); sp = sorted(100 * (b - nu) / b for b in (t, st))
        ax.text(1.03, y, span(so), transform=trans, ha='left', va='center', fontsize=7.6, color='#3F474F')
        ax.text(1.36, y, span(sp), transform=trans, ha='left', va='center', fontsize=7.6, color='#3F474F')
        print(n, f'nu*={nu:.2f}', 'order', {m: round(v, 2) for m, v in base.items()}, 'share order', [round(v, 1) for v in so], 'share NPE', [round(v, 1) for v in sp])
    top = len(rows) - .4
    ax.text(1.03, top + .05, 'order', transform=trans, ha='left', va='bottom', fontsize=7.6, color='#3F474F')
    ax.text(1.36, top + .05, 'NPE', transform=trans, ha='left', va='bottom', fontsize=7.6, color='#3F474F')
    ax.text(1.03, top + .62, 'not forced', transform=trans, ha='left', va='bottom', fontsize=7.6, color='#3F474F')
    ax.set_xscale('log'); ax.set_ylim(-.6, top)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([LAB[n] for n in rows][::-1], fontsize=8)
    ax.set_xlim(xmin, xmax); ax.set_xticks([xmin, 1, 10, xmax]); ax.set_xticklabels([f'{xmin:g}', '1', '10', f'{xmax:g}'])
    ax.tick_params(labelsize=8, length=2, pad=1); ax.tick_params(axis='y', length=0)
    ax.xaxis.grid(True, color='#F0F2F4', lw=.5); ax.set_axisbelow(True)
    for sp_ in ('top', 'right', 'left'): ax.spines[sp_].set_visible(False)
    ax.set_xlabel('error at zero merge error\n(% of axis, log scale)', fontsize=8, labelpad=1)


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
    fig = plt.figure(figsize=(7.05, 2.8))
    ga = fig.add_gridspec(1, 1, left=.105, right=.30, bottom=.325, top=.865)
    forced(fig.add_subplot(ga[0, 0]))
    gb = fig.add_gridspec(2, 3, left=.487, right=.99, bottom=.325, top=.865, wspace=.42, hspace=.62)
    fig.text(.012, .955, '(a) Forced and chosen error', fontsize=9, ha='left', va='bottom')
    fig.text(.43, .955, '(b) What a merge budget releases', fontsize=9, ha='left', va='bottom')
    for k, n in enumerate(['Ring', 'Wildfires', 'Storms', 'PM25', 'Tangaroa', 'Cylinder']):
        plane(fig.add_subplot(gb[k // 3, k % 3]), n, k < 3, k % 3 == 0)
    h = [Patch(facecolor=GREY, edgecolor=HATCH, hatch='////', lw=0, label='unreachable: below the lower bound'),
         Line2D([], [], color='#9AA3AB', lw=.8, label='order error the tree does not force'),
         Line2D([], [], color=BLUE, marker='o', ms=3.4, ls='none', label=r'AnchorMTM order, $\varepsilon=0$'),
         Line2D([], [], color=BLUE, lw=.9, label=r'AnchorMTM order, $\varepsilon$ from 0 to 100%'),
         Line2D([], [], marker='o', ms=3.6, mfc='white', mec='#555', mew=.8, ls='none', label='hollow: final displacement (NPE)'),
         Line2D([], [], marker='s', ms=3.6, color=TM, ls='none', label='TMTM'),
         Line2D([], [], marker='D', ms=3.3, color=ST, ls='none', label='ST-MTM'),
         Line2D([], [], marker='*', ms=6, color='k', ls='none', label='projection (sorted by reference)')]
    fig.legend(handles=h, loc='lower center', bbox_to_anchor=(.5, -.02), ncol=3, fontsize=8, frameon=False,
               handlelength=1.6, columnspacing=1.3)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'forced_plane.{ext}', dpi=300)


if __name__ == '__main__':
    main()
