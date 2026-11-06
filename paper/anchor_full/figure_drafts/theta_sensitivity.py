"""Sensitivity of the certified orders to the fixed configuration Theta_0 (evidence-gap run, 2026-11-06).

The interval cost tau of an order and the width-aware lower bound depend on Theta_0 only through the width scale s,
the gap g and the anchor slack rho (Eqs. 3-4 and 15-17 of the paper); the QP weights and the cap slack beta_0 move
anchors within the selected order and change neither. This script varies s, g and rho one at a time around the
default of every sequence and reruns the width-aware order search (code/src/rgmtm/interval_order.width_order) at
epsilon = 0 and 10%. Reported per variant: frames whose selected order attains the lower bound, mean tau and mean
bound (percent of L), and frames whose widths and gaps exceed the canvas.

Check: the default variant reproduces frames_at_lower of code/results/order_width20261027 exactly.
Run from the repository root:  python paper/anchor_full/figure_drafts/theta_sensitivity.py [names]
Output: paper/anchor_full/figdata/theta_sensitivity20261106/results.json
Reads saved inputs only (experiments/order_layout DATASETS); changes no code, protocol or result.
"""
from dataclasses import replace
import importlib.util, json, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]; CODE = ROOT / 'code'
sys.path[:0] = [str(CODE), str(CODE / 'src')]
from rgmtm.error_budget import Parameters                       # noqa: E402
from rgmtm.order_certificate import budget_order                # noqa: E402
from rgmtm.interval_order import width_order                    # noqa: E402
spec = importlib.util.spec_from_file_location('order_layout_run', CODE / 'experiments/order_layout/run.py')
n1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(n1)

OUT = ROOT / 'paper/anchor_full/figdata/theta_sensitivity20261106'
SAVED = CODE / 'results/order_width20261027'
VARIANTS = [('default', {}), ('s x0.5', {'width_scale': .5}), ('s x2', {'width_scale': 2.}),
            ('g = 0', {'gap': 0.}), ('g x2', {'gap': 2.}), ('rho = 0', {'rho': ('set', 0.)}), ('rho = 1', {'rho': ('set', 1.)})]
EPS = [0, .1]


def variant(p, change):
    kw = {}
    for k, v in change.items():
        kw[k] = v[1] if isinstance(v, tuple) else getattr(p, k) * v
    return replace(p, **kw)


def run(name):
    d = n1.DATASETS[name](); R = d['scalar_range']
    p0 = Parameters(**{k: v for k, v in d['parameters'].items() if k in n1.PARAM_FIELDS}); L = p0.canvas
    saved = json.loads((SAVED / f'{name.replace(".", "").lower()}.json').read_text())['methods']
    out = dict(dataset=name, frames=len(d['references']), defaults=dict(width_scale=p0.width_scale, gap=p0.gap, rho=p0.rho, canvas=L), variants={})
    for label, change in VARIANTS:
        p = variant(p0, change); row = {}
        for e in EPS:
            t0 = time.perf_counter(); tau, low, failed = [], [], 0
            for t, (V, q) in enumerate(zip(d['merge'], d['references'])):
                w = p.width_scale * np.asarray(d['measures'][t], float)
                if w.sum() + p.gap * max(len(w) - 1, 0) > L * (1 + 1e-12):
                    failed += 1; continue
                pt = budget_order(V, q, L, e * R, n1.TIE * R)
                o = width_order(V, q, w, p, e * R, n1.TIE * R, point=pt)
                tau.append(o['tau'] / L); low.append(o['lower'] / L)
            tau, low = np.asarray(tau), np.asarray(low)
            row[f'{e:g}'] = dict(frames_at_lower=int(np.sum(tau <= low + 1e-9)), evaluated=int(len(tau)), capacity_failures=failed,
                                 tau_mean=float(tau.mean()) if len(tau) else None, lower_mean=float(low.mean()) if len(low) else None,
                                 seconds=time.perf_counter() - t0)
            if label == 'default':
                ref = saved[f'width order + cap, eps={e:g}']['frames_at_lower']
                assert row[f'{e:g}']['frames_at_lower'] == ref, f'{name} eps={e:g}: default gives {row[f"{e:g}"]["frames_at_lower"]}, saved {ref}'
        out['variants'][label] = dict(parameters=dict(width_scale=p.width_scale, gap=p.gap, rho=p.rho), results=row)
        r0, r1 = row['0'], row['0.1']
        print(f"  {name:9s} {label:8s} eps=0: {r0['frames_at_lower']}/{r0['evaluated']} at bound (cap fail {r0['capacity_failures']}), "
              f"tau {100 * (r0['tau_mean'] or 0):.2f}%  | eps=10%: {r1['frames_at_lower']}/{r1['evaluated']}", flush=True)
    return out


if __name__ == '__main__':
    names = sys.argv[1:] or list(n1.DATASETS)
    OUT.mkdir(parents=True, exist_ok=True); path = OUT / 'results.json'
    res = json.loads(path.read_text()) if path.exists() else {}
    for n in names:
        res[n] = run(n); path.write_text(json.dumps(res, indent=1) + '\n')
