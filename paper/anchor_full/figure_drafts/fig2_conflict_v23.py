"""v23 Fig. 2: reference-topology conflict, vector schematic (replaces the image-generated anchor_conflict_open.pdf).

Tree ((A,B),(C,D)); references in the order A, C, B, D (the configuration of Fig. 3 and of the controlled trees of
Fig. 4 with d = 0.15). Any exact profile keeps {A,B} and {C,D} contiguous; the shaded overlap of the two reference
ranges is what Theorem 1 charges (half of it). Positions are schematic but consistent: x is a midpoint-ordered,
non-overlapping placement.
Output: ../../pvis2027/latex_v21/figures/anchor_conflict_v23.{pdf,svg}
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from v23_figures import use_times, LEAF

HERE = Path(__file__).resolve().parent; FIG = HERE.parents[1] / 'pvis2027/latex_v21/figures'
q = {'A': .20, 'C': .35, 'B': .50, 'D': .65}           # reference order A, C, B, D
x = {'A': .20, 'B': .40, 'C': .52, 'D': .70}           # an exact profile: blocks {A,B} then {C,D}
W = .07                                                # schematic interval width


def arrow(ax, x0, y0, x1, y1, c, lw=.8):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', lw=lw, color=c, mutation_scale=6, shrinkA=0, shrinkB=0))


def main():
    use_times()
    fig, ax = plt.subplots(figsize=(3.4, 2.15)); ax.set_xlim(0, 1); ax.set_ylim(-.24, 1.06); ax.axis('off')
    yq, yx = .55, .12                                   # reference axis q, exact-profile axis x
    # merge tree ((A,B),(C,D)) with leaves in tree order, top right
    lx = {'A': .62, 'B': .70, 'C': .80, 'D': .88}
    for k, v in lx.items():
        ax.plot([v, v], [.80, .89], color=LEAF[k], lw=1.6)
        ax.text(v, .76, k, ha='center', va='center', fontsize=7.5, color=LEAF[k], style='italic')
    ax.plot([lx['A'], lx['B']], [.89] * 2, 'k', lw=.7); ax.plot([lx['C'], lx['D']], [.89] * 2, 'k', lw=.7)
    ax.plot([.66, .66, .84, .84], [.89, .97, .97, .89], 'k', lw=.7)
    ax.text(.56, .89, 'merge tree', ha='right', va='center', fontsize=7)
    ax.text(.03, .97, r'references interleave: $A, C, B, D$', fontsize=7, ha='left', va='center')
    # reference axis q
    arrow(ax, .06, yq, .97, yq, 'k', .7)
    ax.text(.045, yq, '$q$', ha='right', va='center', fontsize=9)
    ax.add_patch(Rectangle((q['C'], yq - .045), q['B'] - q['C'], .09, color='#d9dde1', lw=0, zorder=0))
    ax.text((q['C'] + q['B']) / 2, yq + .16, 'range overlap', ha='center', va='center', fontsize=6.5, color='#555555')
    for k, v in q.items():
        ax.plot(v, yq, 'o', ms=5.5, mfc='white', mec=LEAF[k], mew=1.2, zorder=3)
        ax.text(v, yq + .075, k, ha='center', va='center', fontsize=7.5, color=LEAF[k], style='italic')
    # exact profile axis x
    arrow(ax, .06, yx, .97, yx, 'k', .7)
    ax.text(.045, yx, '$x$', ha='right', va='center', fontsize=9)
    for k, v in x.items():
        ax.add_patch(Rectangle((v - W / 2, yx - .03), W, .06, color=LEAF[k], alpha=.25, lw=0, zorder=1))
        ax.plot(v, yx, 'o', ms=5.5, color=LEAF[k], mec='white', mew=.5, zorder=3)
        ax.text(v, yx - .08, k, ha='center', va='center', fontsize=7.5, color=LEAF[k], style='italic')
        arrow(ax, q[k], yq - .04, v, yx + .035, LEAF[k])
    for a, b, lab in (('A', 'B', r'$\{A,B\}$'), ('C', 'D', r'$\{C,D\}$')):
        ax.plot([x[a] - W / 2, x[b] + W / 2], [yx - .14] * 2, color='k', lw=.6)
        ax.text((x[a] + x[b]) / 2, yx - .2, lab, ha='center', va='center', fontsize=7)
    ax.text(.97, yx - .19, 'exact profile:\ncontiguous blocks', ha='right', va='center', fontsize=6.5, linespacing=1.0)
    for ext in ('pdf', 'svg'):
        fig.savefig(FIG / f'anchor_conflict_v23.{ext}', bbox_inches='tight', pad_inches=.01)
    fig.savefig(HERE / 'preview_v20/anchor_conflict_v23.png', dpi=300, bbox_inches='tight', pad_inches=.01); plt.close(fig)
    nu = (q['B'] - q['C']) / 2
    print('overlap', round(q['B'] - q['C'], 3), 'nu* (point model, unit canvas)', round(nu, 3),
          'displacements', {k: round(abs(x[k] - q[k]), 3) for k in q})


if __name__ == '__main__':
    main()
