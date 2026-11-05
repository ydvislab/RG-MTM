"""OLR: Hovmoller diagram vs AnchorMTM (Exact Mode) on the same reference axis.

Both displays reduce each 2-D frame to a 1-D profile along the same reference and stack the profiles in time.
  Hovmoller (along the reference): average the field over lines perpendicular to the reference direction.
  AnchorMTM, eps = 0: merge-tree profile anchored to the reference (rendered map cached at upstream 91e1fb8).
The reference is the stored one: auto direction a (171 deg, roughly east -> west), q = a . p, canvas = projection
range of the domain corners (code/analysis/general_method.py: auto_reference).

Step 1 (needs the collaborator's code and the OLR file shipped in data/RG-MTM-public-scalar):
    cd <repo> && PYTHONPATH=code/src:code/analysis:code .venv/bin/python paper/anchor_full/figure_drafts/make_olr_hovmoller.py cache
Step 2 (numpy + matplotlib only):
    python make_olr_hovmoller.py
"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]; RES = HERE.parent / 'figdata'
CACHE = RES / 'olr_hovmoller' / 'olr_hovmoller.npz'
NBINS = 128
T_STAR = 38          # a frame in which two minima share a reference position but lie far apart across it
LEAFC = ['#D55E00', '#E69F00', '#5E3C99', '#B2ABD2', '#56B4E9', '#009E73', '#F0E442', '#000000']
plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'pdf.fonttype': 42, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.linewidth': .6, 'axes.titlesize': 7, 'axes.titleweight': 'bold',
                     'mathtext.fontset': 'dejavusans'})


def build_cache():
    import public_scalar
    D = public_scalar.olr(); sc = D['sc']; C = np.asarray(sc['coords'], float); F = np.asarray(sc['fields'], float)
    U = json.loads((ROOT / 'code/results/unified20261025/olr.json').read_text())['reference']
    a = np.array(U['candidates']['direction']['a']); o, L = U['origin'], U['extent']
    ids = [list(map(int, x)) for x in sc['ids']]
    for t in range(len(ids)):                                    # the stored references are reproduced exactly
        assert np.allclose(C[ids[t]] @ a, U['qs'][t])
    # Average along each line perpendicular to the reference (bilinear samples every 0.5 grid units inside the domain);
    # binning grid points directly aliases, because the bins would be narrower than the grid spacing.
    from scipy.interpolate import RegularGridInterpolator
    xs = np.unique(np.round(C[:, 0], 9)); ys = np.unique(np.round(C[:, 1], 9)); perp = np.array([-a[1], a[0]])
    assert len(xs) * len(ys) == len(C) and np.allclose(C[:len(xs), 0], xs)
    S = np.arange(-250, 250, .5); H = np.full((NBINS, len(F)), np.nan)
    for k, uu in enumerate((np.arange(NBINS) + .5) / NBINS):
        pts = (o + uu * L) * a[None, :] + S[:, None] * perp[None, :]
        pts = pts[(pts[:, 0] >= xs[0]) & (pts[:, 0] <= xs[-1]) & (pts[:, 1] >= ys[0]) & (pts[:, 1] <= ys[-1])]
        if len(pts) < 2: continue
        for t, f in enumerate(F):
            H[k, t] = RegularGridInterpolator((ys, xs), f)(pts[:, ::-1]).mean()
    lengths = np.array([len(x) for x in ids]); flat = np.concatenate(ids)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(CACHE, fields=F, coords=C, a=a, origin=o, extent=L, H=H, ids=flat, lengths=lengths,
                        window=np.array([60., 150., -15., 20.]), dates=np.array(sc['dates']))
    print('cache written', CACHE, 'H', H.shape, 'empty bins', int(np.isnan(H).sum()))


def lonlat_ticks(C):
    xs = np.unique(np.round(C[:, 0], 6)); ys = np.unique(np.round(C[:, 1], 6))
    lon = lambda x: 60 + (np.interp(x, xs, np.arange(len(xs))) + .5) * 90 / len(xs)
    R = 6371.; co = np.cos(np.deg2rad(2.5)); by0, by1 = R * np.sin(np.deg2rad(-15)) / co, R * np.sin(np.deg2rad(20)) / co
    lat = lambda y: np.degrees(np.arcsin((by0 + (np.interp(y, ys, np.arange(len(ys))) + .5) / len(ys) * (by1 - by0)) * co / R))
    return xs, ys, lon, lat


def plot():
    Z = np.load(CACHE, allow_pickle=True); F, C, a, o, L, H = Z['fields'], Z['coords'], Z['a'], float(Z['origin']), float(Z['extent']), Z['H']
    starts = np.r_[0, np.cumsum(Z['lengths'])[:-1]]; ids = [Z['ids'][s:s + n] for s, n in zip(starts, Z['lengths'])]
    M = dict(np.load(RES / 'maps20261030/maps_olr.npz'))['ours_0']; qs = json.loads((RES / 'maps20261030/q_olr.json').read_text())
    T = F.shape[0]; t = T_STAR; dates = Z['dates']
    xs, ys, lon, lat = lonlat_ticks(C)
    P = C[ids[t]]; q = (P @ a - o) / L
    assert np.allclose(sorted(q), sorted(qs[t]))
    order = np.argsort(q); lab = {k: chr(65 + r) for r, k in enumerate(order)}

    fig = plt.figure(figsize=(7.0, 4.15))
    g = fig.add_gridspec(2, 1, height_ratios=[1.05, 1], hspace=.42)
    top = g[0].subgridspec(1, 3, width_ratios=[2.15, .62, .62], wspace=.75)
    bot = g[1].subgridspec(1, 5, width_ratios=[1, .035, .2, 1, .035], wspace=.12)

    # (a) one frame
    ax = fig.add_subplot(top[0]); f = F[t]
    ext = [xs[0] - (xs[1] - xs[0]) / 2, xs[-1] + (xs[1] - xs[0]) / 2, ys[0] - (ys[1] - ys[0]) / 2, ys[-1] + (ys[1] - ys[0]) / 2]
    ax.imshow(f, origin='lower', extent=ext, cmap='RdBu_r', vmin=148.2, vmax=307.7, interpolation='nearest')
    perp = np.array([-a[1], a[0]]); cen = C.mean(0)
    for s in np.linspace(-60, 60, 13):                           # lines averaged by the Hovmoller profile
        p0 = cen + s * a - 40 * perp; p1 = cen + s * a + 40 * perp
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], '-', lw=.35, color='k', alpha=.25)
    for k, (px, py) in enumerate(P):
        ax.plot(px, py, 'o', ms=4.5, color=LEAFC[order.tolist().index(k)], mec='k', mew=.5)
        ax.text(px + 1.6, py + .9, lab[k], fontsize=6.6, fontweight='bold')
    c0 = np.array([ext[1] - 18, ext[2] + 5])
    ax.add_patch(FancyArrowPatch(tuple(c0), tuple(c0 + 14 * a), arrowstyle='-|>', mutation_scale=7, lw=1.1, color='k'))
    ax.text(*(c0 + 7 * a + np.array([0, 2.2])), 'reference (171°)', fontsize=5.6, ha='center')
    ax.set_xlim(ext[:2]); ax.set_ylim(ext[2:]); ax.set_aspect('equal')
    xg = np.linspace(xs[0], xs[-1], 400); yg = np.linspace(ys[0], ys[-1], 400)
    ax.set_xticks([xg[np.argmin(abs(lon(xg) - v))] for v in (60, 80, 100, 120, 140)]); ax.set_xticklabels([f'{v}°E' for v in (60, 80, 100, 120, 140)], fontsize=5.4)
    ax.set_yticks([yg[np.argmin(abs(lat(yg) - v))] for v in (-10, 0, 10, 20)]); ax.set_yticklabels(['10°S', '0°', '10°N', '20°N'], fontsize=5.4)
    ax.set_title(f'(a) One frame, {str(dates[t])[:10]}: 2-D field, minima, reference', pad=3)

    # (b) Hovmoller profile and (c) AnchorMTM profile of this frame, on the shared reference axis
    uu = (np.arange(NBINS) + .5) / NBINS; um = (np.arange(M.shape[0]) + .5) / M.shape[0]
    for k, (cell, prof, uax, title, rng) in enumerate([(top[1], H[:, t], uu, '(b) Hovmöller\nprofile', None),
                                                       (top[2], M[:, t], um, '(c) AnchorMTM\nprofile, $\\varepsilon=0$', None)]):
        ax = fig.add_subplot(cell)
        ax.imshow(prof[:, None], origin='lower', extent=[0, .22, 0, 1], aspect='auto', cmap='RdBu_r',
                  vmin=np.nanmin(prof), vmax=np.nanmax(prof), transform=ax.get_yaxis_transform())
        lo, hi = np.nanmin(prof), np.nanmax(prof); xn = .3 + .68 * (prof - lo) / (hi - lo)
        ax.plot(xn, uax, color='k', lw=.8, transform=ax.get_yaxis_transform())
        ylab_ = {}
        for r_, kk in enumerate(order):
            y_ = q[kk]
            if r_ and y_ - ylab_[order[r_ - 1]] < .045: y_ = ylab_[order[r_ - 1]] + .045
            ylab_[kk] = y_
            ax.plot(-.06, q[kk], '>', ms=3.6, color=LEAFC[r_], mec='k', mew=.3, transform=ax.get_yaxis_transform(), clip_on=False)
            ax.text(-.2, y_, lab[kk], fontsize=5.4, ha='center', va='center', transform=ax.get_yaxis_transform())
        note = ('D, E: one position,\naveraged into one dip' if k == 0 else 'D, E: two minima,\nown values kept')
        ax.text(1.02, .9, note, fontsize=4.9, va='center', ha='left', transform=ax.transAxes, color='#333')
        ax.set_ylim(0, 1); ax.set_xlim(0, 1); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
        ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['E', '', 'W'] if k == 0 else []); ax.tick_params(labelsize=5.4, length=2)
        ax.set_title(title, pad=3, fontsize=6.4)
        ax.text(.64, -.05, f'{lo:.0f}–{hi:.0f} W m$^{{-2}}$', fontsize=4.8, ha='center', va='top', transform=ax.transAxes)

    # (d) Hovmoller diagram, (e) AnchorMTM map, both with reference dots and the selected frame
    for k, (img, title, cell, cbcell, ylab) in enumerate([
            (H, 'Hovmöller along the reference (average across it)', bot[0], bot[1], 'position along reference\n(E → W)'),
            (M, r'AnchorMTM, $\varepsilon=0$ (merge tree kept)', bot[3], bot[4], None)]):
        ax = fig.add_subplot(cell)
        im = ax.imshow(img, origin='lower', aspect='auto', cmap='RdBu_r', extent=[-.5, T - .5, 0, 1],
                       vmin=np.nanmin(img), vmax=np.nanmax(img), interpolation='nearest', rasterized=True)
        for tt, qq in enumerate(qs): ax.plot([tt] * len(qq), qq, 'o', ms=1.4, mfc='k', mec='white', mew=.25)
        ax.axvline(t, color='#FFD000', lw=.9)
        ax.set_xticks([0, 29, T - 1]); ax.set_xticklabels([str(dates[i])[5:10] for i in (0, 29, T - 1)], fontsize=5.4)
        ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['E', '', 'W'] if k == 0 else [], fontsize=5.4); ax.tick_params(length=2)
        if ylab: ax.set_ylabel(ylab, fontsize=6)
        ax.set_title(('(d) ' if k == 0 else '(e) ') + title, pad=3, fontsize=6.6)
        for s in ax.spines.values(): s.set_visible(True); s.set_linewidth(.4)
        cb = fig.colorbar(im, cax=fig.add_subplot(cbcell)); cb.ax.tick_params(labelsize=5, length=2)
        cb.formatter = matplotlib.ticker.FormatStrFormatter('%.0f'); cb.update_ticks()
        cb.set_label(r'OLR (W m$^{-2}$)', fontsize=5.6)
    fig.text(.5, .005, 'Both displays reduce each 2-D frame to one profile along the same reference axis and stack the profiles in time. '
             'Dots: reference positions of the minima; yellow line: frame (a).', ha='center', fontsize=5.6)
    for ext_ in ('pdf', 'png'):
        fig.savefig(HERE / f'draft_olr_hovmoller.{ext_}', dpi=220, bbox_inches='tight', pad_inches=.03)
    print('frame', t, str(dates[t])[:10], 'leaves', len(q), 'q', np.round(np.sort(q), 3))


if __name__ == '__main__':
    build_cache() if sys.argv[1:] == ['cache'] else (plot() if sys.argv[1:] != ['paper'] else None)


def paper_figure():
    """Final single-row figure for Section 5.5: Hovmoller and four instances on the same reference axis, one colour scale."""
    Z = np.load(CACHE, allow_pickle=True); H = Z['H']; dates = Z['dates']
    maps = dict(np.load(RES / 'maps20261030/maps_olr.npz')); qs = json.loads((RES / 'maps20261030/q_olr.json').read_text())
    F = json.loads((RES / 'frontier20261027/olr.json').read_text())['methods']
    U = json.loads((ROOT / 'code/results/unified20261025/olr.json').read_text()); L = U['parameters']['canvas']
    def same_model(key):
        e = np.concatenate([np.abs(np.asarray(r['x'], float) - np.asarray(r['reference'], float)) / L for r in U['regimes'][key]['rows']])
        return 100 * e.mean(), 100 * e.max()
    P1 = json.loads((RES / 'olr_hovmoller/checks_p1_p2.json').read_text())['P1']
    cols = [(H, 'Hovmöller', 'average across the reference',
             f"{100 * P1['Hovmoller']['delta=0.02']['fraction']:.0f}% of minima resolved,\n"
             f"{P1['Hovmoller']['delta=0.02']['depth_mean']:.0f} W m$^{{-2}}$ too shallow"),
            (maps['topology_time'], 'TMTM-style objective', r'$\eta=0$, no cap', 'E$_{{pool}}$ {:.1f}%, E$_\\infty$ {:.0f}%'.format(*same_model('topology_time'))),
            (maps['topology_geometry'], 'ST-MTM-style objective', r'$\eta=0$, no cap', 'E$_{{pool}}$ {:.1f}%, E$_\\infty$ {:.0f}%'.format(*same_model('topology_geometry'))),
            (maps['ours_0'], r'AnchorMTM, $\varepsilon=0$', r'$\eta=\varepsilon_0\Delta_F$, cap $\tau+\beta_0$',
             'E$_{{pool}}$ {:.1f}%, E$_\\infty$ {:.0f}%'.format(100 * F['eps=0']['E_pool'], 100 * F['eps=0']['E_inf'])),
            (maps['ours_0.1'], r'AnchorMTM, $\varepsilon=10\%$', r'$\eta=(\varepsilon_0+0.1)\Delta_F$, cap $\tau+\beta_0$',
             'E$_{{pool}}$ {:.1f}%, E$_\\infty$ {:.0f}%'.format(100 * F['eps=0.1']['E_pool'], 100 * F['eps=0.1']['E_inf']))]
    vmin = min(np.nanmin(c[0]) for c in cols); vmax = max(np.nanmax(c[0]) for c in cols)
    fig = plt.figure(figsize=(7.0, 1.72)); g = fig.add_gridspec(1, 6, width_ratios=[1] * 5 + [.05], wspace=.1)
    for k, (img, name, par, note) in enumerate(cols):
        ax = fig.add_subplot(g[k]); T = img.shape[1]
        im = ax.imshow(img, origin='lower', aspect='auto', cmap='RdBu_r', vmin=vmin, vmax=vmax, extent=[-.5, T - .5, 0, 1],
                       interpolation='nearest', rasterized=True)
        for tt, qq in enumerate(qs): ax.plot([tt] * len(qq), qq, 'o', ms=1.1, mfc='k', mec='white', mew=.2)
        ax.set_title(f'{name}\n{par}', fontsize=6.2, pad=2.5, fontweight='normal', linespacing=1.15)
        ax.text(.03, .025, note, transform=ax.transAxes, ha='left', va='bottom', fontsize=5.6,
                bbox=dict(boxstyle='round,pad=.15', fc='white', ec='none', alpha=.88))
        ax.set_xticks([0, T - 1]); ax.set_xticklabels(['1 Jun', '30 Jul'], fontsize=5.8)
        for lab_, ha_ in zip(ax.get_xticklabels(), ('left', 'right')): lab_.set_ha(ha_)
        ax.set_yticks([0, 1] if k == 0 else []); ax.set_yticklabels(['E', 'W'] if k == 0 else [], fontsize=5.8); ax.tick_params(length=1.5, pad=1)
        if k == 0: ax.set_ylabel('reference axis (171°)', fontsize=6, labelpad=1)
        for s in ax.spines.values(): s.set_visible(True); s.set_linewidth(.4)
    cb = fig.colorbar(im, cax=fig.add_subplot(g[5])); cb.ax.tick_params(labelsize=5.8, length=1.5); cb.set_label(r'OLR (W m$^{-2}$)', fontsize=6)
    for ext_ in ('pdf', 'png'):
        fig.savefig(HERE.parent / 'figures' / f'fig_olr_maps.{ext_}', dpi=220, bbox_inches='tight', pad_inches=.02)
    print('fig_olr_maps written')


if __name__ == '__main__' and sys.argv[1:] == ['paper']:
    paper_figure()
