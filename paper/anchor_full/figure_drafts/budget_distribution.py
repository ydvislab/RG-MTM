"""Per-frame distributions of AnchorMTM over the merge budget epsilon (v20 main figure and supplementary figures).

Inputs (saved results, read only; no algorithm is rerun):
  ../../pvis2027/budget_tradeoff_20261105/planar_per_frame/<Storms|Wildfires|Ring>/epsilon_<e>.csv
      complete-sequence runs with the main-table configuration; epsilon_0 is the Exact run of Table 1 and the selected
      epsilon (Ring 1%, Wildfires 5%, Storms 10%) is the Balanced run (checked below, value by value).
  ../../pvis2027/budget_tradeoff_20261105/volume_per_frame_audit.csv   volumetric default-weight sweep (not Table 3 settings)
  ../../pvis2027/experiments_ratio_p_20261104/balanced_selection.csv   first-quarter validation of the Balanced budget

Per frame t: NPE_t = max_i |x_i - q_i| / L_world (rendered anchors), NMLE_t = attained fixed-leaf merge error / scalar range,
SNS_t = scale-normalized stress. Table NPE is the mean of NPE_t over frames.

Run:  python budget_distribution.py [v21]  ->  ../../pvis2027/latex_v21/figures/budget_*.pdf (+ svg, png previews next to this file)
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
PV = HERE.parents[1] / 'pvis2027'
SWEEP = PV / 'budget_tradeoff_20261105'
RATIO = PV / 'experiments_ratio_p_20261104'
OUT = PV / 'latex_v21/figures'
PREV = HERE / 'preview_v20'
OUT.mkdir(parents=True, exist_ok=True); PREV.mkdir(exist_ok=True)

for f in ['Times New Roman.ttf', 'Times New Roman Bold.ttf', 'Times New Roman Italic.ttf']:
    p = Path('/System/Library/Fonts/Supplemental') / f
    if p.exists():
        font_manager.fontManager.addfont(str(p))
plt.rcParams.update({'font.family': 'Times New Roman', 'mathtext.fontset': 'stix', 'font.size': 7,
                     'axes.titlesize': 7.5, 'axes.labelsize': 7, 'xtick.labelsize': 6.2, 'ytick.labelsize': 6.2,
                     'axes.linewidth': .55, 'xtick.major.size': 2, 'ytick.major.size': 2, 'xtick.major.width': .5,
                     'ytick.major.width': .5, 'pdf.fonttype': 42, 'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False})
BLUE, LIGHT, ORANGE, LORANGE = '#0072B2', '#cfe3f1', '#D55E00', '#f6d2bd'
DARK, LDARK = '#3d4a55', '#dfe3e6'
GREY, GRID, DOT = '#6b7378', '#e3e7ea', '#8a9399'
SELECTED = {'Ring': 1, 'Wildfires': 5, 'Storms': 10}            # Balanced budgets of the main comparison table (percent)
FRAMES = {'Ring': 40, 'Wildfires': 32, 'Storms': 744}
PLANAR = ['Storms', 'Wildfires', 'Ring']


def load_planar(name):
    runs = {}
    for f in (SWEEP / 'planar_per_frame' / name).glob('epsilon_*.csv'):
        e = round(100 * float(f.stem.split('_')[1]), 6)
        d = pd.read_csv(f)
        assert len(d) == FRAMES[name] and d.rendered_budget_ok.all() and d.continuous_budget_ok.all()
        assert (d.topology_max <= e / 100 + 1e-7 + 1e-12).all(), (name, e)
        runs[e] = d
    # the sweep endpoints are exactly the Table 1 runs
    for mode, e in [('Exact', 0), ('Balanced', SELECTED[name])]:
        t = pd.read_csv(RATIO / 'results' / name / mode / 'per_frame.csv')
        for c in ['NPE', 'SNS', 'topology_max']:
            assert np.allclose(t[c].fillna(-1), runs[e][c].fillna(-1), rtol=0, atol=1e-15), (name, mode, c)
        s = json.loads((RATIO / 'results' / name / mode / 'summary.json').read_text())
        assert abs(runs[e].NPE.mean() - s['NPE']) < 1e-12
    return dict(sorted(runs.items()))


def sqrt_axis(ax):
    ax.set_yscale('function', functions=(lambda v: np.sqrt(np.maximum(v, 0)), lambda v: np.square(v)))


def boxes(ax, xs, samples, colors, width=.62, outliers=True, lw=.5):
    """Box: quartiles; whiskers: 5th-95th percentiles; dots: remaining frames; white diamond: mean."""
    for x, v, (edge, fill) in zip(xs, samples, colors):
        v = np.asarray(v, float); v = v[np.isfinite(v)]
        p5, q1, med, q3, p95 = np.percentile(v, [5, 25, 50, 75, 95])
        ax.add_patch(plt.Rectangle((x - width / 2, q1), width, max(q3 - q1, 1e-9), fc=fill, ec=edge, lw=lw, zorder=3))
        ax.plot([x - width / 2, x + width / 2], [med, med], color=edge, lw=1.0, zorder=4, solid_capstyle='butt')
        ax.plot([x, x], [p95, q3], color=edge, lw=lw, zorder=2); ax.plot([x, x], [p5, q1], color=edge, lw=lw, zorder=2)
        for y in (p5, p95):
            ax.plot([x - width / 4, x + width / 4], [y, y], color=edge, lw=lw, zorder=2)
        if outliers:
            o = v[(v > p95) | (v < p5)]
            if len(o):
                jit = (np.random.default_rng(int(1000 * x) + len(v)).random(len(o)) - .5) * width * .5
                ax.scatter(x + jit, o, s=1.3, color=edge, alpha=.55, lw=0, zorder=2)
        ax.scatter([x], [v.mean()], marker='D', s=7, fc='white', ec=edge, lw=.55, zorder=5)


def strip(ax, xs, samples, colors, width=.62, s=1.4, alpha=.35):
    for x, v, (edge, _) in zip(xs, samples, colors):
        v = np.asarray(v, float)
        jit = (np.random.default_rng(7 + int(1000 * x)).random(len(v)) - .5) * width
        ax.scatter(x + jit, v, s=s, color=edge, alpha=alpha, lw=0, zorder=3)


def style(ax, ygrid=True):
    if ygrid:
        ax.yaxis.grid(True, color=GRID, lw=.4); ax.set_axisbelow(True)
    ax.tick_params(pad=1.5)


# ---------------------------------------------------------------- main figure (one column, three planar sequences)
def main_figure():
    eps = list(range(0, 11))
    fig, axes = plt.subplots(2, 3, figsize=(3.45, 2.5), gridspec_kw=dict(height_ratios=[1.45, 1]))
    yt = {'Storms': [0, 1, 5, 10, 20, 40], 'Wildfires': [0, .5, 1, 2, 4], 'Ring': [0, 1, 2, 5, 10]}
    stats = {}
    for c, name in enumerate(PLANAR):
        runs = load_planar(name)
        col = [(ORANGE, LORANGE) if e == SELECTED[name] else (DARK, LDARK) if e == 0 else (BLUE, LIGHT) for e in eps]
        ax = axes[0, c]; sqrt_axis(ax)
        boxes(ax, eps, [100 * runs[e].NPE for e in eps], col)
        top = max(100 * runs[e].NPE.max() for e in eps)
        ax.set_ylim(0, top * 1.08); ax.set_yticks([t for t in yt[name] if t <= top * 1.08])
        ax.set_yticklabels([f'{t:g}' for t in ax.get_yticks()])
        ax.set_xlim(-.7, 10.7); ax.set_xticks([0, 5, 10]); ax.set_xticklabels([])
        ax.set_title(f'{name} ({FRAMES[name]} frames)', pad=2.5); style(ax)
        ax2 = axes[1, c]
        strip(ax2, eps, [100 * runs[e].topology_max for e in eps], col)
        ax2.plot([-.5, 10.5], [-.5, 10.5], color=GREY, ls=(0, (2.5, 1.5)), lw=.6, zorder=1)
        ax2.set_xlim(-.7, 10.7); ax2.set_ylim(-.4, 10.6); ax2.set_xticks([0, 2, 4, 6, 8, 10]); ax2.set_yticks([0, 5, 10])
        s = SELECTED[name]; used = int((runs[s].topology_max > 1e-9).sum())
        ax2.text(.03, .97, f'{used}/{FRAMES[name]} frames > 0\nat $\\varepsilon$ = {s}%', transform=ax2.transAxes,
                 ha='left', va='top', fontsize=5.6, color=ORANGE, linespacing=1.1)
        style(ax2)
        q = lambda e, p: float(np.percentile(100 * runs[e].NPE, p))
        stats[name] = dict(median=(q(0, 50), q(10, 50)), p90=(q(0, 90), q(10, 90)), max=(100 * runs[0].NPE.max(), 100 * runs[10].NPE.max()),
                           mean=(100 * runs[0].NPE.mean(), 100 * runs[s].NPE.mean()),
                           used={e: int((runs[e].topology_max > 1e-9).sum()) for e in eps})
    axes[0, 0].set_ylabel('Worst displacement\nper frame (%)', labelpad=2)
    axes[1, 0].set_ylabel('Merge error\nper frame (%)', labelpad=5)
    axes[1, 1].set_xlabel(r'Merge budget $\varepsilon$ (%)', labelpad=1.5)
    h = [Patch(fc=LDARK, ec=DARK, lw=.5, label=r'Exact ($\varepsilon=0$)'), Patch(fc=LIGHT, ec=BLUE, lw=.5, label=r'$\varepsilon>0$'),
         Patch(fc=LORANGE, ec=ORANGE, lw=.5, label=r'Balanced (selected $\varepsilon$)'),
         Line2D([], [], ls='none', marker='D', ms=2.6, mfc='white', mec=GREY, mew=.55, label='mean'),
         Line2D([], [], color=GREY, ls=(0, (2.5, 1.5)), lw=.6, label=r'$y=\varepsilon$')]
    fig.legend(handles=h, ncol=5, loc='lower center', bbox_to_anchor=(.54, -.02), frameon=False, fontsize=5.9,
               handlelength=1.1, columnspacing=.75, handletextpad=.35)
    fig.subplots_adjust(left=.13, right=.99, top=.93, bottom=.17, hspace=.22, wspace=.3)
    for ext in ['pdf']:
        fig.savefig(OUT / f'budget_distribution.{ext}', bbox_inches='tight', pad_inches=.015)
    fig.savefig(PREV / 'budget_distribution.png', dpi=300, bbox_inches='tight', pad_inches=.015)
    plt.close(fig)
    return stats


def cat_positions(eps):
    """Categorical positions with a small gap where the step leaves the 1% grid (marks unequal spacing)."""
    pos, x = [], 0.
    for i, e in enumerate(eps):
        if i and e > 10 and eps[i - 1] <= 10:
            x += .7
        pos.append(x); x += 1
    return np.array(pos)


def eps_labels(ax, pos, eps, every=None, rot=0, fs=5.4):
    ax.set_xticks(pos); ax.set_xticklabels([f'{e:g}' for e in eps], fontsize=fs, rotation=rot)
    ax.set_xlim(pos[0] - .7, pos[-1] + .7)


# ---------------------------------------------------------------- S1: extended sweep, three metrics per frame
def supp_extended():
    data = {n: load_planar(n) for n in PLANAR}
    widths = [len(data[n]) + .7 for n in PLANAR]
    fig, axes = plt.subplots(3, 3, figsize=(7.0, 4.15), gridspec_kw=dict(width_ratios=widths, height_ratios=[1.3, 1, 1.05]))
    for c, name in enumerate(PLANAR):
        runs = data[name]; eps = list(runs); pos = cat_positions(eps)
        col = [(ORANGE, LORANGE) if e == SELECTED[name] else (DARK, LDARK) if e == 0 else (BLUE, LIGHT) for e in eps]
        ax = axes[0, c]; sqrt_axis(ax)
        boxes(ax, pos, [100 * runs[e].NPE for e in eps], col, width=.64)
        top = max(100 * runs[e].NPE.max() for e in eps); ax.set_ylim(0, top * 1.08)
        tk = {'Storms': [0, 1, 5, 10, 20, 40], 'Wildfires': [0, .5, 1, 2, 4], 'Ring': [0, 1, 2, 5, 10]}[name]
        ax.set_yticks([t for t in tk if t <= top * 1.08]); ax.set_yticklabels([f'{t:g}' for t in ax.get_yticks()])
        eps_labels(ax, pos, eps); ax.set_xticklabels([]); ax.set_title(f'{name} ({FRAMES[name]} frames)', pad=2.5); style(ax)
        ax = axes[1, c]
        boxes(ax, pos, [runs[e].SNS.dropna() for e in eps], col, width=.64)
        eps_labels(ax, pos, eps); ax.set_xticklabels([]); style(ax); ax.set_ylim(bottom=0)
        ax = axes[2, c]
        strip(ax, pos, [100 * runs[e].topology_max for e in eps], col, width=.64, s=1.2, alpha=.35)
        ax.scatter(pos, eps, marker='_', s=30, color=GREY, lw=.9, zorder=4)
        eps_labels(ax, pos, eps, rot=90 if len(eps) > 15 else 0); style(ax); ax.set_ylim(-max(eps) * .03, max(eps) * 1.05)
    axes[0, 0].set_ylabel('Worst displacement\nper frame (%)', labelpad=2)
    axes[1, 0].set_ylabel('SNS per frame', labelpad=2)
    axes[2, 0].set_ylabel('Merge error\nper frame (%)', labelpad=2)
    axes[2, 1].set_xlabel(r'Merge budget $\varepsilon$ (%)', labelpad=2)
    h = [Patch(fc=LDARK, ec=DARK, lw=.5, label=r'Exact ($\varepsilon=0$)'), Patch(fc=LIGHT, ec=BLUE, lw=.5, label=r'$\varepsilon>0$'),
         Patch(fc=LORANGE, ec=ORANGE, lw=.5, label=r'Balanced (selected $\varepsilon$)'),
         Line2D([], [], ls='none', marker='D', ms=2.6, mfc='white', mec=GREY, mew=.55, label='mean'),
         Line2D([], [], ls='none', marker='_', ms=6, mec=GREY, mew=.9, label=r'budget $\varepsilon$')]
    fig.legend(handles=h, ncol=5, loc='lower center', bbox_to_anchor=(.5, -.015), frameon=False, fontsize=6.5, handlelength=1.3, columnspacing=1.4)
    fig.subplots_adjust(left=.075, right=.995, top=.95, bottom=.13, hspace=.16, wspace=.13)
    fig.savefig(OUT / 'budget_supp_extended.pdf', bbox_inches='tight', pad_inches=.015)
    fig.savefig(PREV / 'budget_supp_extended.png', dpi=250, bbox_inches='tight', pad_inches=.015)
    plt.close(fig)
    out = {}
    for n in PLANAR:
        r = data[n]; e = list(r)
        out[n] = {f'{k:g}': (round(100 * r[k].NPE.median(), 2), round(100 * r[k].NPE.quantile(.9), 2), round(100 * r[k].NPE.max(), 2),
                             round(float(r[k].SNS.mean()), 4), int((r[k].topology_max > 1e-9).sum())) for k in e}
    return out


# ---------------------------------------------------------------- S2: frame x budget matrices
def supp_matrix():
    from matplotlib.colors import PowerNorm
    data = {n: load_planar(n) for n in PLANAR}
    fig = plt.figure(figsize=(7.0, 3.55))
    g = fig.add_gridspec(3, 4, height_ratios=[1, 1, 1.25], width_ratios=[1, 1, 1, 1], hspace=.55, wspace=.32)
    cm_d = matplotlib.colormaps['Blues']; cm_m = matplotlib.colormaps['Oranges']
    def matrix(ax, runs, key, norm, cmap, frames_label=True):
        eps = list(runs); M = np.array([100 * runs[e][key].to_numpy() for e in eps])
        im = ax.imshow(M, aspect='auto', interpolation='nearest', cmap=cmap, norm=norm)
        ax.set_yticks(range(len(eps))); ax.set_yticklabels([f'{e:g}' for e in eps], fontsize=4.6)
        ax.tick_params(axis='y', length=1.2, pad=1); ax.tick_params(axis='x', labelsize=5.4, pad=1.2)
        for s in ax.spines.values(): s.set_visible(True); s.set_linewidth(.4)
        return im
    st = data['Storms']
    nd = PowerNorm(.5, vmin=0, vmax=45); nm = PowerNorm(.5, vmin=0, vmax=30)
    ax = fig.add_subplot(g[0, :]); im_d = matrix(ax, st, 'NPE', nd, cm_d)
    ax.set_title('Storms: worst displacement per frame (%)', pad=2.5, loc='left'); ax.set_ylabel(r'$\varepsilon$ (%)', labelpad=1)
    ax = fig.add_subplot(g[1, :]); im_m = matrix(ax, st, 'topology_max', nm, cm_m)
    ax.set_title('Storms: merge error per frame (%)', pad=2.5, loc='left'); ax.set_ylabel(r'$\varepsilon$ (%)', labelpad=1)
    ax.set_xlabel('Frame (hourly, December 1999)', labelpad=1.5)
    for j, (n, key, norm, cmap, lab) in enumerate([('Wildfires', 'NPE', nd, cm_d, 'displacement'), ('Wildfires', 'topology_max', nm, cm_m, 'merge error'),
                                                   ('Ring', 'NPE', nd, cm_d, 'displacement'), ('Ring', 'topology_max', nm, cm_m, 'merge error')]):
        ax = fig.add_subplot(g[2, j]); im = matrix(ax, data[n], key, norm, cmap)
        ax.set_title(f'{n}: {lab}', pad=2.5, loc='left'); ax.set_xlabel('Frame', labelpad=1.5)
        if j == 0: ax.set_ylabel(r'$\varepsilon$ (%)', labelpad=1)
        if j == 3: im_r = im
    for im, rect, lab in [(im_d, [.915, .70, .008, .2], 'displacement (%)'), (im_m, [.915, .41, .008, .2], 'merge error (%)')]:
        cax = fig.add_axes(rect); cb = fig.colorbar(im, cax=cax, extend='max' if 'merge' in lab else 'neither'); cb.ax.tick_params(labelsize=5, length=1.5, pad=1); cb.set_label(lab, fontsize=5.6, labelpad=2)
        cb.outline.set_linewidth(.4)
    fig.subplots_adjust(left=.06, right=.905, top=.95, bottom=.08)
    fig.savefig(OUT / 'budget_supp_matrix.pdf', bbox_inches='tight', pad_inches=.015)
    fig.savefig(PREV / 'budget_supp_matrix.png', dpi=250, bbox_inches='tight', pad_inches=.015)
    plt.close(fig)


# ---------------------------------------------------------------- S3: volumetric default-weight sweep
def supp_volume():
    d = pd.read_csv(SWEEP / 'volume_per_frame_audit.csv')
    assert d.rendered_budget_ok.all()
    fig, axes = plt.subplots(2, 2, figsize=(3.45, 2.45), gridspec_kw=dict(height_ratios=[1.35, 1]))
    out = {}
    for c, name in enumerate(['Tangaroa', 'Cylinder']):
        g = d[d.dataset == name]; eps = sorted(g.epsilon.unique()); pos = np.arange(len(eps))
        col = [(DARK, LDARK) if e == 0 else (BLUE, LIGHT) for e in eps]
        ax = axes[0, c]; sqrt_axis(ax)
        boxes(ax, pos, [100 * g[g.epsilon == e].E_max for e in eps], col, width=.6)
        top = 100 * g.E_max.max(); ax.set_ylim(0, top * 1.08)
        ax.set_yticks([t for t in [0, 1, 2, 5, 10, 20] if t <= top * 1.08]); ax.set_yticklabels([f'{t:g}' for t in ax.get_yticks()])
        ax.set_xticks(pos); ax.set_xticklabels([]); ax.set_xlim(-.6, len(eps) - .4)
        ax.set_title(f'{name} (3D, {g.frame.nunique()} frames)', pad=2.5); style(ax)
        ax = axes[1, c]
        strip(ax, pos, [100 * g[g.epsilon == e].NMLE_max for e in eps], col, width=.6, s=1.4, alpha=.4)
        ax.scatter(pos, [100 * e for e in eps], marker='_', s=40, color=GREY, lw=.9, zorder=4)
        ax.set_xticks(pos); ax.set_xticklabels([f'{100 * e:g}' for e in eps]); ax.set_xlim(-.6, len(eps) - .4); ax.set_ylim(-.8, 21)
        style(ax)
        out[name] = {f'{100 * e:g}': (round(100 * g[g.epsilon == e].E_max.median(), 2), round(100 * g[g.epsilon == e].E_max.max(), 2),
                                      int((g[g.epsilon == e].NMLE_max > 1e-6).sum())) for e in eps}
    axes[0, 0].set_ylabel('Worst displacement\nper frame (%)', labelpad=2)
    axes[1, 0].set_ylabel('Merge error\nper frame (%)', labelpad=5)
    fig.supxlabel(r'Merge budget $\varepsilon$ (%)', y=.0, fontsize=7)
    fig.subplots_adjust(left=.14, right=.99, top=.93, bottom=.15, hspace=.2, wspace=.3)
    fig.savefig(OUT / 'budget_supp_volume.pdf', bbox_inches='tight', pad_inches=.015)
    fig.savefig(PREV / 'budget_supp_volume.png', dpi=300, bbox_inches='tight', pad_inches=.015)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- S4: Balanced selection on the first quarter
def supp_selection():
    d = pd.read_csv(RATIO / 'balanced_selection.csv')
    fig, axes = plt.subplots(2, 4, figsize=(7.0, 1.95), sharex=True, gridspec_kw=dict(height_ratios=[1, 1]))
    for c, name in enumerate(['Gaussian', 'Ring', 'Wildfires', 'Storms']):
        g = d[d.Dataset == name].sort_values('epsilon'); e = 100 * g.epsilon.to_numpy()
        sel = g[g.selected.astype(str) == 'True']; es = 100 * float(sel.epsilon.iloc[0])
        ax = axes[0, c]
        ax.plot(e, 100 * g.NPE, color=BLUE, lw=.9, marker='o', ms=2.2, label='NPE (%)')
        ax2 = ax.twinx(); ax2.plot(e, g.SNS, color=GREY, lw=.9, ls='--', marker='s', ms=2, label='SNS')
        ax2.spines['right'].set_visible(True); ax2.tick_params(labelsize=5.6, length=1.5, pad=1, colors=GREY)
        ax.axvline(es, color=ORANGE, lw=.7, zorder=0); ax.tick_params(labelsize=5.8, colors=BLUE, axis='y')
        n = int(g.validation_frames.iloc[0]); ax.set_title(f'{name} ({n} validation frames)', pad=2.5, fontsize=7)
        style(ax)
        ax = axes[1, c]; gg = g[g.eligible.astype(str) == 'True']
        J = pd.to_numeric(gg.J, errors='coerce'); jmin = float(J.min())
        ax.fill_between([.5, 10.5], jmin, jmin + .01, color=LORANGE, lw=0, zorder=0)
        ax.plot(100 * gg.epsilon, J, color='k', lw=.9, marker='o', ms=2.2)
        ax.plot([es], [float(pd.to_numeric(sel.J).iloc[0])], marker='*', ms=7, color=ORANGE, mec='k', mew=.4, zorder=5)
        ax.axvline(es, color=ORANGE, lw=.7, zorder=0); ax.set_ylim(-.06, 1.06); ax.set_xticks([0, 2, 4, 6, 8, 10]); style(ax)
        if name in ('Gaussian', 'Ring'):
            ax.text(.5, .55, 'all candidates equal;\nsmallest budget kept', transform=ax.transAxes, ha='center', fontsize=5.6, color=GREY)
    axes[0, 0].set_ylabel('NPE (%)', color=BLUE, labelpad=2); axes[1, 0].set_ylabel(r'$J$', labelpad=2)
    fig.supxlabel(r'Merge budget $\varepsilon$ (%)', y=-.02, fontsize=7)
    h = [Line2D([], [], color=BLUE, marker='o', ms=2.2, lw=.9, label='validation NPE (left axis)'),
         Line2D([], [], color=GREY, ls='--', marker='s', ms=2, lw=.9, label='validation SNS (right axis)'),
         Line2D([], [], color='k', marker='o', ms=2.2, lw=.9, label=r'$J=0.5\,\mathrm{NPE}_{norm}+0.5\,\mathrm{SNS}_{norm}$'),
         Patch(fc=LORANGE, lw=0, label='within 0.01 of the minimum'), Line2D([], [], ls='none', marker='*', ms=6, mfc=ORANGE, mec='k', mew=.4, label='selected')]
    fig.legend(handles=h, ncol=5, loc='lower center', bbox_to_anchor=(.5, -.17), frameon=False, fontsize=6, handlelength=1.6, columnspacing=1.2)
    fig.subplots_adjust(left=.06, right=.97, top=.9, bottom=.14, hspace=.3, wspace=.42)
    fig.savefig(OUT / 'budget_supp_selection.pdf', bbox_inches='tight', pad_inches=.015)
    fig.savefig(PREV / 'budget_supp_selection.png', dpi=250, bbox_inches='tight', pad_inches=.015)
    plt.close(fig)


# ---------------------------------------------------------------- v21 main figure: 2D and 3D in one row, common budgets
def main_figure_v21():
    E = [0, 2, 5, 10, 20]
    vol = pd.read_csv(SWEEP / 'volume_per_frame_audit.csv'); assert vol.rendered_budget_ok.all()
    cols = []
    for n in PLANAR:
        runs = load_planar(n)
        cols.append((n, f'{n} (2D, {FRAMES[n]})', {e: 100 * runs[e].NPE.to_numpy() for e in E}, {e: 100 * runs[e].topology_max.to_numpy() for e in E}, SELECTED[n]))
    for n in ['Tangaroa', 'Cylinder']:
        g = vol[vol.dataset == n]; nf = g.frame.nunique()
        cols.append((n, f'{n} (3D, {nf})', {e: 100 * g[np.isclose(g.epsilon, e / 100)].E_max.to_numpy() for e in E},
                     {e: 100 * g[np.isclose(g.epsilon, e / 100)].NMLE_max.to_numpy() for e in E}, None))
    fig = plt.figure(figsize=(7.0, 2.35))
    gs = fig.add_gridspec(2, 6, width_ratios=[1, 1, 1, .12, 1, 1], height_ratios=[1.45, 1], hspace=.2, wspace=.32)
    slots = [0, 1, 2, 4, 5]; pos = np.arange(len(E)); stats = {}
    for c, (n, title, disp, merr, sel) in zip(slots, cols):
        col = [(ORANGE, LORANGE) if e == sel else (DARK, LDARK) if e == 0 else (BLUE, LIGHT) for e in E]
        ax = fig.add_subplot(gs[0, c]); sqrt_axis(ax)
        boxes(ax, pos, [disp[e] for e in E], col, width=.6)
        top = max(v.max() for v in disp.values()); ax.set_ylim(0, top * 1.08)
        tk = [t for t in {'Storms': [0, 1, 5, 10, 20, 40], 'Wildfires': [0, .5, 1, 2, 4], 'Ring': [0, 1, 2, 5, 10],
                          'Tangaroa': [0, 1, 5, 10], 'Cylinder': [0, 1, 5, 10, 20]}[n] if t <= top * 1.08]
        ax.set_yticks(tk); ax.set_yticklabels([f'{t:g}' for t in tk])
        ax.set_xticks(pos); ax.set_xticklabels([]); ax.set_xlim(-.6, len(E) - .4); ax.set_title(title, pad=2.5, fontsize=7); style(ax)
        ax2 = fig.add_subplot(gs[1, c])
        strip(ax2, pos, [merr[e] for e in E], col, width=.6, s=1.1, alpha=.35)
        ax2.scatter(pos, E, marker='_', s=36, color=GREY, lw=.9, zorder=4)
        ax2.set_xticks(pos); ax2.set_xticklabels([f'{e:g}' for e in E]); ax2.set_xlim(-.6, len(E) - .4); ax2.set_ylim(-.8, 21); ax2.set_yticks([0, 10, 20]); style(ax2)
        if c == 0:
            ax.set_ylabel('Worst displacement\nper frame (%)', labelpad=2); ax2.set_ylabel('Merge error\nper frame (%)', labelpad=5)
        stats[n] = {e: (round(float(np.median(disp[e])), 2), round(float(np.percentile(disp[e], 90)), 2), round(float(disp[e].max()), 2),
                        int((merr[e] > 1e-4).sum()), len(merr[e])) for e in E}
    fig.text(.53, .015, r'Merge budget $\varepsilon$ (%)', ha='center', fontsize=7)
    h = [Patch(fc=LDARK, ec=DARK, lw=.5, label=r'Exact ($\varepsilon=0$)'), Patch(fc=LIGHT, ec=BLUE, lw=.5, label=r'$\varepsilon>0$'),
         Patch(fc=LORANGE, ec=ORANGE, lw=.5, label=r'Balanced (selected $\varepsilon$)'),
         Line2D([], [], ls='none', marker='D', ms=2.6, mfc='white', mec=GREY, mew=.55, label='mean'),
         Line2D([], [], ls='none', marker='_', ms=6, mec=GREY, mew=.9, label=r'budget $\varepsilon$')]
    fig.legend(handles=h, ncol=5, loc='upper center', bbox_to_anchor=(.53, 1.06), frameon=False, fontsize=6.3, handlelength=1.2, columnspacing=1.3)
    fig.subplots_adjust(left=.075, right=.995, top=.88, bottom=.13)
    for ext in ['pdf', 'svg']:
        fig.savefig(OUT / f'budget_distribution_2d3d.{ext}', bbox_inches='tight', pad_inches=.015)
    fig.savefig(PREV / 'budget_distribution_2d3d.png', dpi=250, bbox_inches='tight', pad_inches=.015)
    plt.close(fig)
    return stats


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['v21']:
        for k, v in main_figure_v21().items():
            print(k, v)
        raise SystemExit
    st = main_figure()
    for k, v in st.items():
        print(k, {a: (tuple(round(x, 2) for x in b) if isinstance(b, tuple) else b) for a, b in v.items()})
    print('extended', json.dumps(supp_extended()))
    supp_matrix()
    print('volume', json.dumps(supp_volume()))
    supp_selection()
