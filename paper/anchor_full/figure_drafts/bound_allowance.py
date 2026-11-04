"""Order bound at the numerical allowance eps0 (2026-11-05).

Exact Mode allows merge error eta = eps0 * range (eps0 = 1e-7). The tight order bound for
that class is max(Theorem B, Theorem C) at eta, i.e. the ``lower`` of ``budget_order`` at
budget 0 and tie eps0. The collaborator's ``nu_mean`` and the direction sweep store Theorem B
alone (``certificate(..., tie)`` flattens every gap <= 2 tie), which is valid but not attained
on two Cylinder frames (58, 62). This script recomputes, read-only with the collaborator's
code, the 400-direction sweep of experiments/reference_direction with the tight bound.

Shortcut (exact): if Theorem B equals the exact-tree nu* (tie 0) on a frame, Theorem C equals
it too (B <= C <= optimum <= nu*(T)), so C is evaluated only on frames where B < nu*(T).
Run from the RG-MTM root:  .venv/bin/python -I paper/anchor_full/figure_drafts/bound_allowance.py
Output: paper/anchor_full/figdata/bound_allowance20261105/{tangaroa,cylinder}_direction.json;
        argument 'frames': cylinder_frames.json (per-frame bounds, exhaustive check of frames 58 and 62)
"""
import importlib.util, json, sys, time
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path.insert(0, str(CODE / 'src'))
from rgmtm.order_certificate import certificate, chain_certificate

spec = importlib.util.spec_from_file_location('refdir_run', CODE / 'experiments/reference_direction/run.py')
rd = importlib.util.module_from_spec(spec); spec.loader.exec_module(rd)
n1 = rd.n1
OUT = Path(__file__).resolve().parents[1] / 'figdata/bound_allowance20261105'
SAVED = Path(__file__).resolve().parents[1] / 'figdata/reference_direction20261027'


def run(name):
    cfg = dict(rd.SETS[name]); d = n1.DATASETS[name]()
    feats = json.loads((CODE / cfg['features']).read_text())['frames']; X = [np.asarray(f['extrema'], float) for f in feats]
    if cfg['box'] is None:
        c = np.load(CODE / 'data/real/paper1_suite/square-cylinder3d/coordinates.npz') if (CODE / 'data/real').exists() else \
            np.load(ROOT / 'data/real/paper1_suite/square-cylinder3d/coordinates.npz')
        cfg['box'] = [(float(c[k].min()), float(c[k].max())) for k in 'xyz']
    V = [np.asarray(v, float) for v in d['merge']]; R = d['scalar_range']; tie = n1.TIE * R
    saved = json.loads((SAVED / f'{name.lower()}.json').read_text())

    def refs(direction):
        u = np.asarray(direction, float); u = u / np.linalg.norm(u); o, L = rd.canvas(u, cfg['box'])
        return [x @ u for x in X], L

    def bounds(direction):
        qs, L = refs(direction); B, A, T = [], [], []
        for v, q in zip(V, qs):
            b = certificate(v, q, L, 0., tie); a = certificate(v, q, L, 0., 0.)
            t = b if b >= a - 1e-15 else max(b, chain_certificate(v, q, L, 0., tie))
            B.append(b); A.append(a); T.append(t)
        return np.array(A), np.array(B), np.array(T)

    t0 = time.perf_counter(); sweep = []
    for k, direction in enumerate(rd.hemisphere()):
        A, B, T = bounds(direction)
        assert abs(B.mean() - saved['sweep'][k]['nu_mean']) < 1e-12, (k, B.mean(), saved['sweep'][k]['nu_mean'])
        sweep.append(dict(direction=direction.tolist(), nu_exact_tree=float(A.mean()), nu_B=float(B.mean()),
                          nu_allow=float(T.mean()), frames_B_below=int(np.sum(T > B + 1e-12))))
    keys = {}
    for lab, row in saved['key_directions'].items():
        A, B, T = bounds(row['direction'])
        assert abs(B.mean() - row['nu_mean']) < 1e-12
        keys[lab] = dict(direction=row['direction'], nu_exact_tree=float(A.mean()), nu_B=float(B.mean()), nu_allow=float(T.mean()),
                         frames_B_below=int(np.sum(T > B + 1e-12)), ours_NROE=row['ours_NROE'],
                         **{m: row[m] for m in ('TMTM_NROE', 'ST-MTM_NROE')})
    allow = np.array([r['nu_allow'] for r in sweep])
    return dict(dataset=name, frames=len(V), tie=tie, seconds=time.perf_counter() - t0,
                nu_allow_range=[float(allow.min()), float(allow.max())],
                nu_B_range=saved['nu_mean_range'],
                stored_rank_allow=int(np.sum(allow < keys['stored']['nu_allow'] - 1e-15)),
                directions_with_B_below=int(sum(r['frames_B_below'] > 0 for r in sweep)),
                argmin_allow=sweep[int(np.argmin(allow))]['direction'], key_directions=keys, sweep=sweep)


def cylinder_frames():
    """Per-frame bounds on Cylinder (stored x reference) and an exhaustive check of the frames where
    Theorem B is loose: every order with merge error <= tie is legal in T^(2 tie) (Theorem B), so
    enumerating those orders and keeping the ones with merge cost <= tie gives the true optimum."""
    import math
    from itertools import permutations, product
    sys.path.insert(0, str(CODE / 'experiments/order_budget'))
    import run as ob
    from rgmtm.order_certificate import hierarchy, _flattened_children, order_errors, order_error, budget_order, midpoint_order
    from rgmtm.framework import merge_costs
    d = ob.DATASETS['Cylinder'](); L, R = d['extent'], d['range']; tie = ob.TIE * R; rows = []
    for i, (V, q) in enumerate(d['frames']):
        V = np.asarray(V, float); q = np.asarray(q, float)
        b = certificate(V, q, L, 0., tie); c = chain_certificate(V, q, L, 0., tie); bo = budget_order(V, q, L, 0., tie)
        row = dict(frame=i, leaves=len(V), nu_exact_tree=certificate(V, q, L, 0., 0.), nu_B=b, nu_C=c, attained=bo['nroe'],
                   attained_merge_error=bo['delta'] / R)
        if c > b + 1e-12:
            mo = midpoint_order(V, q, 2 * tie); row['B_order_merge_error'] = float(merge_costs([mo], V)[0]) / R
            row['B_order_nroe'] = order_error(mo, q, L)
            nodes, root = hierarchy(V)
            def legal(k):
                if not nodes[k]['children']: return [[k]]
                ch = _flattened_children(nodes, k, 2 * tie); subs = [legal(x) for x in ch]
                return [sum(cmb, []) for perm in permutations(range(len(ch))) for cmb in product(*[subs[p] for p in perm])]
            P = np.array(legal(root), int); mc = merge_costs(P, V); ne = order_errors(P, q, L); ok = mc <= tie
            row.update(enumerated=len(P), enumerated_feasible=int(ok.sum()), enumerated_optimum=float(ne[ok].min()))
        rows.append(row)
    m = lambda k: float(np.mean([r[k] for r in rows]))
    out = dict(tie=tie, frames=len(rows), means={k: m(k) for k in ('nu_exact_tree', 'nu_B', 'nu_C', 'attained')},
               frames_attained=int(sum(abs(r['attained'] - max(r['nu_B'], r['nu_C'])) < 1e-12 for r in rows)),
               max_attained_merge_error=max(r['attained_merge_error'] for r in rows),
               loose_frames=[r for r in rows if 'enumerated' in r], per_frame=rows)
    (OUT / 'cylinder_frames.json').write_text(json.dumps(out, indent=1)); return out


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ['frames']:
        r = cylinder_frames(); print(json.dumps({k: v for k, v in r.items() if k != 'per_frame'}, indent=1)); sys.exit()
    for name in sys.argv[1:] or ['Cylinder', 'Tangaroa']:
        r = run(name); (OUT / f'{name.lower()}_direction.json').write_text(json.dumps(r, indent=1))
        print(name, '%.0fs' % r['seconds'], 'allow range %.2f-%.2f%%' % tuple(100 * x for x in r['nu_allow_range']),
              'B range %.2f-%.2f%%' % tuple(100 * x for x in r['nu_B_range']), 'stored rank', r['stored_rank_allow'],
              'directions where B is loose', r['directions_with_B_below'], flush=True)
        for lab, k in r['key_directions'].items():
            print('   %-15s exact-tree %.2f  B %.2f  allow %.2f  Exact Mode %.2f  gap %.2f' % (lab, *(100 * k[x] for x in ('nu_exact_tree', 'nu_B', 'nu_allow', 'ours_NROE')), 100 * (k['ours_NROE'] - k['nu_allow'])))
