"""Implementation of the inductive (straight-cut) proof in proof_v2.md.

construct(cells, J, banks) follows the written proof step by step:
  * Theorem L2* (top level, Sec. 5): choose a partition P satisfying (G1),
    (G2) and admissible markers rho (red start) and beta (blue start).
  * Lemma S (solve, Sec. 3): slide markers to P-mixed positions, choose a
    separating cut by Lemma C (Case 1: a cut ending at a mixed joint
    position; Case 2: the cut supplied by Lemma K2, built constructively by
    k2_cut exactly as in the proof of K2), split Q into Q1, Q2 (Lemma K1),
    give the subproblems the inherited and transition markers with the tie
    flags of Sec. 3.2, and return O1 ++ O2 (Sec. 3.3).
No search over orders and no search over cuts is performed.

Changes from impl.py (referee reports):
  * Lemma K2 is implemented constructively (k2_cut), with the assertions of
    the written proof (C' contained in C'', extension C'_2 perpendicular and
    inside Q2, separation of a and b); the old search over cuts is gone.
  * Lemma C Case 1 with markers in different stretches moves only the marker
    whose stretch has a mixed joint position to it; the other marker goes to
    the first mixed position of its stretch (any mixed position is allowed).
  * With L2DEBUG=1 the Claim 2 interval identities
        I_R = (I_R^1 restricted to alpha_1) . (I_R^2 restricted to alpha_2),
        I_B = (I_B^2 restricted to alpha_2) . (I_B^1 restricted to alpha_1),
    the position of the cut block inside I_R^i / I_B^i, the marker
    convention after Relabel (coincident markers at p with rho first or at q
    with beta first) and the full Lemma S conclusion are asserted at every
    recursion level.
STATS counts Lemma C branches and K2 extensions (instrumentation only).
"""
import os
from collections import defaultdict, Counter

DEBUG = bool(os.environ.get('L2DEBUG'))
STATS = Counter()

PARTS = ({('V', 0): 'R', ('H', 0): 'R', ('V', 1): 'B', ('H', 1): 'B'},
         {('V', 0): 'R', ('H', 1): 'R', ('V', 1): 'B', ('H', 0): 'B'})


def port_edge(c, p):
    x, y = c
    return {1: ('V', x % 2), 3: ('V', (x - 1) % 2), 2: ('H', y % 2), 0: ('H', (y - 1) % 2)}[p]


def join_edge(cells, a, d):
    x, y = cells[a]
    return ('V', x % 2) if d == 1 else ('H', y % 2)


def corner_xy(c, s):
    x, y = c
    return ((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1))[s]


def is_mixed(XY, k):
    """P0: pure = (odd,odd),(even,even); P1: pure = (odd,even),(even,odd)."""
    return (XY[0] + XY[1]) % 2 == (1 if k == 0 else 0)


class Region:
    """A physical disk: cell indices S (global), retained joins Jq among them."""

    def __init__(self, cells, S, Jq):
        self.cells, self.S, self.Jq = cells, sorted(S), list(Jq)
        par = {}
        for i in self.S:
            for s in range(4):
                par[4 * i + s] = 4 * i + s

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        glued = set()
        for a, b, d in self.Jq:
            if d == 1:
                par[find(4 * a + 1)] = find(4 * b + 0); par[find(4 * a + 2)] = find(4 * b + 3)
                glued |= {(a, 1), (b, 3)}
            else:
                par[find(4 * a + 3)] = find(4 * b + 0); par[find(4 * a + 2)] = find(4 * b + 1)
                glued |= {(a, 2), (b, 0)}
        self.find = find
        self.cnt = Counter(find(4 * i + s) for i in self.S for s in range(4))
        hes = {}
        for i in self.S:
            for s in range(4):
                if (i, s) not in glued:
                    hes[(i, s)] = (find(4 * i + s), find(4 * i + (s + 1) % 4))
        start = defaultdict(list)
        for hh, (u, v) in hes.items():
            start[u].append(hh)
        assert all(len(v) == 1 for v in start.values()), 'not a disk (vertex link)'
        h0 = min(hes); W = [h0]
        while True:
            nxt = start[hes[W[-1]][1]][0]
            if nxt == h0:
                break
            W.append(nxt)
        assert len(W) == len(hes), 'boundary not a single circle'
        self.W = W
        self.L = len(W)
        self.idx = {hh: t for t, hh in enumerate(W)}
        self.bclass = {hes[hh][0] for hh in W}
        self.cellat = {cells[i]: i for i in self.S}
        self.jset = {(a, b, d) for a, b, d in self.Jq}

    # position t = the boundary vertex occurrence between W[t-1] and W[t]
    def pos_class(self, t):
        i, s = self.W[t % self.L]
        return self.find(4 * i + s)

    def pos_xy(self, t):
        i, s = self.W[t % self.L]
        return corner_xy(self.cells[i], s)

    def joint(self, t):
        return self.cnt[self.pos_class(t)] >= 2

    def interior_class(self, c):
        return c not in self.bclass

    def cut_of(self, j):
        """Maximal straight run of joins through j whose interior vertices are
        interior (full-star) vertices; returns a frozenset of joins."""
        cells, F = self.cells, self.find
        a, b, d = j
        run = [j]
        for direction in (+1, -1):
            cur = j
            while True:
                ca, cb, cd = cur
                x, y = cells[ca]
                if cd == 1:   # vertical side x+1; ends: corner 2 (top) / 1 (bottom) of ca
                    end = F(4 * ca + (2 if direction > 0 else 1))
                    nxt = ((x, y + direction), (x + 1, y + direction))
                else:         # horizontal side y+1; ends: corner 2 (right) / 3 (left) of ca
                    end = F(4 * ca + (2 if direction > 0 else 3))
                    nxt = ((x + direction, y), (x + direction, y + 1))
                if not self.interior_class(end):
                    break
                na, nb = self.cellat[nxt[0]], self.cellat[nxt[1]]
                cur = (na, nb, cd)
                assert cur in self.jset, 'full star without its join'
                run.append(cur)
        return frozenset(run)

    def components(self, removed):
        nb = defaultdict(list)
        for a, b, d in self.Jq:
            if (a, b, d) not in removed:
                nb[a].append(b); nb[b].append(a)
        comp = {}
        for s0 in self.S:
            if s0 in comp:
                continue
            comp[s0] = s0; st = [s0]
            while st:
                x = st.pop()
                for y in nb[x]:
                    if y not in comp:
                        comp[y] = s0; st.append(y)
        return comp


def hcol(cells, h, k):
    return PARTS[k][port_edge(cells[h[0]], h[1])]


def red_interval(L, tr, tb, rfirst):
    """Halfedge indices of I_R (from position tr forward to position tb)."""
    if tr == tb:
        return [] if rfirst else [(tr + i) % L for i in range(L)]
    return [(tr + i) % L for i in range((tb - tr) % L)]


def blue_interval(L, tr, tb, rfirst):
    if tr == tb:
        return [(tb + i) % L for i in range(L)] if rfirst else []
    return [(tb + i) % L for i in range((tr - tb) % L)]


def check_hyp(cells, R, Sigma, tr, tb, rfirst, k):
    W, L = R.W, R.L
    for t in red_interval(L, tr, tb, rfirst):
        if W[t] in Sigma:
            assert hcol(cells, W[t], k) == 'R', 'hypothesis: blue halfedge in red interval'
    for t in blue_interval(L, tr, tb, rfirst):
        if W[t] in Sigma:
            assert hcol(cells, W[t], k) == 'B', 'hypothesis: red halfedge in blue interval'


def verify_S(cells, R, Sigma, tr, tb, rfirst, k, order):
    """Full conclusion of Lemma S (merged pages)."""
    rank = {c: i for i, c in enumerate(order)}
    assert sorted(order) == R.S
    arcs = {'R': [], 'B': []}
    for a, b, d in R.Jq:
        lo, hi = sorted((rank[a], rank[b]))
        arcs[PARTS[k][join_edge(cells, a, d)]].append((lo, hi))
    for col in 'RB':
        A = arcs[col]
        for i in range(len(A)):
            for j in range(i + 1, len(A)):
                (a, b), (c, d) = A[i], A[j]
                assert not (a < c < b < d or c < a < d < b), 'S(i) alternation'
    for hh in Sigma:
        m = rank[hh[0]]
        for lo, hi in arcs[hcol(cells, hh, k)]:
            assert not (lo < m < hi), 'S(ii) exposure'
    W, L = R.W, R.L
    seq = [rank[W[t][0]] for t in red_interval(L, tr, tb, rfirst) if W[t] in Sigma]
    assert all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1)), 'S(iii) red not increasing'
    seq = [rank[W[t][0]] for t in blue_interval(L, tr, tb, rfirst) if W[t] in Sigma]
    assert all(seq[i] >= seq[i + 1] for i in range(len(seq) - 1)), 'S(iii) blue not decreasing'


class ProofGap(Exception):
    pass


def join_dir(j):
    return j[2]


def k2_cut(cells, S, Jq, a, b, depth=0):
    """Lemma K2, constructively, following its written proof.
    Returns a cut of the region (S, Jq) having cells a != b on different sides.
    Take a cut C (through the first join).  If it separates a, b, done.
    Otherwise a, b lie in one side Q1; recurse to get a cut C' of Q1; the cut
    C'' of Q containing C' separates a and b (Cases 1 and 2 of the proof)."""
    STATS['k2_calls'] += 1
    R = Region(cells, S, Jq)
    C = R.cut_of(R.Jq[0])
    comp = R.components(C)
    if comp[a] != comp[b]:
        return C
    X = comp[a]
    S1 = [c for c in S if comp[c] == X]
    J1 = [j for j in Jq if j not in C and comp[j[0]] == X]
    assert len(S1) < len(S)
    Cp = k2_cut(cells, S1, J1, a, b, depth + 1)
    Cpp = R.cut_of(next(iter(Cp)))           # the cut of Q containing C'
    if not Cp <= Cpp:
        raise ProofGap("K2: C' not contained in a cut of Q")
    ext = Cpp - Cp
    if ext:
        # Case 2: C' ends at an interior vertex v of C, arriving perpendicular,
        # and C'' = C' + C'_2 with C'_2 a run of joins of Q2.
        STATS['k2_case2'] += 1
        if join_dir(next(iter(Cp))) == join_dir(next(iter(C))):
            raise ProofGap('K2: extension of a cut collinear with C')
        if any(comp[j[0]] == X or comp[j[1]] == X for j in ext):
            raise ProofGap("K2: C'_2 leaves Q2")
    else:
        STATS['k2_case1'] += 1
    comp2 = R.components(Cpp)
    if comp2[a] == comp2[b]:
        raise ProofGap("K2: C'' does not separate")
    return Cpp



def claim2_check(cells, R, Sigma, tr, tb, rfirst, alpha, beta, R1, R2, cut1, cut2,
                 ccol, m1, m2, sels):
    """DEBUG: the interval bookkeeping of Sec. 3.2 (Claim 2 table).
    With sels None: full halfedge sequences before slides; otherwise the
    selected subsequences after slides."""
    W, L = R.W, R.L
    # marker convention after Relabel: coincident markers at p with rho first,
    # or at q with beta first (p: walk leaves alpha_1, q: walk enters alpha_1)
    if tr == tb:
        if rfirst:
            assert W[(tr - 1) % L] in alpha and W[tr] in beta, 'tie: rho first not at p'
        else:
            assert W[(tr - 1) % L] in beta and W[tr] in alpha, 'tie: beta first not at q'

    def seq(Rs, t1, t2, rf, red, sel):
        ts = red_interval(Rs.L, t1, t2, rf) if red else blue_interval(Rs.L, t1, t2, rf)
        return [Rs.W[t] for t in ts if sel is None or Rs.W[t] in sel]
    s0 = None if sels is None else Sigma
    s1 = None if sels is None else sels[0]
    s2 = None if sels is None else sels[1]
    IR = seq(R, tr, tb, rfirst, True, s0)
    IB = seq(R, tr, tb, rfirst, False, s0)
    IR1 = seq(R1, m1[0], m1[1], m1[2], True, s1)
    IB1 = seq(R1, m1[0], m1[1], m1[2], False, s1)
    IR2 = seq(R2, m2[0], m2[1], m2[2], True, s2)
    IB2 = seq(R2, m2[0], m2[1], m2[2], False, s2)
    strip = lambda s, blk: [hh for hh in s if hh not in blk]
    assert IR == strip(IR1, cut1) + strip(IR2, cut2), 'Claim 2: I_R'
    assert IB == strip(IB2, cut2) + strip(IB1, cut1), 'Claim 2: I_B'
    k1, k2 = len(cut1), len(cut2)
    if ccol == 'R':   # kappa_1 ends I_R^1 (p -> q); kappa_2 starts I_R^2 (q -> p)
        assert set(IR1[len(IR1) - k1:]) == cut1 and set(IR2[:k2]) == cut2, 'Claim 2: red cut block'
        assert not (set(IB1) & cut1) and not (set(IB2) & cut2)
    else:             # kappa_1 starts I_B^1 (p -> q); kappa_2 ends I_B^2 (q -> p)
        assert set(IB1[:k1]) == cut1 and set(IB2[len(IB2) - k2:]) == cut2, 'Claim 2: blue cut block'
        assert not (set(IR1) & cut1) and not (set(IR2) & cut2)


def solve(cells, S, Jq, Sigma, tr, tb, rfirst, k):
    """Lemma S.  Markers are positions of the walk of Q=(S,Jq); rfirst breaks
    ties (tr==tb): True means rho precedes beta (empty red interval)."""
    if len(S) == 1:
        return list(S)
    R = Region(cells, S, Jq)
    W, L = R.W, R.L
    Sigma = {hh for hh in Sigma if hh in R.idx}
    inS = [W[t] in Sigma for t in range(L)]
    if DEBUG:
        check_hyp(cells, R, Sigma, tr, tb, rfirst, k)

    # ---- stretches -------------------------------------------------------
    def stretch(t):
        """(s0, positions) : maximal Sigma-free arc of positions containing t,
        listed in walk order from its first position s0."""
        if not any(inS):
            return None, [(t + i) % L for i in range(L)]
        s0 = t
        while not inS[(s0 - 1) % L]:
            s0 = (s0 - 1) % L
        P = [s0]
        while not inS[P[-1]]:
            P.append((P[-1] + 1) % L)
        return s0, P

    s0r, Pr = stretch(tr)
    s0b, Pb = stretch(tb)
    shared = set(Pr) == set(Pb)

    # ---- S0: normalise markers to mixed vertices ------------------------
    mixed = lambda t: is_mixed(R.pos_xy(t), k)
    if shared:
        if s0r is None:
            rho_first = rfirst
        else:
            off = lambda t: (t - s0r) % L
            rho_first = off(tr) < off(tb) if tr != tb else rfirst
        cand = [t for t in Pr if mixed(t)]
        if not cand:
            raise ProofGap('inadmissible shared stretch')
        jm = [t for t in cand if R.joint(t)]
        step1 = bool(jm)
        if jm:
            w = jm[0]
            tr = tb = w; rfirst = rho_first
        else:
            # all mixed vertices of the stretch are non-joint: put the two
            # markers on mixed vertices of two different cells if possible,
            # keeping their order along the stretch (Cand is in walk order)
            e1 = cand[0]
            other = [t for t in cand if W[t][0] != W[e1][0]]
            if other:
                e2 = other[0]
                tr, tb = (e1, e2) if rho_first else (e2, e1)
            else:
                tr = tb = e1; rfirst = rho_first
    else:
        cr = [t for t in Pr if mixed(t)]
        cb = [t for t in Pb if mixed(t)]
        if not cr or not cb:
            raise ProofGap('inadmissible stretch')
        jr = [t for t in cr if R.joint(t)]
        jb = [t for t in cb if R.joint(t)]
        # Lemma C, Case 1: the marker whose stretch has a mixed joint position
        # goes there; the other marker goes to any mixed position of its own
        # stretch (we take the first).  Case 2: both go to first mixed ones.
        if jr:
            tr, tb, w = jr[0], cb[0], jr[0]
        elif jb:
            tr, tb, w = cr[0], jb[0], jb[0]
        else:
            tr, tb, w = cr[0], cb[0], None
        step1 = w is not None

    # ---- S1: a separating straight cut (Lemma C) ------------------------
    STATS['solve'] += 1
    cut = None
    if step1:
        STATS['case1'] += 1
        wc = R.pos_class(w)
        F = R.find
        for (a, b, d) in R.Jq:   # a join at w: its side has w as an endpoint
            ends = (F(4 * a + 1), F(4 * a + 2)) if d == 1 else (F(4 * a + 3), F(4 * a + 2))
            if wc in ends:
                cut = R.cut_of((a, b, d)); break
        assert cut is not None
        comp = R.components(cut)
        if DEBUG:   # w is an endpoint of the cut: both walk halfedges at w on different sides
            assert comp[W[(w - 1) % L][0]] != comp[W[w][0]], 'Case 1: w not a cut endpoint'
    else:
        STATS['case2'] += 1
        cR, cB = W[tr][0], W[tb][0]
        assert W[(tr - 1) % L][0] == cR and W[(tb - 1) % L][0] == cB
        if cR == cB:
            # Reachable only in the shared-stretch subcase the proof shows to
            # be contradictory (two non-joint mixed corners of one cell would
            # isolate it); in the non-shared case cr[0] != cb[0] are distinct
            # non-joint mixed corners, so cR == cB cannot occur there either.
            raise ProofGap('Lemma C contradiction case reached')
        cut = k2_cut(cells, S, Jq, cR, cB)      # Lemma K2, constructive
        comp = R.components(cut)
        assert comp[cR] != comp[cB]

    side = [comp[W[t][0]] for t in range(L)]
    roots = sorted(set(comp.values()))
    assert len(roots) == 2, 'cut does not split into two pieces'

    def sides(t):
        return {side[(t - 1) % L], side[t]}
    # assign rho and beta to different closed arcs
    sr, sb = sides(tr), sides(tb)
    if tr == tb:
        assert len(sr) == 2, 'markers not separated'
        first, second = side[(tr - 1) % L], side[tr]
        X1, X2 = (first, second) if rfirst else (second, first)
    else:
        opts = [(x, y) for x in sorted(sr) for y in sorted(sb) if x != y]
        assert opts, 'markers not separated'
        X1, X2 = opts[0]
    S1 = [c for c in S if comp[c] == X1]
    S2 = [c for c in S if comp[c] == X2]
    alpha = {W[t] for t in range(L) if side[t] == X1}
    beta = {W[t] for t in range(L) if side[t] == X2}
    J1 = [j for j in Jq if j not in cut and comp[j[0]] == X1]
    J2 = [j for j in Jq if j not in cut and comp[j[0]] == X2]

    def cut_he(c_is_in):
        out = set()
        for a, b, d in cut:
            if c_is_in(a):
                out.add((a, 1 if d == 1 else 2))
            else:
                out.add((b, 3 if d == 1 else 0))
        return out
    cut1 = cut_he(lambda a: comp[a] == X1)
    cut2 = cut_he(lambda a: comp[a] == X2)
    ccol = PARTS[k][join_edge(cells, next(iter(cut))[0], next(iter(cut))[2])]

    R1, R2 = Region(cells, S1, J1), Region(cells, S2, J2)

    def inherit(Rsub, arc, t):
        """position in Rsub's walk of the inherited marker at Q-position t"""
        if W[t] in arc:
            return Rsub.idx[W[t]]
        assert W[(t - 1) % L] in arc
        return (Rsub.idx[W[(t - 1) % L]] + 1) % Rsub.L

    def after_block(Rsub, block):
        for t in range(Rsub.L):
            if Rsub.W[(t - 1) % Rsub.L] in block and Rsub.W[t] not in block:
                return t
        raise AssertionError

    def before_block(Rsub, block):
        for t in range(Rsub.L):
            if Rsub.W[t] in block and Rsub.W[(t - 1) % Rsub.L] not in block:
                return t
        raise AssertionError

    Sig1 = (Sigma & alpha) | cut1
    Sig2 = (Sigma & beta) | cut2
    tr1 = inherit(R1, alpha, tr)
    tb2 = inherit(R2, beta, tb)
    # ---- Sec. 3.2: transition endpoint and new markers (before slides) ---
    if ccol == 'R':           # transition endpoint q (walk passes alpha_2 -> alpha_1)
        tb1, rf1 = after_block(R1, cut1), False     # beta_1 = q_1, beta first
        tr2, rf2 = before_block(R2, cut2), False    # rho_2 = q_2, beta first
    else:                     # blue cut: transition endpoint p (alpha_1 -> alpha_2)
        tb1, rf1 = before_block(R1, cut1), True     # beta_1 = p_1, rho first
        tr2, rf2 = after_block(R2, cut2), True      # rho_2 = p_2, rho first

    if DEBUG:
        claim2_check(cells, R, Sigma, tr, tb, rfirst, alpha, beta, R1, R2, cut1, cut2,
                     ccol, (tr1, tb1, rf1), (tr2, tb2, rf2), None)

    # ---- slides at a pure transition endpoint (Claim 1) ------------------
    if ccol == 'R':
        if not is_mixed(R1.pos_xy(tb1), k):          # slide beta_1 forward over h+
            assert R1.W[tb1] in alpha
            if R1.W[tb1] in Sig1:
                raise ProofGap('pure transition endpoint with selected halfedge')
            tb1 = (tb1 + 1) % R1.L
        if not is_mixed(R2.pos_xy(tr2), k):          # slide rho_2 backward over h-
            if R2.W[(tr2 - 1) % R2.L] in Sig2:
                raise ProofGap('pure transition endpoint with selected halfedge')
            tr2 = (tr2 - 1) % R2.L
    else:
        if not is_mixed(R1.pos_xy(tb1), k):          # slide beta_1 backward over g-
            if R1.W[(tb1 - 1) % R1.L] in Sig1:
                raise ProofGap('pure transition endpoint with selected halfedge')
            tb1 = (tb1 - 1) % R1.L
        if not is_mixed(R2.pos_xy(tr2), k):          # slide rho_2 forward over g+
            if R2.W[tr2] in Sig2:
                raise ProofGap('pure transition endpoint with selected halfedge')
            tr2 = (tr2 + 1) % R2.L

    if DEBUG:
        claim2_check(cells, R, Sigma, tr, tb, rfirst, alpha, beta, R1, R2, cut1, cut2,
                     ccol, (tr1, tb1, rf1), (tr2, tb2, rf2), (Sig1, Sig2))
        for (Rs, t1, t2) in ((R1, tr1, tb1), (R2, tr2, tb2)):
            assert is_mixed(Rs.pos_xy(t1), k) and is_mixed(Rs.pos_xy(t2), k), 'new marker not mixed'

    O1 = solve(cells, S1, J1, Sig1, tr1, tb1, rf1, k)
    O2 = solve(cells, S2, J2, Sig2, tr2, tb2, rf2, k)
    order = O1 + O2
    if DEBUG:
        verify_S(cells, R, Sigma, tr, tb, rfirst, k, order)
    return order


def construct(cells, J, banks):
    n = len(cells)
    S = list(range(n))
    R = Region(cells, S, J)
    W, L = R.W, R.L
    Sigma = {hh for B in banks for hh in B}
    bank_of = {hh: bi for bi, B in enumerate(banks) for hh in B}
    if n == 1:
        return [0]
    sel = [t for t in range(L) if W[t] in Sigma]
    for k in (0, 1):
        cols = [hcol(cells, W[t], k) for t in sel]
        changes = sum(1 for i in range(len(cols)) if cols[i] != cols[i - 1])
        if changes > 2:
            continue
        if changes == 2:
            # rho before the first red after a blue; beta before the first blue after a red
            m = len(sel)
            tr = next(sel[i] for i in range(m) if cols[i] == 'R' and cols[i - 1] == 'B')
            tb = next(sel[i] for i in range(m) if cols[i] == 'B' and cols[i - 1] == 'R')
            return solve(cells, S, J, Sigma, tr, tb, True, k)
        # monochromatic or empty: an inter-bank gap containing a P-mixed vertex
        if not sel:
            t = next(t for t in range(L) if is_mixed(R.pos_xy(t), k))
            return solve(cells, S, J, Sigma, t, t, True, k)
        col = cols[0]
        m = len(sel)
        for i in range(m):
            a, b = sel[i - 1], sel[i]          # consecutive selected halfedges
            gap = [(a + 1 + u) % L for u in range((b - a - 1) % L + 1)]  # positions a+1..b
            if (b - a) % L == 1 and bank_of[W[a]] == bank_of[W[b]]:
                continue                        # interior of a bank
            mx = [t for t in gap if is_mixed(R.pos_xy(t), k)]
            if mx:
                t = mx[0]
                return solve(cells, S, J, Sigma, t, t, col == 'B', k)
    raise ProofGap('hypothesis of Theorem L2* not satisfied')
