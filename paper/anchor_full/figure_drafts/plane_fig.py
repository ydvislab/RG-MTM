"""Fig. 3 of the v16 framework draft: the position-topology plane (order model).

One sentence: no map can enter the grey region; topology-preserving maps sit far above it,
and maps that follow the bounds run along its edge.

Inputs (saved, read only):
  ../figdata/plane20261108/<seq>.json        certified boundary and construction (plane_data.py)
  ../figdata/orientation20261106/best_mirror.json   TMTM, ST-MTM, OLO (best mirror, NROE);
                                                     Hilbert, Morton (best orientation, NROE, worst NMLE)
  ../figdata/frontier20261027/<seq>.json      projection (worst NMLE, NROE), same values as Fig. 4(b)
Output: ../../pvis2027/figures/fw_plane.{pdf,png}; numbers used are printed.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.transforms import offset_copy
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata'; OUT = HERE.parents[1] / 'pvis2027/figures'
NAMES = ['Storms', 'Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
FILE = {n: n.replace('.', '').lower() for n in NAMES}
LABEL = {n: (r'PM$_{2.5}$' if n == 'PM2.5' else n) for n in NAMES}
load = lambda p: json.loads(Path(p).read_text())
P = {n: load(RES / f'plane20261108/{FILE[n]}.json') for n in NAMES}
BM = load(RES / 'orientation20261106/best_mirror.json')
FR = {n: load(RES / f'frontier20261027/{FILE[n]}.json')['methods']['projection'] for n in NAMES}

# paper palette (make_figure_drafts.py); curves added in vermillion
M = {'OLO': dict(c='#C9B68C', mk='^'), 'TMTM': dict(c='#7B8790', mk='s'), 'ST-MTM': dict(c='#CC79A7', mk='D'),
     'Hilbert': dict(c='#D55E00', mk='P'), 'Morton': dict(c='#D55E00', mk='X'), 'Projection': dict(c='#000000', mk='*')}
BLUE = '#0072B2'; GREY = '#D9DDE1'; HATCH = '#AEB5BC'; INK = '#222222'
plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'pdf.fonttype': 42, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.linewidth': .6, 'xtick.major.width': .6, 'ytick.major.width': .6,
                     'xtick.major.size': 2.2, 'ytick.major.size': 2.2, 'legend.frameon': False, 'hatch.linewidth': .45,
                     'axes.titlesize': 7.2, 'axes.titleweight': 'bold', 'mathtext.fontset': 'dejavusans'})
XMAX = 62.; XT = [0, 1, 5, 10, 20, 40, 60]
fwd = lambda x: np.sqrt(np.clip(x, 0, None)); inv = lambda y: np.square(y)


def series(n):
    d = P[n]
    be = 100 * np.array(d['bound']['epsilon']); bv = 100 * np.array(d['bound']['envelope'])
    pts = sorted((100 * b['NMLE_max'], 100 * b['NROE_mean'], b['epsilon']) for b in d['construction'])
    # attained frontier: for merge error <= x the construction reaches min{y_k : x_k <= x}
    xs, ys, best = [], [], np.inf
    for x, y, _ in pts:
        if y < best - 1e-12: xs.append(x); ys.append(y); best = y
    return be, bv, np.array(xs), np.array(ys), pts


def mark(ax, x, y, key, ms, dx=0., z=6, clip=False):
    s = M[key]; tr = offset_copy(ax.transData, fig=ax.figure, x=dx, y=0, units='points')
    ms = ms * (1.2 if s['mk'] == '^' else 1)
    ax.plot([x], [y], marker=s['mk'], ms=ms * (1.45 if s['mk'] == '*' else 1), color=s['c'], mfc=s['c'],
            mec='k' if s['mk'] == '*' else 'white', mew=.3 if s['mk'] == '*' else .4, ls='none', transform=tr,
            zorder=z, clip_on=clip)


def panel(ax, n, hero=False):
    be, bv, fx, fy, pts = series(n); nb = BM['native'][n]
    top = max(v['best'] for v in nb.values())
    if n in BM['curves']: top = max(top, *(100 * v['NROE'] for v in BM['curves'][n].values()))
    ymax = 1.13 * top
    # unreachable region below the certified boundary: value on (be[i-1], be[i]] is bv[i] (conservative)
    ax.fill_between(be, 0, bv, step='pre', color=GREY, lw=0, zorder=1)
    ax.fill_between(be, 0, bv, step='pre', facecolor='none', edgecolor=HATCH, hatch='//////', lw=0, zorder=1)
    ax.fill_between([be[-1], XMAX], 0, [bv[-1]] * 2, color=GREY, lw=0, zorder=1)
    ax.step(be, bv, where='pre', color=INK, lw=.9, zorder=3)
    # attained frontier of the construction (steps-post), extended to the right edge
    ax.step(np.append(fx, XMAX), np.append(fy, fy[-1]), where='post', color=BLUE, lw=1.3, zorder=4,
            solid_joinstyle='miter')
    lab = [p for p in pts if p[2] in (0., .05, .2)] if hero else [p for p in pts if p[2] == 0.]
    for x, y, e in lab:
        ax.plot(x, y, 'o', ms=3.2 if hero else 2.6, color=BLUE, mec='white', mew=.4, zorder=7, clip_on=False)
    # topology-preserving maps at zero merge error (small horizontal offsets only to avoid overlap)
    for key, dx in (('OLO', -2.6), ('ST-MTM', 0.), ('TMTM', 2.6)):
        mark(ax, 0., nb[key]['best'], key, 3.8 if hero else 3.1, dx)
    if n in BM['curves']:
        for key in ('Hilbert', 'Morton'):
            c = BM['curves'][n][key]; mark(ax, 100 * c['NMLE_max'], 100 * c['NROE'], key, 4.0 if hero else 3.4,
                                           dx=(-2.2 if key == 'Hilbert' else 2.2))
    mark(ax, 100 * FR[n]['NMLE_max'], 100 * FR[n]['NROE'], 'Projection', 4.0 if hero else 3.4)
    ax.set_xscale('function', functions=(fwd, inv)); ax.set_xlim(0, XMAX); ax.set_ylim(0, ymax)
    ax.set_xticks(XT); ax.set_xticklabels([str(t) for t in XT])
    ax.tick_params(labelsize=6.2 if hero else 5.6, pad=1.5)
    ax.tick_params(axis='y', pad=4.5)
    ax.yaxis.grid(True, color='#EEF0F2', lw=.5); ax.set_axisbelow(True)
    ax.set_title(LABEL[n], loc='left', pad=2.5, fontsize=7.6 if hero else 6.8)
    return dict(be=be, bv=bv, fx=fx, fy=fy, pts=pts, ymax=ymax, nb=nb)


def annotate_hero(ax, s):
    nu = s['bv'][0]; nb = s['nb']; lo = min(v['best'] for v in nb.values())
    share = [100 * (v['best'] - nu) / v['best'] for v in nb.values()]
    off = lambda dx, dy=0: offset_copy(ax.transData, fig=ax.figure, x=dx, y=dy, units='points')
    # ledger at zero merge error, drawn on the axis itself: forced (black) and not forced (grey)
    ax.plot([0, 0], [0, nu], color=INK, lw=3.0, solid_capstyle='butt', zorder=8, clip_on=False)
    ax.plot([0, 0], [nu, lo], color=HATCH, lw=3.0, solid_capstyle='butt', zorder=8, clip_on=False)
    ax.text(0, (nu + lo) / 2, f'not forced:\n{min(share):.0f}\u2013{max(share):.0f}% of their\norder error',
            transform=off(8), fontsize=6.0, va='center', color='#5F6870', linespacing=1.05, zorder=9)
    ax.annotate(r'forced by the tree, $\nu^*$', (0, .62 * nu), xytext=(.55, 6.4), fontsize=6.0, color=INK,
                va='center', zorder=9, arrowprops=dict(arrowstyle='-', lw=.5, color=INK, shrinkA=1, shrinkB=1.5,
                                                      connectionstyle='angle,angleA=180,angleB=60,rad=0'))
    order = sorted(('OLO', 'ST-MTM', 'TMTM'), key=lambda k: nb[k]['best'])
    for j, k in enumerate(order):
        ax.annotate(k, (0, nb[k]['best']), xytext=(8, (j - 1) * 5.0 + (2 if k == 'TMTM' else 0)),
                    textcoords='offset points', fontsize=6.0, va='center',
                    color=M[k]['c'] if k != 'OLO' else '#9C8A5E', zorder=9)
    ax.text(1.25, .42, 'unreachable', fontsize=6.2, color='#4A525A', style='italic', zorder=9)
    for x, y, e in [p for p in s['pts'] if p[2] in (.05, .2)]:
        ax.annotate(r'$\varepsilon=$' + f'{100 * e:g}%', (x, y), xytext=(3, 3.5), textcoords='offset points',
                    fontsize=5.8, color=BLUE, zorder=9)
    ax.text(11.0, 3.3, 'AnchorMTM', fontsize=6.2, color=BLUE, zorder=9, linespacing=1.05)
    c = BM['curves']['Storms']
    ax.annotate('space-filling curves\nbreak the tree', (100 * c['Hilbert']['NMLE_max'], 100 * c['Hilbert']['NROE']),
                xytext=(0, 9), textcoords='offset points', fontsize=6.0, color=M['Hilbert']['c'], ha='center',
                va='bottom', linespacing=1.05)
    ax.annotate('projection', (100 * FR['Storms']['NMLE_max'], 0), xytext=(-3, 15), textcoords='offset points',
                fontsize=6.0, ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-', lw=.5, color=INK, shrinkA=1, shrinkB=3.5))
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))


def main():
    fig = plt.figure(figsize=(7.05, 3.05))
    gs = fig.add_gridspec(2, 4, width_ratios=[1.42, 1, 1, 1], left=.115, right=.995, bottom=.12, top=.86,
                          wspace=.33, hspace=.52)
    hero = fig.add_subplot(gs[:, 0]); s = panel(hero, 'Storms', hero=True); annotate_hero(hero, s)
    hero.set_ylabel('Mean order error NROE (% of axis)', fontsize=6.6)
    hero.set_xlabel('Worst merge error NMLE (% of scalar range)', fontsize=6.6)
    small = ['Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
    for k, n in enumerate(small):
        ax = fig.add_subplot(gs[k // 3, 1 + k % 3]); panel(ax, n)
        if k >= 3: ax.set_xlabel('Worst merge error (%)', fontsize=6.0)
    h = [Patch(facecolor=GREY, edgecolor=HATCH, hatch='//////', lw=0, label='below the bound (unreachable)'),
         Line2D([], [], color=BLUE, lw=1.3, marker='o', ms=2.8, mec='white', mew=.4,
                label=r'AnchorMTM ($\varepsilon$ = 0$-$100%)')]
    for k in ('OLO', 'TMTM', 'ST-MTM', 'Hilbert', 'Morton', 'Projection'):
        s_ = M[k]; h.append(Line2D([], [], marker=s_['mk'], ms=3.6 * (1.45 if s_['mk'] == '*' else 1), color=s_['c'],
                                   mec='k' if s_['mk'] == '*' else 'white', mew=.3, ls='none', label=k))
    fig.legend(handles=h, ncol=8, loc='upper center', bbox_to_anchor=(.54, 1.0), fontsize=6.1, handlelength=1.4,
               columnspacing=.95, handletextpad=.4)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / 'fw_plane.pdf'); fig.savefig(OUT / 'fw_plane.png', dpi=250); plt.close(fig)
    for n in P:
        be, bv, fx, fy, pts = series(n); nb = BM['native'][n]
        print(f"{n:9s} nu*={bv[0]:5.2f}  OLO/TMTM/ST {nb['OLO']['best']:5.2f}/{nb['TMTM']['best']:5.2f}/{nb['ST-MTM']['best']:5.2f}"
              f"  proj NMLE {100 * FR[n]['NMLE_max']:4.1f}", ' curves' if n in BM['curves'] else '',
              {k: (round(100 * v['NMLE_max'], 1), round(100 * v['NROE'], 2)) for k, v in BM['curves'].get(n, {}).items()})


if __name__ == '__main__':
    main()
