# Addendum, 9 November 2026 (evening): Corollary A2

Date: 9 November 2026. This file records the addition of Corollary A2 to the manuscript on the evening of 9 November 2026, after the revision described in `ADDENDUM-2026-11-09-confidence-checks-and-revision.md`. It edits no record and is not a review. The records of the checks lie outside this package, in `publication/disk-folding-checks/9-poly-time/` (the check of the argument before adoption) and `publication/disk-folding-checks/10-polytime-adoption/` (the reviews of the manuscript text).

**Review status.** All checks below were made by AI agents. **No human has reviewed Corollary A2**, and no human has reviewed the proof of Theorem A.

## 1. What changed

- **Section 5**, now titled "Proof of the main theorem and its corollaries":
  - The former unlabelled corollary is now **Corollary A1 (Question 4.9 for disks)**. Its text is unchanged.
  - The former last paragraph, which said that the finite verification gives no polynomial-time algorithm and asserted no runtime bound, is replaced by **Corollary A2 (deciding foldability of disks)**, its proof and two closing paragraphs.
  - Corollary A2: for a polyomino with \(N\) squares given by its cells and retained joins, simple connectivity can be decided in \(O(N)\) time, and for a simply connected one, CubeFolding [ALL25, Section 4.1] can be decided in \(O(N^7)\) time.
  - The proof:
    - The *cuts* are the maximal straight runs of retained joins through full stars. They depend only on the source.
    - Every noncrossing set \(\mathcal S\) of cuts gives exactly one consistent map \(\beta_{\mathcal S}\) with a given root frame whose 90-degree joins are the joins of \(\mathcal S\). It is built from the all-flip map of the Colors paragraph of Section 4.2 by symmetries fixing the target edges of the cuts.
    - The algorithm enumerates the noncrossing sets of five to seven cuts and reads each region's face from precomputed tables.
    - Soundness uses Theorem L7, Theorem M3 and Corollary D1. Completeness uses Proposition C3, so the corollary rests, like Theorem A, on the computer-checked finite claim C2.
- **Abstract:** one sentence was added on the \(O(N^7)\) algorithm, and the last sentence now covers both results.
- **Introduction**, in the paragraph on [ALL25, Open Problem 9.2]:
  - The clause saying that Theorem A does not settle [ALL25, Conjecture 4.10] is replaced. The paragraph now states the conjecture and credits the tree case to [ALL25, Section 7] and [LS25, Section 1]. It says that Corollary A2 settles the simply connected case, conditional on C2, and that the conjecture remains open for polyominoes with holes.
  - The reference to the old corollary now reads "Corollary A1".
- **Layout only:** in Section 1.2 the one-line paragraph "The condition can equivalently be checked by three kinds of comparisons:" was joined to the preceding paragraph, with no change of wording, so that it no longer ends a page apart from its list. `build/build_manuscript.py` now keeps Table 1 (Section 3.1) on one page; other tables may still break.
- **Unchanged:** all other statements, proofs, labels and sections, and the supplement.

## 2. Hashes

Computed on 9 November 2026 after the final fixes; they agree with `build/build-record.json`.

| File | SHA-256 | Status |
|---|---|---|
| `sections/00-introduction.md` | `923aff7e84e3203cb2d9ed6290a1208bf53968774df10b6bf539ed37bc144e08` | changed this evening |
| `sections/01-model-and-realization.md` | `1638d90984e68131d6e643fe3b80a1493003f5a9fd02419f4d308c33028c31bb` | layout-only paragraph merge this evening |
| `sections/02-crease-reduction.md` | `c5beb68335ba7f048d2cfcf077b463c1f41fa9aae0f7877abafbed88807945b3` | unchanged since the first 9 November build |
| `sections/03-finite-certificate.md` | `027a264f25c54349ea111fbd735f3537b470e3adc288970c084e581ccb65ad97` | unchanged since the first 9 November build |
| `sections/04-layer-construction.md` | `fd964ee2c1b1305f05ab4ad8f25f329f9bf23a6f0423b75cbf9c3833e58c587c` | unchanged since the first 9 November build |
| `sections/05-main-theorem.md` | `d789048cca6f283b525c517b86747c18aac9152cebff039db4943d9bdbaa046c` | changed this evening |
| `sections/06-counterexample.md` | `3ff203415ca2a9c6b9813e9541b707d141ac08ec583ab8122cce3c8f3c13cfff` | unchanged since the first 9 November build |
| `sections/07-references.md` | `3e96b86db90f57d374b46a4a3e0b27851f076f6636fb6345b16551424104b185` | unchanged since the first 9 November build |

The PDF is `8455b4cc…` (40 pages; SHA-256 `8455b4cc302206525f726ef7d8483cab50a1dfb696123ceca071e62cf83de6a2`). It replaces the 38-page PDF `1d5b1ff5…` of the first 9 November build. The release is `disk-folding-release-2026-11-09b.zip`, which supersedes `disk-folding-release-2026-11-09.zip`.

The current-hash column of Section 1 of `ADDENDUM-2026-11-09-confidence-checks-and-revision.md` is now out of date for `sections/00-introduction.md`, `sections/01-model-and-realization.md` and `sections/05-main-theorem.md`. Its line references into Sections 0 and 5 must be rechecked, and its references into Section 1 beyond line 35 now point two lines too far down (subtract two); its references into the other five sections still hold.

## 3. Checks

1. **Before adoption** (`9-poly-time/NOTE.md`):
   - a proof checker, an adversarial skeptic and a referee read the argument;
   - an exhaustive computer comparison against brute force found no disagreement:
     - all physical disks with at most 11 squares, and those with all joins retained and at most 13 squares, up to symmetry;
     - 1,140 random disks with 11–40 squares;
     - about 570,000 adversarial evaluations.
   - An independent reimplementation agreed.
2. **Round 1 on the manuscript text** (`10-polytime-adoption/REVIEWS-round1.md`). Three agents: a proof check, an adversarial check and a fidelity and citation check. None found an error or a gap.
   - The adversarial agent implemented the construction exactly as written. It checked all 113,740,261 noncrossing sets on every slit disk with 10 or 11 squares (155,824 disks), with no failures. On every disk, the consistent maps with a fixed root frame were exactly the maps \(\beta_{\mathcal S}\).
   - Its negative controls (the reversed composition order, crossing sets) failed as expected.
   - The fixes these reviews proposed were applied, among them the direct consistency argument for \(\beta_{\mathcal S}\) and the explicit composition order.
3. **Round 2** (`10-polytime-adoption/REVIEWS-round2.md`; workflow wf_df2c73a6-d5a). Four lenses, a proof referee, an adversary, fidelity and rendering, each with one skeptic per finding. No mathematical error or gap.
   - The adversary ran a third independent implementation on 485,470 noncrossing sets over 511 random slit disks, again with full agreement.
   - Eight confirmed wording and layout fixes were applied.
4. **Typesetting.** Because the Abstract and Introduction grew, every page break moved. Full visual check of all 40 pages of the reflowed PDF by four agents (workflow wf_188c9b64-8ac), with every non-cosmetic finding verified by a skeptic. Two notable reflow defects were fixed: a list lead-in stranded at the foot of page 4 (by a layout-only paragraph merge in Section 1.2) and Table 1 split with one data row left on page 17 (by a build rule keeping it whole). Two cosmetic splits before a display equation (pages 6-7 and 31-32) were left. After these fixes only pages 4, 5 and 17-23 changed; the main session viewed them, and the other 31 page images are pixel-identical to the checked build. The main session also viewed pages 1, 2 and 33-36 at full size.

## 4. Effect on earlier records

- The statement in `README.md` and in the earlier review packet that the manuscript does not settle [ALL25, Conjecture 4.10] is superseded for simply connected polyominoes. `README.md` and `reviews/external-review-packet.md` were updated on 9 November 2026.
- The agent reviews of the 9 November revision (`8-apply-updates/`) cover Sections 00 and 05 only as they stood before this addition. The new text is covered by the checks listed above.
