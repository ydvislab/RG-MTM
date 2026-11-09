"""Supplementary tables of v34 (2026-11-09): moving within the common model, and TW / TD / ME with the reference itself.
Inputs: figdata/family_sweep20261109/{cylinder,tangaroa,temporal_reference}.json and code/results/metrics_n1c20261027.
Output: ../../pvis2027/latex_v30/tables/table_family.tex, table_temporal.tex
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]; FIG = HERE.parent / 'figdata/family_sweep20261109'; OUT = HERE.parents[1] / 'pvis2027/latex_v30/tables'
N1C = ROOT / 'code/results/metrics_n1c20261027'
read = lambda p: json.loads(Path(p).read_text())
C, T = read(FIG / 'cylinder.json')['instances'], read(FIG / 'tangaroa.json')['instances']
for I, f in ((C, 'cylinder'), (T, 'tangaroa')):   # the ST-MTM row quotes the stored SNS/TW of Table 1 (recomputing from rounded anchors differs by < 0.001)
    b = read(N1C / f'{f}.json')['baselines']['ST-MTM']; I['ST-MTM'] = {**I['ST-MTM'], 'SNS': b['SNS'], 'TW1': b['TW1']}
ROWS = [('reference', r'Reference, $x=q$', '--', '--', '--'), ('default', r'AnchorMTM default (Table~1, Exact)', r'$(4,1,.5,.1)$', r'$\tau$-selected', 'yes'),
        ('geometry', r'No reference term', r'$(0,1,.5,.1)$', r'$\tau$-selected', 'yes'), ('uncapped', 'No reference term, no cap', r'$(0,1,.5,.1)$', r'$\tau$-selected', 'no'),
        ('ST order', 'ST-MTM leaf order, stationary target', r'$(0,1,.5,.1)$', 'ST-MTM', 'no'), ('ST-MTM', 'ST-MTM run', '--', 'ST-MTM', '--')]
cell = lambda s: f"{s['SNS']:.3f} & {s['TW1']:.3f} & {100 * s['NPE']:.1f}"
lines = [r'\begin{table*}[!htb]', r'\centering', r'\caption{Moving within the common model of Eq.~6 at zero merge error. Same trees, references, widths and tracks as the volume rows of Table~1; the weights are $(\lambda_R,\lambda_G,\lambda_M,\lambda_C)$ and are the same on both volumes. NPE in \% of the axis.}', r'\label{tab:family}', r'\footnotesize', r'\begin{tabular}{@{}llll ccc ccc@{}}', r'\toprule',
         r' & & & & \multicolumn{3}{c}{Cylinder} & \multicolumn{3}{c}{Tangaroa} \\', r'\cmidrule(lr){5-7}\cmidrule(l){8-10}', r'Setting & Weights & Leaf order & Cap & SNS & TW & NPE & SNS & TW & NPE \\', r'\midrule']
for k, name, w, o, cap in ROWS:
    lines.append(f"{name} & {w} & {o} & {cap} & {cell(C[k])} & {cell(T[k])} \\\\")
lines += [r'\bottomrule', r'\end{tabular}', r'\end{table*}']
(OUT / 'table_family.tex').write_text('\n'.join(lines) + '\n')

REF = read(FIG / 'temporal_reference.json'); REF['Cylinder'] = C['reference']; REF['Tangaroa'] = T['reference']
SEQ = [('Storms', 'storms', 'Storms'), ('Wildfires', 'wildfires', 'Wildfires'), ('OLR', 'olr', 'OLR'), ('PM2.5', 'pm25', r'PM$_{2.5}$ (daily)'), ('Ring', 'ring', 'Ring'), ('Cylinder', 'cylinder', 'Cylinder'), ('Tangaroa', 'tangaroa', 'Tangaroa')]
def fmt(v, kind):
    return f'{v:.3f}' if kind == 'TW1' else (f'{v:.1f}' if kind == 'TD' else f'{v:.0f}')
def val(s, kind):
    return 100 * s['ME_errors'] / s['ME_clear'] if kind == 'ME' else s[kind]
L = [r'\begin{table*}[!htb]', r'\centering', r'\caption{Neighborhoods and temporal behavior. $q$ draws every feature at its reference. TW uses $k=1$; TD is the summed displayed motion of matched anchors, in axis lengths; ME is the share (\%) of feature pairs whose displayed approach or separation contradicts the true one. Volume rows are the runs of Table~1; the planar rows are the sequences of an earlier audit, preprocessed differently from the benchmark reconstructions of Table~1.}', r'\label{tab:temporal}', r'\footnotesize', r'\setlength{\tabcolsep}{2.5pt}', r'\begin{tabular}{@{}l ccccc ccccc ccccc@{}}', r'\toprule',
     r' & \multicolumn{5}{c}{TW$\uparrow$} & \multicolumn{5}{c}{TD} & \multicolumn{5}{c}{ME (\%)$\downarrow$} \\', r'\cmidrule(lr){2-6}\cmidrule(lr){7-11}\cmidrule(l){12-16}', r'Sequence' + r' & $q$ & TMTM & ST-MTM & Exact & 10\%' * 3 + r' \\', r'\midrule']
for name, f, label in SEQ:
    d = read(N1C / f'{f}.json'); row = [label]
    for kind in ('TW1', 'TD', 'ME'):
        pick = [REF[name], d['baselines']['TMTM'], d['baselines']['ST-MTM'], d['settings']['eps=0'], d['settings']['eps=0.1']]
        row += [fmt(val(s, kind), kind) for s in pick]
    L.append(' & '.join(row) + r' \\')
L += [r'\bottomrule', r'\end{tabular}', r'\end{table*}']
(OUT / 'table_temporal.tex').write_text('\n'.join(L) + '\n')
print('ok')
