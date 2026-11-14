"""Adversarial tests of impl.py against Lemma L2 and Corollary L2a (Section 4.2).

Regions: single cell; 1 x n and n x 1 strips; full rectangles; width-1 square
spirals; k x k blocks slit into a spiral corridor; combs (polyomino and slit
versions); serpentines with long alternating slits; annuli opened by one slit
(holed polyominoes made into disks); random spanning-tree join sets (every
join a cut, every cell a cut cell); maximal disks grown from spanning trees,
including holed polyominoes.

Selections, each with outward-only and with arbitrary (non-outward) banks:
every maximal run selected whole (every boundary halfedge selected); every run
split into several banks that meet; configurations (a), (b1) (same-edge pair
on one split run or on two runs), (b2) (split runs plus one other bank),
b2-full; and arbitrary selections outside L2a.

For every instance:
  * (H1) and (H2) are recomputed independently, from the text, not from impl;
  * an independent classification into Corollary L2a cases (a), (b1), (b2);
  * L2a case  =>  (H1)+(H2) hold   (tests Corollary L2a, including non-outward);
  * (H1)+(H2) =>  impl.construct returns an order passing l2harness.check;
  * otherwise =>  impl.construct raises ProofGap('hypothesis ...');
  * refused instances with at most 8 cells: exhaustive search for a valid
    order (informational; (H2) is sufficient, not claimed necessary).  The
    key refused_H1_... counts refusals where some partition satisfies (H1),
    so that (H2) is the failing hypothesis; refused_noH1_... the others;
    valid_exists=None means more than 8 cells (not searched).
The output also reports which clause of (H2) impl used (impl.STATS), so the
coverage of the 'meet' clause is visible.

Usage: python3 check_adversarial.py SEED [REPS]      (exit status 0 iff no problem)
Adapted from the computational referee's scratch script adv.py.
"""
import sys, os, random, itertools, json, importlib.util
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
h = load('l2harness', os.path.join(HERE, 'l2harness.py'))
IMPL = os.environ.get('IMPL', os.path.join(HERE, 'impl.py'))
impl = load('impl', IMPL)

PARTS = h.PARTITIONS
def corner_xy(c, s):
    x, y = c
    return ((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1))[s]

# ------------------------------------------------------------- shapes
def rect(w, ht):
    return [(x, y) for x in range(w) for y in range(ht)]

def full(cells):
    return h.joins_of(cells)

def with_slits(cells, slitpairs):
    return h.joins_of(cells, frozenset(frozenset(p) for p in slitpairs))

def spiral_path(turns):
    """width-1 square spiral path with one empty lane between arms (hole-free)."""
    cells = [(0, 0)]; x = y = 0
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]; L = 2
    d = 0
    for t in range(turns):
        dx, dy = dirs[d % 4]
        for _ in range(L):
            x += dx; y += dy; cells.append((x, y))
        d += 1
        if d % 2 == 0: L += 2
    return sorted(set(cells))

def tight_spiral_block(k):
    """k x k block with slits making a spiral corridor of width 1."""
    cells = rect(k, k); S = set(cells)
    # walk spiral order; keep only joins between consecutive spiral cells
    order = []; seen = set(); x, y = 0, 0; dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]; d = 0
    for _ in range(k * k):
        order.append((x, y)); seen.add((x, y))
        nx, ny = x + dirs[d][0], y + dirs[d][1]
        if (nx, ny) not in S or (nx, ny) in seen:
            d = (d + 1) % 4; nx, ny = x + dirs[d][0], y + dirs[d][1]
        x, y = nx, ny
    keep = {frozenset((order[i], order[i + 1])) for i in range(len(order) - 1)}
    idx = {c: i for i, c in enumerate(cells)}
    J = [(a, b, dd) for (a, b, dd) in full(cells) if frozenset((cells[a], cells[b])) in keep]
    return cells, J

def comb(teeth, height, gap=1):
    cells = [(x, 0) for x in range(teeth * (gap + 1) - gap)]
    for t in range(teeth):
        for y in range(1, height + 1): cells.append((t * (gap + 1), y))
    return sorted(cells)

def slit_comb(teeth, height):
    """rectangle (2*teeth-1) x (height+1) with vertical slits between columns above row 0."""
    w = 2 * teeth - 1; cells = rect(w, height + 1)
    sl = [((x, y), (x + 1, y)) for x in range(w - 1) for y in range(1, height + 1)]
    return cells, with_slits(cells, sl)

def serpentine(w, ht):
    """w x ht block with long vertical slits alternating from bottom and top."""
    cells = rect(w, ht); sl = []
    for x in range(w - 1):
        ys = range(0, ht - 1) if x % 2 == 0 else range(1, ht)
        sl += [((x, y), (x + 1, y)) for y in ys]
    return cells, with_slits(cells, sl)

def slit_annulus(w, ht, thick=1, where=0):
    cells = [(x, y) for x in range(w) for y in range(ht)
             if not (thick <= x < w - thick and thick <= y < ht - thick)]
    # one slit through the ring at the bottom arm, between x=where and where+1
    sl = [((where, y), (where + 1, y)) for y in range(thick)]
    return cells, with_slits(cells, sl)

def tree_joins(rng, cells):
    """random spanning tree of the grid adjacency: every join is a cut, many cut cells."""
    J = full(cells); rng.shuffle(J); par = list(range(len(cells)))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    T = []
    for a, b, d in J:
        if f(a) != f(b): par[f(a)] = f(b); T.append((a, b, d))
    return sorted(T)

def maximal_disk_from_tree(rng, cells):
    """start from a spanning tree, add joins back while still a disk (allows polyominoes with holes)."""
    T = tree_joins(rng, cells); rest = [j for j in full(cells) if j not in T]; rng.shuffle(rest)
    J = list(T)
    for j in rest:
        if h.is_disk(cells, J + [j]): J.append(j)
    return sorted(J)

def random_poly(rng, n):
    S = {(0, 0)}
    while len(S) < n:
        x, y = rng.choice(sorted(S)); dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        S.add((x + dx, y + dy))
    return sorted(S)

def holey_poly(rng, n):
    """random polyomino forced to contain a hole (ring plus random growth)."""
    w, ht = rng.randint(3, 5), rng.randint(3, 5)
    S = {c for c in rect(w, ht) if not (0 < c[0] < w - 1 and 0 < c[1] < ht - 1)}
    while len(S) < n:
        x, y = rng.choice(sorted(S)); dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        c = (x + dx, y + dy)
        if not (0 < c[0] < w - 1 and 0 < c[1] < ht - 1): S.add(c)
    return sorted(S)

def shapes(rng):
    out = []
    out.append(('single', [(0, 0)], []))
    for n in list(range(1, 13)) + [17, 30]:
        c = [(x, 0) for x in range(n)]; out.append(('strip1x%d' % n, c, full(c)))
        c = [(0, y) for y in range(n)]; out.append(('strip%dx1' % n, c, full(c)))
        c = [(x, 3) for x in range(n)]; c = [(x + 1, y) for x, y in c]; out.append(('strip1x%d_off' % n, c, full(c)))
    for w, ht in [(2, 2), (2, 3), (3, 3), (4, 2), (2, 4), (4, 4), (3, 5), (6, 2), (5, 5)]:
        c = rect(w, ht); out.append(('rect%dx%d' % (w, ht), c, full(c)))
    for t in (2, 3, 4, 6, 8):
        c = spiral_path(t); out.append(('spiral%d' % t, c, full(c)))
    for k in (3, 4, 5, 6, 7):
        c, J = tight_spiral_block(k); out.append(('tightspiral%d' % k, c, J))
    for t, ht in [(2, 1), (3, 2), (4, 3), (5, 1), (3, 5)]:
        c = comb(t, ht); out.append(('comb%d_%d' % (t, ht), c, full(c)))
        c, J = slit_comb(t, ht); out.append(('slitcomb%d_%d' % (t, ht), c, J))
    for w, ht in [(2, 3), (3, 3), (4, 5), (6, 4), (7, 7), (2, 10)]:
        c, J = serpentine(w, ht); out.append(('serp%dx%d' % (w, ht), c, J))
    for w, ht, th, wh in [(3, 3, 1, 0), (4, 4, 1, 1), (5, 4, 1, 2), (6, 6, 2, 1), (5, 5, 2, 1), (5, 5, 2, 2), (7, 3, 1, 3), (8, 5, 1, 4)]:
        c, J = slit_annulus(w, ht, th, wh); out.append(('annulus%dx%dt%dw%d' % (w, ht, th, wh), c, J))
    for i in range(25):
        c = random_poly(rng, rng.randint(4, 40)); out.append(('tree%d' % i, c, tree_joins(rng, c)))
    for i in range(25):
        c = holey_poly(rng, rng.randint(9, 40)); out.append(('holeymax%d' % i, c, maximal_disk_from_tree(rng, c)))
    for i in range(15):
        c = random_poly(rng, rng.randint(4, 40)); out.append(('maxdisk%d' % i, c, maximal_disk_from_tree(rng, c)))
    res = []
    for name, c, J in out:
        assert h.is_disk(c, J), name
        res.append((name, c, J))
    return res

# ------------------------------------------------------------- independent hypothesis checks
def port_color(cells, hh, k):
    return PARTS[k][h.port_edge(cells[hh[0]], hh[1])]

def mixed_pt(X, Y, k):
    # vertical line X carries edge V((X+1)%2); horizontal line Y carries H((Y+1)%2)
    cx = PARTS[k][('V', (X + 1) % 2)]; cy = PARTS[k][('H', (Y + 1) % 2)]
    return cx != cy

def indep_hyp(cells, walk, banks, k):
    L = len(walk); pos = {hh: t for t, hh in enumerate(walk)}
    sel = {hh for B in banks for hh in B}
    seq = [port_color(cells, hh, k) for hh in walk if hh in sel]
    H1 = sum(1 for i in range(len(seq)) if seq[i] != seq[i - 1]) <= 2
    if not sel: return H1, True
    if len(set(seq)) == 2: return H1, True
    if len(sel) < L: return H1, True
    starts = sorted(banks, key=lambda B: pos[B[0]])
    for u in range(len(starts)):
        A, B = starts[u - 1], starts[u]
        t = pos[B[0]]
        if (t - pos[A[-1]]) % L == 1:
            i, s = walk[t]; X, Y = corner_xy(cells[i], s)
            if mixed_pt(X, Y, k): return H1, True
    return H1, False

def l2a_case(cells, banks):
    E = [h.port_edge(cells[B[0][0]], B[0][1]) for B in banks]
    cnt = Counter(E); cases = []
    if all(v <= 1 for v in cnt.values()): cases.append('a')
    rep = [e for e, v in cnt.items() if v >= 2]
    if len(banks) <= 4 and len(rep) <= 1 and all(v <= 2 for v in cnt.values()): cases.append('b1')
    if any(len(banks) - v <= 1 for v in cnt.values()): cases.append('b2')
    return cases

# ------------------------------------------------------------- bank selections
def runs(cells, J, walk, outward):
    return h.candidate_runs(cells, J, walk, outward_only=outward)

def split(rng, r, maxpieces):
    """split a run into consecutive banks (adjacent banks meet), possibly dropping pieces."""
    m = len(r); cuts = sorted(rng.sample(range(1, m), min(m - 1, rng.randint(0, maxpieces - 1)))) if m > 1 else []
    pieces = []; prev = 0
    for c in cuts + [m]: pieces.append(r[prev:c]); prev = c
    return pieces

def selections(rng, cells, J, walk, reps):
    out = []
    for outward in (False, True):
        R = runs(cells, J, walk, outward)
        if not R: continue
        E = lambda B: h.port_edge(cells[B[0][0]], B[0][1])
        # all whole runs (every boundary halfedge selected when outward False)
        out.append(('allruns_o%d' % outward, [list(r) for r in R]))
        # all halfedges selected, every run split into pieces
        out.append(('allsplit_o%d' % outward, [p for r in R for p in split(rng, r, 3)]))
        byE = defaultdict(list)
        for r in R: byE[E(r)].append(r)
        for _ in range(reps):
            Rs = list(R); rng.shuffle(Rs)
            def sub(r):
                if rng.random() < 0.5: return list(r)
                i = rng.randrange(len(r)); j = rng.randrange(i, len(r)); return r[i:j + 1]
            # (a)
            used = set(); sel = []
            for r in Rs:
                if E(r) not in used and len(sel) < 4: sel.append(sub(r)); used.add(E(r))
            out.append(('a_o%d' % outward, sel))
            # (b1): pick a repeated edge with two banks (maybe on the same run, split)
            e = rng.choice(list(byE)); cand = byE[e]
            r = rng.choice(cand)
            if len(r) >= 2 and (len(cand) == 1 or rng.random() < 0.5):
                c = rng.randrange(1, len(r)); two = [r[:c], r[c:]]
                if rng.random() < 0.5:   # leave a gap between them
                    two = [r[:c], r[c + 1:]] if c + 1 < len(r) else [r[:c]]
            elif len(cand) >= 2:
                r1, r2 = rng.sample(cand, 2); two = [sub(r1), sub(r2)]
            else:
                two = [sub(r)]
            sel = [B for B in two if B]
            others = [ee for ee in byE if ee != e]; rng.shuffle(others)
            for ee in others[:rng.randint(0, 2)]:
                sel.append(sub(rng.choice(byE[ee])))
            out.append(('b1_o%d' % outward, sel))
            # (b2): many banks on edge e (split all its runs), plus at most one other
            sel = []
            for r in cand:
                if rng.random() < 0.8:
                    ps = split(rng, r, 4)
                    sel += [p for p in ps if p and rng.random() < 0.85]
            if others and rng.random() < 0.8:
                sel.append(sub(rng.choice(byE[others[0]])))
            if sel: out.append(('b2_o%d' % outward, sel))
            # b2 with everything on edge e selected whole + other edge whole
            sel = [list(r) for r in cand] + ([list(rng.choice(byE[others[0]]))] if others else [])
            out.append(('b2full_o%d' % outward, sel))
            # arbitrary (outside L2a) random selection
            k = rng.randint(1, min(len(R), 8)); sel = []
            for r in rng.sample(R, k): sel += [p for p in split(rng, sub(r), 2) if p]
            out.append(('rand_o%d' % outward, sel))
    return out

def valid_exists(cells, J, banks, limit=8):
    n = len(cells)
    if n > limit: return None
    for o in itertools.permutations(range(n)):
        if h.check(cells, J, banks, list(o))[0]: return True
    return False

def main():
    seed = int(sys.argv[1]); reps = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    rng = random.Random(seed)
    S = shapes(rng)
    stats = Counter(); problems = []; info = Counter()
    for name, cells, J in S:
        walk = h.boundary_walk(cells, J)
        for tag, banks in selections(rng, cells, J, walk, reps):
            banks = [B for B in banks if B]
            if not banks: continue
            # banks must be disjoint walk intervals with one port
            hyp = [indep_hyp(cells, walk, banks, k) for k in (0, 1)]
            holds = any(a and b for a, b in hyp)
            cases = l2a_case(cells, banks)
            stats['inst'] += 1; stats['tag_' + tag.split('_')[0]] += 1
            if cases: stats['l2a'] += 1
            if cases and not holds:
                problems.append(('L2a case but (H1)+(H2) fail', name, tag, cases, banks)); continue
            try:
                order = impl.construct(cells, J, [list(B) for B in banks]); err = None
            except impl.ProofGap as ex:
                order, err = None, 'ProofGap: %s' % ex
            except Exception as ex:
                order, err = None, 'EXC %s: %s' % (type(ex).__name__, ex)
            if holds:
                if order is None:
                    problems.append(('hyp holds but construct failed', name, tag, err, banks)); continue
                ok, why = h.check(cells, J, banks, order)
                if not ok:
                    problems.append(('check failed', name, tag, why, banks)); continue
                stats['ok'] += 1
                if all(hh in {x for B in banks for x in B} for hh in walk): stats['ok_allselected'] += 1
            else:
                if order is not None or not (err or '').startswith('ProofGap: hypothesis'):
                    problems.append(('hyp fails but construct did not refuse', name, tag, err, banks)); continue
                stats['refused'] += 1
                ve = valid_exists(cells, J, banks)
                # 'H1' = some partition satisfies (H1), so (H2) is what fails
                h1 = 'H1' if any(a for a, b in hyp) else 'noH1'
                info['refused_%s_valid_exists=%s' % (h1, ve)] += 1
    print(json.dumps({'seed': seed, 'shapes': len(S), 'stats': dict(stats), 'refused_info': dict(info),
                      'H2_clause_used': {k: v for k, v in sorted(impl.STATS.items()) if k.startswith('H2_')},
                      'problems': len(problems)}))
    for p in problems[:5]: print('PROBLEM', json.dumps(p)[:1500])
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
