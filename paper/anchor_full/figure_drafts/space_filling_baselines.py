"""Hilbert and Morton leaf orders on the five planar benchmark sequences (same inputs as every other map).

Inputs (unchanged, read only):
  code/results/unified20261025/<name>.json          references q, merge matrices V, scalar range, canvas L
  code/results/public_metrics_20261016/<name>_landmarks.npz, code/results/pm25_2000/landmarks.npz
                                                    extremum positions and leaf-support centroids (aligned leaf by leaf)
Each extremum is assigned to its unit cell on the smallest power-of-two square covering all extrema of the
sequence; the curve index of that cell is its display coordinate. Measures, per frame, then averaged:
  NROE   order error of the curve order (Eq. nroe), the same normalization by L as for every other map;
  NMLE*  delta*(pi)/range, the smallest merge error of ANY profile with the curve order (Proposition 1),
         i.e. a lower bound on the merge error of a curve-ordered map (favourable to the curves);
  NPE    worst |x - q| / L per frame with the curve index mapped linearly onto the canvas [min q, min q + L];
  SNS, TW (k = 1) of curve coordinates against support-centroid distances (ST-MTM protocol, as all other maps).
Curves have no canonical orientation on these domains, so every value is the mean over the eight axis-aligned
orientations (dihedral group of the square); min and max over orientations are also stored.
Run: python3 space_filling_baselines.py   (numpy, scipy; imports rgmtm from code/src)
Output: ../figdata/space_filling20261105/metrics.json
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.spatial.distance import pdist, squareform
HERE = Path(__file__).resolve().parent; CODE = HERE.parents[2] / 'code'
sys.path.insert(0, str(CODE / 'src'))
from rgmtm.framework import merge_costs
from rgmtm.order_certificate import order_error
from rgmtm.baselines.space_filling import sample_order
from rgmtm.baselines.stmtm import scale_normalized_stress, trustworthiness

R = CODE / 'results'
SEQ = {'Storms': ('era5', 'public_metrics_20261016/era5_landmarks.npz'),
       'Wildfires': ('wildfire', 'public_metrics_20261016/wildfire_landmarks.npz'),
       'OLR': ('olr', 'public_metrics_20261016/olr_landmarks.npz'),
       'PM2.5': ('pm25_2000', 'pm25_2000/landmarks.npz'),
       'Ring': ('ring', 'public_metrics_20261016/ring_landmarks.npz')}
ORIENT = [(s, f) for s in (False, True) for f in ((0, 0), (1, 0), (0, 1), (1, 1))]   # swap axes, flip x/y


def curve_index(cells, side, curve, orient):
    swap, (fx, fy) = orient; x, y = cells[:, 0].copy(), cells[:, 1].copy()
    if swap: x, y = y, x
    if fx: x = side - 1 - x
    if fy: y = side - 1 - y
    inv = INV[(side, curve)]; return inv[y * side + x]


INV = {}
def inverse(side, curve):
    if (side, curve) not in INV:
        o = sample_order((side, side), curve); v = np.empty(len(o), int); v[o] = np.arange(len(o)); INV[(side, curve)] = v


out = {}
for name, (key, lm) in SEQ.items():
    d = json.loads((R / f'unified20261025/{key}.json').read_text()); fi = d['frame_inputs']
    L = d['parameters']['canvas']; rng = d['scalar_range']
    z = np.load(R / lm, allow_pickle=True); n = z['count']; assert len(n) == len(fi)
    ex = [np.asarray(z['extrema'][t][:n[t]], float) for t in range(len(n))]
    cen = [np.asarray(z['centroids'][t][:n[t]], float) for t in range(len(n))]
    for t in range(len(n)):   # alignment: centroids equal the unified inputs' centers leaf by leaf
        assert np.allclose(cen[t], np.asarray(fi[t]['centers'], float))
    allp = np.concatenate(ex); lo = np.floor(allp.min(0)); ext = np.floor(allp.max(0)) - lo + 1
    side = 1 << int(max(ext) - 1).bit_length(); qmin = min(min(f['reference']) for f in fi)
    res = {}
    for curve in ('Hilbert', 'Morton'):
        inverse(side, curve); per_or = []
        for orient in ORIENT:
            rows = dict(NROE=[], NMLE=[], NPE=[], SNS=[], TW=[])
            for t, f in enumerate(fi):
                q = np.asarray(f['reference'], float); V = np.asarray(f['merge_values'], float)
                cells = (np.floor(ex[t]) - lo).astype(int); idx = curve_index(cells, side, curve, orient)
                order = np.lexsort((np.arange(len(idx)), idx))
                rows['NROE'].append(order_error(order, q, L))
                rows['NMLE'].append(float(merge_costs(order[None], V)[0]) / rng)
                u = qmin + L * idx / (side * side - 1); rows['NPE'].append(float(np.max(np.abs(u - q))) / L)
                if len(q) >= 2 and pdist(cen[t]).any(): rows['SNS'].append(scale_normalized_stress(squareform(pdist(cen[t])), u))
                if 0 < 1 < len(q) / 2: rows['TW'].append(trustworthiness(cen[t], u, 1))
            per_or.append({k: float(np.mean(v)) for k, v in rows.items()} | dict(NMLE_max=float(np.max(rows['NMLE']))))
        res[curve] = {k: dict(mean=float(np.mean([p[k] for p in per_or])), min=float(np.min([p[k] for p in per_or])),
                              max=float(np.max([p[k] for p in per_or]))) for k in per_or[0]}
    res['frames'] = len(fi); res['grid_side'] = side; out[name] = res
    print(name, side, {c: {k: round(100 * v['mean'], 2) if k not in ('SNS', 'TW') else round(v['mean'], 3) for k, v in res[c].items()} for c in ('Hilbert', 'Morton')})
dst = HERE.parent / 'figdata/space_filling20261105'; dst.mkdir(parents=True, exist_ok=True)
(dst / 'metrics.json').write_text(json.dumps(out, indent=1) + '\n')
