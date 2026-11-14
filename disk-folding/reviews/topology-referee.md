# Internal cross-review: realization and supporting counterexample

Reviewer role: construction author, reviewing the separately authored topology and counterexample sections. This is an internal mathematical review, not external peer review, proof-assistant formalization, or a novelty certification.

## Exact text reviewed

| File | SHA-256 |
|---|---|
| `sections/01-model-and-realization.md` | `96e12108821728676680526f9b79c5b4db29496e0e46094547fbfbd3c83d59ae` |
| `sections/06-counterexample.md` | `7a9875f04aaf5ce97183972db864f380f76896c976d3c00884f11bdc94abe8f8` |

The complete earlier Section 1 text was read adversarially, then its source-frontier clarification, M1–M3/ALL25 renumbering, and final M1 wording correction were checked. Section 6 was read in full, and its later standalone-example paragraph was checked against the supplied program and evidence as recorded in the amendment below. The hashes above were recomputed after those changes. No substantive unresolved defect was found in these final texts.

## Model and transverse connectors

The source uses distinct grid cells and only retained-side-induced corner identifications. A slit tip with a four-sector interval fan is treated as a boundary vertex rather than silently recapped as an interior full star. The complete frames agree on both endpoints of every retained join. These definitions agree with the construction section's BL/BR/TR/TL corners, S/E/N/W ports, and outward-increasing face ranks.

In M1, I checked each of the four connector comparisons. Nested same-ray U-arcs have strictly ordered excursions because their rank intervals have distinct endpoints. Opposite-ray U-arcs are separated by the axial-height/excursion gap. Straight connectors with consistently ordered intercepts do not cross. For the straight/U case, the straight intercept is outside the U interval; when it is above, the explicit lower bound tA/N > tN separates it from the U excursion. The total number N bounds every face rank. This is a geometric construction, not a reference to solver feasibility.

One statement-level issue was found and repaired: M1 initially claimed endpoints at “prescribed” increasing heights, although its proof chooses the arithmetic heights tA(r+1). The final statement says “explicitly chosen,” which is exactly what M3 uses. No inference about arbitrary preassigned heights remains.

## Simultaneous caps

M2 does not cone different links to one point. On the punctured sphere, pairwise disjoint Jordan circles give disjoint or nested closed domains. Each compact child disk lies strictly inside every containing domain, so the containing cap's positive height has a positive minimum there. Choosing a smaller child height therefore separates overlapping graph caps. Different outer branches have disjoint domains.

The arc case is handled relative to the prescribed attaching arc: disjoint one-sided neighborhoods avoid the circle boundaries and can be made shallower than every containing circle cap. The complementary disk-boundary arc is permitted to lie freely in the ball, as required for a source boundary fan. Endpoints remain on the prescribed sphere arc. Thus caps attach along exactly their specified circles/arcs and their interiors are mutually disjoint. These arguments use finite positive minima and PL collars, not a blanket claim that arbitrary knots bound disjoint disks.

## Realization and pointwise control

I checked the incidence between cut face patches, edge ribbons, and sphere links in M3. A translated face corner meets the cubical vertex-ball boundary in an L-shaped polygonal arc. At longitudinal coordinate rho, each edge connector ends on that boundary and joins the correct face-arc endpoints. Positive transverse coordinates separate ribbon interiors from the incident inward-tangential face patches. The D < rho/10 bound separates ribbons belonging to distinct cube edges, including edges sharing a vertex.

Consequently the surface outside the balls is already embedded. Its boundary links follow the actual source corner fans; interval and circle fan links therefore give simple disjoint sphere arcs and circles before M2 is invoked. No argument based solely on Euler characteristic is substituted for this link check.

The source collar reparametrization preserves the longitudinal coordinate and absorbs the added ribbon into the original source collar. This avoids inserting new source material or changing its joins. The final text explicitly assembles the source corner frontier from face truncations and source edge-collar intervals: it lies within rho+eta < 2rho of the source corner. Extension of the boundary parametrization over a disk then respects all adjoining collars.

The three estimates are consistent: translation displacement at most D; edge-collar error at most 2eta+sqrt(2)D; corner error less than (2sqrt(2)+sqrt(3))rho < 5rho < epsilon. These bound F(x)-beta(x) for the same source point, rather than only Hausdorff distance between image sets. Face ranks survive on the unmodified interiors. The permission for caps to enter the cube is explicit and is not confused with an outside-only folding model.

D1 uses the disk case of the published validity criterion. An embedded PL disk has unknotted boundary and can be included as a face of the boundary of a one-sided regular-neighborhood 3-ball. The statement of the model distinguishes PL ambient isotopy from rigid-panel hinge motion. The section appropriately withholds the disk-validity inference for holed sources. The publication-wide verification of the precise ALL25 definitions and theorem citation remains a separate literature task; this review checked that their stated use is logically consistent with the construction.

## Section 6

The explicit H0/H1/V0/V1 frame rules correctly distinguish 180- and 90-degree joins. The three admissible full 2-by-2 turn patterns force a 2-by-4 lobe to have either the transverse-only map or one of eight independent longitudinal maps. The lobes share one square and no extra inter-lobe joins, giving 9 squared normalized maps. Their longitudinal normal sets intersect only in the shared normal/opposite pair; surjectivity forces both signs of each lobe's independent tangent direction, hence all three longitudinal turns in both lobes. This establishes uniqueness without trusting an exhaustive result file.

The two rectangles overlap in a full square, so their union is a disk, not a point-connected source. The disconnected repeated face consists of the two displayed dominoes. Seven monochrome components and twelve 90-degree joins follow directly from the lobe structure. The definition explicitly concerns retained square adjacency, not the literal closed-face preimage including lower-dimensional image pieces.

As a transcription check, a fresh standalone Python snippet parsed the 15-row table directly from the manuscript (without importing polycube), rebuilt all geometric joins, and checked both corner endpoints, six-face coverage, dense ranks per face, and cyclic chord nonalternation at every used cube edge. It found 15 cells and 20 joins and passed every test. The proposition makes no unsupported minimal-size or novelty claim and does not describe the example as nonfoldable.

## Main-proof references

The final reviewed `sections/05-main-theorem.md` has SHA-256 `d892bc454d53f118f33d7676e22d00d8cea3bfe21b6b378fce6fb4ef68a1d545`. Its Proposition C3 reference is correctly named. The final text now explicitly cites Theorem L7 for layers, Theorem M3 for realization, and Corollary D1 with ALL25 Theorem 3.4 for validity. These labels and scopes agree with their statements. The source-preservation claim agrees with both Sections 1 and 4.

## Amendment: standalone example evidence

Section 6 changed only its penultimate supporting-evidence paragraph; its proposition, analytic proof, frame/rank table, and eleven endpoint words are unchanged. The new paragraph points to `examples/README.md` rather than requiring the original repository's result files. I read the complete `examples/verify_counterexample.py`, the README, `verification.json`, and `test-evidence.json`. The current verifier hash is `d0b6f7e4b7f768cafd713fe92bed12568205a914942bc8718b9f8a23291abe90`, and the current `counterexample.json` hash is `c4c6523ce482e6ecad10ace1d7a517b51306c9e3295fb537fe12e8ba245f6a99`; both match the supplied evidence records.

The program independently generates 48 affine frames from cube-coordinate bit flips, reconstructs the fixed fifteen-cell source and its twenty joins, and enumerates maps using sound endpoint-compatibility domain filtering followed by exhaustive branching. It uses no face-coverage pruning or search cutoff. Its final checks require the complete 81-map histogram, the unique surjective map equal to the supplied frame table, dense strict ranks, all eleven reconstructed endpoint words, seven monochrome components, twelve bends, and the two stated disconnected dominoes. Input integer checks exclude JSON Booleans. Validation uses explicit exceptions and is not disabled by Python optimization. The relative default witness path and standard-library-only imports support the stated isolated execution model.

The author-recorded execution evidence reports equal normal and optimized isolated outputs, equal CPython 3.12 output, and four corruptions rejected in both normal and optimized modes. I checked the recorded outcomes and their source bindings; this amendment does not claim to have independently rerun those eight corruption processes. The standalone paragraph accurately describes the listed checks and recorded runs, and clearly leaves PL realization and disk topology to the manuscript. No original research sources or results were modified in making this amendment.

## Verdict and limits

The final Section 1 supplies the local-order-to-embedded-realization bridge and the disk validity implication with explicit construction and pointwise bounds. Section 6 supplies a self-contained finite supporting observation with a literal valid-layer witness. I found no remaining mathematical blocker in these texts. This does not independently establish the separate reduction to the complete finite colored-tree domain, the certificate's coverage, or priority over the literature.
