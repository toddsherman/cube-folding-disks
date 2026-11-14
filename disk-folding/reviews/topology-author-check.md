# Topology author check

Date: 2026-11-05. Scope: newly authored Sections 1 and 6 only. This is an author-side proof audit, not an independent referee report and not a novelty certification.

Reviewed final section hashes:

- `sections/01-model-and-realization.md`: `96e12108821728676680526f9b79c5b4db29496e0e46094547fbfbd3c83d59ae`
- `sections/06-counterexample.md`: `7a9875f04aaf5ce97183972db864f380f76896c976d3c00884f11bdc94abe8f8`

## Primary-source fidelity

Checked against the published `research/jocg-2025.txt`, corresponding to Aichholzer–Lehner–Lindorfer, JoCG 16(1), 601–634 (2025), DOI 10.20382/jocg.v16i1a17. Definitions 3.1–3.3 are on printed pages 604–605; Theorem 3.4 and its proof are on pages 605–606. The manuscript uses pointwise epsilon correspondence, ambient-isotopy validity, and surjectivity of the blueprint. It does not replace this model with rigid-hinge motion or impose an outside-cube condition.

## Adversarial checks and resolutions

1. **Vertex contacts:** the domain is the retained-edge quotient, with no extra identifications of coincident drawn corners. Actual source vertex links must be intervals/circles. The cap argument would not apply to arbitrary singular square complexes; these are excluded explicitly.
2. **Possible intersecting edge ribbons:** Lemma M1 gives explicit straight/U arcs and checks all four pair types. The mixed-pair separation uses the strict bound A>N², rather than an unexplained drawing assumption.
3. **Nested caps:** coning all links to a common center is invalid. Lemma M2 uses laminar Jordan regions and strict graph-depth inequalities. Arc neighborhoods avoid all circles and are placed shallower than every enclosing cap.
4. **Missing simple-link premise:** M3 derives disjoint simple sphere links from the embedded exterior surface and actual source fan incidence before applying M2. Euler characteristic alone is not substituted for this premise.
5. **Extra source material:** inserted edge ribbons are parametrized by shrinking source collars and a transverse PL reparametrization, so no extra rectangle is added to the domain.
6. **Hausdorff versus pointwise proximity:** M3 bounds the error separately on face interiors, edge collars, and source vertex neighborhoods. Source fan images and blueprint fans lie within less than 5 rho of each other, with rho<epsilon/20.
7. **Unproved uniqueness of folded-state type:** none is asserted. Existence of one embedded disk is enough for D1. Holed sources receive no validity conclusion from local orders alone.
8. **Finite counterexample wording:** Section 6 uses monochrome retained-edge components, not inverse images of closed faces. Literal closed-face preimages can contain lower-dimensional pieces of other squares, so the earlier terminology was avoided.
9. **Counterexample completeness:** the 2x2 frame calculation proves nine maps per 2x4 lobe; their single-square overlap gives 81. Six-face coverage forces both longitudinal sequences to be 111. No census cutoff or unproved minimality claim enters this argument.
10. **Positive counterexample witness:** Section 6 contains all fifteen complete frames/ranks and all twenty retained joins grouped into eleven target-edge endpoint words. None of those words has alternating matched endpoints. This makes the layer witness inspectable without trusting an opaque result file.

## Checks already replayed during the preceding audit

Two independent complete-map enumerators regenerated exactly the same 81 maps; `verify_certificate` accepted the frozen counterexample; all fourteen semantic corruption controls rejected; the saved layer witness passed `independent.cyclic_noncrossing`. The read-only replay command is preserved below; this is a legacy-certificate crosscheck, not a dependency of the analytic proof in Section 6.

No original research notes, source modules, or result artifacts were edited. The local-realization statement is an explicit analytic existence proof, not a claim that finite fixture tests establish a universal theorem. External novelty assessment remains separate.

## Read-only legacy-certificate replay

Run from `/Volumes/RAID4/Projects/origami`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python - <<'PYTHON'
from pathlib import Path
import json
from polycube.independent import iter_mappings, cyclic_noncrossing
from polycube.signed_frame_constraint_maps import iter_constraint_mappings
from scripts.test_connected_face_map_selection_v1 import verify_certificate, controls
c = json.loads(Path('results/connected-face-map-selection-counterexample-v1.json').read_text())['counterexample']
cells = [tuple(v) for v in c['cells']]
maps = tuple(sorted(iter_mappings(cells, surjective=False)))
fresh = tuple(sorted(iter_constraint_mappings(cells)))
assert maps == fresh
verify_certificate(c, maps)
print('maps', len(maps), 'controls', len(controls(c, maps)))
w = c['valid_disk_witness']
print('witness cyclic', cyclic_noncrossing(cells, w['mapping'], w['layers']))
PYTHON
```

Observed output:

```text
maps 81 controls 14
witness cyclic True
```

## Standalone packaging update

Section 6 now points to the bundled `examples/` verifier rather than unavailable original-repository result/script paths. Its mathematical proof and displayed witness tables are unchanged. The fresh verifier generates all 48 cube frames and enumerates all 81 normalized maps using endpoint constraints alone, then checks the unique surjective witness, all 20 joins, eleven nonalternating endpoint words, seven monochrome components, and twelve bends. It passed from `/tmp` with `-I -S`; normal and optimized outputs agree, and a CPython 3.12 run agrees with CPython 3.15.0. Four corrupted witnesses were each rejected normally and under optimization. Persistent details are in `examples/README.md`, `examples/verification.json`, and `examples/test-evidence.json`; the main supplement and its manifest were not changed.
