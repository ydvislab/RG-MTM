"""v28 evaluation figure: one storm drawn by four merge tree maps (2026-11-09).

The map row of the v23 teaser (teaser_v23.py), without the snapshot row: Fig. 1 returns to the Storms overview, whose
five snapshots (a)-(e) are the times marked here. Same inputs and numbers as teaser_v23.py.
Output: ../../pvis2027/latex_v21/figures/storm_compare_maps.{pdf,svg}
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import teaser_v23 as tv


def main():
    tv.use_times()
    z = np.load(tv.SRC / 'baseline_maps.npz')
    panels = [('TMTM', z['TMTM'][:, tv.W0:tv.W1 + 1], None), ('ST-MTM', z['STMTM'][:, tv.W0:tv.W1 + 1], None),
              (r'AnchorMTM, $\varepsilon=0$', np.asarray(Image.open(tv.SRC / 'assets/Storms_0_main_aspect_215_140.png').convert('RGB')), 0.0),
              (r'AnchorMTM, $\varepsilon=10\%$', np.asarray(Image.open(tv.SRC / 'assets/Storms_0.1_main_aspect_215_140.png').convert('RGB')), 0.1)]
    t, q, xs = tv.storm()
    fig = plt.figure(figsize=(7.0, 1.5))
    left, right, gap, bottom, height = .065, .925, .018, .22, .6
    w = (right - left - 3 * gap) / 4
    for k, (title, img, e) in enumerate(panels):
        ax = fig.add_axes([left + k * (w + gap), bottom, w, height])
        if img.ndim == 2:
            im = ax.imshow(img, origin='lower', aspect='auto', cmap='RdBu_r', vmin=-35, vmax=35, extent=[tv.W0 - .5, tv.W1 + .5, 0, 1],
                           interpolation='antialiased', rasterized=True)
        else:
            ax.imshow(img, origin='upper', aspect='auto', extent=[tv.W0 - .5, tv.W1 + .5, 0, 1], interpolation='antialiased', rasterized=True)
        ax.plot(t, q, '--', color='black', lw=.9, dashes=(3, 1.6), zorder=5)
        for s, lab in zip(tv.SNAP, 'abcde'):
            ax.plot([s, s], [.965, 1.0], color='black', lw=.7, clip_on=False, zorder=6)
            ax.text(s, 1.015, lab, ha='center', va='bottom', fontsize=6.5)
        if e is not None:
            d = 100 * np.abs(xs[round(e, 4)] - q); print(title, 'mean %.2f max %.2f' % (d.mean(), d.max()))
        ax.set_xlim(tv.W0 - .5, tv.W1 + .5); ax.set_ylim(0, 1)
        ax.set_xticks([360, 384, 408, 432, 456]); ax.set_xticklabels(['16', '17', '18', '19', '20'])
        ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '0.5', '1'] if k == 0 else [])
        ax.tick_params(labelsize=6.5, length=2, pad=1.5)
        ax.set_title(title, fontsize=8, pad=9)
        for sp in ax.spines.values(): sp.set_visible(True); sp.set_linewidth(.5)
    fig.text(left - .045, bottom + height / 2, 'position on the axis', rotation=90, ha='center', va='center', fontsize=7)
    fig.text((left + right) / 2, .03, 'December 1999 (day; hourly frames 355–460)', ha='center', fontsize=7)
    cax = fig.add_axes([right + .012, bottom, .012, height]); cb = fig.colorbar(im, cax=cax)
    cb.ax.tick_params(labelsize=6, length=2, pad=1); cb.set_label('SLP anomaly (hPa)', fontsize=6.5, labelpad=2)
    for ext in ('pdf', 'svg'):
        fig.savefig(tv.FIG / f'storm_compare_maps.{ext}', dpi=450)
    fig.savefig(tv.HERE / 'preview_v20/storm_compare_maps.png', dpi=220); plt.close(fig)


if __name__ == '__main__':
    main()
