"""Data for the position-topology plane (Fig. 3 of the v16 framework draft, notes/2026-11-08-framework-reframe.md).

Order model (NROE), the only fidelity in which every compared map can be measured. For every sequence:
  bound        mean over frames of max(Theorem B, Theorem C) at merge allowance eta = eps * range, tie = 0,
               on a fine grid; the suffix maximum over larger eps is also a valid bound and makes it monotone.
               At eps = 0 it is the strict exact-tree nu* (Theorem 1).
  construction budgeted midpoint ordering (rgmtm.order_certificate.budget_order, tie = 0) on a grid:
               mean NROE and the attained worst merge error (max over frames).
  optimum      exact optimum by enumeration of all leaf orders on frames with at most 8 leaves,
               compared frame by frame with the construction at every grid allowance.
  check        the saved order_budget20261027 sweep is reproduced (tie = 1e-7, nine allowances).
Collaborator code and saved results are only read.  Inputs: code/results (same as code/experiments/order_budget).

Run:  python plane_data.py [Storms ...]   ->  ../figdata/plane20261108/<sequence>.json
"""
import importlib.util, json, sys, time
from itertools import permutations
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; CODE = HERE.parents[2] / 'code'
spec = importlib.util.spec_from_file_location('ob_run', CODE / 'experiments/order_budget/run.py')
ob = importlib.util.module_from_spec(spec); spec.loader.exec_module(ob)       # adds code/src to sys.path
from rgmtm.framework import merge_costs
from rgmtm.order_certificate import certificate, chain_certificate, budget_order, order_errors

OUT = HERE.parent / 'figdata/plane20261108'
NAMES = ['Storms', 'Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
BOUND_EPS = sorted({0., 1e-8, 1e-7, 1e-6, 1e-5} | set(np.geomspace(1e-4, 1, 121).tolist()))
LABELLED = [0., .005, .01, .02, .05, .1, .2, .5, 1.]
BUILD_EPS = sorted({0., 1e-7, 1e-6, 1e-5, 1e-4} | set(np.geomspace(1e-3, 1, 31).tolist()) | set(LABELLED))


def run(name):
    d = ob.DATASETS[name](); L, R = d['extent'], d['range']; frames = d['frames']
    t0 = time.perf_counter()
    lower = np.array([[max(certificate(V, q, L, 2 * e * R), chain_certificate(V, q, L, e * R, 0.)) for V, q in frames]
                      for e in BOUND_EPS])                                              # (eps, frame)
    mean = lower.mean(1); env = np.maximum.accumulate(mean[::-1])[::-1]
    t1 = time.perf_counter()
    small = [i for i, (V, _) in enumerate(frames) if len(V) <= ob.ENUMERATE]
    enum = {}
    for i in small:
        V, q = frames[i]; P = np.array(list(permutations(range(len(V)))))
        enum[i] = (merge_costs(P, V), order_errors(P, q, L))
    build = []
    for e in BUILD_EPS:
        rows = [budget_order(V, q, L, e * R, 0.) for V, q in frames]
        nroe = np.array([r['nroe'] for r in rows]); delta = np.array([r['delta'] for r in rows]) / R
        low = np.array([max(r['lower_b'], r['lower_c']) for r in rows])
        assert np.all(delta <= e + 1e-12) and np.all(nroe + 1e-12 >= low)
        opt = np.array([enum[i][1][enum[i][0] <= e * R + 1e-12 * R].min() for i in small])
        ours = nroe[small]
        build.append(dict(epsilon=e, NROE_mean=float(nroe.mean()), NMLE_max=float(delta.max()),
                          NMLE_mean=float(delta.mean()), lower_mean=float(low.mean()),
                          frames_at_lower=int(np.sum(nroe - low < 1e-9)),
                          frames_used=int(np.sum(delta > 1e-12)),
                          enumerated=len(small), enumerated_optimal=int(np.sum(ours - opt < 1e-9)),
                          enumerated_gap_max=float((ours - opt).max()) if small else None))
    t2 = time.perf_counter()
    saved = json.loads((CODE / f'results/order_budget20261027/{name.replace(".", "").lower()}.json').read_text())
    check = []
    for s in saved['budget_sweep']:
        rows = [budget_order(V, q, L, s['epsilon'] * R, ob.TIE * R) for V, q in frames]
        a = float(np.mean([r['nroe'] for r in rows])); b = float(np.mean([r['lower'] for r in rows]))
        check.append(dict(epsilon=s['epsilon'], NROE=a, saved_NROE=s['NROE_mean'], lower=b, saved_lower=s['lower_mean']))
        assert abs(a - s['NROE_mean']) < 1e-12 and abs(b - s['lower_mean']) < 1e-12, (name, s['epsilon'], a, b)
    return dict(dataset=name, frames=len(frames), leaves=[min(len(V) for V, _ in frames), max(len(V) for V, _ in frames)],
                extent=L, scalar_range=R, all_enumerated=len(small) == len(frames),
                nu_strict=float(mean[0]),
                bound=dict(epsilon=BOUND_EPS, mean=mean.tolist(), envelope=env.tolist(),
                           frames_positive=[int(np.sum(row > 1e-12)) for row in lower]),
                construction=build, check_saved_sweep=check,
                seconds=dict(bound=t1 - t0, construction=t2 - t1, check=time.perf_counter() - t2))


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for n in sys.argv[1:] or NAMES:
        r = run(n)
        (OUT / f'{n.replace(".", "").lower()}.json').write_text(json.dumps(r, indent=1) + '\n')
        c = {round(100 * b['epsilon'], 1): (round(100 * b['NROE_mean'], 2), round(100 * b['NMLE_max'], 1))
             for b in r['construction'] if b['epsilon'] in LABELLED}
        print(n, f"nu*={100 * r['nu_strict']:.2f}%", 'enum optimal:',
              min(b['enumerated_optimal'] for b in r['construction']), '/', r['construction'][0]['enumerated'],
              'secs', {k: round(v, 1) for k, v in r['seconds'].items()}, c, flush=True)
