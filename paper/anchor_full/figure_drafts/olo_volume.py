"""Optimal leaf ordering (OLO) as a standalone hierarchy-preserving baseline on the volumetric sequences (2026-11-06).

OLO (Bar-Joseph et al. 2001) orders the leaves of each merge tree to minimise the ST-MTM ordering cost; each frame's
OLO is mirrored to agree with the previous frame (rgmtm.baselines.stmtm.choose_temporal_order with r = 1, the same
path that gives the planar OLO values in stmtm_threshold20261106/results.json, thresholds['1']).
Trees are rebuilt from the saved hierarchy (the raw TTK trees are not needed); binary refinement, tracks and
references are those of experiments/stmtm_completion/run.py, checked by reproducing its stored r = 0.95 orders.
NROE depends on the order only; both global mirrors are reported, the paper uses the lower (most favourable) one.

Run from the repository root:  .venv/bin/python paper/anchor_full/figure_drafts/olo_volume.py
Output: paper/anchor_full/figdata/stmtm_threshold20261106/olo_volume.json. Reads saved inputs only.
"""
import json, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path[:0] = [str(CODE), str(CODE / 'src')]
from rgmtm.baselines import stmtm as st                                        # noqa: E402

FIG = ROOT / 'paper/anchor_full/figdata'
read = lambda p: json.loads(Path(p).read_text())
SETS = {'tangaroa': ('volume3d/tangaroa-paper-p10-full201', 'results/stmtm_completion20261026/tangaroa'),
        'square-cylinder3d': ('paper1_suite/square-cylinder3d', 'results/stmtm_completion20261026/square-cylinder3d')}


def order_error(order, q, extent):
    x = np.asarray(q, float)[list(order)]
    return max(0., float(np.max(np.maximum.accumulate(x) - x))) / (2 * extent) if len(x) else 0.


class Light:
    """Binary tree rebuilt from the saved hierarchy (features.json), with the right-chain refinement of
    multifurcations used by experiments/stmtm_completion/run.py Adapter; OLO needs only children and centroids."""
    def __init__(self, rec):
        self.leaves = tuple(rec['leaf_ids']); self.centers = dict(zip(self.leaves, np.asarray(rec['centers'], float)))
        self.children = {v: () for v in self.leaves}; self._next = -1
        self.root = self._build(rec['hierarchy'])

    def _node(self, kids):
        v = self._next; self._next -= 1; self.children[v] = tuple(kids); return v

    def _build(self, h):
        if isinstance(h, int): return self.leaves[h]
        kids = [self._build(c) for c in h]
        if len(kids) == 1: return kids[0]
        tail = self._node(kids[-2:])
        for c in reversed(kids[:-2]): tail = self._node((c, tail))
        return tail

    def leaf_centroid(self, leaf): return self.centers[leaf]


def st_orders(frames, tracks, r):
    orders = []
    for t, frame in enumerate(frames):
        if t:
            prev = dict(zip(tracks[t - 1], frames[t - 1].leaves))
            m = {leaf: prev[i] for leaf, i in zip(frame.leaves, tracks[t]) if i in prev}
            o = st.choose_temporal_order(frame, orders[-1], m, r)
        else:
            o = st.optimal_hierarchical_leaf_order(frame)
        orders.append(tuple(o))
    return orders


def run(key, name):
    folder, stored = SETS[key]; source = CODE / 'results' / folder
    feat = read(source / 'features.json'); features, tracks = feat['frames'], feat['tracks']
    L = read(source / 'parameters.json')['canvas']
    qs = read(source / 'reference.json')['qs'] if key == 'tangaroa' else [np.asarray(f['extrema'])[:, 0] for f in features]
    frames = [Light(f) for f in features]
    # check: r = 0.95 reproduces the stored native ST-MTM order of every frame (up to its one global mirror)
    rec = sorted(read(CODE / stored / 'frame_metrics.json'), key=lambda r: r['index']); same = 0
    for frame, o, r in zip(frames, st_orders(frames, tracks, .95), rec):
        saved = [frame.leaves[i] for i in np.argsort(np.asarray(r['anchors'], float), kind='stable')]
        same += tuple(saved) in (o, o[::-1])
    assert same == len(frames), f'{name}: ST-MTM order reproduced on {same}/{len(frames)} frames'
    t0 = time.perf_counter(); orders = st_orders(frames, tracks, 1.0)
    e, e_rev, opt = [], [], 0
    for frame, o, q in zip(frames, orders, qs):
        rank = {k: i for i, k in enumerate(frame.leaves)}; idx = [rank[k] for k in o]
        e.append(order_error(idx, q, L)); e_rev.append(order_error(idx[::-1], q, L))
        opt += abs(st.ordering_cost(frame, o) - st.ordering_cost(frame, st.optimal_hierarchical_leaf_order(frame))) < 1e-9
    strict = read(FIG / f'order_budget20261027/{name.lower()}.json')['nu_tie_sensitivity']['0']
    nu = float(strict if isinstance(strict, (int, float)) else np.mean(strict))
    e, e_rev = np.asarray(e), np.asarray(e_rev); share = lambda v: float((v.mean() - nu) / v.mean())
    row = dict(frames=len(e), nu_strict_mean=nu, NROE_mean=float(e.mean()), NROE_mean_reversed=float(e_rev.mean()),
               not_forced_share=share(e), not_forced_share_reversed=share(e_rev), min_cost_frames=int(opt),
               stmtm_r095_order_reproduced=same, per_frame=e.tolist(), per_frame_reversed=e_rev.tolist(),
               seconds=time.perf_counter() - t0)
    print(f'{name}: OLO NROE {100*e.mean():.2f}% ({100*share(e):.0f}%), mirrored {100*e_rev.mean():.2f}% '
          f'({100*share(e_rev):.0f}%); min-cost frames {opt}/{len(e)}; nu* {100*nu:.2f}%; ST-MTM check {same}/{len(e)}', flush=True)
    return row


if __name__ == '__main__':
    out = {n: run(k, n) for k, n in [('tangaroa', 'Tangaroa'), ('square-cylinder3d', 'Cylinder')]}
    (FIG / 'stmtm_threshold20261106/olo_volume.json').write_text(json.dumps(out, indent=1) + '\n')
