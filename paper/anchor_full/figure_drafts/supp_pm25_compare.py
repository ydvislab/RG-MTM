"""Supplementary figure: the hourly PM2.5 episode of the paper's case study drawn by TMTM, ST-MTM and AnchorMTM (5%).
Same window (frames 504-636, 22-27 January 2017), same colour map and 0-400 ug/m3 range as the case figure.
Inputs: AnchorMTM map from paper/pvis2027/pm25_hourly_20261107/figure_cache.npz (the case figure's data); TMTM and
ST-MTM same-window columns from the collaborator's package 03 (rebuilt with the original configuration; anchors
checked against the stored table runs). Without package 03 (any machine but the Mac), the TMTM and ST-MTM panels are
drawn from the rasters of the v31 figure, saved in ../figdata/pm25_compare_v31/ (same colour map and range).
v33 changes: time ticks inside each panel (the edge labels of neighbouring panels collided), the meaning of each
vertical axis stated under its title, province borders on the snapshots.
Output: ../../pvis2027/latex_v30/figures/supp_pm25_compare.{pdf,png}
"""
import json
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
RASTER = ROOT / 'paper/anchor_full/figdata/pm25_compare_v31'
CASE = ROOT / 'paper/pvis2027/pm25_hourly_20261107'
OUT = ROOT / 'paper/pvis2027/latex_v30/figures'


def main():
    v.use_times()
    C = np.load(CASE / 'figure_cache.npz')
    cm = LinearSegmentedColormap.from_list('pollution', plt.get_cmap('RdYlGn_r')(np.linspace(0, 1, 256) ** .6)); norm = Normalize(0, 400)
    if (PKG / 'tmtm_paper_window_columns.npz').exists():
        base = [np.load(PKG / 'tmtm_paper_window_columns.npz')['concentration'], np.load(PKG / 'temporal_paper_window_columns.npz')['concentration']]
    else:
        base = [plt.imread(RASTER / 'tmtm.png'), plt.imread(RASTER / 'stmtm.png')]   # RGB, already coloured
    maps = [('TMTM', 'axis: tree order', base[0]), ('ST-MTM', 'axis: relative distance', base[1]),
            (r'AnchorMTM, $\varepsilon=5\%$', 'axis: spatial position', C['map'])]
    start, stop = 504, 637; snaps = list(C['frames']); dates = [datetime(2017, 1, 1) + timedelta(hours=i) for i in range(744)]
    # v33 layout: explicit axes positions so that the maps use the full width and the white space between rows is small
    fig = plt.figure(figsize=(7.05, 3.45))
    L, R, gap = .058, .905, .012; w3 = (R - L - 2 * gap) / 3; w5 = (R - L - 4 * .01) / 5
    for k, (title, sub, M) in enumerate(maps):
        ax = fig.add_axes([L + k * (w3 + gap), .44, w3, .42])
        kw = dict(origin='lower', aspect='auto', extent=[start - .5, stop - .5, 0, 1], interpolation='bilinear', rasterized=True)
        if M.ndim == 3: ax.imshow(M[::-1] if M.shape[0] > 1 else M, **kw)   # a saved raster is stored top row first
        else: ax.imshow(M, cmap=cm, norm=norm, **kw)
        for s, lab in zip(snaps, 'abcde'):
            ax.axvline(s, color='k', lw=.5, ls=(0, (2, 2))); ax.text(s, 1.015, lab, ha='center', va='bottom', fontsize=7.5)
        ax.text(0, 1.19, title, transform=ax.transAxes, ha='left', va='bottom', fontsize=8.5)
        ax.text(0, 1.1, sub, transform=ax.transAxes, ha='left', va='bottom', fontsize=7.5, color='#555')
        ax.set_yticks([0, .5, 1] if k == 0 else []); ax.tick_params(labelsize=7.5, length=2, pad=1)
        ax.set_xticks([start, 576, stop - 1]); lab = ax.set_xticklabels(['Jan 22', 'Jan 25', 'Jan 27 12h'])
        lab[0].set_ha('left'); lab[-1].set_ha('right')
        if k == 0: ax.set_ylabel('Mapped position', fontsize=8.5, labelpad=1)
    geo = json.loads((CASE / 'china_admin1.geojson').read_text())
    for i, (t, F) in enumerate(zip(snaps, C['snapshots'])):
        a = fig.add_axes([L + i * (w5 + .01), .015, w5, .33])
        a.imshow(F, origin='lower', extent=[110, 120, 32, 41], cmap=cm, norm=norm, interpolation='bilinear', aspect='auto')
        for ft in geo['features']:
            gm = ft['geometry']; polys = gm['coordinates'] if gm['type'] == 'MultiPolygon' else [gm['coordinates']]
            for poly in polys:
                q = np.array(poly[0]); a.plot(q[:, 0], q[:, 1], color='#444444', lw=.25)
        a.set(xlim=(110, 120), ylim=(32, 41), xticks=[], yticks=[])
        a.text(.03, .96, f"({'abcde'[i]}) {dates[t].strftime('%m-%d %H:%M')}", transform=a.transAxes, ha='left', va='top', fontsize=7.5,
               bbox=dict(facecolor='white', edgecolor='none', alpha=.8, pad=1))
    cax = fig.add_axes([.918, .1, .012, .76]); cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cm), cax=cax); cb.ax.tick_params(labelsize=7.5, length=2)
    cb.set_label(r'PM$_{2.5}$ ($\mu$g m$^{-3}$)', fontsize=8.5)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'supp_pm25_compare.{ext}', dpi=300)


if __name__ == '__main__':
    main()
