## 3. The complete finite certificate

Index the cube faces by \(0,\ldots,5\) with opposite pairs \((0,1)\), \((2,3)\), and \((4,5)\). A colored tree has a face color at each vertex, and the colors at the ends of every edge are adjacent, that is, distinct faces sharing a cube edge (Section 2). We also record the action of each symmetry on the eight cube vertices. This is a redundant, concrete representation: the 48 symmetries act faithfully on the faces.

**Lemma C1 (full-frame evaluation).** Let \(M\) be a member of a fixed toggle family, used as the base map, and let \(T\) be its contracted region tree, obtained from the original region tree by contracting the original arcs that are inactive in \(M\). The vertices of \(T\) are the regions of \(M\), with face colors \(c_v\), and its edges are the active original arcs of \(M\), which are exactly the whole bend arcs of \(M\) (see the paragraph after Lemma R2). Root \(T\), and let \(e=(p,v)\) be an edge of \(T\), with target cube edge \(E_e\) under \(M\). For a chosen bit vector \(b\) on the edges of \(T\), define cube isometries recursively by

\[
g_{\mathrm{root}}=\mathrm{id},\qquad
g_v=\begin{cases}
g_p,&\quad b_e=1,\\
g_p\circ\sigma_{E_e},&\quad b_e=0.
\end{cases}
\]

Apply \(g_v\) to the complete frames of \(M\) on every square in region \(v\). The result is a consistent map in which the joins along an edge \(e\) of \(T\) are 90-degree joins exactly when \(b_e=1\), and all other retained joins are 180-degree joins; its coverage is \(\{g_v(c_v):v\in V(T)\}\). After one global isometry restoring the fixed source square's frame, when necessary, it becomes the member of the same family whose active original arcs are exactly the edges \(e\) with \(b_e=1\), with the same number of covered faces.

**Proof.** On an interface endpoint \(x\in E_e\), either formula gives \(g_v(x)=g_p(x)\), since \(\sigma_{E_e}\) fixes both endpoints. The two incident face colors remain distinct for an active bit and become equal for an inactive bit. Internal joins of a region undergo one common isometry and remain consistent and inactive. The current-edge formulation of an actual sequence of toggles agrees with the recurrence because

\[
\sigma_{g(E)}=g\sigma_Eg^{-1},\qquad
\sigma_{g(E)}g=g\sigma_E.
\]

Thus ancestor transformations do not invalidate the use of the target edge \(E_e\) of \(M\) in the recurrence. No tangent-frame information is needed to identify that edge: the intersection of two adjacent cube faces is a unique edge. If the root region does not contain the fixed source square, apply one global isometry to restore that square's frame; this changes neither the number of covered faces nor any join status. Every original arc is then either an edge \(e\) of \(T\), active along its whole length exactly when \(b_e=1\), or an arc inactive in \(M\), whose joins lie inside one region of \(T\) and remain 180 degrees, as do all originally internal joins. The family member with these arc statuses therefore has the same root frame and the same join statuses, and uniqueness in Lemma R2 identifies the two maps. \(\square\)

The isometries \(g_v\) depend only on the rooted colored tree \((T,c)\) and on \(b\), since \(E_e\) is the common edge of the adjacent faces \(c_p\) and \(c_v\). For an abstract colored tree, the **full-frame evaluation** of a bit vector \(b\) is this recurrence together with the colors \(g_v(c_v)\). As in the proof, \(g_p(c_p)\) and \(g_v(c_v)\) differ exactly when \(b_e=1\); these edges are the active arcs of the evaluation. Because each \(\sigma_E\) is an involution, the rule \(g_v=g_p\sigma_{E_e}^{1-b_e}\) is equivalent to \(g_p=g_v\sigma_{E_e}^{1-b_e}\). Hence, for another root \(r'\), the recurrence gives \(g_{r'}^{-1}g_v\) in place of \(g_v\): a change of root moves all colors by one isometry and changes neither the number of covered faces nor any status.

### 3.1 The domain and its symmetry coverage

For each edge count \(a=5,\ldots,12\), generate the following inputs.

For paths, normalize the ordered endpoint colors to \((0,1)\) when they are opposite or \((0,2)\) when adjacent. These are the two orbits of distinct ordered face pairs under cube symmetries. Assign each internal vertex any of the other four colors and retain exactly the assignments with adjacent consecutive colors and six-color coverage.

For Y-shaped trees, distinguish the degree-three center and enumerate **all ordered positive arm-length triples** summing to \(a\). The three exclusive leaf colors are distinct. They either contain an opposite pair or contain no opposite pair. After an arm permutation and a cube symmetry, they are respectively \((0,1,2)\) or \((0,2,4)\). Assign the center and internal arm vertices any of the other three colors; retain exactly the adjacent, six-covering assignments. All ordered arm lengths are included, so permuting arms does not impose an unproved geometric ordering.

The opposite-pair representation of cube faces shows these are all possibilities: permutations of the three opposite pairs and independent swaps within each pair are exactly the 48 cube symmetries. For the Y case, three distinct colors cannot contain more than one complete opposite pair. The consumer additionally checks explicit normalization witnesses for all 30 ordered distinct leaf pairs and all 120 ordered distinct leaf triples. Symmetry duplicates within the normalized domain do not matter; the obligation is exhaustive coverage.

| Active arcs | Path patterns | Y patterns | Total |
|---:|---:|---:|---:|
| 5 | 16 | 22 | 38 |
| 6 | 60 | 78 | 138 |
| 7 | 196 | 264 | 460 |
| 8 | 552 | 708 | 1,260 |
| 9 | 1,488 | 1,874 | 3,362 |
| 10 | 3,892 | 4,608 | 8,500 |
| 11 | 10,028 | 11,282 | 21,310 |
| 12 | 25,696 | 26,774 | 52,470 |
| Total | 41,928 | 45,610 | 87,538 |

Table: Number of normalized path and Y-shaped domain inputs for each number of active arcs.

### 3.2 What the certificate proves

**Finite claim C2.** Every colored tree in this domain has a bit vector whose full-frame evaluation covers all six cube faces and has at most seven active arcs.

The supplement contains one explicit bit vector for every input. Its consumer regenerates the normalized domain recursively and requires exact equality of the certificate key set with the generated input set, rejecting omissions, additions, and duplicate records. It independently constructs the 48 opposite-preserving face permutations and derives their actions on cube vertices from three-face incidence. For each witness it checks that the record's parent array equals that of the regenerated tree, evaluates the recurrence of Lemma C1 on all eight cube vertices, and checks six-face coverage and that at most seven bits are active, in agreement with the recorded active count. These checks and the exact key-set equality are the substantive ones. The consumer also asserts the pointwise endpoint match at every edge and the selected active/inactive status. Each reflection \(\sigma_E\) is selected as the unique symmetry that fixes both endpoints of \(E\) and maps one incident face to the other, so these assertions hold for every bit vector once the reflection table is correct: they are consistency checks of the reflection (\(\sigma\)) table, not of the witnesses.

The verification records 87,538 patterns and 1,987,252 endpoint comparisons, two for each edge of each pattern; these comparisons are reflection-table consistency checks. Witness active counts are five for 72,982 patterns, six for 14,532, and seven for 24. In particular every input with eight through twelve arcs has a strict reduction.

The certificate was generated by a direct bit-vector search, separate from the primary minimum-cost dynamic program. The direct search examined 98,037,403 bit vectors. This generation count is provenance, not a premise required to trust a positive witness. The consumer does not invoke a solver, a compiler, or either producer. A mathematical reading of the domain enumeration and witness evaluator, together with successful execution, establishes the finite claim.

For additional diagnostics, the consumer checks the primary program's 80 minimal survivors: 38 with five arcs, 38 with six, and four with seven. It rejects all 4,080 cheaper assignments for these survivors. Minimality of these 80 examples is not needed for the universal upper bound C2. The output lists nine negative controls. Seven are semantic corruption controls, which exercise invalid coverage, active count, parent tree, original colors, full vertex reflection, leaf-orbit coverage, and a forged arm permutation. The other two, for a missing and an extra domain entry, are set-comparison illustrations: each compares the generated key set with a copy of the certificate key set with one key removed or one out-of-domain key added. The two compared sets differ by construction, so these two controls report a rejection without exercising the consumer's key-set checks; those checks, in the main loop, are what reject omissions and additions. The semantic controls detect specified failure modes, not every possible programming error.

### 3.3 Consequence for physical disks

**Proposition C3.** Every physical disk admitting a surjective consistent complete-frame map has a surjective member of the fixed toggle family of that map with at most seven active arcs; indeed every active-arc-minimal surjective member has at most seven, and a member's active original arcs are exactly its whole bend arcs.

**Proof.** Let \(M\) be an active-arc-minimal surjective member of the family; one exists because the family is finite and contains the given map. Let \(T\) be its contracted region tree, with face colors \(c\). Lemmas R3 and R6 give two through four leaves and five through twelve arcs. The four-leaf case has five arcs by Lemma R7. Otherwise \(T\) is a path or a Y tree; suppose that it has at least eight arcs.

By Section 3.1 there are a cube isometry \(h\) and an isomorphism \(\psi\) from \(T\) onto one of the enumerated trees (for a path, either orientation; for a Y tree, a suitable ordering of its arms) such that \(c'=h\circ c\circ\psi^{-1}\) has normalized leaf colors. Since \(h\) preserves face adjacency, six-face coverage and the exclusivity of leaf colors, \(c'\) is a domain input. By C2 it has a bit vector \(b'\) with at most seven active bits whose full-frame evaluation \(g'\) covers all six faces. Put \(b_e=b'_{\psi(e)}\), root \(T\) and \(\psi(T)\) at corresponding vertices (by the paragraph after Lemma C1, the root is immaterial), and let \(g\) be the full-frame evaluation of \(b\) on \((T,c)\). The target edges correspond, \(E'_{\psi(e)}=h(c_p)\cap h(c_v)=h(E_e)\), so the identity \(\sigma_{h(E)}=h\sigma_Eh^{-1}\) from the proof of Lemma C1 and induction from the root give \(g'_{\psi(v)}=hg_vh^{-1}\). Hence \(g'_{\psi(v)}(c'_{\psi(v)})=h(g_v(c_v))\). The evaluation of \(b\) therefore also covers all six faces, and \(b\) has as many active bits as \(b'\).

Lemma C1 with \(M\) as base map now gives a surjective member of the same family whose active original arcs are the at most seven edges \(e\) of \(T\) with \(b_e=1\), contradicting minimality. Thus every active-arc-minimal surjective member has at most seven active arcs. By the paragraph after Lemma R2, the active original arcs of any member are exactly its whole bend arcs. \(\square\)

This is the only exhaustive computational obligation in the main theorem. The argument reducing arbitrary physical disks to this domain is analytic, as is the downstream layer construction. The supplement documents its invocation, tested interpreter, data hashes, validation behavior, and fresh execution output. The finite certificate does not by itself establish any geometric or topological lemma.
