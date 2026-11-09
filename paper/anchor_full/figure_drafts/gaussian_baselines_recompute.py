"""Recompute TMTM and ST-MTM on the Gaussian preparation (64 frames) with the collaborator's own pipeline, unchanged,
then measure their order error (NROE) and the exact-topology bound nu* per frame.

Pipeline: paper/pvis2027/experiments_ratio_p_20261104/source/run.py, functions load() and baseline_npe() (the path its
line 269 uses for baselines only). Only the output folder run.O is redirected to scratch; no repository file is written.
Check: the recomputed NPE of both baselines must equal Table 1 (0.1118 and 0.1154).
"""
import json, sys, types
from pathlib import Path
import numpy as np

REPO = Path('C:/Users/ASUS/Desktop/RG-MTM')
SRC = REPO / 'paper/pvis2027/experiments_ratio_p_20261104/source'
PREP = Path(sys.argv[1])                       # extracted preparation folder
OUT = Path(sys.argv[2])                        # scratch output
sys.path[:0] = [str(SRC)]
sys.modules['netCDF4'] = types.SimpleNamespace(Dataset=None, num2date=None)   # only the Storms loader uses it
import run                                     # noqa: E402  (the collaborator's module, not modified)
from rgmtm.order_certificate import certificate, budget_order   # noqa: E402

run.O = OUT
F = np.load(PREP / 'fields.npy'); xy = np.load(PREP / 'coordinates.npy'); meta = json.loads((PREP / 'protocol.json').read_text())
d = run.load('Gaussian', F, xy, meta['sample_measure'], PREP / 'trees')
res = run.baseline_npe('Gaussian', d)
print('baseline_npe:', [(r['Method'], r.get('NPE'), r.get('success'), r.get('one_global_reflection')) for r in res])

p = d['parameters']; L = float(p.canvas); qs = d['reference']['qs']; V = d['merge_values']
print('canvas', L, 'origin', p.canvas_origin, 'frames', len(qs), 'leaves per frame', sorted({len(q) for q in qs}))
print('merge_values[0]:', np.asarray(V[0]).shape)
nroe = lambda order, q: max([0.] + [q[order[j]] - q[order[k]] for k in range(len(order)) for j in range(k)]) / (2 * L)
nu = np.array([certificate(np.asarray(V[t], float), np.asarray(qs[t], float), L, 0.) for t in range(len(qs))])
anc = np.array([budget_order(np.asarray(V[t], float), np.asarray(qs[t], float), L, 0., 0.)['nroe'] for t in range(len(qs))])
out = dict(dataset='Gaussian', frames=len(qs), nu_strict=100 * float(nu.mean()), anchor_nroe=100 * float(anc.mean()))
for mode, label in (('tmtm', 'TMTM'), ('temporal', 'ST-MTM')):
    U = json.loads((OUT / 'results/Gaussian/baseline_npe' / f'{mode}_anchors.json').read_text())
    per = [nroe(list(np.argsort(np.asarray(u, float), kind='stable')), np.asarray(q, float)) for u, q in zip(U, qs)]
    npe = np.mean([np.max(np.abs(np.asarray(u) - np.asarray(q))) / L for u, q in zip(U, qs)])
    out[label] = 100 * float(np.mean(per)); out[label + '_NPE'] = float(npe)
    out[label + '_frames_with_order_error'] = int(sum(x > 1e-12 for x in per))
print(json.dumps(out, indent=1))
(OUT / 'gaussian_result.json').write_text(json.dumps(out, indent=1))
