"""Mutation controls for impl.py.  Each mutant is a one-line patch of impl.py,
written to a temporary directory (nothing is written next to impl.py), and is
run through l2harness.py with and without L2DEBUG=1.

  tie_flag   red-cut subproblem Q1: tie flag of t_B^1 flipped (False -> True)
  blue_p1    blue cut: t_B^1 placed at q_1 instead of p_1
  O2_O1      Step 4 returns O2 ++ O1 instead of O1 ++ O2
  no_slide   the Step-3 slide of t_B^1 over h+ is removed

The plain harness checks only the final conclusions 1-4 of Lemma L2.  O2 ++ O1
is exactly the reversal of a valid construction (by induction on the recursion),
and a removed Step-3 slide is repeated by the next level's Step 1, so the plain
checker cannot detect these two; only the L2DEBUG invariants (orientation in
(S3), mixedness of the Step-3 markers) catch them.  Expected: tie_flag detected
under L2DEBUG; blue_p1 detected by the plain checker; O2_O1 undetected plain and
detected under L2DEBUG; no_slide is reported for information.
Usage: python3 controls/mutation_controls.py [N] [SEED]   (exit 0 iff expectations hold)
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SUPP = os.path.dirname(HERE)
SRC = open(os.path.join(SUPP, 'impl.py')).read()
MUTANTS = {
    'tie_flag': ("tb1, rf1 = after_block(R1, cut1), False", "tb1, rf1 = after_block(R1, cut1), True"),
    'blue_p1': ("tb1, rf1 = before_block(R1, cut1), True", "tb1, rf1 = after_block(R1, cut1), True"),
    'O2_O1': ("order = O1 + O2", "order = O2 + O1"),
    'no_slide': ("if not is_mixed(R1.pos_xy(tb1), k):          # slide beta_1 forward over h+",
                 "if False:          # slide beta_1 forward over h+"),
}
N = sys.argv[1] if len(sys.argv) > 1 else '300'
SEED = sys.argv[2] if len(sys.argv) > 2 else '4406'
tmp = tempfile.mkdtemp(prefix='l2mut-')
res = {}
for name, (a, b) in MUTANTS.items():
    assert SRC.count(a) == 1, name
    path = os.path.join(tmp, 'impl_%s.py' % name)
    open(path, 'w').write(SRC.replace(a, b))
    for dbg in (False, True):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        env.pop('L2DEBUG', None)
        if dbg:
            env['L2DEBUG'] = '1'
        out = subprocess.run([sys.executable, '-B', os.path.join(SUPP, 'l2harness.py'), path, N, SEED, '30', 'a,b1,b2'],
                             capture_output=True, text=True, env=env).stdout
        res[(name, dbg)] = json.loads(out.splitlines()[0])['failures']
for name in MUTANTS:
    print('%-9s failures: plain %4d   L2DEBUG %4d   (of %s)' % (name, res[(name, False)], res[(name, True)], N))
ok = (res[('tie_flag', True)] > 0 and res[('blue_p1', False)] > 0
      and res[('O2_O1', False)] == 0 and res[('O2_O1', True)] > 0)
print('expectations hold' if ok else 'EXPECTATIONS VIOLATED')
sys.exit(0 if ok else 1)
