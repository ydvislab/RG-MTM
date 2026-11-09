# v30 source (2026-11-09)

Built on the collaborator's `AnchorMTM_Revised` (upstream d67c9c2, `paper/pvis2027/current`). Decisions: `notes/2026-11-09-v30-figure-decisions.md`.

Changes against her version:
- Header: `[preprint]`, authors shown (single-blind), "Online Submission ID: 1037" (main and supplement).
- Fig. 1: tikz overlay adds the W→E arrow ($a^*$) beside the map; caption rewritten.
- Fig. 2: new panel (d), `figures/anchor_related_work_panel_d.pdf` (script `paper/anchor_full/figure_drafts/fig2_panel_d.py`), same 35-sample field; caption rewritten.
- Fig. 3 (node mapping): caption explains the gap filling that a relaxed order changes.
- Leaf-correspondence figure, controlled four-leaf figure, Ring and PM2.5 figures, parameter tables: removed from the main text; the controlled, Ring and PM2.5 figures are in supplement S8 (leaf correspondence and the tables were already in her supplement).
- Fig. 8 (Storms budget maps): "Improvement 1/2" boxes replaced by a tikz overlay ("Relative geometry + pairwise distances", "Fixed spatial axis + merge budget"); caption rewritten. The edited PPT is `figure_sources/fig10_storms_v30.pptx`.
- Pending data from the collaborator: plane figure on her seven sequences (replaces the budget-response figure), anchored Cylinder phase figure, PM2.5 baselines, raw Storms columns.
Build: `tectonic -X compile main.tex`, `tectonic -X compile supplementary.tex`.

## v32 (2026-11-09)
Decisions and details: `notes/2026-11-09-v32-revisions.md`. Title on one line; Theorems 1-3 and Proposition 1 are now Propositions 1-4 with full proofs in supplement S1; abstract (no number list), introduction (one claim softened) and conclusion rewritten; Fig. 6 is `figures/forced_plane.pdf` (`fig6_forced_plane.py`); Fig. 8 relabelled (`fig7_budget_her.py`, summary data in `anchor_full/figdata/budget_her20261109/`); supplement rewritten without repeating the paper (S1 proofs, S2 construction, S3 protocol, S4 verification, S5 results).

## v33 (2026-11-09)
Two-line title (method and scope); supplement rewritten by paper section (S1-S4, 4 pages) with no repeated text; submission package `paper/1037_v33_submission.zip`. See the v33 part of `notes/2026-11-09-v32-revisions.md`.
