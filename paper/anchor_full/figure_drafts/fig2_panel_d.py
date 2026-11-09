"""v30 Fig. 2 panel (d): the same 35-sample field as panels (a)-(c) of the collaborator's mapping-strategy figure,
drawn as a spatially anchored topology-based profile (this paper). 2026-11-09.

Field (rows r1-r5 top to bottom, columns c1-c7) and colours copied from figure_sources/fig02_related_work.pptx:
A blue (r1-r2, c1-c2; extremum r2c1), B orange (r1-r2, c4-c6; extremum r1c5), C teal (r4-r5, c1-c4; extremum r5c3),
D purple (r4-r5, c6-c7; extremum r4c7); merge tree {A,B}{C,D}. Projecting the extrema onto the column direction
gives the reference order A, C, B, D, which interleaves the two sibling blocks.
Output: ../../pvis2027/latex_v30/figures/anchor_related_work_panel_d.{pdf,png}
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import v23_figures as v

OUT = Path(__file__).resolve().parents[2] / 'pvis2027/latex_v30/figures'
COL = dict(A='#0077FF', B='#FF9000', C='#00B999', D='#A324CD')
LIGHT = dict(A='#B9D9FB', B='#FDD9B0', C='#B4EDE1', D='#E6C6F0')
CELLS = dict(A=[(1, 1), (1, 2), (2, 1), (2, 2)], B=[(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6)],
             C=[(4, 1), (4, 2), (4, 3), (4, 4), (5, 1), (5, 2), (5, 3), (5, 4)], D=[(4, 6), (4, 7), (5, 6), (5, 7)])
EXT = dict(A=(2, 1), B=(1, 5), C=(5, 3), D=(4, 7))


def main():
    v.use_times()
    W, H = 6.9, 2.05
    fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    ax.add_patch(FancyBboxPatch((.02, .03), W - .04, H - .06, boxstyle='round,pad=0,rounding_size=.08', fc='white', ec='#9AA1A8', lw=.8))
    ax.add_patch(FancyBboxPatch((.02, H - .36), W - .04, .33, boxstyle='round,pad=0,rounding_size=.08', fc='#E9EBEE', ec='#9AA1A8', lw=.8))
    ax.text(.14, H - .195, '(d) Spatially anchored topology — AnchorMTM (this paper)', fontsize=10.5, fontweight='bold', va='center')
    # grid
    s = .19; x0, y0 = .45, .68
    cx = lambda c: x0 + (c - .5) * s
    cy = lambda r: y0 + (5 - r + .5) * s
    lab = {}
    for k, cells in CELLS.items():
        for r, c in cells: lab[(r, c)] = k
    for r in range(1, 6):
        for c in range(1, 8):
            k = lab.get((r, c))
            ax.add_patch(Rectangle((x0 + (c - 1) * s, y0 + (5 - r) * s), s, s, fc=LIGHT[k] if k else '#F2F3F5', ec='#C9CDD2', lw=.5))
    for k, (r, c) in EXT.items():
        ax.plot(cx(c), cy(r), 'D', ms=6.2, mfc=COL[k], mec='black', mew=.5, zorder=5)
        ax.plot([cx(c), cx(c)], [cy(r), y0 - .2], ls=(0, (2, 1.5)), color=COL[k], lw=.8, zorder=4)
        ax.text(cx(c), y0 - .3, k, color=COL[k], fontsize=9.5, fontweight='bold', ha='center', va='center')
    ax.add_patch(FancyArrowPatch((x0, y0 - .47), (x0 + 7 * s, y0 - .47), arrowstyle='-|>', mutation_scale=8, lw=.9, color='#333'))
    ax.text(x0 + 7 * s + .05, y0 - .47, r'$a^*$', fontsize=10, va='center')
    # right: tree, reference order vs exact profile order
    X0 = 2.45; xs = [X0 + .5 * i for i in range(4)]
    ax.text(X0 - .25, 1.32, r'$q$', fontsize=10, ha='right', va='center', style='italic')
    ax.text(X0 - .25, .62, r'$x$', fontsize=10, ha='right', va='center', style='italic')
    for y in (1.32, .62): ax.plot([X0 - .15, xs[-1] + .15], [y, y], color='#333', lw=.8)
    qord = ['A', 'C', 'B', 'D']; xord = ['A', 'B', 'C', 'D']
    pos_q = {k: xs[i] for i, k in enumerate(qord)}; pos_x = {k: xs[i] for i, k in enumerate(xord)}
    for k in 'ABCD':
        ax.plot(pos_q[k], 1.32, 'o', ms=5.5, mfc='white', mec=COL[k], mew=1.2, zorder=5)
        ax.plot(pos_x[k], .62, 'D', ms=5.5, mfc=COL[k], mec='black', mew=.4, zorder=5)
        ax.text(pos_q[k], 1.47, k, color=COL[k], fontsize=9, fontweight='bold', ha='center')
        ax.text(pos_x[k], .45, k, color=COL[k], fontsize=9, fontweight='bold', ha='center', va='top')
        ax.plot([pos_q[k], pos_x[k]], [1.28, .66], color=COL[k], lw=1.0)
    for a, b in (('A', 'B'), ('C', 'D')):
        ax.add_patch(FancyBboxPatch((pos_x[a] - .13, .53), pos_x[b] - pos_x[a] + .26, .18, boxstyle='round,pad=0,rounding_size=.05',
                                    fc='none', ec='#555', lw=.7, ls=(0, (2, 1.2))))
    ax.text(xs[-1] + .3, 1.32, 'reference order', fontsize=8.5, va='center')
    ax.text(xs[-1] + .3, .62, 'exact profile:\nblocks {A,B}, {C,D}', fontsize=8.5, va='center', linespacing=1.1)
    ax.text((xs[0] + xs[-1]) / 2, .18, 'B and C must leave their references', fontsize=8.5, ha='center', va='center', color='#333')
    # explanation
    ax.text(5.45, 1.0, 'Extrema keep their tree and\nget a fixed spatial target\nalong one direction. When\nsibling blocks interleave in\nspace, the bounds give the\nleast displacement; a merge\nbudget can release the blocks.',
            fontsize=8.0, ha="left", va="center", linespacing=1.15)
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'anchor_related_work_panel_d.{ext}', dpi=300)


if __name__ == '__main__':
    main()
