"""Most favourable orientation of every compared map (decision 2026-11-06, notes/2026-11-06-orientation.md).

A 1D merge tree map has no intrinsic direction: the global mirror of a TMTM, ST-MTM, TMTM-style or ST-MTM-style map
is an equally optimal output of the same objective, and a space-filling curve has eight axis-aligned orientations.
Errors against the reference depend on that choice, so every compared map is evaluated in the orientation that
agrees better with the reference. The rule only lowers the errors of the compared maps; AnchorMTM has no such
choice because the reference defines its axis.

  native maps (TMTM, ST-MTM):    mirror with the lower mean NROE
      planar: figdata/stmtm_threshold20261106/results.json (r = 0.95 = protocol, TMTM), recomputed from the same
              pipeline and checked against code/results/final_performance.json;
      volumetric: figdata/stmtm_threshold20261106/volume_orientation.json (checked against saved frame metrics).
  same-model layouts (TMTM-style, ST-MTM-style; code/results/unified20261025):
                                 canvas mirror x' = 2 o + L - x with the lower mean displacement E_pool
  space-filling curves (figdata/space_filling20261105, per orientation): orientation with the lowest mean NROE

Run:  python best_mirror.py   ->  ../figdata/orientation20261106/best_mirror.json (summary, printed)
"""
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata'; CODE = HERE.parents[2] / 'code' / 'results'
NAMES = ['Storms', 'Wildfires', 'OLR', 'PM2.5', 'Ring', 'Tangaroa', 'Cylinder']
PLANAR = NAMES[:5]
UNIFIED = {'Storms': 'era5', 'Wildfires': 'wildfire', 'OLR': 'olr', 'PM2.5': 'pm25_2000', 'Ring': 'ring'}
load = lambda p: json.loads(Path(p).read_text())


def native():
    """{sequence: {'TMTM'|'ST-MTM': dict(protocol, reversed, best (percent NROE), mirrored)}}."""
    T = load(RES / 'stmtm_threshold20261106/results.json'); V = load(RES / 'stmtm_threshold20261106/volume_orientation.json'); out = {}
    for n in NAMES:
        if n in PLANAR:
            pairs = {'TMTM': (T[n]['tmtm']['NROE_mean'], T[n]['tmtm']['NROE_mean_reversed']),
                     'ST-MTM': (T[n]['thresholds']['0.95']['NROE_mean'], T[n]['thresholds']['0.95']['NROE_mean_reversed'])}
        else:
            m = V[n]['methods']; pairs = {k: (m[k]['NROE_mean'], m[k]['NROE_mean_reversed']) for k in ('TMTM', 'ST-MTM')}
        out[n] = {k: dict(protocol=100 * a, reversed=100 * b, best=100 * min(a, b), mirrored=bool(b < a)) for k, (a, b) in pairs.items()}
    return out


def mirror(x, origin, L): return 2 * origin + L - np.asarray(x, float)


def same_model_rows(n, key):
    """Rows of a same-model layout in its favourable mirror; returns (rows with 'x' replaced, mirrored, L, origin)."""
    d = load(CODE / f'unified20261025/{UNIFIED[n]}.json'); L = d['parameters']['canvas']; o = d['parameters']['canvas_origin']
    R = d['regimes'][key]['rows']
    pool = lambda xs: float(np.concatenate([np.abs(np.asarray(x, float) - np.asarray(r['reference'], float)) for x, r in zip(xs, R)]).mean())
    xs = [np.asarray(r['x'], float) for r in R]; xm = [mirror(x, o, L) for x in xs]
    flip = pool(xm) < pool(xs)
    rows = [dict(r, x=(m if flip else x).tolist()) for r, x, m in zip(R, xs, xm)]
    return rows, flip, L, o


def same_model(n, key):
    rows, flip, L, o = same_model_rows(n, key)
    dev = [np.abs(np.asarray(r['x'], float) - np.asarray(r['reference'], float)) / L for r in rows]; e = np.concatenate(dev)
    return dict(E_pool=100 * e.mean(), E_inf=100 * e.max(), NPE=100 * float(np.mean([v.max() for v in dev])), mirrored=flip)


def curve(n, c):
    """Space-filling curve values in its orientation with the lowest mean NROE."""
    per = load(RES / 'space_filling20261105/metrics.json')[n][c]['per_orientation']
    return min(per, key=lambda p: p['NROE'])


def summary():
    out = dict(native=native(), same_model={}, curves={})
    for n in PLANAR:
        out['same_model'][n] = {lab: same_model(n, key) for key, lab in (('topology_time', 'TMTM-style'), ('topology_geometry', 'ST-MTM-style'))}
        out['curves'][n] = {c: curve(n, c) for c in ('Hilbert', 'Morton')}
    return out


if __name__ == '__main__':
    S = summary(); dst = RES / 'orientation20261106'; dst.mkdir(parents=True, exist_ok=True)
    (dst / 'best_mirror.json').write_text(json.dumps(S, indent=1) + '\n')
    for n, v in S['native'].items():
        print('native', n, {k: f"{x['protocol']:.2f}->{x['best']:.2f}{' (mirrored)' if x['mirrored'] else ''}" for k, x in v.items()})
    for n, v in S['same_model'].items():
        print('same-model', n, {k: f"E_pool {x['E_pool']:.1f} E_inf {x['E_inf']:.1f} NPE {x['NPE']:.1f}{' (mirrored)' if x['mirrored'] else ''}" for k, x in v.items()})
    for n, v in S['curves'].items():
        print('curves', n, {k: f"NROE {100 * x['NROE']:.2f} NMLE_max {100 * x['NMLE_max']:.1f} swap={x['swap']} flip={x['flip']}" for k, x in v.items()})
