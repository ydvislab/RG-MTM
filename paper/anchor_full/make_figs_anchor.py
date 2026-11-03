"""Regenerate fig_compare and fig_frontier for the AnchorMTM draft without the earlier kappa construction.

Same data, layout and styling as paper/pvis2027/scripts/make_figures.py at upstream commit 91e1fb8
(functions compare_data, fig_compare, fig_frontier); only the 'kappa R20 (earlier)' markers and the
'earlier pool' curves are removed. Inputs: figdata/ (copies of code/results/* at 91e1fb8).
Run: python make_figs_anchor.py   (needs numpy, matplotlib)
"""
import csv, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent; RES = HERE / 'figdata'; FIG = HERE / 'figures'
NAMES = ['Storms', 'Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
FILE = {n: n.replace('.', '').lower() for n in NAMES}
LABEL = {n: (r'PM$_{2.5}$' if n == 'PM2.5' else n) for n in NAMES}
BUDGET = {n: json.loads((RES / f'order_budget20261027/{FILE[n]}.json').read_text()) for n in NAMES}
C = dict(A='#0072B2', B='#D55E00', C='#009E73', D='#CC79A7', base='#7B8790', grid='#DFE4E8', light='#56B4E9')
plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'pdf.fonttype': 42, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.linewidth': .6, 'xtick.major.width': .6, 'ytick.major.width': .6,
                     'legend.frameon': False, 'axes.titlesize': 7})
EX, BU = r'AnchorMTM, $\varepsilon=0$', r'AnchorMTM, $\varepsilon=10\%$'


def save(fig, stem):
    fig.savefig(FIG / f'{stem}.pdf', bbox_inches='tight', pad_inches=.02)
    fig.savefig(FIG / f'{stem}.png', dpi=200, bbox_inches='tight', pad_inches=.02); plt.close(fig)


def fig_frontier():
    F = {n: json.loads((RES / f'frontier20261027/{FILE[n]}.json').read_text())['methods'] for n in NAMES}
    fig, axes = plt.subplots(2, 4, figsize=(7.0, 3.0)); axes = axes.ravel()
    keys = [k for k in F['Ring'] if k.startswith('eps=')] + ['projection']
    for ax, n in zip(axes, NAMES):
        ms = [F[n][k] for k in keys]; x = [100 * m['NMLE_max'] for m in ms]
        for key, col, mk, lab in [('E_inf', C['A'], 'o', r'worst $E_\infty$'), ('E_pool', C['light'], 's', r'mean $E_{pool}$')]:
            y = [100 * m[key] for m in ms]
            ax.plot(x[:-1], y[:-1], '-', marker=mk, ms=2.6, lw=1, color=col, label=lab)
            ax.plot(x[-2:], y[-2:], ':', lw=.9, color=col)
            ax.plot(x[-1], y[-1], marker='*', ms=6, color=col, mec='k', mew=.3, ls='none')
        for k, xi, yi in zip(keys, x, [100 * m['E_inf'] for m in ms]):
            if k in ('eps=0', 'eps=0.02', 'eps=0.1', 'projection') and (k == 'projection' or abs(xi - x[-1]) + abs(yi - 100 * ms[-1]['E_inf']) > .3):
                lab = r'$\infty$' if k == 'projection' else '%g' % (100 * float(k[4:]))
                ax.annotate(lab, (xi, yi), xytext=(2, 2.5), textcoords='offset points', fontsize=5.4, color='#333')
        ax.set_title(LABEL[n], pad=2); ax.yaxis.grid(True, color=C['grid'], lw=.5); ax.set_axisbelow(True)
        ax.set_ylim(bottom=0); ax.set_xlim(left=-1); ax.tick_params(labelsize=5.8)
    for ax in axes[4:7]: ax.set_xlabel('Worst merge error NMLE (%)', fontsize=6.2)
    for ax in (axes[0], axes[4]): ax.set_ylabel('Displacement (%)', fontsize=6.4)
    h, l = axes[0].get_legend_handles_labels(); axes[7].axis('off')
    h += [plt.Line2D([], [], marker='*', ms=6, color=C['A'], mec='k', mew=.3, ls='none')]
    l += [r'projection ($\varepsilon=\infty$)']
    axes[7].legend(h, l, loc='center', fontsize=6.2, handlelength=1.6)
    axes[7].text(.5, .1, r'labels: $\varepsilon$ in %', transform=axes[7].transAxes, ha='center', fontsize=6)
    fig.subplots_adjust(hspace=.45, wspace=.28); save(fig, 'fig_frontier')


def compare_data():
    rows = list(csv.DictReader((RES / 'stmtm_completion20261026/unified_metrics.csv').open()))
    st = lambda n, m: next(r for r in rows if r['dataset'] == n and r['method'] == m)
    out = {}
    for n in NAMES:
        F = json.loads((RES / f'frontier20261027/{FILE[n]}.json').read_text())['methods']
        Q = json.loads((RES / f'metrics_n1c20261027/{FILE[n]}.json').read_text())['settings']
        me = lambda c: 100 * c['ME_errors'] / c['ME_clear']
        d = {}
        for m in ('TMTM', 'ST-MTM'):
            r = st(n, m)
            d[m] = dict(NROE=float(r['NROE']), NMLE=float(r['NMLE_max']), ME=100 * int(r['motion_errors']) / int(r['N_clear']),
                        SNS=float(r['SNS']), TW=float(r['TW1']))
        for m, fk in [('Projection', 'projection'), (EX, 'eps=0'), (BU, 'eps=0.1')]:
            d[m] = dict(NROE=100 * F[fk]['NROE'], NMLE=100 * F[fk]['NMLE_max'], ME=me(Q[fk]), SNS=Q[fk]['SNS'], TW=Q[fk]['TW1'])
        out[n] = d
    return out


def fig_compare():
    D = compare_data(); methods = list(D[NAMES[0]])
    style = {'TMTM': ('s', C['base']), 'ST-MTM': ('D', C['D']), 'Projection': ('*', '#000000'),
             EX: ('o', C['A']), BU: ('o', C['C'])}
    panels = [('NROE', 'Order error NROE (%)', 'lower'), ('NMLE', 'Worst merge error (%)', 'lower'),
              ('ME', 'Motion error ME (%)', 'lower'), ('SNS', 'Distance stress SNS', 'lower'), ('TW', 'Trustworthiness TW', 'higher')]
    fig, axes = plt.subplots(1, 5, figsize=(7.0, 2.05)); x = np.arange(len(NAMES)); off = np.linspace(-.28, .28, len(methods))
    for ax, (key, title, better) in zip(axes, panels):
        for k, m in enumerate(methods):
            mk, col = style[m]
            ax.plot(x + off[k], [D[n][m][key] for n in NAMES], mk, ms=3.6 if mk != '*' else 5, color=col,
                    mec='white' if mk != '*' else col, mew=.3, ls='none', label=m)
        if key == 'NROE':
            ax.hlines([100 * BUDGET[n]['nu_mean'] for n in NAMES], x - .42, x + .42, color='k', lw=1.1, zorder=1,
                      label=r'lower bound $\nu^*$')
        ax.set_xticks(x); ax.set_xticklabels([LABEL[n] for n in NAMES], fontsize=5.2, rotation=90)
        ax.set_title(title + (r' $\downarrow$' if better == 'lower' else r' $\uparrow$'), fontsize=6.2, pad=3)
        ax.tick_params(labelsize=5.4, length=2); ax.yaxis.grid(True, color=C['grid'], lw=.5); ax.set_axisbelow(True)
        for v in x[:-1] + .5: ax.axvline(v, color=C['grid'], lw=.4)
        ax.axvline(4.5, color='#999', lw=.6)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, ncol=6, fontsize=6, loc='upper center', bbox_to_anchor=(.5, 1.1), handlelength=1.2, columnspacing=1.0)
    fig.subplots_adjust(wspace=.38); save(fig, 'fig_compare')
    return D


def fig_direction_column():
    """Column-width version of fig_direction (same data and encodings): 2 rows x (disk, bars)."""
    fig = plt.figure(figsize=(3.4, 3.15))
    g = fig.add_gridspec(2, 2, width_ratios=[.9, 1.35], hspace=.55, wspace=.45)
    for k, n in enumerate(['Tangaroa', 'Cylinder']):
        D = json.loads((RES / f'reference_direction20261027/{n.lower()}.json').read_text())
        dirs = np.array([r['direction'] for r in D['sweep']]); nu = 100 * np.array([r['nu_mean'] for r in D['sweep']])
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
        cb.ax.tick_params(labelsize=5.2, length=2); cb.set_label(r'$\nu^*$ (%)', fontsize=5.6, labelpad=1)
        ax.set_title(n, fontsize=7, pad=2)
        ax = fig.add_subplot(g[k, 1]); labs = ['x', 'y', 'z', 'stored', 'smallest bound']; x = np.arange(len(labs)); w = .2
        for j, (key, col, lab) in enumerate([('nu_mean', '#000000', r'$\nu^*$'), ('ours_NROE', C['A'], r'AnchorMTM, $\varepsilon=0$'),
                                              ('ST-MTM_NROE', C['D'], 'ST-MTM'), ('TMTM_NROE', C['base'], 'TMTM')]):
            ax.bar(x + (j - 1.5) * w, [100 * K[l][key] for l in labs], w, color=col, label=lab, lw=0)
        ax.set_xticks(x); ax.set_xticklabels(['x', 'y', 'z', 'stored', 'best'], fontsize=5.6)
        ax.set_ylabel('NROE (%)', fontsize=5.8); ax.tick_params(labelsize=5.4, length=2)
        ax.yaxis.grid(True, color=C['grid'], lw=.5); ax.set_axisbelow(True)
        if k == 0: fig.legend(*ax.get_legend_handles_labels(), ncol=2, fontsize=5.8, loc='upper center', bbox_to_anchor=(.55, 1.04),
                              handlelength=1, frameon=False, columnspacing=.8)
    save(fig, 'fig_direction_col')


if __name__ == '__main__':
    fig_direction_column()
    D = fig_compare(); fig_frontier()
    for n in NAMES:
        print(n, {m: {k: round(v, 3) for k, v in D[n][m].items()} for m in D[n]})
