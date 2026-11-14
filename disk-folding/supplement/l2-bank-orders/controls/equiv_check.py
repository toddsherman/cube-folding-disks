"""Equivalence control: impl.py (the construction of the final text) against the
refereed C_induction implementation (controls/C_induction_impl_v2.py, a byte copy).

On 3000 random harness instances (seed 4410, cases a, b1, b2, g) both are run.
Orders may differ only through the choice of marker position in the one-colour
case; every differing order must pass the harness checker, and the two must
agree on which instances raise ProofGap.  Also prints which (H2) clause impl.py
used.  Usage: python3 controls/equiv_check.py      (exit status 0 iff all asserts hold)
"""
import importlib.util, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
SUPP = os.path.dirname(HERE)


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m


h = load('l2harness', os.path.join(SUPP, 'l2harness.py'))
new = load('impl', os.path.join(SUPP, 'impl.py'))
old = load('impl_v2', os.path.join(HERE, 'C_induction_impl_v2.py'))
rng = random.Random(4410); same = diff = gap = 0; N = 0
while N < 3000:
    case = rng.choice(['a', 'b1', 'b2', 'g'])
    inst = h.make_instance(rng, 40, case)
    if inst is None:
        continue
    cells, J, banks, walk = inst; N += 1
    try:
        o1 = new.construct(cells, J, [list(B) for B in banks])
    except new.ProofGap:
        o1 = None
    try:
        o2 = old.construct(cells, J, [list(B) for B in banks])
    except old.ProofGap:
        o2 = None
    if o1 is None or o2 is None:
        gap += 1; assert (o1 is None) == (o2 is None)
    elif o1 == o2:
        same += 1
    else:
        diff += 1; assert h.check(cells, J, banks, o1)[0]
print({'instances': N, 'identical_orders': same, 'different_but_valid': diff, 'both_ProofGap': gap})
print('impl.py (H2) clause used:', {k: v for k, v in sorted(new.STATS.items()) if k.startswith('H2_')})
