"""Tables and the Storms figure of the supplement (Part B), from saved results only.

Writes ../tables/supp_*.tex and ../figures/fig_supp_storms.{pdf,png}; prints the numbers it uses.
Inputs as in make_figure_drafts.py, plus ../figdata/olr_hovmoller/checks_p1_p2.json (olr_checks.py).
Run:  python make_supplement.py
"""
import csv, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata'; TAB = HERE.parent / 'tables'; FIG = HERE.parent / 'figures'
CODE = HERE.parents[2] / 'code' / 'results'
NAMES = ['Storms', 'Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
FILE = {n: n.replace('.', '').lower() for n in NAMES}
TEX = {n: (r'PM$_{2.5}$' if n == 'PM2.5' else n) for n in NAMES}
UNIFIED = {'Storms': 'era5', 'Wildfires': 'wildfire', 'OLR': 'olr', 'PM2.5': 'pm25_2000', 'Ring': 'ring'}
load = lambda p: json.loads(Path(p).read_text())
ROWS = list(csv.DictReader((RES / 'stmtm_completion20261026/unified_metrics.csv').open()))
st = lambda n, m: next(r for r in ROWS if r['dataset'] == n and r['method'] == m)
F = {n: load(RES / f'frontier20261027/{FILE[n]}.json') for n in NAMES}
Q = {n: load(RES / f'metrics_n1c20261027/{FILE[n]}.json')['settings'] for n in NAMES}
B = {n: load(RES / f'order_budget20261027/{FILE[n]}.json') for n in NAMES}
f2 = lambda v: f'{v:.2f}'; f3 = lambda v: f'{v:.3f}'


def table(path, caption, label, head, rows, spec, note=''):
    lines = [r'\begin{table}[h]', r'\centering\small\setlength{\tabcolsep}{3.2pt}', rf'\caption{{{caption}}}\label{{{label}}}',
             rf'\begin{{tabular}}{{{spec}}}\toprule', head + r'\\\midrule'] + [' & '.join(r) + r'\\' for r in rows] + [r'\bottomrule\end{tabular}']
    if note: lines.append(r'\par\smallskip\parbox{\linewidth}{\footnotesize ' + note + '}')
    lines.append(r'\end{table}'); (TAB / path).write_text('\n'.join(lines) + '\n')


def values():
    out = {}
    for n in NAMES:
        d = {}
        for m in ('TMTM', 'ST-MTM'):
            r = st(n, m); d[m] = dict(NROE=float(r['NROE']), NMLE=100 * float(r['NMLE_max']), ME=100 * int(r['motion_errors']) / int(r['N_clear']),
                                      SNS=float(r['SNS']), TW=float(r['TW1']), TD=float(r['TD']))
        for m, k in (('Exact', 'eps=0'), ('Budgeted', 'eps=0.1'), ('Projection', 'projection')):
            c = Q[n][k]; d[m] = dict(NROE=100 * F[n]['methods'][k]['NROE'], NMLE=100 * F[n]['methods'][k]['NMLE_max'],
                                     ME=100 * c['ME_errors'] / c['ME_clear'], SNS=c['SNS'], TW=c['TW1'], TD=c['TD'])
        d['nu'] = 100 * B[n]['nu_mean']; out[n] = d
    return out


M5 = ['TMTM', 'ST-MTM', 'Exact', 'Budgeted', 'Projection']
H5 = r'TMTM & ST-MTM & $\varepsilon{=}0$ & $\varepsilon{=}10\%$ & Proj.'
def two(first, groups, sub):
    head = first + ' & ' + ' & '.join(rf'\multicolumn{{{n}}}{{c}}{{{g}}}' for g, n in groups) + r'\\'
    c0 = first.count('&') + 2; rules = []
    for g, n in groups: rules.append(rf'\cmidrule(lr){{{c0}-{c0 + n - 1}}}'); c0 += n
    return head + ''.join(rules) + '\n' + ' & ' * (first.count('&') + 1) + sub


def tables_values(V):
    rows = [[TEX[n], f2(V[n]['nu'])] + [f2(V[n][m]['NROE']) for m in M5] + [f2(V[n][m]['NMLE']) for m in ('Budgeted', 'Projection')] for n in NAMES]
    table('supp_values_position.tex', r'Position and topology behind Fig.~4(a,b) of the paper (percent). $\nu^*$: mean exact-topology order bound; NROE: mean order error; NMLE: worst rendered merge error (zero for TMTM, ST-MTM and $\varepsilon=0$).',
          'tab:supp_values_position', two(r'Sequence & $\nu^*$', [('NROE', 5), ('NMLE', 2)], H5 + r' & $\varepsilon{=}10\%$ & Proj.'), rows, 'l' + 'r' * 8)
    rows = [[TEX[n]] + [f'{V[n][m]["ME"]:.1f}' for m in M5] + [f'{V[n][m]["TD"]:.1f}' for m in M5] for n in NAMES]
    table('supp_values_temporal.tex', r'Temporal measures behind Fig.~4(c) and the discussion. ME: share of clear approach or separation events shown wrongly (percent); TD: summed map displacement of matched features in canvas units, protocol of ST-MTM.',
          'tab:supp_values_temporal', two('Sequence', [(r'ME (\%)', 5), ('TD', 5)], H5 + ' & ' + H5), rows, 'l' + 'r' * 10)
    rows = [[TEX[n]] + [f3(V[n][m]['SNS']) for m in M5] + [f3(V[n][m]['TW']) for m in M5] for n in NAMES]
    table('supp_values_geometry.tex', r'Distance measures behind Fig.~4(d,e): scale-normalized stress (lower is better) and trustworthiness with $k=1$ (higher is better), protocol of ST-MTM.',
          'tab:supp_values_geometry', two('Sequence', [('SNS', 5), ('TW', 5)], H5 + ' & ' + H5), rows, 'l' + 'r' * 10)
    for n in NAMES:
        print('values', n, {m: {k: round(v, 3) for k, v in V[n][m].items()} for m in M5}, 'nu', round(V[n]['nu'], 3))


def unified_rows(n):
    d = load(CODE / f'unified20261025/{UNIFIED[n]}.json'); L = d['parameters']['canvas']
    assert d['frames'] == F[n]['frames'] and abs(L - F[n]['canvas']) < 1e-9
    tracks = [fi['tracks'] for fi in d['frame_inputs']]
    return d, L, tracks


def same_model_and_jumps():
    rows_d, rows_t = [], []
    for n in NAMES:
        fm = F[n]['methods']
        ours = [f'{100 * fm[k]["E_pool"]:.2f} / {100 * fm[k]["E_inf"]:.1f}' for k in ('eps=0', 'eps=0.1', 'projection')]
        jumps = {k: (100 * fm[k]['jump_mean'], 100 * fm[k]['anchor_motion_mean']) for k in ('eps=0', 'eps=0.1', 'projection')}
        if n in UNIFIED:
            d, L, tracks = unified_rows(n); base = []; bj = {}
            for key, m in (('topology_time', 'TMTM'), ('topology_geometry', 'ST-MTM')):
                R = d['regimes'][key]['rows']
                e = np.concatenate([np.abs(np.asarray(r['x'], float) - np.asarray(r['reference'], float)) / L for r in R])
                base.append(f'{100 * e.mean():.2f} / {100 * e.max():.1f}')
                jm, mv = [], []
                for t in range(1, len(R)):
                    prev = {tr: i for i, tr in enumerate(tracks[t - 1])}
                    for j, tr in enumerate(tracks[t]):
                        if tr in prev:
                            i = prev[tr]; du = R[t]['x'][j] - R[t - 1]['x'][i]; dq = R[t]['reference'][j] - R[t - 1]['reference'][i]
                            jm.append(abs(du - dq) / L); mv.append(abs(du) / L)
                bj[m] = (100 * np.mean(jm), 100 * np.mean(mv))
            rows_d.append([TEX[n]] + base + ours)
            rows_t.append([TEX[n]] + [f'{bj[m][0]:.2f} / {bj[m][1]:.2f}' for m in ('TMTM', 'ST-MTM')] + [f'{jumps[k][0]:.2f} / {jumps[k][1]:.2f}' for k in ('eps=0', 'eps=0.1', 'projection')])
        else:
            rows_d.append([TEX[n], '--', '--'] + ours)
            rows_t.append([TEX[n], '--', '--'] + [f'{jumps[k][0]:.2f} / {jumps[k][1]:.2f}' for k in ('eps=0', 'eps=0.1', 'projection')])
    hd = r'Sequence & TMTM obj. & ST-MTM obj. & $\varepsilon{=}0$ & $\varepsilon{=}10\%$ & Projection'
    table('supp_same_model.tex', r'Displacement in one interval model, mean $E_{\mathrm{pool}}$ / worst $E_\infty$ (percent of $L$). TMTM and ST-MTM objectives: their objectives solved with exact topology in the same interval model, references and canvas (grey boxes of Fig.~5 of the paper); available for the planar sequences.',
          'tab:supp_same_model', hd, rows_d, 'lrrrrr')
    table('supp_jumps.tex', r'Layout-induced jump $|\Delta x_i-\Delta q_i|/L$ / anchor motion $|\Delta x_i|/L$ of matched features per step (percent), same interval model. A map that keeps its features still while their references move has a jump close to the reference motion.',
          'tab:supp_jumps', hd, rows_t, 'lrrrrr')
    for r in rows_d: print('same-model', r)
    for r in rows_t: print('jumps', r)


def table_ties():
    keys = ['0', '1e-08', '1e-07', '1e-06', '1e-05']
    rows = [[TEX[n]] + [f'{100 * B[n]["nu_tie_sensitivity"][k]:.2f}' for k in keys] + [f'{100 * B[n]["nu_mean"]:.2f}'] for n in NAMES]
    table('supp_ties.tex', r'Sensitivity of the mean order bound $\nu^*$ (percent) to the relative tie tolerance on merge levels. Saddles closer than the tolerance are treated as one multifurcation. Last column: value used in the paper.',
          'tab:supp_ties', r'Sequence & 0 & $10^{-8}$ & $10^{-7}$ & $10^{-6}$ & $10^{-5}$ & paper', rows, 'lrrrrrr',
          note=r'Only Cylinder is sensitive: about half of its hierarchy cost comes from merge levels that differ by less than $10^{-6}$ of the scalar range.')
    for r in rows: print('ties', r)


def tables_olr():
    C = load(RES / 'olr_hovmoller/checks_p1_p2.json')
    rows = []
    for name, lab in (('Hovmoller', r'Hovm\"oller'), ('AnchorMTM eps=0', r'AnchorMTM, $\varepsilon=0$'), ('AnchorMTM eps=10%', r'AnchorMTM, $\varepsilon=10\%$')):
        r = C['P1'][name]
        rows.append([lab] + [f"{100 * r[f'delta={d}']['fraction']:.1f}" for d in ('0.02', '0.05')] +
                    [f"{r[f'delta={d}']['depth_mean']:.1f} / {r[f'delta={d}']['depth_median']:.1f}" for d in ('0.02', '0.05')])
    table('supp_olr_resolution.tex', r'OLR, 60 days, 264 minima. Share of minima with their own profile dip within $\delta$ of their reference position (percent; one-to-one, nearest first), and depth error of matched dips, mean / median (W\,m$^{-2}$). $\delta$ was fixed before the evaluation.',
          'tab:supp_olr_resolution', r'Profile & $\delta{=}2\%$ & $\delta{=}5\%$ & depth, $\delta{=}2\%$ & depth, $\delta{=}5\%$', rows, 'lrrrr')
    rows = []
    lab = {'topology_time': 'TMTM objective', 'topology_geometry': 'ST-MTM objective', 'ours_0': r'AnchorMTM, $\varepsilon=0$',
           'ours_0.1': r'AnchorMTM, $\varepsilon=10\%$', 'Hovmoller': r'Hovm\"oller'}
    for n in ('OLR', 'Storms', 'Ring'):
        r = C['P2'][n]
        for k in ('topology_time', 'topology_geometry', 'ours_0', 'ours_0.1', 'Hovmoller'):
            if k not in r: continue
            v = r[k]; fmt = lambda x: '--' if x is None else f'{100 * x:.2f}'
            rows.append([f"{n} ({r['event_steps']}/{r['steps']})", lab[k], fmt(v['mean']), fmt(v['no_event']), fmt(v['event']), f"{v['spearman_events']:.2f}"])
    table('supp_column_change.tex', r'Mean column change $\frac{1}{L}\int|I(t{+}1,u)-I(t,u)|\,du$ of the rendered maps, in percent of the scalar range, overall and at steps without and with a topological event (a tracked minimum appears or vanishes), and its Spearman correlation with the number of events. In parentheses: steps with an event / all steps.',
          'tab:supp_column_change', r'Sequence & Map & all & no event & event & $\rho_S$', rows, 'llrrrr')


def fig_storms():
    Mp = dict(np.load(RES / 'maps20261030/maps_era5.npz')); qs = load(RES / 'maps20261030/q_era5.json'); S = load(RES / 'maps20261030/storms_case.json')
    cols = [('topology_time', 'TMTM objective', '#7B8790'), ('topology_geometry', 'ST-MTM objective', '#CC79A7'),
            ('ours_0', r'AnchorMTM, $\varepsilon=0$', '#0072B2'), ('ours_0.1', r'AnchorMTM, $\varepsilon=10\%$', '#009E73')]
    vmin = min(np.nanmin(Mp[k]) for k, *_ in cols); vmax = max(np.nanmax(Mp[k]) for k, *_ in cols)
    plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'pdf.fonttype': 42, 'mathtext.fontset': 'dejavusans'})
    fig = plt.figure(figsize=(7.0, 3.3)); g = fig.add_gridspec(2, 5, width_ratios=[1] * 4 + [.04], height_ratios=[1, .45], hspace=.38, wspace=.1)
    for c, (k, title, col) in enumerate(cols):
        ax = fig.add_subplot(g[0, c]); T = Mp[k].shape[1]
        im = ax.imshow(Mp[k], origin='lower', aspect='auto', cmap='RdBu_r', vmin=vmin, vmax=vmax, extent=[-.5, T - .5, 0, 1], interpolation='nearest', rasterized=True)
        for t, q in enumerate(qs): ax.plot([t] * len(q), q, 'o', ms=1.1, mfc='k', mec='white', mew=.2)
        if k == 'ours_0.1':
            for t, mk in enumerate(S['marks_10']):
                if mk: ax.plot([t] * len(mk), mk, '_', ms=3, mew=1, color='#FFD000')
        ax.set_title(title, fontsize=6.4, color=col if c else '#555', pad=2); ax.set_xticks([0, T - 1]); ax.tick_params(labelsize=5.4, length=1.5)
        for lab_, ha_ in zip(ax.get_xticklabels(), ('left', 'right')): lab_.set_ha(ha_)
        ax.set_yticks([0, 1] if c == 0 else []); ax.set_yticklabels(['W', 'E'] if c == 0 else [], fontsize=5.4)
        if c == 0: ax.set_ylabel('reference axis', fontsize=6)
    cb = fig.colorbar(im, cax=fig.add_subplot(g[0, 4])); cb.ax.tick_params(labelsize=5, length=1.5); cb.set_label('MSLP (hPa)', fontsize=5.6)
    ax = fig.add_subplot(g[1, :2])
    for k, title, col in cols: ax.plot(100 * np.array(S['worst'][k]), lw=.8, color=col, label=title)
    ax.set_ylabel('worst displacement\nper step (%)', fontsize=5.8); ax.set_xlabel('time step', fontsize=5.8); ax.tick_params(labelsize=5.2, length=1.5)
    ax.legend(fontsize=5, ncol=2, frameon=False, loc='upper right'); ax.spines[['top', 'right']].set_visible(False)
    ax = fig.add_subplot(g[1, 2:4]); ax.bar(range(len(S['nmle_10'])), 100 * np.array(S['nmle_10']), color='#E69F00', width=.9)
    ax.axhline(10, ls='--', lw=.6, color='k'); ax.text(len(S['nmle_10']) - 1, 10.4, r'allowance $\varepsilon=10\%$', ha='right', fontsize=5)
    ax.set_ylabel('merge error (%)', fontsize=5.8); ax.set_xlabel(r'time step ($\varepsilon=10\%$)', fontsize=5.8); ax.tick_params(labelsize=5.2, length=1.5)
    ax.spines[['top', 'right']].set_visible(False)
    for e in ('pdf', 'png'): fig.savefig(FIG / f'fig_supp_storms.{e}', dpi=220, bbox_inches='tight', pad_inches=.02)
    w = {k: 100 * np.mean(v) for k, v in S['worst'].items()}; n10 = np.array(S['nmle_10'])
    print('storms mean worst per step', {k: round(v, 2) for k, v in w.items()}, 'steps with budget', int((n10 > 1e-9).sum()), 'max', round(100 * n10.max(), 2),
          'mean', round(100 * n10.mean(), 2), 'marked barriers', sum(len(m) for m in S['marks_10']))


if __name__ == '__main__':
    tables_values(values()); same_model_and_jumps(); table_ties(); tables_olr(); fig_storms()
