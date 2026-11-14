# Folding a sheet of squares onto a cube: the case without holes

**Status: a claimed result, not yet checked by an expert.** The proof in this repository was written and checked by AI systems under the direction of one person. No human with sufficient expertise in this field of study has reviewed it. Treat it as a claim to be tested, and please report any error you find.

## What is claimed

Take a flat sheet made of unit squares (a polyomino), possibly with slits cut along the grid lines, and a cube whose sides are the size of one square. The sheet may be folded only along grid lines, by 90 or 180 degrees. Squares may stack in layers, but the paper may not pass through itself.

- **Theorem A.** A sheet without holes can be folded so that it covers all six sides of the cube if and only if it has a consistent mapping onto all six sides, that is, if and only if it could be folded that way were the paper allowed to pass through itself. This would answer, for sheets without holes, Question 4.9 of Aichholzer, Lehner and Lindorfer, *Folding polyominoes into cubes* (Journal of Computational Geometry 16(1), 2025; [arXiv:2402.14965](https://arxiv.org/abs/2402.14965)).
- **Corollary A2.** Whether a sheet without holes with N squares folds onto the cube can be decided in O(N^7) time. This would settle, for sheets without holes, Conjecture 4.10 of the same paper.

Nothing is claimed for sheets with holes. For them the question remains open.

## Where to start

| If you want | Read |
|---|---|
| An account in plain language | [plain-language-summary.md](plain-language-summary.md) |
| The manuscript (41 pages) | [disk-folding/output/pdf/disk-folding-manuscript.pdf](disk-folding/output/pdf/disk-folding-manuscript.pdf) |
| The points where a specialist's judgement would help most | [disk-folding/reviews/questions-for-a-referee.md](disk-folding/reviews/questions-for-a-referee.md) |
| To check the computer-assisted step yourself | "Checking the certificate" below |
| The history of checks and corrections | [disk-folding/README.md](disk-folding/README.md) and [disk-folding/reviews/](disk-folding/reviews/) |

## Checking the certificate

One step of the proof is checked by computer: each of 87,538 cases has an explicit witness, and a short program replays them all. It needs Python 3.10 or newer and nothing else, and runs in a few seconds.

```sh
cd disk-folding/supplement
python3 -I -S check_integrity.py
python3 -I -S verify.py --output verification-new.json
```

The first command should print `Verified SHA-256 hashes for 29 packaged files.` The second should end with a line that contains `"patterns": 87538` and `"negative_controls": 9`. What the program does and does not establish is described in [disk-folding/supplement/README.md](disk-folding/supplement/README.md).

## How this was produced, and how far to trust it

- **Who did the work.** The proof, the programs and the checks were written by AI systems: Anthropic's Fable 5.2 and Opus 5.5, Google's Carbon, and OpenAI's Astra. One person, Todd S. Sherman, directed the work. He is not a mathematician and has not verified the proof himself.
- **What has been checked.** Separate AI sessions re-read the argument step by step several times, and one such check found a false step in an early version, which was replaced. A different AI model then audited the work and re-ran the 87,538 cases with its own program. On about 11,500 small sheets the result agrees with software written by other researchers for the same problem, once two defects in that software were corrected. Searches through tens of thousands of further sheets found no counterexample.
- **What those checks cannot show.** In small sheets almost every way of folding that works for "ghost" paper already works for real paper, so tests on small sheets rarely reach the hard case. And every checker so far was an AI system, which may share blind spots with the systems that wrote the proof.
- **The record is kept.** The errors found along the way, and how they were corrected, are in [disk-folding/reviews/](disk-folding/reviews/).

## What is in this repository

- [disk-folding/](disk-folding/) is the release package: the manuscript and its sources, the certificate with its verifier, a worked example, a comparison with earlier work, and the AI review records. It is file for file the archive `disk-folding-release-2026-11-14c.zip` (SHA-256 `2b5e3ad78f2bb5edde32bb91aa9927c10e02ab3f88cc03729101f23122ad42f2`), which is attached to the release of that name. The PDF has SHA-256 `6f4478119c8919eb65a56415053b78cc07a067fec74221793eb463f870d1911a`.
- Some records in the package refer to paths that begin with `../`. Those are working records of the project and are not published here.
- The working notes of the project are not here either. They include unfinished work on sheets with holes, for which nothing is claimed.

## Comments and corrections

Please open an issue on this repository. Reports of errors are especially welcome.

## Licence

The text, the manuscript and the data are licensed under CC BY 4.0, and the program code under the MIT licence. See [LICENSE.md](LICENSE.md).

## How to cite

Todd S. Sherman. *Square-grid disks with a surjective consistent cube map fold validly onto the cube.* Manuscript, 14 November 2026. https://github.com/toddsherman/cube-folding-disks (release 2026-11-14c).
