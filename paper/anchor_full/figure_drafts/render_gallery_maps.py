"""Rendered scalar maps for the v28 map gallery (2026-11-09).

For a planar bound sequence: AnchorMTM at eps = 0 and 5% (frontier orders + capped QP, as planar_gallery_data.py,
checked against the stored frontier values) rendered with the shared renderer and optimal-barrier filling of
experiments/unified/run.py (render); native TMTM and ST-MTM maps from experiments/era5.py run_method (the
implementations used throughout), each flipped by the global mirror chosen in planar_gallery_data.py.
Also saved: the references q (raw, with origin and extent) and three source-field snapshots.
Run from the repository root:  .venv/bin/python paper/anchor_full/figure_drafts/render_gallery_maps.py [OLR Ring PM2.5]
Output: paper/anchor_full/figdata/map_gallery20261109/<name>.npz
"""
import importlib.util, json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import volume_gallery_data as vg
import stmtm_threshold as sth
from rgmtm.order_certificate import budget_order        # noqa: E402
from rgmtm.interval_order import width_order            # noqa: E402
from rgmtm.error_budget import Parameters               # noqa: E402
spec = importlib.util.spec_from_file_location('unified_run', vg.CODE / 'experiments/unified/run.py')
ur = importlib.util.module_from_spec(spec); spec.loader.exec_module(ur)
n1 = vg.n1; fr = vg.fr
OUT = vg.FIG / 'map_gallery20261109'; PG = vg.FIG / 'planar_gallery20261109'


def run(name):
    t0 = time.perf_counter(); key = sth.KEYS[name]; ds = sth.dataset(key); sc = ds['sc']
    d = n1.DATASETS[name](); R = d['scalar_range']
    p = Parameters(**{k: v for k, v in d['parameters'].items() if k in n1.PARAM_FIELDS}); L = p.canvas
    stored = vg.read(vg.FIG / f'frontier20261027/{name.lower().replace(".", "")}.json')['methods']
    out = dict(q=np.array([np.asarray(q, float) for q in d['references']], dtype=object), origin=float(p.canvas_origin), extent=float(L))
    for e in (0, .05):
        orders = []
        for V, q, m in zip(d['merge'], d['references'], d['measures']):
            w = p.width_scale * np.asarray(m, float); pt = budget_order(V, q, L, e * R, n1.TIE * R)
            orders.append(width_order(V, q, w, p, e * R, n1.TIE * R, point=pt))
        rows = n1.capped_sequence(d, orders, R, e, p)
        m = fr.summarize(d, L, R, orders, rows, p); s = stored[f'eps={e:g}']
        for k in ('E_pool', 'E_inf', 'NMLE_max'):
            assert abs(m[k] - s[k]) < 1e-6, (name, e, k)
        maps, check = ur.render(sc, rows, p, ds['nominal'])
        out[f'eps={e:g}'] = maps; out[f'eps={e:g}_x'] = np.array([np.asarray(r['x'], float) for r in rows], dtype=object)
        print(name, f'eps={e:g} rendered {maps.shape}, raster merge discrepancy {check["max_barrier_discrepancy"]:.2e}', flush=True)
    span = ds['native_span']
    px = sth.gm.Parameters(canvas=span, canvas_origin=float(min(ds['lo'][0], 0.)), width_scale=.5 * span / ds['domain_area'],
                           gap=span / 240, extra_budget=span / 120, rho=.5)
    kw = dict(canvas=span, length=ds['nominal'], refine_raster=False, strict_checks=False)
    mir = json.loads((PG / f'{name.lower().replace(".", "")}.json').read_text())['maps']
    for meth in ('TMTM', 'ST-MTM'):
        if meth == 'ST-MTM':
            prm = sth.ep.b2.LayoutParameters.from_preset('ring') if ds['name'] == 'ring' else sth.ep.b2.LayoutParameters(
                'uniform', float(sth.ep.P.width_scale * sc['areas'][0].sum()), .95, .5, kw['length'], 0, min_spacing_delta=.01, optimizer_tolerance=1e-11)
            res = sth.ep.run_method(sc, 'ST-MTM', px, stmtm_parameters=prm, **kw)
        else:
            res = sth.ep.run_method(sc, 'TMTM', px, **kw)
        M = np.asarray(res['maps'], float)
        if mir[meth]['mirrored']: M = M[::-1, :]
        out[meth] = M; out[meth + '_mirrored'] = mir[meth]['mirrored']
        print(name, meth, 'map', M.shape, 'mirrored' if mir[meth]['mirrored'] else '', flush=True)
    fields = np.asarray(sc['fields'], float); T = fields.shape[0]
    out['snap_t'] = np.array([0, T // 2, T - 1]); out['snaps'] = fields[out['snap_t']]
    out['field_range'] = np.array([np.nanmin(fields), np.nanmax(fields)])
    out['kind'] = sc['trees'][0].kind
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT / f'{name.lower().replace(".", "")}.npz', **out)
    print(name, 'done %.0f s' % (time.perf_counter() - t0), flush=True)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['OLR', 'Ring', 'PM2.5']:
        run(n)
