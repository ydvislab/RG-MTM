"""v21 main-paper 3D figure: where each method draws the features of Tangaroa and Cylinder (draft, 2026-11-08).

Each panel plots every feature of every frame at its displayed position on the axis (vertical, fraction of the canvas)
against time, coloured by its signed displacement from the reference (x - q) / L. The first column shows the
references themselves, i.e. what a map that reads as location would show.
Input: ../figdata/volume_gallery20261108/<name>.json (volume_gallery_data.py).
Output: ../../pvis2027/latex_v21/figures/volume_gallery.{pdf,svg}; preview_v20/volume_gallery.png; numbers printed.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata/volume_gallery20261108'
OUT = HERE.parents[1] / 'pvis2027/latex_v21/figures'
for f in ['Times New Roman.ttf', 'Times New Roman Italic.ttf']:
    q = Path('/System/Library/Fonts/Supplemental') / f
    if q.exists():
        font_manager.fontManager.addfont(str(q))
plt.rcParams.update({'font.family': 'Times New Roman', 'mathtext.fontset': 'stix', 'font.size': 7, 'pdf.fonttype': 42,
                     'svg.fonttype': 'none', 'axes.linewidth': .5, 'xtick.major.size': 1.8, 'ytick.major.size': 1.8,
                     'xtick.major.width': .5, 'ytick.major.width': .5})
COLS = [('reference', 'Reference $q$'), ('TMTM', 'TMTM'), ('ST-MTM', 'ST-MTM'),
        ('eps=0', r'AnchorMTM, $\varepsilon=0$'), ('eps=0.05', r'$\varepsilon=5\%$'), ('eps=0.2', r'$\varepsilon=20\%$')]
NAMES = ['Tangaroa', 'Cylinder']


def main():
    D = {n: json.loads((RES / f'{n.lower()}.json').read_text()) for n in NAMES}
    fig = plt.figure(figsize=(7.05, 2.55))
    g = fig.add_gridspec(2, len(COLS) + 1, width_ratios=[1] * len(COLS) + [.05], hspace=.5, wspace=.1,
                         left=.055, right=.955, top=.9, bottom=.1)
    norm = TwoSlopeNorm(0, -.3, .3)
    cmap = LinearSegmentedColormap.from_list('dev', ['#2d004b', '#8073ac', '#4d5358', '#e08214', '#7f3b08'])  # grey = on target
    stats = {}
    for r, n in enumerate(NAMES):
        d = D[n]; L = d['canvas']; o = d['origin']; Q = [(np.asarray(q) - o) / L for q in d['q']]
        t = np.concatenate([[i] * len(q) for i, q in enumerate(Q)]); qn = np.concatenate(Q)
        for c, (key, title) in enumerate(COLS):
            ax = fig.add_subplot(g[r, c])
            if key == 'reference':
                u = qn; dv = np.zeros_like(u); note = f'frames 0\u2013{len(Q) - 1}'
                ax.scatter(t, u, s=.3, lw=0, color='#4d5358', rasterized=True)
            else:
                m = d['maps'][key]; X = [(np.asarray(x) - o) / L for x in m['x']]; u = np.concatenate(X); dv = u - qn
                srt = np.argsort(np.abs(dv))
                ax.scatter(t[srt], u[srt], c=dv[srt], s=.3, lw=0, cmap=cmap, norm=norm, rasterized=True)
                mean = 100 * np.mean(np.abs(dv)); worst = 100 * np.mean([np.max(np.abs(x - q)) for x, q in zip(X, Q)])
                nmle = 100 * m.get('NMLE_max', m.get('NMLE_max_stored', 0.))
                note = f'mean {mean:.1f}%, worst {worst:.1f}%\nmerge error {nmle:.1f}%' if key.startswith('eps') and key != 'eps=0' \
                    else f'mean {mean:.1f}%, worst {worst:.1f}%'
                stats[(n, key)] = dict(mean=round(mean, 2), worst=round(worst, 2), merge_max=round(nmle, 2), mirrored=m.get('mirrored'))
            ax.text(.5, -.04, note, transform=ax.transAxes, fontsize=5.5, va='top', ha='center', linespacing=1.0)
            ax.set_xlim(-1, len(Q)); ax.set_ylim(-.02, 1.02)
            ax.set_xticks([0, len(Q) - 1]); ax.set_xticklabels([])
            ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '.5', '1'] if c == 0 else [], fontsize=5.8)
            ax.tick_params(pad=1.2)
            if r == 0:
                ax.set_title(title, fontsize=7, pad=3)
            if c == 0:
                ax.set_ylabel(f'{n} (3D)\nposition on axis', fontsize=6.6, labelpad=2)
    cax = fig.add_subplot(g[:, -1]); sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, cax=cax, extend='both'); cb.ax.tick_params(labelsize=5.6, length=1.6, pad=1)
    cb.set_label('signed displacement $(x-q)/L$', fontsize=6.4, labelpad=2); cb.outline.set_linewidth(.4)
    fig.text(.5, .01, 'Time (frame) \u2192', ha='center', fontsize=7)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ('pdf', 'svg'):
        fig.savefig(OUT / f'volume_gallery.{ext}', dpi=400)
    fig.savefig(HERE / 'preview_v20/volume_gallery.png', dpi=250); plt.close(fig)
    for k, v in stats.items():
        print(k, v)


if __name__ == '__main__':
    main()
