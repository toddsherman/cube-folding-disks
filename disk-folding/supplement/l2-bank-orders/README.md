# L2 supplement: cofacial bank orders (Section 4.2)

This directory was `drafts/L2-supplement/` until 7 November 2026, when the new Section 4.2 was pasted into `sections/04-layer-construction.md`; Remark L2b cites `check_counterexample.py` at this path. Standard-library Python (tested with 3.15.0). Run every command from this directory. `PYTHONDONTWRITEBYTECODE=1` keeps `__pycache__` out of the tree. Outputs are recorded in `harness.log`; its last section belongs to the current `impl.py`.

Update, 9 November 2026: the manuscript revision of 9 November edited Section 4.2 again: [MT01] citations and a sentence on the use of (Sch) in Lemma R1, an added boundary conclusion in (Sch) and a fuller proof of it, the identification of the halves in L2.2(2), the converse step and the fans in L2.2 Part 3, the base case of L2.3, the marker-slide sentence in Step 1 of L2.4, and a slit-tip example in Remark (ii). The statements of Lemma L2, Lemmas L2.3 and L2.4 and Corollary L2a, and Remark L2b, are unchanged. No other file in this directory was changed, so the tests and the runs recorded in `harness.log` still apply to the current statements of Lemma L2 and Corollary L2a and to Remark L2b. These edits were drafted and checked by AI agents and have had no human review.

| file | role |
|---|---|
| `impl.py` | The construction of the final text. `construct` is the proof of L2, `solve` is Lemma L2.4 (Steps 1–4), and `k2_cut` is Lemma L2.3. It does no search over orders or cuts. `L2DEBUG=1` asserts the internal invariants of L2.4 at every recursion level. |
| `l2harness.py` | Hash-pinned byte copy of the shared harness, left unchanged (sha256 `d936b4d5…9489`). Its docstring still labels case `a` "(L2(a))"; read that as Corollary L2a(a). |
| `check_counterexample.py` | Remark L2b: exhaustive checks of the \(2\times2\), \(4\times2\) and \(2\times4\) blocks, with positive controls. |
| `check_adversarial.py` | Adversarial disks and selections. It recomputes (H1)/(H2) and the L2a cases independently of `impl.py`. |
| `controls/` | Mutation controls, the equivalence check against the refereed implementation, the old-gap example (a revision note) and the long-strip size check. |

## Commands

```
python3 l2harness.py impl.py 3000 5501 40 a,b1,b2
python3 l2harness.py impl.py 1000 5502 80 a,b1,b2
python3 check_counterexample.py
L2DEBUG=1 python3 l2harness.py impl.py 1500 5503 60 a,b1,b2
python3 check_adversarial.py 5504 4
L2DEBUG=1 python3 check_adversarial.py 5505 3
python3 controls/long_strip.py 1000
python3 controls/mutation_controls.py 300 4406
python3 controls/equiv_check.py
python3 controls/old_gap_example.py
```

Every command exits with status 0 exactly when all of its assertions hold.

## What is and is not covered

- **The plain harness checks only the final conclusions** of Lemma L2: local feasibility, exposure, monotonicity and separation. The invariants of L2.4 (the orientation in (S3), the mixed Step-3 markers, the interval formulas and tie flags) are certified only by the `L2DEBUG=1` runs. `controls/mutation_controls.py` shows two mutants (O2 ++ O1, and a removed Step-3 slide) that the plain checker cannot detect and `L2DEBUG` does.
- **The harness tests b1 and b2 with outward banks only.** Its cases `b1` and `b2` generate outward banks only, and every case takes at most one sub-interval per maximal run. That alone does not exclude the "meet" clause of (H2): it can hold with whole maximal runs as banks, at the tip of a slit (Remark (ii) of Section 4.2; finding P2 of check 6 of the 7 November 2026 confidence checks, `publication/disk-folding-checks/REPORT.md`, outside this package), and the random disks of `l2harness.py` include slits. In cases `a`, `b1` and `b2` the clause is nevertheless never needed: by the (H2) part of the proof of Corollary L2a, in every such instance some boundary halfedge is unselected or both merged colors are selected, whichever partition is used, and `impl.py` tests those two clauses before the "meet" clause. The `l2harness.py` runs do not report which clause was used; in the 3,000 harness instances of `controls/equiv_check.py` (seed 4410, cases a, b1, b2, g), `impl.py` used only the "both colors" and "unselected" clauses.
  - Non-outward (b1)/(b2) selections are exercised by `check_adversarial.py`, and non-outward selections in general also by case `g`.
  - `check_adversarial.py` also covers runs split into meeting banks, selections of every boundary halfedge, holed polyominoes made into disks by slits, and spanning-tree regions.
  - The "meet" clause is reached in `check_adversarial.py`, whose output reports how often each (H2) clause was used, and in the two hand-built controls of `check_counterexample.py`.
- **Size.** The recursion depth grows linearly with the number of cells, and `construct` raises Python's recursion limit to match. Strips of size \(1\times n\) with all four sides as banks were run up to \(n=3000\); \(n=3000\) took about 250 s. Only the \(n=1000\) run is recorded in `harness.log`.
- **Harness scope (note of 9 November 2026).** `l2harness.py` draws disks with at least 6 cells; smaller regions are covered by `check_adversarial.py` and `check_counterexample.py`. Always pass the CASES argument: the default includes case `g`, whose generator enforces (H1) but not (H2), so a run without it can report a failure on an instance that Lemma L2 excludes. Since 9 November 2026 `check_counterexample.py` exits with status 0 only if exactly eight orders of each even block satisfy conclusions 1–3, as Remark L2b states (before, any positive number passed). All commands also run under `python3 -I -S`.
- **These are tests of the construction, not a proof.** (H2) is sufficient but not claimed necessary: some refused instances do have valid orders, and `check_adversarial.py` reports how many. In every `check_adversarial.py` run recorded in `harness.log`, each refused instance small enough to be searched exhaustively (at most 8 cells) that has a valid order fails (H1) for both partitions (`refused_noH1_valid_exists=True`). The refusals in which some partition satisfies (H1), so that (H2) is the failing hypothesis, number 12 per run: the 6 of them that were searched have no valid order, and the other 6 (`valid_exists=None`, more than 8 cells) were not searched. In check 6 of the 7 November 2026 confidence checks, none of the 706 tested selections that satisfy (H1) but fail (H2) had a valid order, and the output of `impl.py` was checked and found correct on about 9.7M selections, including every maximal (H1)+(H2) selection on every all-flip disk up to 9 cells. These are observations on tested instances; the manuscript claims only that (H2) is sufficient.
