"""Fig. 8 (v32): where a merge budget acts, per frame (2026-11-09).

Data: the collaborator's recomputed per-frame records (package 01: planar_per_frame_recomputed.csv,
volume_per_frame_recomputed.csv): worst displacement E_max per frame and the attained merge error, for every budget.
If that package is present (PKG, or the environment variable ANCHOR_PKG01), the summary is computed from it and written
to ../figdata/budget_her20261109/summary.json; otherwise the saved summary is drawn.
Encoding: for each sequence, the median, the 90th percentile and the worst frame of E_max over the budget, plus the mean
(= NPE) as a dashed line; the bar row gives the share of frames whose attained merge error is positive.
v32 wording: no abbreviations ("pct."), axis labels state the unit (% of the axis), the bar row says what is counted.
Output: ../../pvis2027/latex_v30/figures/budget_response_v30.{pdf,png}
"""
import json, os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import v23_figures as v

PKG = Path(os.environ.get('ANCHOR_PKG01', '/Users/yudong/Downloads/老师所需四项材料_20261109/01_七序列下界与AnchorMTM输入'))
HERE = Path(__file__).resolve().parent
SUMMARY = HERE.parent / 'figdata/budget_her20261109/summary.json'
OUT = HERE.parents[1] / 'pvis2027/latex_v30/figures'
SEQ = [('Ring', 'Ring (2D)'), ('Wildfires', 'Wildfires (2D)'), ('Storms', 'Storms (2D)'), ('PM2.5', r'PM$_{2.5}$ (2D)'), ('Tangaroa', 'Tangaroa (3D)'), ('Cylinder', 'Cylinder (3D)')]
BLUE = '#0B5CAD'; LIGHT = '#9EC3E6'; GREY = '#555555'; ORANGE = '#C25A00'


def gaussian():
    L = json.loads((PKG / 'Gaussian/metadata.json').read_text())['parameters']['canvas']; o = dict(epsilon=[], median=[], p90=[], max=[], mean=[], used=[])
    for e, f in ((0., 'Exact'), (.01, 'epsilon_0.01'), (.02, 'epsilon_0.02'), (.05, 'epsilon_0.05'), (.1, 'epsilon_0.1'), (.2, 'epsilon_0.2')):
        J = json.loads((PKG / f'Gaussian/AnchorMTM_{f}_layouts.json').read_text())
        E = 100 * np.array([np.max(np.abs(np.array(x['x']) - np.array(x['reference']))) / L for x in J]); M = np.array([x['continuous_NMLE'] for x in J])
        for k, v in zip(('epsilon', 'median', 'p90', 'max', 'mean', 'used'), (e, np.median(E), np.percentile(E, 90), E.max(), E.mean(), 100 * (M > 1e-5).mean())):
            o[k].append(float(v))
    return o


def summary():
    saved = json.loads(SUMMARY.read_text())['data'] if SUMMARY.exists() else {}
    if not (PKG / 'planar_per_frame_recomputed.csv').exists():
        return saved
    import pandas as pd
    d = pd.concat([pd.read_csv(PKG / 'planar_per_frame_recomputed.csv'), pd.read_csv(PKG / 'volume_per_frame_recomputed.csv')])
    assert (d['NMLE_max'] <= d['epsilon'] + 1e-6).all() and d['rendered_budget_ok'].all()
    out = {}
    for n, _ in SEQ:
        s = d[d.dataset == n]
        if n == 'Gaussian':   # not in the CSVs: the archived layouts of package 01 (their NPE equals Table 1, 0.0089)
            out[n] = gaussian(); continue
        if s.empty:   # Wildfires: taken from the saved summary (planar_per_frame records, see its 'wildfires_source')
            out[n] = saved[n]; continue
        E = sorted(s.epsilon.unique()); st = {e: 100 * s[s.epsilon == e].E_max.values for e in E}
        out[n] = dict(epsilon=[float(e) for e in E], median=[float(np.median(st[e])) for e in E], p90=[float(np.percentile(st[e], 90)) for e in E],
                      max=[float(st[e].max()) for e in E], mean=[float(st[e].mean()) for e in E],
                      used=[float(100 * (s[s.epsilon == e].NMLE_max > 1e-5).mean()) for e in E])
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(dict(source=f'computed by fig7_budget_her.py from {PKG.name} (exact; Gaussian from its archived layouts; Wildfires from the planar_per_frame records)', unit='percent', data=out), indent=1))
    return out


def main():
    v.use_times(); S = summary()
    v35 = HERE.parent / 'figdata/volumes_v35/tangaroa_x_budget.json'   # v35: Tangaroa along the streamwise x axis (no 1% run)
    if v35.exists(): S['Tangaroa'] = json.loads(v35.read_text())
    fig = plt.figure(figsize=(7.05, 2.4)); g = fig.add_gridspec(2, 6, height_ratios=[3.2, 1], hspace=.2, wspace=.3,
                                                                left=.085, right=.995, top=.79, bottom=.2)
    for k, (n, title) in enumerate(SEQ):
        s = S[n]; E = s['epsilon']; x = np.arange(len(E))
        ax = fig.add_subplot(g[0, k])
        ax.fill_between(x, s['median'], s['p90'], color=LIGHT, alpha=.55, lw=0)
        ax.plot(x, s['max'], '-', color=GREY, lw=.8, marker='^', ms=2.6)
        ax.plot(x, s['p90'], '-', color=BLUE, lw=1.1, marker='o', ms=2.6, mfc='white', mew=.8)
        ax.plot(x, s['median'], '-', color=BLUE, lw=1.6, marker='o', ms=2.8)
        ax.plot(x, s['mean'], '--', color=ORANGE, lw=1.0)
        ax.set_yscale('log'); ax.set_ylim(.5, 50); ax.set_xticks(x); ax.set_xticklabels([])
        ax.set_yticks([.5, 1, 10, 50]); ax.set_yticklabels(['0.5', '1', '10', '50']); ax.minorticks_off()
        ax.set_title(title, fontsize=8.2, pad=3); ax.tick_params(labelsize=8, length=2, pad=1)
        ax.yaxis.grid(True, color='#EEF0F2', lw=.5); ax.set_axisbelow(True)
        for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
        if k == 0: ax.set_ylabel('worst displacement\nin a frame (% of axis)', fontsize=8)
        b = fig.add_subplot(g[1, k])
        b.bar(x, s['used'], width=.6, color=LIGHT, edgecolor=BLUE, lw=.5); b.set_ylim(0, 100); b.set_yticks([0, 100])
        b.set_xticks(x); b.set_xticklabels([f'{100 * e:g}' for e in E], fontsize=7); b.tick_params(labelsize=8, length=2, pad=1)
        for sp in ('top', 'right'): b.spines[sp].set_visible(False)
        if k == 0: b.set_ylabel('frames using\nbudget (%)', fontsize=8)
        print(n, {f'{100 * e:g}': tuple(round(s[q][i], 2) for q in ('median', 'p90', 'max', 'mean', 'used')) for i, e in enumerate(E)})
    fig.text(.54, .025, r'merge budget $\varepsilon$ (% of the scalar range)', ha='center', fontsize=8.5)
    h = [Line2D([], [], color=BLUE, lw=1.6, marker='o', ms=2.8, label='median frame'),
         Line2D([], [], color=BLUE, lw=1.1, marker='o', ms=2.6, mfc='white', label='90th percentile'),
         Patch(color=LIGHT, alpha=.55, label='between the two'),
         Line2D([], [], color=GREY, lw=.8, marker='^', ms=2.6, label='worst frame'),
         Line2D([], [], color=ORANGE, lw=1, ls='--', label='mean over frames (NPE)')]
    fig.legend(handles=h, ncol=5, loc='upper center', bbox_to_anchor=(.54, 1.0), fontsize=8, frameon=False, handlelength=1.6, columnspacing=1.2)
    for ext in ('pdf', 'png'): fig.savefig(OUT / f'budget_response_v30.{ext}', dpi=300)


if __name__ == '__main__':
    main()
