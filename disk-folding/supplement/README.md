# Finite colored-tree certificate supplement

This directory is self-contained. Its verifier uses only Python's standard
library; it does not import the surrounding research repository, execute the
certificate producers, call a solver, compile code, or access the network.
Python 3.10 or newer is required. Clean-room runs were performed with Python
3.12.14 and 3.15.0; the detailed results are included below.

## Verify the distributed files and mathematical certificate

From this directory, with an ordinary Python installation:

```sh
python3 -I -S check_integrity.py
python3 -I -S verify.py --output verification-new.json
```

`-I` isolates Python from `PYTHONPATH` and the user site; `-S` also prevents
loading site packages. The output path is relative to this directory unless
absolute. Choose a fresh filename on each run: the verifier refuses to
replace an existing result. Do not use `-O`, `-OO`, or `PYTHONOPTIMIZE`; the
verifier explicitly refuses optimized execution because its checks use
assertions. A failed check terminates with a nonzero exit status.

The expected final counts are:

| Check | Count |
|---|---:|
| Complete normalized path/Y patterns | 87,538 |
| Cube actions | 48 |
| Ordered path leaf-color pairs | 30 |
| Ordered Y leaf-color triples | 120 |
| Endpoint comparisons, two per edge of each pattern (reflection-table consistency checks) | 1,987,252 |
| Small surviving all-active minima | 80 |
| Cheaper assignments rejected for those minima | 4,080 |
| Negative controls rejected (seven semantic corruption controls, two set-comparison illustrations) | 9 |

The 80 minima split as 38 with five arcs, 38 with six, and four with seven.
Every pattern has a replayed six-face witness with at most seven active
arcs, so every pattern with eight through twelve arcs has a strictly
smaller witness. Timings and output hashes vary between executions because
the result includes elapsed time.

Update, 9 November 2026: the endpoint-comparison and control rows above,
the descriptions under "What is checked", and the control wording and the
`validation/` and `PACKAGING_REVIEW.md` entries under "Files and
provenance" were relabeled to agree with Section 3.2 of the
manuscript as revised on 9 November 2026. This follows findings F3 and F4
of check 4 of the 7 November 2026 confidence checks
(`publication/disk-folding-checks/`, outside this package): the endpoint
and active/inactive-status assertions hold for every bit vector, and two
of the nine controls cannot fail. `verify.py`, the certificate files, the
printed keys (`edge_endpoint_matches`, `negative_controls`) and all counts
are unchanged. The relabeling was drafted and checked by AI agents and has
had no human review.

Hardening of 9 November 2026: an agent mutation audit of this supplement
(`publication/disk-folding-checks/11-full-review/supplement-audit/`,
outside this package) re-derived the domain, the counts and Finite claim
C2 with its own enumeration, evaluator and search, and found the verifier
sound: every certificate mutation that should be rejected was rejected,
and every generator and evaluator mutant of the main run was detected. It
also found
inputs that the verifier accepted although they were not as described:
an emptied input-binding list in the certificate or in the primary
result, changed summary fields (`total_patterns`,
`maximum_witness_arcs`, `minimum_histogram`, `direct_masks_examined`),
and non-integer encodings of colors, parents and arc counts. None of
these affects Finite claim C2, which is checked record by record.
`verify.py` now rejects all of them: it requires the two binding lists to
name exactly the expected producer files, checks the integer types,
asserts the summary fields against the records, and counts a negative
control as rejected only when an assertion fails. `check_integrity.py`
now also fails when a file in this directory is not listed in
`SHA256SUMS`; before, a file removed from the manifest and then altered
passed unnoticed. Verifier outputs written here as `verification*.json`
are exempt, as are the manifest itself, bytecode caches and `.DS_Store`;
any other file written here, including the three outputs of the optional
regeneration below, is reported as unlisted until it is removed. The
expected integrity line is now
`Verified SHA-256 hashes for 28 packaged files.` The certificate files,
the producers and all counts are unchanged, and a run of the hardened
verifier from a scratch copy of this directory is recorded in
`validation/verification-python315-hardened-2026-11-09.json`. These
changes were made and tested by AI agents and have had no human review.

Hardening of 14 November 2026: an outside AI audit of the project, made
on 13 November 2026
(`publication/disk-folding-checks/12-outside-audit/`, outside this
package), again confirmed Finite claim C2 with its own enumeration and
search, and reported further altered inputs that the verifier accepted.
None of them affects C2. They were: a valid witness larger than
necessary, with `minimum_histogram` recomputed to match (the verifier
tests minimality only for the 80 all-active survivors, as "What is
checked" says); `leg_lengths` and `direct_masks_examined` written as
booleans, floats, an empty string or negative numbers; changed `status`
and `schema` strings, which the verifier did not read; and, in the
primary result, a survivor listed twice. A re-read of the first version
of this hardening added two more: an object that repeats a key, of which
Python's `json` module keeps only the last value, and an action index
written as a negative number, which Python counts from the end of a
list. `verify.py` now also requires: that no object in either file
repeats a key; that, outside the timing field, every value in the
certificate is an integer, a string or null, and likewise in the
counts, survivor list and histogram of the primary result; that `status`
and `schema` are the expected strings; that path records, and path
survivors of the primary result, carry no leg lengths and Y records
three; that no `direct_masks_examined` is
negative; that every action index lies between 0 and 47; and that
`minimum_histogram` equals the `minimum_histogram` of the primary
result, whose list of survivors must have 80 entries. The last check
makes the number of witnesses of each size, in each class (kind and
number of arcs), equal to the number of patterns for which the primary
producer records that size as the minimum. A replayed witness cannot be
smaller than the minimum, so, if the primary counts are right, every
witness has minimum size; the verifier does not prove those counts,
except for the 80 survivors. The text of `scope` is still not compared
with anything, and the other fields of the primary result are still not
type-checked. Of 26 altered inputs tested, the verifier of 9 November
accepted 21, and the present one accepts one, the changed `scope` text
(`f2_mutants.json` in the folder named above). The shipped certificate
verifies with the same counts, and a run from a scratch copy of this
directory is recorded in
`validation/verification-python315-hardened-2026-11-14.json`. The
expected integrity line is now `Verified SHA-256 hashes for 29 packaged
files.` These changes were made and tested by AI agents and have had no
human review.

## What is checked

The verifier reconstructs all 48 opposite-preserving cube-face permutations
and obtains their eight-vertex actions from face incidence. It derives each
pointwise edge-fixing involution, verifies the supplied leaf-orbit witnesses,
and independently regenerates the complete normalized path/Y domain for
five through twelve arcs with exclusive leaf colors. The generated keys
must agree exactly with the supplied certificate keys, including no
missing, extra, or duplicate record.

Every saved active-bit assignment is replayed as full cube-vertex actions.
The checks that discriminate are the exact key-set equality above and, for
every record, equality of its parent array with that of the regenerated
tree, six-face coverage, and at most seven active bits in agreement with
the recorded active count. The verifier also asserts the endpoint match
at both endpoints of every original target edge and the active/inactive
status of every interface. Each reflection is selected as the unique
symmetry that fixes both endpoints of its edge and maps one incident face
to the other, so these assertions hold for every bit vector once the
reflection table is correct: they are consistency checks of the reflection
(σ) table (the endpoint identity in the proof of Lemma C1), not of the
witnesses. For all 80 saved all-active survivors, the verifier also tests
every cheaper bit assignment.
It compares domain counts, survivor keys and, since 14 November 2026,
the histogram of witness sizes with the separate primary
result. It does not independently re-prove the minimum cost recorded for
every already-reduced pattern; that stronger assertion is unnecessary for
the at-most-seven bound. In one respect the verifier is stricter than
Finite claim C2: a record whose witness keeps every arc active is
accepted only for the 80 patterns with no cheaper covering assignment,
so an all-active witness on a reducible pattern with at most seven arcs,
though sufficient for C2, is rejected.

The output lists nine negative controls. Seven in-memory corruptions
(all-inactive coverage, an incorrect active count, a wrong parent tree,
nonadjacent original colors, a wrong full vertex reflection, a missing
leaf-orbit witness, and a forged arm permutation) exercise semantic
validation. They operate after the initial provenance checks, so they test
the semantic checks rather than merely rejecting changed file hashes. They
detect specified failure modes, not every possible programming error. The
other two controls, for a missing high-arc pattern and an extra
out-of-domain pattern, only illustrate the set comparison: each compares
the generated key set with a copy of the certificate key set with one key
removed or one out-of-domain key added. The compared sets differ by
construction, so these two controls cannot fail and do not exercise the
key-set checks. Omissions and additions are rejected in the main loop, by
`assert k in records` and `seen==set(records)`.

## Files and provenance

- `verify.py`: portability adaptation of the frozen independent consumer.
- `check_integrity.py` and `SHA256SUMS`: standard-library integrity check and
  hashes of all distributed files except the manifest itself.
- `results/colored-disk-tree-toggle-certificates-independent-v1.json`:
  complete 87,538-record certificate, copied byte for byte.
- `results/minimal-colored-disk-region-trees-primary-v1.json`: frozen
  primary comparison result, copied byte for byte.
- `scripts/`: three original producer sources, included byte for byte
  because the original certificates bind their hashes. They are not run
  or imported during verification.
- `provenance/`: original consumer and exact portability patch.
- `PROVENANCE.json`: original repository paths, byte sizes, hashes, and
  description of every consumer adaptation.
- `validation/`: clean-room results and execution context of 5 November
  2026 (finite certificate only), made with the verifier as it then
  stood, and `verification-python315-hardened-2026-11-09.json`, a run of
  the hardened verifier made on 9 November 2026 from a scratch copy of
  this directory; its execution context was not recorded separately.
  `verification-python315-hardened-2026-11-14.json` is the same for the
  verifier as hardened on 14 November 2026.
- `PACKAGING_REVIEW.md`: packaging checks, scope, and limitations (review
  of 5 November 2026, which predates `l2-bank-orders/`, with addenda
  of 9 and 14 November 2026).
- `l2-bank-orders/`: tests of the construction in the proof of Lemma L2
  (manuscript Section 4.2), added on 7 November 2026; see the section below.
  `verify.py` neither reads nor runs it.

The adaptation changes input/output locations and adds the optimization
refusal and, since 9 and 14 November 2026, the hardening assertions
described above. Domain enumeration, cube reconstruction, witness replay, survivor
checks, and the nine negative controls (seven semantic, two set-comparison
illustrations) are unchanged. This packaging work is not a
new independently authored verifier or external peer review.

## Optional regeneration, beyond certificate replay

The frozen primary producer can regenerate the dynamic-programming result:

```sh
python3 -I -S scripts/probe_minimal_colored_disk_region_trees_v1.py --output primary-new.json
```

The separate producer regenerates certificates by direct enumeration and
requires an available C++17 compiler named `c++`:

```sh
python3 -I -S scripts/certify_colored_disk_tree_toggles_independent_v1.py --output certificate-new.json
python3 -I -S verify.py --input certificate-new.json --output regenerated-verification.json
```

These optional producer reruns were not part of this packaging test. Their
three output files are not in `SHA256SUMS`, so `check_integrity.py` fails
until they are moved out of this directory. The
frozen producer sources also use assertions; run them without Python
optimization. They are included for provenance and reproducibility, not
required for checking the saved certificate.

## Bank-order construction tests (`l2-bank-orders/`)

This directory tests the construction in the proof of Lemma L2 (Section
4.2) and is independent of the finite certificate above. It uses only
Python's standard library. Run its scripts from inside it. They load
their sibling modules by path, so `-I -S` may be added to every command
below (an earlier version of this sentence said that `-I` could not be
used; that was wrong):

```sh
cd l2-bank-orders
python3 l2harness.py impl.py 3000 5501 40 a,b1,b2
python3 check_counterexample.py
python3 check_adversarial.py 5504 4
```

`l2-bank-orders/README.md` lists the remaining commands (the `L2DEBUG=1`
runs, mutation controls, an equivalence check and a size check), and
`harness.log` records their outputs. `check_counterexample.py` is the
exhaustive check cited in Remark L2b. These runs test the construction on
random and adversarial instances; the lemma itself rests on the written
proof.

## Scope of the conclusion

This supplement proves the stated finite combinatorial certificate. It
does not prove the universal reduction of physical disks to these trees,
the four-leaf reduction, local layer-order existence, geometric realization,
ambient-isotopy validity, literature novelty, or the larger rank-three
claims elsewhere in the research repository. Those require the manuscript's
separate mathematical arguments. It does not enumerate physical sources
of bounded area or certify arbitrary holed sources.
