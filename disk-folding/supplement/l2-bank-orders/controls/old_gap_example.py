"""Revision-note control (not part of the proof): the one-colour gap in the
proof of the former Section 4.2, even in case (a).

Row of three cells a=(0,0), b=(1,0), c=(2,0), one bank (their south sides),
partition P0, spokes subdivided as in the old proof.  The separating curve
u -> w_b -> b -> c -> w_c -> w_a -> a -> u is inserted into the GIVEN rotation
system as chords inside faces; the augmented map is checked to be planar
(V - E + F = 2), the chord cycle to split the faces into two classes, and the
red and blue edges to lie in different classes.  Cutting at u gives the cell
order b, c, a, which is not monotone on the bank.

Extracted from Example 10.2 of the A_blocks candidate (dev2/examples_v2.py);
faces_of is copied from A_blocks impl_v2.py.  Usage: python3 controls/old_gap_example.py
"""
import importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location('l2harness', os.path.join(os.path.dirname(HERE), 'l2harness.py'))
h = importlib.util.module_from_spec(_s); _s.loader.exec_module(h)


def faces_of(V, bedges, rot):
    colour = {}
    for a, b, c in bedges: colour[(a, b)] = colour[(b, a)] = c
    R = {v: [x for x in rot[v] if (v, x) in colour] for v in V}
    fid = {}; faces = []
    for (a, b) in colour:
        if (a, b) in fid: continue
        cyc = []; e = (a, b)
        while e not in fid:
            fid[e] = len(faces); cyc.append(e[0])
            x, y = e; L = R[y]; i = L.index(x); e = (y, L[i - 1])
        faces.append(cyc)
    return colour, R, fid, faces



cells = [(0, 0), (1, 0), (2, 0)]; J = h.joins_of(cells); walk = h.boundary_walk(cells, J)
bank = [(0, 0), (1, 0), (2, 0)]; P = h.PARTITIONS[0]
n = 3; u = 3; seq = [x for x in walk if x in set(bank)]
wid = {x: 4 + t for t, x in enumerate(seq)}
name = {0: 'a', 1: 'b', 2: 'c', 3: 'u'}
for x, i in wid.items(): name[i] = 'w_' + name[x[0]]
edges = [(a, b, P[h.join_edge(cells, a, d)]) for a, b, d in J]
for x in seq:
    c = P[h.port_edge(cells[x[0]], x[1])]; edges += [(u, wid[x], c), (wid[x], x[0], c)]
via = {}
for a, b, d in J:
    if d == 1: via[(a, 1)] = b; via[(b, 3)] = a
    else: via[(a, 2)] = b; via[(b, 0)] = a
for x in seq: via[x] = wid[x]
rot = {c: [via[(c, p)] for p in range(4) if (c, p) in via] for c in range(n)}
rot[u] = [wid[x] for x in reversed(seq)]
for x in seq: rot[wid[x]] = [x[0], u]
V = list(range(7))
colour, Rr, fid, faces = faces_of(set(V), edges, rot)
print('edges:', [(name[a], name[b], c) for a, b, c in edges])
print('faces of the given embedding:', [[name[v] for v in f] for f in faces])
assert len(V) - len(edges) + len(faces) == 2
F = {frozenset(name[v] for v in f): k for k, f in enumerate(faces)}
Fab = F[frozenset({'u', 'w_a', 'a', 'b', 'w_b'})]; Fbc = F[frozenset({'u', 'w_b', 'b', 'c', 'w_c'})]
Fout = F[frozenset({'u', 'w_c', 'c', 'b', 'a', 'w_a'})]
inv = {v: k for k, v in name.items()}
curve = [('u', Fab, 'w_b'), ('w_b', Fab, 'b'), ('b', Fout, 'c'), ('c', Fout, 'w_c'),
         ('w_c', Fout, 'w_a'), ('w_a', Fout, 'a'), ('a', Fab, 'u')]
print('curve (vertex, face, vertex):', [(x, [name[v] for v in faces[f]], y) for x, f, y in curve])
# insert the chords into the rotation system
R2 = {v: list(Rr[v]) for v in V}
chords = []
for x, f, y in curve:
    chords.append((inv[x], inv[y], f))
nid = 100
ins = {}                               # (vertex, face) -> list of (offset, chord-end id)
L_edges = []
for k, (x, y, f) in enumerate(chords):
    cyc = faces[f]; m = len(cyc)
    jx, jy = cyc.index(x), cyc.index(y)
    a, b = ('L', k, 0), ('L', k, 1)   # half-edge tokens
    ins.setdefault((x, f), []).append(((jy - jx) % m, y, k))
    ins.setdefault((y, f), []).append(((jx - jy) % m, x, k))
# augmented graph: subdivide each chord with a midpoint vertex (keeps it simple)
Vx = list(V); Ex = list(edges); mid = {}
for k, (x, y, f) in enumerate(chords):
    mvert = 200 + k; mid[k] = mvert; Vx.append(mvert)
    Ex += [(x, mvert, 'L'), (mvert, y, 'L')]
R3 = {v: list(R2[v]) for v in V}
for (v, f), lst in ins.items():
    cyc = faces[f]; j = cyc.index(v); nxt = cyc[(j + 1) % len(cyc)]
    L = R3[v]; i = L.index(nxt)
    lst.sort()
    for t, (_, other, k) in enumerate(lst): L.insert(i + 1 + t, mid[k])
for k, (x, y, f) in enumerate(chords): R3[mid[k]] = [x, y]
col3, RR3, fid3, faces3 = faces_of(set(Vx), Ex, R3)
euler = len(Vx) - len(Ex) + len(faces3)
print('augmented map: V-E+F =', euler)
assert euler == 2, 'curve cannot be drawn in the given embedding as specified'
par = list(range(len(faces3)))
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for (a, b), c in col3.items():
    if c != 'L': par[find(fid3[(a, b)])] = find(fid3[(b, a)])
groups = {find(f) for f in range(len(faces3))}
print('sides of the curve (face classes):', len(groups))
side = {c: {find(fid3[(a, b)]) for a, b, cc in edges if cc == c for (a, b) in ((a, b), (b, a))} for c in 'RB'}
print('red edges lie in classes', sorted(side['R']), '; blue edges in classes', sorted(side['B']))
assert len(groups) == 2 and len(side['R']) == 1 and len(side['B']) == 1 and side['R'] != side['B']
order = [inv[x] for x, _, _ in curve]
print('vertex order along the curve:', [name[v] for v in order])
cell_order = [v for v in order if v < n]
print('cell order after cutting at u:', [name[v] for v in cell_order], h.check(cells, J, [bank], cell_order))
