**The core bounds are sound, but the paper needs several substantive corrections before submission.** The most important concern is the interpretation of “avoidable error”: the manuscript mixes strict topology preservation with preservation up to a numerical allowance. I also found a false dominance claim for the width certificate and inconsistencies in the claimed unified formulation.

This assessment uses the current TeX and included tables. **The compiled PDFs are stale:** `main.pdf` lacks the applied A–G corrections, and `supplement.pdf` is 15 pages and lacks the new ST-MTM setting paragraph. The named v6 PDF copies are stale too. My visual assessment therefore concerns the existing layout, not a verified compilation of the current source. No files were modified.

## 1. Mock PacificVis review

**Summary.** AnchorMTM assigns merge-tree-map features targets on a fixed spatial projection and constructs layouts under a merge-level allowance. Its principal technical contributions are an exact point-order bound, a width-aware packing bound, a chain-aware separation bound, and an optimal-barrier construction for a fixed leaf order. Experiments investigate position, topology, motion, and geometry on seven sequences.

**Strengths**

- The position–topology conflict is well motivated and illustrated particularly effectively by the four-leaf example.
- The exact point-order result is elegant: midpoint ordering simultaneously chooses the cheaper orientation for every sibling pair.
- The paper distinguishes point-order error, finite-width placement, and final rendered displacement. These distinctions provide useful diagnostic information.
- The barrier proposition and fixed-order placement analysis give precise guarantees inside an otherwise heuristic construction.
- Evaluation includes controlled examples, volumetric cases, direction sensitivity, exhaustive small-instance checks, and failure modes. Reporting ST-MTM’s geometry advantages improves the balance.
- The scope is appropriate for a conference paper. Temporal behavior and relative geometry are explicitly measured rather than certified.

**Weaknesses**

- The central “54–95% avoidable” result uses a tolerance-relaxed benchmark while the surrounding argument invokes the strict exact-topology theorem. Cylinder materially exposes the difference.
- Equation 6 and Table 1 do not yet establish literal equivalence with the native baseline methods: temporal targets, width decisions, and optimization stages differ.
- The chain width certificate does not always dominate the flattened-tree certificate as claimed.
- The supplement retains contradictory definitions and explanations after the main-text corrections.
- The comparison demonstrates gains for a chosen spatial-reference objective. It does not establish general superiority over methods designed for different spatial and temporal objectives.
- Several figure annotations are too small for comfortable reading at print size.

**Questions to authors**

1. Is the headline improvement available while preserving the original merge matrix exactly, or only after admitting \(\varepsilon_0\Delta_F\)?
2. Which quantities and decisions vary between instances of Equation 6—particularly widths and temporal targets?
3. Are reported width certificates \(C_{w,\eta}\) alone or the maximum of the chain and flattened-tree certificates?
4. Can the supplement clearly separate the implemented RMS motion residual from the event-based ME used in the evaluation?
5. Can claims about native ST-MTM consistently identify the shared-input reimplementation and distinguish it from common-model objective comparisons?

**Overall score: 3/5 — borderline. Confidence: 4/5.**

The technical contribution is credible and potentially acceptance-worthy. The current presentation makes several central claims stronger than the formal definitions support. These are largely repairable using existing results and focused edits.

**Best-paper potential:** Not in its current form. The exact-order result is attractive, but the contribution and evidence need cleaner integration.

**Single most likely reason for rejection:** Reviewers conclude that the headline improvement conflates changing an order under exact topology with relaxing topology, making the comparison appear stronger than it is.

## 2. Ranked issues

### [Critical — submission artifact] Current source and compiled PDFs disagree

**Location:** `main.pdf`, `supplement.pdf`, and the named v6 delivery PDFs.

The inspected `main.pdf` still contains “only 3,” the old exhaustive-optimum claim, and no “untuned” baseline disclosure. Its supplement lacks the ST-MTM setting paragraph. This is direct evidence of stale output, not merely a timestamp discrepancy.

**Fix:** Rebuild both documents from the final source and replace the delivery copies. Then check their actual text and page counts. The existing PDF ends its body on page 9, but that does not certify the current source’s pagination.

### [Major] The numerical-allowance benchmark needs its own symbol and interpretation

**Location:** §5.1 Measures, §5.3, Fig. 4, §6 opening paragraph, abstract/conclusion, S14–S16.

Reporting \(C_{\varepsilon_0\Delta_F}\) “as \(\nu^*\)” is not acceptable here. Theorem 1 defines \(\nu^*(T,q)\) as the strict-tree point-order optimum. The new quantity has a different feasible set, and its attainment is an empirical result rather than a general theorem.

Cylinder is consequential:

- Strict-tree optimum: **12.24%**.
- Attained allowance-dependent bound: **8.01%**.
- The intervening **4.23 percentage points** are released by the allowance, not solely by changing an order while retaining zero merge error.

S16 correctly discloses this, but Fig. 4 and §5.3 still attribute the decomposition to Theorem 1. The discussion’s midpoint-attainment argument cannot be transferred to \(C_\eta\).

**Fix:** Retain \(\nu^*\) exclusively for Theorem 1. Define, for example,

\[
c_0(T,q)=C_{\varepsilon_0\Delta_F}(T,q).
\]

Suggested wording:

> “We report the allowance-dependent certificate \(c_0\). The point-order search attains it on all 917 evaluated frames. It equals the strict-tree optimum \(\nu^*\) except on Cylinder.”

For the headline, choose explicitly:

- **Strict-topology interpretation:** use the strict benchmark. S16 already gives Cylinder’s avoidable shares as 54% for TMTM and 31% for ST-MTM; the combined range becomes **31–95%**.
- **Allowance-dependent interpretation:** retain 54–95%, but say it is avoidable **when permitting merge error up to \(\varepsilon_0\Delta_F\)**. Attribute this to Theorem 3 plus observed attainment.

The latter is defensible, but “without giving up the merge tree” must not describe Cylinder’s allowance-enabled improvement.

### [Major] The chain width certificate does not universally dominate flattening

**Location:** Last sentence following Theorem 3; S4 paragraph beginning “A coarser certificate…”

The stated \(\mathcal P_\eta\) contains internal-node–leaf and internal-node–internal-node pairs. It omits leaf–leaf pairs. Those pairs contribute nothing positive to the point-order bound but can contribute positive packing costs.

A counterexample is:

\[
L=1,\quad q_1=q_2=0.5,\quad W_1=W_2=0.2,\quad
\rho=g=0.
\]

Take a root with two leaf children. There are no eligible pairs in the stated \(\mathcal P_\eta\); the boundary term is zero, so \(C_{w,\eta}=0\). However, the exact-tree—and unchanged flattened-tree—width bound is \(0.1\), attained by centers at \(0.4\) and \(0.6\).

Thus the **lower bound remains valid**, but the claimed dominance is false.

The implementation already uses `max(lower_b, lower_c)` in [interval_order.py](/Users/yudong/Research/RG-MTM/code/src/rgmtm/interval_order.py:161).

**Fix:** Match that implementation:

> “The chain certificate captures accumulated ancestor gaps. We report the maximum of the chain and flattened-tree certificates.”

Define that combined certificate explicitly wherever it is used in evaluation. Alternatively, extend the pair family with all distinct singleton pairs and establish the claimed dominance for the revised definition. The first repair is smaller.

### [Major] The unified formulation is useful, but literal baseline equivalence is overstated

**Location:** §4.1, Equation 6, Table 1, §5.1 Instances.

There are three concrete gaps.

1. **Temporal objective:** \(E_M\) is defined using the reference-displacement target \(x_{\mathrm{prev}}+\Delta q\). Native temporal stabilization is a different target; changing its weight does not change that target.
2. **Widths:** The formulation fixes \(W_i=s\,m_i\), whereas the ST-MTM description includes a width optimization with fixed total extent. With fixed widths, a width-deviation objective cannot reproduce that decision.
3. **Optimization claim:** “Each solves an instance” suggests a common minimization problem, whereas the methods use different staged and heuristic procedures.

The independent order bound does **not** require literal equivalence of all objectives and feasible sets. It applies whenever the required hierarchy and reference assumptions hold.

**Fix:** Present Equation 6 as a common **layout template**, with method-specific width policies, temporal targets, and ordering procedures. Add those policies to Table 1 or explain them briefly in the supplement.

Suggested wording:

> “The methods share a hierarchy-constrained layout representation, but differ in their width policies, temporal targets, ordering procedures, and placement objectives.”

Also replace “reproduces both” with the actual validation:

> “Given the native orders, we validate the TMTM linearization against the official implementation and the implemented ST-MTM quadratic programs through their optimality conditions.”

KKT residuals support correctness of the implemented quadratic solves; they do not establish full reproduction of the original results.

### [Major] Equation 6 constrains the existence of a suitable profile, not the selected profile

**Location:** Equation 6 and the definition of \(\Pi_\eta\).

The optimization variable includes \(\psi_t\), but its constraints only require that the selected order *admits* a budget-feasible profile. That does not force the actual \(\psi_t\) to be such a profile.

The barrier oracle also assumes fixed extremum values, which should be explicit in this formulation.

**Fix:** Add

\[
d_{\rm top}(\psi_t,T_t)\le\eta,\qquad
\psi_t(x_i^t)=V_{ii}^t,
\]

with compatibility between the profile and the selected anchor order. Alternatively, define \(\psi_t\) as the prescribed barrier-based reconstruction rather than a free optimization variable.

### [Major] “Exact Mode” has incompatible definitions

**Location:** §4.3.1, §5.1, abstract, §6; supplement opening configuration paragraph and S8.

Section 4.3.1 defines Exact Mode by \(\eta=0\). Experiments call \(\varepsilon=0\), \(\eta=\varepsilon_0\Delta_F>0\), Exact Mode. The supplement explicitly says that default setting is **not strict Exact Mode**.

This matters because near-tied events can change despite a very small scalar discrepancy.

**Fix:** Define “strict exact” and “default numerical-exact” once, then use them consistently. Reserve “unchanged merge tree” for the cases where zero error was actually measured.

Suggested wording:

> “The default zero-budget setting retains the numerical allowance \(\varepsilon_0\Delta_F\); strict exactness requires \(\eta=0\). On the evaluated planar sequences, the default setting nevertheless has zero measured merge error.”

### [Major] Main-text and supplement metric definitions disagree

**Location:** Supplement opening implementation paragraph; §5.1 Measures; S13 and its resolution table.

- Main-text **ME** is an approach/separation event-error fraction.
- The supplement calls the **RMS reference-motion residual** ME.

These are different quantities and require distinct names.

S13 also still says unresolved map minima are displaced beyond \(\delta\), whereas correction B identifies neighboring-minimum mismatches. Its table caption says “their own profile dip,” despite the proximity matching sometimes selecting another minimum.

Finally, additional Hovmöller dips make the matching permissive, but do not by themselves establish a mathematical “upper bound.”

**Fix:** Rename the implementation residual, explicitly define the evaluation ME, and synchronize S13 with correction B:

> “The proximity score can match a source minimum to another minimum’s dip. We therefore report identity-preserving placement separately.”

Call the Hovmöller measure a **permissive proximity-based resolution score**, unless an upper-bound claim is formally established.

### [Major] Baseline disclosure G is good; interpretation still needs narrowing

**Location:** §5.1, §5.3–5.5, Fig. 4 versus Figs. 5–6, S10.

The applied G disclosure is useful and appropriately explicit. It distinguishes the shared-input reimplementation from original-paper results.

However:

- Fig. 4 compares native outputs under that protocol.
- Figs. 5–6 compare objectives inside the common interval model.

These are different comparisons. The latter’s very large spatial errors should not be presented as native baseline performance.

Also, error relative to a newly imposed physical reference measures a particular capability. It does not make the baselines’ alternative objectives inherently mistaken.

**Fix:** State this distinction directly in §5.1 and retain it in captions:

> “Figure 4 uses native layouts; Figures 5–6 isolate objective choices within the common interval model and do not reproduce native baseline layouts.”

Use “avoidable reference-order error” consistently. Retain the discussion of ST-MTM’s superior geometry scores.

### [Minor] Several interpretive sentences exceed the evidence

**Location:** §§5.2–5.4 and §6.

- Similar gaps at two budgets do not establish whether slack comes from the bound or the search. Both remain possible.
- “A feature that moves … now also moves on the map” is not guaranteed by the capped QP.
- A large improvement at a small budget does not alone distinguish packing-dominated conflict from weak-saddle ordering conflict.
- Persistence thresholds need scalar units: \(2\varepsilon\) is inconsistent with the normalized budget unless explicitly normalized.

**Fix:** Use narrower wording:

> “The remaining gap does not distinguish bound slack from search suboptimality.”

> “The motion term encourages the displayed motion to follow the projected motion.”

Use \(2\eta\), or explicitly state the intended normalized persistence threshold.

### [Minor] Presentation is coherent but crowded

**Location:** Sections 1–7 and Figs. 1–6.

The section sequence works: motivation → representation → construction → bounds → evaluation → interpretation. No major restructuring is needed.

Specific improvements:

- **Fig. 2:** Strongest explanatory figure; retain it.
- **Fig. 3:** The inset and legend are very small; some substantive legend text is approximately 5 pt in the inspected PDF.
- **Fig. 4:** Replace the incorrect Theorem 1 attribution and add the frame aggregation convention.
- **Fig. 5:** Grey comparison-box text is approximately 5.9 pt. Enlarge it or move the detailed numbers to S11.
- **Fig. 6:** The same-model objective labels are helpful. Enlarge displacement annotations and avoid implying exact placement where displacement remains nonzero.
- **Fig. 1:** The normalized “mapped position” axis weakens the geographic message. Add projected-coordinate interpretation rather than treating a tilted projection as literal longitude.

Recover space by shortening repeated assertions about “one formulation,” “one control,” and “bounds independent of the solver” across the introduction, §4 opening, §6, and conclusion.

### [Minor] Anonymity and format are mostly satisfactory, pending final compilation

The inspected main PDF has anonymous author metadata; the supplement’s author metadata is empty. I found no identity-revealing repository link, acknowledgment, or first-person self-citation. The Dong dataset citation is an ordinary third-person reference and is not itself an anonymity violation.

The existing main PDF uses US Letter, VGTC review formatting, and ends the body on page 9. Replace `\onlineid{0}` with the actual submission ID.

The official conference limit is 9+2 pages; the full-paper deadline is November 9, 2026, AoE. The venue permits both single- and double-blind submissions, so double-blind is the chosen submission mode rather than a universal requirement. [Conference call](https://pacificvis2027.github.io/contribute/conference-papers/), [submission guidelines](https://pacificvis2027.github.io/contribute/paper-submission-guidelines/).

**Supplement pointers:** The numbered pointers land correctly: S2–S5 cover the bounds and barriers; S10 comparison values/settings; S11 common-model displacement; S12 Storms; S13 OLR; S14 directions; S15 tracked features; S16 allowance sensitivity. Replace generic supplement references with S6–S8 for implementation and “opening configuration paragraphs” for direction/default conventions.

**Assessment of applied audit fixes A–G**

| Item | Judgment |
|---|---|
| **A** | Agree. “Only 4” is correctly applied in current TeX. |
| **B** | Main-text correction is substantially right. Clarify identity-preserving matching and update S13/table captions. |
| **C** | Agree with the added exceptions. Say “every tested budget” and identify attainment as \(\tau\), not final QP displacement. |
| **D** | Agree. The planar scope and 26.2%/4.2% wording are appropriate. |
| **E** | §5.6 is corrected. The limitations sentence should also explicitly say **point-model search**; adding only “in NROE” leaves its antecedent ambiguous. |
| **F** | Agree. Rounded descriptive wording is appropriate. |
| **G** | Agree. The applied disclosure is good; narrow “reproduces both” and consistently identify common-model comparisons. |

The corrected Storms aggregation wording is good. S12 still uses “steps” where it reports frame-level quantities.

## 3. Theory check

| Statement | Verdict and reason |
|---|---|
| **Theorem 1: exact-topology order bound** | **Correct.** Midpoint ordering chooses the smaller sibling inversion cost; every leaf-pair inversion is covered at its LCA. Attainment is for NROE, not finite-width or rendered placement. |
| **Theorem 2: width-aware bound** | **Correct.** The selected-subset packing and boundary arguments give valid lower bounds; the zero-width/gap limit is \(L\nu^*\). No general attainment is claimed. |
| **Theorem 3: chain-aware bound** | **Correct with caveat.** Separation and the resulting bounds are valid. The following claim of universal dominance over flattened-tree width bounds is incorrect for the stated pair family. |
| **Proposition 1: optimal barriers** | **Correct.** Upper constraints give \(b_k\le C_k+\delta\); choosing these maximal barriers simultaneously tests all lower requirements. Attainment requires the stated fixed-extremum, continuous non-strict model. |
| **S3 fixed-order formula for \(\tau\)** | **Correct.** The monotone slack-variable feasibility argument establishes necessity, sufficiency, and attainment when capacity is feasible. |
| **Interleaving/bottleneck remark** | **Correct with caveat.** Under the stated canonical representation and complete leaf labeling, the matrix discrepancy supports the claimed distance bounds. The conclusion must remain restricted to outputs satisfying those conditions; anchor-matrix error alone does not certify extra unlabeled rendered extrema. This agrees with the cited [labeled merge-tree formulation](https://pmc.ncbi.nlm.nih.gov/articles/PMC7752151/). |
| **“Applies to every instance”** | **Correct conditionally.** Objective independence is valid. The width theorem still requires the stated interval model; the point-order theorem does not require full equivalence with Equation 6. |

## 4. Prioritized TODO before submission

| Priority | Action | Effort |
|---|---|---|
| 1 | Separate \(\nu^*\) from \(c_0\); choose and consistently state the strict or allowance-dependent headline interpretation. | 2–3 h |
| 2 | Correct the chain-versus-flattening dominance claim and identify the combined certificate used by the implementation. | 1 h |
| 3 | Repair Equation 6’s profile constraints and qualify the unified-template claim. | 2–3 h |
| 4 | Make strict exactness and the default numerical allowance consistent throughout both documents. | 1 h |
| 5 | Reconcile ME definitions and repair S13’s matching explanation and table caption. | 1–2 h |
| 6 | Narrow baseline reproduction language and distinguish native-output from common-model comparisons. | 1 h |
| 7 | Finish the residual A–G wording fixes: tested budgets, point-model search, \(\tau\) versus final displacement, frame terminology. | 45 min |
| 8 | Remove unsupported causal interpretations and fix persistence-budget units. | 30–45 min |
| 9 | Enlarge Fig. 3/5/6 annotations; correct Fig. 4’s theorem attribution, symbol, and aggregation description. | 2–3 h |
| 10 | Cut repeated framing sentences to preserve the nine-page body. | 1 h |
| 11 | Rebuild main/supplement and replace all delivery copies; verify corrected phrases, page counts, references, metadata, and submission ID. | 1–2 h |

These changes require no new experimental campaign.

## 5. Journal-version items

- Temporal guarantees and temporal-aware order selection.
- Broader references beyond one fixed projection.
- Stronger or characterized-tight width/budget certificates and scalable order search.
- Sensitivity to matching, direction estimation, and fixed configuration.
- Broader baseline parameter evaluation and reproduction on original inputs where available.
- Analyst evaluation of position, nesting, motion, and changed-barrier interpretation.
- Full rendered-tree certification, including label coverage and strict-extremum effects.