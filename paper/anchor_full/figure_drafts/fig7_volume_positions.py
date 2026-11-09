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
COLS = [('reference', 'Reference $q$ (target)'), ('TMTM', 'TMTM'), ('ST-MTM', 'ST-MTM'), ('eps=0', r'AnchorMTM, $\varepsilon$=0'), ('eps=0.05', r'$\varepsilon$=5%'), ('eps=0.2', r'$\varepsilon$=20%')]
MS = {'tangaroa': .7, 'cylinder': 1.}
LIM = .3
TINT = '#F1F4F8'; FAINT = '#D5DAE0'


def main():
    v.use_times()
    fig = plt.figure(figsize=(7.05, 3.7))
    g = fig.add_gridspec(2, 7, width_ratios=[1] * 6 + [.05], left=.075, right=.925, top=.935, bottom=.205, wspace=.13, hspace=.68)
    norm = TwoSlopeNorm(0, -LIM, LIM)
    cmap = LinearSegmentedColormap.from_list('dev', ['#3b1d6e', '#7a5ba8', '#5b6066', '#c98a2b', '#8a4b06'])   # grey = on its reference
    for r, (f, name) in enumerate(ROWS):
        v35 = DATA.parent / f'volumes_v35/{f}_x_gallery.json'   # v35: Tangaroa along the streamwise x axis (Cylinder already is)
        d = json.loads((v35 if v35.exists() else DATA / f'{f}.json').read_text()); L = d['canvas']; o = d['origin']
        Q = [(np.asarray(q) - o) / L for q in d['q']]; T = len(Q)
        t = np.concatenate([[i] * len(q) for i, q in enumerate(Q)]); qn = np.concatenate(Q)
        for c, (key, title) in enumerate(COLS):
            ax = fig.add_subplot(g[r, c])
            if key == 'reference':
                ax.set_facecolor(TINT); ax.scatter(t, qn, s=MS[f], lw=0, color='#5b6066', rasterized=True)
                ax.text(.97, -.235, 'NPE', transform=ax.transAxes, ha='right', va='top', fontsize=9, fontweight='bold')
                ax.text(.97, -.40, 'merge error', transform=ax.transAxes, ha='right', va='top', fontsize=8.5)
            else:
                ax.scatter(t, qn, s=MS[f], lw=0, color=FAINT, rasterized=True, zorder=1)
                m = d['maps'][key]; X = [(np.asarray(x) - o) / L for x in m['x']]; u = np.concatenate(X); dv = u - qn
                srt = np.argsort(np.abs(dv))
                ax.scatter(t[srt], u[srt], c=dv[srt], s=MS[f], lw=0, cmap=cmap, norm=norm, rasterized=True, zorder=2)
                npe = 100 * np.mean([np.max(np.abs(x - q)) for x, q in zip(X, Q)])
                ax.text(.5, -.235, f'{npe:.1f}%', transform=ax.transAxes, ha='center', va='top', fontsize=9, fontweight='bold')
                me = m.get('NMLE_max'); me = 0. if me is None else 100 * me    # TMTM and ST-MTM keep the tree exactly
                ax.text(.5, -.40, '0' if me < 5e-3 else f'{me:.1f}%', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
            ax.set_xlim(-1, T); ax.set_ylim(0, 1)
            ax.set_xticks([0, T - 1]); lab = ax.set_xticklabels(['0', f'{T - 1}']); lab[0].set_ha('left'); lab[1].set_ha('right')
            ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '0.5', '1'] if c == 0 else [])
            ax.tick_params(labelsize=8, length=2, pad=1)
            for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
            if r == 0: ax.set_title(title, fontsize=9, pad=3, fontweight='bold' if key == 'reference' else 'normal')
            if c == 0: ax.set_ylabel(f'{name}\naxis position', fontsize=9, labelpad=2)
    cax = fig.add_subplot(g[:, -1])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, extend='both', ticks=[-.3, -.15, 0, .15, .3])
    cb.ax.set_yticklabels(['-0.3', '-0.15', '0', '0.15', '0.3']); cb.ax.tick_params(labelsize=8, length=2, pad=1)
    cb.set_label('signed displacement $(x-q)/L$', fontsize=8.5, labelpad=2); cb.outline.set_linewidth(.4)
    fig.text(.5, .008, 'Time (frame)', ha='center', fontsize=9)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'volume_gallery.{ext}', dpi=400)


if __name__ == '__main__':
    main()
