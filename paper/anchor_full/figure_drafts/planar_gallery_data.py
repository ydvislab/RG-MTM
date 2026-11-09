"""Displayed feature positions on the planar bound sequences for the v26 position gallery (2026-11-09).

AnchorMTM, eps in {0, 5, 20}%: rerun of experiments/frontier/run.py (as volume_gallery_data.anchor), checked against the
stored E_pool / E_inf / NMLE_max of figdata/frontier20261027/<name>.json.
Native TMTM and ST-MTM: rerun of the implementations of the published methods (experiments/era5.py run_method, the
pipeline of stmtm_threshold.py, which reproduces the stored per-frame NROE), anchors rescaled to the canvas
(TMTM: x / C; ST-MTM: (x - lo) / (hi - lo) over its displayed span), each in the global mirror with the lower mean
displacement, as for the volumes. Checks: the native orders reproduce the stored per-frame NROE.
Run from the repository root:  .venv/bin/python paper/anchor_full/figure_drafts/planar_gallery_data.py [Wildfires OLR PM2.5 Ring]
Output: paper/anchor_full/figdata/planar_gallery20261109/<name>.json
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import volume_gallery_data as vg            # AnchorMTM rerun (frontier) with checks
import stmtm_threshold as sth               # native pipeline with checks
vg.EPS = [0, .05, .2]
OUT = vg.FIG / 'planar_gallery20261109'


def native(name, out):
    key = sth.KEYS[name]; ds = sth.dataset(key); sc = ds['sc']
    ext = sth.reference_points_from_frames(sc['frames'], sc['ids'], kind='extremum')
    ref = sth.gm.auto_reference(sc, ext, ds['lo'], ds['hi']); qs, extent = ref['qs'], ref['extent']
    S = sth.stored(key); span = ds['native_span']
    px = sth.gm.Parameters(canvas=span, canvas_origin=float(min(ds['lo'][0], 0.)), width_scale=.5 * span / ds['domain_area'],
                           gap=span / 240, extra_budget=span / 120, rho=.5)
    kw = dict(canvas=span, length=ds['nominal'], refine_raster=False, strict_checks=False)
    qA = [np.asarray(q, float) for q in out['q']]; oA, LA = out['origin'], out['canvas']
    qn = [(q - oA) / LA for q in qA]
    # the references of the native pipeline must be the same references, up to the common origin and scale
    qb = [(np.asarray(q, float) - ref['origin']) / extent for q in qs]
    gap = max(float(np.max(np.abs(a - b))) for a, b in zip(qn, qb))
    print(name, 'reference agreement (normalized) max gap %.2e' % gap, flush=True)
    for meth in ('TMTM', 'ST-MTM'):
        t0 = time.perf_counter()
        if meth == 'ST-MTM':
            if ds['name'] == 'ring':
                prm = sth.ep.b2.LayoutParameters.from_preset('ring')
            else:
                prm = sth.ep.b2.LayoutParameters('uniform', float(sth.ep.P.width_scale * sc['areas'][0].sum()), .95, .5, kw['length'], 0,
                                                 min_spacing_delta=.01, optimizer_tolerance=1e-11)
            res = sth.ep.run_method(sc, 'ST-MTM', px, stmtm_parameters=prm, **kw)
        else:
            res = sth.ep.run_method(sc, 'TMTM', px, **kw)
        X = [np.asarray(r['pixel_x'], float) for r in res['rows']]
        lo = min(x.min() for x in X); hi = max(x.max() for x in X)
        us = [(x - lo) / (hi - lo) for x in X] if meth == 'ST-MTM' else [x / span for x in X]
        e = sth.nroe([list(np.argsort(u, kind='stable')) for u in us], qs, extent)
        stored = np.asarray(S['methods'][meth]['per_frame'], float)
        ok = float(np.max(np.minimum(np.abs(e - stored), np.abs(sth.nroe([list(np.argsort(u, kind='stable'))[::-1] for u in us], qs, extent) - stored))))
        e0 = np.mean(np.concatenate([np.abs(u - q) for u, q in zip(us, qn)])); e1 = np.mean(np.concatenate([np.abs(1 - u - q) for u, q in zip(us, qn)]))
        flip = e1 < e0; us = [1 - u if flip else u for u in us]
        out['maps'][meth] = dict(x=[list(map(float, oA + u * LA)) for u in us], mirrored=bool(flip), E_pool=float(min(e0, e1)),
                                 NMLE_max_stored=0., nroe_reproduction_gap=ok)
        print(name, meth, 'mirrored' if flip else 'as computed', f'mean |u-q| {100*min(e0, e1):.2f}%  NROE gap {ok:.1e}  {time.perf_counter()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for n in sys.argv[1:] or ['Wildfires', 'OLR', 'PM2.5', 'Ring']:
        out = vg.anchor(n); native(n, out)
        (OUT / f'{n.lower().replace(".", "")}.json').write_text(json.dumps(out) + '\n')
