"""v26 paper Fig. 3, the AnchorMTM pipeline (2026-11-09), following pipeline_draft_v26.pptx (approved by the user).

Six columns: Input, (1) trees and reference, (2) price of the axis (new: the three bounds and the unreachable region,
drawn from the saved Storms plane data as in Fig. 5), (3) leaf order and anchors, (4) profiles and checks, Output
(new: the Storms map at epsilon = 10% with changed barriers marked and its per-frame record). Columns (1), (3), (4) and
the input frames are the collaborator's artwork (figures/anchor_framework.pdf), cropped at 300 dpi; text, boxes, arrows
and the two new panels are drawn here as vectors.
Run from this folder:  python fig3_v26.py  ->  ../../pvis2027/latex_v21/figures/anchor_pipeline_v26.{pdf,png}
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from PIL import Image
import plane_fig as pf
import v23_figures as v

HERE = Path(__file__).resolve().parent
ART = HERE.parents[1] / 'pvis2027/figure_drafts_v26'
OUT = HERE.parents[1] / 'pvis2027/latex_v21/figures'
RES = HERE.parent / 'figdata/maps20261030'
INK = '#222222'; EDGE = '#9AA1A8'; HEAD = '#F0F1F3'; NEW = '#FFF4E0'; NEWEDGE = '#E08214'; BLUE = '#0072B2'; BOXF = '#EEF5FB'
W, H = 7.05, 3.45
# columns: x, width (inches), header, new
COLS = [(0.02, 0.86, 'Input', False), (0.94, 1.28, '(1) Trees and reference', False), (2.28, 1.08, '(2) Price of the axis', True),
        (3.42, 1.30, '(3) Leaf order and anchors', False), (4.78, 1.30, '(4) Profiles and checks', False), (6.14, 0.89, 'Output', True)]
TOP, BOT, HH = H - 0.02, 0.03, 0.24


def ax_in(fig, x, y, w, h):
    return fig.add_axes([x / W, y / H, w / W, h / H])


def image(fig, name, x, y, w, h, crop=None):
    im = Image.open(ART / f'{name}.png')
    if crop: im = im.crop(crop)
    a = im.height / im.width
    if w * a > h: w2, h2 = h / a, h
    else: w2, h2 = w, w * a
    ax = ax_in(fig, x + (w - w2) / 2, y + (h - h2), w2, h2); ax.imshow(np.asarray(im), interpolation='lanczos'); ax.axis('off')
    return y + (h - h2)


def main():
    v.use_times()
    fig = plt.figure(figsize=(W, H)); bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, W); bg.set_ylim(0, H); bg.axis('off')
    for x, w, head, new in COLS:
        ec = NEWEDGE if new else EDGE; lw = 1.0 if new else .6
        bg.add_patch(Rectangle((x, BOT), w, TOP - BOT, fc='none', ec=ec, lw=lw))
        bg.add_patch(Rectangle((x, TOP - HH), w, HH, fc=NEW if new else HEAD, ec=ec, lw=lw))
        bg.text(x + w / 2, TOP - HH / 2, head, ha='center', va='center', fontsize=7.2, fontweight='bold', color=INK)
    for (x, w, *_), (x2, *__) in zip(COLS[:-1], COLS[1:]):
        bg.add_patch(FancyArrowPatch((x + w + .005, 1.75), (x2 - .005, 1.75), arrowstyle='-|>', mutation_scale=7, lw=1.0, color=BLUE))
    y0 = TOP - HH - .04
    # Input
    bg.text(0.45, y0 - .1, r'$F(x,t)$, budget $\varepsilon$', ha='center', va='center', fontsize=6.6)
    image(fig, 'input', 0.08, 0.38, 0.74, y0 - .27 - .38, crop=(60, 150, 545, 1790))
    bg.text(0.45, 0.2, 'scalar fields over\ntime, one budget', ha='center', va='center', fontsize=5.6, linespacing=1.05)
    # (1)
    image(fig, 'extract', 0.98, 0.42, 1.20, y0 - .02 - .42)
    bg.text(1.58, 0.22, r'merge trees $T_t$, matched supports,' '\n' r'one direction $a^*$, references $q$', ha='center', va='center',
            fontsize=5.6, linespacing=1.1)
    # (2) new: bounds
    x2 = 2.28
    bg.text(x2 + .54, y0 - .1, r'from $T$, $q$, $W$ only', ha='center', va='center', fontsize=6.2, color=NEWEDGE)
    rows = [(r'$\nu^*(T,q)$', 'exact tree'), (r'$\mathcal{B}_w(T,q,W)$', 'finite widths'), (r'$C_\eta(T,q)$', r'merge error $\leq\eta$')]
    for k, (a, b) in enumerate(rows):
        yy = y0 - .32 - k * .2
        bg.text(x2 + .06, yy, a, ha='left', va='center', fontsize=6.6); bg.text(x2 + 1.03, yy, b, ha='right', va='center', fontsize=5.6, color='#444')
    be, bv, fx, fy, pts = pf.series('Storms')
    ax = ax_in(fig, x2 + .25, 0.74, 0.76, 1.42)
    ax.fill_between(be, 0, bv, step='pre', color=pf.GREY, lw=0); ax.fill_between(be, 0, bv, step='pre', facecolor='none', edgecolor=pf.HATCH, hatch='////', lw=0)
    ax.step(be, bv, where='pre', color='k', lw=.8)
    ax.set_xscale('function', functions=(pf.fwd, pf.inv)); ax.set_xlim(0, 40); ax.set_ylim(0, 5.2)
    ax.text(.35, 1.0, 'unreachable', fontsize=5.4, color='#333', bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none'))
    ax.annotate(r'$\nu^*$', (0, bv[0]), xytext=(4, 4.5), fontsize=6.5, arrowprops=dict(arrowstyle='->', lw=.5))
    ax.set_xticks([0, 5, 20]); ax.set_yticks([0, 2, 4]); ax.tick_params(labelsize=5, length=1.5, pad=1)
    ax.set_xlabel(r'merge allowance $\eta$', fontsize=5.4, labelpad=0.5); ax.set_ylabel('least order error', fontsize=5.4, labelpad=0.5)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'): ax.spines[s].set_linewidth(.5)
    bg.text(x2 + .54, 0.3, 'known before layout:\nhow much the tree forces,\nwhere, and what\nmerge error releases it', ha='center', va='center',
            fontsize=5.6, linespacing=1.05)
    # (3)
    ytop = image(fig, 'layout', 3.46, 1.02, 1.22, y0 - .02 - 1.02)
    bg.add_patch(FancyBboxPatch((3.47, 0.6), 1.20, .36, boxstyle='round,pad=0.01,rounding_size=0.03', fc=BOXF, ec=BLUE, lw=.6))
    bg.text(4.07, 0.78, r'admit $\pi$ if $\delta^*(\pi)\leq\eta$ (closed form)' '\n' r'choose least $\tau(\pi)$, then NROE', ha='center',
            va='center', fontsize=5.6, linespacing=1.15)
    bg.text(4.07, 0.3, r'anchors: convex QP with' '\n' r'$\|x-q\|_\infty\leq\tau(\pi)+\beta_0$', ha='center', va='center', fontsize=5.6, linespacing=1.15)
    # (4)
    image(fig, 'mapping', 4.82, 1.02, 1.22, y0 - .02 - 1.02)
    bg.add_patch(FancyBboxPatch((4.83, 0.6), 1.20, .36, boxstyle='round,pad=0.01,rounding_size=0.03', fc=BOXF, ec=BLUE, lw=.6))
    bg.text(5.43, 0.78, r'barriers $b_k=C_k+\delta^*(\pi)$' '\n' r'check $d_{\mathrm{top}}\leq\eta$ on every frame', ha='center',
            va='center', fontsize=5.6, linespacing=1.15)
    bg.text(5.43, 0.3, r'profiles $\psi_t$ share origin,' '\n' 'direction and scale', ha='center', va='center', fontsize=5.6, linespacing=1.15)
    # Output: map with marked barriers + per-frame record
    M = np.load(RES / 'maps_era5.npz')['ours_0.1']; S = json.loads((RES / 'storms_case.json').read_text()); T = M.shape[1]
    ax = ax_in(fig, 6.32, 1.62, 0.66, 1.22)
    ax.imshow(M, origin='lower', aspect='auto', cmap='RdBu_r', extent=[-.5, T - .5, 0, 1], interpolation='nearest', rasterized=True)
    for t, mk in enumerate(S['marks_10']):
        if mk: ax.plot([t] * len(mk), mk, '_', ms=2.2, mew=.8, color='#FFD000')
    ax.set_xticks([]); ax.set_yticks([]); [s.set_linewidth(.4) for s in ax.spines.values()]
    ax.set_title(r'map $I^\varepsilon(t,u)$', fontsize=5.8, pad=1.5); ax.set_ylabel(r'position on $a^*$', fontsize=5.2, labelpad=1)
    ax2 = ax_in(fig, 6.32, 0.72, 0.66, 0.62); t = np.arange(T)
    ax2.plot(t, 100 * np.array(S['worst']['ours_0.1']), color=BLUE, lw=.6)
    ax2.plot(t, 100 * np.array(S['nmle_10']), color=NEWEDGE, lw=.6)
    ax2.axhline(10, color=NEWEDGE, lw=.5, ls='--')
    ax2.set_xlim(0, T - 1); ax2.set_ylim(0, 22); ax2.set_xticks([]); ax2.set_yticks([0, 10, 20]); ax2.tick_params(labelsize=4.8, length=1.2, pad=.8)
    ax2.set_title('per-frame record (%)', fontsize=5.6, pad=1.5)
    for s in ('top', 'right'): ax2.spines[s].set_visible(False)
    for s in ('left', 'bottom'): ax2.spines[s].set_linewidth(.4)
    bg.text(6.58, 0.36, 'barriers changed (yellow);\ndisplacement (blue),\nmerge error within $\\varepsilon$', ha='center', va='center',
            fontsize=5.4, linespacing=1.05)
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'anchor_pipeline_v26.{ext}', dpi=400)
    plt.close(fig)


if __name__ == '__main__':
    main()
