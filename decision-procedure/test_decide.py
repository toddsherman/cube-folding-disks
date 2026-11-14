#!/usr/bin/env python3
"""Tests for decide.py. Standard library only.

    python3 test_decide.py            the full run
    python3 test_decide.py --quick    a shorter run

Measured on an Apple M4: the full run took 12 seconds with Python 3.15 and 21 seconds with
Python 3.9; the shorter run took 3 and 7 seconds.

The main test compares the program with a brute-force search that knows nothing of fold
lines, cuts or the manuscript's theory. For a sheet without holes it tries every way of
folding each attached side by 180 or by 90 degrees, places the squares on the cube corner
by corner, keeps the ways in which attached squares stay attached, and asks whether any of
them covers all six sides. The program's answer must be the same on every sheet tested.

The other tests:

  - reading: blank lines, slits and comments in a picture, the JSON form, and input that
    must be refused;
  - position: small sheets are run again in all 8 rotations and reflections, and in each
    of them a second time, moved to another place and with the last square moved to the
    front of the list (the search starts from the first square). The answer must not
    change;
  - command line: decide.py is started as a separate program, to check its exit status
    (0, 1, 2 and 3), its --json output, reading from standard input, and that
    `python3 -O` behaves the same;
  - printed output: for sheets that fold, the printed picture of letters and the printed
    fold lines are read back and checked against each other.

One line of the output is information, not a test: it says how many of the sheets that
fold stop folding when the program is allowed six fold lines, or five, instead of seven.
In the full run none stops folding with six, so these tests would pass just the same if
the program stopped at six lines: they do not exercise the seventh.

What this does and does not test. It tests that the program finds a six-sided assignment
exactly when one exists, on small sheets. It does not test that such an assignment can be
carried out with real paper; that is Theorem A of the manuscript.
"""
import itertools
import json
import os
import random
import re
import subprocess
import sys
import time

from decide import decide, read_sheet

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAM = os.path.join(HERE, "decide.py")
EXAMPLES = os.path.join(HERE, "examples")
LETTERS = set("DUFBLR")

# ----------------------------------------------------------------------------- brute force

def corners_of(cell):
    x, y = cell
    return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]


def brute_force_has_six_sided_map(cells, joins):
    """True if some consistent assignment of the squares to cube sides covers all six sides."""
    cells = [tuple(c) for c in cells]
    joined = {frozenset((tuple(a), tuple(b))) for a, b in joins}
    present = set(cells)
    if len(cells) < 6:
        return False

    def attached(c):
        x, y = c
        return [d for d in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                if d in present and frozenset((c, d)) in joined]

    # order the squares so that each one after the first is attached to an earlier one
    order, parent = [cells[0]], {cells[0]: None}
    for c in order:
        for d in attached(c):
            if d not in parent:
                parent[d] = c
                order.append(d)
    if len(order) != len(cells):
        raise RuntimeError("the sheet is not in one piece")

    frames = {cells[0]: dict(zip(corners_of(cells[0]), [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]))}

    def side(frame):
        pts = list(frame.values())
        for axis in range(3):
            if len({p[axis] for p in pts}) == 1:
                return (axis, pts[0][axis])
        raise RuntimeError("a square does not lie on one side of the cube")

    def place(child, par, right_angle):
        fp = frames[par]
        shared = [p for p in corners_of(child) if p in fp]
        if len(shared) != 2:
            raise RuntimeError("attached squares do not share two corner points")
        axis, _ = side(fp)
        frame = {}
        for p in corners_of(child):
            if p in shared:
                frame[p] = fp[p]
                continue
            # the corner of the child across from a shared corner q; `mirror` is the
            # corner of the parent across from q
            q = next(s for s in shared if abs(s[0] - p[0]) + abs(s[1] - p[1]) == 1)
            mirror = (2 * q[0] - p[0], 2 * q[1] - p[1])
            if right_angle:
                v = list(fp[q])
                v[axis] = 1 - v[axis]
                frame[p] = tuple(v)
            else:
                frame[p] = fp[mirror]
        return frame

    def extend(k):
        if k == len(order):
            return len({side(frames[c]) for c in cells}) == 6
        child = order[k]
        for right_angle in (False, True):
            frame = place(child, parent[child], right_angle)
            ok = True
            for d in attached(child):
                if d in frames and d != parent[child]:
                    if any(frame[p] != frames[d][p] for p in frame if p in frames[d]):
                        ok = False
                        break
            if ok:
                frames[child] = frame
                if extend(k + 1):
                    return True
                del frames[child]
        return False

    return extend(1)


# ----------------------------------------------------------------------------- sheets to test

def free_polyominoes(n_max):
    def canon(cells):
        best = None
        for t in range(8):
            pts = []
            for x, y in cells:
                if t & 1:
                    x = -x
                if t & 2:
                    y = -y
                if t & 4:
                    x, y = y, x
                pts.append((x, y))
            mx, my = min(p[0] for p in pts), min(p[1] for p in pts)
            key = tuple(sorted((p[0] - mx, p[1] - my) for p in pts))
            if best is None or key < best:
                best = key
        return best

    level = {canon(((0, 0),))}
    yield 1, sorted(level)
    for n in range(2, n_max + 1):
        new = set()
        for p in level:
            ps = set(p)
            for x, y in p:
                for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if q not in ps:
                        new.add(canon(p + (q,)))
        level = new
        yield n, sorted(level)


def adjacencies(cells):
    present = set(cells)
    return [((x, y), d) for (x, y) in cells for d in ((x + 1, y), (x, y + 1)) if d in present]


def check(cells, joins, counts, label, limits):
    try:
        result = decide(cells, joins)
    except Exception as err:
        counts["MISMATCHES"] += 1
        print(f"ERROR ({label}): decide() failed with {type(err).__name__}: {err}: cells={cells} joins={joins}")
        return
    if not result.applicable:
        counts["not a sheet without holes"] += 1
        return
    expected = brute_force_has_six_sided_map(cells, joins)
    counts["folds" if result.folds else "does not fold"] += 1
    if result.folds != expected:
        counts["MISMATCHES"] += 1
        print(f"MISMATCH ({label}): program says {result.folds}, brute force says {expected}: cells={cells} joins={joins}")
    if result.folds:        # information only: what a smaller limit on the number of fold lines would do
        limits["fold"] += 1
        if not decide(cells, joins, max_lines=6).folds:
            limits["need a seventh line"] += 1
        elif not decide(cells, joins, max_lines=5).folds:
            limits["need a sixth line"] += 1


# The fixed examples: name -> (picture, expected answer). True and False are the expected
# answer, None means "whatever the brute force says", "n/a" means not a sheet without holes.
FIXED_EXAMPLES = {
    "cube net (a cross)": (".#.\n###\n.#.\n.#.\n", True),
    "2 x 3 rectangle": ("###\n###\n", False),
    "1 x 6 strip": ("######\n", False),
    "the example of Section 6 of the manuscript": (".####\n#####\n##...\n##...\n##...\n", True),
    "3 x 3 block": ("###\n###\n###\n", False),
    "3 x 3 block with three slits": ("###\n###\n###\nslit 0 0 right\nslit 0 1 down\nslit 1 1 right\n", None),
    "ring of eight squares (has a hole)": ("###\n#.#\n###\n", "n/a"),
    "3 x 3 block with a slit that does not reach the border (a hole)": ("###\n###\n###\nslit 1 1 right\n", "n/a"),
}


class Checks:
    """Counts checks and collects the ones that fail."""

    def __init__(self):
        self.done = 0
        self.failed = []

    def expect(self, ok, what):
        self.done += 1
        if not ok:
            self.failed.append(what)

    def report(self, title):
        print(f"{'ok  ' if not self.failed else 'FAIL'} {title}: {self.done} checks" + ("" if not self.failed else f", {len(self.failed)} failed"))
        for what in self.failed:
            print(f"     failed: {what}")
        return len(self.failed)


def group(title, checks):
    """Run one group of checks and report it. An error that stops the group counts as a failure."""
    try:
        done = checks()
    except Exception as err:
        print(f"FAIL {title}: stopped by {type(err).__name__}: {err}")
        return 1
    return done.report(title)


# ----------------------------------------------------------------------------- reading sheets

def as_sets(sheet):
    cells, joins, _ = sheet
    return set(cells), {frozenset(j) for j in joins}


def refused(text):
    """True if read_sheet refuses the text with a ValueError, the error that main reports as unreadable input."""
    try:
        read_sheet(text)
    except ValueError:
        return True
    return False


def reading_checks():
    t = Checks()
    cross = ".#.\n###\n.#.\n.#.\n"

    # blank lines
    for gap in ("\n", "   \n"):
        cells, joins, layout = read_sheet(".#.\n###\n" + gap + ".#.\n.#.\n")
        t.expect(sorted(layout.values()) == [(0, 1), (1, 0), (1, 1), (1, 2), (3, 1), (4, 1)],
                 "a blank line between two rows of the picture is a row of empty places")
        result = decide(cells, joins)
        t.expect(not result.applicable and "one piece" in result.reason,
                 "a cross cut in two by a blank line is not in one piece")
    t.expect(as_sets(read_sheet("\n  \n" + cross + "\n\n")) == as_sets(read_sheet(cross)),
             "blank lines before the first row and after the last are ignored")
    t.expect(as_sets(read_sheet("###\n###\n\n\nslit 0 0 right\n")) == as_sets(read_sheet("###\n###\nslit 0 0 right\n")),
             "blank lines between the picture and the slit lines are ignored")
    cells, joins, layout = read_sheet("###\n\n###\nslit 2 0 right\n")
    t.expect(len(cells) == 6 and len(joins) == 3 and frozenset(((0, -2), (1, -2))) not in {frozenset(j) for j in joins},
             "slit row numbers count a blank line inside the picture")
    t.expect(refused("###\n\n###\nslit 1 0 right\n"), "a slit in a blank row is refused")

    # comments, blanks and dots
    t.expect(as_sets(read_sheet("; one\n###\n ; two\n###\nslit 1 0 right\n; three\n")) == as_sets(read_sheet("###\n###\nslit 1 0 right\n")),
             "comment lines are not rows")
    t.expect(as_sets(read_sheet(" #\n###\n #\n #\n")) == as_sets(read_sheet(cross)), "a blank is an empty place")
    t.expect(sorted(read_sheet("...\n" + cross)[2].values()) == [(1, 1), (2, 0), (2, 1), (2, 2), (3, 1), (4, 1)],
             "a row of dots is a row")

    # slits
    square = {frozenset(((0, 0), (1, 0))), frozenset(((0, -1), (1, -1))), frozenset(((0, 0), (0, -1))), frozenset(((1, 0), (1, -1)))}
    t.expect(as_sets(read_sheet("##\n##\n"))[1] == square, "squares that share a side are attached")
    t.expect(as_sets(read_sheet("##\n##\nslit 0 0 right\n"))[1] == square - {frozenset(((0, 0), (1, 0)))}, "slit ... right")
    t.expect(as_sets(read_sheet("##\n##\nslit 0 1 down\n"))[1] == square - {frozenset(((1, 0), (1, -1)))}, "slit ... down")
    t.expect(as_sets(read_sheet("slit 1 0 right\n##\n##\n"))[1] == square - {frozenset(((0, -1), (1, -1)))}, "a slit line may come first")
    t.expect(as_sets(read_sheet("#.\n.#\n"))[1] == set(), "squares that touch only at a corner are not attached")
    for bad in ("##\n##\nslits 0 0 right\n", "##\n##\nslitherin 0 0 right\n", "##\n##\nslit 0 0 left\n",
                "##\n##\nslit 0 0\n", "##\n##\nslit a 0 right\n", "##\n##\nslit -1 0 down\n",
                "##\n##\nslit 0.0 0 right\n", "##\n##\nslit 0 1 right\n", "##\n##\nslit 5 5 down\n",
                "#X#\n", "### ; three\n", "\t#\n", "", "\n\n", "; only a comment\n", "...\n"):
        t.expect(refused(bad), f"refused: {bad!r}")

    # the JSON form
    json_cross = '{"cells": [[1, 0], [0, -1], [1, -1], [2, -1], [1, -2], [1, -3]]}'
    t.expect(as_sets(read_sheet(json_cross)) == as_sets(read_sheet(cross)) and read_sheet(json_cross)[2] is None,
             "JSON with only \"cells\": all squares that share a side are attached")
    block = '"cells": [[0, 0], [1, 0], [2, 0], [0, -1], [1, -1], [2, -1]]'
    picture = as_sets(read_sheet("###\n###\nslit 0 0 right\nslit 1 1 right\n"))
    t.expect(as_sets(read_sheet("{" + block + ', "slits": [[0, 1], [5, 4]]}')) == picture, "JSON with \"slits\"")
    t.expect(as_sets(read_sheet("  \n{" + block + ', "joins": [[1, 2], [3, 4], [0, 3], [4, 1], [2, 5]]}')) == picture, "JSON with \"joins\"")
    t.expect(read_sheet("{" + block + "}")[0] == [(0, 0), (1, 0), (2, 0), (0, -1), (1, -1), (2, -1)],
             "JSON: the squares keep the order in which they are listed")
    malformed = {
        "a slit that is not two squares sharing a side": "{" + block + ', "slits": [[0, 5]]}',
        "a join that is not two squares sharing a side": "{" + block + ', "joins": [[0, 2]]}',
        "squares that touch only at a corner": "{" + block + ', "joins": [[0, 4]]}',
        "a negative index in joins": "{" + block + ', "joins": [[2, -1]]}',
        "a negative index in slits": "{" + block + ', "slits": [[-2, 5]]}',
        "an index out of range": "{" + block + ', "slits": [[0, 6]]}',
        "a pair that names one square twice": "{" + block + ', "joins": [[0, 0]]}',
        "both joins and slits": "{" + block + ', "joins": [[0, 1]], "slits": [[1, 2]]}',
        "an empty sheet": '{"cells": []}',
        "a repeated square": '{"cells": [[0, 0], [1, 0], [0, 0]]}',
        "coordinates that are not whole numbers": '{"cells": [[1.0, 3.0], [0.0, 2.0], [1.0, 2.0], [2.0, 2.0], [1.0, 1.0], [1.0, 0.0]]}',
        "half-integer coordinates": '{"cells": [[0.5, 0], [1.5, 0]]}',
        "true and false as coordinates": '{"cells": [[false, false], [true, false]]}',
        "text as coordinates": '{"cells": [["0", "0"]]}',
        "three coordinates": '{"cells": [[0, 0, 0], [1, 0, 0]]}',
        "an index that is not a whole number": "{" + block + ', "joins": [[0.0, 1.0]]}',
        "true and false as an index": "{" + block + ', "slits": [[false, true]]}',
        "a pair with three entries": "{" + block + ', "joins": [[0, 1, 2]]}',
        "joins that are not a list": "{" + block + ', "joins": {"0": 1}}',
        "no cells": "{}",
        "cells that are not a list": '{"cells": "###"}',
        "an unknown key": "{" + block + ', "slit": [[0, 1]]}',
        "a key given twice": "{" + block + ", " + block + "}",
        "JSON that is cut short": '{"cells": [[0, 0],',
    }
    for name, text in malformed.items():
        t.expect(refused(text), f"JSON refused: {name}")

    # decide() itself, called with input that read_sheet would have refused
    for cells, joins in (([], []), ([(0, 0), (0, 0)], []), ([(0.0, 0.0), (1.0, 0.0)], []), ([(0, 0), (2, 0)], [((0, 0), (2, 0))]),
                         ([(0, 0), (1, 0)], [((0, 0), (5, 5))]), ([(0, 0), (True, 0)], [])):
        result = decide(cells, joins)
        t.expect(not result.applicable and result.reason and result.folds is None, f"decide() gives no answer for cells={cells} joins={joins}")
    return t


# ----------------------------------------------------------------------------- the limit on the number of lines

# A strip of seven squares with one bend. It folds, but not with fewer than six fold lines.
NEEDS_SIX = "#...\n#...\n#...\n####\n"


def limit_checks():
    t = Checks()
    cells, joins, _ = read_sheet(".#.\n###\n.#.\n.#.\n")
    usual = decide(cells, joins)
    same = decide(cells, joins, max_lines=7)
    t.expect((usual.folds, usual.fold_lines, usual.sides, usual.sets_tried) == (same.folds, same.fold_lines, same.sides, same.sets_tried),
             "max_lines=7 is the default")
    t.expect(decide(cells, joins, max_lines=5).folds is True, "the cross folds with five lines")
    t.expect(decide(cells, joins, max_lines=4).folds is False, "the cross does not fold with four lines")
    cells, joins, _ = read_sheet(NEEDS_SIX)
    t.expect(brute_force_has_six_sided_map(cells, joins) and decide(cells, joins).folds is True, "the six-line sheet folds")
    t.expect(decide(cells, joins, max_lines=6).folds is True, "the six-line sheet folds with six lines")
    t.expect(decide(cells, joins, max_lines=5).folds is False, "the six-line sheet does not fold with five lines")
    return t


# ----------------------------------------------------------------------------- position

def turned(cell, t):
    """One of the 8 rotations and reflections of the plane, numbered 0 to 7."""
    x, y = cell
    if t & 1:
        x = -x
    if t & 2:
        y = -y
    if t & 4:
        x, y = y, x
    return (x, y)


def position_checks(sheets):
    """Each sheet in all 8 positions, and in each a second time, moved and with its last square first."""
    runs = changed = 0
    for label, cells, joins in sheets:
        base = decide(cells, joins)
        for t in range(8):
            cells_t = [turned(c, t) for c in cells]
            joins_t = [(turned(a, t), turned(b, t)) for a, b in joins]
            moved = [(x + 3, y - 5) for x, y in cells_t]
            moved = moved[-1:] + moved[:-1]
            joins_m = [((a[0] + 3, a[1] - 5), (b[0] + 3, b[1] - 5)) for a, b in joins_t]
            for cs, js in ((cells_t, joins_t), (moved, joins_m)):
                runs += 1
                try:
                    result = decide(cs, js)
                    now = (result.applicable, result.folds)
                except Exception as err:
                    now = f"{type(err).__name__}: {err}"
                if now != (base.applicable, base.folds):
                    changed += 1
                    print(f"ANSWER CHANGED ({label}, position {t}): {(base.applicable, base.folds)} became {now}: cells={cs} joins={js}")
    return runs, changed


# ----------------------------------------------------------------------------- the command line

def run(args, stdin_text="", flags=()):
    """Start decide.py as a separate program. Returns (exit status, standard output, standard error)."""
    done = subprocess.run([sys.executable, "-B", *flags, PROGRAM, *args], input=stdin_text,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=HERE)
    return done.returncode, done.stdout, done.stderr


def run_changed(change, sheet_file, flags=()):
    """Start a copy of the program in which one thing has been changed on purpose."""
    code = ("import sys\n"
            f"sys.path.insert(0, {HERE!r})\n"
            "import decide\n"
            + change +
            f"sys.exit(decide.main([{sheet_file!r}]))\n")
    done = subprocess.run([sys.executable, "-B", *flags, "-c", code], input="",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=HERE)
    return done.returncode, done.stdout, done.stderr


# The fold lines are moved one place, so the folding that the search finds is wrong and the
# check of a "yes" must catch it.
WRONG_LINES = ("real = decide.find_cuts\n"
               "def wrong(sheet, stars):\n"
               "    cuts = real(sheet, stars)\n"
               "    for cut in cuts:\n"
               "        cut['line'] += 1\n"
               "    return cuts\n"
               "decide.find_cuts = wrong\n")
CRASH = "decide.decide = lambda cells, joins: 1 // 0\n"


def bent_pairs(joins, sides):
    """The attached sides across which the letter changes."""
    return {frozenset(j) for j in joins if sides[j[0]] != sides[j[1]]}


def pairs_on_lines(fold_lines):
    """The pairs of squares on either side of the fold lines of the --json output, read as the README says."""
    pairs = set()
    for line in fold_lines:
        for u in range(line["from"], line["to"]):
            if line["axis"] == "x":     # vertical grid line x = line, from y = from to y = to
                pairs.add(frozenset(((line["line"] - 1, u), (line["line"], u))))
            else:                       # horizontal grid line y = line, from x = from to x = to
                pairs.add(frozenset(((u, line["line"] - 1), (u, line["line"]))))
    return pairs


def read_printed_yes(output):
    """Read back a printed "yes": (number of squares, fold lines as printed, picture rows)."""
    lines = output.splitlines()
    head = re.fullmatch(r"FOLDS ONTO THE CUBE: yes \((\d+) squares?\)", lines[0])
    count = re.fullmatch(r"Corner folds \(90 degrees\) along (\d+) lines?; every other attached side is a flat fold \(180 degrees\):", lines[1])
    if not head or not count:
        return None
    k = 2
    folds = []
    while lines[k].startswith("  "):
        folds.append(lines[k][2:])
        k += 1
    rows = []
    if lines[k].startswith("Side of the cube for each square"):
        k += 1
        while lines[k].startswith("  "):
            rows.append(lines[k][2:])
            k += 1
    if len(folds) != int(count.group(1)) or not lines[k].startswith("This assignment was rebuilt"):
        return None
    return int(head.group(1)), folds, rows


def printed_checks(t, name, text, output):
    """The printed picture and fold lines of a "yes" for a sheet given as a picture."""
    cells, joins, layout = read_sheet(text)
    printed = read_printed_yes(output)
    t.expect(printed is not None, f"{name}: the printed answer has the expected form")
    if printed is None:
        return
    squares, folds, rows = printed
    place = {rc: cell for cell, rc in layout.items()}
    letters = {}
    stray = 0
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if (r, c) in place and ch in LETTERS:
                letters[place[(r, c)]] = ch
            elif (r, c) in place or ch != ".":
                stray += 1
    t.expect(stray == 0 and len(letters) == len(cells) == squares, f"{name}: one letter for each square and a dot elsewhere")
    t.expect(set(letters.values()) == LETTERS, f"{name}: all six letters appear in the printed picture")
    t.expect(letters == decide(cells, joins).sides, f"{name}: the printed letters are those decide() returns")
    if len(letters) != len(cells):
        return
    on_lines = set()
    for fold in folds:
        across_rows = re.fullmatch(r"between rows (\d+) and (\d+), columns (\d+) to (\d+)", fold)
        across_cols = re.fullmatch(r"between columns (\d+) and (\d+), rows (\d+) to (\d+)", fold)
        if across_rows:
            a, b, lo, hi = map(int, across_rows.groups())
            on_lines |= {frozenset((place.get((a, c)), place.get((b, c)))) for c in range(lo, hi + 1)}
        elif across_cols:
            a, b, lo, hi = map(int, across_cols.groups())
            on_lines |= {frozenset((place.get((r, a)), place.get((r, b)))) for r in range(lo, hi + 1)}
        else:
            on_lines.add(None)
    t.expect(on_lines == bent_pairs(joins, letters),
             f"{name}: the printed fold lines are exactly the attached sides across which the letter changes")


def command_line_checks():
    t = Checks()
    status_of = {"cross.txt": 0, "section-6.txt": 0, "block-3x3-with-slits.txt": 0, "rectangle-2x3.txt": 1, "ring.txt": 2}
    first_words = {0: "FOLDS ONTO THE CUBE: yes", 1: "FOLDS ONTO THE CUBE: no", 2: "Not a sheet without holes: "}
    t.expect(sorted(os.listdir(EXAMPLES)) == sorted(status_of), "the examples folder holds the five sheets")
    for name, status in sorted(status_of.items()):
        path = os.path.join(EXAMPLES, name)
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        cells, joins, layout = read_sheet(text)
        result = decide(cells, joins)
        plain = run([path])
        as_json = run(["--json", path])
        t.expect(plain[0] == status and as_json[0] == status, f"{name}: exit status {status}")
        t.expect(plain[1].startswith(first_words[status]) and plain[2] == "" and as_json[2] == "", f"{name}: the answer is printed")
        try:
            data = json.loads(as_json[1])
        except ValueError:
            data = None
        t.expect(data == {
            "applicable": result.applicable, "reason": result.reason, "folds": result.folds, "squares": result.squares,
            "cuts_available": result.cuts_available, "sets_tried": result.sets_tried, "fold_lines": result.fold_lines,
            "sides": [[list(c), s] for c, s in sorted(result.sides.items())],
        }, f"{name}: the --json output parses and agrees with decide()")
        t.expect(run(["-"], text) == plain and run(["--json", "-"], text) == as_json, f"{name}: - reads standard input")
        t.expect(run([path], flags=["-O"]) == plain and run(["--json", path], flags=["-O"]) == as_json,
                 f"{name}: python -O gives the same output and exit status")
        if status == 0 and data is not None:
            sides = {tuple(c): s for c, s in data["sides"]}
            t.expect(set(sides) == {(c, -r) for r, c in layout.values()}, f"{name}: in --json, the square in row r and column c is [c, -r]")
            t.expect(set(sides.values()) == LETTERS and pairs_on_lines(data["fold_lines"]) == bent_pairs(joins, sides),
                     f"{name}: the --json fold lines are exactly the attached sides across which the letter changes")
            printed_checks(t, name, text, plain[1])

    # a picture that does not start in the corner, and a sheet given as JSON
    shifted = "; a cube net\n.....\n...#.\n.###.\n..#..\n..#..\n"
    status, out, err = run(["-"], shifted)
    t.expect(status == 0 and err == "", "a cube net away from the corner folds")
    printed_checks(t, "a cube net away from the corner", shifted, out)
    as_json_input = '{"cells": [[1, 3], [0, 2], [1, 2], [2, 2], [1, 1], [1, 0]], "joins": [[0, 2], [1, 2], [2, 3], [2, 4], [4, 5]]}'
    cells, joins, _ = read_sheet(as_json_input)
    status, out, err = run(["-"], as_json_input)
    printed = read_printed_yes(out) if status == 0 else None
    t.expect(printed is not None and printed[2] == [], "a sheet given as JSON: the answer is printed, without a picture")
    if printed is not None:
        lines = []
        for fold in printed[1]:
            m = (re.fullmatch(r"vertical grid line at (x) = (-?\d+), from y = (-?\d+) to (-?\d+)", fold)
                 or re.fullmatch(r"horizontal grid line at (y) = (-?\d+), from x = (-?\d+) to (-?\d+)", fold))
            lines.append({"axis": m.group(1), "line": int(m.group(2)), "from": int(m.group(3)), "to": int(m.group(4))} if m else None)
        t.expect(lines == decide(cells, joins).fold_lines, "a sheet given as JSON: the printed fold lines are those decide() returns")
        t.expect(None not in lines and pairs_on_lines(lines) == {frozenset(j) for j in joins},
                 "a sheet given as JSON: the printed grid lines are the five attached sides of the cross")

    # exit status 1, and the wording for one square and one line
    for text, words in (("#\n", "no (1 square, 0 possible fold lines)"), ("##\n", "no (2 squares, 1 possible fold line)"),
                        ("##.\n#.#\n###\n", "no (7 squares, 6 possible fold lines)")):
        status, out, err = run(["-"], text)
        t.expect(status == 1 and out.startswith("FOLDS ONTO THE CUBE: " + words + "\n") and err == "", f"{text!r}: {words}")

    # exit status 2: not a sheet without holes (standard output), or input that cannot be read (standard error)
    for text, reason in ((".#.\n###\n   \n.#.\n.#.\n", "the sheet is not in one piece"), ("#.\n.#\n", "the sheet is not in one piece"),
                         ("###\n###\n###\nslit 1 1 right\n", "the sheet has a hole")):
        status, out, err = run(["-"], text)
        t.expect(status == 2 and out.startswith("Not a sheet without holes: " + reason) and err == "", f"{text!r}: {reason}")
    unreadable = [["-"], ["--json", "-"]]
    for text in ("###\n#X#\n", "", '{"cells": [[1.0, 3.0], [0.0, 2.0], [1.0, 2.0], [2.0, 2.0], [1.0, 1.0], [1.0, 0.0]]}',
                 '{"cells": [[0, 0], [1, 0]], "joins": [[0, 0]]}', "##\n##\nslits 0 0 right\n"):
        for args in unreadable:
            status, out, err = run(args, text)
            t.expect(status == 2 and out == "" and err.startswith("Cannot read the sheet: ") and len(err.splitlines()) == 1,
                     f"{text!r} with {args}: cannot be read")
    status, out, err = run([os.path.join(HERE, "no-such-file.txt")])
    t.expect(status == 2 and out == "" and err.startswith("Cannot read the sheet: "), "a file that does not exist")
    for args in ([], ["a.txt", "b.txt"], ["--no-such-option"]):
        status, out, err = run(args)
        t.expect(status == 2 and out == "" and err.startswith("usage: "), f"wrong command line {args}")

    # exit status 0 for help
    for args in (["-h"], ["--help"]):
        status, out, err = run(args)
        t.expect(status == 0 and "python3 decide.py --json SHEET_FILE" in out and "Exit status" in out and err == "", f"{args[0]} prints the usage")

    # exit status 3: the program fails, or its check of a "yes" fails; with and without -O
    cross = os.path.join(EXAMPLES, "cross.txt")
    for change, words, what in ((WRONG_LINES, "check of its own work failed", "a wrong folding is caught by the check of a \"yes\""),
                                (CRASH, "ZeroDivisionError", "a failure inside the program")):
        for flags in ([], ["-O"]):
            status, out, err = run_changed(change, cross, flags)
            t.expect(status == 3 and out == "" and err.startswith("Internal error, no answer: ") and words in err
                     and len(err.splitlines()) == 1, f"{what}: exit status 3 {' '.join(flags)}")
    return t


# ----------------------------------------------------------------------------- the run

def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    failures = 0

    # ---- fixed examples
    fixed = []
    for name, (text, expected) in FIXED_EXAMPLES.items():
        cells, joins, _ = read_sheet(text)
        fixed.append((name, cells, joins))
        try:
            result = decide(cells, joins)
        except Exception as err:
            print(f"FAIL {name}: decide() failed with {type(err).__name__}: {err}")
            failures += 1
            continue
        if expected == "n/a":
            ok = not result.applicable
        else:
            ok = result.applicable and result.folds == brute_force_has_six_sided_map(cells, joins)
            if expected is not None:
                ok = ok and result.folds == expected
        print(f"{'ok  ' if ok else 'FAIL'} {name}: " + ("not applicable" if not result.applicable else ("folds" if result.folds else "does not fold")))
        failures += not ok

    # ---- reading sheets, and the limit on the number of lines
    failures += group("reading sheets", reading_checks)
    failures += group("the limit on the number of fold lines", limit_checks)

    limits = dict.fromkeys(["fold", "need a seventh line", "need a sixth line"], 0)

    # ---- every sheet with all sides attached, up to n_full squares
    n_full = 9 if quick else 10
    n_position = 7 if quick else 8
    small = []
    counts = dict.fromkeys(["folds", "does not fold", "not a sheet without holes", "MISMATCHES"], 0)
    for n, shapes in free_polyominoes(n_full):
        for cells in shapes:
            check(list(cells), adjacencies(cells), counts, f"all attached, {n} squares", limits)
            if n <= n_position:
                small.append((f"all attached, {n} squares", list(cells), adjacencies(cells)))
    print(f"all sides attached, up to {n_full} squares: {counts}")
    failures += counts["MISMATCHES"]

    # ---- every pattern of slits, up to n_slit squares
    n_slit = 7 if quick else 8
    counts = dict.fromkeys(["folds", "does not fold", "not a sheet without holes", "MISMATCHES"], 0)
    for n, shapes in free_polyominoes(n_slit):
        for cells in shapes:
            adj = adjacencies(cells)
            for r in range(1, len(adj) + 1):
                for cut in itertools.combinations(range(len(adj)), r):
                    joins = [a for i, a in enumerate(adj) if i not in cut]
                    check(list(cells), joins, counts, f"slits, {n} squares", limits)
    print(f"every pattern of slits, up to {n_slit} squares: {counts}")
    failures += counts["MISMATCHES"]

    # ---- random larger sheets with random slits
    rng = random.Random(20261114)
    counts = dict.fromkeys(["folds", "does not fold", "not a sheet without holes", "MISMATCHES"], 0)
    trials = 150 if quick else 600
    for _ in range(trials):
        n = rng.randint(9, 14)
        cells = [(0, 0)]
        present = {(0, 0)}
        while len(cells) < n:
            x, y = rng.choice(cells)
            q = rng.choice([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
            if q not in present:
                present.add(q)
                cells.append(q)
        joins = adjacencies(cells)
        if not decide(cells, joins).applicable:
            continue
        # cut attached sides at random, keeping each cut only if the sheet stays without holes
        for a in rng.sample(joins, len(joins)):
            if rng.random() < 0.5:
                fewer = [j for j in joins if j != a]
                if decide(cells, fewer).applicable:
                    joins = fewer
        check(cells, joins, counts, "random", limits)
    print(f"random sheets with 9 to 14 squares and random slits: {counts}")
    failures += counts["MISMATCHES"]

    # ---- information, not a test: what a smaller limit on the number of fold lines would change
    print(f"information: of the {limits['fold']} sheets that fold in the three groups above, "
          f"{limits['need a seventh line']} stop folding when at most six fold lines are allowed instead of seven, "
          f"and {limits['need a sixth line']} more when at most five are allowed")

    # ---- position
    try:
        runs, changed = position_checks(fixed + small)
    except Exception as err:
        print(f"FAIL position: stopped by {type(err).__name__}: {err}")
        runs, changed = 0, 1
    print(f"{'ok  ' if not changed else 'FAIL'} position: {len(fixed)} fixed examples and {len(small)} sheets with all sides attached, "
          f"up to {n_position} squares, in 8 positions, each run twice: {runs} runs, {changed} answers changed")
    failures += changed

    # ---- the command line and the printed output
    failures += group("command line and printed output", command_line_checks)

    print(f"{'ALL TESTS PASSED' if not failures else str(failures) + ' FAILURES'} in {time.time() - t0:.0f} s")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
