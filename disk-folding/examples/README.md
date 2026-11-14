# Standalone check of the 15-cell example (Proposition X1)

This directory reproduces the finite claims of manuscript Proposition X1 without the original research repository. It is separate from the main finite-reduction supplement and does not modify that supplement's manifest.

The source of Proposition X1 folds validly onto the cube (Section 6); it is not a nonfoldable source. It is a counterexample only to selecting a surjective map with a single monochrome component on each target face: with the complete frame of the square (0,0) fixed, its only surjective map has seven monochrome components. The file names `counterexample.json` and `verify_counterexample.py` are unchanged; the verifier's default witness path is `counterexample.json`.

Files:

- [`counterexample.json`](counterexample.json): all fifteen cells, complete cube frames, dense layer ranks, and eleven target-edge endpoint words from Section 6.
- [`verify_counterexample.py`](verify_counterexample.py): a Python standard-library verifier and exhaustive complete-map search.
- [`verification.json`](verification.json): the successful result, including SHA-256 bindings to the witness and verifier.
- [`test-evidence.json`](test-evidence.json): isolated execution and corruption-control results.

Copy this directory anywhere. From any working directory, run:

```sh
python3 -I -S /absolute/path/to/examples/verify_counterexample.py
```

No installation, network, third-party package, repository import, or precomputed map inventory is required. The default witness is resolved relative to the script, not the working directory. A different witness can be checked with `--witness /path/to/witness.json`. Failure prints `VERIFICATION FAILED:` to standard error and exits with status 1. All validation uses explicit exceptions; Python optimization does not disable it.

The verifier generates the 48 affine cube-face frames from cube vertices, reconstructs all geometric retained joins, and fixes the first complete frame to `(0,1,3,2)`. It then searches the complete finite domain using exact retained-edge endpoint equality, arc consistency, and exhaustive branching. It performs no face-coverage pruning. Restricting each variable to a consistent domain and then branching over every remaining state is exhaustive; no bounded-search cutoff is used.

After enumeration it compares the unique surjective map to the displayed witness, checks strict dense face ranks, reconstructs all endpoint words, rejects alternating matched endpoints, and recomputes monochrome connected components and 90-degree join counts. Source disk topology and the PL validity implication are proved in the manuscript; this finite program does not claim to prove the realization theorem.

Expected results:

| Check | Result |
|---|---:|
| Complete cube frames | 48 |
| Source cells | 15 |
| Actual retained joins | 20 |
| Complete normalized maps | 81 |
| Surjective maps | 1 |
| Used target edges / checked endpoint words | 11 |
| Monochrome retained-edge components | 7 |
| 90-degree joins | 12 |

The face-count histogram for one through six covered faces is `(1,12,29,26,12,1)`. The deterministic search visits 161 recursive nodes. The disconnected monochrome face consists of row pairs `(1,5)` and `(11,12)`, exactly the two dominoes stated in Section 6.

## Recorded execution

On 2026-11-05, the verifier passed from working directory `/tmp` with `-I -S` under CPython 3.15.0. It also passed under CPython 3.12 with byte-for-byte identical JSON output. The normal and `-O -I -S` CPython 3.15.0 runs produced identical results. Four independent corruptions were rejected both normally and with `-O`, for eight rejected runs:

1. Replace a rank by a JSON Boolean.
2. Swap ranks of rows 1 and 11. Ranks remain dense, but a retained-edge pairing crosses.
3. Forge an endpoint word as `ABAB`.
4. Replace a stored target-edge vertex number by a JSON Boolean.

The exact error messages and source/witness hashes are in `test-evidence.json`. These controls exercise input typing, actual geometric layer consistency, and reconstruction of displayed certificate data. They are not premises of the analytic 81-map proof.

For an optimization check, run the same command with `-O`:

```sh
python3 -O -I -S /absolute/path/to/examples/verify_counterexample.py
```

The script and witness are small enough to inspect directly. No statement of novelty or global size minimality is attached to this example. The foldability of this source is not new: as Section 6 notes, it also follows from [ALL25, Theorem 8.2] (reference [ALL25] of the manuscript), whose hypothesis holds at the boundary vertex (2,3) with the valid corner (5,0) of the bounding box, at distance 3 in both directions. The assertions about consistent maps and monochrome components do not depend on that theorem.
