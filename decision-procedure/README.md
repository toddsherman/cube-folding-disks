# A program that decides whether a sheet folds onto the cube

`decide.py` reads a sheet of unit squares without holes and says whether it can be folded so as to cover all six sides of a unit cube. It follows the procedure of Corollary A2 of the manuscript.

**The proof does not depend on this program.** It is here so that anyone can try the claimed result on a sheet of their own. Like the rest of this repository it was written by AI systems and has not been reviewed by a human with expertise in this field. If you find a sheet on which it gives a wrong answer, please open an issue.

## Use

It is written for Python 3.8 or newer and needs nothing else. It has been run with Python 3.9, 3.14 and 3.15.

```sh
python3 decide.py examples/cross.txt
```

```
FOLDS ONTO THE CUBE: yes (6 squares)
Corner folds (90 degrees) along 5 lines; every other attached side is a flat fold (180 degrees):
  between rows 0 and 1, columns 1 to 1
  between rows 1 and 2, columns 1 to 1
  between columns 0 and 1, rows 1 to 1
  between columns 1 and 2, rows 1 to 1
  between rows 2 and 3, columns 1 to 1
Side of the cube for each square (D down, U up, F front, B back, L left, R right):
  .D.
  LFR
  .U.
  .B.
This assignment was rebuilt corner by corner and checked: attached squares stay attached and all six sides are covered.
That it can be carried out with real paper is Theorem A of the manuscript, a claimed result.
```

Add `--json` for machine-readable output, or give `-` in place of the file name to read from standard input. `python3 decide.py --help` prints a summary.

The exit status says which of four things happened:

| Exit status | Meaning |
|---:|---|
| 0 | The sheet folds onto the cube. |
| 1 | It does not. |
| 2 | No answer, because of the input: it cannot be read, or it is not a sheet without holes, or the command line is wrong. |
| 3 | No answer, because the program itself failed or its check of a "yes" failed. A message goes to standard error. This should not happen; if it does, please open an issue. |

## Describing a sheet

Draw it, one text line per row: `#` is a square, `.` or a blank is empty. Squares that share a side are attached unless you say otherwise with a slit line:

```
; a 3 x 3 block with three slits
###
###
###
slit 0 0 right
slit 0 1 down
slit 1 1 right
```

`slit ROW COL right` cuts the side between the square at that row and column and the square to its right; `slit ROW COL down` cuts the side between it and the square below. Rows and columns are counted from 0 at the top left. Lines that begin with `;` are comments. They are not rows.

A blank line between two rows of the picture is a row of empty places, and it is counted when the rows are numbered. Blank lines before the first row of the picture and after the last are ignored.

Squares that touch only at a corner are not attached there.

The folder `examples/` has five sheets: a cube net, a 2 × 3 rectangle, the sheet of Section 6 of the manuscript, a 3 × 3 block with slits, and a ring with a hole.

### A sheet as JSON

The input may also be JSON. This is a 2 × 3 block with one slit:

```json
{"cells": [[0, 0], [1, 0], [2, 0], [0, -1], [1, -1], [2, -1]], "slits": [[0, 1]]}
```

`"cells"` lists the squares. Each is a pair `[x, y]` of whole numbers; x grows to the right and y grows upwards. Squares that share a side are attached, except the pairs listed in `"slits"`. A pair `[i, j]` names two squares by their places in `"cells"`, counted from 0. In place of `"slits"` you may give `"joins"`, and then exactly the pairs listed there are attached.

The program refuses the input, with a message and exit status 2, if a position or a place is not a whole number, if a square is listed twice, if a pair does not name two different squares that share a side, if a place is below 0 or past the end of the list, if both `"slits"` and `"joins"` are given, if there is any other key, or if there are no squares.

## The `--json` output

The output is one line of JSON with these keys:

| Key | Meaning |
|---|---|
| `applicable` | `true` if the input is a sheet without holes |
| `reason` | if it is not, the reason; otherwise empty |
| `folds` | `true` or `false`; `null` if not applicable |
| `squares` | the number of squares |
| `cuts_available` | the number of possible fold lines |
| `sets_tried` | how many times the search added a line to the set it was building |
| `fold_lines` | for a "yes", the fold lines; otherwise empty |
| `sides` | for a "yes", each square with the letter of the side of the cube it lands on; otherwise empty |

A square is written `[x, y]`. It covers the plane from x to x + 1 and from y to y + 1, and y grows upwards. If the sheet was given as a picture, the square in row r and column c is `[c, -r]`. If it was given as JSON, `[x, y]` is the position given in `"cells"`.

A fold line has an `axis`, a `line`, a `from` and a `to`:

- With `"axis": "x"` it lies on the vertical grid line x = `line`, between the squares at x = `line` − 1 and the squares at x = `line`. It runs from y = `from` to y = `to`.
- With `"axis": "y"` it lies on the horizontal grid line y = `line`, between the squares at y = `line` − 1 and the squares at y = `line`. It runs from x = `from` to x = `to`.

For `examples/cross.txt` the first fold line is `{"axis": "y", "line": 0, "from": 1, "to": 2}`. It lies on the grid line y = 0, between the squares `[1, -1]` and `[1, 0]`, which are rows 1 and 0 of column 1. The plain output calls it "between rows 0 and 1, columns 1 to 1".

## What the answers mean

- **Yes.** The program has found a way to put every square on a side of the cube, using corner folds along at most seven straight lines and flat folds everywhere else, so that attached squares stay attached and all six sides are covered. It rebuilds that assignment corner by corner and checks it, so this part of a "yes" can be trusted without the theory. If the check fails, the program gives no answer and exits with status 3. That the assignment can be carried out with real paper, with the layers in a workable order, is Theorem A of the manuscript. The program does not work out the layers.

  The fold lines it reports are the first set it finds that works. They are not always the fewest possible. For this sheet it reports seven lines, and five are enough:

  ```
  ###
  .#.
  ###
  #..
  ```

  In Python, `decide(cells, joins, max_lines=5)` allows at most five lines, and for this sheet it finds five.

- **No.** No choice of up to seven lines works. That no folding exists at all then follows from Proposition C3 of the manuscript, which rests on the computer-checked step.
- **Not a sheet without holes.** The sheet is in more than one piece, or it has a hole. The theorem says nothing about such sheets, and the program stops.

  The sheet is in one piece if every square can be reached from every other by going from a square to a square attached to it. A hole is something that is not paper and has paper all the way round it: a ring of squares, each attached to the next, that closes up around one or more empty places, or around a slit that does not reach the edge of the sheet. An empty place with squares on all four sides is not always a hole. In

  ```
  ##.
  #.#
  ###
  ```

  the top middle square and the right middle square touch only at a corner, so they are not attached and the ring is open there. This sheet is a strip of seven squares bent round. It has no hole, and the program answers it: no.

- **Cannot read the sheet.** The input is not a picture or JSON as described above. The message says what is wrong.

So a "yes" or a "no" from this program is only as reliable as the manuscript, which is a claimed result.

## Speed

The times below were measured with Python 3.15 on an Apple M4. They are the time spent deciding, without the time Python takes to start.

Each of the five examples is decided in less than a thousandth of a second. The whole command took 0.02 seconds.

What costs time is the number of possible fold lines that do not cross one another, because every set of up to seven of them may have to be tried. A "no" on such a sheet can take long:

| Sheet | Squares | Possible fold lines | Answer | Time |
|---|---:|---:|---|---:|
| Strip of 20 squares in a row | 20 | 19 | no | 0.03 s |
| Strip of 40 | 40 | 39 | no | 2.4 s |
| Strip of 60 | 60 | 59 | no | 29 s |
| Block of 2 × 60, no slits | 120 | 60 | no | 29 s |
| Block of 20 × 20, no slits | 400 | 38 | no | 0.08 s |
| Block of 40 × 40, no slits | 1,600 | 78 | no | 5.1 s |

In a strip no two lines cross. In a block with no slits every line across crosses every line down, so a set can only hold lines that run the same way. In these measurements a block of m × n squares cost about as much as a strip of m squares and a strip of n squares together: the 40 × 40 block took 5.1 seconds and two strips of 40 take 4.8, the 20 × 20 block took 0.08 seconds and two strips of 20 take 0.07, and the 2 × 60 block took about as long as the strip of 60.

With Python 3.9 on the same computer the strip of 60 took 54 seconds.

Small sheets are decided at once: each of the 8,288 sheets in the table of the next section, which have up to 14 squares, took less than 0.002 seconds. On a larger sheet the time for a "yes" can depend on which square comes first, because the search starts there. In a picture that is the first square in reading order, top row first and left to right. In JSON it is the first entry of `"cells"`. For example, attach a strip of 80 squares to the first square of the sheet of Section 6. The new sheet has 95 squares and folds. Drawn with the strip pointing up, it was decided in 0.005 seconds:

```sh
python3 -c "print('.#...\n' * 80 + '.####\n#####\n##...\n##...\n##...')" | python3 decide.py -
```

The same sheet turned over, so that the strip points to the left, took 13 seconds:

```sh
python3 -c "print('.' * 81 + '####\n' + '#' * 85 + '\n' + ('.' * 80 + '##...\n') * 3)" | python3 decide.py -
```

## How it was tested

Run the tests yourself with `python3 test_decide.py`. On an Apple M4 the full run took 12 seconds with Python 3.15 and 21 seconds with Python 3.9. `python3 test_decide.py --quick` is a shorter run, which took 3 and 7 seconds.

The main test compares the program with a brute-force search that knows nothing about fold lines or the manuscript's theory: it tries every way of folding each attached side by 180 or by 90 degrees and asks whether any of them covers all six sides. The two must agree on every sheet. The full run covers:

| Sheets | Number tested | Fold | Do not fold |
|---|---:|---:|---:|
| Every sheet with all sides attached, up to 10 squares | 6,454 | 5,655 | 799 |
| Every pattern of slits, up to 8 squares | 1,236 | 689 | 547 |
| Random sheets with 9 to 14 squares and random slits | 598 | 576 | 22 |

The full run also makes these checks:

- **Position.** Every arrangement of up to 8 squares with all sides attached (533 of them, one of which has a hole) and 8 fixed examples are run again in all 8 rotations and reflections. In each of these they are run a second time, moved to another place and with the last square moved to the front of the list. The search starts from the first square in the list. That is 8,656 runs. No answer changed.
- **Reading.** 66 checks of how a sheet is read: blank lines, slits and comments in a picture, the JSON form, and each kind of input that must be refused.
- **Command line and printed output.** 82 checks in which the program is started as a separate command. They cover exit statuses 0, 1, 2 and 3, that the `--json` output can be parsed and agrees with the answer, that `-` reads standard input, and that `python3 -O decide.py` gives the same output. For sheets that fold, the printed picture is read back: it must have one letter for each square and all six letters, and the printed fold lines must be exactly the attached sides across which the letter changes. Exit status 3 is produced by starting copies of the program that have been changed on purpose: in one the check of a "yes" has to fail, in the other the program breaks down.

**What the tests do not show.** The program stops at seven fold lines, as the manuscript allows. The tests cannot tell this from stopping at six. When the limit is lowered to six, none of the 6,920 sheets that fold in the table above changes its answer, so no sheet in the tests needs a seventh line. When the limit is lowered to five, 51 of them change to "no", so the sixth line is needed. The test run prints these two numbers as information.

Outside this test file, after the last change to the program, it was also compared with:

- a second brute-force search, written separately from the one in the test file, on every sheet with all sides attached up to 12 squares (86,679 sheets without holes, of which 84,262 fold) and on every pattern of slits up to 10 squares (35,233 sheets without holes, of which 31,125 fold). The two agreed on every sheet. None of these sheets needs a seventh line either;
- results recorded earlier in the project: it agrees on all 11,501 sheets without holes with up to 10 squares (up to 9 with slits), in every position in which they were recorded;
- two other implementations of the same procedure, on 400 random sheets with 10 to 22 squares and at most 17 possible fold lines. All three agreed.

These tests show that the program finds a six-sided assignment exactly when one exists, on small sheets. They do not show that such an assignment can always be folded with real paper. That is what the manuscript claims to prove.

## How it follows the manuscript

1. The sheet must be in one piece, and must satisfy N − R + n = 1, where N, R and n count its squares, its attached sides, and the corner points at which four squares meet with all four sides between them attached.
2. A *cut* is a maximal straight run of attached sides whose interior corner points are of that kind. Two cuts cross when they share such a point.
3. With every attached side folded flat, all squares lie on one side of the cube and each cut lies along one edge of that side.
4. For a set of cuts no two of which cross, the sheet is folded by 90 degrees along those cuts instead. The squares beyond a cut, seen from a fixed root square, are moved by the reflection of the cube that fixes the cut's edge; nested cuts compose, outermost first.
5. The sheet folds onto the cube exactly when some such set of five, six or seven cuts covers all six sides.

The search does not look at every such set. It tries the cuts from the outermost inwards, skips a partial choice as soon as it can no longer reach six sides within seven cuts, and stops at the first set that works. This does not change the answer.

## Files

| File | What it is |
|---|---|
| `decide.py` | The program |
| `test_decide.py` | Its tests, with the brute-force search |
| `examples/` | Five sheets to try |
