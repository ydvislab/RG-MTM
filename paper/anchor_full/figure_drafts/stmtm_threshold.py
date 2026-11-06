"""ST-MTM order error across its temporal reordering threshold r (evidence-gap run, 2026-11-06).

ST-MTM keeps the temporally concordant order of a frame unless ordering_cost(OLO) / ordering_cost(concordant) <= r,
in which case it switches to (orientation-aligned) OLO (rgmtm.baselines.stmtm.choose_temporal_order). r = 0 keeps
the concordant order almost always; r = 1 takes OLO on every frame. The paper's protocol uses r = 0.95 on all
sequences; the original ST-MTM paper used 0.65 (storms) and 0.85 (wildfires).

This script uses the references, extent and strict bound of the pipeline that produced the native ST-MTM values of
Fig. 4 (analysis/misreading.py method_positions, analysis/result_tables.py position_metrics) and recomputes ST-MTM's
order sequence for each r with the same functions (experiments/era5.py run_method, ST-MTM branch). Reported per sequence and r: mean NROE and the share not
forced by the tree, (NROE - nu*) / NROE, with nu* the strict exact-topology bound of the same pipeline.

Checks before any number is reported:
  * input fields hash equals code/results/framework20261025/<key>.json;
  * r = 0.95 reproduces the stored per-frame NROE (code/results/final_performance.json) to 1e-9.

Run from the repository root:  python paper/anchor_full/figure_drafts/stmtm_threshold.py [Storms OLR PM2.5 Ring]
Output: paper/anchor_full/figdata/stmtm_threshold20261106/results.json (appended per sequence)
Reads saved inputs only; changes no code, protocol or result of the collaborator.
"""
from dataclasses import replace
import hashlib, json, pickle, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path[:0] = [str(CODE), str(CODE / 'src'), str(CODE / 'analysis')]
import general_method as gm                                     # noqa: E402
from experiments import era5 as ep                              # noqa: E402
from pointcert import tau_pt                                    # noqa: E402
from rgmtm.reference_points import reference_points_from_frames  # noqa: E402

OUT = ROOT / 'paper/anchor_full/figdata/stmtm_threshold20261106'
KEYS = {'Storms': 'era5', 'Wildfires': 'wildfire', 'OLR': 'olr', 'PM2.5': 'pm25_2000', 'Ring': 'ring'}
THRESHOLDS = [0.0, 0.25, 0.5, 0.65, 0.85, 0.95, 1.0]
read = lambda p: json.loads(Path(p).read_text())


def dataset(key):
    if key == 'pm25_2000':
        return pickle.loads((CODE / 'results/pm25_2000/dataset.pkl').read_bytes())
    import replicate
    return replicate.LOADERS[key]()


def stored(key):
    if key == 'pm25_2000':
        d = read(CODE / 'results/pm25_2000/final_performance.json'); return d if 'methods' in d else next(iter(d.values()))
    return read(CODE / 'results/final_performance.json')[key]


def index_order(frame, leaves, order):
    rank = {k: i for i, k in enumerate(leaves)}; return [rank[k] for k in order]


def orders_for(sc, r):
    """ST-MTM's temporal-mode order sequence (experiments/era5.py run_method, ST-MTM branch) for threshold r.

    The order depends on the frames, the matches and r only; anchor positions do not enter it, so the
    position solver (SLSQP) is not run. Returned as index permutations of ids[t].
    """
    out, prev = [], None
    for t, (fr, leaves, m) in enumerate(zip(sc['frames'], sc['ids'], sc['matches'])):
        order = ep.b2.optimal_hierarchical_leaf_order(fr) if t == 0 else ep.b2.choose_temporal_order(fr, prev, m, r)
        prev = order; out.append(index_order(fr, leaves, order))
    return out


def gauge_flip(sc, params):
    """Protocol gauge of run_method (TMTM/ST-MTM): one global flip if frame-0 anchors anti-correlate with centroid x.

    Frame 0 is OLO for every r and its anchors do not depend on r, so the flip is the same for all thresholds.
    """
    fr, leaves = sc['frames'][0], sc['ids'][0]; o = ep.b2.optimal_hierarchical_leaf_order(fr)
    x = np.asarray(ep.b2.project_leaf_anchors(fr, o, params, None), float)[[o.index(k) for k in leaves]]
    c = np.asarray(sc['centers'][0])[:, 0]
    return bool(np.dot(x - x.mean(), c - c.mean()) < 0), x


def nroe(orders, qs, extent):
    return np.array([float(tau_pt([list(o)], q)[0]) / extent for o, q in zip(orders, qs)])


def share(e, nu): return float((e.mean() - nu.mean()) / e.mean()) if e.mean() > 0 else 0.


def run(name):
    key = KEYS[name]; t0 = time.perf_counter(); ds = dataset(key); sc = ds['sc']
    sha = hashlib.sha256(np.asarray(sc['fields'], dtype='<f8').tobytes()).hexdigest()
    assert sha == read(CODE / f'results/framework20261025/{key}.json')['fields_sha256'], f'{name}: input fields differ'
    ext = reference_points_from_frames(sc['frames'], sc['ids'], kind='extremum')
    ref = gm.auto_reference(sc, ext, ds['lo'], ds['hi']); qs, extent = ref['qs'], ref['extent']
    olos = [index_order(fr, leaves, ep.b2.optimal_hierarchical_leaf_order(fr)) for fr, leaves in zip(sc['frames'], sc['ids'])]
    S = stored(key); nu = np.asarray(S['bound_per_frame'], float); ref95 = np.asarray(S['methods']['ST-MTM']['per_frame'], float)
    span = ds['native_span']
    px = gm.Parameters(canvas=span, canvas_origin=float(min(ds['lo'][0], 0.)), width_scale=.5 * span / ds['domain_area'],
                       gap=span / 240, extra_budget=span / 120, rho=.5)
    kw = dict(canvas=span, length=ds['nominal'], refine_raster=False, strict_checks=False)
    if ds['name'] == 'ring':
        base = ep.b2.LayoutParameters.from_preset('ring')
    else:   # the default of run_method, written out so that only r changes
        base = ep.b2.LayoutParameters('uniform', float(ep.P.width_scale * sc['areas'][0].sum()), .95, .5, kw['length'], 0,
                                      min_spacing_delta=.01, optimizer_tolerance=1e-11)
    flip, x0 = gauge_flip(sc, base); rows = {}
    q0 = np.asarray(qs[0], float)
    # Alternative gauge: the same frame-0 rule, but against the reference q instead of centroid x.
    ref_flip = bool(np.dot((-x0 if flip else x0) - (-x0 if flip else x0).mean(), q0 - q0.mean()) < 0)
    for r in THRESHOLDS:
        orders = orders_for(sc, r)
        protocol = [o[::-1] for o in orders] if flip else orders
        e = nroe(protocol, qs, extent); e_rev = nroe([o[::-1] for o in protocol], qs, extent)
        rows[f'{r:g}'] = dict(r=r, NROE_mean=float(e.mean()), not_forced_share=share(e, nu),
                              NROE_mean_reversed=float(e_rev.mean()), not_forced_share_reversed=share(e_rev, nu),
                              reference_gauge_reversed=ref_flip,
                              olo_frames=int(sum(o in (olo, olo[::-1]) for o, olo in zip(orders, olos))), per_frame=e.tolist())
        if abs(r - .95) < 1e-12:
            gap = float(np.max(np.abs(e - ref95)))
            assert gap < 1e-9, f'{name}: r=0.95 does not reproduce the stored ST-MTM NROE (max gap {gap:.3g})'
        v = rows[f'{r:g}']
        print(f"  {name} ST-MTM r={r:g}: NROE {100*v['NROE_mean']:.2f}% ({100*v['not_forced_share']:.1f}% not forced); "
              f"reversed {100*v['NROE_mean_reversed']:.2f}% ({100*v['not_forced_share_reversed']:.1f}%); OLO frames {v['olo_frames']}/{len(orders)}", flush=True)
    # TMTM: native output of the same runner, measured in both global orientations
    tm = ep.run_method(sc, 'TMTM', px, **kw)
    tm_orders = [list(np.argsort(np.asarray(z['pixel_x'], float), kind='stable')) for z in tm['rows']]
    e = nroe(tm_orders, qs, extent); e_rev = nroe([o[::-1] for o in tm_orders], qs, extent)
    tm_stored = np.asarray(S['methods']['TMTM']['per_frame'], float); tm_gap = float(np.max(np.abs(e - tm_stored)))
    assert tm_gap < 1e-9, f'{name}: TMTM does not reproduce the stored NROE (max gap {tm_gap:.3g})'
    x_tm = np.asarray(tm['rows'][0]['pixel_x'], float)
    tm_ref_flip = bool(np.dot(x_tm - x_tm.mean(), q0 - q0.mean()) < 0)
    tmtm = dict(NROE_mean=float(e.mean()), not_forced_share=share(e, nu), NROE_mean_reversed=float(e_rev.mean()),
                not_forced_share_reversed=share(e_rev, nu), reference_gauge_reversed=tm_ref_flip, reproduction_max_gap=tm_gap)
    print(f"  {name} TMTM: NROE {100*e.mean():.2f}% ({100*tmtm['not_forced_share']:.1f}%); reversed {100*e_rev.mean():.2f}% ({100*tmtm['not_forced_share_reversed']:.1f}%); reference gauge reverses: {tm_ref_flip}", flush=True)
    print(f"  {name} ST-MTM reference gauge reverses: {ref_flip}", flush=True)
    return dict(dataset=name, key=key, frames=len(qs), reference_extent=extent, fields_sha256=sha, nu_mean=float(nu.mean()),
                stored_NROE_mean=float(ref95.mean()), reproduction_max_gap=gap, gauge_flip=flip, thresholds=rows, tmtm=tmtm, seconds=time.perf_counter() - t0)


if __name__ == '__main__':
    names = sys.argv[1:] or ['Storms', 'OLR', 'PM2.5', 'Ring']
    OUT.mkdir(parents=True, exist_ok=True); path = OUT / 'results.json'
    res = read(path) if path.exists() else {}
    for n in names:
        res[n] = run(n); path.write_text(json.dumps(res, indent=1) + '\n')
        print(n, 'nu* %.2f%%, stored ST-MTM %.2f%%, %.0f s' % (100 * res[n]['nu_mean'], 100 * res[n]['stored_NROE_mean'], res[n]['seconds']), flush=True)
