# Independent-pass prior-art and model-comparison review

Review date and cutoff: 5 November 2026. This is an AI review in the same
preparation workflow, not a human specialist opinion, external peer review,
or a guarantee of publication priority. No researchers were contacted.
The search sought counterevidence to novelty and checked the cited models
rather than accepting the manuscript's prior comparison at face value.

## Versions reviewed

| File | SHA-256 |
|---|---|
| `literature/theorem-comparison.md` | `3129f71a62d5b0f6d9cc8dcf5877a08c5437ebf0d4244aae2e73a2d212874bd8` |
| `sections/00-introduction.md` | `f95ab82fb250d8db6f1f48db2947f24cfe510de5b76068950430580102b8b2a8` |
| `sections/05-main-theorem.md` | `d892bc454d53f118f33d7676e22d00d8cea3bfe21b6b378fce6fb4ef68a1d545` |
| `sections/07-references.md` | `d911a913d371c5650fdceee6b414cba8043e6ccdaabef3fc97eeaee9bc3d2d73` |

The comparison file includes two precision amendments suggested during
this review: the 2018 algorithm's angle restriction is now explicit, and
Open Problem 9.2 is no longer said to contain an unstated “geometric”
qualifier. These amendments were read before the hash above was recorded. Section 5
was re-read after its construction and pointwise-proximity wording changed;
its attribution and existential scope remain consistent with this review.

## Assessment

No inspected primary source states the same arbitrary-physical-disk
consistent-map-to-valid-fold implication. The manuscript's cautious
assessment of a plausible new contribution is supported by this search.
The search does not prove priority. Its statement that the general holed
case remains outside the theorem is appropriate; so is the distinction
between existential map repair and realization of every prescribed map.
The corollary concerning the disk restriction of Question 4.9 follows if
the manuscript's mathematical theorem is correct. This literature review
is not a substitute for auditing that proof.

## Primary-source checks

### Published ALL25, rather than preprint numbering

The [JoCG publication record](https://jocg.org/index.php/jocg/article/view/4749)
confirms volume 16(1), pages 601–634, and publication on 16 November 2025.
The [published PDF](https://jocg.org/index.php/jocg/article/download/4749/4049/18445)
was checked through its saved published-text extraction, with journal
headers and printed pagination, supplemented by current publisher-indexed
text. The browser's direct PDF fetch returned a redirect loop.

- Question 4.9 asks whether a source can admit surjective pseudo-foldings
  yet have no valid surjective folding. The candidate addresses its disk
  restriction, allowing the map and orders to change.
- Theorem 8.2 gives sufficiency when an appropriate boundary point is at
  least three units away in each coordinate from a valid bounding-box
  corner. It is not the candidate's map-existence equivalence.
- Open Problem 9.2 asks for a complete characterization of simply connected
  foldable sources. The new theorem supplies an equivalence with a finite
  map-existence condition, but no direct geometric shape classification.
- Theorem 3.4 is the credited validity/containing-sphere/unlink equivalence;
  the manuscript uses its disk case.

The extraction read is `research/jocg-2025.txt`, SHA-256
`509dc2c007813527c567cdae396902dac255ef466714270df0d14b488376bfde`.
Its PDF is SHA-256
`96598c0b51382520994209d34c6f0fee92070fbb9960e8ab49dbb542b9bf8afd`.
No conclusion relies on transferring preprint theorem numbering.

### Earlier folding papers

[ABDD18, author PDF](https://erikdemaine.org/papers/PolyformFolding_IJCGA/paper.pdf),
Theorem 5, treats tree-shaped sources and constant-size target polycubes
under grid folds of ±90 degrees, with the stated target-edge restriction.
The following discussion explicitly does not extend that algorithm to
180-degree folds or general non-tree sources. Its extra-crease results
therefore do not supply the present fixed-grid disk theorem. The
[author bibliographic record](https://erikdemaine.org/papers/PolyformFolding_IJCGA/)
agrees with the manuscript's authors, journal, volume, year, and pages.

[AAAC21, author PDF](https://erikdemaine.org/papers/CubeFoldingHoles_CGTA/paper.pdf),
Section 4.3, gives the consistent-vertex-map necessary test; Section 5
asks about sufficiency. It does not prove the universal disk repair claim.
The [author bibliographic page](https://erikdemaine.org/papers/CubeFoldingHoles_CGTA/)
confirms the 2021 journal citation, despite the accepted-manuscript PDF's
2020 preparation date. Its source/motion discussion reinforces the need
to name the manuscript's PL model explicitly.

[LS25, arXiv v2](https://arxiv.org/abs/2510.18197)
concerns cooperating holes in rectangular sources. The primary arXiv record
lists submission on 21 October 2025 and revision on 22 October 2025.
Its abstract and relevant indexed theorem discussion did not supply the
candidate disk implication. This review did not re-audit that paper's full
proof, and makes no stronger exclusion claim.

### The connected separating-curve theorem

The [HN18 publisher article](https://www.sciencedirect.com/science/article/pii/S0304397515012207)
was read through its indexed full Section 3 after direct fetches returned
403. Published Theorem 4 explicitly handles connected partitioned planar
graphs, without requiring biconnectivity. Its constructive proof obtains
a separating curve in the supplied disjunctive, splitter-free embedding,
not merely in some unrelated embedding. This supports the comparison's
connected-graph attribution. The older technical-report restriction must
not replace this published statement. Journal volume 725, pages 79–98,
2018, and DOI 10.1016/j.tcs.2015.12.039 agree with the reference entry.
This check verifies the cited result's scope, not every hypothesis of its
application in Section 4.

### Recent counterevidence search

The [3 November 2026 primary arXiv record](https://arxiv.org/abs/2611.04246)
concerns common nets for four or five distinct boxes. Its abstract does
not assert the universal layered unit-cube disk implication. This was an
abstract-level screen, not a full-paper audit.

I inspected the thirteen-record metadata file `literature/arxiv-query.json`
retrieved by the coordinating review, including the 2026 hiccup-sequence
and common-box-net titles. I did not independently rerun that API query;
its detailed abstract screening is separately logged by that review.
The independent web searches below did not identify another same-model
theorem. A current author/puzzle page is contextual evidence only, not a
proof that no unpublished result exists.

## Actual independent searches

The following query strings were submitted during this pass (quotes are
search syntax, not quotations from a paper):

- `"polyominoes" "consistent" "simply connected" cube`
- `"polyominoes" "pseudo-folding" disk`
- `"Folding polyominoes into cubes" 2026 theorem`
- `"polyominoes" "surjective" disk folding`
- `"cube folding" "simply-connected" 2025 2026`
- `"cube" "surjective consistent" polyomino`
- `"polyomino" "disk" "pseudo" folding theorem`
- `"polyominoes" "cube" "2026" folding -site:themoonlight.io -site:researchgate.net`
- `"polyomino" "consistent mapping" folding theorem simply`
- `"polyomino" "pseudo-foldings" -site:themoonlight.io`
- `"simply connected" "cube" "consistent map"`
- `"simply-connected polyominoes" folding theorem -site:themoonlight.io`
- `"surjective pseudo-foldings" -site:themoonlight.io`
- `site:florian-lehner.net polyomino cube 2026`
- `"Folding polyominoes into cubes" "Question 4.9"`
- `"Folding polyominoes into cubes" "Open Problem 9.2"`
- `"Simpler algorithms for testing two-page book embedding" "Theorem 4"`
- `site.sciencedirect.com/science/article/pii/S0304397515012207 "Theorem 4" "connected partitioned graph"`

Primary publication pages, author copies, arXiv records, and the published
JoCG extraction were inspected. Secondary result snippets were used only
for discovery, not to establish theorem statements. Exact-phrase searches
sometimes returned irrelevant results; their failure is not evidence of
nonexistence. The author homepage's dynamic publication content was not
fully exposed by the browser text reader, which further limits that check.

## Limits and disposition

No blocking prior-art or model-comparison error was found in the hashed
files after the two precision amendments. The references identify the
relevant established ingredients instead of claiming them as new. A
qualified human specialist could still identify an overlooked equivalent
formulation, unpublished result, or a stronger interpretation of an older
paper. No MathSciNet/zbMATH subscription search or human response is claimed
by this independent pass. “First ever” and unqualified priority language
would remain unsupported.

The review's cutoff is 5 November 2026. Later publications, changed source
versions, and edits to the hashed manuscript files require a fresh check.
