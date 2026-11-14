"""Remark L2b of Section 4.2: (H2) cannot be omitted, even for outward banks.

For the 2m x 2n blocks with their four whole sides selected as banks, this
script checks with the harness checker (l2harness.check):
  * every bank is outward and a genuine walk interval with one port;
  * some adjacent-pair partition makes the merged colours consecutive
    (the grouping hypothesis of the former L2(b), and (H1));
  * (H2) fails for every partition satisfying (H1) (impl.hyp_H2), and
    impl.construct raises ProofGap;
  * EXHAUSTIVELY over all orders: no order satisfies conclusions 1-4
    (0 valid orders), and the number of orders satisfying conclusions 1-3
    (failing only separation) is reported.
The 2x2 block (24 orders) is the example of the text; the 4x2 and 2x4
blocks (40320 orders each) are further members of the family.  Positive
control: the 3x2 and 2x3 blocks (one odd side length, so (H1)+(H2) hold)
are solved by impl.construct and pass the checker; and splitting one side
bank of the 2x2 or 4x2 block at the mixed point (1,0) satisfies (H2) through
its third clause, and impl.construct then succeeds.
Exit status 0 iff every assertion holds.
"""
import importlib.util
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


h = load('l2harness', 'l2harness.py')
impl = load('impl', 'impl.py')


def block(w, ht):
    cells = [(x, y) for x in range(w) for y in range(ht)]
    J = h.joins_of(cells)
    assert h.is_disk(cells, J)
    walk = h.boundary_walk(cells, J)
    banks = h.candidate_runs(cells, J, walk, outward_only=True)
    return cells, J, walk, banks


def describe(cells, J, walk, banks):
    S = set(cells)
    assert len(banks) == 4, 'expected the four whole sides'
    assert sum(len(B) for B in banks) == len(walk), 'every boundary halfedge selected'
    for B in banks:
        assert len({p for _, p in B}) == 1, 'bank with one port'
        for i, p in B:
            dx, dy = h.PORT_DELTA[p]
            assert (cells[i][0] + dx, cells[i][1] + dy) not in S, 'outward'
    edges = [h.port_edge(cells[B[0][0]], B[0][1]) for B in banks]
    return edges


def main():
    allok = True
    print('# Remark L2b: four whole-side banks of a 2m x 2n block')
    for (w, ht) in ((2, 2), (4, 2), (2, 4)):
        cells, J, walk, banks = block(w, ht)
        edges = describe(cells, J, walk, banks)
        k = h.consecutive_partition(cells, walk, banks)
        R = impl.Region(cells, list(range(len(cells))), J)
        Sigma = {hh for B in banks for hh in B}
        h1 = [kk for kk in (0, 1) if impl.hyp_H1(cells, R, Sigma, kk)]
        h2 = {kk: impl.hyp_H2(cells, R, Sigma, banks, kk)[0] for kk in h1}
        try:
            impl.construct(cells, J, [list(B) for B in banks])
            gap = 'returned an order (UNEXPECTED)'
        except impl.ProofGap as e:
            gap = 'ProofGap: %s' % e
        n = len(cells)
        valid = 0
        only13 = 0
        example = None
        reasons = {}
        for o in itertools.permutations(range(n)):
            ok, why = h.check(cells, J, banks, list(o))
            reasons[why] = reasons.get(why, 0) + 1
            if ok:
                valid += 1
            elif why == 'same-edge banks not separated':
                only13 += 1
                if example is None:
                    example = [cells[i] for i in o]
        print('%dx%d block (width x height), %d cells, %d boundary halfedges' % (w, ht, n, len(walk)))
        print('  banks (target edge, length):', [(e, len(B)) for e, B in zip(edges, banks)])
        print('  all halfedges outward, all selected; grouping partition (former L2(b), (H1)):', k)
        print('  partitions satisfying (H1):', h1, ' (H2) holds for them:', h2)
        print('  impl.construct:', gap)
        print('  orders checked exhaustively: %d' % sum(reasons.values()))
        print('  valid orders (conclusions 1-4): %d' % valid)
        print('  orders satisfying conclusions 1-3 (only separation fails): %d' % only13)
        print('  first such order (cells, lowest first):', example)
        print('  checker verdicts:', dict(sorted(reasons.items())))
        cond = (valid == 0 and k is not None and h1 and not any(h2.values())
                and gap.startswith('ProofGap') and only13 == 8)
        print('  ->', 'OK' if cond else 'FAILED')
        allok &= bool(cond)
    print('# positive controls (one odd side length)')
    for (w, ht) in ((3, 2), (2, 3)):
        cells, J, walk, banks = block(w, ht)
        describe(cells, J, walk, banks)
        order = impl.construct(cells, J, [list(B) for B in banks])
        ok, why = h.check(cells, J, banks, order)
        print('%dx%d block: impl.construct order %s -> checker %s' % (w, ht, [cells[i] for i in order], why))
        allok &= ok
    print('# positive controls for the third clause of (H2): split the bottom bank of the')
    print('# 2x2 and 4x2 blocks into two banks meeting at the mixed position (1,0)')
    for (w, ht) in ((2, 2), (4, 2)):
        cells, J, walk, banks = block(w, ht)
        describe(cells, J, walk, banks)
        B0 = [B for B in banks if B[0][1] == 0][0]
        banks = [B for B in banks if B is not B0] + [B0[:1], B0[1:]]
        R = impl.Region(cells, list(range(len(cells))), J)
        Sigma = {hh for B in banks for hh in B}
        h1 = [kk for kk in (0, 1) if impl.hyp_H1(cells, R, Sigma, kk)]
        wit = {kk: impl.hyp_H2(cells, R, Sigma, banks, kk) for kk in h1}
        order = impl.construct(cells, J, [list(B) for B in banks])
        ok, why = h.check(cells, J, banks, order)
        nvalid = sum(1 for o in itertools.permutations(range(len(cells)))
                     if h.check(cells, J, banks, list(o))[0])
        print('%dx%d block, 5 banks: (H1) partitions %s, (H2) witness %s; impl.construct order %s -> checker %s; '
              'exhaustive valid orders %d' % (w, ht, h1, wit, [cells[i] for i in order], why, nvalid))
        allok &= ok and nvalid > 0 and all(v[0] and v[1][0] == 'meet' for v in wit.values())
    print('ALL OK' if allok else 'SOME CHECK FAILED')
    sys.exit(0 if allok else 1)


if __name__ == '__main__':
    main()
