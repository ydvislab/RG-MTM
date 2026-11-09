"""v23 hourly PM2.5 case figure: the collaborator's draw.py layout with the map and the snapshots linked.

Same data as paper/pvis2027/pm25_hourly_20261107/draw.py (figure_cache.npz: the epsilon = 5% map of hours 504-636
and five source snapshots). Added: dashed time markers a-e on the map at the snapshot hours, matching labels under
the snapshots, Times New Roman. The reference direction is not stored with the run, so no direction arrow is drawn.
Output: ../../pvis2027/latex_v21/figures/pm25_hourly.{pdf,svg}
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from v23_figures import use_times

HERE = Path(__file__).resolve().parent; SRC = HERE.parents[1] / 'pvis2027/pm25_hourly_20261107'
FIG = HERE.parents[1] / 'pvis2027/latex_v21/figures'
START, STOP = 504, 637
FRAMES = [504, 540, 576, 612, 636]


def main():
    use_times()
    C = np.load(SRC / 'figure_cache.npz'); assert C['map'].shape[1] == STOP - START
    snaps = dict(zip(C['frames'].tolist(), C['snapshots'])); assert sorted(snaps) == FRAMES
    date = lambda t: datetime(2017, 1, 1) + timedelta(hours=t)
    cm = LinearSegmentedColormap.from_list('pollution', plt.get_cmap('RdYlGn_r')(np.linspace(0, 1, 256) ** .6)); norm = Normalize(0, 400)
    fig = plt.figure(figsize=(3.4, 2.45))
    ax = fig.add_axes([.11, .56, .86, .37])
    im = ax.imshow(C['map'], origin='lower', aspect='auto', extent=[START - .5, STOP - .5, 0, 1], cmap=cm, norm=norm, interpolation='bilinear')
    for t, lab in zip(FRAMES, 'abcde'):
        ax.axvline(t, color='black', lw=.6, ls=(0, (2.5, 1.5)), zorder=3)
        ax.text(t, 1.03, lab, ha='center', va='bottom', fontsize=7, transform=ax.get_xaxis_transform())
    ticks = [504, 528, 552, 576, 600, 624]
    ax.set_xticks(ticks); ax.set_xticklabels([date(t).strftime('Jan %d') for t in ticks])
    ax.set_yticks([0, .5, 1]); ax.set_ylabel('position on the map axis', fontsize=7)
    ax.tick_params(labelsize=6.5, pad=1.5, length=2)
    geo = json.loads((SRC / 'china_admin1.geojson').read_text())
    for i, (t, lab) in enumerate(zip(FRAMES, 'abcde')):
        a = fig.add_axes([.11 + i * .174, .2, .164, .27])
        a.imshow(snaps[t], origin='lower', extent=[110, 120, 32, 41], cmap=cm, norm=norm, interpolation='bilinear', aspect='auto')
        for ft in geo['features']:
            g = ft['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            for poly in polys:
                p = np.array(poly[0]); a.plot(p[:, 0], p[:, 1], color='#444444', lw=.22)
        a.set(xlim=(110, 120), ylim=(32, 41), xticks=[], yticks=[])
        a.text(.5, -.06, f'({lab}) ' + date(t).strftime('%d %H:%M'), transform=a.transAxes, ha='center', va='top', fontsize=6.3)
    cb = fig.colorbar(im, cax=fig.add_axes([.25, .065, .58, .025]), orientation='horizontal', extend='max')
    cb.set_ticks([0, 100, 200, 300, 400]); cb.ax.tick_params(labelsize=6.3, pad=1, length=2)
    cb.set_label(r'PM$_{2.5}$ ($\mu$g/m$^3$)', fontsize=6.8, labelpad=1)
    for panel in fig.axes:
        for sp in panel.spines.values(): sp.set_visible(True); sp.set_color('black'); sp.set_linewidth(.45)
    for ext in ('pdf', 'svg'):
        fig.savefig(FIG / f'pm25_hourly.{ext}', dpi=600, bbox_inches='tight', pad_inches=.02)
    fig.savefig(HERE / 'preview_v20/pm25_hourly.png', dpi=300, bbox_inches='tight', pad_inches=.02); plt.close(fig)
    print('snapshot hours', [date(t).strftime('%m-%d %H:%M') for t in FRAMES])


if __name__ == '__main__':
    main()
