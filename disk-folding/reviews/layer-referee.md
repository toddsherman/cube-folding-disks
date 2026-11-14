# Independent adversarial review of the layer construction

Date: 2026-11-05.

Reviewed file: `sections/04-layer-construction.md`.

SHA-256: `dc1335b386faa81c5e0b0cb2d158be7aa2f8889a34fdcdaa32fc474887eb8fb9`.

Reviewer role: author of the separate model/realization and counterexample sections, not author of Section 4. This review independently reconstructed the arguments below; earlier positive research reviews were not used as proof premises. It is a mathematical proof review, not a formal proof-assistant certification or an external peer-review decision.

The final integration replaced the duplicate L4 and L8 proofs with references to Section 2, R3/R5 and R7, respectively. I checked those references against their actual statements after the change. The corresponding cancellation arguments had already been reviewed in full before deduplication; the remaining layer proof was unchanged.

## Verdict and scope

No unresolved substantive gap was found in L1–L8 in the reviewed version. The conclusion is conditional on the explicitly stated geometric interface (G), supplied by Section 2: proper straight bend arcs, the unchanged-source region tree, complete-frame toggle consistency, and closure under the indicated component reflections. This review checks Section 4's use of (G); it does not replace the independent review of Section 2. The only external graph-theoretic premise is the stated Hong–Nagamochi theorem, checked against the published primary source as described below. Ambient validity is correctly deferred to Section 1's disk-realization result.

## Published separator theorem

The primary published article is Hong–Nagamochi, *Simpler algorithms for testing two-page book embedding of partitioned graphs*, TCS 725 (2018), 79–98, [doi:10.1016/j.tcs.2015.12.039](https://doi.org/10.1016/j.tcs.2015.12.039). Its indexed Section 3 text was independently retrieved using the query `site.sciencedirect.com/science/article/pii/S0304397515012207 "Theorem 4" "connected partitioned graph"`. Direct page retrieval returned HTTP 403; the primary publisher's indexed text supplied the theorem, its proof construction, and the connectedness claim. The published theorem allows connected graphs, not just biconnected graphs. Its sufficiency proof constructs the separating curve within the supplied disjunctive splitter-free embedding. Thus the actual apex rotation is available, as required for bank order, rather than merely an unspecified two-page embedding.

The current manuscript removes reliance on a multigraph convention: every edge is subdivided using a private vertex, producing a simple graph. Subdivision preserves disjunctivity and the empty facial side of every monochromatic cycle. After applying the theorem, each new same-color degree-two vertex can be bypassed by a small separator detour into the opposite-color side. That detour crosses no graph edge, preserves simplicity, and leaves all original vertices and their rotations untouched. This repair covers both same-color and different-color parallel spokes. I checked that suppressing these vertices changes neither the order of original vertices on the separator nor the bank rotations.

## L2: cofacial bank order, exposure, and monotonicity

- In an all-flip region the horizontal and vertical frame reversals commute. Each adjacent-color merged subgraph is therefore a subgraph of one grid four-cycle, so its connected components are paths of length at most three or complete four-cycles. This structural restriction is essential; the splitter proof would not hold for arbitrary colored planar graphs.
- The virtual spokes are routed in a single actual dual face, preserving boundary occurrences at split source corners. A zero-, one-, or two-edge monochromatic path between spoke parents is a one-, two-, or three-cell corner fan. Its two terminal halfedges are consecutive at the same abstract source corner, giving an empty facial side. This does not depend on treating coincident drawn corners as identical.
- A three-edge path has the two terminal ports of the missing join of a four-cell star. They have the same original color and opposite source ports. L2(a) excludes them because its unique bank for that color has a fixed port; L2(b) excludes them because each port points to an already present region cell. Merely assuming a port is unjoined would not justify this step. The stronger outward hypothesis is present and later applications satisfy it.
- Complete four-cycles have an empty full-star face and no same-color spoke at a cycle vertex. These cases exhaust all monochromatic cycles through or away from the apex; no remaining splitter is hidden.
- A separator page is a disk. Disjoint spokes at its boundary apex preserve the linear order of their other endpoints, up to reversal, giving bank monotonicity. Same-target-edge banks cannot share a parent and occupy disjoint spoke intervals, giving separation. The proof does not assert an independently prescribed direction for every bank.
- The one-color and empty-selection cases are explicitly handled. The adjacent-pair grouping assertion in L2a holds even when three same-edge banks are interspersed in the cyclic order: with at most one other bank their union is the cyclic complement of that single interval.

## L3: all joins and reversal compatibility

Rooting the region tree permits one whole child-order reversal for each interface; a child has only one already aligned neighbor. Hence correlated orientations of its other banks do not create a cycle of demands. Reversal preserves nonalternation, strict betweenness, exposure, and bank separation. Whole-region concatenation cannot introduce a flip interval spanning another region's block. Internal flip/bend pairs are protected by exposure, external ones by block separation. Every unit join of every interface is retained. This is stronger than checking one representative edge per bank.

## L4–L6: cancellations and a single repeated face

The common-edge reflection fixes both complete edge endpoints and swaps exactly the two incident faces and their opposites. For three repeated target-edge interfaces along a tree path, the two consecutive middle components are disjoint and include all side branches. Minimality forces each to confine one opposite face and exclude the other; the two confined faces differ. Their larger union contains all four moved colors, so reflecting it preserves coverage and cancels two arcs. This checks the substantive coverage step in the three-edge cancellation argument.

For one repeated face, leaf cancellation does not create a second repeated color. In the remaining tree, opposite-face adjacency supplies the extra uncounted edge giving multiplicity at most three. At multiplicity three, the degree bound gives either repeated-color banks plus one other bank, or distinct bank colors. Pairwise block-order forces form a forest unless a single common neighbor orders all three blocks, in which case a second pair force would create a cycle. Arbitrary interface lengths do not enter these counts.

## L7: degree-three controls and coupled repeated-block orders

For two repeated faces in an eight-vertex tree, the repeated faces must be adjacent. With four repeated vertices, induced repeated-edge count x, and unique/unique-edge count y, the degree identity is `7+x-y`. Nonleaf status gives a sum at least eight, while the three-edge cancellation excludes x=3. Thus x is one or two and every repeated vertex has degree at most three.

A unique region meeting both copies of one repeated face cannot meet both copies of the other, because an induced repeated edge would form a triangle. If it meets three repeated vertices and x=2, both induced edges would have to use the fourth repeated vertex, creating a four-cycle through the unique region. This verifies the nontrivial degree-three bound; it is not assumed from a small picture. All interface marks are outward because the adjacent square lies in a different physical region.

The final whole-block constraints exhaust three induced forests: one edge, a two-edge path, and a matching. A path fixes only the opposite repeated-face order through its center's separated banks. In the matching case, both repeated-face orders cannot be independently forced: the two common-neighbor paths plus the matching form a tree cycle (or a triangle if the common neighbors coincide). At most one force remains, so the other order can be chosen to agree. This resolves the possible coupling between the two repeated faces rather than choosing their orders independently without justification.

## L8 and conclusion

With four exclusive leaf colors, only two face colors can occur internally. Their connected induced subtree has no three-edge path, hence is a star. If it has at least two equal-color arms, an arm avoiding the opposite-color leaf can be reflected away while preserving all six colors; that contradicts minimality. The surviving internal edge plus four leaves yields the stated five-arc case.

The final claim is correctly a local-order construction for the unchanged source. Applying it to holed sources without an additional boundary-link argument would be invalid, but the manuscript does not do so. No finite search result is used as a substitute for the universal bank and cancellation arguments above.
