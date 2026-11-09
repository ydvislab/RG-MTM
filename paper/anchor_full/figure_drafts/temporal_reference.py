"""TD and ME of the reference positions themselves (x = q) on the sequences of the metrics_n1c audit (v34, 2026-11-09).

TD sums the displayed motion of matched anchors, so a map that follows real motion has a large TD by construction. The value
for x = q tells how much displayed motion the data themselves imply along the axis. Volumes: see family_sweep.py.
Run from the repository root. Output: paper/anchor_full/figdata/family_sweep20261109/temporal_reference.json
"""
import importlib.util, json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path[:0] = [str(ROOT), str(CODE / 'src'), str(CODE / 'analysis'), str(CODE)]
s = importlib.util.spec_from_file_location('metrics_n1c_run', CODE / 'experiments/metrics_n1c/run.py'); nc = importlib.util.module_from_spec(s); s.loader.exec_module(nc)
from rgmtm.error_budget import Parameters   # noqa: E402
out = {}
for name in nc.PLANAR:
    d = nc.n1.DATASETS[name](); p = Parameters(**{k: v for k, v in d['parameters'].items() if k in nc.n1.PARAM_FIELDS})
    _, _, feats = nc.landmarks(name)
    diag = json.loads((CODE / f'results/metrics_n1c20261027/{name.replace(".", "").lower()}.json').read_text())['diagonal']['value']
    r = nc.score(d, [np.asarray(q, float) for q in d['references']], p, feats, diag, True)
    out[name] = {k: r[k] for k in ('SNS', 'TW1', 'TD', 'ME_errors', 'ME_clear')}; print(name, out[name], flush=True)
(ROOT / 'paper/anchor_full/figdata/family_sweep20261109/temporal_reference.json').write_text(json.dumps(out, indent=1) + '\n')
