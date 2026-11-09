# Project: RG-MTM (paper collaboration, private fork)

Reference-Guided Merge Tree Maps: certify how far merge-tree features must move from a fixed spatial reference when the hierarchy is kept (positional certificate τ*, hierarchy cost H, conflict triples), and measure the merge-level cost of relaxing it (optimal filling δ*, exact position–topology frontier). Two modes: RG-MTM-P (preserving; historical key `A`) and RG-MTM-R (relaxed, κ=20%; historical key `R 20%`). Compared against TMTM and ST-MTM.

The collaborator (lelewang1109) restarted the project as this repository on 2026-10-08 (first CD-MTM, renamed RG-MTM on 2026-10-16). It absorbed our earlier RA-MTM prototypes (`analysis/` = our former `prototypes/`). The user (GitHub: ydvislab) co-authors the paper. Decision 2026-10-24: **this repository is the working repo**; `~/Research/RA-MTM` (ydvislab/RA-MTM) is the archive of the earlier phase. Comparison with RA-MTM: `notes/2026-10-23-rgmtm-comparison.md`.

## Target venue

PacificVis 2027 **Conference Paper Track**. Abstract **Nov 2, 2026**, full paper **Nov 9, 2026** (verify the time zone on https://pacificvis2027.github.io/). 9 pages + 2 pages of references. Earlier plan and history: `notes/2026-09-26-submission-plan.md`, `notes/2026-09-27-handoff.md`.

## Remotes and sync

- `origin` = `ydvislab/RG-MTM` (**private**). All commits and pushes go here.
- `upstream` = `lelewang1109/RG-MTM` (collaborator, **public**). Fetch/merge only; push is disabled on purpose. Never push or open PRs there unless the user asks. This fork tracks `paper/` and `notes/`, which must never reach the public repo.
- Pull collaborator updates: `git fetch upstream && git merge upstream/main`. A conflict in `.gitignore` is expected: keep our version, which tracks `paper/` and `notes/`.
- The user works from several machines and Claude accounts. Everything needed to resume work must live in tracked files. When a session produces a decision or result, record it in `notes/` and commit + push before ending.

## Where things are

**Layout change (upstream merge 2026-11-03, through `6f0f2dc`):** the collaborator moved `src/`, `analysis/`, `experiments/`, `results/`, `tests/`, `provenance/` under `code/` (e.g. `code/src/rgmtm/`, `code/analysis/`, `code/experiments/`). Read the paths below with that prefix. Their current manuscript is `paper/pvis2027/drafts/method_anchor_figures_updated_en.tex` (identical to our copy in `paper/anchor_full/`), with supplement draft `method_anchor_single_parameter_supplement.tex`. **Our submission draft is now `paper/pvis2027/latex_v21/main.tex`** on branch `paper/submit-1037` (v25 on 2026-11-09; supplement `supplement.tex`, Chinese `main_zh.tex`; PDFs `paper/1037_v25*.pdf`; logic framework `notes/2026-11-09-v25-framework.md`). The older `paper/anchor_full/main.tex` (v12) is superseded. `data/real` is now a tracked upstream directory (metadata only); large inputs still live in `~/Research/RA-MTM/data/real` and must be linked in per file before rerunning. `.venv` needs `pip install -e code` again.

- **Collaborator's material:**
  - `README.md`: overview and reproduction;
  - `publications/`: latest manuscript and supplement **PDFs** (2026-10-16, text-only; the collaborator keeps the LaTeX locally);
  - `experiments/latest/`, `experiments/publication2027/`: run, build and validate;
  - `results/publication2027/`: the active snapshot (`main_comparison.csv`);
  - `results/figures/`: current figures;
  - `experiments/volume3d/`, `results/volume3d/`: 3-D Tangaroa.
- **Code:**
  - `src/rgmtm/`: the collaborator's core, formerly `src/ramtm`;
  - `analysis/`: certificate, frontier, filling, relaxation, datasets and figure scripts (from our RA-MTM `prototypes/`);
  - `analysis/dataset_suite.py`: the six main sequences, 342 frames.
- **Ours (copied from RA-MTM on 2026-10-24):**
  - `paper/pacificvis2027/`: our LaTeX manuscript "How Faithful Can a Hierarchy-Constrained 1-D Layout Be?", with 8 figures; Overleaf zip in `paper/pacificvis2027_overleaf.zip`;
  - `paper/proofs.tex`: supplement proofs;
  - `paper/translation_zh.md`, `paper/plain_zh.md`: Chinese versions;
  - `notes/`: decisions, reviews, progress notes;
  - `.aris/traces/`: Codex review traces.
  - Our old script paths `prototypes/X.py` now correspond to `analysis/X.py`. Check before rerunning, because the collaborator modified some of them.

## Not in git (per machine)

- `data/real` is git-ignored. On the office machine it is a symlink to `~/Research/RA-MTM/data/real`. On a fresh machine, fetch the inputs:
  - **ERA5** (public ARCO mirror; SHA-256 listed in `data/README.md`):
    ```bash
    PYTHONPATH=src python analysis/era5_arco_expanded.py 1999-11-17T00 2000-01-15T00 data/real/ERA5_MSLP/ERA5_MSLP_19991117_20000114_12h_arco_expanded.nc
    ```
    This needs `xarray zarr gcsfs`.
  - **Wildfire**: `https://zenodo.org/records/11234747/files/wildfire.json` → `data/real/wildfire/`.
  - **OLR**: `python3 tools/fetch_public_scalar.py olr`.
  - **PM2.5**: `tools/prepare_cn_pm25.py`; the source is DOI 10.57760/sciencedb.35623 and needs a manual download.
  - **Tangaroa 3-D**: see `experiments/volume3d/README.md`.
- Reference PDFs go in `references/pdf/` (ignored). Hashes are in `references/provenance.json`.
- `.venv/`: `python3 -m venv .venv && .venv/bin/python -m pip install -e . xarray zarr gcsfs`. Tests: `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q`.

## Conventions

- The user writes in Chinese; notes and docs are in Chinese, code and paper text in English.
- Do not change the collaborator's code, protocol parameters, or saved results without discussing it first. They are hash-audited (`experiments/publication2027/validate.py`, `experiments/latest/manifest.json`).
- Keep claims honest and list limitations. User requirement: improvements must be general, with no per-dataset parameters or hand-picked references.
