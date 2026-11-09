"""Supplementary figure: the hourly PM2.5 episode of the paper's case study drawn by TMTM, ST-MTM and AnchorMTM (5%).
Same window (frames 504-636, 22-27 January 2017), same colour map and 0-400 ug/m3 range as the case figure.
Inputs: AnchorMTM map from paper/pvis2027/pm25_hourly_20261107/figure_cache.npz (the case figure's data); TMTM and
ST-MTM same-window columns from the collaborator's package 03 (rebuilt with the original configuration; anchors
checked against the stored table runs). Five snapshot times as in the case figure.
Output: ../../pvis2027/latex_v30/figures/supp_pm25_compare.{pdf,png}
"""
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import v23_figures as v

ROOT = Path(__file__).resolve().parents[3]
PKG = Path('/Users/yudong/Downloads/老师所需四项材料_20261109/03_PM25同窗TMTM与STMTM原始列')
OUT = ROOT / 'paper/pvis2027/latex_v30/figures'


def main():
    v.use_times()
    C = np.load(ROOT / 'paper/pvis2027/pm25_hourly_20261107/figure_cache.npz')
    maps = [('TMTM', np.load(PKG / 'tmtm_paper_window_columns.npz')['concentration']),
            ('ST-MTM', np.load(PKG / 'temporal_paper_window_columns.npz')['concentration']),
            (r'AnchorMTM, $\varepsilon=5\%$', C['map'])]
    cm = LinearSegmentedColormap.from_list('pollution', plt.get_cmap('RdYlGn_r')(np.linspace(0, 1, 256) ** .6)); norm = Normalize(0, 400)
    start, stop = 504, 637; snaps = list(C['frames']); dates = [datetime(2017, 1, 1) + timedelta(hours=i) for i in range(744)]
    fig = plt.figure(figsize=(7.05, 3.0)); g = fig.add_gridspec(2, 5, height_ratios=[1.25, 1], hspace=.35, wspace=.12, left=.06, right=.9, top=.92, bottom=.06)
    top = g[0, :].subgridspec(1, 3, wspace=.06)
    for k, (title, M) in enumerate(maps):
        ax = fig.add_subplot(top[0, k])
        im = ax.imshow(M, origin='lower', aspect='auto', extent=[start - .5, stop - .5, 0, 1], cmap=cm, norm=norm, interpolation='bilinear', rasterized=True)
        for s, lab in zip(snaps, 'abcde'):
            ax.axvline(s, color='k', lw=.5, ls=(0, (2, 2))); ax.text(s, 1.02, lab, ha='center', va='bottom', fontsize=6.5)
        ax.set_title(title, fontsize=7.6, pad=11); ax.set_yticks([0, .5, 1] if k == 0 else []); ax.tick_params(labelsize=6, length=2, pad=1)
        ax.set_xticks([504, 576, 636]); ax.set_xticklabels(['Jan 22', 'Jan 25', 'Jan 27'])
        if k == 0: ax.set_ylabel('position on the axis', fontsize=6.6)
    for i, (t, F) in enumerate(zip(snaps, C['snapshots'])):
        a = fig.add_subplot(g[1, i]); a.imshow(F, origin='lower', extent=[110, 120, 32, 41], cmap=cm, norm=norm, interpolation='bilinear', aspect='auto')
        a.set_title(f"({'abcde'[i]}) {dates[t].strftime('%m-%d %H:%M')}", fontsize=6.6, pad=2); a.set_xticks([]); a.set_yticks([])
    cax = fig.add_axes([.915, .2, .012, .6]); cb = fig.colorbar(im, cax=cax); cb.ax.tick_params(labelsize=6, length=2)
    cb.set_label(r'PM$_{2.5}$ ($\mu$g m$^{-3}$)', fontsize=6.6)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'supp_pm25_compare.{ext}', dpi=300)


if __name__ == '__main__':
    main()
