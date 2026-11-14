# Lemma L2 correction notes (for the author)

**Status, 7 November 2026: applied.** The body below is the 6 November draft, left as written. Its line numbers refer to the files before the 7 November edits (for Section 4, the pre-paste file; the `README.md` line 19 it cites is now line 21), and its `drafts/L2-supplement/` paths now read `supplement/l2-bank-orders/`. A snapshot of the package before these edits is `publication/disk-folding-snapshot-pre-L2-fix-2026-11-07.tar.gz`.

- `drafts/04-2-cofacial-bank-orders.md` was pasted over old lines 30–66. §4.2 is now lines 30–204. The L3a, L5, L6 and L7 citations are at lines 216, 232, 238 and 256. All §5 edits were made (L3a, L5–L7, Lemma R1, the Introduction, the References), and the §5 grep checks pass.
- After the paste, a review of the applied edits (integration, fidelity and rendering, each finding checked by a skeptic) found no mathematical error. These small changes were then made in `sections/`, so `drafts/04-2-cofacial-bank-orders.md` is now the pre-review version:
  - Corollary L2a: "every region with a repeated bank color in L7" became "every region of L7 with two banks on one target edge";
  - L6: "have distinct bank colors" became "have at most one bank on each target edge", matching L5;
  - the root cell \(c_0\) of the Colors paragraph became \(c_\ast\), since \(c_0\) is a corner in Section 1.1;
  - "(a)" became "(a\)" in the statement and proof of L2a, so that Pandoc no longer turns case (a) alone into a list;
  - in L2.3, "\(|Q|\ge3\)" became "\(Q\) has at least three cells", to avoid a page break inside the formula;
  - in Step 4 (S3), "weakly increasing in \(<_1\)" became "weakly increasing in the order of \(Q_1\)";
  - in L7, "the two \(A\)-blocks and two \(B\)-blocks" became "the two blocks on face \(A\) and the two on face \(B\)"; in L3, "L1's asserted cases" became "the cases asserted in L1";
  - the Introduction's date line now adds "revised 7 November 2026".
- A second check (every PDF page viewed, and a fidelity check of the files, again with skeptics) led to three more changes in §4.2:
  - in Steps 3–4 of L2.4, "orders \(<_1\) and \(<_2\)" became "orders", and "\(O\) list \(<_1\) followed by \(<_2\)" became "\(O\) list the order of \(Q_1\) followed by the order of \(Q_2\)" (Typst sets these subscripts under the symbol);
  - in Remark L2b, "gives 0 valid orders" became "gives no valid orders";
  - Remark L2b was moved after the proof of Corollary L2a, so that the labels appear in order. It is still the last item of §4.2 (lines 202–204).
- `drafts/L2-supplement/` was moved to `supplement/l2-bank-orders/`. Only the first docstring line of `impl.py` changed, so its sha256 is now `5d72bdd2…e727a`, not `2388c415…0c20` (§6, §10). The newest `harness.log` block (2026-11-07, from line 299) covers the current files: every command in the supplement README was rerun from the new location, with the same outputs as before apart from elapsed times. `supplement/README.md`, `PROVENANCE.json` and `SHA256SUMS` were updated, and `check_integrity.py` passes.
- The manuscript was rebuilt in the pinned environment (`pypandoc_binary` 1.17, `typst` 0.15.2), which reproduced the old PDF (`cf63554b…`) exactly from the old sections. The current PDF hash is in `build/build-record.json`. `build/pdf-quality-check.json` (entry `final_2026_11_07`) records a visual check of every page of that PDF, together with the cosmetic page-break issues that were left for later. The LaTeX export is not compiled.
- `README.md`, `literature/theorem-comparison.md` (lines 14 and 16), `reviews/external-review-packet.md` (question 5) and `reviews/source-preservation.json` were updated.
- `publication/external-review-request-status-2026-11-06.json` is now `on_hold_attachments_superseded` and needs fresh send approval. The §5 statement that no repeat send approval is needed no longer holds.
- Checklist (§7): items 0 (the hold), 2, 3, 6, 8 and 9 are done. Item 4 is done for the Typst PDF; the LaTeX bullet check was not possible, because the LaTeX export is not compiled. Item 7 is done apart from `RELEASE-MANIFEST.json` and `build/package_release.py`, which have not been rerun. Item 1 (a human read) and item 5 (a recorded review of the pasted text) are open, and the re-read of L2.2–L2.4 that §8 asks for "before the paste" is now a post-paste requirement. The exact [MT01] lemma number is still unchecked.
- **Later on 7 November 2026: six confidence checks** (`publication/disk-folding-checks/REPORT.md`; that folder is outside the release package). They found no mathematical counterexample. Check 6, three agent lenses with skeptics, re-read the pasted §4.2 line by line, including L2.2–L2.4 and the uses in L3, L3a and L5–L8, tested it from the definitions without importing `impl.py`, and found presentation items only. Check 4 re-read §4 outside §4.2 and the proof of R1. So the §8 re-read and item 5 (a recorded review of the pasted text, the edited L5–L7 lines and the R1 wording) were done, at agent level only, and their records (`6-l2-reread/` and `4-reading-audit/` in `publication/disk-folding-checks/`) are outside `reviews/`. Item 1 (a human read) stayed open. Item 9 had fixed only the Jordan → Jordan–Schoenflies wording of R1: check 4 found that the collar-separation sentence of R1's proof ("Their complementary square sectors and retained joins are unchanged") is false at a boundary fan with two or more run endpoints, and check 1 found that L1 condition 2, then stated only for a flip on \(F\), is false as written. REPORT.md edit 4 supersedes the R1 row of the §5 table as a description of what R1 needs; edit 2 is the L1 rewording. Edit 11 also asked for a citation of the planar PL Jordan–Schoenflies theorem, besides the [MT01] item for the \(\theta\)-graph lemma. Check 6 further observed that within (H1) every tested selection failing (H2) has no valid order (706 of 706), so in its tests (H2) behaved as exactly necessary; it suggested an optional remark. §8 is left as written.
- **Update, 9 November 2026: revision.** The REPORT.md edits were applied to `sections/` with the author's approval (record: `publication/disk-folding-checks/8-apply-updates/APPLIED-SUMMARY.json`; pre-edit snapshot `publication/disk-folding-snapshot-pre-confidence-edits-2026-11-09.tar.gz`). In §4, L1 condition 2 now covers a flip on either incident face (line 14), (G) is restated (line 26), L5 and L6 conclude a six-face member (lines 230 and 236), L6 has the \(r=1\) exit (line 238) and L7 the one-line degree bound (line 254). Check 6's presentation items were applied, except the [MT01] item number and the optional merge of (b1) and (b2): Corollary L2a keeps cases (a), (b1), (b2). The optional remark on the necessity of (H2) was not added; Remark (ii) still says that (H2) is sufficient and that necessity is not claimed. R1's proof (`02-crease-reduction.md`, lines 7–15) now cuts the runs one at a time, using (Sch) of §4.2 and the argument of Part 2 of L2.2, and the collar-separation sentence is gone. The Jordan–Schoenflies theorem is cited as [MT01, Section 2.2] and the \(\theta\)-graph lemma as [MT01, Section 2.1], without item numbers; the item numbers, and whether Section 2.2 of [MT01] states the PL form, are still unchecked. These edits had agent drafting, agent skeptic verification and an agent review of the applied text (workflow `wf_f023602f-a41`), which found no mathematical error; its minor fixes, and rendering fixes after a visual check of the rebuilt PDF, were applied the same day. The records are in `publication/disk-folding-checks/8-apply-updates/`. No human has read the 7 or 9 November text, so item 1 is still open. The package summary of the checks and of this revision is `reviews/ADDENDUM-2026-11-09-confidence-checks-and-revision.md`.
- **Update, 9 November 2026: line numbers.** The §4 line numbers given above for 7 November (§4.2 at lines 30–204, Remark L2b at 202–204, and the L3a, L5, L6 and L7 citations at 216, 232, 238 and 256) refer to `sections/04-layer-construction.md` at sha256 `40d991c7…` (PDF `25684f7e…`). Other line numbers in this status block, such as `README.md` line 21 and `literature/theorem-comparison.md` lines 14 and 16, also refer to the files of 7 November. The line numbers in the previous bullet refer to the revised files, `04-layer-construction.md` at sha256 `fd964ee2…` and `02-crease-reduction.md` at sha256 `c5beb683…`. In the revised §4, §4.2 is lines 32–206, Remark L2b is still its last item (lines 204–206), and the L3a, L5, L6 and L7 citations of Corollary L2a are at lines 218, 234, 240 and 258. Checklist item 2 is done. Do not paste `drafts/04-2-cofacial-bank-orders.md` again: it is the pre-review draft, now marked as superseded, and pasting it would undo the post-paste fixes and the revision.

Draft date: 6 November 2026; revised the same day after four referee reports (rigor, downstream fit, computation, completeness), all "accept with minor fixes". Nothing under `publication/` outside `drafts/` has been modified. The new material is only in `drafts/`:

- `drafts/04-2-cofacial-bank-orders.md`: replacement for §4.2 of `sections/04-layer-construction.md`, lines 30–66. It keeps the heading level `## 4.2.`.
- `drafts/L2-supplement/`: `README.md`, `impl.py`, `l2harness.py`, `check_counterexample.py`, `check_adversarial.py`, `controls/` and `harness.log`.
- This file.

## 1. Summary

- **New statement.** Lemma L2 now covers an all-flip physical disk with any disjoint banks, not necessarily outward. Its hypotheses are:
  - **(H1):** the merged colors are cyclically consecutive. This is the old grouping condition.
  - **(H2):** a nondegeneracy condition. Both merged colors are selected, or some boundary halfedge is unselected, or two consecutive banks meet at a mixed position.

  Its conclusions are local feasibility, exposure, monotonicity, and **separation of every pair of same-edge banks**.
- **New proof.** The proof is self-contained: an induction along straight cuts. It uses no Hong–Nagamochi theorem. Its external inputs are standard PL topology: (Sch), the Schoenflies form of the fact that a proper arc splits a disk into two disks (derived from the Jordan–Schoenflies theorem and the \(\theta\)-graph lemma), and the classification of compact PL surfaces (final referee round, §10). Lemma R1 uses that fact but currently cites only the Jordan curve theorem, which does not give disks; R1's wording must therefore be changed (§5, a required edit).
- **Corollary L2a.** It now states that (H1) and (H2) hold in three cases, without outwardness:
  - **(a):** at most one bank per target edge;
  - **(b1):** at most four banks, with one edge repeated at most twice;
  - **(b2):** any number of banks on one edge plus at most one other.

  These cases cover every use in §§4.3–4.7.
- **Remark L2b.** It shows that (H2) cannot be dropped, even for outward banks, using the \(2\times2\) block and every \(2m\times2n\) block. Its wording is neutral and mathematical. It does not mention the earlier version.
- **Downstream effect.** None of L3, L3a, L5, L6, L7, L8 or the main theorem changes in substance. Each cites a case of L2a that its own counting already establishes. The required edits (§5 below) are:
  - four short citation edits in §4 (L3a, L5, L6, L7);
  - one in the Introduction, one in the References, and one wording edit in Lemma R1;
  - outside `sections/`: `literature/theorem-comparison.md` lines 14 and 16, and `reviews/external-review-packet.md` line 40.

## 2. What was wrong with the reviewed §4.2

### 2.1 The cited theorem could not be verified in the form used

§4.2, line 32, cites "Hong–Nagamochi, published Theorem 4" [HN18] for **connected** plane graphs in the **given** embedding. Two problems:

- The accessible full version, Kyoto Univ. Tech. Rep. 2013-001, states Theorem 4 only for **biconnected** graphs. Its Lemma 2 reduces connected graphs to blocks only for *existence*: it re-chooses outer faces and does not keep the embedding.
- The TCS 2018 full text could not be retrieved.

The earlier layer review (`reviews/layer-referee.md`, lines 15–19) relied on indexed publisher snippets after an HTTP 403. The connected, given-embedding form is therefore unverified. About 99% of the regions arising in the proof have cut cells, so their dual graphs are not biconnected, and the gap is not academic.

### 2.2 The separation clause of L2(b) is false as stated

Take the \(2\times2\) block \(\{(0,0),(1,0),(0,1),(1,1)\}\) with all four joins, and select its four whole sides as four banks.

- All selected halfedges are outward.
- The bottom and top banks lie on one target edge \(H_1\), and the left and right banks on \(V_1\).
- The partition \(\{V_0,H_0\}\mid\{V_1,H_1\}\) colors every selected halfedge alike.

So the hypothesis of the old L2(b) holds, but no order separates both same-edge pairs. The two separations would each require a different two-cell set to be the first half of a four-cell order.

The exhaustive check in `check_counterexample.py` (log in `harness.log`) finds:

| block | orders checked | orders satisfying conclusions 1–4 | orders satisfying conclusions 1–3 |
|---|---|---|---|
| \(2\times2\) | 24 | 0 | 8 |
| \(4\times2\) | 40,320 | 0 | 8 |
| \(2\times4\) | 40,320 | 0 | 8 |

Only the final sentence of the old lemma fails: "In case (b), any two selected banks on the same target edge have separated parent sets." The main sentence (an order that is locally feasible, exposing and monotone) is not refuted by these blocks. Remark L2b in the draft proves the failure for every even-by-even rectangle by a short hand argument.

L5, L6 and L7 use exactly this separation clause. For those applications (b1) and (b2), the separation is true, and the new proof establishes it.

### 2.3 A one-color gap in the old derivation of monotonicity and separation, even in case (a)

The last paragraph of the old proof (line 62) reads: "A bank is a consecutive spoke interval with distinct parents, hence those parents are monotone". Sometimes every spoke at the virtual vertex \(u\) has one merged color. For example, a single bank in case (a) can be like this under either partition. The separating curve of the theorem may then pass through \(u\) **between two spokes of one bank**, and cutting at \(u\) breaks the bank's spoke interval.

Concrete instance (case (a)):
- cells \(a=(0,0)\), \(b=(1,0)\), \(c=(2,0)\), with one bank, the south sides (target \(H_1\));
- partition \(P_0\), with spokes subdivided as in the old proof;
- the curve \(u\to w_b\to b\to c\to w_c\to w_a\to a\to u\), drawn in the faces \(F_{ab}\), \(F_{\rm out}\), \(F_{ab}\).

This curve is a separating curve of the given embedding. Cutting it at \(u\) gives the order \(b,c,a\), which is not monotone on the bank.

This is checked mechanically by `L2-supplement/controls/old_gap_example.py`, extracted from the A_blocks candidate's `dev2/examples_v2.py` (Example 10.2), with its output in `harness.log`. It checks \(V-E+F=2\) and that the red and blue edges lie on opposite sides, and reports `cell order after cutting at u: ['b','c','a'] (False, 'bank not monotone')`.

So even where the conclusion is true (case (a), and (b1)/(b2)), the old proof did not derive it. That is why the **whole** proof is replaced, not only case (b). This example belongs in a revision note or referee response, not in the manuscript.

## 3. What changed, old versus new

| item | reviewed §4.2 | draft §4.2 |
|---|---|---|
| title | A separator that orders arbitrary-length banks | Cofacial bank orders by straight cuts |
| external input | Hong–Nagamochi, connected given-embedding form (unverified) | (Sch): Jordan–Schoenflies for a proper arc in a PL disk, the Schoenflies form of the fact Lemma R1 uses |
| scope | "connected physical all-flip region", banks on one boundary component | all-flip physical disk; every application is to a disk (§4 below) |
| hypotheses | (a) one bank per edge; or (b) outward + consecutive merged colors | (H1) consecutive merged colors + (H2) nondegeneracy, for one adjacent-pair partition; no outwardness |
| separation | claimed in case (b) only (false in general) | claimed for all same-edge pairs, under (H1)+(H2) |
| L2a | "Case (b)'s grouping hypothesis holds for …" | "The hypotheses of Lemma L2 hold, without outwardness, in cases (a), (b1), (b2)", with proofs of (H1) and (H2) |
| counterexample | none | Remark L2b: every \(2m\times2n\) block with its four sides as banks |

Structure of the new proof:

- **Lemma L2.1 (parity).** Pure and mixed lattice points.
- **Lemma L2.2 (cuts split the disk).** It now argues explicitly that each side is itself an all-flip physical disk: fans split at the cut, and identifications happen only through joins.
- **Lemma L2.3 (any two cells are separated by a cut).**
- **Lemma L2.4 (marked orders).** An induction with prescribed red and blue markers. It has four steps: the separating cut, the interval formula, the subproblems with their slides, and the combination \(O_1{+\!\!+}O_2\).
- **Proof of L2.** The markers are placed in the color-changing gaps, or at the mixed position given by (H2).

The base proof is C_induction `proof_v2.md` (§§1–5), condensed. The judges' grafts used are:

1. B_halfcells Prop. 2.1: the hand proof for every even-by-even rectangle (Remark L2b).
2. D_free Remark 0.2(ii) / B_halfcells Lemma 1.4(iii): partition independence (Remark (iii) after L2).
3. D_free Remark 0.2(i) / B_halfcells Remark 1.3.1: the easy sufficient condition. "Some boundary halfedge is unselected" is now a clause of (H2) itself, and Remark (ii) gives the exact failure set.
4. B_halfcells (M1) and (B3): "distinct cells are distinct lattice squares" is stated in the setting, and L2.1(5) gives disjoint parent sets for same-edge banks.
5. B_halfcells (TOP2): (Sch) is stated in the full form actually used. The two closures meet exactly in the arc and are bounded by the two boundary arcs.
6. The judges' concerns:
   - The physical-disk claim for the sides of a cut is spelled out in L2.2(2).
   - Conclusion 4 is stated separately for \(I_R\) and \(I_B\).
   - "Cuts" are framed as proof decompositions.
   - The labels are renamed: L2.1–L2.4, (H1)/(H2), (Sch), (S1)–(S3). The old names Lemma C/K1/K2/S/F clashed with Proposition C3 and §4.1's \(F\).
   - Symbols that clashed with the rest of the manuscript were renamed after the referee reports. `grep` over `sections/` finds none of the new names elsewhere.
     - The fact (T) became (Sch), since \(T\) is the contracted region tree.
     - The cut \(C\) became \(\Gamma\), since \(C=\partial[0,1]^3\) in §1.1 and §5.
     - The partition \(P\) became \(\Pi\), since \(P\) is the physical source.
     - The stretch \(S\) became \(\Lambda\), since \(S\) is the cell set.
     - In L2.3, the sides \(A,B\) became \(Q_a,Q_b\) (and \(Q_{2,a},Q_{2,b}\)), since \(A,B\) are faces in L5–L7, and the endpoint \(e\) became \(z\), since \(e\) is a target edge.
     - The line color \(\kappa\) in the proof of L2.1 became \(\lambda\), since \(\kappa_i\) are the cut blocks.
     - The Step-4 parent \(m\) became \(\mu\), since \(m,n\) are the dimensions in Remark L2b.
   - Two clashes were deliberately kept:
     - The cut endpoints \(p,q\). The port letters of §1.1 and L1 occur only as bound entries of the join notation \((i,p,j,q)\) and \((a,p;b,q)\), and §4.2 never names a port by a letter.
     - The rectangle dimensions \(m,n\) of Remark L2b. They are bound inside that remark, and L6's \(m_F\) and L7's local \(m\) are bound in their own proofs.
   - American spelling is used throughout.
7. A_blocks §11: the place / old text / new text table format (§5 below).
8. A_blocks §10.2: the old-gap example, kept in these notes (§2.3), not in the manuscript.

One judges' suggestion was **not** followed: absorbing L2a into L2. The task asked for a corrected Corollary L2a that proves its configurations satisfy the new hypothesis, and that is what the draft does. The optional multiset rewrite of (H1) (A_blocks Prop. 9.2) was not adopted, because the three-case proof is already short.

## 4. Are L3, L3a, L5, L6, L7, L8 and the main theorem affected?

None is affected in substance. Each use was checked against the new statement. Line numbers refer to `sections/04-layer-construction.md` unless stated otherwise.

**Disk hypothesis.** The draft now says this in its setting paragraph. Every region to which L2 is applied comes from the geometric interface (G), line 24, which yields "\(k+1\) all-flip physical disks". After the inactive edges are contracted, the regions of \(T\) are still disks. `02-crease-reduction.md`, line 21: "A contraction glues two disks along the entire common proper arc and gives a disk". The leaf reflections of L6 (line 98) merge a leaf into its parent along a whole arc, which is again such a gluing. L7 (line 118) already says that the interfaces "lie on its one boundary component". So the narrowing from "connected region" to "disk" loses nothing.

**Banks.** Each interface is a whole straight run of retained joins, and "consecutive parents on either bank retain their tangent joins" (line 24). So every interface bank is a bank in the sense of line 26. Banks of distinct interfaces select disjoint halfedges.

| use | line | what it needs | configuration | covered by |
|---|---|---|---|---|
| L3 | 70 | each region: locally feasible, exposes and is monotone on all interface banks | any of the below | conclusions of L2 |
| L3a | 78 | "Each region has at most one bank on each target edge" | (a) | L2 via L2a(a) |
| L8 | 132 | through L3a | (a) | unchanged |
| L5, region \(B\) | 94 | "two on edge \(AB\) and at most two others, with distinct other colors" + separation of the two \(AB\)-banks | ≤4 banks, one edge twice | L2 via L2a(b1) |
| L5, other regions | 94 | "All other regions use L2(a)" | (a) | L2 via L2a(a) |
| L6, \(r=3\), \(m_F\ge2\) | 100 | "\(m_F\) banks on \(AF\) and at most one other" + separation | (b2) | L2 via L2a(b2) |
| L6, remaining regions | 100 | "distinct bank colors" | (a) | L2 via L2a(a) |
| L6, block order | 102 | "a common neighbor … imposes the order of its separated banks" | separation | conclusion 4 |
| L7, repeated bank color | 118 | "two banks on one edge and at most one other bank" + separation | (b2) (also (b1)) | L2 via L2a(b2) |
| L7, others | 118 | no repeated bank color | (a) | L2 via L2a(a) |
| L7, block choices | 120–126 | "its separated banks … force that face's block order" | separation | conclusion 4 |
| Main theorem | `05-main-theorem.md` line 5 | Theorem L7 | — | unchanged |

**Outwardness.** It is no longer a hypothesis. The two sentences that assert it (L5, line 94; L7, line 118) are now unused, though still true, and the edits below drop them. The definition of **outward** in §4.1 (line 26) is still used, by the statement of L2 ("No outwardness is assumed"), Remark L2b and Corollary L2a, and must be kept. Every downstream interface bank is in fact outward, since the partner square lies in another region, so dropping the hypothesis loses nothing.

**Monotonicity.** L3 (line 72) reverses whole regions so that the "straight tangent-coordinate order" of §4.1 (line 28) agrees across an interface. Remark (i) after the new L2 shows that monotonicity along the boundary walk *is* that tangent-coordinate monotonicity. So L3 needs no change.

**Exposure.** The new conclusion is exactly the definition at line 28: the parent is not strictly between the endpoints of any internal flip on that target edge.

## 5. Exact text edits needed outside the new §4.2

All lines are in `sections/04-layer-construction.md` unless another file is named.

| place | old text | new text |
|---|---|---|
| §4.2, lines 30–66 | whole subsection | contents of `drafts/04-2-cofacial-bank-orders.md` |
| L3a proof, line 78 | "Each region has at most one bank on each target edge, so L2(a) applies." | "Each region has at most one bank on each target edge, so L2 applies by Corollary L2a(a)." |
| L5 proof, line 94 | "They are outward: their neighboring squares are in different physical regions. L2(b) and L2a order \(B\), including separation of its two \(AB\)-banks. All other regions use L2(a)." | "By Corollary L2a(b1), L2 orders \(B\), including separation of its two \(AB\)-banks. All other regions have at most one bank on each target edge and use L2 by L2a(a)." |
| L6 proof, line 100 | "L2(b) applies by L2a. All remaining regions have distinct bank colors and use L2(a)." | "L2 applies by Corollary L2a(b2). All remaining regions have distinct bank colors and use L2 by L2a(a)." |
| L7 proof, line 118 | "All interfaces are outward relative to their region and lie on its one boundary component. L2 supplies local orders, exposures, monotonicity and repeated-bank separation." | "Each region is a physical disk whose interfaces lie on its one boundary component. L2 supplies local orders, exposures, monotonicity and repeated-bank separation, by Corollary L2a(b2) for these regions and L2a(a) for the others." |
| `02-crease-reduction.md`, R1 proof, line 11 (required: the new §4.2 and the Introduction sentence below cite R1 for the Schoenflies form) | "join it to either boundary interval and apply the planar Jordan curve theorem." | "join it to either boundary interval and apply the planar (PL) Jordan–Schoenflies theorem." |
| `00-introduction.md`, line 27 | "The bank-order argument uses Hong and Nagamochi's connected-graph separating-curve theorem [HN18, Theorem 4]. All remaining geometric reductions are proved below." | "The bank-order lemma is proved directly, by induction along straight runs of joins; its topological inputs are the PL Jordan–Schoenflies theorem, also used in Lemma R1 of Section 2, the \(\theta\)-graph lemma [MT01], and the classification of compact PL surfaces. All geometric reductions are proved below." |
| `07-references.md`, line 9 | the [HN18] entry | delete; nothing cites it after the edits above. Keep it only if a background sentence is added that cites it. |
| `07-references.md`, new entry (required: the new §4.2 cites [MT01, Section 2.1] for the \(\theta\)-graph lemma) | — | "**[MT01]** Bojan Mohar and Carsten Thomassen. *Graphs on Surfaces*. Johns Hopkins University Press, 2001." Before pasting, check the exact statement number of the \(\theta\)-graph lemma in §2.1 and, if wanted, cite it as [MT01, Lemma 2.1.x]. |

Checks after these edits:

- `grep -n "L2(a)\|L2(b)\|HN18\|Hong" sections/*.md` should return nothing.
- `grep -n "outward" sections/04-layer-construction.md` should return the §4.1 definition (line 26), L3's "process outward" (line 72), and the occurrences in the new §4.2 (the statement of L2, Remark L2b and Corollary L2a) only. The L5 and L7 outwardness sentences should be gone.
- `grep -n "Jordan curve" sections/*.md` should return nothing.
- Combined check (final referee round): `grep -n "L2(a)\|L2(b)\|Jordan curve\|HN18\|Hong" sections/*.md` must return nothing, and `grep -n "MT01" sections/*.md` must find the new §4.2 and the new reference entry.

There is no other reference to L2 outside §4: `grep` over `sections/` finds L2 only in `04-layer-construction.md`.

**Why the R1 edit is required.** R1 (`02-crease-reduction.md`, line 11) justifies "a proper arc in a disk separates it into two disks" with "the planar Jordan curve theorem". Jordan alone does not give that the pieces are disks; that needs Schoenflies. The new §4.2 calls (Sch) "the Schoenflies form of the fact used in Lemma R1", and the new Introduction sentence also refers to R1. Without the R1 edit, the manuscript would contain a false cross-reference.

**Files outside `sections/` that describe the old argument and must be updated or superseded:**

- `literature/theorem-comparison.md`, line 14: the Hong–Nagamochi row ("An explicitly credited proof ingredient …"). Remove it or mark it as no longer used.
- `literature/theorem-comparison.md`, line 16: "Neither the graph separator nor the published PL validity criterion is claimed as new." → "The PL validity criterion [ALL25] is not claimed as new; the bank-order lemma (§4.2) is proved directly."
- `reviews/external-review-packet.md`, line 40: question 5 asks about "the application of the connected Hong–Nagamochi theorem". Rewrite it to ask about Lemmas L2.2–L2.4 (cuts, separation of cells by cuts, marker bookkeeping) and Remark L2b.
- Historical records of the old §4.2. Do not edit them. Add a new review of the new §4.2 instead (checklist below).
  - `reviews/layer-referee.md`, lines 15–30;
  - `reviews/construction-author-check.md`, lines 14 and 24–32;
  - `reviews/literature-referee.md`, line 94, which cites the HN18 article.
- `literature/previous-audit-search-record.json` mentions HN. It is historical, so leave it as it is.
- `reviews/source-preservation.json`: its `unique_statement_labels` list L2 and L2a but not L2.1–L2.4, L2b or (Sch). Update the list when the new section is pasted, or mark the file as superseded.
- `README.md`, line 19: "Each substantive section received a distinct-agent review." This is false for §4 until the new review of §4.2 is recorded. Qualify the sentence until then.
- Release package. Besides `RELEASE-MANIFEST.json`, rerun `build/package_release.py`. It regenerates the release zip, its `.sha256` file and the validation JSON beside `disk-folding/` (currently `disk-folding-release-2026-11-05.zip`, `.zip.sha256` and `.validation.json`), all of which contain the old §4.2.
- **Pending external-review request.** `publication/external-review-request-status-2026-11-06.json` records a prepared, not yet sent request to a named outside referee. Its status is `not_sent_access_blocked`, and its note says no repeat send approval is needed. Its attachments are the current PDF (sha256 `cf63554b…`) and the 2026-11-05 release zip. Both contain the old §4.2, with the false L2(b) separation clause and the unverified HN citation. See checklist item 0.

## 6. Supplement (`drafts/L2-supplement/`)

`README.md` in the supplement lists the files and commands and states what is and is not covered.

- `impl.py` implements the construction in the final text: `construct` is the proof of L2, `solve` is Lemma L2.4 Steps 1–4, and `k2_cut` is Lemma L2.3, built constructively.
  - It does no search over orders or over cuts.
  - It was adapted from the refereed C_induction `impl_v2.py`. `solve` and `k2_cut` are unchanged apart from comments and message strings.
  - `construct` tests (H1) and (H2) literally in the stated form, and places the markers exactly as the proof of L2 does.
  - After the referee reports, `construct` also raises Python's recursion limit. The recursion depth grows linearly with the cell count, and a \(1\times1000\) strip previously raised `RecursionError`. Strips up to \(1\times3000\) now run. After the final referee round only the module docstring changed (§10); the current sha256 is `2388c415…0c20`.
  - With `L2DEBUG=1`, it asserts the color condition, the Step 2–3 interval formulas, the tie convention, the slide claims and (S1)–(S3) at every recursion level, and Remark (iii) at the top level.
- `l2harness.py` is a byte copy of the shared harness (sha256 `d936b4d5…9489`), left unchanged because it is hash-pinned. Its docstring still labels case `a` "(L2(a))"; read that as Corollary L2a(a).
- `check_counterexample.py` checks the \(2\times2\), \(4\times2\) and \(2\times4\) blocks exhaustively with the harness checker:
  - 0 valid orders and 8 orders satisfying conclusions 1–3 in each;
  - (H1) holds and (H2) fails for every (H1)-partition, and `construct` raises `ProofGap`.

  It also runs positive controls: \(3\times2\) and \(2\times3\), and two blocks satisfying (H2) only through its third clause (a side bank split at the mixed point \((1,0)\)). Both are solved, and exhaustive search confirms that they are feasible.
- `check_adversarial.py` (new) is adapted from the computational referee's script. It runs 151 adversarial disks:
  - strips, spirals, slit spirals, combs, serpentines;
  - annuli opened by a slit (holed polyominoes made into disks);
  - spanning-tree regions and maximal disks grown from trees.

  Selections come in outward and non-outward versions: every halfedge selected, runs split into meeting banks, (a), (b1), (b2), b2-full, and arbitrary. It recomputes (H1)/(H2) and the L2a cases independently, and asserts three things: every L2a configuration satisfies (H1)+(H2); (H1)+(H2) gives an order that passes the checker; and `construct` refuses otherwise.
- `controls/` (new) makes the earlier scratchpad-only evidence durable:
  - `mutation_controls.py`: four one-line mutants;
  - `equiv_check.py`: the comparison with a byte copy of the refereed `C_induction_impl_v2.py`;
  - `old_gap_example.py`: §2.3;
  - `long_strip.py`: the size check.
- **Coverage.** The plain harness checks only the final conclusions; the L2.4 invariants are certified only by the `L2DEBUG=1` runs. The O2 ++ O1 mutant (an exact reversal of a valid construction) and the removed Step-3 slide pass the plain checker and fail under `L2DEBUG`. Two coverage limits of the harness itself:
  - Its cases b1 and b2 generate outward banks only. Non-outward (b1)/(b2) selections are exercised by `check_adversarial.py`, and non-outward selections in general also by case g.
  - Its random instances reach only the "both colors" and "unselected" clauses of (H2). The "meet" clause is reached in `check_adversarial.py` (11–12 times per run) and in the two hand-built controls of `check_counterexample.py`.
- `harness.log`. The first block was run with the earlier `impl.py` (sha256 `a5db1601…0f74`). The appended block belongs to the current files:

| run | instances | failures |
|---|---|---|
| `l2harness.py impl.py 3000 5501 40 a,b1,b2` | 3000 | 0 |
| `l2harness.py impl.py 1000 5502 80 a,b1,b2` | 1000 | 0 |
| `check_counterexample.py` | 3 blocks, exhaustive, + 4 controls | ALL OK; 0 valid orders on every block |
| `L2DEBUG=1 … 1500 5503 60 a,b1,b2` | 1500 | 0 |
| `check_adversarial.py 5504 4` | 6619 (5583 in an L2a case; 335 with every halfedge selected) | 0 problems; 476 correct refusals |
| `L2DEBUG=1 check_adversarial.py 5505 3` | 5115 | 0 problems; 458 correct refusals |
| `controls/long_strip.py 1000` | 1 | 0 |
| `controls/mutation_controls.py 300 4406` | 4 mutants × 300, plain and debug | tie flag 149/222, blue \(p_1\) 300/300, O2 ++ O1 0/300, no slide 0/248; expectations hold |
| `controls/equiv_check.py` | 3000 | 2941 identical orders, 59 different but valid, 0 `ProofGap` |
| `controls/old_gap_example.py` | 1 | reproduces `['b','c','a'] (False, 'bank not monotone')` |

## 7. Checklist for the author

0. [ ] **Do not send the pending external-review request** (`publication/external-review-request-status-2026-11-06.json`) with its current attachments. Both the PDF (`cf63554b…`) and the 2026-11-05 release zip contain the old §4.2. After rebuilding and repackaging (items 4 and 7), update its attachment paths and hashes, together with question 5 of the review packet (item 6).
1. [ ] Read the draft §4.2 against this note.
   - It is about 5,300 words, against about 1,300 for the old §4.2 (lines 30–66).
   - Decide whether to keep the full proof of L2.3 in the main text or move it to an appendix.
   - Consider adding one figure showing the two sub-walks \(\alpha_1\kappa_1\) and \(\alpha_2\kappa_2\) with \(p,q\) and the markers. The judges flagged the marker bookkeeping as where a reader is most likely to slip.
2. [ ] Paste `drafts/04-2-cofacial-bank-orders.md` over lines 30–66 of `sections/04-layer-construction.md`. Apply the edits in §5 to L3a, L5, L6, L7, Lemma R1, the Introduction and the References. Keep the §4.1 definition of outward.
3. [ ] Run the `grep` checks in §5.
4. [ ] Rebuild with `python build/build_manuscript.py`, in the pinned build environment (`pypandoc_binary==1.17`, `typst==0.15.2`).
   - Check the PDF rendering of the new displays: the frame formula in the Colors paragraph, the two-line interval formulas in Step 3, and \(O_1{+\!\!+}O_2\) if you add it.
   - Check that the bullets inside the proofs render correctly in Typst and LaTeX.
   - `build/build-record.json` will record new section hashes.
5. [ ] Commission a fresh review of the new §4.2, of the edited L5–L7 lines and of the R1 wording. The README states that a changed section is not covered by an earlier review unless its hash agrees. Until that review exists, qualify `README.md` line 19 ("Each substantive section received a distinct-agent review"). Points for the reviewer:
   - L2.2(2), the claim that each side of a cut is a physical disk;
   - L2.3, Case 2;
   - L2.4, Steps 1 and 3 (the tie flags and the slides);
   - the derivation of the checkerboard colors;
   - the downstream citations.
6. [ ] Update `reviews/external-review-packet.md` (question 5) and `literature/theorem-comparison.md` (lines 14 and 16). Update or mark as superseded the labels in `reviews/source-preservation.json`.
7. [ ] **Before pasting**, move `drafts/L2-supplement/` into the supplement as `supplement/l2-bank-orders/`. Remark L2b cites `supplement/l2-bank-orders/check_counterexample.py`, which does not exist until this move; if you choose another path, change that citation too.
   - Add a section to `supplement/README.md` with the commands from the supplement's `README.md`.
   - Update `supplement/SHA256SUMS` and `supplement/PROVENANCE.json`. The source is the C_induction candidate, `impl_v2.py`, adapted as described in §6.
   - Update the top-level `README.md` ("Run the proof checks") and `RELEASE-MANIFEST.json`.
   - Rerun `build/package_release.py`, which regenerates the release zip, its `.sha256` file and the validation JSON.
   - The README now claims that the supplement "does not by execution alone prove the … layer assembly". Keep that caveat: the L2 checks are tests of the construction, not a proof.
8. [ ] From the new location, rerun the commands in the supplement's `README.md`, at least `python3 l2harness.py impl.py 3000 5501 40 a,b1,b2`, `python3 check_counterexample.py` and `python3 check_adversarial.py 5504 4`. Paste the outputs into the supplement log.
9. [ ] Change R1's "planar Jordan curve theorem" to "planar (PL) Jordan–Schoenflies theorem". This is required, not optional (§5).

## 8. Open points and limitations

- **(Sch) is derived from cited facts, not reproved from scratch.** It is the Schoenflies form of the input of Lemma R1 and is standard PL topology. The draft spells out the identification with a convex polygon, the derivation from the \(\theta\)-graph lemma [MT01, §2.1] and the Jordan–Schoenflies theorem, and the step from "homeomorphic to a disk" to "PL disk" (the classification of compact PL surfaces).
- **(H2) is sufficient; necessity is not proved.** The supplement's evidence:
  - In `check_adversarial.py` (`harness.log`, keys `refused_H1_valid_exists=…`), every refused instance with at most 8 cells in which some partition satisfies (H1), so that (H2) is the failing hypothesis, has no valid order: 6 such instances in each run.
  - Refused instances that also fail (H1) sometimes do have valid orders.
  - `check_counterexample.py` gives the three exhaustive blocks.
- **Case g is not claimed.** The unrestricted form (any consecutive grouping) is false by Remark L2b. Whether conclusions 1–3 alone always hold there is open and is not needed.
- **Disk scope.** The new L2 is stated for disks only. This is harmless downstream (§4), but it is a change of statement, and the authors should accept it as such.
- **Review status.**
  - The base argument (C_induction v2) was refereed by three lenses and judged sound by a fresh skeptic. It was then ranked first by three judges.
  - The draft text was then refereed by four lenses: rigor, downstream fit, computation and completeness. All four accepted it with minor fixes, all of which are applied here or declined with a reason (§9). The revised text has not been re-refereed after these fixes.
  - A human or agent re-read of L2.2–L2.4 is still required before the paste.

## 9. Referee reports: disposition

All four reports found no mathematical error. Every fix was applied, with these exceptions or variants:

- **Symbol clashes (completeness).** All flagged symbols were renamed (§3, item 6) except the cut endpoints \(p,q\) and the rectangle dimensions \(m,n\) of Remark L2b. Both are bound locally and cannot be misread in §4.2.
- **Harness coverage (downstream fit, computation).** The l2harness byte copy is left unchanged, as the downstream-fit referee suggested, because it is hash-pinned. The gaps are covered by the new `check_adversarial.py` instead, and documented in the supplement's README and in `harness.log`.
- **Recursion limit (computation).** Fixed in the code. Because `impl.py` changed, the required runs were repeated with fresh seeds (§6).
- **"Q is a PL disk" (completeness).** The bridging sentence cites the classification of compact PL surfaces and the recognition criterion of §1.1. This is the same input §1.1 already uses.

## 10. Final referee round

Three fresh referees (notation, hostile mathematical read, marker bookkeeping against `impl.py`) all returned "ready after minor fixes". None found a mathematical error. Changes made, all in `drafts/`:

**Draft §4.2 (`04-2-cofacial-bank-orders.md`).**

- *Opening and (Sch).* The opening now lists the external inputs accurately: the Jordan–Schoenflies theorem and the \(\theta\)-graph lemma, which give (Sch), and the classification of compact PL surfaces. The (Sch) derivation now proves the two-component and \(D_1\cap D_2=\Gamma\) claims from the \(\theta\)-graph lemma, cited as [MT01, Section 2.1]. The inaccurate sentence "No graph-embedding theorem is used" is removed. **New required edit:** add the [MT01] entry to `07-references.md` (§5 table).
- *Setting.* The classification of compact PL surfaces is cited on its own, no longer equated with the recognition criterion of §1.1. The contraction sentence now says that the gluing arc lies in the boundary of each piece. "Interior" occurrences are now also called *full stars*, with a pointer to R1's "full retained star".
- *Colors.* Rewritten in the §1.1 convention \(\beta_c(x,y)\), with \((x,y)\in[0,1]^2\) local and \(c=(x_c,y_c)\) the cell; \(\tau\) is defined without a named argument. The letter \(t\) is now used only for positions, and \(X\) only for lattice lines. \(\xi\bmod2\) became "the parity of \(\xi\)". The *vertical* and *horizontal* target edges are now named, which defines \(e_V,e_H\).
- *"Side" vs "half".* The two pieces of a cut are now its *halves* (defined in L2.2(2)); "side" means a cell side only. Changed in L2.2 Part 2 (where the pieces are still \(D_i\)), the L2.3 statement and proof, and L2.4 (opening, Step 1 naming, Cases 1 and 2). "A pure neighbor on either side" became "at either end".
- *L2.3 letters.* The interior vertex \(v\) became \(z\), the same letter as the endpoint it specializes. The line \(\ell\) became "the lattice line containing \(\pi(\Gamma)\)", phrased with half-planes.
- *Marked selections.* The tie flag is now stated as an order ("\(t_R\) first" means \(t_R\) precedes \(t_B\)). New sentences say how a slide may separate coincident markers (with \(t_R\) first only \(t_R\) backward or \(t_B\) forward, and the reverse), and that markers in different stretches impose no order constraint.
- *L2.4 Step 1.* The endpoint in the naming paragraph is \(z\); \(w\) is kept for Cases 1–2. Case 1 says which coincident marker moves first. Case 2 reads "placed by slides at mixed positions \(x_R,x_B\) with \(c(x_R)\ne c(x_B)\)". The selected halfedges next to \(\Lambda\) are \(\omega_\pm\), not \(h_\pm\). We used \(\omega\) rather than the suggested \(\eta\): \(\omega\) occurs nowhere else in the manuscript, while \(\eta\) is the collar width of §1.5.
- *L2.4 Step 3.* The inherited markers are named \(t_R^1=t_R\) and \(t_B^2=t_B\). "Exactly when" is now limited to "before the slides". A sentence records that landings are the only other coincidences, with the same flags. The slide paragraph ends with the common contradiction for all four of \(h^\pm,g^\pm\).
- *L2.4 Step 4.* "Final/initial part of \(I_R^1\)" (and the three analogues) became "of \(\Sigma_1\cap I_R^1\)", which stays true after the Step-3 slides. The (S3) paragraph now names the selected sets explicitly, as \(\Sigma_1\cap I^1_R\cap\alpha_1\) and so on. "Red cut", "Blue cut" and "(S3), both cuts" are italic labels.
- *Proof of L2.* The empty-selection bullet now says "with either tie flag".
- *Corollary L2a(b1).* \(f,g\) became \(e',e''\).
- *Remark L2b.* The script is cited at its shipping path `supplement/l2-bank-orders/check_counterexample.py`. Checklist item 7 now says the move must happen before pasting.
- *Rendering.* `pypandoc_binary==1.17` (Pandoc 3.9) and `typst==0.15.2` were installed in a scratch virtualenv, and the draft alone was rendered with the transformations of `build/build_manuscript.py`. `\varnothing` came out as Typst `diameter` (⌀, U+2300), the wrong glyph, so all occurrences were replaced by `\emptyset` (rendered ∅). `\sqcup`, `\ni`, `\mid`, `\bar\alpha`, `\operatorname{int}` and `\text` render correctly (⊔, ∋, ∣, macron accent, upright "int"). `\setminus` becomes `\\` (a backslash), as it already does for the one existing use in `sections/`. Not changed: Typst sets the subscript of \(<_1\) below the symbol. §4.1's existing \(<_F\) renders the same way. The full manuscript was not rebuilt; checklist item 4 still applies.

**Not changed, with reasons.**

- *Edits outside `drafts/`* (L3a/L5/L6/L7 citations of L2(a)/L2(b), R1's "Jordan curve", the Introduction, the References, and the move of the supplement). This round may edit only `drafts/`. These edits stay required in §5 and checklist items 2, 7 and 9. §5 now also has a combined grep check and the [MT01] row, and the Introduction sentence names the new inputs.
- *Referee 3, (S3) wording "the selected parents along \(I_R^1\)".* This would wrongly include the parents of \(\kappa_1\), which are not in \(I_R\). We used the explicit sets \(\Sigma_i\cap I^i_R\cap\alpha_i\) instead. These exclude both \(\kappa_i\) and the unselected \(h^\pm,g^\pm\).
- *Letters \(a,b\)* in L2.3 versus the corner cells of Remark L2b. Both are bound locally, and the referee proposed no change.
- *`impl.py` comments.* We added a dictionary from the old notation (rho/beta, the sets alpha/beta, C, `claim2_check`, "after Relabel") to the final text in the module docstring, which is the referee's alternative fix. We did not rename the comments themselves: `controls/mutation_controls.py` patches `impl.py` by exact comment-line match, and `controls/equiv_check.py` compares against the byte copy of `impl_v2.py`. No code line changed.

**Runs** (`impl.py` sha256 `2388c415…0c20`, docstring-only change; appended to `harness.log`):

| run | result |
|---|---|
| `l2harness.py impl.py 3000 6601 40 a,b1,b2` | 3000 instances, 0 failures |
| `l2harness.py impl.py 1000 6602 80 a,b1,b2` | 1000 instances, 0 failures |
| `check_counterexample.py` | ALL OK: 24 / 40,320 / 40,320 orders, 0 valid and 8 satisfying 1–3 on each block; 4 positive controls solved |
| `L2DEBUG=1 check_adversarial.py 6603 3` | 5116 instances, 0 problems, 446 correct refusals, (H2) meet clause used 11 times |
| `controls/mutation_controls.py 300 4406` | unchanged from the previous round, expectations hold |
| `controls/equiv_check.py` | 2941 identical, 59 different but valid, 0 `ProofGap` |

The revised §4.2 has not been re-refereed after these fixes. Checklist items 1 and 5 (a human re-read and a recorded review of the pasted text) still apply.
