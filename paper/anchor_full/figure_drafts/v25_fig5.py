"""v25 redraw of paper Fig. 5, the position-topology plane (2026-11-09). Same saved data as v23_figures.fig5.

Changes requested by the user: the forced / not-forced labels no longer cover the data (each panel states the
not-forced share in its free upper-right corner, and a thin dashed segment at zero merge error marks the gap between
the bound and the lowest tree-keeping map); larger panels in two rows; the y axis is moved outward so that markers at
zero merge error are not drawn on the axis line; every marker is drawn above the bound and frontier lines.
Run from this folder:  python v25_fig5.py  ->  ../../pvis2027/latex_v21/figures/plane_compact.{pdf,svg}
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import v23_figures as v
pf = v.pf


def panel(ax, n):
    be, bv, fx, fy, pts = pf.series(n); nb = pf.BM['native'][n]
    tops = [x['best'] for x in nb.values()]
    if n in pf.BM['curves']: tops += [100 * c['NROE'] for c in pf.BM['curves'][n].values()]
    top = max(tops)
    ax.fill_between(be, 0, bv, step='pre', color=pf.GREY, lw=0, zorder=1)
    ax.fill_between(be, 0, bv, step='pre', facecolor='none', edgecolor=pf.HATCH, hatch='//////', lw=0, zorder=1)
    ax.fill_between([be[-1], pf.XMAX], 0, [bv[-1]] * 2, color=pf.GREY, lw=0, zorder=1)
    ax.step(be, bv, where='pre', color=pf.INK, lw=.8, zorder=2)
    ax.step(np.append(fx, pf.XMAX), np.append(fy, fy[-1]), where='post', color=pf.BLUE, lw=1.5, zorder=3)
    nu = bv[0]; lo = min(x['best'] for x in nb.values())
    ax.plot([0, 0], [nu, lo], ls=(0, (2, 1.5)), color='#7A838C', lw=.8, zorder=4, clip_on=False)
    ms = 4.4
    ax.plot(0, nb['TMTM']['best'], 's', ms=ms, color=pf.M['TMTM']['c'], mec='white', mew=.5, zorder=12, clip_on=False)
    ax.plot(0, nb['ST-MTM']['best'], 'D', ms=ms * .9, color=pf.M['ST-MTM']['c'], mec='white', mew=.5, zorder=12, clip_on=False)
    ax.plot(0, nb['OLO']['best'], '^', ms=ms * 1.15, mfc='none', mec='#8A7744', mew=.9, zorder=13, clip_on=False)
    if n in pf.BM['curves']:
        for key in ('Hilbert', 'Morton'):
            c = pf.BM['curves'][n][key]
            ax.plot(100 * c['NMLE_max'], 100 * c['NROE'], pf.M[key]['mk'], ms=ms + .6, color=pf.M[key]['c'], mec='white', mew=.5, zorder=12)
    ax.plot(100 * pf.FR[n]['NMLE_max'], 100 * pf.FR[n]['NROE'], '*', ms=ms * 1.9, color='k', mec='white', mew=.4, zorder=12, clip_on=False)
    for x, y, e in pts:
        if e == 0.:
            ax.plot(x, y, 'o', ms=4.0, color=pf.BLUE, mec='white', mew=.5, zorder=14, clip_on=False)
    share = [100 * (x['best'] - nu) / x['best'] for x in nb.values()]
    lo_s, hi_s = round(min(share)), round(max(share)); rng = f'{lo_s}%' if lo_s == hi_s else f'{lo_s}–{hi_s}%'
    ax.text(.98, .97, f'not forced by the tree:\n{rng} of the order error', transform=ax.transAxes,
            ha='right', va='top', fontsize=6.8, color='#3F474F', linespacing=1.15)
    ax.set_xscale('function', functions=(pf.fwd, pf.inv)); ax.set_xlim(0, pf.XMAX); ax.set_ylim(0, 1.32 * top)
    ax.set_xticks([0, 1, 5, 20, 60]); ax.set_xticklabels(['0', '1', '5', '20', '60'])
    ax.spines['left'].set_position(('outward', 5)); ax.spines['bottom'].set_position(('outward', 2))
    ax.tick_params(labelsize=7, pad=1.5)
    ax.yaxis.grid(True, color='#EEF0F2', lw=.5); ax.set_axisbelow(True)
    return dict(nu=round(float(nu), 3), share=[round(s, 1) for s in share], **{m: round(x['best'], 3) for m, x in nb.items()})


def main():
    v.use_times()
    fig = plt.figure(figsize=(7.05, 2.85))
    gs = fig.add_gridspec(2, 4, left=.065, right=.97, bottom=.11, top=.95, wspace=.33, hspace=.5)
    out = {}
    for k, n in enumerate(pf.NAMES):
        ax = fig.add_subplot(gs[k // 4, k % 4]); out[n] = panel(ax, n)
        ttl = {'PM2.5': r'PM$_{2.5}$ (daily)'}.get(n, n) + (' (3D)' if n in ('Tangaroa', 'Cylinder') else '')
        ax.set_title(ttl, loc='left', pad=3, fontsize=8)
        if k % 4 == 0: ax.set_ylabel('Mean order error (%)', fontsize=7.5)
        if k // 4 == 1 or k == 3: ax.set_xlabel('Worst merge error (% of scalar range)', fontsize=7.2, labelpad=1.5)
    lg = fig.add_subplot(gs[1, 3]); lg.axis('off')
    h = [Patch(facecolor=pf.GREY, edgecolor=pf.HATCH, hatch='//////', lw=0, label='unreachable: below the bound'),
         Line2D([], [], color=pf.BLUE, lw=1.5, label=r'AnchorMTM, $\varepsilon$ from 0 to 100%'),
         Line2D([], [], color=pf.BLUE, marker='o', ms=4, mec='white', ls='none', label=r'AnchorMTM, $\varepsilon=0$'),
         Line2D([], [], marker='s', ms=4.4, color=pf.M['TMTM']['c'], mec='white', ls='none', label='TMTM'),
         Line2D([], [], marker='D', ms=4, color=pf.M['ST-MTM']['c'], mec='white', ls='none', label='ST-MTM'),
         Line2D([], [], marker='^', ms=5, mfc='none', mec='#8A7744', mew=.9, ls='none', label='OLO'),
         Line2D([], [], marker='P', ms=5, color=pf.M['Hilbert']['c'], mec='white', ls='none', label='Hilbert curve'),
         Line2D([], [], marker='X', ms=5, color=pf.M['Morton']['c'], mec='white', ls='none', label='Morton curve'),
         Line2D([], [], marker='*', ms=7.5, color='k', ls='none', label='projection'),
         Line2D([], [], color='#7A838C', ls=(0, (2, 1.5)), lw=.8, label='order error not forced')]
    lg.legend(handles=h, loc='center left', bbox_to_anchor=(-.02, .5), fontsize=7, handlelength=1.6, labelspacing=.45, ncol=1)
    v.save(fig, 'plane_compact', bbox_inches='tight', pad_inches=.02)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
