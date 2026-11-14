# 6. A finite obstruction to connected monochrome map selection

The following independent observation concerns selection of a consistent map, not nonfoldability. Here a **monochrome component** means a connected component of the retained cell-adjacency graph after deleting every join between different target faces. This is not the literal inverse image of a closed cube face, which can also contain edges and vertices of differently mapped squares. No novelty or minimum-size assertion is made.

**Proposition X1.** The ordinary disk source

\[
P=(\{0,1\}\times\{0,1,2,3\})\cup(\{1,2,3,4\}\times\{3,4\}),
\]

with all geometric joins retained, admits a valid folding onto the cube. It has exactly 81 consistent complete-frame maps after fixing the complete frame of the square \((0,0)\), exactly one of which is surjective. That surjective map has seven monochrome components and twelve retained 90-degree joins. In particular, no surjective consistent map has a single monochrome component on each target face.

**Proof.** First consider a complete \(2\times2\) block. Write a frame as \((n,u,v)\), its outward normal and its source-right/source-up tangent vectors, and let 0 denote a 180-degree join and 1 a 90-degree join. For an east (respectively north) step, from a square to the neighbor across its right (respectively top) side, the neighbor's frame is obtained from the square's frame by \(H_0\) or \(H_1\) (respectively \(V_0\) or \(V_1\)), the subscript being the bit of the join, where

\[
\begin{aligned}
H_0(n,u,v)&=(n,-u,v), &\quad H_1(n,u,v)&=(u,-n,v),\\
V_0(n,u,v)&=(n,u,-v), &\quad V_1(n,u,v)&=(v,u,-n).
\end{aligned}
\]

If \(a,b,c,d\) are the turn bits of the lower east step, the left north step, the upper east step, and the right north step, respectively, and \((n,u,v)\) is the frame of the lower-left square, consistency is exactly

\[
V_dH_a(n,u,v)=H_cV_b(n,u,v).
\]

Substitution in the four displayed formulas gives only

\[
(a,b,c,d)=(0,0,0,0),\ (0,1,0,1),\ (1,0,1,0).
\]

For clarity, when \(a=b=0\), equality of normals forces \(c=d=0\). When \((a,b)=(0,1)\) or \((1,0)\), it forces \((c,d)=(0,1)\) or \((1,0)\), respectively, and the full frames agree. When \(a=b=1\), the two possible equal-normal choices give unequal tangent vectors. This proves the \(2\times2\) assertion without relying on enumerated map files.

Apply it to the three overlapping \(2\times2\) blocks in a \(2\times4\) rectangle. Call a join transverse or longitudinal according as its step is parallel to a short or a long side of the rectangle; the six longitudinal joins form three separators of two parallel joins each. By the uniqueness argument in the proof of Lemma R2, a map is determined by the complete frame of one square and the turn bits of all joins. Conversely, given a frame and bits, propagation by the four displayed formulas and their inverses along the spanning tree formed by the four transverse joins and the three longitudinal joins of one long side assigns a frame to every square. Each of the three remaining joins closes exactly one \(2\times2\) block, so these frames form a consistent map exactly when every block has one of the three patterns above. Hence all four transverse joins have the same turn bit. If that bit is 1, every longitudinal join is 0, giving one map. If the transverse bit is 0, each of the three longitudinal separators independently has bit 0 or 1, with its two parallel joins having that same bit, giving eight maps. Thus a fixed corner frame extends in exactly nine ways.

Call \(\{0,1\}\times\{0,1,2,3\}\) the vertical lobe and \(\{1,2,3,4\}\times\{3,4\}\) the horizontal lobe of \(P\). They meet in the single square \((1,3)\), a corner square of each, and there are no additional joins between their other squares. Fix the complete frame of \((1,3)\). The two choices are independent, giving \(9^2=81\) maps. Fixing any other square's frame, in particular that of \((0,0)\) as in the statement, gives the same count: whole-cube isometries act freely and transitively on the 48 complete frames, and preserve consistency and face coverage.

The exceptional transverse-only map of a lobe covers two faces. The other lobe covers at most four, including the common-square face, so a surjective map must use the longitudinal family on both lobes. Let \(n\) be the common-square normal and \(u,v\) its tangent axes. In the longitudinal family the transverse joins are 180-degree joins. Since \(H_0\), \(V_0\), \(V_1\) and their inverses change the source-right tangent at most in sign, every frame of the vertical lobe has source-right tangent \(\pm u\); since \(V_0\), \(H_0\), \(H_1\) and their inverses change the source-up tangent at most in sign, every frame of the horizontal lobe has source-up tangent \(\pm v\). As a normal is orthogonal to both tangents, the vertical lobe has normals in \(\{\pm n,\pm v\}\), and the horizontal lobe has normals in \(\{\pm n,\pm u\}\). Covering all six faces requires each lobe to attain both signs of its own tangent normal: \(\pm v\) on the vertical lobe and \(\pm u\) on the horizontal lobe.

The common square \((1,3)\) is an end square of both lobes: it lies in the top row of the vertical lobe and in the left column of the horizontal lobe. In the longitudinal family both squares of a row of the vertical lobe, or of a column of the horizontal lobe, have the same normal, since \(H_0\) and \(V_0\) preserve the normal. Starting at the end containing \((1,3)\), three successive 90-degree turns have normal sequence \(n,d,-n,-d\), where \(d\in\{v,-v\}\) on the vertical lobe and \(d\in\{u,-u\}\) on the horizontal lobe. This is the only binary sequence of three turns attaining both \(d\) and \(-d\): with at most one 90-degree turn there is only one non-\(n\) normal; with two, adjacent turns give \(n,d,-n\) with one repetition, whereas the separated pattern 101 returns to \(n\) and never reaches \(-d\). Thus all three longitudinal turns must be 90 degrees in both lobes. This proves uniqueness of the surjective map.

The face opposite the shared-square face occurs in exactly the two separated dominoes

\[
\{(0,1),(1,1)\},\qquad\{(3,3),(3,4)\}.
\]

The common-square face has one connected three-square component, and the other four target faces each have one domino component. There are therefore seven monochrome components. Each lobe contributes three separators of two 90-degree joins, giving twelve such joins altogether.

It remains to prove that the source actually folds. First, \(P\) is homeomorphic to a closed disk; as Section 1.1 requires, this is checked on the quotient, not on the drawing. Place the cell \((i,j)\) on the unit square \([i,i+1]\times[j,j+1]\). All geometric joins are retained, and at every lattice point the squares of \(P\) containing it are consecutive in the four-sector star, so the retained joins identify all their corners there to a single vertex of \(P\). In particular, at the lattice points \((1,4)\) and \((2,3)\), where two squares of \(P\) meet only in a corner, these two squares are joined in this way through the square \((1,3)\). Hence the position map from \(P\) onto the union of its squares in the plane is a continuous bijection of a compact space onto a Hausdorff space, and so a homeomorphism. That union consists of the rectangles \([0,2]\times[0,4]\) and \([1,5]\times[3,5]\), which overlap in a square with nonempty interior; it is a planar disk, since it is star-shaped about an interior point of their overlap and has a simple polygonal boundary. For an explicit locally feasible surjective witness, encode cube vertices by \(x+2y+4z\) and use this table. Corner order is bottom-left, bottom-right, top-right, top-left; ranks increase away from the cube.

| Row | Cell | Complete frame | Rank |
|---:|---|---|---:|
| 0 | (0,0) | (0,1,3,2) | 0 |
| 1 | (0,1) | (2,3,7,6) | 0 |
| 2 | (0,2) | (6,7,5,4) | 0 |
| 3 | (0,3) | (4,5,1,0) | 0 |
| 4 | (1,0) | (1,0,2,3) | 1 |
| 5 | (1,1) | (3,2,6,7) | 1 |
| 6 | (1,2) | (7,6,4,5) | 1 |
| 7 | (1,3) | (5,4,0,1) | 1 |
| 8 | (1,4) | (1,0,4,5) | 2 |
| 9 | (2,3) | (4,6,2,0) | 0 |
| 10 | (2,4) | (0,2,6,4) | 1 |
| 11 | (3,3) | (6,7,3,2) | 2 |
| 12 | (3,4) | (2,3,7,6) | 3 |
| 13 | (4,3) | (7,5,1,3) | 0 |
| 14 | (4,4) | (3,1,5,7) | 1 |

The table agrees on both endpoints of every geometric join and uses dense strict ranks on each face. The following is a short complete check of the local order condition. At each used cube edge, label the listed joined row pairs A, B, C in order. The last column lists their endpoints in the cyclic layer order: increasing rank on the lexicographically smaller incident face (represented by its sorted vertex tuple), then decreasing rank on the other face. If all joined occurrences use only one incident face, list their ranks increasingly. Unpaired occurrences can be omitted.

| Cube edge | Joined row pairs, labeled A, B, C | Endpoint word |
|---|---|---|
| {0,1} | (7,8) | AA |
| {0,2} | (9,10) | AA |
| {0,4} | (7,9), (8,10) | ABBA |
| {1,3} | (0,4), (13,14) | AABB |
| {1,5} | (3,7) | AA |
| {2,3} | (0,1), (4,5), (11,12) | ABCCBA |
| {2,6} | (9,11), (10,12) | ABBA |
| {3,7} | (1,5), (11,13), (12,14) | BCCBAA |
| {4,5} | (2,3), (6,7) | ABBA |
| {5,7} | (2,6) | AA |
| {6,7} | (1,2), (5,6) | ABBA |

The unused cube edge has no retained connector. No word contains alternating endpoints of two different letters. Thus the orders are locally feasible. Corollary D1 supplies a valid folding of this disk source onto the cube. \(\square\)

The foldability of this source is not new: it also follows from [ALL25, Theorem 8.2]. By Lemma B1(a) and (b), \(P\) is a simply connected polyomino in the sense of [ALL25], and its bounding box is \([0,5]\times[0,5]\). Orient the boundary of \(P\) and the box clockwise, as in [ALL25, Section 8]. From the boundary vertex \((2,3)\), which does not lie on the box, the boundary of \(P\) first reaches the box at \((5,3)\) in the negative direction and at \((2,0)\) in the positive direction. The nearest corner of the box in the positive direction from \((5,3)\) and the nearest corner in the negative direction from \((2,0)\) are both \((5,0)\), so \((5,0)\) is a valid corner for \((2,3)\). Its horizontal and vertical distances from \((2,3)\) are both \(3\), so the hypothesis of that theorem, distance at least \(3\) in both directions, holds. The explicit witness above keeps the proof self-contained. The assertions about consistent maps and monochrome components do not depend on [ALL25, Theorem 8.2].

The accompanying standalone example package (directory `examples/`) contains the complete witness and a standard-library verifier. It generates all 48 cube frames, reconstructs all 20 retained joins, enumerates the 81 normalized maps under complete endpoint constraints, identifies the unique surjective map, and checks the eleven nonalternating endpoint words and the component and join counts. It runs from outside the research repository with Python isolated mode and site imports disabled. Recorded normal and optimized runs agree, and four corrupted witnesses are rejected in both modes. These checks support transcription and implementation reliability; the proof above does not require a catalog of larger sources or the original repository.

The proposition refutes only the universal requirement of six monochrome components. It provides neither a general bound on their number nor a nonfoldable source, and it does not settle the question whether some surjectively mappable polyomino has no valid folding.
