"""v23 redraw of paper Figs. 4, 5 and 7 (2026-11-09): same saved data, clearer and literal marks.

Changes against v21/v22 (no data changed, no algorithm rerun):
  Fig. 4 (controlled trees): inset tree moved inside the axes (its labels no longer sit on the x axis),
          x ticks every 10%, headroom for the legend, 7 pt Times.
  Fig. 5 (position-topology plane): every marker at its measured coordinates (the former horizontal offsets
          of OLO/TMTM and Hilbert/Morton are removed); only the epsilon = 0 point of AnchorMTM is marked;
          short Storms labels with a white background; larger fonts.
  Fig. 7 (per-frame budget distribution): outliers drawn at their own x (no jitter); log axis extended to
          0.004% so the seven Storms frames below 0.1% appear at their values (no floor triangles).

Inputs are those of make_figure_drafts.fig_controlled_v2, plane_fig.compact and budget_distribution.main_figure_v22
(asserts tying the per-frame data to Table 2 are reused).
Run from this folder:  python v23_figures.py   ->  ../../pvis2027/latex_v21/figures/{anchor_controlled_bounds,plane_compact,budget_per_frame}.pdf
"""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.transforms import offset_copy

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'pvis2027/latex_v21/figures'
CODE = HERE.parents[2] / 'code/results'

import plane_fig as pf            # loads the saved plane, mirror and frontier data
import budget_distribution as bd  # loaders with the Table 2 checks


def use_times():
    for d in [Path('C:/Windows/Fonts'), Path('/System/Library/Fonts/Supplemental'), Path('/usr/share/fonts/truetype/msttcorefonts')]:
        for f in ['times.ttf', 'timesbd.ttf', 'timesi.ttf', 'Times New Roman.ttf', 'Times New Roman Bold.ttf', 'Times New Roman Italic.ttf']:
            if (d / f).exists(): font_manager.fontManager.addfont(str(d / f))
    plt.rcParams.update({'font.family': 'Times New Roman', 'mathtext.fontset': 'stix', 'font.size': 7,
                         'pdf.fonttype': 42, 'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.linewidth': .6, 'xtick.major.width': .6, 'ytick.major.width': .6,
                         'xtick.major.size': 2.2, 'ytick.major.size': 2.2, 'legend.frameon': False,
                         'axes.titleweight': 'normal', 'hatch.linewidth': .45})


def save(fig, stem, **kw):
    for ext in ('pdf', 'svg'):
        fig.savefig(OUT / f'{stem}.{ext}', **kw)
    fig.savefig(HERE / 'preview_v20' / f'{stem}.png', dpi=250, **kw)
    plt.close(fig)


# ------------------------------------------------------------------------------------------- Fig. 4
LEAF = {'A': '#D55E00', 'B': '#E69F00', 'C': '#5E3C99', 'D': '#B2ABD2'}
GRID = '#E3E7EA'; BLUE = '#0072B2'


def fig4():
    base = CODE / 'controlled_conflict20261030'
    ov = list(csv.DictReader((base / 'overlap.csv').open())); bu = list(csv.DictReader((base / 'budget.csv').open()))
    fig, axes = plt.subplots(1, 2, figsize=(3.45, 1.9), gridspec_kw=dict(wspace=.42))
    ax = axes[0]; sel = [r for r in ov if abs(float(r['width']) - .06) < 1e-9]
    d = np.array([float(r['overlap']) for r in sel]); f = lambda k: 100 * np.array([float(r[k]) for r in sel])
    ax.plot(100 * d, f('nu'), '--', color='#D55E00', lw=1, label=r'point bound $\nu^*$')
    ax.plot(100 * d, f('exact_tau'), '-', color=BLUE, lw=1.1, label='optimum over 24 orders')
    ax.plot(100 * d[::3], f('width_lower')[::3], 'o', ms=2.8, mfc='white', mec=BLUE, mew=.7, label='width bound (Thm. 2)')
    ax.set_xlim(-13, 31); ax.set_xticks([-10, 0, 10, 20, 30]); ax.set_ylim(-.6, 22)
    ax.set_xlabel('signed overlap $d$ (%)'); ax.set_ylabel('displacement (%)')
    ax.legend(fontsize=6.3, loc='upper left', handlelength=1.5, borderaxespad=.1, labelspacing=.25)
    ax.yaxis.grid(True, color=GRID, lw=.5); ax.set_axisbelow(True); ax.set_title('(a) Overlap forces displacement', fontsize=7.2, pad=2)
    # inset: the two sibling pairs, drawn entirely inside the lower-right corner of the axes
    ins = ax.inset_axes([.62, .05, .37, .33]); ins.set_xlim(0, 1); ins.set_ylim(0, 1.05); ins.axis('off')
    for k, xi in zip('ABCD', [.1, .37, .63, .9]):
        ins.plot([xi, xi], [.3, .62], color=LEAF[k], lw=1.3)
        ins.text(xi, .25, k, fontsize=6.3, ha='center', va='top', color=LEAF[k])
    ins.plot([.1, .37], [.62, .62], 'k', lw=.6); ins.plot([.63, .9], [.62, .62], 'k', lw=.6)
    ins.plot([.235, .235, .765, .765], [.62, .95, .95, .62], 'k', lw=.6)
    ax = axes[1]; levels = sorted({float(r['inner_level']) for r in bu}); cm = plt.get_cmap('viridis')
    for i, lv in enumerate(levels):
        s = [r for r in bu if float(r['inner_level']) == lv]; e = 100 * np.array([float(r['epsilon']) for r in s])
        t = 100 * np.array([float(r['tau']) for r in s]); h = 100 * float(s[0]['parent_gap']); c = cm(.15 + .7 * i / (len(levels) - 1))
        ax.step(e, t, where='post', color=c, lw=1.1)
        ax.text(h / 2 + .9, 6.5 + 1.7 * i, f'$h$ = {h:.0f}%', fontsize=6.3, color=c, rotation=90, va='center')
    ax.set_ylim(-.6, 15.5); ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))
    ax.set_xlabel(r'merge budget $\varepsilon$ (%)'); ax.set_ylabel('displacement (%)')
    ax.set_title(r'(b) Released at $\varepsilon=h/2$ (Thm. 3)', fontsize=7.2, pad=2)
    ax.yaxis.grid(True, color=GRID, lw=.5); ax.set_axisbelow(True)
    for a in axes: a.tick_params(labelsize=6.5, length=2, pad=1.5)
    save(fig, 'anchor_controlled_bounds', bbox_inches='tight', pad_inches=.02)
    return dict(d24=dict(nu=float(f('nu')[np.argmin(abs(d - .24))]), tau=float(f('exact_tau')[np.argmin(abs(d - .24))])))


# ------------------------------------------------------------------------------------------- Fig. 5
def plane_panel(ax, n, wide):
    be, bv, fx, fy, pts = pf.series(n); nb = pf.BM['native'][n]
    top = max(v['best'] for v in nb.values())
    if n in pf.BM['curves']: top = max(top, *(100 * v['NROE'] for v in pf.BM['curves'][n].values()))
    ax.fill_between(be, 0, bv, step='pre', color=pf.GREY, lw=0, zorder=1)
    ax.fill_between(be, 0, bv, step='pre', facecolor='none', edgecolor=pf.HATCH, hatch='//////', lw=0, zorder=1)
    ax.fill_between([be[-1], pf.XMAX], 0, [bv[-1]] * 2, color=pf.GREY, lw=0, zorder=1)
    ax.step(be, bv, where='pre', color=pf.INK, lw=.9, zorder=3)
    ax.step(np.append(fx, pf.XMAX), np.append(fy, fy[-1]), where='post', color=pf.BLUE, lw=1.3, zorder=4)
    for x, y, e in pts:                                   # only the Exact (epsilon = 0) point is marked
        if e == 0.:
            ax.plot(x, y, 'o', ms=3.2, color=pf.BLUE, mec='white', mew=.4, zorder=10, clip_on=False)
    ms = 3.9 if wide else 3.4
    # tree-keeping maps at their measured coordinates (zero merge error); hollow OLO stays visible under overlaps
    ax.plot(0, nb['TMTM']['best'], 's', ms=ms, color=pf.M['TMTM']['c'], mec='white', mew=.4, zorder=6, clip_on=False)
    ax.plot(0, nb['ST-MTM']['best'], 'D', ms=ms * .92, color=pf.M['ST-MTM']['c'], mec='white', mew=.4, zorder=6, clip_on=False)
    ax.plot(0, nb['OLO']['best'], '^', ms=ms * 1.15, mfc='none', mec='#9C8A5E', mew=.8, zorder=8, clip_on=False)
    if n in pf.BM['curves']:
        for key in ('Hilbert', 'Morton'):
            c = pf.BM['curves'][n][key]
            ax.plot(100 * c['NMLE_max'], 100 * c['NROE'], pf.M[key]['mk'], ms=ms + .4, color=pf.M[key]['c'], mec='white', mew=.4, zorder=6)
    ax.plot(100 * pf.FR[n]['NMLE_max'], 100 * pf.FR[n]['NROE'], '*', ms=(ms + .5) * 1.45, color='k', zorder=6, clip_on=False)
    ax.set_xscale('function', functions=(pf.fwd, pf.inv)); ax.set_xlim(0, pf.XMAX); ax.set_ylim(0, 1.13 * top)
    ax.set_xticks([0, 5, 20, 60]); ax.set_xticklabels(['0', '5', '20', '60'])
    ax.tick_params(labelsize=6.5, pad=1.5); ax.tick_params(axis='y', pad=3)
    ax.yaxis.grid(True, color='#EEF0F2', lw=.5); ax.set_axisbelow(True)
    return bv[0], nb


def fig5():
    fig = plt.figure(figsize=(7.05, 2.0))
    gs = fig.add_gridspec(1, 7, width_ratios=[1.5, 1, 1, 1, 1, 1, 1], left=.06, right=.995, bottom=.2, top=.79, wspace=.42)
    out = {}
    for k, n in enumerate(pf.NAMES):
        ax = fig.add_subplot(gs[0, k]); nu, nb = plane_panel(ax, n, k == 0)
        ttl = {'PM2.5': r'PM$_{2.5}$ (daily)'}.get(n, n) + (' (3D)' if n in ('Tangaroa', 'Cylinder') else '')
        ax.set_title(ttl, loc='left', pad=2.5, fontsize=7.5)
        out[n] = dict(nu=round(nu, 3), **{m: round(v['best'], 3) for m, v in nb.items()})
        if k == 0:
            lo = min(v['best'] for v in nb.values()); share = [100 * (v['best'] - nu) / v['best'] for v in nb.values()]
            ax.plot([0, 0], [0, nu], color=pf.INK, lw=3.0, solid_capstyle='butt', zorder=8, clip_on=False)
            ax.plot([0, 0], [nu, lo], color=pf.HATCH, lw=3.0, solid_capstyle='butt', zorder=8, clip_on=False)
            off = offset_copy(ax.transData, fig=fig, x=6, y=0, units='points')
            box = dict(boxstyle='square,pad=0.12', fc='white', ec='none')
            ax.text(0, (nu + lo) / 2, f'not forced: {min(share):.0f}\u2013{max(share):.0f}%', transform=off, fontsize=6.5,
                    va='center', color='#5F6870', zorder=9, bbox=box)
            ax.text(0, nu / 2, r'forced: $\nu^*$', transform=off, fontsize=6.5, va='center', color=pf.INK, zorder=9, bbox=box)
            ax.set_ylabel('Mean order error (%)', fontsize=7.5)
            ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
            out['share'] = [round(s, 1) for s in share]
    fig.text(.53, .025, 'Worst merge error over frames (% of scalar range, square-root scale)', ha='center', fontsize=7.5)
    h = [Patch(facecolor=pf.GREY, edgecolor=pf.HATCH, hatch='//////', lw=0, label='below the bound'),
         Line2D([], [], color=pf.BLUE, lw=1.3, label=r'AnchorMTM, $\varepsilon$ = 0$-$100%'),
         Line2D([], [], color=pf.BLUE, marker='o', ms=3.2, mec='white', mew=.4, ls='none', label=r'AnchorMTM, $\varepsilon$ = 0'),
         Line2D([], [], marker='s', ms=3.8, color=pf.M['TMTM']['c'], mec='white', ls='none', label='TMTM'),
         Line2D([], [], marker='D', ms=3.5, color=pf.M['ST-MTM']['c'], mec='white', ls='none', label='ST-MTM'),
         Line2D([], [], marker='^', ms=4.3, mfc='none', mec='#9C8A5E', mew=.8, ls='none', label='OLO'),
         Line2D([], [], marker='P', ms=4.2, color=pf.M['Hilbert']['c'], mec='white', ls='none', label='Hilbert'),
         Line2D([], [], marker='X', ms=4.2, color=pf.M['Morton']['c'], mec='white', ls='none', label='Morton'),
         Line2D([], [], marker='*', ms=6, color='k', ls='none', label='Projection')]
    fig.legend(handles=h, ncol=9, loc='upper center', bbox_to_anchor=(.53, 1.02), fontsize=7, handlelength=1.4,
               columnspacing=1.0, handletextpad=.35)
    save(fig, 'plane_compact')
    return out


# ------------------------------------------------------------------------------------------- Fig. 7
def boxes_log(ax, xs, samples, styles, width=.64):
    """Box: quartiles; whiskers: 5th-95th percentiles; dots: every frame outside the whiskers, at its own x and value;
    diamond: mean (= NPE)."""
    for x, v, (fill, edge, med_c, lw) in zip(xs, samples, styles):
        v = np.asarray(v, float); p5, q1, med, q3, p95 = np.percentile(v, [5, 25, 50, 75, 95])
        ax.add_patch(plt.Rectangle((x - width / 2, q1), width, q3 - q1, fc=fill, ec=edge, lw=lw, zorder=3))
        ax.plot([x - width / 2, x + width / 2], [med] * 2, color=med_c, lw=1.0, zorder=4, solid_capstyle='butt')
        for a, b in ((p95, q3), (p5, q1)):
            ax.plot([x, x], [a, b], color=bd.NAVY, lw=.5, zorder=2)
            ax.plot([x - width / 4, x + width / 4], [a] * 2, color=bd.NAVY, lw=.5, zorder=2)
        o = v[(v > p95) | (v < p5)]
        ax.scatter(np.full(len(o), x), o, s=2.0, color=bd.MID, alpha=.45, lw=0, zorder=2)
        ax.scatter([x], [v.mean()], marker='D', s=11, fc='white', ec='black', lw=.55, zorder=5)


def fig7():
    import pandas as pd
    st = bd.load_planar('Storms'); pm = bd.load_pm25()
    vol = pd.read_csv(bd.SWEEP / 'volume_per_frame_audit.csv'); assert vol.rendered_budget_ok.all()
    EP, EV = [0, 1, 2, 5, 10, 20], [0, 2, 5, 10, 20]
    panels = [('Storms (2D, 744 frames)', EP, {e: 100 * st[e].NPE.to_numpy() for e in EP}, {e: st[e].topology_max.to_numpy() for e in EP}, 10),
              (r'PM$_{2.5}$ hourly (2D, 744 frames)', EP, {e: 100 * pm[e].E_max.to_numpy() for e in EP}, {e: pm[e].NMLE_max.to_numpy() for e in EP}, 5)]
    for n in ['Tangaroa', 'Cylinder']:
        g = vol[vol.dataset == n]; nf = g.frame.nunique()
        gg = {e: g[np.isclose(g.epsilon, e / 100)].sort_values('frame') for e in EV}
        for e in EV:
            assert len(gg[e]) == nf and (gg[e].NMLE_max <= e / 100 + 1e-6).all()
        panels.append((f'{n} (3D, {nf} frames)', EV, {e: 100 * gg[e].E_max.to_numpy() for e in EV}, {e: gg[e].NMLE_max.to_numpy() for e in EV}, None))
    lo = min(min(v.min() for v in p[2].values()) for p in panels); assert lo > .004, lo
    fig = plt.figure(figsize=(7.0, 1.9))
    gs = fig.add_gridspec(1, 5, width_ratios=[6, 6, .3, 5, 5], wspace=.1)
    stats = {}
    for k, (slot, (title, E, disp, merr, sel)) in enumerate(zip([0, 1, 3, 4], panels)):
        ax = fig.add_subplot(gs[0, slot]); pos = np.arange(len(E))
        sty = [(bd.NAVY, bd.NAVY, 'white', .5) if e == 0 else (bd.PALE, bd.SEL, bd.NAVY, 1.1) if e == sel else (bd.PALE, bd.MID, bd.NAVY, .5) for e in E]
        boxes_log(ax, pos, [disp[e] for e in E], sty)
        ax.set_yscale('log'); ax.set_ylim(.004, 70)
        ax.set_yticks([.01, .1, 1, 10]); ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.set_yticklabels(['0.01', '0.1', '1', '10'] if k == 0 else [])
        ax.yaxis.grid(True, color=bd.GRID, lw=.4); ax.set_axisbelow(True)
        ax.set_xlim(-.6, len(E) - .4); ax.set_xticks(pos); ax.set_xticklabels([f'{e:g}' for e in E]); ax.tick_params(pad=1.5, labelsize=6.8)
        ax.set_title(title, pad=2.5, fontsize=7.5)
        if sel is not None:
            ax.text(E.index(sel), 48, 'Table 2', ha='center', va='center', fontsize=6.5, color=bd.SEL, zorder=6)
        used = {e: int((merr[e] > 1e-6).sum()) for e in E}; nf = len(merr[E[0]])
        for i, e in enumerate(E):
            pct = 100 * used[e] / nf; lab = '>99%' if 99 < pct < 100 and round(pct) == 100 else f'{pct:.0f}%'
            ax.text(i, -.21, lab, transform=ax.get_xaxis_transform(), ha='center', va='top', fontsize=6.2, color=bd.SEL if e == sel else '#444444')
        if k == 0:
            ax.set_ylabel('Worst displacement per frame\n(% of axis length)', labelpad=2, fontsize=7, linespacing=1.0)
            ax.text(-.03, -.035, r'budget $\varepsilon$ (%)', transform=ax.transAxes, ha='right', va='top', fontsize=6.6)
            ax.text(-.03, -.21, 'frames using it', transform=ax.transAxes, ha='right', va='top', fontsize=6.6, color='#444444')
        q = lambda e, p: round(float(np.percentile(disp[e], p)), 2)
        stats[title] = {f'{e:g}': dict(median=q(e, 50), p90=q(e, 90), max=round(float(disp[e].max()), 2), mean=round(float(disp[e].mean()), 4),
                                       used=f'{used[e]}/{nf}', merge_max=round(100 * float(merr[e].max()), 3)) for e in E}
    fig.subplots_adjust(left=.093, right=.997, top=.86, bottom=.25)
    save(fig, 'budget_per_frame', bbox_inches='tight', pad_inches=.015)
    return stats


if __name__ == '__main__':
    import json
    use_times()
    s4 = fig4(); s5 = fig5(); s7 = fig7()
    print(json.dumps(dict(fig4=s4, fig5=s5, fig7={k: {e: v for e, v in d.items() if e in ('0', '5', '10', '20')} for k, d in s7.items()}), indent=1))
