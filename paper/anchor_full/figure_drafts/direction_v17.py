"""Supplementary Fig. S2 of v17: direction dependence of the order bound (same data and encodings as
make_figs_anchor.fig_direction_column; only labels change: no method name, 'bound' instead of c0).

Input: ../figdata/bound_allowance20261105/<tangaroa|cylinder>_direction.json (saved, read only).
Output: ../../pvis2027/figures/fw_direction_v17.{pdf,png}
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata'; OUT = HERE.parents[1] / 'pvis2027/figures'
C = dict(A='#0072B2', B='#D55E00', D='#CC79A7', base='#7B8790', grid='#DFE4E8')
plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'pdf.fonttype': 42, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.linewidth': .6, 'legend.frameon': False})

fig = plt.figure(figsize=(3.4, 3.15))
g = fig.add_gridspec(2, 2, width_ratios=[.9, 1.35], hspace=.55, wspace=.45)
for k, n in enumerate(['Tangaroa', 'Cylinder']):
    D = json.loads((RES / f'bound_allowance20261105/{n.lower()}_direction.json').read_text())
    dirs = np.array([r['direction'] for r in D['sweep']]); nu = 100 * np.array([r['nu_allow'] for r in D['sweep']])
    ax = fig.add_subplot(g[k, 0])
    th = np.arccos(np.clip(dirs[:, 2], -1, 1)); ph = np.arctan2(dirs[:, 1], dirs[:, 0]); rr = np.sqrt(2) * np.sin(th / 2)
    sc = ax.scatter(rr * np.cos(ph), rr * np.sin(ph), c=nu, s=6, cmap='viridis', lw=0)
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, lw=.5, color='#999'))
    K = D['key_directions']
    for lab, mk in [('x', 'o'), ('y', 's'), ('z', '^'), ('stored', '*'), ('smallest bound', 'P')]:
        v = np.array(K[lab]['direction'], float); v = -v if v[2] < 0 else v
        t_, p_ = np.arccos(np.clip(v[2], -1, 1)), np.arctan2(v[1], v[0]); r_ = np.sqrt(2) * np.sin(t_ / 2)
        ax.plot(r_ * np.cos(p_), r_ * np.sin(p_), mk, ms=6 if mk == '*' else 4, mfc='white' if mk != '*' else C['B'], mec='k', mew=.6)
        if lab in ('x', 'y', 'z'): ax.annotate(lab, (r_ * np.cos(p_), r_ * np.sin(p_)), xytext=(3, 3), textcoords='offset points', fontsize=6)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.12, 1.12)
    cax = ax.inset_axes([.1, -.14, .8, .06]); cb = fig.colorbar(sc, cax=cax, orientation='horizontal')
    cb.ax.tick_params(labelsize=5.2, length=2); cb.set_label('mean order bound (%)', fontsize=5.6, labelpad=1)
    ax.set_title(n, fontsize=7, pad=2)
    ax = fig.add_subplot(g[k, 1]); labs = ['x', 'y', 'z', 'stored', 'smallest bound']; x = np.arange(len(labs)); w = .2
    for j, (key, col, lab) in enumerate([('nu_allow', '#000000', 'bound'), ('ours_NROE', C['A'], r'AnchorMTM, $\varepsilon=0$'),
                                          ('ST-MTM_NROE', C['D'], 'ST-MTM'), ('TMTM_NROE', C['base'], 'TMTM')]):
        ax.bar(x + (j - 1.5) * w, [100 * K[l][key] for l in labs], w, color=col, label=lab, lw=0)
    ax.set_xticks(x); ax.set_xticklabels(['x', 'y', 'z', 'stored', 'best'], fontsize=5.6)
    ax.set_ylabel('NROE (%)', fontsize=5.8); ax.tick_params(labelsize=5.4, length=2)
    ax.yaxis.grid(True, color=C['grid'], lw=.5); ax.set_axisbelow(True)
    if k == 0: fig.legend(*ax.get_legend_handles_labels(), ncol=2, fontsize=5.8, loc='upper center', bbox_to_anchor=(.55, 1.04),
                          handlelength=1, frameon=False, columnspacing=.8)
    print(n, 'bound range over', len(nu), 'directions: %.2f-%.2f%%' % (nu.min(), nu.max()))
fig.savefig(OUT / 'fw_direction_v17.pdf', bbox_inches='tight', pad_inches=.02)
fig.savefig(OUT / 'fw_direction_v17.png', dpi=200, bbox_inches='tight', pad_inches=.02)
