"""Rendered Cylinder maps of AnchorMTM (default configuration) for the v29 map figure (2026-11-09).

Orders and anchors: frontier pipeline (volume_gallery_data.anchor; checked against figdata/frontier20261027).
Rendering: the per-frame path of experiments/paper1_suite/run.py (render_sequence on the native grid trees, optimal
barrier filling for a positive budget), with every rendered column checked against the leaf merge matrix
(barrier_matrix) to the budget plus 2e-6.
Native TMTM and ST-MTM display maps: results/paper1_suite/square-cylinder3d and results/stmtm_completion20261026.
Output: figdata/map_gallery20261109/cylinder.npz
"""
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import volume_gallery_data as vg
from rgmtm.reference_guided import render_sequence          # noqa: E402
sys.path.insert(0, str(vg.CODE))
from experiments.paper1_suite.run import Frame as GridFrame  # noqa: E402
from experiments.volume3d.compact_tmtm import barrier_matrix  # noqa: E402
sys.path.insert(0, str(vg.CODE / 'analysis'))
import filling                                               # noqa: E402

RASTER = 4096


def main():
    vg.EPS = [0, .05]; A = vg.anchor('Cylinder'); L, o = A['canvas'], A['origin']
    data = vg.ROOT / 'data/real/paper1_suite/square-cylinder3d'; c = np.load(data / 'coordinates.npz')
    T = len(A['q']); frames = [GridFrame(i, data / 'trees', c['x'], c['y'], c['z'] if 'z' in c else None) for i in range(T)]
    d = vg.n1.DATASETS['Cylinder'](); R = d['scalar_range']
    from rgmtm.error_budget import Parameters
    p = Parameters(**{k: v for k, v in d['parameters'].items() if k in vg.n1.PARAM_FIELDS})
    from rgmtm.order_certificate import budget_order
    from rgmtm.interval_order import width_order
    out = dict(q=np.array([np.asarray(q, float) for q in A['q']], dtype=object), origin=o, extent=L)
    for e in (0, .05):
        orders = []
        for V, q, m in zip(d['merge'], d['references'], d['measures']):
            w = p.width_scale * np.asarray(m, float); pt = budget_order(V, q, L, e * R, vg.n1.TIE * R)
            orders.append(width_order(V, q, w, p, e * R, vg.n1.TIE * R, point=pt))
        rows = vg.n1.capped_sequence(d, orders, R, e, p); cols = []; worst = 0.
        for t, (fr, row) in enumerate(zip(frames, rows)):
            mat, sk, err = render_sequence([fr], [list(fr.leaves)], [row], L, RASTER, canvas_origin=o)
            col = mat[:, 0].astype(float); s = sk[0]
            if e > 0: col, _ = filling.optimal_fill(col, list(s.ordering), s.anchors, fr, 'join')
            anchors = np.asarray(s.anchors)[[s.ordering.index(v) for v in fr.leaves]]
            gap = float(np.max(np.abs(barrier_matrix(col, anchors) - fr.lca_values())))
            worst = max(worst, gap / R); cols.append(col)
        assert worst <= e + 1e-6 + 2e-6, (e, worst)
        out[f'eps={e:g}'] = np.column_stack(cols)
        print(f'Cylinder eps={e:g}: rendered {out[f"eps={e:g}"].shape}, worst rendered merge error {100 * worst:.3f}%', flush=True)
    tm = np.load(vg.CODE / 'results/paper1_suite/square-cylinder3d/display_maps.npz')['TMTM']
    stm = np.load(vg.CODE / 'results/stmtm_completion20261026/square-cylinder3d/display_maps.npz')['ST_MTM']
    G = vg.read(vg.FIG / 'volume_gallery20261108/cylinder.json')['maps']
    out['TMTM'] = tm[::-1] if G['TMTM']['mirrored'] else tm; out['ST-MTM'] = stm[::-1] if G['ST-MTM']['mirrored'] else stm
    out['TMTM_mirrored'] = G['TMTM']['mirrored']; out['ST-MTM_mirrored'] = G['ST-MTM']['mirrored']
    out['kind'] = 'join'
    np.savez_compressed(vg.FIG / 'map_gallery20261109/cylinder.npz', **out); print('saved')


if __name__ == '__main__':
    main()
