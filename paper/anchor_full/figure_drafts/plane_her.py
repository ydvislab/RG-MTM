"""Position-topology plane on the collaborator's planar sequences (v30, 2026-11-09).

Input: the collaborator's package "老师所需四项材料_20261109/01_七序列下界与AnchorMTM输入": for every frame the merge
matrix V, the references q and the widths w in fixed canvas units, with canvas L and scalar range R (metadata.json).
Same computation as plane_data.py (bound = mean over frames of max(flattened, chain) certificate at allowance
eps*R, suffix-max envelope; construction = budgeted midpoint ordering), without the exhaustive enumeration.
Check: the strict bound at eps = 0 equals the collaborator's point bound (real_bounds_per_frame.csv) frame by frame.
Projection: the reference-sorted order, NROE 0, worst merge error max_t delta*(sorted order) / R.
Run:  python plane_her.py [Ring Wildfires Storms PM25]   ->  ../figdata/plane_her20261109/<name>.json
"""
import importlib.util, json, sys, time, csv
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; CODE = HERE.parents[2] / 'code'
spec = importlib.util.spec_from_file_location('ob_run', CODE / 'experiments/order_budget/run.py')
ob = importlib.util.module_from_spec(spec); spec.loader.exec_module(ob)
from rgmtm.framework import merge_costs
from rgmtm.order_certificate import certificate, chain_certificate, budget_order

PKG = Path('/Users/yudong/Downloads/老师所需四项材料_20261109/01_七序列下界与AnchorMTM输入')
OUT = HERE.parent / 'figdata/plane_her20261109'
BOUND_EPS = sorted({0., 1e-6} | set(np.geomspace(1e-4, 1, 49).tolist()))
LABELLED = [0., .01, .02, .05, .1, .2, .5, 1.]
BUILD_EPS = sorted({0.} | set(np.geomspace(1e-3, 1, 19).tolist()) | set(LABELLED))


def frames(name):
    z = np.load(PKG / name / 'per_frame_inputs.npz', allow_pickle=False); m = json.loads((PKG / name / 'metadata.json').read_text())
    fo, mo, n = z['feature_offsets'], z['matrix_offsets'], z['counts']; out = []
    for t in range(len(n)):
        k = int(n[t]); V = z['V'][mo[t]:mo[t + 1]].reshape(k, k); q = z['q'][fo[t]:fo[t + 1]]
        out.append((np.asarray(V, float), np.asarray(q, float)))
    return out, float(m['parameters']['canvas']), float(m['scalar_range'])


def run(name):
    F, L, R = frames(name); t0 = time.perf_counter()
    lower = np.array([[max(certificate(V, q, L, 2 * e * R), chain_certificate(V, q, L, e * R, 0.)) for V, q in F] for e in BOUND_EPS])
    mean = lower.mean(1); env = np.maximum.accumulate(mean[::-1])[::-1]
    # check against the collaborator's point bound at eps = 0
    key = {'PM25': 'PM25'}.get(name, name)
    with open(PKG / 'real_bounds_per_frame.csv') as f:
        pb = np.array([float(r['point_bound']) for r in csv.DictReader(f) if r['dataset'] == key])
    gap = float(np.max(np.abs(lower[0] - pb))) if len(pb) == len(F) else None
    build = []
    for e in BUILD_EPS:
        rows = [budget_order(V, q, L, e * R, 0.) for V, q in F]
        nroe = np.array([r['nroe'] for r in rows]); delta = np.array([r['delta'] for r in rows]) / R
        assert np.all(delta <= e + 1e-12)
        build.append(dict(epsilon=e, NROE_mean=float(nroe.mean()), NMLE_max=float(delta.max()), frames_used=int(np.sum(delta > 1e-12))))
    proj = [float(merge_costs(np.array([np.argsort(q, kind='stable')]), V)[0]) / R for V, q in F]
    r = dict(dataset=name, frames=len(F), extent=L, scalar_range=R, nu_strict=float(mean[0]), point_bound_check_maxgap=gap,
             bound=dict(epsilon=BOUND_EPS, mean=mean.tolist(), envelope=env.tolist()), construction=build,
             projection=dict(NROE=0., NMLE_max=float(max(proj))), seconds=time.perf_counter() - t0)
    return r


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for n in sys.argv[1:] or ['Ring', 'Wildfires', 'Storms', 'PM25']:
        r = run(n); (OUT / f'{n.lower()}.json').write_text(json.dumps(r) + '\n')
        print(n, f"nu*={100 * r['nu_strict']:.2f}%  check gap {r['point_bound_check_maxgap']}  proj NMLE {100 * r['projection']['NMLE_max']:.1f}%  {r['seconds']:.0f}s",
              {round(100 * b['epsilon'], 1): (round(100 * b['NROE_mean'], 2), round(100 * b['NMLE_max'], 1)) for b in r['construction'] if b['epsilon'] in LABELLED}, flush=True)
