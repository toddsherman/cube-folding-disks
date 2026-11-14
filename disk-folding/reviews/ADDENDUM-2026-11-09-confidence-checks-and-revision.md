# Addendum, 9 November 2026: confidence checks of 7 November and the revision of 9 November

Date: 9 November 2026. This file qualifies the review records in this folder after the six confidence checks of 7 November 2026 and the manuscript revision of 9 November 2026. It edits no record and is not a new review. Each record keeps the text and hashes it was written with; read it together with its entry in Section 2 below. The records of the checks and of the revision are in `publication/disk-folding-checks/`, which lies outside this package; this file is the package's summary of them.

**Review status.** The review records in this folder were written by AI agents in the preparation workflow (see "Provenance and AI assistance" in `README.md`). The checks of 7 November, and the drafting, verification and review of the 9 November edits, were also done by AI agents. **No human has reviewed the 7 November text or the 9 November text** (Section 4).

## 1. Records, reviewed hashes and current hashes

Current hashes were computed with `shasum -a 256` on 9 November 2026, after the revision, the review fixes and the rendering fixes described in Section 3.2 of this addendum, and agreed then with `build/build-record.json`. The 7 November hashes are those of the text the six confidence checks examined: the sections as revised on 7 November, from which the PDF `25684f7e…` was built. That text is preserved in `publication/disk-folding-snapshot-pre-confidence-edits-2026-11-09.tar.gz`.

| File | SHA-256 on 9 November 2026 |
|---|---|
| `sections/00-introduction.md` | `ace1642a868eee4ac1a8b329b3087aeb28e34869a0dea3e5119ddf01232429aa` |
| `sections/01-model-and-realization.md` | `00d2796a119bc6e26177207ed17f4d517dd7c8a85cedf8773c55ba337a110474` |
| `sections/02-crease-reduction.md` | `c5beb68335ba7f048d2cfcf077b463c1f41fa9aae0f7877abafbed88807945b3` |
| `sections/03-finite-certificate.md` | `027a264f25c54349ea111fbd735f3537b470e3adc288970c084e581ccb65ad97` |
| `sections/04-layer-construction.md` | `fd964ee2c1b1305f05ab4ad8f25f329f9bf23a6f0423b75cbf9c3833e58c587c` |
| `sections/05-main-theorem.md` | `5601339f5f467197641f1c3535226ab7080b359ca4e67e8b8d24eda421abba07` |
| `sections/06-counterexample.md` | `3ff203415ca2a9c6b9813e9541b707d141ac08ec583ab8122cce3c8f3c13cfff` |
| `sections/07-references.md` | `3e96b86db90f57d374b46a4a3e0b27851f076f6636fb6345b16551424104b185` |
| `literature/theorem-comparison.md` | `6c1c6e946a5f64999883e0134b0d27fc287bcced5d3044f06e22862db29559af` |

The PDF built from the revised sections is `1d5b1ff5…` (38 pages; SHA-256 `1d5b1ff57b09ca76af0a7e65241c0e4890386d53d920a442e28412f0980c0df5`). Line numbers given below for `sections/` refer to the files with the hashes in this table. If a section changes after this addendum, its hash here no longer agrees, and the line references for that section must be rechecked.

A record is **current** for a file when the hash it reviewed still matches, **lapsed** when the file has changed since (its findings may still be right, but they do not cover the current text), and **superseded** when the text it reviewed was replaced and some of its conclusions are withdrawn.

| Record | File | Reviewed | 7 November | 9 November (current) | Status |
|---|---|---|---|---|---|
| `foundations-referee.md` (5 Nov) | `sections/02-crease-reduction.md` | `e39ed6fe…` | `2cb8673c…` | `c5beb683…` | lapsed on 7 Nov (R1 wording edit) and again on 9 Nov |
| | `sections/03-finite-certificate.md` | `6d28c702…`; follow-up `b8323559…` | `b8323559…` | `027a264f…` | lapsed on 9 Nov |
| `layer-referee.md` (5 Nov) | `sections/04-layer-construction.md` | `dc1335b3…` | `40d991c7…` | `fd964ee2…` | superseded (§4.2 replaced on 7 Nov; §4 revised on 9 Nov) |
| `construction-author-check.md` (undated; in the 5 Nov release) | `sections/04-layer-construction.md` | no hash recorded; it describes the Hong–Nagamochi version of §4.2 | `40d991c7…` | `fd964ee2…` | superseded |
| `literature-referee.md` (5 Nov) | `literature/theorem-comparison.md` | `3129f71a…` | `b19b41b2…` | `6c1c6e94…` | lapsed on 7 Nov |
| | `sections/00-introduction.md` | `f95ab82f…` | `1980d54f…` | `ace1642a…` | lapsed on 7 Nov |
| | `sections/05-main-theorem.md` | `d892bc45…` | `d892bc45…` | `5601339f…` | lapsed on 9 Nov |
| | `sections/07-references.md` | `d911a913…` | `934cd12d…` | `3e96b86d…` | lapsed on 7 Nov; its Hong–Nagamochi check superseded |
| | `research/jocg-2025.txt` | `509dc2c0…` | `509dc2c0…` | `509dc2c0…` | current |
| `topology-referee.md` (undated) | `sections/01-model-and-realization.md` | `96e12108…` | `96e12108…` | `00d2796a…` | lapsed on 9 Nov |
| | `sections/06-counterexample.md` | `7a9875f0…` | `7a9875f0…` | `3ff20341…` | lapsed on 9 Nov |
| | `sections/05-main-theorem.md` (its line 50) | `d892bc45…` | `d892bc45…` | `5601339f…` | lapsed on 9 Nov |
| | `examples/verify_counterexample.py`, `examples/counterexample.json` | `d0b6f7e4…`, `c4c6523c…` | unchanged | unchanged | current |
| `topology-author-check.md` (5 Nov) | `sections/01-model-and-realization.md` | `96e12108…` | `96e12108…` | `00d2796a…` | lapsed on 9 Nov |
| | `sections/06-counterexample.md` | `7a9875f0…` | `7a9875f0…` | `3ff20341…` | lapsed on 9 Nov |
| `external-review-packet.md` | — | — | — | — | not a review record: a prepared request, not sent |
| `source-preservation.json` | baseline research and code files | `baseline_manifest` | — | 26 of 27 match; the rank-four note equals its recorded `current_sha256` | current; dated block `post_checks_edits_2026_11_09` added |

`README.md` states that no later change to a proof section should be treated as covered by an earlier review unless its recorded hash still agrees or a new review is added. By that rule no record in this folder covers the current text of any section. The current text is covered only by the agent processes of Section 3.2, which are recorded outside this package.

## 2. Superseded and qualified claims, by record

"REPORT.md" is `publication/disk-folding-checks/REPORT.md`; "edit A.n" and "edit B.n" are its recommended edits, and "part C" is its list of optional presentation items.

### `foundations-referee.md` (Sections 2 and 3)

- **Attempt 1 (lines 33–43), separation of run endpoints in a half-disk collar: superseded.** The corresponding sentence of the proof of Lemma R1, "Their complementary square sectors and retained joins are unchanged", was in the reviewed text (`e39ed6fe…`) and remained in the 7 November text. Check 4 found it false at a boundary fan with two or more run endpoints (REPORT.md, Bottom line and edit A.4). In the 9 November text the proof of R1 (`sections/02-crease-reduction.md`, lines 7–15) cuts the runs one at a time, using (Sch) of Section 4.2 and the argument of Part 2 of Lemma L2.2 (lines 11–13). The collar separation is gone; a fan carrying several run endpoints needs no separate treatment (line 13). The geometric interface (G) of Section 4 was reworded to match (`sections/04-layer-construction.md`, line 26).
- **Verdict (lines 23–29), "No substantive mathematical gap … No unresolved item remains": qualified.** (1) By the record's own rule (lines 122–123), its coverage of Section 2 lapsed on 7 November, when R1's "planar Jordan curve theorem" became "planar (PL) Jordan–Schoenflies theorem" (`e39ed6fe…` → `2cb8673c…`). Section 2 was then re-read by check 4 (crease-reduction lens, an agent), not by this reviewer. Its coverage of Section 3 lapsed on 9 November. (2) In the Section 3 text it endorsed (`b8323559…`, unchanged until 9 November), Proposition C3 omitted "surjective" and was vacuous as printed (REPORT.md edit A.1; check 1 part A). In the 9 November text, C3 (`sections/03-finite-certificate.md`, line 66) gives a surjective member of the fixed toggle family of that map, its proof states the equivariance step (line 70), and Lemma C1 is stated for the contracted region tree of a family member (line 5).
- **Certificate counts (lines 100–105, 107–109 and 113–116): qualified.** The 1,987,252 endpoint comparisons are consistency checks of the reflection (\(\sigma\)) table, not checks of the witnesses, and two of the nine corruption controls, the missing and the extra domain entry, cannot fail (REPORT.md edit B.12). So "all nine semantic corruption controls" (line 115) overstates them. In the 9 November text, Section 3.2 (lines 56–62) names the substantive checks (exact key-set equality, the recurrence of Lemma C1 on all eight cube vertices, six-face coverage and at most seven active bits), calls the endpoint comparisons reflection-table consistency checks, and describes seven semantic corruption controls and two set-comparison illustrations.

### `layer-referee.md` (Section 4, `dc1335b3…`)

The reviewed Section 4 is superseded: its Section 4.2 was replaced on 7 November (see `drafts/L2-correction-notes.md`), and Section 4 was revised again on 9 November.

- **The Hong–Nagamochi premise (lines 15 and 17–21): withdrawn.** The record's check of [HN18, Theorem 4] rested on publisher-indexed text after an HTTP 403. The connected, given-embedding form it relies on could not be verified: the accessible technical report states the theorem for biconnected graphs only (`drafts/L2-correction-notes.md`, §2.1). The subdivision-and-detour repair of line 21 belongs to that argument. The manuscript has not used the theorem since 7 November, and the citation was removed. Research notes that rest on the same premise are listed in `research/errata-2026-11-09-bank-separator-HN-and-collar-v1.md`.
- **Bank separation in L2 (lines 23–30, in particular lines 27 and 29): withdrawn.** The separation clause of the old L2(b) is false: the \(2\times2\) block with its four whole sides as banks satisfies the old hypothesis, yet no order separates both same-edge pairs (`drafts/L2-correction-notes.md`, §2.2; now Remark L2b, `sections/04-layer-construction.md`, lines 204–206). Even where its conclusions hold, as in case (a), the old proof did not derive monotonicity and separation when every spoke at the apex has one merged color (§2.3 of the notes). The replacement is the straight-cut Section 4.2 (lines 32–206), with hypotheses (H1) and (H2) and Corollary L2a.
- **"No unresolved substantive gap was found in L1–L8" (line 15): qualified.** L1 condition 2, unchanged from the reviewed text until 9 November, was stated only for a flip on \(F\) and is false as written (check 1 part B; REPORT.md edit A.2). In the 9 November text it covers a flip on either incident face (line 14). L5 and L6 did not state the six-face conclusion that L7 and Section 5 use (edit A.5); in the 9 November text they do (lines 230 and 236). Part C items on (G), the \(r=1\) case of L6 and the degree bound in L7 were applied on 9 November (lines 26, 238 and 254).
- The Section 4 examined on 7 November (`40d991c7…`) was re-read by agents only: check 4 outside Section 4.2 and check 6 for Section 4.2. Checks 1 and 3 tested its statements and its construction computationally. The 9 November text (`fd964ee2…`) has had only the agent processes of Section 3.2.

### `construction-author-check.md` (Section 4, no hash)

The record has no hash and no date, so its version cannot be identified exactly. Its description of L2 and L2a through the Hong–Nagamochi theorem shows that it concerns Section 4 before 7 November. It is superseded.

- **Lines 14 and 22–28 (L2 and L2a from the Hong–Nagamochi theorem; the external theorem check): superseded** by the straight-cut Section 4.2 of 7 November, for the reasons given under `layer-referee.md`. **Line 44**, obligation 3 (a second reader should check "the apex embedding and empty-fan-face argument"), refers to that argument, which no longer exists.
- **Line 13 (L1, "exact local edge predicates"): qualified.** L1 condition 2 was false as written (edit A.2); 9 November text: `sections/04-layer-construction.md`, line 14.
- **Lines 17–18 (L5, L6): qualified.** Neither stated the six-face conclusion (edit A.5); 9 November text: lines 230 and 236.
- **Line 42 ("The geometric interface (G) is supplied by Section 2, R1–R2"): qualified** by the false collar sentence in the proof of R1 (edit A.4) and by the missing statement that each interface bank is one interval of each incident region's boundary walk (edit A.6). In the 9 November text, R1's proof is `sections/02-crease-reduction.md`, lines 7–15, and (G) (`sections/04-layer-construction.md`, line 26) states the interval property and names its sources, Lemma R1 and its proof, Lemma R2 and the contraction paragraph after R2 (line 24).
- **Line 38:** the file `/tmp/polycube-publication-constructions.txt`, cited for the detailed commands and temporary artifacts, no longer exists (checked on 9 November, also under `/private/tmp`). That provenance is lost.
- **Line 45 ("No unresolved gap was found"): superseded** by the points above.

### `literature-referee.md` (prior art and model comparison)

All four reviewed files have changed since: the Introduction, the References and `literature/theorem-comparison.md` first on 7 November, and all four on 9 November. The record's coverage has lapsed.

- **Cutoff of 5 November (lines 3 and 163–164): superseded** by the check 5 searches through 7 November 2026 (`publication/disk-folding-checks/5-novelty/`; REPORT.md, Check 5). In this package they are summarized in `literature/theorem-comparison.md` ("Refresh of 7 November 2026") and in the `refresh_2026_11_07` entry of `literature/search-log.json`. The access limits listed under Check 5 apply.
- **The connected separating-curve theorem (lines 92–104): withdrawn**, as under `layer-referee.md`. Line 94 cites the [HN18] article. `literature/theorem-comparison.md` now marks the theorem as no longer used.
- **"The references identify the relevant established ingredients instead of claiming them as new" (lines 154–156): contradicted by check 5.** The Introduction did not credit the classification of tree-shaped polyominoes in [ALL25, Section 7] (which completes [ABDD18, Theorem 4]), the disks already covered by [ALL25, Theorem 8.2], or the question of [AAAC21, Section 5] (REPORT.md edit B.9). Lines 68–75 likewise describe [ABDD18] only through its Theorem 5 algorithm and omit its Theorem 4. In the 9 November text, `sections/00-introduction.md`, lines 23–31, gives these credits and states what Theorem A adds.
- **"The corollary concerning the disk restriction of Question 4.9 follows if the manuscript's mathematical theorem is correct" (lines 33–35): qualified.** The Corollary also needs the identification of the polyominoes, simple connectivity and consistent mappings of [ALL25] with the manuscript's physical sources, physical disks and complete-frame maps. Under the literal "homomorphism" reading a \(1\times6\) strip has a surjective consistent mapping, and the Corollary would be false (REPORT.md edit A.3; `publication/disk-folding-checks/4-reading-audit/question-fidelity/`, finding F2). In the 9 November text this is Lemma B1 in Section 1.6 (`sections/01-model-and-realization.md`, lines 125–145; the strip is discussed at line 145), and Section 5 (`sections/05-main-theorem.md`, lines 3–9) uses Lemma B1 for necessity and for the Corollary, without the earlier hedge "if one exists in this physical surface model".
- The record's assessment of a plausible new contribution (lines 27–29) is consistent with check 5, which found no prior or concurrent resolution of the disk case of [ALL25, Question 4.9]. REPORT.md's estimate, about 90% that the theorem is new if true, is an agent estimate with the stated access limits; it is not strengthened here.

### `topology-referee.md` (Sections 1 and 6, and the references of Section 5)

Its hashes matched until 9 November, so through 7 November it described the text it reviewed. The checks of 7 November found no false lemma or theorem statement in Sections 1, 5 and 6. They found gaps and wording slips, some of them in text this record endorsed. Its verdict (line 62, "I found no remaining mathematical blocker in these texts") is qualified, not withdrawn.

- **Line 38, the check of the [ALL25] definitions deferred to "a separate literature task":** that check had not been done by 7 November. It is the bridge lemma of REPORT.md edit A.3. In the 9 November text it is Lemma B1 (`sections/01-model-and-realization.md`, lines 125–145).
- **Line 38, Corollary D1:** its proof joined two different sufficient conditions of [ALL25, Theorem 3.4] by "equivalently" (REPORT.md part C). In the 9 November text the proof of D1 (line 149) cites condition 3, the unknotted boundary, and, as an alternative, condition 2.
- **Line 42, the lobe argument of Section 6: qualified.** The two normal sets were matched to the lobes by a "respectively" in the wrong order, the step wording mixed east and north, and the proof used four facts it did not state (REPORT.md edit A.7). In the 9 November text, `sections/06-counterexample.md` names the vertical and horizontal lobes and their normal sets (lines 38–40), words the steps "for an east (respectively north) step" (line 13), and states the four facts: uniqueness from the root frame and the bits as in the proof of Lemma R2, the reduction of \(2\times4\) consistency to its three \(2\times2\) blocks (line 36), that \((1,3)\) is an end square of both lobes (line 42), and that the fixed square is \((0,0)\) (line 11).
- **Line 44, "The two rectangles overlap in a full square, so their union is a disk": qualified.** This derives the disk from the drawn outline, whereas Section 1.1 requires checking the quotient (edit A.7). In the 9 November text the disk is derived from the actual identifications (`sections/06-counterexample.md`, line 52).
- **Section 6 and [ALL25, Theorem 8.2]:** the source of Proposition X1 satisfies the hypothesis of that theorem, so its foldability already follows from [ALL25] (REPORT.md edit B.10). In the 9 November text this is stated at line 90; the assertions about maps and monochrome components do not depend on it.
- **Line 50, "These labels and scopes agree with their statements": qualified.** Proposition C3 as printed was vacuous (edit A.1); the Corollary of Section 5 kept the hedge "if one exists in this physical surface model", to be dropped once the bridge lemma exists (edit A.3); and L5 and L6 lacked the six-face conclusion that L7 and Section 5 use (edit A.5). 9 November text: `sections/03-finite-certificate.md`, line 66; `sections/05-main-theorem.md`, lines 3–9; `sections/04-layer-construction.md`, lines 230 and 236.
- **Title (line 1), "supporting counterexample":** the source of X1 folds validly; X1 is a counterexample only to selecting a surjective map with a single monochrome component on each face (REPORT.md part C, Packaging). Section 6 already says that the source folds (line 11). The file name `sections/06-counterexample.md` is kept (item G2-33 was skipped), and this record is not renamed.

### `topology-author-check.md` (Sections 1 and 6)

Its hashes matched until 9 November and lapsed then. None of its claims is contradicted by REPORT.md.

- **Line 12:** the blueprint, folded-state and \(\varepsilon\)-correspondence definitions of [ALL25] are in the running text of its Section 3 before Definition 3.1 (pp. 604–605), not in Definitions 3.1–3.3 alone (REPORT.md part C, Introduction and Section 1.6), and the identification of [ALL25]'s consistent mappings with complete-frame maps (edit A.3) is not raised. In the 9 November text, Section 1.6 cites "[ALL25, Section 3, pp. 604–605, and Definitions 3.1–3.3]" and defines a trivial folding (`sections/01-model-and-realization.md`, line 121), and Lemma B1(c) states the identification (line 133).
- **Items 8–10 (lines 23–25)** call X1 a "counterexample"; see the last entry for `topology-referee.md`.

### `external-review-packet.md` and `source-preservation.json`

`external-review-packet.md` is a draft request, not a review record. Nothing has been sent to any outside reviewer. `source-preservation.json` remains current: on 9 November, 26 of its 27 baseline files still match `baseline_manifest`, and `research/rank4-all-topologies-theorem-v1.md` equals its recorded `current_sha256`. The labels changed and added on 9 November are in its new block `post_checks_edits_2026_11_09`.

## 3. The checks of 7 November and the revision of 9 November

### 3.1 Six confidence checks, 7 November 2026

Consolidated record: `publication/disk-folding-checks/REPORT.md`. Four agents fact-checked a first draft of that report (`00-resume/report-factcheck-*`). The manuscript was not edited during the checks. Every check was done by AI agents.

1. **Lemma-by-lemma counterexample search** (`1-lemma-tests/part-A-crease-reduction/`, `1-lemma-tests/part-B-orders-certificate/`), with a builder and an independent verifier. No mathematical counterexample. It found L1 condition 2 false as written, and C3 vacuous as printed.
2. **3D realization of Theorem M3** (`2-realization/`), built in exact rational arithmetic on 564 full-pipeline instances. No counterexample. The \(\varepsilon\)-parametrization, M2 beyond the link systems M3 produces, and D1's appeal to [ALL25, Theorem 3.4] were checked only by reading or through component bounds.
3. **End-to-end construction of Sections 4.3–4.7** (`3-construction/`), run as written, without search over orders. It produced locally feasible layers every time.
4. **Adversarial reading** of Sections 0–3, Section 4 outside Section 4.2, Section 5 and Section 6 (`4-reading-audit/<lens>/`, six lenses, each with a skeptic). No false lemma or theorem statement and no fatal or major gap. It found the collar sentence in the proof of R1 and the title false as written, the missing bridge lemma to [ALL25], and smaller gaps and presentation items.
5. **Novelty refresh** through 7 November 2026 (`5-novelty/`). No prior or concurrent resolution of the disk case of [ALL25, Question 4.9] was found. The tree case is essentially in [ALL25, Section 7], and [ALL25, Theorem 8.2] covers many disks without implying Theorem A. Several databases and the TU Graz thesis repositories could not be searched.
6. **Re-read of the pasted Section 4.2** (`6-l2-reread/`, three lenses with skeptics). No false statement, proof gap, hidden hypothesis or use mismatch; presentation items only.

REPORT.md recommended edits A.1–A.7 and B.8–B.12 and the optional items of part C; none was applied on 7 November. Its estimates, made for the 7 November text, are: Theorem A true, about 95%; the proof correct after the listed small repairs, about 85–90%; correct exactly as written, no; new if true, about 90%; significance, modest but publishable. These are agent estimates. The revision of 9 November applies the listed repairs, but no new estimate has been made, and these numbers are not raised here.

### 3.2 The revision of 9 November 2026

Records: `publication/disk-folding-checks/7-materials-audit/MATERIALS-TO-UPDATE.md`, a read-only audit of the materials to update (seven auditors, each checked by a skeptic, workflow `wf_6e80032d-d51`), and `publication/disk-folding-checks/8-apply-updates/`: the skeptic-corrected items (`items/`), the record of what was applied and skipped (`APPLIED-SUMMARY.json`), the applied batches and their logs, the pre-edit sections (`pre/sections/`) and the diff of the first round (`manuscript.diff`). Pre-edit snapshot: `publication/disk-folding-snapshot-pre-confidence-edits-2026-11-09.tar.gz`.

With the author's approval, the edits were drafted in workflow `wf_f5f9286f-e5c` (nine units, each drafted by one agent and checked by a skeptic verifier) and applied to `sections/`, to `literature/`, to the top-level research summaries `README.md` and `RESEARCH_REPORT.md`, and as one new research errata file. `APPLIED-SUMMARY.json` lists 114 items as applied; the errata file is recorded there as the new file of a unit of its own. The REPORT.md edits are at these places in the 9 November text:

| REPORT.md edit | 9 November text |
|---|---|
| A.1 C3 (surjective member; equivariance step; C1 for a member) | `03-finite-certificate.md`, lines 5, 66 and 70 |
| A.2 L1 condition 2 | `04-layer-construction.md`, line 14 |
| A.3 bridge to [ALL25] | Lemma B1, `01-model-and-realization.md`, lines 125–145; `05-main-theorem.md`, lines 3–9 |
| A.4 proof of R1 by sequential cuts; tangent-join clause; R2 as a characterization | `02-crease-reduction.md`, lines 5, 7–15 and 19 |
| A.5 L5 and L6 with the six-face conclusion | `04-layer-construction.md`, lines 230 and 236 |
| A.6 (G), banks as boundary-walk intervals | `04-layer-construction.md`, line 26 |
| A.7 Section 6 | `06-counterexample.md`, lines 11, 13, 36–42 and 52 |
| B.8 title | `00-introduction.md`, line 1 |
| B.9 credit and positioning | `00-introduction.md`, lines 23–31 |
| B.10 X1 and [ALL25, Theorem 8.2] | `06-counterexample.md`, line 90 |
| B.11 citations | [MT01, Section 2.2] for the Jordan–Schoenflies theorem and [MT01, Section 2.1] for the \(\theta\)-graph lemma (`00-introduction.md` line 33, `02-crease-reduction.md` line 11, `04-layer-construction.md` lines 34 and 38), without item numbers; new references [ADK26], [ABD+04], [CDD+20], [DDMO04], [DW18] and [Mel17] in `07-references.md` |
| B.12 Section 3.2 | `03-finite-certificate.md`, lines 56–62 |

Most part C items were applied too. Of the presentation items of check 6, all were applied except an [MT01] item number (only section locators are given) and the optional merge of cases (b1) and (b2). Among the manuscript items, `APPLIED-SUMMARY.json` lists these as deliberately not applied: G2-12 (L8 is kept as a proposition), G2-14 (no computational remark on branches that minimal members never reach), G2-22 (no remark on the necessity of (H2); Remark (ii) still says that (H2) is sufficient and that necessity is not claimed), G2-23 and G2-V02 (Corollary L2a keeps cases (a), (b1) and (b2)), G2-V01 (the heading of Section 4.7 is kept), G2-33 (the file name `06-counterexample.md` is kept), and an optional tightening of a corner bound in the proof of M3 (part of G1-23). It also records G5-18, G5-19 and G5-26 as needing no change in the files of the literature unit (the first two were applied in other units; G5-26 is the rebuild), and two partial skips outside the manuscript: the optional results file of G7-29, and `RESUME_RESEARCH.md` under G6-14, which is historical and was not edited.

The research notes that state or use the false outward-bank separator lemma, the unverified form of the Hong–Nagamochi theorem or the collar step are corrected by one additive file, `research/errata-2026-11-09-bank-separator-HN-and-collar-v1.md`; the notes themselves are unchanged. It also records that several holed-source research theorems now have conditional proofs. The manuscript does not cite these notes.

The sections were then rebuilt and reviewed. The agent review of the applied text (workflow `wf_f023602f-a41`: five lenses, math-front, math-back, refs-consistency, fidelity and rendering, with a skeptic for each finding) found no mathematical error. Of its 27 findings, 3 were refuted and 24 were real but minor (presentation and consistency). Its fixes were applied on 9 November, except rendering-05, rendering-07 and fidelity-04, and the sections were rebuilt again. Record: `review-wf_f023602f.json`, `batch3-review-fixes.json` and its log, and the `review_round` entry of `APPLIED-SUMMARY.json`, all in `publication/disk-folding-checks/8-apply-updates/`. A page-by-page visual check of the rebuilt PDF (`visual-check-*.json` in the same folder) then led to rendering and notation fixes in the sections. The hashes in Section 1 are those after these fixes.

### 3.3 Still open

- A human read of the proof. Points that most need it: Section 4.2; Lemma B1, which is new on 9 November, in particular the proof of its part (b); and the PL topology.
- The PL topology was checked by reading and by combinatorial certificates on instances, not by a full formal construction: the \(\varepsilon\)-parametrization of M3, M2 for arbitrary curve systems, and (Sch) with its use in R1.
- [MT01] has not been checked against a copy of the book: its item numbers, whether its Section 2.2 states the PL form of the Jordan–Schoenflies theorem, and whether its Section 2.1 contains the polygonal Jordan curve theorem with the parity criterion used in the proof of Lemma B1(b).
- Novelty: the access limits of check 5 apply, and work under review cannot be searched.
- External review: nothing has been sent. The request recorded in `publication/external-review-request-status-2026-11-06.json` is on hold and needs fresh approval from the author before any send. The PDFs `cf63554b…` (5 November) and `25684f7e…` (7 November) and the release archive of 5 November predate this revision and are superseded by it.

## 4. Review status

No human has reviewed the 7 November text or the 9 November text of the manuscript. Every review, check, audit, drafting step and verification recorded in this folder or in `publication/disk-folding-checks/` was done by AI agents. The 9 November edits have had agent drafting, agent skeptic verification and an agent review of the applied text, whose minor fixes were then applied. None of these is a human review, an external peer review or a proof-assistant verification. The estimates of correctness and novelty are those of REPORT.md and are not strengthened by the revision or by this addendum.
