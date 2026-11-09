"""Moving within the common model of Eq. 6 on the two volumes (v34, 2026-11-09).

Question: TMTM and ST-MTM are other settings of the common model, so why does the AnchorMTM default lose to ST-MTM on TW
(and on SNS on Tangaroa)? Because the default is a different point of the family, and because a map that follows a 1-D
reference inherits the neighbourhood quality of that reference. This script measures both, on the trees, references,
widths and tracks of the volume rows of Table 1, with the same interval QP (rgmtm.unified.solve_unified_frame):

  reference    x = q: the reference positions themselves (the limit of a map that draws every feature where it is)
  default      (lambda_R, lambda_G, lambda_M, lambda_C) = (4, 1, .5, .1), tau-selected order, cap tau + beta [Table 1, Exact]
  geometry     (0, 1, .5, .1), same order and cap
  uncapped     (0, 1, .5, .1), same order, no position cap
  ST order     (0, 1, .5, .1), no position cap, leaf order of the ST-MTM run, temporal target x_{t-1} as in ST-MTM
  ST-MTM       the stored ST-MTM anchors

All at zero merge error. Weights are the same on both volumes; nothing is tuned. Scores: metrics_n1c.score (SNS, TW k=1, TD, ME).
Run from the repository root:  .venv/bin/python paper/anchor_full/figure_drafts/family_sweep.py [Tangaroa Cylinder]
Output: paper/anchor_full/figdata/family_sweep20261109/<name>.json
"""
import importlib.util, json, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path[:0] = [str(ROOT), str(CODE / 'src'), str(CODE / 'analysis'), str(CODE)]
def module(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
nc = module('metrics_n1c_run', CODE / 'experiments/metrics_n1c/run.py'); n1 = nc.n1
from rgmtm.error_budget import Parameters                       # noqa: E402
from rgmtm.order_certificate import budget_order                # noqa: E402
from rgmtm.interval_order import width_order                    # noqa: E402
from rgmtm.unified import Controls, solve_unified_frame         # noqa: E402
from rgmtm.framework import interval_costs                      # noqa: E402
OUT = ROOT / 'paper/anchor_full/figdata/family_sweep20261109'
KEY = {'Tangaroa': 'tangaroa', 'Cylinder': 'square-cylinder3d'}


def sequence(d, orders, R, p, weights, capped, motion_fraction=1.):
    lr, lg, lm, lc = weights; rows = []
    for t, o in enumerate(orders):
        q = np.asarray(d['references'][t], float); w = p.width_scale * np.asarray(d['measures'][t], float)
        tau = float(interval_costs(np.array([o]), w, q, p)[0])
        prev = prevq = mask = None
        if t:
            old = {k: i for i, k in enumerate(d['tracks'][t - 1])}
            mask = np.array([k in old for k in d['tracks'][t]])
            prev = np.array([rows[-1]['x'][old[k]] if k in old else 0. for k in d['tracks'][t]])
            prevq = np.array([d['references'][t - 1][old[k]] if k in old else 0. for k in d['tracks'][t]])
        c = Controls(topology_budget=n1.TIE, position_budget=(tau + p.extra_budget) / p.canvas if capped else np.inf,
                     reference_weight=lr, geometry_weight=lg, temporal_weight=lm, eccentricity_weight=lc, motion_fraction=motion_fraction)
        rows.append(solve_unified_frame(d['centers'][t], d['measures'][t], d['hierarchies'][t], q, d['merge'][t], R, c, p,
                                        candidate_orders=[o], previous=prev, previous_q=prevq, matched=mask))
    return [r['x'] for r in rows]


REFRESH = False


def run(name):
    d = n1.DATASETS[name](); R = d['scalar_range']
    p = Parameters(**{k: v for k, v in d['parameters'].items() if k in n1.PARAM_FIELDS}); L = p.canvas
    folder, _, occupied = nc.VOLUME[name]; feats = json.loads((CODE / folder / 'features.json').read_text())['frames']
    if name == 'Tangaroa':
        diag = json.loads((CODE / folder / 'reference.json').read_text())['domain_diagonal']
    else:
        c = np.load(ROOT / 'data/real/paper1_suite/square-cylinder3d/coordinates.npz')
        diag = float(np.linalg.norm([np.ptp(c['x']), np.ptp(c['y']), np.ptp(c['z'])]))
    Q = [np.asarray(q, float) for q in d['references']]
    def scored(xs, reflect=False):
        s = nc.score(d, xs, p, feats, float(diag), occupied)
        npe = lambda V: float(np.mean([np.max(np.abs(np.asarray(x) - q)) / L for x, q in zip(V, Q)]))
        # as in Table 1, an axis with no direction of its own (ST-MTM order) is reflected once in its favour
        s['NPE'] = min(npe(xs), npe([2 * p.canvas_origin + L - np.asarray(x) for x in xs])) if reflect else npe(xs); return s
    orders = []
    for t, (V, q) in enumerate(zip(d['merge'], d['references']) if not REFRESH else ()):
        w = p.width_scale * np.asarray(d['measures'][t], float)
        orders.append(width_order(V, q, w, p, 0., n1.TIE * R, point=budget_order(V, q, L, 0., n1.TIE * R))['order'])
    nat = json.loads((CODE / f'results/stmtm_completion20261026/{KEY[name]}/landmarks.json').read_text())['positions']['ST-MTM']
    stored = [p.canvas_origin + L * np.asarray(u, float) for u in nat]
    st_orders = [[int(i) for i in np.argsort(np.asarray(u, float), kind='stable')] for u in nat]
    out = dict(dataset=name, frames=len(Q), canvas=L, weights='(lambda_R, lambda_G, lambda_M, lambda_C)', instances={})
    if REFRESH: out = json.loads((OUT / f'{name.lower()}.json').read_text())
    def add(tag, xs):
        out['instances'][tag] = scored(xs, tag in ('ST-MTM', 'ST order')); s = out['instances'][tag]
        print(name, tag, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items() if k in ('SNS', 'TW1', 'TD', 'ME_errors', 'ME_clear', 'NPE')}, flush=True)
    if not REFRESH: add('reference', Q)
    add('ST-MTM', stored)
    for tag, oo, wt, cap, mf in (('default', orders, (4., 1., .5, .1), True, 1.),
                                 ('geometry', orders, (0., 1., .5, .1), True, 1.),
                                 ('uncapped', orders, (0., 1., .5, .1), False, 1.),
                                 ('ST order', st_orders, (0., 1., .5, .1), False, 0.)):
        if REFRESH and tag != 'ST order': continue
        t0 = time.perf_counter()
        try:
            add(tag, sequence(d, oo, R, p, wt, cap, mf))
        except Exception as e:
            out['instances'][tag] = dict(failed=repr(e)); print(name, tag, 'FAILED', repr(e), flush=True)
        print(name, tag, f'{time.perf_counter() - t0:.0f}s', flush=True)
    return out


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    REFRESH = '--refresh-st' in sys.argv     # recompute only the two ST-MTM rows of an existing result
    for name in [a for a in sys.argv[1:] if not a.startswith('--')] or KEY:
        (OUT / f'{name.lower()}.json').write_text(json.dumps(run(name), indent=1) + '\n')
