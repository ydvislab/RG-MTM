"""Fig. 7 (v33, enlarged and relabelled in v34: one figure of merit per panel, reference shown in every panel): feature positions on Tangaroa and Cylinder, redrawn in the layout of the collaborator's v30 figure so that
every axis, including the colour bar, labels both of its ends (2026-11-09).

Data (read only): ../figdata/volume_gallery20261108/{tangaroa,cylinder}.json (volume_gallery_data.py: displayed positions of
TMTM, ST-MTM and AnchorMTM at eps = 0, 5, 20% on the same features, references q, canvas). The panel statistics recomputed
from these positions equal those printed in the v30 figure (e.g. Tangaroa TMTM mean 8.8%, NPE 30.6%; Cylinder ST-MTM
24.3%, 51.6%; Tangaroa 20% merge 19.9%).
Output: ../../pvis2027/latex_v30/figures/volume_gallery.{pdf,png}
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import v23_figures as v

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'figdata/volume_gallery20261108'
OUT = HERE.parents[1] / 'pvis2027/latex_v30/figures'
ROWS = [('tangaroa', 'Tangaroa'), ('cylinder', 'Cylinder')]
COLS = [('reference', 'Reference $q$\n(target)'), ('TMTM', 'TMTM'), ('ST-MTM', 'ST-MTM'), ('eps=0', r'$\varepsilon$=0'), ('eps=0.05', r'$\varepsilon$=5%'), ('eps=0.2', r'$\varepsilon$=20%')]
MS = {'tangaroa': .7, 'cylinder': 1.}
LIM = .3
TINT = '#F1F4F8'; FAINT = '#D5DAE0'; BLUE = '#0072B2'; TM = '#7B8790'; ST = '#CC79A7'


def bars(ax, rows):
    """NPE of each map as a bar; for a positive budget the merge error follows in parentheses."""
    y = np.arange(len(rows))[::-1]
    for yy, (lab, npe, me, col) in zip(y, rows):
        ax.barh(yy, npe, height=.64, color=col, lw=0)
        ax.text(npe + 1.2, yy, f'{npe:.1f}' + (f'  (merge {me:.1f})' if me > 5e-3 else ''), va='center', ha='left', fontsize=7.6)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8); ax.set_xlim(0, 62); ax.set_xticks([0, 30, 60]); ax.set_ylim(-.6, len(rows) - .4)
    ax.tick_params(labelsize=8, length=2, pad=1); ax.tick_params(axis='y', length=0)
    for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)


def main():
    v.use_times()
    fig = plt.figure(figsize=(7.05, 3.1))
    g = fig.add_gridspec(2, 7, width_ratios=[1] * 6 + [.06], left=.068, right=.695, top=.845, bottom=.115, wspace=.13, hspace=.34)
    gb = fig.add_gridspec(2, 1, left=.815, right=.998, top=.845, bottom=.115, hspace=.34)
    norm = TwoSlopeNorm(0, -LIM, LIM)
    cmap = LinearSegmentedColormap.from_list('dev', ['#3b1d6e', '#7a5ba8', '#5b6066', '#c98a2b', '#8a4b06'])   # grey = on its reference
    for r, (f, name) in enumerate(ROWS):
        v35 = DATA.parent / f'volumes_v35/{f}_x_gallery.json'   # v35: Tangaroa along the streamwise x axis (Cylinder already is)
        d = json.loads((v35 if v35.exists() else DATA / f'{f}.json').read_text()); L = d['canvas']; o = d['origin']
        Q = [(np.asarray(q) - o) / L for q in d['q']]; T = len(Q)
        t = np.concatenate([[i] * len(q) for i, q in enumerate(Q)]); qn = np.concatenate(Q); summary = {}
        for c, (key, title) in enumerate(COLS):
            ax = fig.add_subplot(g[r, c])
            if key == 'reference':
                ax.set_facecolor(TINT); ax.scatter(t, qn, s=MS[f], lw=0, color='#5b6066', rasterized=True)
            else:
                ax.scatter(t, qn, s=MS[f], lw=0, color=FAINT, rasterized=True, zorder=1)
                m = d['maps'][key]; X = [(np.asarray(x) - o) / L for x in m['x']]; u = np.concatenate(X); dv = u - qn
                srt = np.argsort(np.abs(dv))
                ax.scatter(t[srt], u[srt], c=dv[srt], s=MS[f], lw=0, cmap=cmap, norm=norm, rasterized=True, zorder=2)
                me = m.get('NMLE_max'); summary[key] = (100 * np.mean([np.max(np.abs(x - q)) for x, q in zip(X, Q)]), 0. if me is None else 100 * me)
            ax.set_xlim(-1, T); ax.set_ylim(0, 1)
            ax.set_xticks([0, T - 1]); lab = ax.set_xticklabels(['0', f'{T - 1}']); lab[0].set_ha('left'); lab[1].set_ha('right')
            ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '0.5', '1'] if c == 0 else [])
            ax.tick_params(labelsize=8, length=2, pad=1)
            for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
            if r == 0: ax.set_title(title, fontsize=9, pad=3, fontweight='bold' if key == 'reference' else 'normal', linespacing=.95)
            if c == 0: ax.set_ylabel(f'{name}\naxis position', fontsize=9, labelpad=2)
            if r == 0 and c == 3: x0 = ax.get_position().x0
            if r == 0 and c == 5: x1 = ax.get_position().x1
        b = fig.add_subplot(gb[r, 0])
        rows = [('TMTM', *summary['TMTM'], TM), ('ST-MTM', *summary['ST-MTM'], ST), (r'$\varepsilon$=0', *summary['eps=0'], BLUE), (r'$\varepsilon$=5%', *summary['eps=0.05'], BLUE), (r'$\varepsilon$=20%', *summary['eps=0.2'], BLUE)]
        bars(b, rows); print(name, [(a, round(n, 2), round(e, 2)) for a, n, e, _ in rows])
        if r == 0: b.set_title('NPE (% of axis)', fontsize=9, pad=3, loc='left')
    fig.text((x0 + x1) / 2, .955, 'AnchorMTM', ha='center', va='center', fontsize=9)
    fig.add_artist(plt.Line2D([x0, x1], [.925, .925], color='#333', lw=.6))
    cax = fig.add_subplot(g[:, -1])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, extend='both', ticks=[-.3, -.15, 0, .15, .3])
    cb.ax.set_yticklabels(['-0.3', '-0.15', '0', '0.15', '0.3']); cb.ax.tick_params(labelsize=8, length=2, pad=1)
    cb.set_label('signed displacement $(x-q)/L$', fontsize=8.5, labelpad=2); cb.outline.set_linewidth(.4)
    fig.text(.38, .012, 'Time (frame)', ha='center', fontsize=9)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'volume_gallery.{ext}', dpi=400)


if __name__ == '__main__':
    main()
