"""Fig. 7 (v33): feature positions on Tangaroa and Cylinder, redrawn in the layout of the collaborator's v30 figure so that
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
COLS = [('reference', 'Reference $q$'), ('TMTM', 'TMTM'), ('ST-MTM', 'ST-MTM'), ('eps=0', 'AnchorMTM, 0%'), ('eps=0.05', '5%'), ('eps=0.2', '20%')]
MS = {'tangaroa': .5, 'cylinder': .8}
LIM = .3


def main():
    v.use_times()
    fig = plt.figure(figsize=(7.05, 2.42))
    g = fig.add_gridspec(2, 7, width_ratios=[1] * 6 + [.045], left=.075, right=.955, top=.91, bottom=.185, wspace=.16, hspace=.78)
    norm = TwoSlopeNorm(0, -LIM, LIM)
    cmap = LinearSegmentedColormap.from_list('dev', ['#3b1d6e', '#7a5ba8', '#5b6066', '#c98a2b', '#8a4b06'])   # grey = on its reference
    for r, (f, name) in enumerate(ROWS):
        d = json.loads((DATA / f'{f}.json').read_text()); L = d['canvas']; o = d['origin']
        Q = [(np.asarray(q) - o) / L for q in d['q']]; T = len(Q)
        t = np.concatenate([[i] * len(q) for i, q in enumerate(Q)]); qn = np.concatenate(Q)
        for c, (key, title) in enumerate(COLS):
            ax = fig.add_subplot(g[r, c])
            if key == 'reference':
                ax.scatter(t, qn, s=MS[f], lw=0, color='#5b6066', rasterized=True)
            else:
                m = d['maps'][key]; X = [(np.asarray(x) - o) / L for x in m['x']]; u = np.concatenate(X); dv = u - qn
                srt = np.argsort(np.abs(dv))
                ax.scatter(t[srt], u[srt], c=dv[srt], s=MS[f], lw=0, cmap=cmap, norm=norm, rasterized=True)
                mean = 100 * np.mean(np.abs(dv)); npe = 100 * np.mean([np.max(np.abs(x - q)) for x, q in zip(X, Q)])
                note = f'mean {mean:.1f}%, NPE {npe:.1f}%'
                if key in ('eps=0.05', 'eps=0.2'): note += f'\nmerge {100 * m["NMLE_max"]:.1f}%'
                ax.text(.5, -.2, note, transform=ax.transAxes, ha='center', va='top', fontsize=6.6, linespacing=1.05)
            ax.set_xlim(-1, T); ax.set_ylim(0, 1)
            ax.set_xticks([0, T - 1]); lab = ax.set_xticklabels(['0', f'{T - 1}']); lab[0].set_ha('left'); lab[1].set_ha('right')
            ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '0.5', '1'] if c == 0 else [])
            ax.tick_params(labelsize=7, length=2, pad=1)
            for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
            if r == 0: ax.set_title(title, fontsize=8, pad=3)
            if c == 0: ax.set_ylabel(f'{name}\naxis position', fontsize=7.5, labelpad=2)
    cax = fig.add_subplot(g[:, -1])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, extend='both', ticks=[-.3, -.2, -.1, 0, .1, .2, .3])
    cb.ax.set_yticklabels(['-0.3', '-0.2', '-0.1', '0', '0.1', '0.2', '0.3']); cb.ax.tick_params(labelsize=7, length=2, pad=1)
    cb.set_label('signed displacement $(x-q)/L$', fontsize=7, labelpad=2); cb.outline.set_linewidth(.4)
    fig.text(.5, .015, 'Time (frame)', ha='center', fontsize=8)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'volume_gallery.{ext}', dpi=400)


if __name__ == '__main__':
    main()
