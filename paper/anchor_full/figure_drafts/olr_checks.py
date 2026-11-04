"""P1 and P2 checks for the PacificVis draft (notes/2026-11-04-pacificvis-scope.md). numpy only.

P1  Feature resolution, OLR, 60 frames. A source minimum is resolved by a profile if the profile has its own local
    minimum within delta of the minimum's reference position (one-to-one, nearest first). delta is fixed in advance
    at 2% and 5% of the canvas. Depth error = profile value at the matched dip minus the source extremum value.
    Profiles: Hovmoller along the reference (figdata/olr_hovmoller) and the AnchorMTM columns (figdata/maps20261030).
P2  Frame-to-frame change of each rendered map, d_t = mean_u |I(t+1,u) - I(t,u)| / scalar range, against the number
    of topological events between t and t+1 (track births + deaths, from code/results/unified20261025 frame inputs).

Run:  python olr_checks.py
"""
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'figdata'; CODE = HERE.parents[2] / 'code' / 'results'
DELTAS = (.02, .05)


def runs_minima(y):
    """Positions (sample indices, plateau centres) of local minima, plateaus counted once; ends included."""
    y = np.asarray(y, float); keep = np.r_[True, np.diff(y) != 0]; starts = np.flatnonzero(keep)
    ends = np.r_[starts[1:] - 1, len(y) - 1]; v = y[starts]; out = []
    for k in range(len(v)):
        left = v[k - 1] if k else np.inf; right = v[k + 1] if k + 1 < len(v) else np.inf
        if v[k] < left and v[k] < right: out.append(((starts[k] + ends[k]) / 2, v[k]))
    return out


def match(u_leaf, dips, n, delta):
    """One-to-one nearest matching of leaves to dips within delta; returns {leaf: dip value}."""
    pairs = sorted((abs(u - (k + .5) / n), i, j) for i, u in enumerate(u_leaf) for j, (k, _) in enumerate(dips)
                   if abs(u - (k + .5) / n) <= delta)
    used_i, used_j, out = set(), set(), {}
    for _, i, j in pairs:
        if i not in used_i and j not in used_j: used_i.add(i); used_j.add(j); out[i] = dips[j][1]
    return out


def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y)); return float(np.corrcoef(rx, ry)[0, 1])


def p1():
    Z = np.load(RES / 'olr_hovmoller/olr_hovmoller.npz', allow_pickle=True)
    F, C, a, o, L, H = Z['fields'], Z['coords'], Z['a'], float(Z['origin']), float(Z['extent']), Z['H']
    starts = np.r_[0, np.cumsum(Z['lengths'])[:-1]]; ids = [Z['ids'][s:s + n] for s, n in zip(starts, Z['lengths'])]
    maps = dict(np.load(RES / 'maps20261030/maps_olr.npz'))
    profiles = {'Hovmoller': H, 'AnchorMTM eps=0': maps['ours_0'], 'AnchorMTM eps=10%': maps['ours_0.1']}
    out = {}
    for name, P in profiles.items():
        n = P.shape[0]; rec = {d: dict(resolved=0, total=0, depth=[]) for d in DELTAS}; dips_vs_leaves = []
        for t in range(F.shape[0]):
            u = (C[ids[t]] @ a - o) / L; v = F[t].ravel()[ids[t]]; dips = runs_minima(P[:, t])
            dips_vs_leaves.append((len(dips), len(u)))
            for d in DELTAS:
                m = match(u, dips, n, d); rec[d]['resolved'] += len(m); rec[d]['total'] += len(u)
                rec[d]['depth'] += [m[i] - v[i] for i in m]
        dl = np.array(dips_vs_leaves)
        out[name] = {f'delta={d:g}': dict(resolved=rec[d]['resolved'], total=rec[d]['total'],
                                          fraction=rec[d]['resolved'] / rec[d]['total'],
                                          depth_mean=float(np.mean(rec[d]['depth'])), depth_median=float(np.median(rec[d]['depth'])),
                                          depth_max=float(np.max(rec[d]['depth']))) for d in DELTAS}
        out[name]['frames_with_fewer_dips_than_minima'] = int(np.sum(dl[:, 0] < dl[:, 1]))
        out[name]['mean_dips_per_frame'] = float(dl[:, 0].mean()); out[name]['mean_minima_per_frame'] = float(dl[:, 1].mean())
    return out


def events(key):
    tr = [set(f['tracks']) for f in json.loads((CODE / f'unified20261025/{key}.json').read_text())['frame_inputs']]
    return np.array([len(tr[t + 1] - tr[t]) + len(tr[t] - tr[t + 1]) for t in range(len(tr) - 1)])


def p2():
    out = {}
    for name, key, fr in [('OLR', 'olr', 'olr'), ('Storms', 'era5', 'storms'), ('Ring', 'ring', 'ring')]:
        R = json.loads((RES / f'frontier20261027/{fr}.json').read_text())['scalar_range']
        maps = dict(np.load(RES / f'maps20261030/maps_{key}.npz')); ev = events(key)
        if key == 'olr': maps['Hovmoller'] = np.load(RES / 'olr_hovmoller/olr_hovmoller.npz')['H']
        res = dict(steps=len(ev), event_steps=int((ev > 0).sum()))
        for m, I in maps.items():
            d = np.nanmean(np.abs(np.diff(I, axis=1)), axis=0) / R
            res[m] = dict(mean=float(d.mean()), no_event=float(d[ev == 0].mean()) if (ev == 0).any() else None,
                          event=float(d[ev > 0].mean()) if (ev > 0).any() else None, spearman_events=spearman(d, ev))
        out[name] = res
    return out


if __name__ == '__main__':
    R = dict(P1=p1(), P2=p2())
    (RES / 'olr_hovmoller/checks_p1_p2.json').write_text(json.dumps(R, indent=1))
    for name, r in R['P1'].items():
        print('P1', name, {k: (round(v['fraction'], 3), round(v['depth_mean'], 1), round(v['depth_median'], 1)) for k, v in r.items() if k.startswith('delta')},
              'fewer-dip frames', r['frames_with_fewer_dips_than_minima'], 'dips/minima', round(r['mean_dips_per_frame'], 2), round(r['mean_minima_per_frame'], 2))
    for name, r in R['P2'].items():
        print('P2', name, 'steps', r['steps'], 'event steps', r['event_steps'])
        for m, v in r.items():
            if isinstance(v, dict): print('   ', f'{m:18s}', {k: (round(x, 4) if isinstance(x, float) else x) for k, x in v.items()})
