#!/usr/bin/env python3
"""Decide whether a sheet of unit squares without holes folds onto the unit cube.

This program follows the procedure in the proof of Corollary A2 of the manuscript
(disk-folding/output/pdf/disk-folding-manuscript.pdf, Section 5). It needs Python 3.8 or
newer and nothing outside the standard library.

    python3 decide.py SHEET_FILE          human-readable answer
    python3 decide.py --json SHEET_FILE   the same as JSON
    python3 decide.py -                   read the sheet from standard input
    python3 decide.py --help              print this text

Exit status:
    0  the sheet folds onto the cube
    1  it does not
    2  the input cannot be read, or it is not a sheet without holes (the theorem says
       nothing about it), or the command line is wrong
    3  the program itself failed, or its check of a "yes" failed; there is no answer

WHAT THE ANSWERS MEAN

"yes": the program has found a way to assign every square to a side of the cube, with at
most seven straight lines of corner folds and flat folds everywhere else, such that squares
that are attached stay attached and all six sides are covered. It rebuilds that assignment
corner by corner and checks it directly, so a "yes" does not rest on the theory for this
part. That such an assignment can be carried out with real paper, with the layers in a
workable order, is Theorem A of the manuscript; the program does not compute the layers.
The lines it reports are the first set it finds that works, not the fewest possible.

"no": no choice of up to seven lines works. That then no assignment at all exists, with any
number of lines, is Proposition C3 of the manuscript, which rests on a computer-checked
step.

The manuscript is a claimed result. It has not been reviewed by a human with sufficient
expertise in this field.

INPUT

A picture, one text line per row of the sheet: `#` is a square, `.` or a blank is empty.
A blank line between two rows of the picture is a row of empty places. Blank lines before
the first row of the picture and after the last are ignored. Squares that share a side are
attached unless a line says otherwise:

    slit ROW COL right     the side between square (ROW, COL) and the one to its right is cut
    slit ROW COL down      the side between square (ROW, COL) and the one below it is cut

Rows and columns are counted from 0, from the top left; a blank line inside the picture
counts as a row. Lines that begin with `;` are comments and are not rows. Squares that
touch only at a corner are not attached there.

Alternatively the input may be JSON: {"cells": [[x, y], ...]}, optionally with either
"joins": [[i, j], ...] (the attached sides) or "slits": [[i, j], ...] (the cut sides), not
both. x and y are whole numbers, and i and j are positions in "cells", counted from 0. Each
pair must name two different squares that share a side. With neither key, all squares that
share a side are attached.

OUTPUT WITH --json

A square is named by [x, y] and covers the plane from x to x + 1 and from y to y + 1; y
grows upwards. For a picture, the square in row r and column c is [c, -r]. A fold line with
"axis": "x" lies on the vertical grid line x = "line" and runs from y = "from" to y = "to";
with "axis": "y" it lies on the horizontal grid line y = "line" and runs from x = "from" to
x = "to". "sides" gives, for each square, the side of the cube it lands on.

THE METHOD, IN THE MANUSCRIPT'S TERMS

1. The sheet must be connected through its attached sides, and N - R + n must equal 1,
   where N, R and n are the numbers of squares, attached sides and "full stars" (corner
   points at which four squares meet with all four sides between them attached).
2. A cut is a maximal straight run of attached sides along one grid line whose interior
   corner points are full stars. Two cuts cross when they share a full star.
3. Fold every attached side flat. All squares then lie on one side F0 of the cube, and
   each cut lies along one edge of F0.
4. For a set of cuts no two of which cross, fold the sheet by 90 degrees along those cuts
   instead. The squares beyond a cut, seen from a fixed root square, are moved by the
   reflection of the cube that fixes the cut's edge; nested cuts compose, outermost first.
5. The sheet folds onto the cube if and only if some such set of five, six or seven cuts
   covers all six sides.
"""
import json
import sys
from collections import deque
from numbers import Integral

USAGE = """\
usage: python3 decide.py [--json] SHEET_FILE
       python3 decide.py [--json] -        read the sheet from standard input
       python3 decide.py --help            explain the input, the answers and the exit status
"""


class SelfCheckError(Exception):
    """The program found its own working to be inconsistent. There is then no answer."""


# ----------------------------------------------------------------------------- the cube
# Cube corners are triples of 0/1. The root square lies on the side z = 0, which the
# pictures call D (down). The other sides: U up (z = 1), F front (y = 0), B back (y = 1),
# L left (x = 0), R right (x = 1).
CORNERS = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
CORNER_INDEX = {c: i for i, c in enumerate(CORNERS)}
SIDES = {(2, 0): "D", (2, 1): "U", (1, 0): "F", (1, 1): "B", (0, 0): "L", (0, 1): "R"}
SIDE_ORDER = "DUFBLR"


def _perm(fn):
    return tuple(CORNER_INDEX[fn(*c)] for c in CORNERS)


# The four edges of the side z = 0, and for each the reflection of the cube that fixes the
# edge point by point and exchanges the two sides that meet along it.
REFLECTIONS = {
    ("x", 0): _perm(lambda x, y, z: (z, y, x)),            # edge x = 0, z = 0
    ("x", 1): _perm(lambda x, y, z: (1 - z, y, 1 - x)),    # edge x = 1, z = 0
    ("y", 0): _perm(lambda x, y, z: (x, z, y)),            # edge y = 0, z = 0
    ("y", 1): _perm(lambda x, y, z: (x, 1 - z, 1 - y)),    # edge y = 1, z = 0
}
IDENTITY = tuple(range(8))


def compose(a, b):
    """The symmetry "first b, then a"."""
    return tuple(a[b[i]] for i in range(8))


def side_of(corner_indices):
    """The side of the cube that contains the given corners, as a letter."""
    pts = [CORNERS[i] for i in corner_indices]
    for axis in range(3):
        values = {p[axis] for p in pts}
        if len(values) == 1:
            return SIDES[(axis, values.pop())]
    raise SelfCheckError("corners do not lie on one side of the cube")


BASE_SIDE = [CORNER_INDEX[(x, y, 0)] for x in (0, 1) for y in (0, 1)]


# ----------------------------------------------------------------------------- the sheet
def _is_whole(value):
    """A whole number, and not True or False."""
    return isinstance(value, Integral) and not isinstance(value, bool)


class Sheet:
    """Squares at integer positions (x, y) and the set of attached sides between them."""

    def __init__(self, cells, joins):
        try:
            self.cells = [tuple(c) for c in cells]
        except TypeError:
            raise ValueError("the position of a square must be a pair of whole numbers") from None
        for c in self.cells:
            if len(c) != 2 or not (_is_whole(c[0]) and _is_whole(c[1])):
                raise ValueError("the position of a square must be a pair of whole numbers")
        self.index = {c: i for i, c in enumerate(self.cells)}
        if len(self.index) != len(self.cells):
            raise ValueError("a square is listed twice")
        self.joins = set()
        for join in joins:
            try:
                a, b = (tuple(end) for end in join)
            except (TypeError, ValueError):
                raise ValueError("an attached side must be a pair of squares") from None
            if a not in self.index or b not in self.index:
                raise ValueError("an attached side names a square that is not in the sheet")
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
                raise ValueError("an attached side joins two squares that do not share a side")
            self.joins.add(frozenset((a, b)))

    def joined(self, a, b):
        return frozenset((a, b)) in self.joins

    def neighbours(self, c):
        x, y = c
        for d in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if d in self.index and self.joined(c, d):
                yield d

    def component(self, start, removed=frozenset()):
        """Squares reachable from `start` through attached sides other than `removed`."""
        seen = {start}
        queue = deque([start])
        while queue:
            c = queue.popleft()
            for d in self.neighbours(c):
                if d not in seen and frozenset((c, d)) not in removed:
                    seen.add(d)
                    queue.append(d)
        return seen

    def is_full_star(self, p):
        """Four squares meet at the corner point p, with all four sides between them attached."""
        i, j = p
        a, b, c, d = (i - 1, j - 1), (i, j - 1), (i, j), (i - 1, j)
        return (all(q in self.index for q in (a, b, c, d))
                and self.joined(a, b) and self.joined(b, c) and self.joined(c, d) and self.joined(d, a))

    def full_stars(self):
        points = {(x + dx, y + dy) for (x, y) in self.cells for dx in (0, 1) for dy in (0, 1)}
        return {p for p in points if self.is_full_star(p)}


def find_cuts(sheet, stars):
    """All cuts: maximal straight runs of attached sides whose interior corner points are full stars.

    Each cut is a dict with: axis ("x" for a vertical grid line, "y" for a horizontal one),
    line (the coordinate of that grid line), lo and hi (its extent along the line), joins
    (the attached sides on it) and stars (its interior corner points).
    """
    # An attached side between (x, y) and (x+1, y) is the unit segment on the vertical line
    # at x+1 from height y to y+1; between (x, y) and (x, y+1) it lies on the horizontal
    # line at y+1 from x to x+1.
    segments = {}
    for j in sheet.joins:
        a, b = sorted(j)
        if a[1] == b[1]:
            segments[("x", b[0], a[1])] = j
        else:
            segments[("y", b[1], a[0])] = j
    cuts = []
    used = set()
    for key in sorted(segments):
        if key in used:
            continue
        axis, line, t = key
        point = (lambda s: (line, s)) if axis == "x" else (lambda s: (s, line))
        lo = t
        while point(lo) in stars:           # extend backwards through full stars
            lo -= 1
            if (axis, line, lo) not in segments:
                raise SelfCheckError("a full star has no attached side on one of its four arms")
        run = []
        s = lo
        while True:
            run.append((axis, line, s))
            used.add((axis, line, s))
            if point(s + 1) not in stars:
                break
            s += 1
            if (axis, line, s) not in segments:
                raise SelfCheckError("a full star has no attached side on one of its four arms")
        cuts.append({
            "axis": axis, "line": line, "lo": lo, "hi": s + 1,
            "joins": frozenset(segments[k] for k in run),
            "stars": frozenset(point(u) for u in range(lo + 1, s + 1)),
        })
    if sum(len(c["joins"]) for c in cuts) != len(sheet.joins):
        raise SelfCheckError("the cuts do not use every attached side exactly once")
    return cuts


class Decision:
    def __init__(self):
        self.applicable = False     # is the input a sheet without holes?
        self.reason = ""            # why not, if not
        self.folds = None           # True / False when applicable
        self.squares = 0
        self.cuts_available = 0
        self.sets_tried = 0
        self.fold_lines = []        # the cuts used, when it folds
        self.sides = {}             # square -> letter of the side it lands on


def decide(cells, joins, max_lines=7):
    """Decide whether the sheet folds onto the cube. Returns a Decision.

    `max_lines` is the largest number of fold lines a set may have. The manuscript's bound,
    and the default, is 7. The tests pass smaller values to see what the bound does; the
    answer for the manuscript's question is the one with the default.

    Raises SelfCheckError if the program finds its own working to be inconsistent; there is
    then no answer.
    """
    if not _is_whole(max_lines):
        raise ValueError("max_lines must be a whole number")
    out = Decision()
    try:
        sheet = Sheet(cells, joins)
    except ValueError as err:
        out.reason = str(err)
        return out
    n_cells = len(sheet.cells)
    out.squares = n_cells
    if n_cells == 0:
        out.reason = "the sheet has no squares"
        return out
    root = sheet.cells[0]
    if len(sheet.component(root)) != n_cells:
        out.reason = "the sheet is not in one piece"
        return out
    stars = sheet.full_stars()
    if n_cells - len(sheet.joins) + len(stars) != 1:
        out.reason = "the sheet has a hole (a window, or a slit that does not reach the border)"
        return out
    out.applicable = True

    cuts = find_cuts(sheet, stars)
    # For each cut: the squares beyond it as seen from the root square, and the edge of the
    # base side that the cut lies along once every attached side is folded flat.
    for c in cuts:
        beyond = set(sheet.cells) - sheet.component(root, removed=c["joins"])
        if not beyond or len(beyond) >= n_cells:
            raise SelfCheckError("a cut does not split the sheet in two")
        c["beyond"] = frozenset(beyond)
        origin = root[0] if c["axis"] == "x" else root[1]
        c["reflection"] = REFLECTIONS[(c["axis"], (c["line"] - origin) % 2)]
    # Outermost cuts first: a cut can only lie beyond cuts with a strictly larger far side.
    cuts.sort(key=lambda c: (-len(c["beyond"]), c["axis"], c["line"], c["lo"]))
    k = len(cuts)
    out.cuts_available = k

    crosses = [0] * k           # bit j set: cuts i and j share a full star
    star_owner = {}
    for i, c in enumerate(cuts):
        for p in c["stars"]:
            if p in star_owner:
                j = star_owner[p]
                crosses[i] |= 1 << j
                crosses[j] |= 1 << i
            else:
                star_owner[p] = i
    beyond_of = [0] * k         # bit j set: cut i lies beyond cut j
    for i, c in enumerate(cuts):
        for j, d in enumerate(cuts):
            if i == j or crosses[i] >> j & 1:
                continue
            flags = {cell in d["beyond"] for join in c["joins"] for cell in join}
            if len(flags) != 1:
                raise SelfCheckError("a cut lies on both sides of a cut that it does not cross")
            if flags.pop():
                if len(d["beyond"]) <= len(c["beyond"]):
                    raise SelfCheckError("a cut beyond another does not have a smaller far side")
                beyond_of[i] |= 1 << j

    base = side_of(BASE_SIDE)
    all_sides = set(SIDE_ORDER)
    chosen = []                 # indices of the cuts chosen so far, increasing
    moves = []                  # for each chosen cut, the symmetry that moves the squares just beyond it
    found = []
    # Five new sides are needed and each chosen cut adds at most one, so a set of at most
    # `max_lines` cuts has room for max_lines - 5 cuts that add no new side: two by default.
    spare_allowed = max_lines - 5

    def search(start, blocked, sides, spare):
        # `spare` counts chosen cuts that added no new side.
        for i in range(start, k):
            if blocked >> i & 1:
                continue
            parent = IDENTITY
            for pos in range(len(chosen) - 1, -1, -1):      # nearest chosen cut that i lies beyond
                if beyond_of[i] >> chosen[pos] & 1:
                    parent = moves[pos]
                    break
            move = compose(parent, cuts[i]["reflection"])
            side = side_of([move[v] for v in BASE_SIDE])
            new = side not in sides
            if not new and spare >= spare_allowed:
                continue
            out.sets_tried += 1
            chosen.append(i)
            moves.append(move)
            now = sides | {side}
            if now == all_sides:
                found.extend(chosen)
                return True
            if len(chosen) < max_lines and search(i + 1, blocked | crosses[i], now, spare + (not new)):
                return True
            chosen.pop()
            moves.pop()
        return False

    out.folds = n_cells >= 6 and max_lines >= 5 and search(0, 0, {base}, 0)
    if not out.folds:
        return out

    # ---- rebuild the folding corner by corner and check it directly
    used = [cuts[i] for i in found]            # outermost first
    if not 5 <= len(used) <= max_lines:
        raise SelfCheckError("the set found does not have between five and the allowed number of lines")
    corner_image = {}
    for cell in sheet.cells:
        move = IDENTITY
        for c in used:
            if cell in c["beyond"]:
                move = compose(move, c["reflection"])
        x, y = cell
        image = []
        for px, py in ((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)):
            flat = CORNER_INDEX[((px - root[0]) % 2, (py - root[1]) % 2, 0)]
            image.append(move[flat])
        if len(set(image)) != 4:
            raise SelfCheckError("a square does not land on four different corners of the cube")
        corner_image[cell] = dict(zip(((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)), image))
        out.sides[cell] = side_of(image)
    cut_joins = set().union(*(c["joins"] for c in used))
    for j in sheet.joins:
        a, b = tuple(j)
        shared = set(corner_image[a]) & set(corner_image[b])
        if len(shared) != 2:
            raise SelfCheckError("two attached squares do not share exactly two corner points")
        if any(corner_image[a][p] != corner_image[b][p] for p in shared):
            raise SelfCheckError("attached squares came apart")
        if (out.sides[a] != out.sides[b]) != (j in cut_joins):
            raise SelfCheckError("a fold is not where it should be")
    if set(out.sides.values()) != all_sides:
        raise SelfCheckError("a side of the cube is not covered")
    out.fold_lines = [{"axis": c["axis"], "line": c["line"], "from": c["lo"], "to": c["hi"]} for c in used]
    return out


# ----------------------------------------------------------------------------- input and output
def read_sheet(text):
    """Return (cells, joins, layout). `layout` maps a square to its (row, column), or is None.

    Raises ValueError, with a message that says what is wrong, if the text cannot be read as
    a sheet. Whether the sheet is in one piece and has no hole is not checked here; decide()
    does that.
    """
    if text.startswith("\ufeff"):       # a byte-order mark, which some editors put first
        text = text[1:]
    if text.lstrip().startswith("{"):
        return _read_json(text)
    return _read_picture(text)


def _short(value):
    shown = json.dumps(value)
    return shown if len(shown) <= 60 else shown[:57] + "..."


def _is_json_whole(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _no_repeated_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f'the key "{key}" appears twice')
        seen[key] = value
    return seen


def _read_json(text):
    try:
        data = json.loads(text, object_pairs_hook=_no_repeated_keys)
    except json.JSONDecodeError as err:
        raise ValueError(f"the JSON is not well formed: {err}") from None
    except RecursionError:
        raise ValueError("the JSON is nested too deeply") from None
    unknown = sorted(set(data) - {"cells", "joins", "slits"})
    if unknown:
        raise ValueError(f'unknown key "{unknown[0]}"; the keys are "cells", "joins" and "slits"')
    if "cells" not in data:
        raise ValueError('there is no "cells" list')
    if "joins" in data and "slits" in data:
        raise ValueError('give either "joins" or "slits", not both')
    if not isinstance(data["cells"], list):
        raise ValueError('"cells" must be a list of pairs [x, y]')
    cells = []
    index = {}
    for k, entry in enumerate(data["cells"]):
        if not (isinstance(entry, list) and len(entry) == 2
                and _is_json_whole(entry[0]) and _is_json_whole(entry[1])):
            raise ValueError(f'"cells" entry {k} is not a pair [x, y] of whole numbers: {_short(entry)}')
        cell = (entry[0], entry[1])
        if cell in index:
            raise ValueError(f'the square at {_short(entry)} is listed twice ("cells" entries {index[cell]} and {k})')
        index[cell] = k
        cells.append(cell)
    if not cells:
        raise ValueError("the sheet has no squares")

    def pairs(key):
        if not isinstance(data[key], list):
            raise ValueError(f'"{key}" must be a list of pairs [i, j]')
        out = set()
        for k, entry in enumerate(data[key]):
            where = f'"{key}" entry {k}, {_short(entry)}'
            if not (isinstance(entry, list) and len(entry) == 2
                    and _is_json_whole(entry[0]) and _is_json_whole(entry[1])):
                raise ValueError(f"{where}, is not a pair [i, j] of whole numbers")
            i, j = entry
            if not (0 <= i < len(cells) and 0 <= j < len(cells)):
                raise ValueError(f'{where}, names a square that is not there: positions in "cells" run from 0 to {len(cells) - 1}')
            if i == j:
                raise ValueError(f"{where}, names the same square twice")
            a, b = cells[i], cells[j]
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
                raise ValueError(f"{where}: the squares at {list(a)} and {list(b)} do not share a side")
            out.add(frozenset((a, b)))
        return out

    adjacent = [(a, b) for a in cells for b in ((a[0] + 1, a[1]), (a[0], a[1] + 1)) if b in index]
    if "joins" in data:
        attached = pairs("joins")
    else:
        cut = pairs("slits") if "slits" in data else set()
        attached = {frozenset(pair) for pair in adjacent} - cut
    joins = [pair for pair in adjacent if frozenset(pair) in attached]
    return cells, joins, None


def _read_picture(text):
    rows, slits = [], []
    blank = 0                   # blank lines seen since the last row of the picture
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        words = line.split()
        if not words:
            blank += 1
            continue
        if words[0].startswith(";"):
            continue
        if words[0].lower() == "slit":
            if (len(words) != 4 or words[3].lower() not in ("right", "down")
                    or not all(w.isascii() and w.isdigit() for w in words[1:3])):
                raise ValueError(f"line {number}: a slit line reads 'slit ROW COL right' or 'slit ROW COL down', "
                                 f"with ROW and COL counted from 0: {line!r}")
            slits.append((int(words[1]), int(words[2]), words[3].lower()))
            continue
        if set(line) - set("#. "):
            raise ValueError(f"line {number} is not a row of the picture ('#', '.' and blanks only), "
                             f"a slit line or a comment: {line!r}")
        if rows:                # blank lines inside the picture are rows of empty places
            rows.extend([""] * blank)
        blank = 0
        rows.append(line)
    layout = {}
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch == "#":
                layout[(c, -r)] = (r, c)        # x to the right, y upwards
    if not layout:
        raise ValueError("the sheet has no squares")
    cells = sorted(layout, key=lambda cell: layout[cell])
    cut = set()
    for r, c, direction in slits:
        a = (c, -r)
        b = (c + 1, -r) if direction == "right" else (c, -r - 1)
        if a not in layout or b not in layout:
            raise ValueError(f"slit {r} {c} {direction}: there is no pair of squares there")
        cut.add(frozenset((a, b)))
    joins = []
    for (x, y) in cells:
        for d in ((x + 1, y), (x, y - 1)):
            if d in layout and frozenset(((x, y), d)) not in cut:
                joins.append(((x, y), d))
    return cells, joins, layout


def picture(result, layout):
    rows = max(r for r, _ in layout.values()) + 1
    cols = max(c for _, c in layout.values()) + 1
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    for cell, (r, c) in layout.items():
        grid[r][c] = result.sides[cell]
    return ["".join(row) for row in grid]


def describe_line(line, layout):
    if layout is None:
        kind = "vertical" if line["axis"] == "x" else "horizontal"
        along = "y" if line["axis"] == "x" else "x"
        return f"{kind} grid line at {line['axis']} = {line['line']}, from {along} = {line['from']} to {line['to']}"
    if line["axis"] == "x":     # between columns line-1 and line; rows run downwards
        top, bottom = -line["to"] + 1, -line["from"]
        return f"between columns {line['line'] - 1} and {line['line']}, rows {top} to {bottom}"
    return f"between rows {-line['line']} and {-line['line'] + 1}, columns {line['from']} to {line['to'] - 1}"


def _count(number, noun):
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


def _one_line(message):
    return " ".join(str(message).split())


def main(argv):
    """Run the program on the command-line arguments `argv` and return the exit status."""
    try:
        return _main(argv)
    except SelfCheckError as err:
        print("Internal error, no answer: the program's check of its own work failed: " + _one_line(err),
              file=sys.stderr)
    except Exception as err:    # a failure of the program must never look like an answer
        print("Internal error, no answer: " + _one_line(f"{type(err).__name__}: {err}"), file=sys.stderr)
    return 3


def _main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip() if __doc__ else USAGE.rstrip())
        return 0
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    if len(args) != 1 or (args[0].startswith("-") and args[0] != "-"):
        print(USAGE, end="", file=sys.stderr)
        return 2
    try:
        if args[0] == "-":
            text = sys.stdin.read()
        else:
            with open(args[0], encoding="utf-8") as handle:
                text = handle.read()
        cells, joins, layout = read_sheet(text)
    except (OSError, ValueError) as err:
        print("Cannot read the sheet: " + _one_line(err), file=sys.stderr)
        return 2
    result = decide(cells, joins)
    if as_json:
        print(json.dumps({
            "applicable": result.applicable, "reason": result.reason, "folds": result.folds,
            "squares": result.squares, "cuts_available": result.cuts_available,
            "sets_tried": result.sets_tried, "fold_lines": result.fold_lines,
            "sides": [[list(c), s] for c, s in sorted(result.sides.items())],
        }))
    elif not result.applicable:
        print(f"Not a sheet without holes: {result.reason}.")
        print("The theorem says nothing about this input.")
    elif result.folds:
        print(f"FOLDS ONTO THE CUBE: yes ({_count(result.squares, 'square')})")
        print(f"Corner folds (90 degrees) along {_count(len(result.fold_lines), 'line')}; every other attached side is a flat fold (180 degrees):")
        for line in result.fold_lines:
            print("  " + describe_line(line, layout))
        if layout is not None:
            print("Side of the cube for each square (D down, U up, F front, B back, L left, R right):")
            for row in picture(result, layout):
                print("  " + row)
        print("This assignment was rebuilt corner by corner and checked: attached squares stay attached and all six sides are covered.")
        print("That it can be carried out with real paper is Theorem A of the manuscript, a claimed result.")
    else:
        print(f"FOLDS ONTO THE CUBE: no ({_count(result.squares, 'square')}, {_count(result.cuts_available, 'possible fold line')})")
        print("No set of up to seven fold lines covers all six sides.")
        print("That this rules out every folding is Proposition C3 of the manuscript, a claimed result.")
    return 2 if not result.applicable else (0 if result.folds else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
