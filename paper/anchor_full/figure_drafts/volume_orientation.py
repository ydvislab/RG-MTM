"""Global orientation of the native volumetric TMTM and ST-MTM maps (2026-11-06).

NROE compares a map's order with the reference order, so it depends on the global mirror of a native map, which
neither TMTM nor ST-MTM fixes relative to the reference. For Tangaroa and Cylinder this script recomputes the stored
per-frame NROE from the saved anchors (check), then the NROE of the mirrored map, and the share not forced by the
tree, (NROE - nu*) / NROE, with the strict nu* of paper Fig. 4 (figdata/order_budget20261027).

Run from the repository root:  python paper/anchor_full/figure_drafts/volume_orientation.py
Output: paper/anchor_full/figdata/stmtm_threshold20261106/volume_orientation.json. Reads saved results only.
"""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'; FIG = ROOT / 'paper/anchor_full/figdata'
read = lambda p: json.loads(Path(p).read_text())
SETS = {
    'Tangaroa': ('results/volume3d/tangaroa-paper-p10-full201', 'results/stmtm_completion20261026/tangaroa',
                 lambda src, f, t: read(src / 'reference.json')['qs'][t]),
    'Cylinder': ('results/paper1_suite/square-cylinder3d', 'results/stmtm_completion20261026/square-cylinder3d',
                 lambda src, f, t: np.asarray(f['extrema'])[:, 0]),
}


def order_error(order, q, extent):
    x = np.asarray(q, float)[list(order)]
    return max(0., float(np.max(np.maximum.accumulate(x) - x))) / (2 * extent) if len(x) else 0.


def main():
    out = {}
    for name, (src, st, ref) in SETS.items():
        src, st = CODE / src, CODE / st; feats = read(src / 'features.json')['frames']; L = read(src / 'parameters.json')['canvas']
        qs = [np.asarray(ref(src, f, t), float) for t, f in enumerate(feats)]
        strict = read(FIG / f'order_budget20261027/{name.lower()}.json')['nu_tie_sensitivity']['0']
        nu_mean = float(strict if isinstance(strict, (int, float)) else np.mean(strict))
        rows = {}
        recs = [r for r in read(src / 'frame_metrics.json') if r['method'] == 'TMTM'] + read(st / 'frame_metrics.json')
        for method in ('TMTM', 'ST-MTM'):
            rs = sorted((r for r in recs if r['method'] == method), key=lambda r: r['index'])
            e, e_rev, gap = [], [], 0.
            for r, q in zip(rs, qs):
                x = np.asarray(r['anchors'], float)
                assert len(x) == len(q), f'{name} {method} frame {r["index"]}: {len(x)} anchors vs {len(q)} references'
                o = list(np.argsort(x, kind='stable')); a = order_error(o, q, L)
                gap = max(gap, abs(a - r['NROE'])); e.append(a); e_rev.append(order_error(o[::-1], q, L))
            e, e_rev = np.asarray(e), np.asarray(e_rev)
            share = lambda v: float((v.mean() - nu_mean) / v.mean())
            rows[method] = dict(NROE_mean=float(e.mean()), NROE_mean_reversed=float(e_rev.mean()), not_forced_share=share(e),
                                not_forced_share_reversed=share(e_rev), reproduction_max_gap=gap, frames=len(e))
            print(f'{name:9s} {method:6s} NROE {100 * e.mean():.2f}% ({100 * share(e):.0f}%)  reversed {100 * e_rev.mean():.2f}% '
                  f'({100 * share(e_rev):.0f}%)  stored-vs-recomputed max gap {gap:.2e}', flush=True)
        out[name] = dict(nu_strict_mean=nu_mean, extent=L, methods=rows)
    path = FIG / 'stmtm_threshold20261106/volume_orientation.json'; path.write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
