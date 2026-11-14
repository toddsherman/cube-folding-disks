# Packaging review

Review date: 2026-11-05. This records checks performed during preparation;
it is not an external referee report, authorship attribution, or formal proof.

## Deliverable and changes

The complete certificate, primary comparison result, three provenance-bound
producer sources, and original consumer are byte-for-byte copies. Their
repository paths, sizes, and SHA-256 hashes are in `PROVENANCE.json`.
The only consumer adaptations are its package root, self-path, default
output name, and an explicit refusal to execute when assertions are
disabled. Mechanically reversing exactly these four changes recovered the
original consumer text. The exact patch is included.

The runtime consumer has no repository imports or third-party dependencies.
The included producer programs are provenance inputs; the consumer hashes
but does not import or execute them. The optional direct-search producer
requires a compiler, while verification does not.

## Clean-room validation

A copy was made outside the repository at
`/var/folders/3d/cvrypchd0jg6zplyg3hywt7w0000gn/T/disk-folding-cleanroom-v00a4g45`.
The process working directory was that external directory. `PYTHONPATH` was
explicitly removed. Both complete replays succeeded:

| Interpreter | Isolation | Elapsed seconds | Result |
|---|---|---:|---|
| Python 3.15.0 | `-I` | 3.438180 | `validation/verification-python315.json` |
| Python 3.12.14 | `-I -S` | 4.058327 | `validation/verification-python312.json` |

Both reproduced 87,538 patterns, 48 cube actions, 30 ordered path pairs,
120 ordered Y triples, 1,987,252 endpoint matches, 80 small minima, and
4,080 rejected cheaper assignments. All nine semantic corruption controls
were rejected on both runs. Exact interpreter flags and versions are
recorded in `validation/clean-room-context.json`. The Python 3.12 run
explicitly disabled site loading as well as user-site and environment
influence.

Independent process checks confirmed that `-O` and `-OO` each exit with
status 1 before reading certificates, explain that assertions are required,
and create no result file. A repeated output filename is rejected without
changing the existing result. File-integrity controls are recorded in
`validation/integrity-controls.json`.

## Scope and remaining limits

The package verifies the finite colored-tree obligation. Its successful
execution does not validate the manuscript's topological source reduction,
layer assembly, or geometric realization arguments. It also does not
establish novelty or audit the separate annular/rank-three research claims.
The semantic controls are targeted tests, not a proof of the verifier's
correctness. The assertion guard makes optimized execution fail closed;
the consumer has not been rewritten as a proof-assistant kernel.

The primary dynamic program and direct C++ search were not regenerated
during packaging. Their full source provenance is included, and their
saved certificates were replayed using the consumer. The exact minimum
cost of every reduced pattern is not a claim of the replay; the verified
at-most-seven witness bound and the 80 checked all-active minima suffice
for the manuscript's finite step.

Original repository sources, results, and research notes were not edited.
The final release archive is prepared separately from this directory to
avoid recursive archive or manifest hashing.

## Addendum, 9 November 2026

The text above is the record of 5 November 2026 and is kept unchanged.
This addendum corrects how it describes two reported results and records
later checks. Like the record above, it is not an external referee report;
it was drafted and checked by AI agents and has had no human review.

1. **Endpoint matches.** The 1,987,252 endpoint matches reported above are
   consistency checks of the reflection (σ) table, not evidence about the
   witnesses. Each reflection is selected as the unique symmetry that
   fixes both endpoints of its edge and maps one incident face to the
   other, so the endpoint and active/inactive-status assertions hold for
   every bit vector (check 4 of the 7 November 2026 confidence checks,
   certificate lens, finding F3; a replay of 2,097,430 non-certified bit
   vectors with the verifier's own replay function raised no assertion).
   The substantive checks are exact key-set equality with the regenerated
   domain, the parent arrays, at most seven active bits, and six-face
   coverage.
2. **Controls.** Of the nine controls reported above as semantic
   corruption controls, seven are semantic. The other two,
   `missing_high_arc_pattern` and `extra_out_of_domain_pattern`, compare
   sets that differ by construction, so they cannot fail; they only
   illustrate the set comparison (finding F4). Duplicate, missing and
   out-of-domain records are rejected by the record checks at lines 116,
   119 and 129 of `verify.py`. Check 4 confirmed this by running that
   logic, with the verifier's own functions, on in-memory certificates
   with a duplicated record, a deleted record and an added out-of-domain
   record.
3. **Later replays.** In the confidence checks of 7 November 2026, check 4
   re-ran `check_integrity.py` (27 files) and `verify.py` and reproduced
   every count above, and check 1 regenerated the 87,538-pattern domain
   and the 80 survivors independently. On 9 November 2026, after the
   description changes in item 5, `check_integrity.py` (27 files) and
   `verify.py` were run again and reproduced the same counts.
4. **Scope.** `l2-bank-orders/`, added on 7 November 2026, is outside the
   scope of this review and of the clean-room replays in `validation/`.
   The runs in the last section of `l2-bank-orders/harness.log` were made
   in the package tree under Python 3.15.0.
5. **Unchanged files.** `verify.py`, the certificates, the producer
   sources, the copy of the original consumer, the portability patch and
   the `validation/` records are unchanged since 5 November 2026. Only
   descriptions were corrected: in `README.md`, `PROVENANCE.json`, this
   addendum, and Section 3.2 of the manuscript as revised on 9 November
   2026 (and, outside the scope of this review, in
   `l2-bank-orders/README.md`); the `SHA256SUMS` lines of the changed
   files were recomputed. On 9 November 2026 the six repository originals listed in
   `PROVENANCE.json` still had their recorded SHA-256 hashes.

The check records are in `publication/disk-folding-checks/`, outside this
package: `REPORT.md` and `4-reading-audit/certificate/REPORT.md`.

## Addendum, 9 November 2026 (evening): verifier and integrity-tool hardening

An agent mutation audit of the supplement
(`publication/disk-folding-checks/11-full-review/supplement-audit/`)
found no error: its own enumeration reproduced the 87,538-pattern domain
and the per-size table, its own search confirmed Finite claim C2 with
minimal active counts 72,982 / 14,532 / 24 for five, six and seven arcs,
and all 70 mutations of the main runs that must be rejected were rejected
(44 of the certificate, 26 of the verifier's generator and evaluator). It found four
gaps, none affecting C2, and they were closed the same evening:

1. `verify.py` accepted an emptied `inputs` list in the certificate and
   an emptied `bindings` map in the primary result. It now requires both
   to name exactly the expected producer files.
2. `verify.py` never read the certificate's summary fields. It now
   asserts `total_patterns`, `maximum_witness_arcs`,
   `direct_masks_examined` and `minimum_histogram` against the records.
   The `status` and `schema` strings are still not read.
3. `verify.py` type-checked only `active_mask`. It now requires integer
   colors, parents, `arcs` and `active_arcs`.
4. `check_integrity.py` passed when a file was removed from `SHA256SUMS`
   and then altered, or when an unlisted file was added. It now fails on
   any unlisted file, apart from the exemptions listed in `README.md`.

The control wrapper in `verify.py` now counts a control as rejected only
on `AssertionError`. `l2-bank-orders/check_counterexample.py` now exits
with status 0 only if exactly eight orders of each even block satisfy
conclusions 1–3, as Remark L2b states; before, any positive number
passed. After these changes the shipped certificate verifies with the
same counts, the ten previously accepted mutants are rejected, and the
integrity check reports 28 files (27 before, plus the new validation
record). `provenance/consumer-portability.patch` was regenerated and
still reproduces `verify.py` from the original consumer byte for byte.
The line numbers 116, 119 and 129 cited in item 2 of the earlier addendum refer to the
5 November `verify.py`; the same checks are now at lines 119, 122 and
132. Item 5 of the earlier addendum ("Unchanged files") describes the state before this
addendum. These changes were made and tested by AI agents and have had
no human review.

## Addendum, 14 November 2026: further hardening after an outside audit

An outside AI audit of the project, made on 13 November 2026
(`publication/disk-folding-checks/12-outside-audit/`), enumerated the
domain and decided Finite claim C2 with its own code, with the same
counts, and found no error. It reported altered inputs that `verify.py`
still accepted (its finding F-2). Each was reproduced against this
directory before anything was changed. A separate agent then re-read the
first version of the hardening and found two further classes (items 5
and 6). None affects C2.

1. A valid witness larger than necessary, with `minimum_histogram`
   recomputed to match, was accepted. `verify.py` tests minimality only
   for the 80 all-active survivors and still does. It now also requires
   `minimum_histogram` to equal the `minimum_histogram` of the primary
   result. This makes the number of witnesses of each size, in each
   class (kind and number of arcs), equal to the number of patterns for
   which the primary producer records that size as the minimum. A
   replayed witness cannot be smaller than the minimum, so, if the
   primary counts are right, every witness has minimum size. The
   verifier does not prove those counts.
2. `leg_lengths` written as `[true, 2.0, 2]`, `false` or `""`, and
   `direct_masks_examined` written as a float or a negative number, were
   accepted. `verify.py` now requires every value in the certificate
   outside the timing field to be an integer, a string or null, path
   records to carry no leg lengths and Y records three, and every
   `direct_masks_examined` to be non-negative. The same type test is
   applied to the counts, survivor list and histogram of the primary
   result, and the same test of leg lengths to its survivors.
3. The `status` and `schema` strings were not read, as item 2 of the
   previous addendum says. They are now required to be the expected
   strings. The text of `scope` is still not compared with anything.
4. A survivor listed twice in the primary result was accepted, because
   survivors are compared as a set. The list must now have 80 entries.
5. An object that repeats a key was accepted, because Python's `json`
   module keeps the last value and discards the earlier ones; a reader
   that keeps the first would see different data. Both files are now
   read with a hook that refuses a repeated key.
6. `identity_action`, the entries of `edge_reflection_actions` and the
   `action` of a leaf-orbit witness were accepted when lowered by 48,
   because Python counts a negative index from the end of a list. They
   must now lie between 0 and 47.

Still accepted, and not claimed otherwise: both histograms recomputed
together for a non-minimal witness (the verifier does not prove minima);
`direct_masks_examined` set to other non-negative integers with a
matching total (a producer statistic that the verifier cannot
recompute); extra keys with string or integer values; any content in
`seconds`; and, in the primary result, fields other than its bindings,
counts, survivors and histogram.

Of the 26 altered inputs in
`publication/disk-folding-checks/12-outside-audit/f2_mutants.py`, the
verifier of 9 November accepted 21 and the present one accepts one, the
changed `scope` text; the other five were already rejected. The shipped
certificate verifies with the same counts. The new assertions were added
after line 137 of `verify.py`, with two helpers at the end of the file
and one change within line 107, so the line numbers cited in the
previous addendum (119, 122 and 132) still hold. The integrity check
reports 29 files (28 before, plus the new validation record).
`provenance/consumer-portability.patch` was regenerated and still
reproduces `verify.py` from the original consumer byte for byte. These
changes were made and tested by AI agents and have had no human review.
