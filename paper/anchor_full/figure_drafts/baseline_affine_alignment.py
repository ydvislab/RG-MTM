"""Best affine alignment of the baseline axes on the volumes (v34, 2026-11-09).

TMTM and ST-MTM do not define an origin or scale for their axis, so comparing their anchors with q on the canvas could be
unfair. For each baseline and volume this script fits ONE affine map x = s u + b per sequence that minimizes the mean over
frames of the worst displacement (a linear program). It favours the baselines. The unaligned value must reproduce Table 1.
Run from the repository root. Output: paper/anchor_full/figdata/family_sweep20261109/affine_alignment.json
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
ROOT = Path(__file__).resolve().parents[3]; FIG = ROOT / 'paper/anchor_full/figdata'; RES = ROOT / 'code/results/stmtm_completion20261026'
TABLE = {'Tangaroa': (.3063, .3418), 'Cylinder': (.4769, .5160)}
KEY = {'Tangaroa': 'tangaroa', 'Cylinder': 'square-cylinder3d'}


def fit(U, Q, L):
    T = len(Q); R, C, V, b = [], [], [], []; k = 0
    for t, (u, q) in enumerate(zip(U, Q)):
        for ui, qi in zip(u, q):
            for sg in (1, -1):
                R += [k] * 3; C += [0, 1, 2 + t]; V += [sg * ui, sg, -L]; b.append(sg * qi); k += 1
    r = linprog(np.r_[0, 0, np.ones(T) / T], A_ub=sparse.csr_matrix((V, (R, C)), shape=(k, 2 + T)), b_ub=b, bounds=[(None, None)] * 2 + [(0, None)] * T, method='highs')
    assert r.status == 0; return float(r.fun), [float(v) for v in r.x[:2]]


out = {}
for name, key in KEY.items():
    G = json.loads((FIG / f'volume_gallery20261108/{name.lower()}.json').read_text()); L, o = G['canvas'], G['origin']; Q = [np.asarray(q, float) for q in G['q']]
    nat = json.loads((RES / key / 'landmarks.json').read_text())['positions']; out[name] = {}
    for m, table in zip(('TMTM', 'ST-MTM'), TABLE[name]):
        U = [np.asarray(a, float) for a in nat[m]]; f = lambda V: float(np.mean([np.max(np.abs(a - q)) / L for a, q in zip(V, Q)]))
        raw = f([o + L * (1 - a) if G['maps'][m]['mirrored'] else o + L * a for a in U]); assert abs(raw - table) < 5e-4, (name, m, raw, table)
        v, x = fit(U, Q, L); out[name][m] = dict(table1_NPE=raw, best_affine_NPE=v, slope=x[0], intercept=x[1]); print(name, m, out[name][m], flush=True)
(FIG / 'family_sweep20261109/affine_alignment.json').write_text(json.dumps(out, indent=1) + '\n')
