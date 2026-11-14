"""Standalone test harness for constructive proofs of Lemma L2 (cofacial bank orders).

Standard library only.  Usage:
    python3 l2harness.py CANDIDATE.py N SEED [NMAX] [CASES]
CANDIDATE.py must define
    construct(cells, J, banks) -> list of cell indices (lowest layer first)
where
    cells : list of (x, y) lower-left lattice coordinates of unit cells
    J     : list of retained joins (a, b, d): cell b is the east (d=1) or
            north (d=2) neighbour of cell a.  Unlisted adjacencies are slits.
    banks : list of banks; a bank is a list of (cell_index, port) in boundary-
            walk order, port 0=S, 1=E, 2=N, 3=W.  All halfedges are unjoined.
The region is a disk (checked) and all cells map to one face with the
all-flip (checkerboard) frames.  Target cube edge of a port/join (parity):
    east port of (x,y), join (x,y)-(x+1,y): ('V', x%2)
    west port of (x,y):                     ('V', (x-1)%2)
    north port of (x,y), join (x,y)-(x,y+1): ('H', y%2)
    south port of (x,y):                     ('H', (y-1)%2)
V0/V1 are opposite square edges, H0/H1 opposite; every V is adjacent to every H.

CASES (comma list, default a,b1,b2,g):
  a  : at most one bank per target edge, banks need not be outward (L2(a)).
  b1 : all halfedges outward; <=4 banks, one target edge repeated at most twice.
  b2 : all halfedges outward; any number of banks on one edge + at most one other.
  g  : GENERAL (stronger than the manuscript): any disjoint banks, not
       necessarily outward, such that for SOME partition of the four target
       edges into two adjacent pairs ({V0,H0}|{V1,H1} or {V0,H1}|{V1,H0}) each
       merged class is cyclically consecutive in the boundary-walk order of
       the selected halfedges.
Checked conclusions (all cases): (1) for each target edge, flips pairwise
non-alternating; (2) every selected halfedge's parent is not strictly between
the endpoints of any flip on that halfedge's target edge (exposure); (3) every
bank's parents are monotone in the returned order; (4) banks on the same
target edge have separated parent sets (all of one before all of the other).
"""
import random, sys, json, time, importlib.util, traceback
from collections import defaultdict
from itertools import combinations

# ------------------------------------------------------------------ sources
def joins_of(cells, slits=frozenset()):
    idx = {c: i for i, c in enumerate(cells)}
    J = []
    for i, (x, y) in enumerate(cells):
        for d, (dx, dy) in ((1, (1, 0)), (2, (0, 1))):
            j = idx.get((x + dx, y + dy))
            if j is not None and frozenset(((x, y), (x + dx, y + dy))) not in slits:
                J.append((i, j, d))
    return J

def _corner_classes(cells, J):
    n = len(cells); par = list(range(4 * n))
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    glued = set()
    for a, b, d in J:
        if d == 1:
            par[find(4*a+1)] = find(4*b+0); par[find(4*a+2)] = find(4*b+3); glued |= {(a, 1), (b, 3)}
        else:
            par[find(4*a+3)] = find(4*b+0); par[find(4*a+2)] = find(4*b+1); glued |= {(a, 2), (b, 0)}
    return find, glued

def is_disk(cells, J):
    n = len(cells); find, glued = _corner_classes(cells, J)
    V = len({find(k) for k in range(4 * n)}); E = 4 * n - len(J)
    bd = defaultdict(list)
    for i in range(n):
        for s in range(4):
            if (i, s) not in glued:
                a, b = find(4*i+s), find(4*i+(s+1) % 4); bd[a].append(b); bd[b].append(a)
    if any(len(v) != 2 for v in bd.values()): return False
    seen = set(); comps = 0
    for a in bd:
        if a in seen: continue
        comps += 1; st = [a]; seen.add(a)
        while st:
            x = st.pop()
            for y in bd[x]:
                if y not in seen: seen.add(y); st.append(y)
    g = defaultdict(list)
    for a, b, d in J: g[a].append(b); g[b].append(a)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in g[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n and V - E + n == 1 and comps == 1

def random_disk(rng, n, slit_frac):
    while True:
        S = {(0, 0)}
        while len(S) < n:
            x, y = rng.choice(sorted(S)); dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            S.add((x + dx, y + dy))
        cells = sorted(S)
        if not is_disk(cells, joins_of(cells)): continue
        full = joins_of(cells); rng.shuffle(full); slits = set()
        target = int(slit_frac * len(full))
        for a, b, d in full:
            if len(slits) >= target: break
            s = frozenset((cells[a], cells[b]))
            if is_disk(cells, joins_of(cells, frozenset(slits | {s}))): slits.add(s)
        return cells, joins_of(cells, frozenset(slits))

PORT_DELTA = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
def port_edge(c, p):
    x, y = c
    return {1: ('V', x % 2), 3: ('V', (x - 1) % 2), 2: ('H', y % 2), 0: ('H', (y - 1) % 2)}[p]

def join_edge(cells, a, d):
    x, y = cells[a]
    return ('V', x % 2) if d == 1 else ('H', y % 2)

def boundary_walk(cells, J):
    """Cyclic list of boundary halfedges (cell, port), counterclockwise with the
    region on the left; side s runs from corner s to corner s+1
    (corners 0=BL,1=BR,2=TR,3=TL).  Uses the true abstract corner fans."""
    n = len(cells); find, glued = _corner_classes(cells, J)
    hes = {}
    for i in range(n):
        for s in range(4):
            if (i, s) not in glued: hes[(i, s)] = (find(4*i+s), find(4*i+(s+1) % 4))
    start = defaultdict(list)
    for h, (u, v) in hes.items(): start[u].append(h)
    assert all(len(v) == 1 for v in start.values())
    h0 = min(hes); walk = [h0]
    while True:
        nxt = start[hes[walk[-1]][1]][0]
        if nxt == h0: break
        walk.append(nxt)
    assert len(walk) == len(hes)
    return walk

def candidate_runs(cells, J, walk, outward_only):
    S = set(cells); Jset = {(a, b) for a, b, d in J} | {(b, a) for a, b, d in J}
    def ok_he(h):
        if not outward_only: return True
        i, p = h; dx, dy = PORT_DELTA[p]; x, y = cells[i]
        return (x + dx, y + dy) not in S
    def cont(h1, h2):
        (i, p), (j, q) = h1, h2
        if p != q or i == j: return False
        (x, y), (X, Y) = cells[i], cells[j]
        if abs(X - x) + abs(Y - y) != 1: return False
        if p in (1, 3) and X != x: return False
        if p in (0, 2) and Y != y: return False
        return (i, j) in Jset
    m = len(walk); st = 0
    for k in range(m):
        if not cont(walk[k - 1], walk[k]): st = k; break
    W = walk[st:] + walk[:st]; runs = []; cur = []
    for h in W:
        if cur and cont(cur[-1], h): cur.append(h)
        else:
            if cur: runs.append(cur)
            cur = [h]
    if cur: runs.append(cur)
    out = []
    for r in runs:
        seg = []
        for h in r:
            if ok_he(h): seg.append(h)
            else:
                if seg: out.append(seg)
                seg = []
        if seg: out.append(seg)
    return out

PARTITIONS = ({('V', 0): 'R', ('H', 0): 'R', ('V', 1): 'B', ('H', 1): 'B'},
              {('V', 0): 'R', ('H', 1): 'R', ('V', 1): 'B', ('H', 0): 'B'})

def consecutive_partition(cells, walk, banks):
    """Return a partition index making merged colours cyclically consecutive
    in boundary order of the selected halfedges, or None."""
    sel = {h for B in banks for h in B}
    seq = [port_edge(cells[i], p) for (i, p) in walk if (i, p) in sel]
    for k, P in enumerate(PARTITIONS):
        cols = [P[e] for e in seq]
        changes = sum(1 for t in range(len(cols)) if cols[t] != cols[t - 1])
        if changes <= 2: return k
    return None

def make_instance(rng, nmax, case):
    n = rng.randint(6, nmax)
    cells, J = random_disk(rng, n, rng.choice((0.0, 0.1, 0.25)))
    walk = boundary_walk(cells, J)
    runs = candidate_runs(cells, J, walk, outward_only=case in ('b1', 'b2'))
    if not runs: return None
    rng.shuffle(runs); banks = []
    for r in runs:
        i = rng.randrange(len(r)); j = rng.randrange(i, len(r)); banks.append(r[i:j + 1])
    E = lambda B: port_edge(cells[B[0][0]], B[0][1])
    sel = []
    if case == 'a':
        used = set()
        for B in banks:
            if E(B) not in used and len(sel) < 4: sel.append(B); used.add(E(B))
    elif case == 'b1':
        cnt = defaultdict(int); rep = None
        for B in banks:
            e = E(B)
            if len(sel) >= 4: break
            if cnt[e] == 0: sel.append(B); cnt[e] += 1
            elif cnt[e] == 1 and rep is None: sel.append(B); cnt[e] += 1; rep = e
    elif case == 'b2':
        main = E(banks[0]); other = None
        for B in banks:
            if E(B) == main: sel.append(B)
            elif other is None: sel.append(B); other = E(B)
    elif case == 'g':
        k = rng.randint(1, min(len(banks), 12))
        sel = banks[:k]
        # greedily drop banks until some partition is consecutive
        while sel and consecutive_partition(cells, walk, sel) is None:
            sel.pop(rng.randrange(len(sel)))
    if not sel: return None
    # banks are reported in boundary-walk order of their halfedges
    pos = {h: t for t, h in enumerate(walk)}
    return cells, J, sel, walk

# ------------------------------------------------------------------ checker
def check(cells, J, banks, order):
    n = len(cells)
    if sorted(order) != list(range(n)): return False, 'not a permutation of all cells'
    rank = {c: t for t, c in enumerate(order)}
    flips = defaultdict(list)
    for a, b, d in J: flips[join_edge(cells, a, d)].append((a, b))
    for e, L in flips.items():
        for (a, b), (c, d) in combinations(L, 2):
            a, b = sorted((rank[a], rank[b])); c, d = sorted((rank[c], rank[d]))
            if a < c < b < d or c < a < d < b: return False, f'flips alternate on {e}'
    for B in banks:
        e = port_edge(cells[B[0][0]], B[0][1])
        for (m, p) in B:
            for a, b in flips[e]:
                lo, hi = sorted((rank[a], rank[b]))
                if lo < rank[m] < hi: return False, f'halfedge {(m, p)} not exposed on {e}'
        r = [rank[m] for m, _ in B]
        if not (all(r[t] < r[t + 1] for t in range(len(r) - 1)) or all(r[t] > r[t + 1] for t in range(len(r) - 1))):
            return False, 'bank not monotone'
    for B1, B2 in combinations(banks, 2):
        if port_edge(cells[B1[0][0]], B1[0][1]) != port_edge(cells[B2[0][0]], B2[0][1]): continue
        r1 = [rank[m] for m, _ in B1]; r2 = [rank[m] for m, _ in B2]
        if not (max(r1) < min(r2) or max(r2) < min(r1)): return False, 'same-edge banks not separated'
    return True, 'ok'

# ------------------------------------------------------------------ runner
def main():
    path, N, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    nmax = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    cases = sys.argv[5].split(',') if len(sys.argv) > 5 else ['a', 'b1', 'b2', 'g']
    spec = importlib.util.spec_from_file_location('candidate', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    rng = random.Random(seed); stats = defaultdict(int); fails = []; t = time.time()
    while sum(stats[c] for c in cases) < N:
        case = rng.choice(cases)
        inst = make_instance(rng, nmax, case)
        if inst is None: continue
        cells, J, banks, walk = inst
        stats[case] += 1
        try:
            order = mod.construct(cells, J, [list(B) for B in banks])
            ok, why = check(cells, J, banks, order)
        except Exception as ex:
            ok, why = False, 'exception: ' + ''.join(traceback.format_exception_only(type(ex), ex)).strip()
        if ok: stats['ok_' + case] += 1
        else:
            fails.append({'case': case, 'why': why, 'cells': cells, 'J': J, 'banks': banks})
    print(json.dumps({'instances': dict(stats), 'failures': len(fails), 'seconds': round(time.time() - t, 1)}))
    for f in fails[:3]: print('FAIL', json.dumps(f)[:3000])
    if fails:
        with open(path + f'.fails-{seed}.json', 'w') as fh: json.dump(fails, fh)
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
