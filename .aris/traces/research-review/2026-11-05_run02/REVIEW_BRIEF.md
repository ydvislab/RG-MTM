# Cross-model review brief (run 2): AnchorMTM paper v6 + supplement v1
PacificVis 2027 Conference Paper Track, double-blind, IEEE VGTC, 9 pages body + up to 2 pages references. Full paper due 2026-11-09 AoE.

## How to work (important)
- Work as ONE reviewer. Do not load or follow any reviewer/academic-paper skill or plugin, do not propose reviewer panels, do not spawn sub-agents, and do not pause for confirmation. Write the review directly.
- Read files yourself; this brief is not evidence. Use read-only commands only. Keep tool use focused: the number audit is already done (below), so do not re-trace numbers except where you doubt a specific one.

## Files
- Manuscript: /Users/yudong/Research/RG-MTM/paper/anchor_full/main.tex (compiled main.pdf, 10 pages; body ends on page 9).
- Supplement: /Users/yudong/Research/RG-MTM/paper/anchor_full/supplement.tex (supplement.pdf). Part A (S1–S8): proofs and implementation; Part B (S9–S16): extra evaluation.
- Number audit done today (every number in abstract, contributions, Sections 5–7 traced to saved records, with six issues A–F and one missing disclosure G already identified and NOT yet fixed in the manuscript): /Users/yudong/Research/RG-MTM/notes/2026-11-05-number-audit.md
- Scope decision: /Users/yudong/Research/RG-MTM/notes/2026-11-04-pacificvis-scope.md (claims are position–topology only; temporal behaviour and relative geometry are measured, not certified; a broader framework is deferred to a journal paper).

## Questions (in priority order)
1. Correctness of the theory: Theorems order, width, chain and the barrier proposition in Section 4.4 of main.tex, with proofs in the supplement (S2–S5). Is each statement true as written, are assumptions stated, is anything claimed (e.g., attainment, "applies to every instance", the interleaving/bottleneck remark in Section 6) stronger than what is proved? Check notation consistency between main text and supplement, including today's change: the paper now reports C_eta at eta = eps0*Delta_F "as nu*" (Section 5.1 Measures, Fig. 4, S16). Is that acceptable or should it get its own symbol?
2. Argument and framing: Does the paper make a coherent case that merge tree maps are one constrained layout problem with TMTM and ST-MTM as instances (Table 1), and that the bounds measure existing maps? Where is the logic weakest? Is the comparison with TMTM/ST-MTM framed fairly (also see disclosure G in the audit note)?
3. Mock PacificVis review: summary, strengths, weaknesses, questions to authors, overall score 1–5 (5 = strong accept) with confidence, best-paper potential, and the single most likely reason for rejection.
4. Presentation: structure of Sections 1–7, redundancy, figure and caption quality at print size, double-blind anonymity (names, repository URLs, acknowledgements, self-citations, PDF metadata), VGTC compliance.
5. Supplement: consistency with the main text; whether each "Supplement Sx" pointer in main.tex lands on the right content.
6. Fix list for the remaining days: text and figure edits within 9 pages, cheap recomputation only, no new experiments. Say which of audit items A–G you agree with and whether the proposed wording is right.

Scope limits: report what is actually wrong; do not propose new user studies or large experiments before the deadline (list them under "journal version"); do not propose provenance/hash machinery; say plainly when something is correct; do not manufacture findings.

## Output format
1. Mock review (question 3).
2. Ranked issues [Critical/Major/Minor] — location — problem — concrete fix (replacement wording where useful).
3. Theory check: one line per theorem/proposition: correct / correct with caveat / incorrect, with the reason.
4. Prioritized TODO for the remaining days (at most 12 items, each with effort).
5. Journal-version items.

## Update (2026-11-05, before this run)

Fixes A–G from the audit note have now been applied to `paper/anchor_full/main.tex`, `main_zh.tex` and `supplement.tex` (commit b85482a; the applied wording is listed at the end of `notes/2026-11-05-number-audit.md`, and the ST-MTM setting paragraph is at the start of supplement S10). Review the manuscript as it is now, and for A–G judge the applied wording rather than the proposals.
