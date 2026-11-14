#!/usr/bin/env python3
"""Standalone exact check of Section 6; Python standard library only.

The complete map search starts from all 48 affine cube-face frames and
uses only equality of the two retained-edge endpoint images.  No original
repository module, precomputed map inventory, solver, or network is used.
"""

import argparse
from collections import Counter, defaultdict, deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys


class VerificationError(ValueError):
    """An explicitly checked mathematical or input condition failed."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def integer(value):
    return type(value) is int


def cube_frames():
    """Generate complete BL,BR,TR,TL frames without an external state table."""
    frames = set()
    for origin in range(8):
        for right_axis in range(3):
            for up_axis in range(3):
                if right_axis == up_axis:
                    continue
                # Toggling an axis moves to the other end of its unit edge.
                right = origin ^ (1 << right_axis)
                up = origin ^ (1 << up_axis)
                opposite = origin ^ (1 << right_axis) ^ (1 << up_axis)
                frames.add((origin, right, opposite, up))
    require(len(frames) == 48, "Cube-frame generation did not give 48 frames")
    return tuple(sorted(frames))


def source_cells():
    left = {(x, y) for x in range(2) for y in range(4)}
    right = {(x, y) for x in range(1, 5) for y in range(3, 5)}
    require(left & right == {(1, 3)}, "Lobes do not have the stated overlap")
    return tuple(sorted(left | right))


def source_joins(cells):
    index = {cell: i for i, cell in enumerate(cells)}
    joins = []
    for i, (x, y) in enumerate(cells):
        for dx, dy, port in ((1, 0, 1), (0, 1, 2)):
            neighbor = (x + dx, y + dy)
            if neighbor in index:
                joins.append((i, port, index[neighbor], (port + 2) % 4))
    return tuple(joins)


def compatible(first, port, second, other_port):
    return (first[port] == second[(other_port + 1) % 4]
            and first[(port + 1) % 4] == second[other_port])


def all_maps(frames, cells, joins):
    """Exhaustive arc consistency plus branching; no coverage pruning."""
    allowed = {
        (port, si): frozenset(
            sj for sj, second in enumerate(frames)
            if compatible(first, port, second, (port + 2) % 4)
        )
        for port in range(4) for si, first in enumerate(frames)
    }
    require(all(len(values) == 2 for values in allowed.values()),
            "A cube-edge frame must have exactly two neighboring frames")
    neighbors = defaultdict(list)
    arcs = []
    for i, p, j, q in joins:
        neighbors[i].append((j, q))
        neighbors[j].append((i, p))
        arcs.extend(((i, j, p), (j, i, q)))

    def propagate(domains):
        pending = deque(arcs)
        while pending:
            i, j, port = pending.popleft()
            revised = {s for s in domains[i] if allowed[port, s] & domains[j]}
            if not revised:
                return False
            if revised != domains[i]:
                domains[i] = revised
                for k, port_from_k in neighbors[i]:
                    pending.append((k, i, port_from_k))
        return True

    root = frames.index((0, 1, 3, 2))
    initial = [set(range(len(frames))) for _ in cells]
    initial[0] = {root}
    solutions = []
    search_nodes = 0

    def visit(domains):
        nonlocal search_nodes
        search_nodes += 1
        if not propagate(domains):
            return
        choices = [i for i, domain in enumerate(domains) if len(domain) > 1]
        if not choices:
            mapping = tuple(frames[next(iter(domain))] for domain in domains)
            require(all(compatible(mapping[i], p, mapping[j], q)
                        for i, p, j, q in joins), "Search emitted an invalid map")
            solutions.append(mapping)
            return
        chosen = min(choices, key=lambda i: (len(domains[i]), i))
        for state in sorted(domains[chosen]):
            child = [set(domain) for domain in domains]
            child[chosen] = {state}
            visit(child)

    visit(initial)
    require(len(solutions) == len(set(solutions)), "Search duplicated a map")
    return tuple(sorted(solutions)), search_nodes


def face(frame):
    return tuple(sorted(frame))


def read_witness(path, cells, frames):
    data = json.loads(path.read_text(encoding="utf-8"))
    require(type(data) is dict, "Witness must be a JSON object")
    require(type(data.get("cells")) is list, "Missing cells")
    require(all(type(row) is list and len(row) == 2
                and all(integer(x) for x in row) for row in data["cells"]),
            "Cells must be integer pairs")
    require(tuple(map(tuple, data["cells"])) == cells,
            "Witness cells differ from the stated 15-cell source")
    raw_frames = data.get("frames")
    require(type(raw_frames) is list and len(raw_frames) == len(cells),
            "One complete frame is required per cell")
    require(all(type(row) is list and len(row) == 4
                and all(integer(x) for x in row) for row in raw_frames),
            "Frames must be four integer cube vertices")
    mapping = tuple(map(tuple, raw_frames))
    require(all(row in frames for row in mapping), "Invalid affine cube frame")
    ranks = data.get("ranks")
    require(type(ranks) is list and len(ranks) == len(cells)
            and all(integer(x) for x in ranks), "Ranks must be one integer per cell")
    for target in set(map(face, mapping)):
        values = sorted(ranks[i] for i, row in enumerate(mapping) if face(row) == target)
        require(values == list(range(len(values))), "Ranks are not dense and strict")
    stored_checks = data.get("edge_checks")
    require(type(stored_checks) is list, "Missing target-edge checks")
    for check in stored_checks:
        require(type(check) is dict and set(check) == {"edge", "joins", "word"},
                "Invalid target-edge check fields")
        edge, pairs = check["edge"], check["joins"]
        require(type(edge) is list and len(edge) == 2 and all(integer(x) for x in edge),
                "Target edges must be integer vertex pairs")
        require(type(pairs) is list and all(type(pair) is list and len(pair) == 2
                    and all(integer(x) for x in pair) for pair in pairs),
                "Connector row pairs must contain integers")
        require(type(check["word"]) is str, "An endpoint word must be a string")
    return data, mapping, ranks


def edge_order_checks(mapping, ranks, joins):
    by_edge = defaultdict(list)
    for i, p, j, q in joins:
        require(compatible(mapping[i], p, mapping[j], q),
                "Witness disagrees on retained-edge endpoints")
        edge = tuple(sorted((mapping[i][p], mapping[i][(p + 1) % 4])))
        by_edge[edge].append((i, j))
    checks = []
    for edge, raw_pairs in sorted(by_edge.items()):
        pairs = sorted(raw_pairs)
        incident_faces = sorted({face(mapping[i]) for pair in pairs for i in pair})
        require(1 <= len(incident_faces) <= 2, "Too many incident cube faces")
        occurrences = []
        used_cells = set()
        for pair_id, pair in enumerate(pairs):
            for i in pair:
                require(i not in used_cells, "Two connectors reuse a cell at one cube edge")
                used_cells.add(i)
                side = incident_faces.index(face(mapping[i]))
                key = (side, ranks[i] if side == 0 else -ranks[i])
                occurrences.append((key, chr(65 + pair_id)))
        word = "".join(label for _, label in sorted(occurrences))
        positions = {label: [i for i, value in enumerate(word) if value == label]
                     for label in set(word)}
        require(all(len(values) == 2 for values in positions.values()),
                "Every connector must have exactly two endpoints")
        for left, right in combinations(sorted(positions), 2):
            start, finish = positions[left]
            inside = sum(start < pos < finish for pos in positions[right])
            require(inside != 1, "Alternating connector endpoints at edge " + str(edge))
        checks.append({"edge": list(edge), "joins": [list(pair) for pair in pairs], "word": word})
    return checks


def monochrome_components(mapping, joins):
    graph = [set() for _ in mapping]
    bends = 0
    for i, _, j, _ in joins:
        if face(mapping[i]) == face(mapping[j]):
            graph[i].add(j)
            graph[j].add(i)
        else:
            bends += 1
    remaining = set(range(len(mapping)))
    components = []
    while remaining:
        first = min(remaining)
        reached = {first}
        pending = [first]
        for i in pending:
            new = graph[i] - reached
            reached.update(new)
            pending.extend(sorted(new))
        remaining -= reached
        components.append(sorted(reached))
    return components, bends


def verify(path):
    frames = cube_frames()
    cells = source_cells()
    joins = source_joins(cells)
    require(len(cells) == 15 and len(joins) == 20, "Incorrect source size/incidence")
    data, mapping, ranks = read_witness(path, cells, frames)
    mappings, search_nodes = all_maps(frames, cells, joins)
    require(len(mappings) == 81, "Complete map count is not 81")
    histogram = Counter(len(set(map(face, candidate))) for candidate in mappings)
    require(dict(histogram) == {1: 1, 2: 12, 3: 29, 4: 26, 5: 12, 6: 1},
            "Unexpected complete-map face-count histogram")
    surjective = [candidate for candidate in mappings if len(set(map(face, candidate))) == 6]
    require(len(surjective) == 1 and surjective[0] == mapping,
            "Witness is not the unique root-normalized six-face map")
    checks = edge_order_checks(mapping, ranks, joins)
    require(len(checks) == 11, "Expected eleven used target cube edges")
    require(data.get("edge_checks") == checks, "Stored edge words differ from reconstruction")
    components, bends = monochrome_components(mapping, joins)
    require(len(components) == 7 and bends == 12,
            "Incorrect monochrome component or 90-degree join count")
    by_face = defaultdict(list)
    for component in components:
        by_face[face(mapping[component[0]])].append(component)
    disconnected = [parts for parts in by_face.values() if len(parts) > 1]
    require(disconnected == [[[1, 5], [11, 12]]],
            "The disconnected same-face components are not the two stated dominoes")
    return {
        "status": "passed",
        "algorithm": "all 48 complete frames; endpoint constraints; exhaustive arc consistency and branching",
        "cube_frames": len(frames), "cells": len(cells), "retained_joins": len(joins),
        "normalized_complete_maps": len(mappings), "search_nodes": search_nodes,
        "face_count_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "surjective_maps": len(surjective), "used_target_edges": len(checks),
        "monochrome_components": len(components), "ninety_degree_joins": bends,
        "edge_checks": checks, "monochrome_component_rows": components,
        "witness_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Finite map/order certificate; PL realization and disk validity use manuscript M3 and D1.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--witness", type=Path,
                        default=Path(__file__).resolve().with_name("counterexample.json"))
    args = parser.parse_args()
    try:
        result = verify(args.witness)
    except (VerificationError, OSError, json.JSONDecodeError) as error:
        print("VERIFICATION FAILED: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
