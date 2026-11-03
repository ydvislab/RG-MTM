# Cross-model review brief: AnchorMTM Sections 5–7 (PacificVis 2027 Conference Track, full paper due 2026-11-09)

You are an expert PacificVis / IEEE VIS reviewer (topology-based visualization, layout optimization). Be critical and concrete.

## Files (read them yourself; do not trust this brief beyond the file contents)
- Manuscript: /Users/yudong/Research/RG-MTM/paper/anchor_full/main.tex
  - Sections 1–4 (Introduction … Certified Position–Topology Bounds) are the collaborator's text of 2026-11-02 and are NOT under review except for consistency.
  - Sections 5 (Experiments), 6 (Discussion and Limitations), 7 (Conclusion) are a new draft and ARE under review.
- Source of every number in Sections 5–7: /Users/yudong/Research/RG-MTM/paper/anchor_full/oct30_main.tex.ref (the collaborator's verified complete version of 2026-10-30, Sections "Evaluation", "Discussion", "Conclusion", plus Table "instances" and paragraph "Cost.").
- Tables: /Users/yudong/Research/RG-MTM/paper/anchor_full/tables/*.tex (tab_volume.tex is included; tab_main.tex / tab_compare.tex are supplement tables with the underlying values).

## Author intent (from the co-author)
The paper should present AnchorMTM as a unified framework (automatic spatial anchoring + single-control topology-budgeted layout + three certified bounds), with existing merge tree maps (TMTM, ST-MTM) as instances of one layout model. Comparison with prior methods is only one part of the evidence; the contribution must not be made to look smaller. Target: an excellent PacificVis paper. Claims must stay honest and traceable.

## Questions
1. Framing: Do Sections 5–7 present a unified framework convincingly, and are they consistent with the contributions and definitions in Sections 1–4 (Exact/Budgeted Mode, ε, Θ0, Theorems 1–3, Algorithm 1, Eq. labels)? Where does the text still read like a "method vs baselines" comparison or understate the contribution?
2. Evidence: For each claim in Sections 5–7, is it supported by the source file? List every number or statement that is NOT traceable to oct30_main.tex.ref / tables, or that is stretched beyond what the source says (overclaims). Check especially the "instances" claim (Table tab:instances, reproduction of TMTM/ST-MTM), "removes this excess", "tight", "data-dependent", and the case-study interpretation of Figure 1.
3. Structure and writing quality at PacificVis level: subsection order, lead sentences, figure/table usage, redundancy, what to cut. The paper has a 9-page limit (+2 pages refs); Sections 1–4 take ~5.1 pages; Sections 5–7 currently have ~2900 words plus 5 figures (3 full-width figure*, 1 full-width overview of ~2/3 page, 1 column) and 3 tables. Estimate whether it fits and what to move to the supplement.
4. Missing pieces a PacificVis reviewer would expect in the evaluation/discussion of such a framework paper (e.g., limitations, generality, design guidance), within what existing results support (no new experiments can be run before 2026-11-09 except cheap recomputation from saved records).

## Output format
- Overall assessment (3–5 sentences) and a score 1–10 for Sections 5–7 as-is.
- Ranked list of issues: [Critical/Major/Minor] location (subsection/paragraph) — problem — concrete fix (give replacement wording where useful).
- A list "Untraceable or overstated claims" with exact quotes.
- Page-budget recommendation.
