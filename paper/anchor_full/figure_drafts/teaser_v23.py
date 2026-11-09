"""v23 teaser (Fig. 1): one storm, its geography and four maps of the same week (2026-11-09).

Replaces the former Fig. 1 (Storms overview) and Fig. 8 (Storms parameter maps and method comparison).
Top: the five spatial snapshots of the former Fig. 1 (cropped from its PDF and rendered at 450 dpi, unchanged
content). Bottom: hourly frames 355-460 drawn by TMTM, ST-MTM and AnchorMTM (epsilon = 0 and 10%), with the
storm's projected location (its reference q) as a dashed line in every panel and the five snapshot times marked.

Inputs (saved, read only):
  ../../pvis2027/latex_v21/figures/anchor_storms_overview.pdf                 former Fig. 1 (snapshot row)
  ../../pvis2027/figures/source/storms_structure_20261107/baseline_maps.npz   TMTM, ST-MTM maps (8192 x 744)
  ../../pvis2027/figures/source/storms_structure_20261107/assets/Storms_<eps>_main_aspect_215_140.png
                                                                            AnchorMTM maps of frames 355-460
  ../../../code/results/local_redistribution20261030/inputs/storms-hourly.npz  references q, positions x, tracks
Output: ../../pvis2027/latex_v21/figures/teaser_storms_compare.{pdf,svg}; numbers used are printed.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pymupdf
from PIL import Image
from v23_figures import use_times

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
FIG = ROOT / 'paper/pvis2027/latex_v21/figures'; SRC = ROOT / 'paper/pvis2027/figures/source/storms_structure_20261107'
W0, W1 = 355, 460                      # hourly frames of the shared window (as in the former Fig. 8)
SNAP = [363, 385, 408, 430, 452]       # snapshot frames of the former Fig. 1 (12-16 03:00 ... 12-19 20:00)
TRACK = 260                            # the storm shown in the snapshots (reference 0.7512 at frame 433)


def snapshot_row(dpi=450):
    p = pymupdf.open(FIG / 'anchor_storms_overview.pdf')[0]
    pix = p.get_pixmap(dpi=dpi, clip=pymupdf.Rect(0, 0, p.rect.width, 80))
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3], p.rect.width / 80


def storm():
    h = np.load(ROOT / 'code/results/local_redistribution20261030/inputs/storms-hourly.npz')
    q, x, tr, n, eps = h['q'], h['x'], h['tracks'], h['count'], list(np.round(h['epsilon'], 4))
    t, qq, xx = [], [], {e: [] for e in eps}
    for f in range(744):
        ids = list(tr[f, :n[f]])
        if TRACK in ids:
            j = ids.index(TRACK); t.append(f); qq.append(q[f, j])
            for k, e in enumerate(eps): xx[e].append(x[k, f, j])
    assert t[0] == SNAP[0] and t[-1] == SNAP[-1]
    return np.array(t), np.array(qq), {e: np.array(v) for e, v in xx.items()}


def main():
    use_times()
    snap, ratio = snapshot_row()
    z = np.load(SRC / 'baseline_maps.npz')
    panels = [('TMTM', z['TMTM'][:, W0:W1 + 1], None), ('ST-MTM', z['STMTM'][:, W0:W1 + 1], None),
              (r'AnchorMTM, $\varepsilon=0$', np.asarray(Image.open(SRC / 'assets/Storms_0_main_aspect_215_140.png').convert('RGB')), 0.0),
              (r'AnchorMTM, $\varepsilon=10\%$', np.asarray(Image.open(SRC / 'assets/Storms_0.1_main_aspect_215_140.png').convert('RGB')), 0.1)]
    t, q, xs = storm()
    fig = plt.figure(figsize=(7.0, 3.05))
    top_h = 7.0 / ratio / 3.05
    ax0 = fig.add_axes([0, 1 - top_h - .005, 1, top_h]); ax0.imshow(snap, aspect='auto', interpolation='lanczos'); ax0.axis('off')
    for k, lab in enumerate('abcde'):
        ax0.text((k + .015) / 5 * snap.shape[1], .8 * snap.shape[0], f'({lab})', fontsize=8, ha='left', va='center', weight='bold')
    # reference direction under the snapshots: left-to-right in the snapshots is bottom-to-top in the maps
    fig.text(.5, 1 - top_h - .035, r'reference direction $a^*$: left to right in (a)–(e) $=$ bottom to top in the maps below',
             ha='center', va='center', fontsize=7, color='#333333')
    fig.patches.append(matplotlib.patches.FancyArrowPatch((.16, 1 - top_h - .062), (.84, 1 - top_h - .062), transform=fig.transFigure,
                                                          arrowstyle='-|>', mutation_scale=7, lw=.7, color='#333333'))
    left, right, gap, bottom, height = .065, .925, .018, .13, .43
    w = (right - left - 3 * gap) / 4
    stat = {}
    for k, (title, img, e) in enumerate(panels):
        ax = fig.add_axes([left + k * (w + gap), bottom, w, height])
        if img.ndim == 2:
            im = ax.imshow(img, origin='lower', aspect='auto', cmap='RdBu_r', vmin=-35, vmax=35, extent=[W0 - .5, W1 + .5, 0, 1],
                           interpolation='antialiased', rasterized=True)
        else:
            ax.imshow(img, origin='upper', aspect='auto', extent=[W0 - .5, W1 + .5, 0, 1], interpolation='antialiased', rasterized=True)
        ax.plot(t, q, '--', color='black', lw=.9, dashes=(3, 1.6), zorder=5)
        for s, lab in zip(SNAP, 'abcde'):
            ax.plot([s, s], [.965, 1.0], color='black', lw=.7, clip_on=False, zorder=6)
            ax.text(s, 1.015, lab, ha='center', va='bottom', fontsize=6.5)
        if e is not None:
            d = 100 * np.abs(xs[round(e, 4)] - q); stat[title] = (round(float(d.mean()), 2), round(float(d.max()), 2))
        ax.set_xlim(W0 - .5, W1 + .5); ax.set_ylim(0, 1)
        ax.set_xticks([360, 384, 408, 432, 456]); ax.set_xticklabels(['16', '17', '18', '19', '20'])
        ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '0.5', '1'] if k == 0 else [])
        ax.tick_params(labelsize=6.5, length=2, pad=1.5)
        ax.set_title(title, fontsize=8, pad=9)
        for sp in ax.spines.values(): sp.set_visible(True); sp.set_linewidth(.5)
    fig.text(left - .045, bottom + height / 2, 'position on the map axis', rotation=90, ha='center', va='center', fontsize=7)
    fig.text((left + right) / 2, .025, 'December 1999 (day; hourly frames 355–460)', ha='center', fontsize=7)
    cax = fig.add_axes([right + .012, bottom, .012, height]); cb = fig.colorbar(im, cax=cax)
    cb.ax.tick_params(labelsize=6, length=2, pad=1); cb.set_label('SLP anomaly (hPa)', fontsize=6.5, labelpad=2)
    for ext in ('pdf', 'svg'):
        fig.savefig(FIG / f'teaser_storms_compare.{ext}', dpi=450)
    fig.savefig(HERE / 'preview_v20/teaser_storms_compare.png', dpi=220); plt.close(fig)
    print('storm track', TRACK, 'frames', t[0], t[-1], 'reference from', round(q[0], 3), 'to', round(q[-1], 3))
    print('AnchorMTM |x - q| of the storm (mean, max, % of axis):', stat)


if __name__ == '__main__':
    main()
