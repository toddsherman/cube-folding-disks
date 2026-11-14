# Addendum, 9 November 2026 (night): full review

Date: 9 November 2026. This file summarizes, for this package, the full review recorded in `publication/disk-folding-checks/11-full-review/REPORT.md` (outside the package), and the changes it led to. It edits no earlier record and is not a human review.

**Review status.** The review was made by AI: the main session, which by then ran on a different model from the one that wrote the earlier text, and six independent agents. **No human has reviewed the proof of Theorem A or of Corollary A2.**

## 1. Findings

- **Full read.** The main session read every section and re-derived each argument from the text: M1–M3, R1–R7, C1–C3, L2.1–L2.4 in full, L3–L7, and Sections 5 and 6. It found no mathematical error or gap. It also checked Lemma B1's reading against the text of [ALL25].
- **Comparison with the published implementation of the [ALL25] algorithm** ([Shi25]). A copy with three small corrections (called input-handling corrections here until 14 November 2026; one of the two defects they remove is in an internal conversion step) was run on all 11,501 simply connected polyominoes with at most 10 squares, or at most 9 with slits. Its face-map and layer-map stages find a surjective mapping with a layer map passing its self-intersection test exactly when a surjective consistent mapping exists (9,709 of them). That test, unchanged from the published code, and the local order condition of Section 1.2 agree on all 4,707,035 pairs compared. The unmodified code can be run on 10,353 of the inputs and disagrees on 187 of them; with the corrections 16 disagreements remain, all crashes in its knot stage. Every disagreement traces to a defect in the implementation, each with a reproducer.
- **Exhaustive test written from the definitions.** Every physical disk with at most 11 squares and every slit pattern: each disk with a six-face map has one with locally feasible orders, and in fact every six-face map there has them (15.2 million maps up to symmetry). A 33.8% sample at 12 squares and a sample at 13 agree. The smallest disks found with a six-face map lacking such orders have 14 squares; whether 14 is least is not known.
- **Supplement audit.** No error. An independent enumeration reproduced the domain and its table, an independent search confirmed Finite claim C2, and all 70 mutations of the main runs that must be rejected were rejected (44 of the certificate, 26 of the verifier's generator and evaluator). It found inputs the verifier should not have accepted; see Section 2.
- **Novelty.** A further search through 9 November 2026 found nothing that states, implies, contradicts or concurrently claims Theorem A or Corollary A2. Google Scholar's citing lists, the TU Graz theses and the Dunham–Whieldon chapter were again not reached.
- **Outside this package.** Claims made elsewhere in the repository for sources with holes are not proved as stated (`research/errata-2026-11-09b-holed-source-claims-v1.md`). They are not used here.

What the two tests do not show: no surjective map of a disk fails up to 11 squares (12 with all joins retained), so they do not exercise the part of Theorem A in which the map must change. They test the statement and the layer criterion, not the proof.

## 2. Changes to the package

- **Section 5:** a closing paragraph reports the two computations. **Section 7:** the reference [Shi25]. No statement or proof changed.
- **Build:** tables are kept whole.
- **Supplement:**
  - `verify.py` requires the two binding lists to name exactly the expected producer files, checks integer types, asserts the certificate's summary fields against its records, and counts a control as rejected only on an assertion failure.
  - `check_integrity.py` fails on a file missing from `SHA256SUMS`.
  - `l2-bank-orders/check_counterexample.py` requires exactly eight orders.
  - The supplement READMEs were updated, the portability patch was regenerated, and a run of the hardened verifier from a scratch copy was added under `validation/`.
  - The certificate data and all counts are unchanged.

## 3. Hashes

Computed after the final build; they agree with `build/build-record.json`.

| File | SHA-256 | Status |
|---|---|---|
| `sections/00-introduction.md` | `923aff7e84e3203cb2d9ed6290a1208bf53968774df10b6bf539ed37bc144e08` | unchanged since the Corollary A2 build |
| `sections/01-model-and-realization.md` | `1638d90984e68131d6e643fe3b80a1493003f5a9fd02419f4d308c33028c31bb` | unchanged since the Corollary A2 build |
| `sections/02-crease-reduction.md` | `c5beb68335ba7f048d2cfcf077b463c1f41fa9aae0f7877abafbed88807945b3` | unchanged since the Corollary A2 build |
| `sections/03-finite-certificate.md` | `027a264f25c54349ea111fbd735f3537b470e3adc288970c084e581ccb65ad97` | unchanged since the Corollary A2 build |
| `sections/04-layer-construction.md` | `fd964ee2c1b1305f05ab4ad8f25f329f9bf23a6f0423b75cbf9c3833e58c587c` | unchanged since the Corollary A2 build |
| `sections/05-main-theorem.md` | `308d1cc2a6f5ee1e91046fc67cb6338cd05d9ea8fcd1bf4265e23cde6e2af7d3` | closing remark added this night |
| `sections/06-counterexample.md` | `3ff203415ca2a9c6b9813e9541b707d141ac08ec583ab8122cce3c8f3c13cfff` | unchanged since the Corollary A2 build |
| `sections/07-references.md` | `3637b45233f116f42c09486ffdb51e8bb5a8838811bae6de6cf3c8b5672b2b99` | reference [Shi25] added this night |

The PDF is `5725c856…` (41 pages; SHA-256 `5725c856f27daace680c08fb854f830cc2dab54dce659cd6a2dc217e3a42d2f1`). It replaces the 40-page PDF `8455b4cc…`. The release is `disk-folding-release-2026-11-09c.zip`, which supersedes `disk-folding-release-2026-11-09b.zip`.

The hash table of `ADDENDUM-2026-11-09b-decision-corollary.md` is now out of date for Sections 5 and 7. Line references into Section 5 before its last paragraph still hold.

## 4. Typesetting

Relative to the fully checked 40-page build 8455b4cc…, only pages 18 and 36–41 changed (page images compared one by one); the main session viewed each of them. Page 18 carries Table 1 whole at its top. Pages 36–38 carry the new closing paragraph of Section 5 and the start of Section 6. Page 38 ends about half full because the witness table of Section 6 is kept whole and opens page 39. Page 41 is the reference list with the new entry [Shi25]. The other 34 pages are pixel-identical to the checked build. Text extraction shows no replacement characters and no raw markup.

## 5. Effect on earlier records

- The review of the verifier in `reviews/` and the clean-room records of 5 November under `supplement/validation/` describe `verify.py` as it stood before the hardening. The mutation audit of this night, and the rerun recorded in `supplement/PACKAGING_REVIEW.md`, cover the current file.
- Statements in earlier records that the supplement code is unchanged since 5 November are true of the certificate data and the producers, and no longer true of `verify.py`, `check_integrity.py` and `l2-bank-orders/check_counterexample.py`.
