"""Draft figures for the redesign proposed in notes/2026-11-04-review-and-figure-plan.md.

Everything is drawn from saved results; no experiment is rerun.
  ../figdata/{frontier,metrics_n1c,order_budget}20261027, ../figdata/stmtm_completion20261026  (as make_figs_anchor.py)
  ../figdata/maps20261030/   rendered maps and Storms case data cached by the collaborator's
                             paper/pvis2027/scripts/make_figures.py at upstream commit 91e1fb8
  ../../../code/results/unified20261025/   TMTM- and ST-MTM-objective layouts in the same interval model
  ../../../code/results/controlled_conflict20261030/   four-leaf controlled trees
The concept and design-space figures are schematics computed exactly for the paper's four-leaf example
(sibling pairs merging at 0.4 below a root at 1, references (0.2, 0.5, 0.5-d, 0.8-d), d = 0.24).

Run:  python make_figure_drafts.py      (numpy, matplotlib)
Outputs: draft_*.pdf / draft_*.png in this folder; numbers used are printed.
"""
import csv, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata'; CODE = HERE.parents[2] / 'code' / 'results'
NAMES = ['Storms', 'Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
FILE = {n: n.replace('.', '').lower() for n in NAMES}
UNIFIED = {'Storms': 'era5', 'Wildfires': 'wildfire', 'OLR': 'olr', 'PM2.5': 'pm25_2000', 'Ring': 'ring'}
LABEL = {n: (r'PM$_{2.5}$' if n == 'PM2.5' else n) for n in NAMES}

# One palette for the whole paper: methods keep their colour and shape in every figure.
M = {'TMTM': dict(c='#7B8790', mk='s', fill=True), 'ST-MTM': dict(c='#CC79A7', mk='D', fill=True),
     'Exact': dict(c='#0072B2', mk='o', fill=True), 'Budgeted': dict(c='#009E73', mk='o', fill=False),
     'Projection': dict(c='#000000', mk='*', fill=True)}
MLAB = {'TMTM': 'TMTM', 'ST-MTM': 'ST-MTM', 'Exact': r'AnchorMTM, $\varepsilon=0$', 'Budgeted': r'AnchorMTM, $\varepsilon=10\%$',
        'Projection': 'Projection'}
LEAF = {'A': '#D55E00', 'B': '#E69F00', 'C': '#5E3C99', 'D': '#B2ABD2'}   # subtree X warm, subtree Y purple
GRID = '#E3E7EA'; FORCED = '#2B2B2B'
plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'pdf.fonttype': 42, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.linewidth': .6, 'xtick.major.width': .6, 'ytick.major.width': .6,
                     'legend.frameon': False, 'axes.titlesize': 7.2, 'axes.titleweight': 'bold', 'mathtext.fontset': 'dejavusans'})


def save(fig, stem):
    fig.savefig(HERE / f'{stem}.pdf', bbox_inches='tight', pad_inches=.03)
    fig.savefig(HERE / f'{stem}.png', dpi=220, bbox_inches='tight', pad_inches=.03); plt.close(fig)


def mstyle(key, ms=4):
    s = M[key]; return dict(marker=s['mk'], ms=ms * (1.5 if s['mk'] == '*' else 1), color=s['c'],
                            mfc=s['c'] if s['fill'] else 'white', mec=s['c'] if s['mk'] != '*' else 'k',
                            mew=.9 if not s['fill'] else .3, ls='none')


def load(path): return json.loads(Path(path).read_text())


BUDGET = {n: load(RES / f'order_budget20261027/{FILE[n]}.json') for n in NAMES}
FRONT = {n: load(RES / f'frontier20261027/{FILE[n]}.json') for n in NAMES}
ROWS = list(csv.DictReader((RES / 'stmtm_completion20261026/unified_metrics.csv').open()))
def st(n, m): return next(r for r in ROWS if r['dataset'] == n and r['method'] == m)


# ------------------------------------------------------------------ schematic example (exact)
D_OV = .24; Q = dict(A=.2, B=.5, C=.5 - D_OV, D=.8 - D_OV); INNER = .4; ROOT = 1.0
HW = .015          # half display width: rho * W / 2 with W = 0.06, rho = 0.5; gap 0.01 => centre separation 0.04
TAU = (D_OV + .04) / 2   # interval optimum of the controlled example (0.14); point bound nu* = d/2 = 0.12
EXACT = dict(order='ABCD', x=dict(A=Q['A'], B=Q['B'] - TAU, C=Q['C'] + TAU, D=Q['D']), bar=[INNER, ROOT, INNER])
EPS_DEMO = (ROOT - INNER) / 2   # 0.3 = h/2: the allowance at which the conflict disappears (Theorem 3)
BUDG = dict(order='ACBD', x=dict(Q), bar=[ROOT - EPS_DEMO] * 3)
TRUE = {frozenset('AB'): INNER, frozenset('CD'): INNER}


def merge_true(a, b): return TRUE.get(frozenset(a + b), ROOT)


def merge_error(L):
    o = L['order']; b = L['bar']; err = 0
    for i in range(4):
        for j in range(i + 1, 4):
            err = max(err, abs(max(b[i:j]) - merge_true(o[i], o[j])))
    return err


def field():
    x, y = np.meshgrid(np.linspace(.05, .75, 300), np.linspace(.05, .95, 380))
    band = lambda c: np.exp(-((y - c) / .12) ** 2)
    pos = dict(A=(Q['A'], .72), B=(Q['B'], .72), C=(Q['C'], .28), D=(Q['D'], .28))
    f = ROOT - (ROOT - INNER) * (band(.72) + band(.28))
    for p in pos.values(): f -= INNER * np.exp(-((x - p[0]) ** 2 + (y - p[1]) ** 2) / .055 ** 2)
    return x, y, f, pos


def profile_path(L):
    o = L['order']; xs = [L['x'][k] for k in o]; px, py = [xs[0] - HW - .05], [ROOT]
    for i, k in enumerate(o):
        px += [xs[i] - HW, xs[i] + HW]; py += [0, 0]
        if i < 3: px.append((xs[i] + HW + xs[i + 1] - HW) / 2); py.append(L['bar'][i])
    px.append(xs[-1] + HW + .05); py.append(ROOT)
    return np.array(px), np.array(py)


def draw_profile(ax, L, title, mode):
    px, py = profile_path(L); col = M[mode]['c']
    ax.plot(px, py, color='k', lw=1)
    for k in L['order']:
        ax.add_patch(Rectangle((L['x'][k] - HW, -.02), 2 * HW, .04, color=LEAF[k], lw=0, zorder=3))
        ax.text(L['x'][k], -.13, k, ha='center', va='top', fontsize=6.5, color=LEAF[k], fontweight='bold')
    # one map column: the profile colour-coded along the axis
    xx = np.linspace(px[0], px[-1], 400); strip = np.interp(xx, px, py)
    ax.imshow(strip[None, :], extent=[px[0], px[-1], -.52, -.36], aspect='auto', cmap='RdBu_r', vmin=-.25, vmax=1.25)
    for k in 'ABCD':
        ax.plot(Q[k], -.62, '^', ms=3.6, color='k', clip_on=False)
        moved = abs(L['x'][k] - Q[k]) > 1e-9
        ax.plot([Q[k], L['x'][k]], [-.6, -.52], '-', lw=1.1 if moved else .5, color=col if moved else '#777', clip_on=False)
    for lv in (INNER, ROOT): ax.axhline(lv, color=GRID, lw=.6, zorder=0)
    if mode == 'Budgeted':
        for i in range(3): ax.plot(px[3 * i + 3], L['bar'][i], 'o', ms=3.5, mfc=col, mec='k', mew=.4, zorder=4)
        note = 'all barriers at 0.7\n' r'merge error $0.3=\varepsilon$, position error 0'
    else:
        note = 'merge error 0\n' r'B, C displaced 14% (points: $\nu^*=12\%$)'
    ax.text(.5, 1.01, note, transform=ax.transAxes, ha='center', va='bottom', fontsize=5.6, linespacing=1.1)
    ax.set_xlim(.08, .68); ax.set_ylim(-.7, 1.12); ax.set_yticks([0, .4, 1]); ax.tick_params(labelsize=5.6, length=2)
    ax.set_xticks([]); ax.spines['bottom'].set_visible(False); ax.set_ylabel('scalar', fontsize=6, labelpad=1)
    ax.set_title(title, color=col, pad=17)


def fig_concept():
    print('concept: merge error exact', merge_error(EXACT), 'budgeted', round(merge_error(BUDG), 3),
          'tau', TAU, 'nu*', D_OV / 2)
    fig = plt.figure(figsize=(7.0, 1.95))
    g = fig.add_gridspec(1, 4, width_ratios=[1.05, .8, 1.15, 1.15], wspace=.32)
    # (a) field and reference
    ax = fig.add_subplot(g[0]); x, y, f, pos = field()
    ax.contourf(x, y, f, levels=14, cmap='RdBu_r', vmin=-.25, vmax=1.25)
    for k, (px, py) in pos.items():
        ax.plot(px, py, 'o', ms=4, color=LEAF[k], mec='k', mew=.4); ax.text(px + .03, py + .04, k, fontsize=6.5, fontweight='bold', color='k')
        ax.plot([px, px], [py, -.02], ':', lw=.6, color='#333', clip_on=False)
    ax.annotate('', (.74, -.02), (.06, -.02), arrowprops=dict(arrowstyle='-|>', lw=.8, color='k'), annotation_clip=False)
    for k in 'ABCD': ax.plot(Q[k], -.02, '^', ms=3.6, color='k', clip_on=False)
    ax.text(.4, -.08, 'reference direction:  order A C B D', ha='center', va='top', fontsize=5.8)
    ax.set_xlim(.05, .75); ax.set_ylim(.05, .95); ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('auto')
    for s in ax.spines.values(): s.set_visible(True); s.set_linewidth(.5)
    ax.set_title('(a) Features and reference', pad=17)
    # (b) merge tree
    ax = fig.add_subplot(g[1]); X = dict(A=0, B=1, C=2, D=3)
    for k, xi in X.items():
        ax.plot([xi, xi], [0, INNER], color=LEAF[k], lw=1.6); ax.plot(xi, 0, 'o', ms=4, color=LEAF[k], mec='k', mew=.4)
        ax.text(xi, -.08, k, ha='center', va='top', fontsize=6.5, fontweight='bold', color=LEAF[k])
    for a, b, lab in [(0, 1, 'X'), (2, 3, 'Y')]:
        ax.plot([a, b], [INNER, INNER], 'k', lw=.9); ax.plot([(a + b) / 2] * 2, [INNER, ROOT], 'k', lw=.9)
        ax.text((a + b) / 2 + .08, INNER + .05, lab, fontsize=6.3, style='italic')
    ax.plot([.5, 2.5], [ROOT, ROOT], 'k', lw=.9); ax.plot([1.5, 1.5], [ROOT, ROOT + .12], 'k', lw=.9)
    ax.axhline(INNER, color=GRID, lw=.5, zorder=0); ax.axhline(ROOT, color=GRID, lw=.5, zorder=0)
    ax.set_yticks([0, INNER, ROOT]); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
    ax.set_ylim(-.3, 1.32); ax.set_xlim(-.5, 3.5); ax.tick_params(labelsize=5.6, length=2)
    ax.set_ylabel('merge level', fontsize=6, labelpad=1)
    ax.text(1.5, -.3, 'tree needs (A B)(C D) contiguous\nreference interleaves them', ha='center', va='top', fontsize=5.6)
    ax.set_title('(b) Merge tree', pad=17)
    draw_profile(fig.add_subplot(g[2]), EXACT, r'(c) Exact Mode, $\varepsilon=0$', 'Exact')
    draw_profile(fig.add_subplot(g[3]), BUDG, r'(d) Budgeted Mode, $\varepsilon=30\%$', 'Budgeted')
    fig.text(.995, -.07, r'$\blacktriangle$ reference position; coloured link: displacement on the map; strip: the profile as one map column', ha='right', fontsize=5.6)
    save(fig, 'draft_concept')


# ------------------------------------------------------------------ design space
def fig_design_space():
    eps = [0, 1, 2, 5, 10, 20, 50]; xs = list(range(len(eps))); xinf = len(eps) + .6
    fig, ax = plt.subplots(figsize=(3.45, 2.05))
    ax.axvspan(-.45, .45, color=M['Exact']['c'], alpha=.06, lw=0)
    ax.text(0, 1.62, 'exact topology\n(Thm. 1 measures\nevery map here)', ha='center', va='top', fontsize=5.4, color='#335')
    ax.plot(xs, [1] * len(xs), '-', color=M['Exact']['c'], lw=1.6, zorder=1)
    cm = plt.get_cmap('Blues')
    for xi, e in zip(xs, eps):
        ax.plot(xi, 1, 'o', ms=5, mfc=cm(.95 - .6 * xi / len(eps)), mec='white', mew=.6, zorder=3)
        ax.text(xi, 1.09, f'{e}', ha='center', fontsize=5.4)
    ax.text(3, 1.2, r'AnchorMTM: one control $\varepsilon$ (%)', ha='center', fontsize=6.2, color=M['Exact']['c'], fontweight='bold')
    ax.plot([xs[-1], xinf], [1, 1], ':', color=M['Exact']['c'], lw=1)
    ax.plot(xinf, 1, **mstyle('Projection', 5)); ax.text(xinf, 1.09, r'$\infty$', ha='center', fontsize=5.8)
    ax.text(xinf, .9, 'Projection\n(reference order,\ntree broken)', ha='center', va='top', fontsize=5.4)
    ax.plot(-.12, 0, **mstyle('TMTM', 5)); ax.plot(.12, 0, **mstyle('ST-MTM', 5))
    ax.text(.4, 0, r'TMTM ($E_O$), ST-MTM ($E_G, E_M, E_W$)' '\naxis free: no reference, no cap', va='center', fontsize=5.6)
    ax.add_patch(FancyArrowPatch((0, .1), (0, .88), arrowstyle='-|>', mutation_scale=7, lw=.9, color='#444'))
    ax.text(.1, .5, 'add reference and cap:\n54–95% of order error removed', fontsize=5.4, va='center', color='#333')
    ax.text(3.6, .55, r'Thm. 3: within allowance $\eta$' '\n' r'Thm. 2: interval model', fontsize=5.4, color='#335', ha='left')
    ax.set_xticks([0, 3, xinf]); ax.set_xticklabels(['0', 'merge-level allowance', r'$\infty$'], fontsize=5.8)
    ax.set_yticks([0, 1]); ax.set_yticklabels(['none', r'cap $\tau_t+\beta_0$'], fontsize=5.8)
    ax.set_ylabel('position constraint', fontsize=6.2); ax.set_xlim(-.6, xinf + .6); ax.set_ylim(-.3, 1.7)
    ax.tick_params(length=0); ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
    ax.set_title('Merge tree maps as instances of one formulation', pad=3)
    save(fig, 'draft_design_space')


# ------------------------------------------------------------------ order-error decomposition + compare
def compare_values():
    out = {}
    for n in NAMES:
        F = FRONT[n]['methods']; Qs = load(RES / f'metrics_n1c20261027/{FILE[n]}.json')['settings']
        me = lambda c: 100 * c['ME_errors'] / c['ME_clear']; d = {}
        for m in ('TMTM', 'ST-MTM'):
            r = st(n, m); d[m] = dict(NROE=float(r['NROE']), NMLE=100 * float(r['NMLE_max']),
                                      ME=100 * int(r['motion_errors']) / int(r['N_clear']), SNS=float(r['SNS']), TW=float(r['TW1']))
        for m, k in [('Projection', 'projection'), ('Exact', 'eps=0'), ('Budgeted', 'eps=0.1')]:
            d[m] = dict(NROE=100 * F[k]['NROE'], NMLE=100 * F[k]['NMLE_max'], ME=me(Qs[k]), SNS=Qs[k]['SNS'], TW=Qs[k]['TW1'])
        d['nu'] = 100 * BUDGET[n]['budget_sweep'][0]['lower_mean']   # c0: bound at Exact Mode's numerical allowance eps0 (S16)
        d['nu_strict'] = 100 * BUDGET[n]['nu_tie_sensitivity']['0']   # nu*: strict exact-topology bound (Theorem 1)
        out[n] = d
    return out


def fig_compare_v2():
    V = compare_values(); fig = plt.figure(figsize=(7.0, 2.35))
    g = fig.add_gridspec(2, 3, width_ratios=[2.25, 1, 1], hspace=1.0, wspace=.3)
    ax = fig.add_subplot(g[:, 0]); x = np.arange(len(NAMES)); w = .26
    frac = {}
    for j, m in enumerate(['TMTM', 'ST-MTM', 'Exact']):
        xo = x + (j - 1) * w; tot = np.array([V[n][m]['NROE'] for n in NAMES])
        nu = np.array([V[n]['nu' if m == 'Exact' else 'nu_strict'] for n in NAMES])   # strict maps: nu*; Exact Mode: c0
        ex = np.clip(tot - nu, 0, None)
        ax.bar(xo, nu, w * .92, color=FORCED, lw=0)
        ax.bar(xo, ex, w * .92, bottom=nu, color=M[m]['c'], lw=0, alpha=1 if m != 'Exact' else .9)
        if m != 'Exact':
            frac[m] = 100 * ex / tot
            for xi, t, fr in zip(xo, tot, frac[m]): ax.text(xi, t + .5, f'{fr:.0f}', ha='center', fontsize=5.6, rotation=90, va='bottom')
    ax.axvline(4.5, color='#999', lw=.6); ax.text(4.4, 34, 'planar', ha='right', va='top', fontsize=5.6, color='#666'); ax.text(4.6, 34, 'volumetric', va='top', fontsize=5.6, color='#666')
    ax.set_xticks(x); ax.set_xticklabels([LABEL[n] for n in NAMES], fontsize=5.7)
    ax.set_ylabel('Order error NROE (%)', fontsize=6.3); ax.set_ylim(0, 36); ax.tick_params(labelsize=6, length=2)
    ax.yaxis.grid(True, color=GRID, lw=.5); ax.set_axisbelow(True)
    h = [Rectangle((0, 0), 1, 1, color=FORCED)] + [Rectangle((0, 0), 1, 1, color=M[m]['c']) for m in ('TMTM', 'ST-MTM', 'Exact')]
    ax.legend(h, [r'forced by hierarchy ($\nu^*$, Thm. 1; $c_0$ for $\varepsilon=0$)', 'avoidable: TMTM', 'avoidable: ST-MTM', r'avoidable: AnchorMTM $\varepsilon=0$'],
              fontsize=6, loc='upper center', ncol=2, handlelength=1, columnspacing=.8, bbox_to_anchor=(.5, -.1))
    ax.set_title('(a) Order error: forced by the hierarchy vs avoidable (labels: % avoidable)', pad=3, fontsize=6.3, fontweight='normal')
    print('avoidable % TMTM', np.round(frac['TMTM'], 1), 'ST-MTM', np.round(frac['ST-MTM'], 1))
    print('exact minus c0', {n: round(V[n]['Exact']['NROE'] - V[n]['nu'], 3) for n in NAMES})
    small = [('NMLE', 'Worst merge error (%)', g[0, 1]), ('ME', 'Motion error (%)', g[0, 2]),
             ('SNS', r'Distance stress SNS $\downarrow$', g[1, 1]), ('TW', r'Trustworthiness TW $\uparrow$', g[1, 2])]
    for j, (key, title, cell) in enumerate(small):
        title = '(' + 'bcde'[j] + ') ' + title
        ax = fig.add_subplot(cell); off = np.linspace(-.3, .3, 5)
        for k, m in enumerate(['TMTM', 'ST-MTM', 'Projection', 'Exact', 'Budgeted']):
            ax.plot(x + off[k], [V[n][m][key] for n in NAMES], **mstyle(m, 2.6))
        ax.axvline(4.5, color='#999', lw=.5); ax.set_xticks(x)
        ax.set_xticklabels([LABEL[n] for n in NAMES], fontsize=5.6, rotation=90)
        ax.set_title(title, fontsize=6.3, pad=2, fontweight='normal'); ax.tick_params(labelsize=5.8, length=2)
        ax.yaxis.grid(True, color=GRID, lw=.5); ax.set_axisbelow(True)
    hs = [Line2D([], [], **mstyle(m, 3.2)) for m in ['TMTM', 'ST-MTM', 'Projection', 'Exact', 'Budgeted']]
    fig.legend(hs, [MLAB[m] for m in ['TMTM', 'ST-MTM', 'Projection', 'Exact', 'Budgeted']], ncol=5, fontsize=6.2,
               loc='lower center', bbox_to_anchor=(.68, -.2), handlelength=1, columnspacing=.9)
    save(fig, 'draft_compare_v2')


# ------------------------------------------------------------------ frontier with existing maps
def baseline_displacement(n):
    """E_inf and E_pool of the TMTM- and ST-MTM-objective layouts in the same interval model (unified20261025)."""
    if n not in UNIFIED: return None
    d = load(CODE / f'unified20261025/{UNIFIED[n]}.json'); L = d['parameters']['canvas']
    assert d['frames'] == FRONT[n]['frames'] and abs(L - FRONT[n]['canvas']) < 1e-9
    out = {}
    for key, m in [('topology_time', 'TMTM'), ('topology_geometry', 'ST-MTM')]:
        e = np.concatenate([np.abs(np.asarray(r['x'], float) - np.asarray(r['reference'], float)) / L for r in d['regimes'][key]['rows']])
        out[m] = dict(E_inf=100 * e.max(), E_pool=100 * e.mean())
    return out


def fig_frontier_v2():
    fig, axes = plt.subplots(2, 4, figsize=(7.0, 2.45)); axes = axes.ravel()
    keys = [k for k in FRONT['Ring']['methods'] if k.startswith('eps=')]; cm = plt.get_cmap('Blues')
    for ax, n in zip(axes, NAMES):
        F = FRONT[n]['methods']; ms = [F[k] for k in keys]; P = F['projection']
        x = [100 * m['NMLE_max'] for m in ms]; yw = [100 * m['E_inf'] for m in ms]; yp = [100 * m['E_pool'] for m in ms]
        ax.plot(x, yp, '--', lw=.7, color=M['Exact']['c'], alpha=.6)
        ax.plot(x, yw, '-', lw=1.1, color=M['Exact']['c'])
        for i, (xi, yi) in enumerate(zip(x, yw)):
            ax.plot(xi, yi, 'o', ms=3.4, mfc=cm(.95 - .65 * i / (len(keys) - 1)), mec='white', mew=.4, zorder=3)
            ax.plot(xi, yp[i], 'o', ms=2, color=M['Exact']['c'], alpha=.6)
        for k, xi, yi in zip(keys, x, yw):
            if k in ('eps=0', 'eps=0.02', 'eps=0.1'): ax.annotate('%g' % (100 * float(k[4:])), (xi, yi), xytext=(2, 2.5), textcoords='offset points', fontsize=5.8)
        ax.plot([x[-1], 100 * P['NMLE_max']], [yw[-1], 100 * P['E_inf']], ':', lw=.8, color=M['Exact']['c'])
        ax.plot(100 * P['NMLE_max'], 100 * P['E_inf'], **mstyle('Projection', 4))
        top = max(yw + [100 * P['E_inf']]) * 1.35
        B = baseline_displacement(n)
        if B:
            txt = 'same model, $\\varepsilon=0$:\n' + '\n'.join(f"{m}-style: {B[m]['E_inf']:.0f}% / {B[m]['E_pool']:.0f}%" for m in ('TMTM', 'ST-MTM'))
            ax.text(.97, .97, txt, transform=ax.transAxes, ha='right', va='top', fontsize=5.5, linespacing=1.15,
                    bbox=dict(boxstyle='round,pad=.25', fc='#F4F5F7', ec='none'))
            ax.annotate('', (0, top), (0, top * .86), arrowprops=dict(arrowstyle='-|>', lw=.8, color=M['TMTM']['c']), annotation_clip=False)
            print('frontier baseline', n, {m: {k: round(v, 2) for k, v in B[m].items()} for m in B})
        ax.set_ylim(0, top); ax.set_title(LABEL[n], pad=2, fontweight='normal')
        ax.yaxis.grid(True, color=GRID, lw=.5); ax.set_axisbelow(True); ax.tick_params(labelsize=6, length=2)
    for ax in axes[4:7]: ax.set_xlabel('Worst merge error NMLE (%)', fontsize=6.3)
    for ax in (axes[0], axes[4]): ax.set_ylabel('Displacement (%)', fontsize=6.3)
    axes[7].axis('off')
    hs = [Line2D([], [], color=M['Exact']['c'], lw=1.1, marker='o', ms=3), Line2D([], [], color=M['Exact']['c'], lw=.7, ls='--', alpha=.6),
          Line2D([], [], **mstyle('Projection', 4))]
    axes[7].legend(hs, [r'AnchorMTM worst $E_\infty$', r'AnchorMTM mean $E_{pool}$', r'projection ($\varepsilon=\infty$)'],
                   loc='upper center', fontsize=6, handlelength=1.6, bbox_to_anchor=(.5, 1.12))
    axes[7].text(.5, .0, 'shade, labels: $\\varepsilon$ (%), dark = 0\ngrey box: TMTM-/ST-MTM-style\nobjectives, same model,\nworst / mean; arrow: off scale',
                 transform=axes[7].transAxes, ha='center', va='bottom', fontsize=5.6, linespacing=1.2)
    fig.subplots_adjust(hspace=.48, wspace=.3)
    save(fig, 'draft_frontier_v2')


# ------------------------------------------------------------------ rendered maps side by side
def fig_maps_v2():
    S = load(RES / 'maps20261030/storms_case.json')
    cols = [('topology_time', 'TMTM', 'TMTM objective'), ('topology_geometry', 'ST-MTM', 'ST-MTM objective'),
            ('ours_0', 'Exact', r'AnchorMTM, $\varepsilon=0$'), ('ours_0.1', 'Budgeted', r'AnchorMTM, $\varepsilon=10\%$')]
    rows = [('Storms', 'era5', 'RdBu_r', 'MSLP (hPa)', 'reference axis\n(west → east)'), ('OLR', 'olr', 'RdBu_r', r'OLR (W m$^{-2}$)', 'reference axis')]
    fig = plt.figure(figsize=(7.0, 3.3)); g = fig.add_gridspec(2, 5, width_ratios=[1, 1, 1, 1, .04], hspace=.32, wspace=.08)
    for r, (n, key, cmap, clab, ylab) in enumerate(rows):
        Mp = dict(np.load(RES / f'maps20261030/maps_{key}.npz')); qs = load(RES / f'maps20261030/q_{key}.json')
        vmin = min(np.nanmin(Mp[k]) for k, *_ in cols); vmax = max(np.nanmax(Mp[k]) for k, *_ in cols)
        B = baseline_displacement(n); F = FRONT[n]['methods']
        stat = {'TMTM': B['TMTM'], 'ST-MTM': B['ST-MTM'],
                'Exact': dict(E_pool=100 * F['eps=0']['E_pool'], E_inf=100 * F['eps=0']['E_inf']),
                'Budgeted': dict(E_pool=100 * F['eps=0.1']['E_pool'], E_inf=100 * F['eps=0.1']['E_inf'])}
        for c, (k, m, title) in enumerate(cols):
            ax = fig.add_subplot(g[r, c]); T = Mp[k].shape[1]
            im = ax.imshow(Mp[k], origin='lower', aspect='auto', interpolation='nearest', cmap=cmap, vmin=vmin, vmax=vmax,
                           extent=[-.5, T - .5, 0, 1], rasterized=True)
            for t, q in enumerate(qs): ax.plot([t] * len(q), q, 'o', ms=1.25, mfc='k', mec='white', mew=.25)
            if m == 'Budgeted' and n == 'Storms':
                for t, mk in enumerate(S['marks_10']):
                    if mk: ax.plot([t] * len(mk), mk, '_', ms=3.2, mew=1.1, color='#FFD000')
            ax.text(.02, .02, f"mean {stat[m]['E_pool']:.1f}% / worst {stat[m]['E_inf']:.0f}%", transform=ax.transAxes, fontsize=5.1,
                    va='bottom', bbox=dict(boxstyle='round,pad=.15', fc='white', ec='none', alpha=.85))
            ax.set_xticks([0, T - 1]); ax.set_yticks([0, .5, 1] if c == 0 else []); ax.tick_params(labelsize=5.4, length=2)
            for s in ax.spines.values(): s.set_visible(True); s.set_linewidth(.4)
            if r == 0:
                ax.set_title(title, pad=4, color=M[m]['c'] if m != 'TMTM' else '#555', fontsize=6.6)
                ax.add_patch(Rectangle((0, 1.015), 1, .025, transform=ax.transAxes, color=M[m]['c'], clip_on=False, lw=0))
            if c == 0: ax.set_ylabel(f'{LABEL[n]}\n{ylab}', fontsize=6.1)
            if r == 1: ax.set_xlabel('Time step', fontsize=6, labelpad=1)
        cb = fig.colorbar(im, cax=fig.add_subplot(g[r, 4])); cb.ax.tick_params(labelsize=5.2, length=2); cb.set_label(clab, fontsize=5.8)
        print('maps', n, {m: {k: round(v, 2) for k, v in s.items()} for m, s in stat.items()})
    fig.text(.5, -.01, r'black dots: reference positions $q_i$;  yellow ticks (Storms, $\varepsilon=10\%$): barriers whose merge level changed;  '
             'labels: mean $E_{pool}$ / worst $E_\\infty$ displacement', ha='center', fontsize=5.6)
    save(fig, 'draft_maps_v2')


# ------------------------------------------------------------------ controlled conflict with setup inset
def fig_controlled_v2():
    base = CODE / 'controlled_conflict20261030'
    ov = [r for r in csv.DictReader((base / 'overlap.csv').open())]; bu = [r for r in csv.DictReader((base / 'budget.csv').open())]
    fig, axes = plt.subplots(1, 2, figsize=(3.45, 1.75), gridspec_kw=dict(wspace=.42))
    ax = axes[0]; sel = [r for r in ov if abs(float(r['width']) - .06) < 1e-9]
    d = np.array([float(r['overlap']) for r in sel]); f = lambda k: 100 * np.array([float(r[k]) for r in sel])
    ax.plot(100 * d, f('nu'), '--', color='#D55E00', lw=1, label=r'point bound $\nu^*$')
    ax.plot(100 * d, f('exact_tau'), '-', color=M['Exact']['c'], lw=1.1, label='interval optimum (24 orders)')
    ax.plot(100 * d[::3], f('width_lower')[::3], 'o', ms=2.6, mfc='white', mec=M['Exact']['c'], mew=.7, label='width bound (Thm. 2)')
    ax.set_xlabel('signed overlap d (%)', fontsize=6); ax.set_ylabel('displacement (%)', fontsize=6)
    ax.legend(fontsize=5.6, loc='upper left', handlelength=1.4); ax.tick_params(labelsize=5.8, length=2)
    ax.yaxis.grid(True, color=GRID, lw=.5); ax.set_axisbelow(True); ax.set_title('(a) Overlap forces displacement', fontsize=6.3, pad=2)
    ins = ax.inset_axes([.6, .03, .4, .3]); ins.set_xlim(0, 1); ins.set_ylim(-.1, 1.15); ins.axis('off')
    for k, xi in zip('ABCD', [.08, .36, .64, .92]):
        ins.plot([xi, xi], [0, .45], color=LEAF[k], lw=1.2); ins.text(xi, -.08, k, fontsize=5.6, ha='center', va='top', color=LEAF[k])
    ins.plot([.08, .36], [.45, .45], 'k', lw=.6); ins.plot([.64, .92], [.45, .45], 'k', lw=.6)
    ins.plot([.22, .22, .78, .78], [.45, .9, .9, .45], 'k', lw=.6); ins.text(.5, -.42, 'q = (.2, .5, .5−d, .8−d)', fontsize=5.2, ha='center')
    ax = axes[1]; levels = sorted({float(r['inner_level']) for r in bu}); cm = plt.get_cmap('viridis')
    for i, lv in enumerate(levels):
        sel = [r for r in bu if float(r['inner_level']) == lv]; e = 100 * np.array([float(r['epsilon']) for r in sel])
        t = 100 * np.array([float(r['tau']) for r in sel]); h = 100 * float(sel[0]['parent_gap']); c = cm(.15 + .7 * i / (len(levels) - 1))
        ax.step(e, t, where='post', color=c, lw=1); ax.text(h / 2 + .6, 7 + 1.6 * i, f'h = {h:.0f}%', fontsize=5.6, color=c, rotation=90, va='center')
    ax.set_xlabel(r'merge budget $\varepsilon$ (%)', fontsize=6); ax.set_ylabel('displacement (%)', fontsize=6)
    ax.tick_params(labelsize=5.8, length=2); ax.set_title(r'(b) Released at $\varepsilon=h/2$ (Thm. 3)', fontsize=6.3, pad=2)
    ax.yaxis.grid(True, color=GRID, lw=.5); ax.set_axisbelow(True)
    save(fig, 'draft_controlled_v2')


if __name__ == '__main__':
    fig_concept(); fig_design_space(); fig_compare_v2(); fig_frontier_v2(); fig_maps_v2(); fig_controlled_v2()


# ------------------------------------------------------------------ page plan (current v5 vs proposed)
def fig_page_plan():
    cur = {1: [('Teaser', 'f', .42)], 3: [('Fig 2 leaf corresp.', 'c', .3)], 4: [('Alg. 1', 'c', .45)], 6: [('Table 1 instances', 'c', .16)],
           7: [('Fig 3 compare', 'f', .3), ('Table 2 data', 'c', .17), ('Fig 4 controlled', 'c', .2)], 8: [('Fig 5 frontier', 'f', .43)],
           9: [('Fig 6 direction', 'c', .45)]}
    new = {1: [('Teaser (+ W–E axis)', 'f', .42)], 2: [('Design space', 'c', .22)], 3: [('Concept (a–d)', 'f', .28)],
           4: [('Alg. 1 (5 steps)', 'c', .3)], 6: [('Maps side by side', 'f', .45)], 7: [('Compare v2', 'f', .33), ('Table data', 'c', .17)],
           8: [('Frontier v2', 'f', .43), ('Controlled v2', 'c', .2)], 9: []}
    moved = ['Fig 2 leaf corresp.', 'Fig 6 direction', 'proof sketches', 'Table 1 (into design-space caption)']
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 2.9), gridspec_kw=dict(hspace=.35))
    for ax, plan, title in [(axes[0], cur, 'Current draft v5'), (axes[1], new, 'Proposed layout')]:
        ax.set_xlim(0, 9 * 1.1); ax.set_ylim(0, 1.3); ax.axis('off'); ax.set_title(title, loc='left', fontsize=7)
        for p in range(1, 10):
            x0 = (p - 1) * 1.1; ax.add_patch(Rectangle((x0, 0), 1, 1.29, fill=False, lw=.6, ec='#888'))
            ax.text(x0 + .5, -.08, str(p), ha='center', va='top', fontsize=6)
            ytop = 1.27; ycol = None
            for name, kind, h in plan.get(p, []):
                w = .96 if kind == 'f' else .46; xx = x0 + .02 if kind == 'f' else x0 + .52
                if kind == 'c':
                    ycol = ytop if ycol is None else ycol
                    ax.add_patch(Rectangle((xx, ycol - h), w, h, color='#BFC6CC' if not (title.startswith('Proposed') and 'v2' in name or 'Design' in name) else M['Budgeted']['c'], alpha=.55, lw=0))
                    ax.text(xx + w / 2, ycol - h / 2, name.replace(' ', '\n', 1), ha='center', va='center', fontsize=4.2); ycol -= h + .02
                    continue
                new_fig = title.startswith('Proposed') and any(t in name for t in ('Design', 'Concept', 'Maps', 'v2', 'W–E'))
                ax.add_patch(Rectangle((xx, ytop - h), w, h, color=M['Budgeted']['c'] if new_fig else '#BFC6CC', alpha=.55, lw=0))
                ax.text(xx + w / 2, ytop - h / 2, name, ha='center', va='center', fontsize=4.6)
                ytop -= h + .02; ycol = None if ycol is None else ycol
    fig.text(.01, -.02, 'Moved to the supplement: ' + '; '.join(moved) + '.   Green: new or redrawn.   Heights are rough estimates.', fontsize=5.6)
    save(fig, 'draft_page_plan')


if __name__ == '__main__':
    import sys
    for name in (sys.argv[1:] or ['fig_page_plan']): globals()[name]()
