# Wrapping a cube with a sheet of squares

*A plain-language summary. The result described here is a claim: the proof was written and checked by AI systems, and no human mathematician has checked it yet.*

## 1. The setup

Imagine wrapping a small wooden cube in a flat piece of paper made of squares, like a connected sheet of square postage stamps. Each square is exactly the size of one side of the cube, and the cube has six sides, like a die.

There are four rules:

- **The sheet is fixed.** It may already have straight slits cut along the lines between squares, as long as it is still in one piece. You may not make new cuts, and you may not glue or tape anything.
- **Fold only on the lines between squares.** Every line where two squares are attached gets one of two folds:
  - a *corner fold* (90 degrees), which bends the paper around an edge of the cube onto the neighboring side;
  - a *flat fold* (180 degrees), which folds one square back on top of its neighbor, like closing a book, so that both lie on the same side of the cube.
- **Stacking is allowed. Passing through is not.** Squares may pile up in layers on the same side of the cube, but the paper may never pass through itself.
- **The goal is to cover all six sides.**

## 2. The question: ghost paper and real paper

Suppose someone hands you a sprawling sheet of 50 squares and asks whether it can wrap the cube. There are really two questions:

1. **The Ghost Test.** Pretend the paper is a ghost that can pass through itself. Can you fold it along the lines so that at least one square lands on each of the six sides?
2. **The Real-Paper Test.** Can you do it with real paper, with every layer tucked over or under the others, so that nothing has to pass through anything else?

A folding plan can pass the Ghost Test and still fail with real paper. For example, two folds wrapped around the same edge of the cube can be arranged so that each would have to slice through the other.

In a paper published in 2025, three mathematicians (Aichholzer, Lehner and Lindorfer) asked:

> If a sheet passes the Ghost Test, can it always be folded for real? Or is there a sheet where every ghost folding jams, so that it can never wrap the cube?

They also predicted that a computer should be able to decide whether a sheet wraps the cube without trying an exploding number of folding combinations.

## 3. The answer, for sheets without holes

This project claims to settle both points for every sheet without holes. A hole is a window cut out of the middle of the sheet, or a slit that lies entirely inside the sheet and never reaches its border. A slit that starts at the border is fine.

- **Main result.** If a sheet without holes passes the Ghost Test, it can be folded for real. One folding plan may jam, but there is always another way to fold the same sheet, with no new cuts, that covers all six sides cleanly.
- **Computer method.** A computer can decide whether a sheet without holes wraps the cube with an amount of work that grows steadily as the sheet gets bigger, instead of doubling with every added square.

## 4. Why it works, in three steps

Proving something about every possible sheet sounds hopeless, since a sheet could have a million squares. The proof shows that only the corner folds matter, and that very few are needed.

1. **At most 12 lines of corner folds.** A flat fold keeps the paper on the same side of the cube. Only a corner fold moves it to a new side. Corner folds line up: each one belongs to a straight line of corner folds that runs across the sheet from border to border. On a sheet without holes, every such line splits the sheet in two. So the lines divide the sheet into patches, and each patch ends up entirely on one side of the cube. A line can be switched from corner folds to flat folds, which merges the two patches beside it. The proof shows that after switching every line you can spare, at most 12 remain.
2. **A computer check brings 12 down to 7.** With at most 12 lines, there are few enough arrangements of patches to list them all: 87,538 cases. For each one, a computer program confirms that more lines can be switched, down to 7 or fewer, with all six sides still covered. So the whole sheet, however large, is divided into at most 8 patches: six to cover the six sides, and at most two extra.
3. **Fold up each patch and nest the stacks.** Inside a patch there are only flat folds, so the patch folds up, back and forth like a road map, into one stack on one side of the cube. Where two patches meet along an edge of the cube, one stack has to wrap around the other. Because at most two patches are extra, there are only a handful of ways the stacks can meet, and the proof goes through each one and shows how to nest them so that nothing passes through anything else. This is the longest and most delicate part of the proof.

A final part of the proof shows that a layered plan of this kind can always be carried out with real paper.

The limit of 7 lines also gives the computer method. Instead of trying every way to fold every square, the computer looks only at the straight lines that run across the sheet. It tries groups of up to 7 lines that do not cross each other and checks whether any group reaches all six sides.

## 5. Why holes are harder

The proof needs the sheet to have no holes. Picture a sheet shaped like a picture frame, with a window in the middle:

1. A line of folds across one side of the frame no longer splits it into two pieces. The step that divides the sheet into a few patches breaks down.
2. A frame has two borders: its outer rim and the rim of the window. Folded up, those two rims can end up linked like two links of a chain, even though no two squares pass through each other. Real paper cannot get from flat into that position without being cut and taped back together.

For sheets with holes, the original question is still open. Nobody knows a sheet with holes that passes the Ghost Test but cannot be folded. In this project, every one of about 39,000 sheets with holes and up to 12 squares that passed the Ghost Test did fold. But a search is not a proof. Earlier in the project, AI sessions claimed proofs for many kinds of sheets with holes. A later review found gaps in those proofs, and the claims were withdrawn.

## 6. How far to trust this

- **Who did the work.** The proof, the programs and the checks were all produced by AI systems, directed by one person. No human mathematician has checked the proof yet.
- **What has been checked.**
  - Separate AI sessions re-read the argument step by step several times. One of these checks found a false step in an early version, which was then replaced.
  - A different AI model audited the work independently. It re-ran the 87,538 cases with its own program and found no error in the proof.
  - On about 11,500 small sheets, the result agrees with software written by other researchers for the same problem, once two small bugs in that software were corrected.
  - Searches through tens of thousands of further sheets found no counterexample.
- **What those checks cannot show.** In small sheets, almost every ghost folding already works with real paper. The smallest sheet found where one jams has 14 squares. So tests on small sheets rarely reach the hard case. And every checker so far was an AI system, which may share blind spots with the systems that wrote the proof.
- **What comes next.** Review by mathematicians who work on this problem.
