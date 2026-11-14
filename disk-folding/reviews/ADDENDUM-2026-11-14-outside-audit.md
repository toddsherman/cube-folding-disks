# Addendum, 14 November 2026: outside audit and the changes it led to

Date: 14 November 2026. This file summarizes, for this package, an audit made on 13 November 2026 by another AI model, the check of its findings, and the changes made on 14 November. The full records are in `publication/disk-folding-checks/12-outside-audit/` (outside the package). This file edits no earlier record, except that one phrase of `ADDENDUM-2026-11-09c-full-review.md` and of `README.md` was corrected in place and marked with the date. It is not a human review.

**Review status.** The audit was made by an AI model working from a copy of the project, with instructions to form its own view before reading earlier reviews; its reading order cannot be verified. Its findings were checked against the files by the main AI session. Two separate AI agents re-read the first version of the changes; their corrections were applied and not re-read again. **No human with sufficient expertise in this field of study has reviewed the proof of Theorem A or of Corollary A2.**

## 1. What the audit reported

- **Verdict.** No error found in Theorem A, its proof, Corollary A2 or Finite claim C2. Its own confidence figures: Theorem A true 98%, proof correct as written 92%, new 96%, Corollary A2 correct 95%.
- **What it says it did:** a line-by-line re-derivation of Sections 1–5 against the text of [ALL25]; its own enumeration of the 87,538 patterns and its own decision of C2; its own implementation of the model, of the local order condition and of the table algorithm of Corollary A2; searches for a counterexample; recounts of the figures of the review of 9 November from the raw outputs; and a literature search.
- **What was rerun here.** Its enumeration and decision of C2 use only the standard library and no project code; rerun, they give 87,538 patterns, minimum active counts 72,982 / 14,532 / 24, and 80 survivors (38, 38, 4). Its counterexample search over about 33,600 disks was rerun with the same result, no counterexample. Its implementation of the table algorithm of Corollary A2 was rerun and agrees with exhaustive search for a surjective map on all 13,917 disks it tested.
- **Limits of its tests.** In that search no disk had a surjective map without locally feasible orders, so, like the tests of 9 November, it does not exercise the step of Theorem A in which the map must change. Sixteen further disks of 33 squares, built from pieces of [ALL25, Example 4.5], each carry a map that its solver finds to have no locally feasible orders, but all 40,000 maps it sampled on each one have them (also rerun here). One of its stored outputs records 40 disagreements of its Corollary A2 routine with exhaustive search; rerun with its final code, the same test gives none, so that file is stale.

## 2. Its findings that concern this package, and what was done

| Finding | Checked | Action |
|---|---|---|
| The closing paragraph of Section 5 calls both defects of the published implementation [Shi25] defects of input handling. The second is in an internal step that converts a vertex labelling into a face map. | Holds. The re-read of the first rewording found that it, and the sentence it replaced, described the second defect too broadly: the step fails only for a labelling that gives the top-right corner of the first square two labels, and the answer is wrong only when this happens to every labelling. | Section 5 reworded. The draft message reworded. |
| Section 1.6 does not say that the polyominoes of [ALL25] are finite and connected, which Lemma B1(a) uses. | Holds as a point of wording; [ALL25, Section 2] says so. | One sentence added in Section 1.6, and one clause in the proof of Lemma B1(a). |
| The \(O(N)\) bounds in Corollary A2 depend on how the input is encoded. | Holds. The \(O(N^7)\) bound does not depend on it. | The conventions after the statement now give the encoding. |
| `verify.py` accepts some altered certificates: a non-minimal witness with a matching histogram, non-integer `leg_lengths` and `direct_masks_examined`, changed `status` and `schema`. | Holds; each was reproduced. None affects C2. The supplement README already said that minimality is not re-proved, and the packaging review that the two strings were not read. The re-read found two more classes: repeated keys and negative indices. | `verify.py` hardened; see `supplement/README.md`. |
| The draft message says "developed with substantial AI assistance". | Holds: every proof and program was written by AI agents. | Reworded. |
| The copies of the draft message differ by a sign-off. | Holds. | The email copy now says that its sign-off is not part of the canonical text. |

Its other findings concern records outside this package (a note on sources with holes, and two remarks on the report of 9 November), and are handled there.

## 3. Changes to the package

- **Section 1.6:** one sentence added: a polyomino of [ALL25] consists of finitely many squares, at least one, joined edge to edge into a connected whole, and Definition 3.1 is read with these conditions. In the proof of Lemma B1(a), the set of cells is now said to be finite and nonempty.
- **Section 5, after the statement of Corollary A2:** the squares are numbered and each retained join is given by the numbers of its two squares, so the square joined to a given square across a given side is found in constant time.
- **Section 5, closing paragraph:** "two defects of input handling" became "two defects". The first is that the published code assumes the first square of the input to be the top-left square of the bounding box. The second is that a vertex labelling which gives the top-right corner of the first square two labels, one on each side of a slit, makes the conversion to a face map raise an error, and the labelling is dropped.
- No statement changed, and no label was added or removed. The only change inside a proof is the clause in Lemma B1(a).
- **Supplement:** `verify.py` has six further assertions and two helpers, and reads both JSON files with a check against repeated keys; `README.md`, `PACKAGING_REVIEW.md`, `PROVENANCE.json` and the portability patch were updated; a run of the hardened verifier from a scratch copy was added under `validation/`; `SHA256SUMS` lists 29 files. The certificate data and all counts are unchanged.
- **Draft message** (`reviews/external-review-packet.md`): the version line, the description of the corrections, the statement of who wrote the manuscript, and one sentence on this audit.

## 4. Hashes

Computed after the final build; they agree with `build/build-record.json`.

| File | SHA-256 | Status |
|---|---|---|
| `sections/00-introduction.md` | `923aff7e84e3203cb2d9ed6290a1208bf53968774df10b6bf539ed37bc144e08` | unchanged since the build of 9 November (night) |
| `sections/01-model-and-realization.md` | `e11afb022a6580607e827fc9434639a52e7c23e687526baed9c8d86071068b92` | one sentence added in Section 1.6 and one clause in the proof of Lemma B1(a), on 14 November |
| `sections/02-crease-reduction.md` | `c5beb68335ba7f048d2cfcf077b463c1f41fa9aae0f7877abafbed88807945b3` | unchanged since the build of 9 November (night) |
| `sections/03-finite-certificate.md` | `027a264f25c54349ea111fbd735f3537b470e3adc288970c084e581ccb65ad97` | unchanged since the build of 9 November (night) |
| `sections/04-layer-construction.md` | `fd964ee2c1b1305f05ab4ad8f25f329f9bf23a6f0423b75cbf9c3833e58c587c` | unchanged since the build of 9 November (night) |
| `sections/05-main-theorem.md` | `b6278398cb39fab7d051ccfb22f9a39c073bd1d2143ba520b2270a612fa18f8d` | the conventions after Corollary A2 and the closing paragraph reworded on 14 November |
| `sections/06-counterexample.md` | `3ff203415ca2a9c6b9813e9541b707d141ac08ec583ab8122cce3c8f3c13cfff` | unchanged since the build of 9 November (night) |
| `sections/07-references.md` | `3637b45233f116f42c09486ffdb51e8bb5a8838811bae6de6cf3c8b5672b2b99` | unchanged since the build of 9 November (night) |

The PDF is `5f38f455…` (41 pages; SHA-256 `5f38f455e986a2e813c873b654750275a4a169daada3651f48757b9283b7ea3a`). It replaces the 41-page PDF `5725c856…`. The release is `disk-folding-release-2026-11-14.zip`, which supersedes `disk-folding-release-2026-11-09c.zip`.

The hash table of `ADDENDUM-2026-11-09c-full-review.md` is now out of date for Sections 1 and 5. Line numbers in those two files are unchanged, since each change is within one line.

## 5. Typesetting

The 16 pages that differ from the build of 9 November (pages 8 to 17 and 33 to 38) were rendered at 110 ppi and viewed; the other 25 pages are pixel-identical to that build. No heading is stranded and no table is split. Page 38 still ends short, before the witness table of Section 6.

## 6. Effect on earlier records

- Where earlier records in this package say "three small input-handling corrections", read "three small corrections". The phrase was corrected in place, with the date, in `README.md` and in `ADDENDUM-2026-11-09c-full-review.md`.
- The mutation audit of 9 November and the records under `supplement/validation/` dated before 14 November describe `verify.py` as it stood then. `supplement/PACKAGING_REVIEW.md` has an addendum for the present file.

## 7. Later on 14 November 2026: models named, review wording, release 14b

At the author's request the statement of how this work was produced now names the models and is worded more exactly.

- **Models.** The work in this package was written and checked by AI agents under one person's direction, using Anthropic's Fable 5.2 and Opus 5.5, Google's Carbon, and OpenAI's Astra. Opus 5.5 is listed because the local session records show that it wrote part of the work of 6 to 9 November 2026. Which model made the audit of 13 November is not recorded in this package.
- **Review status.** "No human with sufficient expertise in this field of study has reviewed any proof" replaces "No human has reviewed" in the review-status line at the top of this file, in the two newest paragraphs and the status table of `README.md`, and in `reviews/external-review-packet.md`. Earlier dated records are left as written and are to be read in this sense.
- **Draft message.** It now says that the manuscript and supplement "were written and checked by AI agents under my direction, using Anthropic's Fable 5.2 and Opus 5.5, Google's Carbon, and OpenAI's Astra", and that "no one with sufficient expertise in this field has yet reviewed the proof". Before, it said "written by AI agents (Claude models)" and "no human has yet read the proof".
- **Release.** `disk-folding-release-2026-11-14b.zip` supersedes `disk-folding-release-2026-11-14.zip`. No section of the manuscript changed, so the PDF is still `5f38f455…` and the hash table of Section 4 still holds. The supplement is unchanged.

## 8. Third build of 14 November 2026: author named, request notes removed, release 14c

At the author's request, before the package is sent to anyone:

- **Title block.** Section 0 now begins with the author's name, Todd S. Sherman; the date line reads "revised 7, 9 and 14 November 2026"; and a note in italics says that the manuscript and supplement were written and checked by AI agents under the author's direction, names the models, and says that no human with sufficient expertise in this field of study has reviewed any proof. The note was proposed by the AI session, to match the statement in the project's README. The build sets the PDF's author field and its date to 14 November 2026. Nothing else in the manuscript changed.
- **Request packet.** `reviews/external-review-packet.md` was moved out of the package to `publication/external-review-packet.md`. It holds the draft message and notes on whom to ask, which are not for the recipient. Its questions for a referee are now `reviews/questions-for-a-referee.md` in this package. Sections 2, 3 and 7 above name the packet by its old path.
- **Package README.** The description of `reviews/` and the row "Independent specialist scrutiny" of the status table no longer describe the state of the request.
- **Hashes.** `sections/00-introduction.md` is now `0254cae1fab12f8a484ae8fab9f0948a96a90abb03faba3d9a6ddc4774020bd2`; the other seven are as in Section 4. The PDF is `6f447811…` (41 pages; SHA-256 `6f4478119c8919eb65a56415053b78cc07a067fec74221793eb463f870d1911a`). The release is `disk-folding-release-2026-11-14c.zip`, which supersedes `disk-folding-release-2026-11-14b.zip`.
- **Typesetting.** The 28 pages that differ from the previous build (pages 1 to 28) were rendered at 110 ppi and viewed; pages 29 to 41 are pixel-identical to it. The title block shows the author's name, the revision dates and the note. No heading is stranded and no table is split. Page 38 still ends short, before the witness table of Section 6.
