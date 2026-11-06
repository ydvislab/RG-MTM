"""Volumetric figure for Section 5.3: where the Tangaroa features are drawn (2026-11-06).

Each panel plots every feature of every frame at its displayed position on the reference axis, coloured by its signed
displacement (x - q) / L. Native TMTM and ST-MTM anchors are rescaled to the canvas and shown in the mirror with the
lower mean displacement; AnchorMTM positions come from volume_positions.py (checked against the frontier run).
Run:  python volume_figure.py  ->  ../figures/fig_tangaroa_positions.{pdf,png}
"""
import json
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata'
plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'pdf.fonttype': 42, 'mathtext.fontset': 'dejavusans'})


def main():
    D = json.loads((RES / 'volume_maps20261106/tangaroa.json').read_text()); L = D['canvas']; o = D['origin']; qs = [list((np.asarray(q) - o)) for q in D['q']]
    cols = [('TMTM', 'TMTM (native)'), ('ST-MTM', 'ST-MTM (native)'), ('eps=0', r'AnchorMTM, $\varepsilon=0$')]
    fig = plt.figure(figsize=(3.4, 1.2)); g = fig.add_gridspec(1, 4, width_ratios=[1] * 3 + [.06], wspace=.12)
    norm = TwoSlopeNorm(0, -.3, .3); cmap = plt.get_cmap('PuOr_r')
    for k, (key, title) in enumerate(cols):
        ax = fig.add_subplot(g[k]); xs = [list(np.asarray(x) - o) for x in D['maps'][key]['x']]
        t = np.concatenate([[i] * len(x) for i, x in enumerate(xs)]); u = np.concatenate(xs) / L
        dv = u - np.concatenate(qs) / L; srt = np.argsort(np.abs(dv))
        sc = ax.scatter(t[srt], u[srt], c=dv[srt], s=.35, lw=0, cmap=cmap, norm=norm, rasterized=True)
        mean = 100 * np.mean(np.abs(dv)); worst = 100 * np.mean([np.max(np.abs(np.asarray(x) / L - np.asarray(q) / L)) for x, q in zip(xs, qs)])
        ax.text(.03, .03, f'mean {mean:.1f}%\nNPE {worst:.0f}%', transform=ax.transAxes, fontsize=5.8, linespacing=1.1, va='bottom',
                bbox=dict(boxstyle='round,pad=.15', fc='white', ec='none', alpha=.9))
        print(key, f'mean |x-q|/L {mean:.2f}%  NPE {worst:.2f}%', flush=True)
        ax.set_xlim(-1, len(xs)); ax.set_ylim(-.02, 1.02); ax.set_title(title, fontsize=6.2, pad=2.5)
        ax.set_xticks([0, 100, 200]); ax.set_xticklabels(['0', '100', '200' if k == len(cols) - 1 else '']); ax.tick_params(labelsize=5.8, length=1.5, pad=1)
        ax.set_yticks([0, .5, 1] if k == 0 else []); ax.set_xlabel('time step' if k == 1 else '', fontsize=6, labelpad=1)
        if k == 0: ax.set_ylabel('position on the axis / L', fontsize=6, labelpad=1)
        for s in ax.spines.values(): s.set_linewidth(.4)
    cb = fig.colorbar(sc, cax=fig.add_subplot(g[3]), extend='both'); cb.ax.tick_params(labelsize=5.8, length=1.5)
    cb.set_ticks([-.3, 0, .3]); cb.set_ticklabels(['-30%', '0', '+30%']); cb.set_label('(x - q) / L', fontsize=6, labelpad=0)
    for ext in ('pdf', 'png'):
        fig.savefig(HERE.parent / 'figures' / f'fig_tangaroa_positions.{ext}', dpi=240, bbox_inches='tight', pad_inches=.02)


if __name__ == '__main__':
    main()
