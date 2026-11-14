"""Size control: 1 x n strips with all four sides as banks (Corollary L2a(b1)).
The recursion depth of solve()/k2_cut() grows linearly with n; construct() raises
Python's recursion limit.  Usage: python3 controls/long_strip.py N [N ...]
"""
import importlib.util, os, sys, time

SUPP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m


h = load('l2harness', os.path.join(SUPP, 'l2harness.py'))
impl = load('impl', os.path.join(SUPP, 'impl.py'))
for n in map(int, sys.argv[1:]):
    c = [(x, 0) for x in range(n)]; J = h.joins_of(c); w = h.boundary_walk(c, J)
    banks = [list(r) for r in h.candidate_runs(c, J, w, False)]
    t = time.time(); o = impl.construct(c, J, banks)
    print('1x%d strip, all four sides as banks (case b1):' % n, h.check(c, J, banks, o), '%.1fs' % (time.time() - t))
