"""v28 paper figure: rendered merge tree maps with the references overlaid (2026-11-09).

Rows: planar bound sequences. Columns: three source snapshots, then TMTM, ST-MTM, AnchorMTM eps = 0 and 5%.
Every map is the rendered scalar profile stack (render_gallery_maps.py); white dots are the references q of every
extremum in every frame, i.e. where a map whose axis encodes location should draw it. Native maps are shown in the
mirror chosen by planar_gallery_data.py and stretched to the canvas, as in the position figure of the supplement.
Labels: mean displacement over all features and NPE (mean worst displacement per frame), from planar_gallery20261109.
Run:  python map_gallery_fig.py [OLR Ring Wildfires]  ->  ../../pvis2027/latex_v21/figures/map_gallery.{pdf,png}
"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import v23_figures as v
import stmtm_threshold as sth
TRACK_COLORS = ['#00E5FF', '#7CFC00', '#FF4FD8']   # cyan, green, magenta: visible on both colour maps
K = 2
MARKERS = ['o', 's']

HERE = Path(__file__).resolve().parent; FIGD = HERE.parent / 'figdata'
OUT = HERE.parents[1] / 'pvis2027/latex_v21/figures'
CMAP = {'Storms': ('RdBu_r', 'SLP (hPa)'), 'OLR': ('RdBu_r', r'OLR (W m$^{-2}$)'), 'Ring': ('magma', 'intensity'), 'Wildfires': ('inferno', r'log(1+FRP)'),
        'PM2.5': ('YlOrRd', r'PM$_{2.5}$')}
LAB = {'Storms': 'Storms', 'OLR': 'OLR', 'Ring': 'Ring', 'Wildfires': 'Wildfires', 'PM2.5': r'PM$_{2.5}$ (daily)'}
DOT = {'Ring': 3.4, 'Wildfires': 2.2, 'OLR': 1.5, 'PM2.5': .8}
COLS = [('TMTM', 'TMTM'), ('ST-MTM', 'ST-MTM'), ('eps=0', r'AnchorMTM, $\varepsilon=0$'), ('eps=0.05', r'AnchorMTM, $\varepsilon=5\%$')]


def stats(name):
    d = json.loads((FIGD / f'planar_gallery20261109/{name.lower().replace(".", "")}.json').read_text()); L = d['canvas']; o = d['origin']
    Q = [(np.asarray(q) - o) / L for q in d['q']]; out = {}
    for k in ('TMTM', 'ST-MTM', 'eps=0', 'eps=0.05'):
        X = [(np.asarray(x) - o) / L for x in d['maps'][k]['x']]
        out[k] = (100 * np.mean(np.concatenate([abs(a - b) for a, b in zip(X, Q)])), 100 * np.mean([np.max(abs(a - b)) for a, b in zip(X, Q)]))
    return out


def tracks(name, q, o, L, jump=.12):
    """The K most significant tracked features, by one rule for every sequence: extrema on the domain boundary are
    excluded; a track is cut where its reference jumps by more than `jump` of the axis between consecutive frames
    (a likely identity swap); each continuous segment scores the sum over its frames of the leaf-arc persistence
    |h(parent saddle) - h(extremum)|, i.e. lifetime x mean persistence."""
    ds = sth.dataset(sth.KEYS[name]); sc = ds['sc']; life = {}
    for t, (ids, tr, bd) in enumerate(zip(sc['ids'], sc['tracks'], sc['boundary'])):
        fr = sc['frames'][t]; vals = np.asarray(fr.values, float)
        for j, k in enumerate(tr):
            if bd[j]: continue
            leaf = ids[j]; par = fr.parent(leaf)
            life.setdefault(int(k), []).append((t, j, abs(vals[par] - vals[leaf]) if par is not None else 0.))
    segs = []
    for k, items in life.items():
        cur = [items[0]]
        for a in items[1:]:
            qa, qb = (float(q[cur[-1][0]][cur[-1][1]]) - o) / L, (float(q[a[0]][a[1]]) - o) / L
            if a[0] == cur[-1][0] + 1 and abs(qa - qb) <= jump: cur.append(a)
            else: segs.append((k, cur)); cur = [a]
        segs.append((k, cur))
    segs.sort(key=lambda s: -sum(x[2] for x in s[1])); out = []
    for k, seg in segs[:K]:
        tt = np.array([t for t, j, _ in seg])
        xy = np.array([np.asarray(sc['frames'][t].coordinates)[list(sc['ids'][t])][j] for t, j, _ in seg])
        qq = np.array([float(q[t][j]) for t, j, _ in seg])
        out.append(dict(id=k, t=tt, q=qq, xy=xy))
    return out, (ds['lo'], ds['hi'])


def mark(ax, x, y, k, ms=3.8):
    m = MARKERS[k]
    ax.plot(x, y, m, ms=ms + 1.6, mfc='none', mec='black', mew=1.5, zorder=6, clip_on=False)
    ax.plot(x, y, m, ms=ms, mfc='none', mec='white', mew=1.0, zorder=7, clip_on=False)


def main(names, stem='map_gallery'):
    v.use_times()
    rows = len(names); fig = plt.figure(figsize=(7.05, .42 + 1.0 * rows))
    g = fig.add_gridspec(rows, 6, width_ratios=[1.55, 1, 1, 1, 1, .05], hspace=.55, wspace=.08, left=.045, right=.955,
                         top=1 - .2 / (.42 + 1.0 * rows), bottom=.36 / (.42 + 1.0 * rows))
    for r, n in enumerate(names):
        Z = np.load(FIGD / f'map_gallery20261109/{n.lower().replace(".", "")}.npz', allow_pickle=True)
        q = Z['q']; o = float(Z['origin']); L = float(Z['extent']); T = len(q); cmap, clab = CMAP[n]
        lo, hi = [float(x) for x in Z['field_range']]
        if n == 'Wildfires': lo = 0.
        S = stats(n)
        # snapshots
        TR, (dlo, dhi) = tracks(n, q, o, L)
        span = (int(TR[0]['t'][0]), int(TR[0]['t'][-1]))
        snap_t = np.linspace(span[0], span[1], 3).round().astype(int)
        fields = None
        sub = g[r, 0].subgridspec(1, 3, wspace=.06)
        ds_f = np.asarray(sth.dataset(sth.KEYS[n])['sc']['fields'], float)
        for k, tt in enumerate(snap_t):
            F = ds_f[tt]
            ax = fig.add_subplot(sub[0, k]); ax.imshow(F, origin='lower', cmap=cmap, vmin=lo, vmax=hi, interpolation='nearest', rasterized=True,
                                                         extent=[dlo[0], dhi[0], dlo[1], dhi[1]])
            for kk, x in enumerate(TR):
                m = np.where(x['t'] == tt)[0]
                if len(m): mark(ax, *x['xy'][m[0]], kk, ms=3.4)
            ax.set_xticks([]); ax.set_yticks([]); [s.set_linewidth(.4) for s in ax.spines.values()]
            ax.set_title(f't = {int(tt)}', fontsize=5.8, pad=1.5)
            if k == 0: ax.set_ylabel(LAB[n], fontsize=7.5, labelpad=3)
        tq = np.concatenate([[t] * len(x) for t, x in enumerate(q)]); qn = (np.concatenate(list(q)).astype(float) - o) / L
        for c, (key, title) in enumerate(COLS):
            ax = fig.add_subplot(g[r, c + 1]); M = np.asarray(Z[key], float)
            im = ax.imshow(M, origin='lower', aspect='auto', cmap=cmap, vmin=lo, vmax=hi, extent=[-.5, T - .5, 0, 1],
                           interpolation='nearest', rasterized=True)
            for kk, x in enumerate(TR):   # reference position at five moments of the feature's life only
                sel = np.unique(np.linspace(0, len(x['t']) - 1, min(5, max(2, len(x['t']) // 2))).round().astype(int))
                mark(ax, x['t'][sel], (x['q'][sel] - o) / L, kk)
            mean, npe = S[key]
            ax.text(.5, -.12, f'{mean:.1f}% / {npe:.1f}%', transform=ax.transAxes, fontsize=6, va='top', ha='center')
            ax.set_xticks([]); ax.set_yticks([])
            ax.tick_params(labelsize=5.6, length=1.5, pad=1); [s.set_linewidth(.4) for s in ax.spines.values()]
            if r == 0: ax.set_title(title, fontsize=7.2, pad=3)
        cax = fig.add_subplot(g[r, 5]); cb = fig.colorbar(im, cax=cax); cb.ax.tick_params(labelsize=5.4, length=1.5, pad=1)
        cb.set_label(clab, fontsize=5.8, labelpad=1); cb.outline.set_linewidth(.4)
    fig.text(.5, .006, 'time runs left to right; circle and square: reference positions of the two most significant tracked features at a few moments (same symbols in the snapshots); below each map: mean displacement / NPE', ha='center', fontsize=6.4)
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'{stem}.{ext}', dpi=400)
    plt.close(fig)


if __name__ == '__main__':
    args = sys.argv[1:]; stem = 'map_gallery'
    if args and args[0].startswith('out='): stem = args.pop(0)[4:]
    main(args or ['Ring', 'Wildfires'], stem)
