# Adversarial review of the source reduction and finite certificate

Review date: 2026-11-05. This is an automated, separate-pass mathematical and
code review within the same preparation workflow. It is not external peer
review or proof-assistant verification. The review started from the newly
written manuscript sections rather than inheriting the earlier notes'
“adopted” labels or treating prior positive reports as proof.

## Exact versions reviewed

| File | SHA-256 |
|---|---|
| `sections/02-crease-reduction.md` | `e39ed6fe994c76138ef79f517f88b268a4b62f3f4c10192c0e4d9715c5d87aa7` |
| `sections/03-finite-certificate.md` | `6d28c7028fb73b63cdfe0f9841cda17f04beb9881f066d426c5b8e46435a835f` |

The physical-source definition in Section 1.1 was consulted to check the
hypotheses, but this report does not review its realization proof or the
later layer-order assembly. The standalone consumer and its complete data
were read and replayed during the associated packaging review.

## Verdict within this scope

No substantive mathematical gap or invalid computational inference was
found in these exact versions of Sections 2 and 3. They establish a
map-only reduction to at most seven active original arcs, conditional on
the explicitly defined physical disk model. No unresolved item remains
within this assigned scope. This verdict does not certify the manuscript's
separate geometric/layer arguments, novelty claims, or the unrelated
rank-three theorem in the research notes.

## Attempts to break the universal reduction

1. **Interior stars and boundary fans.** R1 uses the actual retained-corner
   quotient. An interior vertex has a full four-sector star, so the proper
   three-coloring classification is exhaustive. Its two possible active
   rays are opposite and share the complete target edge. Boundary fans
   are intervals, including four-sector slit-tip fans; their incident
   terminating rays can be separated in their existing sector order in a
   half-disk collar. The deformation is used only to identify cut-region
   topology, not to add physical joins or change the blueprint. Undoing it
   recovers the induced separate corner fans. A straight run cannot close
   or return to its original drawn endpoint. These facts justify the
   proper-arc tree even when runs share boundary endpoints.

2. **Independent toggles and contraction.** A cut-side isometry fixes both
   endpoints of every unit join on a complete interface. All other joins
   undergo the same isometry at both incident squares or at neither.
   Another original arc lies on one side, apart from boundary endpoints,
   so its common target edge survives. Root-frame plus join statuses gives
   at most one map, which justifies both family cardinality and subsequent
   root normalization. Inactive original arcs contracted into one current
   region receive a common isometry in C1 and remain inactive. The finite
   certificate therefore does not accidentally enlarge the original family.

3. **Leaves and middle components.** Repeated-color leaves can be removed
   without losing coverage, so leaves are exclusive. Five leaves force a
   one-vertex nonleaf subtree adjacent to five distinct face colors; six
   leaves leave no nonleaf color. Both are impossible. Removing any two
   tree edges produces a uniquely defined middle component with precisely
   those two boundary interfaces. Side branches belong wholly to the
   appropriate component. The coverage-loss condition in R4 follows from
   involutivity, not from a weaker unsupported color-count criterion.

4. **Three occurrences and global charging.** In R5 the two middle
   components are disjoint even with branches. The third edge supplies
   both incident colors outside the first middle component, and conversely.
   Minimality therefore confines different opposite colors inside the two
   components. Their outer union contains all four moved colors, giving
   the claimed contradiction. R6's chain intervals exclude chain endpoints
   and are disjoint across chains; a globally confined color cannot pay
   for two intervals. The nonleaf-color cases and bounds 12, 12, 9 are
   correct. The lower bound five follows from six occupied regions.

5. **Four leaves.** The nonleaf subtree has two colors and no path with
   three equal-target edges, hence is a star. If it has multiple arms,
   one arm avoids both opposite leaf colors, retains the other moved
   colors outside, and contains only fixed leaf colors. Its reflection
   cancels one edge. Thus R7's reduction to six uniquely colored regions
   does not depend on a finite enumeration or a layer assumption.

## Attempts to break finite-domain completeness and replay

- Opposite-pair permutations and independent pair swaps give exactly the
  48 cube symmetries. Distinct ordered leaf pairs have exactly the
  adjacent/opposite types. Three distinct leaves have at most one opposite
  pair; allowing arm permutations yields exactly the two stated Y types.
  All ordered positive arm-length triples are generated. Exclusivity,
  adjacency, and six-face coverage are the only filters, so the domain is
  a conservative superset of possible physical trees.
- C1's composition order agrees with the code's vertex-index action:
  `old[sigma[e][q]]` means `g_parent o sigma_e`. Pointwise target-edge
  matching preserves complete endpoint data. The conjugacy identity
  handles ancestor transformations; no tangent orientation is discarded
  by identifying an edge from its incident faces.
- The consumer regenerates the domain independently, checks exact key-set
  equality and duplicate exclusion, and replays each complete vertex
  action. The primary dynamic program is a comparison input rather than
  the source of the upper-bound witness computation. No floating-point
  geometry or external solver enters the verification.
- All eight manuscript table rows, all three totals, and the witness
  histogram were mechanically compared with the fresh Python 3.12 replay.
  They agree: 41,928 path patterns plus 45,610 Y patterns equals 87,538;
  witness costs 72,982 at five, 14,532 at six, and 24 at seven also sum to
  87,538. Endpoint checks are 1,987,252. The survivor split is 38/38/4 and
  the cheaper-assignment count is 4,080.
- The text correctly distinguishes positive witness replay from the
  producer's 98,037,403 search-count provenance. It also correctly states
  that the extra survivor minimality checks are unnecessary for C2 and
  that nine negative controls do not detect every programming error.

## Reproducibility evidence and publication limits

The self-contained supplement was copied outside the repository and replayed
with isolated Python 3.15.0 and Python 3.12.14, the latter with site loading
disabled. Both passed all nine semantic corruption controls. Optimized
execution is explicitly refused rather than silently losing assertions.
See `supplement/PACKAGING_REVIEW.md` and the saved `validation/` records.

The manuscript now makes the source-model restriction, the conservative
abstract domain, the full-frame transfer, and the finite certificate's
limited conclusion explicit. No amendment to these reviewed versions is
required by this report. If either section changes, its new hash is outside
this review until the changes are checked.

## Typography-only follow-up, 2026-11-05

Re-read the revised opening of `sections/03-finite-certificate.md`, SHA-256
`b832355902f826483d983578a6067671161824548adf4a8f9c77437f0bdd5d1a`.
It now explicitly lists opposite face pairs `(0,1)`, `(2,3)`, and `(4,5)`.
This is exactly the pairing encoded by `i ^ 1` in the standalone verifier
and is mathematically equivalent to the former notation. The change
improves typesetting without changing the domain or certificate claim.
The prior endorsement extends to this revised Section 3. No new computation
was necessary for this notation-only check; the review remains an AI
internal review, with the limits stated above.
