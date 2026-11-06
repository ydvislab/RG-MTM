"""Displayed positions of the Tangaroa features for the volumetric figure (2026-11-06).

AnchorMTM (eps = 0 and 10%): rerun of experiments/frontier/run.py for Tangaroa (same inputs, orders, capped QP),
checked against the stored E_pool / E_inf / NMLE_max of figdata/frontier20261027/tangaroa.json.
Native TMTM and ST-MTM: saved anchors (positions_unit / anchors) in the mirror with the lower mean NROE.
Run from the repository root:  .venv/bin/python paper/anchor_full/figure_drafts/volume_positions.py
Output: paper/anchor_full/figdata/volume_maps20261106/tangaroa.json
"""
import importlib.util, json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path.insert(0, str(CODE / 'src'))
spec = importlib.util.spec_from_file_location('frontier_run', CODE / 'experiments/frontier/run.py')
fr = importlib.util.module_from_spec(spec); spec.loader.exec_module(fr)
from rgmtm.order_certificate import budget_order        # noqa: E402
from rgmtm.interval_order import width_order            # noqa: E402
from rgmtm.error_budget import Parameters               # noqa: E402
FIG = ROOT / 'paper/anchor_full/figdata'; n1 = fr.n1
read = lambda p: json.loads(Path(p).read_text())


def main():
    d = n1.DATASETS['Tangaroa'](); R = d['scalar_range']
    p = Parameters(**{k: v for k, v in d['parameters'].items() if k in n1.PARAM_FIELDS}); L = p.canvas
    stored = read(FIG / 'frontier20261027/tangaroa.json')['methods']; out = dict(canvas=L, q=[list(map(float, q)) for q in d['references']], maps={})
    for e in (0, .1):
        orders = []
        for V, q, m in zip(d['merge'], d['references'], d['measures']):
            w = p.width_scale * np.asarray(m, float); pt = budget_order(V, q, L, e * R, n1.TIE * R)
            orders.append(width_order(V, q, w, p, e * R, n1.TIE * R, point=pt))
        rows = n1.capped_sequence(d, orders, R, e, p)
        m = fr.summarize(d, L, R, orders, rows, p); s = stored[f'eps={e:g}']
        for k in ('E_pool', 'E_inf', 'NMLE_max'):
            assert abs(m[k] - s[k]) < 1e-6, (e, k, m[k], s[k])
        out['maps'][f'eps={e:g}'] = dict(x=[list(map(float, r['x'])) for r in rows], delta=[float(r['delta']) / R for r in rows],
                                         E_pool=m['E_pool'], E_inf=m['E_inf'], NMLE_max=m['NMLE_max'])
        print(f'eps={e:g}: E_pool {100*m["E_pool"]:.2f}% E_inf {100*m["E_inf"]:.2f}% (stored match)', flush=True)
    native(out)
    (FIG / 'volume_maps20261106/tangaroa.json').write_text(json.dumps(out) + '\n')


def native(out):
    """Native TMTM / ST-MTM positions on the canvas [o, o + L]: TMTM anchors are sample indices of a column that holds
    every voxel once (length = raster), ST-MTM stores unit positions; each map in the mirror with lower mean displacement."""
    src = CODE / 'results/volume3d/tangaroa-paper-p10-full201'; P = read(src / 'parameters.json')
    o, L = P['canvas_origin'], P['canvas']; out['origin'] = o; ids = [f['leaf_ids'] for f in read(src / 'features.json')['frames']]
    recs = [r for r in read(src / 'frame_metrics.json') if r['method'] == 'TMTM'] + read(CODE / 'results/stmtm_completion20261026/tangaroa/frame_metrics.json')
    qn = [(np.asarray(q, float) - o) / L for q in out['q']]
    for meth in ('TMTM', 'ST-MTM'):
        rs = sorted((r for r in recs if r['method'] == meth), key=lambda r: r['index']); us = []
        for r, leaves in zip(rs, ids):
            a = np.asarray(r['positions_unit'], float) if 'positions_unit' in r else np.asarray(r['anchors'], float) / (r['raster'] - 1)
            assert len(a) == len(leaves) and a.min() >= 0 and a.max() <= 1; us.append(a)
        e0 = np.mean(np.concatenate([np.abs(u - q) for u, q in zip(us, qn)])); e1 = np.mean(np.concatenate([np.abs(1 - u - q) for u, q in zip(us, qn)]))
        flip = e1 < e0; us = [1 - u if flip else u for u in us]
        out['maps'][meth] = dict(x=[list(map(float, o + u * L)) for u in us], mirrored=bool(flip), E_pool=float(min(e0, e1)))
        print(meth, 'mirrored' if flip else 'as stored', f'mean |u-q| {100*min(e0, e1):.2f}%', flush=True)


if __name__ == '__main__':
    if sys.argv[1:] == ['native']:   # refresh the native entries only
        path = FIG / 'volume_maps20261106/tangaroa.json'; out = read(path); native(out); path.write_text(json.dumps(out) + '\n')
    else:
        main()
