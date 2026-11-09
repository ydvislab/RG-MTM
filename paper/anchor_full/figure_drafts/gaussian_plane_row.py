"""Gaussian row of Fig. 6a: mean order error (NROE) of TMTM and ST-MTM on Gaussian, at zero merge error (2026-11-09).

Gaussian's bound nu* is zero, so its share of error not forced by the tree is 100% and Table 2 of the collaborator's
package gives no magnitude. This script reads the per-frame records of package 01 (real_bounds_per_frame.csv) on the
machine that holds it, finds the columns with the baselines' per-frame order error, and checks them: the columns must
reproduce the shares the paper reports for Ring, Wildfires, Storms and PM2.5 (1 - sum nu* / sum NROE). Only then it
writes ../figdata/plane_her20261109/gaussian.json, which fig6_forced_plane.py draws as the Gaussian row.
Usage (Mac):  python gaussian_plane_row.py [package-01 folder]   then   python fig6_forced_plane.py
"""
import csv, json, os, sys
from pathlib import Path

PKG = Path(sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    'ANCHOR_PKG01', '/Users/yudong/Downloads/老师所需四项材料_20261109/01_七序列下界与AnchorMTM输入'))
OUT = Path(__file__).resolve().parent.parent / 'figdata/plane_her20261109/gaussian.json'
SHARES = {'Ring': (.645, .257), 'Wildfires': (.925, .981), 'Storms': (.910, .830), 'PM25': (.564, .597)}   # TMTM, ST-MTM


def main():
    rows = list(csv.DictReader(open(PKG / 'real_bounds_per_frame.csv', encoding='utf-8')))
    cols = list(rows[0]); print('columns:', cols)
    by = {}
    for r in rows: by.setdefault(r['dataset'], []).append(r)
    print('datasets:', {k: len(v) for k, v in by.items()})
    num = lambda r, c: float(r[c]) if r.get(c) not in (None, '', 'nan') else None
    cand = [c for c in cols if c not in ('dataset', 'frame', 'point_bound') and all(num(r, c) is not None for r in rows[:5])]

    def share(name, c):
        R = by.get(name, []); nu = sum(num(r, 'point_bound') for r in R); e = sum(num(r, c) for r in R)
        return 1 - nu / e if e > 0 else None
    found = {}
    for k, label in ((0, 'TMTM'), (1, 'ST-MTM')):
        for c in cand:
            ok = all(share(n, c) is not None and abs(share(n, c) - s[k]) < .006 for n, s in SHARES.items() if n in by)
            if ok: found[label] = c
    if len(found) < 2 or 'Gaussian' not in by:
        sys.exit(f'No column pair reproduces the reported shares (found {found}). The baselines\' per-frame order error is '
                 f'not in this file; ask for it, or pass the right file. Columns were: {cols}')
    G = by['Gaussian']; mean = lambda c: 100 * sum(num(r, c) for r in G) / len(G)
    out = dict(dataset='Gaussian', frames=len(G), nu_strict=mean('point_bound'), anchor_nroe=mean('point_bound'),
               TMTM=mean(found['TMTM']), **{'ST-MTM': mean(found['ST-MTM'])}, unit='percent of the axis',
               source=f'{PKG.name}/real_bounds_per_frame.csv, columns {found}; shares of the other sequences reproduced')
    OUT.write_text(json.dumps(out, indent=1)); print('wrote', OUT, out)


if __name__ == '__main__':
    main()
