"""Displayed feature positions on Tangaroa and Cylinder for the v21 3D gallery (2026-11-08).

AnchorMTM, eps in {0, 2, 5, 10, 20}%: rerun of experiments/frontier/run.py (width-aware orders + capped QP, default
configuration), checked against the stored E_pool / E_inf / NMLE_max of figdata/frontier20261027/<name>.json, which equal
the collaborator's volumetric budget sweep (paper/pvis2027/budget_tradeoff_20261105/volume_curve_metrics.csv).
Native TMTM and ST-MTM: saved anchors of the implementations of the published methods on the same features
(TMTM: results/volume3d/... and results/paper1_suite/...; ST-MTM: results/stmtm_completion20261026/...), each in the
global mirror with the lower mean displacement (protocol of notes/2026-11-06-orientation.md).
Run from the repository root:  .venv/bin/python paper/anchor_full/figure_drafts/volume_gallery_data.py [Tangaroa Cylinder]
Output: paper/anchor_full/figdata/volume_gallery20261108/<name>.json
"""
import importlib.util, json, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path.insert(0, str(CODE / 'src'))
spec = importlib.util.spec_from_file_location('frontier_run', CODE / 'experiments/frontier/run.py')
fr = importlib.util.module_from_spec(spec); spec.loader.exec_module(fr)
from rgmtm.order_certificate import budget_order        # noqa: E402
from rgmtm.interval_order import width_order            # noqa: E402
from rgmtm.error_budget import Parameters               # noqa: E402
FIG = ROOT / 'paper/anchor_full/figdata'; OUT = FIG / 'volume_gallery20261108'; n1 = fr.n1
read = lambda p: json.loads(Path(p).read_text())
EPS = [0, .02, .05, .1, .2]
SRC = {'Tangaroa': (CODE / 'results/volume3d/tangaroa-paper-p10-full201', CODE / 'results/stmtm_completion20261026/tangaroa'),
       'Cylinder': (CODE / 'results/paper1_suite/square-cylinder3d', CODE / 'results/stmtm_completion20261026/square-cylinder3d')}


def anchor(name):
    d = n1.DATASETS[name](); R = d['scalar_range']
    p = Parameters(**{k: v for k, v in d['parameters'].items() if k in n1.PARAM_FIELDS}); L = p.canvas
    stored = read(FIG / f'frontier20261027/{name.lower()}.json')['methods']
    out = dict(dataset=name, canvas=L, origin=float(p.canvas_origin), q=[list(map(float, q)) for q in d['references']], maps={})
    for e in EPS:
        t0 = time.perf_counter(); orders = []
        for V, q, m in zip(d['merge'], d['references'], d['measures']):
            w = p.width_scale * np.asarray(m, float); pt = budget_order(V, q, L, e * R, n1.TIE * R)
            orders.append(width_order(V, q, w, p, e * R, n1.TIE * R, point=pt))
        rows = n1.capped_sequence(d, orders, R, e, p)
        m = fr.summarize(d, L, R, orders, rows, p); s = stored[f'eps={e:g}']
        for k in ('E_pool', 'E_inf', 'NMLE_max'):
            assert abs(m[k] - s[k]) < 1e-6, (name, e, k, m[k], s[k])
        out['maps'][f'eps={e:g}'] = dict(x=[list(map(float, r['x'])) for r in rows], delta=[float(r['delta']) / R for r in rows],
                                         E_pool=m['E_pool'], E_inf=m['E_inf'], NMLE_max=m['NMLE_max'])
        print(name, f'eps={e:g}: E_pool {100*m["E_pool"]:.2f}% E_inf {100*m["E_inf"]:.2f}% (stored match) {time.perf_counter()-t0:.0f}s', flush=True)
    return out


def native(name, out):
    tm, st = SRC[name]; P = read(tm / 'parameters.json'); o, L = P['canvas_origin'], P['canvas']
    feats = read(tm / 'features.json')['frames']; ids = [f['leaf_ids'] for f in feats]
    qn = [(np.asarray(q, float) - out['origin']) / out['canvas'] for q in out['q']]
    assert abs(o - out['origin']) < 1e-9 and abs(L - out['canvas']) < 1e-9
    T = sorted((r for r in read(tm / 'frame_metrics.json') if r['method'] == 'TMTM'), key=lambda r: r['index'])
    S = sorted(read(st / 'frame_metrics.json'), key=lambda r: r['index'])
    for meth, rows in (('TMTM', T), ('ST-MTM', S)):
        us = []
        for r, leaves in zip(rows, ids):
            if 'positions_unit' in r:
                a = np.asarray(r['positions_unit'], float)
            elif 'raster' in r:
                a = np.asarray(r['anchors'], float) / (r['raster'] - 1)
            else:
                a = (np.asarray(r['positions'], float) - o) / L
            if 'leaf_ids' in r:
                assert list(r['leaf_ids']) == list(leaves), (name, meth, r['index'])
            assert len(a) == len(leaves) and a.min() >= -1e-9 and a.max() <= 1 + 1e-9, (name, meth, r['index'])
            us.append(a)
        e0 = np.mean(np.concatenate([np.abs(u - q) for u, q in zip(us, qn)])); e1 = np.mean(np.concatenate([np.abs(1 - u - q) for u, q in zip(us, qn)]))
        flip = e1 < e0; us = [1 - u if flip else u for u in us]
        worst = float(np.mean([np.max(np.abs(u - q)) for u, q in zip(us, qn)]))
        out['maps'][meth] = dict(x=[list(map(float, o + u * L)) for u in us], mirrored=bool(flip), E_pool=float(min(e0, e1)), mean_worst=worst,
                                 NROE_stored=float(np.mean([r['NROE'] for r in rows])), NMLE_max_stored=float(max(r['NMLE'] for r in rows)))
        print(name, meth, 'mirrored' if flip else 'as stored', f'mean |u-q| {100*min(e0, e1):.2f}%  mean worst {100*worst:.2f}%', flush=True)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or ['Cylinder', 'Tangaroa']:
        out = anchor(name); native(name, out)
        (OUT / f'{name.lower()}.json').write_text(json.dumps(out) + '\n')
