"""v29 Table 1: one comparison table on the seven sequences used throughout the paper (2026-11-09).

Rows: Storms, Wildfires, OLR, PM2.5 (daily), Ring, Tangaroa, Cylinder (the former "bound suite").
Columns: Hilbert and Morton curves (planar only; orientation with the lowest mean NROE, best_mirror.curve),
TMTM and ST-MTM (native outputs in the mirror with the lower mean displacement), AnchorMTM at eps = 0 and 10%
(default configuration; frontier orders and capped QP). Measures: NPE (mean over frames of the worst displacement /
canvas), SNS and TW (k = 1) of anchor distances against support-centroid distances.
Sources (all saved or recomputed with checks):
  NPE   natives and AnchorMTM eps = 0: planar_gallery20261109 / volume_gallery20261108 (x positions);
        AnchorMTM eps = 10%: recomputed here with volume_gallery_data.anchor (checked against the frontier values);
        curves: space_filling20261105 per orientation.
  SNS, TW  natives: metrics_n1c20261027 baselines (make_figure_drafts.st); AnchorMTM: metrics_n1c settings eps=0 / eps=0.1;
        curves: space_filling20261105 per orientation.
Output: figdata/table1_suite20261109.json and ../../pvis2027/latex_v21/tables/table1_suite.tex
"""
import json
from pathlib import Path
import numpy as np
import volume_gallery_data as vg
import make_figure_drafts as mf
import best_mirror as bm

HERE = Path(__file__).resolve().parent; FIG = HERE.parent / 'figdata'; OUT = HERE.parents[1] / 'pvis2027/latex_v21/tables'
NAMES = ['Storms', 'Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
PLANAR = NAMES[:5]
LABEL = {'PM2.5': r'PM$_{2.5}$'}
read = lambda p: json.loads(Path(p).read_text())


def npe(xs, qs, o, L):
    return float(np.mean([np.max(np.abs((np.asarray(x) - np.asarray(q)) / L)) for x, q in zip(xs, qs)]))


def gallery(n):
    f = FIG / (f'planar_gallery20261109/{n.lower().replace(".", "")}.json' if n in PLANAR else f'volume_gallery20261108/{n.lower()}.json')
    if n == 'Storms':
        return None
    return read(f)


def main():
    rows = {}
    vg.EPS = [.1]
    for n in NAMES:
        r = {}
        M = read(FIG / f'metrics_n1c20261027/{mf.FILE[n]}.json')
        G = gallery(n)
        if G is None:   # Storms is not in the planar gallery: compute its native and eps=0 positions here
            import planar_gallery_data as pg
            vg.EPS = [0, .05, .2]; G = vg.anchor(n); pg.native(n, G); vg.EPS = [.1]
            (FIG / 'planar_gallery20261109/storms.json').write_text(json.dumps(G) + '\n')
        L, o, Q = G['canvas'], G['origin'], G['q']
        A10 = vg.anchor(n)
        for key, lab in (('TMTM', 'TMTM'), ('ST-MTM', 'ST-MTM')):
            s = mf.st(n, key)
            r[lab] = dict(NPE=npe(G['maps'][key]['x'], Q, o, L), SNS=float(s['SNS']), TW=float(s['TW1']), NMLE=0.)
        r['Exact'] = dict(NPE=npe(G['maps']['eps=0']['x'], Q, o, L), SNS=M['settings']['eps=0']['SNS'], TW=M['settings']['eps=0']['TW1'],
                          NMLE=G['maps']['eps=0']['NMLE_max'])
        r['10%'] = dict(NPE=npe(A10['maps']['eps=0.1']['x'], Q, o, L), SNS=M['settings']['eps=0.1']['SNS'], TW=M['settings']['eps=0.1']['TW1'],
                        NMLE=A10['maps']['eps=0.1']['NMLE_max'])
        if n in PLANAR:
            for c in ('Hilbert', 'Morton'):
                b = bm.curve(n, c); r[c] = dict(NPE=b['NPE'], SNS=b['SNS'], TW=b['TW'], NMLE=b['NMLE_max'])
        rows[n] = r
        print(n, {k: {m: round(v, 4) for m, v in d.items()} for k, d in r.items()}, flush=True)
    (FIG / 'table1_suite20261109.json').write_text(json.dumps(rows, indent=1) + '\n')
    write_tex(rows)


def write_tex(rows):
    meths = ['Hilbert', 'Morton', 'TMTM', 'ST-MTM', 'Exact', '10%']
    def fmt(n, m, k):
        if m not in rows[n]: return '--'
        v = rows[n][m][k]; vals = [rows[n][mm][k] for mm in meths if mm in rows[n]]
        best = min(vals) if k != 'TW' else max(vals)
        s = f'{v:.3f}'
        return f'$\\mathbf{{{s}}}$' if abs(v - best) < 5e-4 else f'${s}$'
    head = ' & '.join([f'\\multicolumn{{3}}{{c}}{{{h}}}' for h in ['Hilbert', 'Morton', 'TMTM', 'ST-MTM', r'Ours, $\varepsilon=0$', r'Ours, $\varepsilon=10\%$']])
    sub = ' & '.join(['NPE$\\downarrow$ & SNS$\\downarrow$ & TW$\\uparrow$'] * 6)
    cmid = ''.join([f'\\cmidrule(lr){{{2 + 3 * k}-{4 + 3 * k}}}' for k in range(6)])
    lines = [r'\begin{table*}[t]', r'\centering',
             r'\caption{Comparison on the seven sequences. NPE: mean worst displacement per frame, relative to the axis length (the property AnchorMTM optimizes); SNS and TW: distance fidelity of anchor separations to support-centroid distances (not optimized by AnchorMTM). Bold: best per row and measure. All maps keep the tree except the curves, whose worst merge error is 8--40\% of the scalar range, and AnchorMTM at $\varepsilon=10\%$, which stays within its budget. Curves exist for planar data only.}',
             r'\label{tab:quantitative-final}', r'\footnotesize', r'\setlength{\tabcolsep}{1.6pt}', r'\renewcommand{\arraystretch}{0.95}',
             r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l*{18}{c}@{}}', r'\toprule',
             'Sequence & ' + head + r' \\', cmid, ' & ' + sub + r' \\', r'\midrule']
    for n in NAMES:
        cells = [fmt(n, m, k) for m in meths for k in ('NPE', 'SNS', 'TW')]
        lines.append(LABEL.get(n, n) + ' & ' + ' & '.join(cells) + r' \\')
        if n == 'Ring': lines.append(r'\midrule')
    lines += [r'\bottomrule', r'\end{tabular*}', r'\end{table*}']
    (OUT / 'table1_suite.tex').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
