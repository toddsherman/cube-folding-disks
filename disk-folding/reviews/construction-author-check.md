# Construction section: author check

File reviewed: `sections/04-layer-construction.md`.

## Scope and interfaces

The section proves locally feasible layer construction on the original physical disk from a six-face map with at most seven whole active crease arcs; it also proves the four-leaf minimal-map reduction. It does not use a finite census as a universal theorem premise. It states the proper-arc/toggle-family geometric interface explicitly as (G), and leaves the independent disk-realization theorem to the geometry/topology section. Neither is claimed to have been proved merely by citing an adoption record.

No new source cuts are introduced. Region separation is analytical. Every original unit join is restored in L3 and checked again in L7. Source-corner fans and boundary occurrences, rather than coincident coordinates, control the apex construction. Interface lengths are arbitrary: alignment reverses an entire region order and matches the full bank sequence.

## Dependencies and numbering

- L1: exact local edge predicates, proved by chord alternation.
- L2 and L2a: cofacial distinct-bank and outward repeated-bank ordering, from the published connected, embedding-preserving Hong–Nagamochi theorem and an explicit fan-cycle analysis.
- L3 and L3a: full-interface tree alignment, whole-face block assembly and distinct-target-edge construction.
- L4: records exclusive leaf colors and the unbounded three-occurrences cancellation lemma, with precise references to the proofs R3 and R5 in Section 2.
- L5: six-arc repair from L2–L4.
- L6: a single repeated face, using L5 only for multiplicity two.
- L7: seven arcs, using L5/L6 and L4, with exhaustive induced-forest block analysis.
- L8: records the four-leaf consequence from Section 2, R7, then supplies layers through L3a. Neither R7 nor L8 invokes L7's seven-arc bound; the normal-form reduction does not depend circularly on seven-arc realization.

## External theorem check

Seok-Hee Hong and Hiroshi Nagamochi, *Simpler algorithms for testing two-page book embedding of partitioned graphs*, Theoretical Computer Science 725 (2018), 79–98, DOI 10.1016/j.tcs.2015.12.039, published Theorem 4.

The publisher-indexed full Section 3 was retrieved through web search; direct URL open returned HTTP 403. The published statement explicitly permits connected graphs without biconnectivity. Its sufficiency proof constructs the separator in the supplied embedding, supporting use of the fixed apex rotation. This differs from the biconnected statement in the older author preprint. The section paraphrases the external theorem and gives its DOI rather than relying on the internal adoption JSON.

The manuscript now uses only the simple-graph instance of the external theorem. Every augmented edge is subdivided once; this preserves disjunctivity and the empty-facial-side property of every monochromatic cycle, including original digons. After obtaining the separator, local detours remove its visits to the inserted monochromatic degree-two vertices. Suppressing them restores the original fixed embedding and its vertex rotations. This resolves the parallel-spoke question without relying on an unverified graph-model convention. The single-color degeneracy is handled directly rather than hidden under the published hypothesis.

## Adversarial checks completed before manuscript drafting

- Fresh independent separator replay: 42,316 selected-bank queries; 104,084 facial monochromatic cycles; four corruption controls.
- Fresh complete eight-vertex tree diagnostic: 262,144 labeled trees; all repeated-region degree and block-coupling cases matched.
- Fresh doubled-bank consumer: 168,834 positive orders; both exact 6! and 8! method-obstruction checks; 16 corruption controls.
- The preceding three replay payloads match frozen results after omitting only elapsed runtime.
- Supplementary adapted structural check: all 211,377 outward selections with at most four banks on the saved 760-disk domain, including outside-first-strip collisions excluded by the older census; 501,270 facial monochromatic cycles. Only the original structural checker's distinct-page assertion was removed. This is shared-checker corroboration, not an independently authored proof.

Detailed commands and temporary artifacts are recorded in `/tmp/polycube-publication-constructions.txt`. No original research note, program, or frozen result was edited.

## Remaining integration/review obligations

1. The geometric interface (G) is supplied by Section 2, R1–R2. The final physical folding conclusion uses Section 1, M3 and D1. L4 and L8 now cite the corresponding proved Section 2 results rather than duplicating their proofs; the unified manuscript remains self-contained.
2. The section's hypotheses use the paper's connected physical source model: each source cell has a distinct grid coordinate, while corners may split along slits. The main definitions must use the same model.
3. A second reader should check the apex embedding and empty-fan-face argument against the final physical-corner definition. The proof spells out the boundary occurrences and does not silently merge slit banks.
4. No unresolved gap was found in this author's combinatorial construction. This statement is an internal author check, not an external peer-review certification or a novelty determination.
