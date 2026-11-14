#!/usr/bin/env python3
"""Complete abstract path/Y color domain through twelve arcs; not a geometry proof.

Face colors are 0..5, with opposite colors i^1.  Each leaf color is
exclusive. Cube symmetries reduce ordered path leaf pairs to two types
and Y leaf sets to two types; all ordered Y leg lengths are retained.
Tree-mask DP computes the least active-arc count in the full toggle
family, using the original target-edge involutions and covariance.
"""
import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()


def adjacent(a, b):
    return a != b and (a ^ 1) != b


def reflection(a, b):
    assert adjacent(a, b)
    permutation = list(range(6))
    permutation[a], permutation[b] = b, a
    permutation[a ^ 1], permutation[b ^ 1] = b ^ 1, a ^ 1
    return [sum(1 << permutation[c] for c in range(6) if mask >> c & 1)
            for mask in range(64)]


REFLECTION = {(a, b): reflection(a, b) for a in range(6)
              for b in range(6) if adjacent(a, b)}


def minimum_arcs(parents, colors):
    children = [[] for _ in colors]
    for v in range(1, len(colors)):
        children[parents[v]].append(v)
    tables = [None] * len(colors)
    for v in range(len(colors) - 1, -1, -1):
        table = {1 << colors[v]: 0}
        for w in children[v]:
            sigma = REFLECTION[colors[v], colors[w]]
            choices = {}
            for mask, cost in tables[w].items():
                choices[mask] = min(choices.get(mask, 100), cost + 1)
                moved = sigma[mask]
                choices[moved] = min(choices.get(moved, 100), cost)
            combined = {}
            for mask, cost in table.items():
                for other, child_cost in choices.items():
                    union = mask | other
                    combined[union] = min(combined.get(union, 100), cost + child_cost)
            table = combined
        tables[v] = table
    return tables[0].get(63, 100)


def direct_toggle_minimum(parents, colors):
    best = len(colors) - 1
    for bits in range(1 << (len(colors) - 1)):
        active = bits.bit_count()
        if active >= best:
            continue
        transformations = [list(range(6))]
        covered = 1 << colors[0]
        for v in range(1, len(colors)):
            p = parents[v]
            old = transformations[p]
            if bits >> (v - 1) & 1:
                new = old
            else:
                sigma = REFLECTION[colors[p], colors[v]]
                new = [old[sigma[1 << c].bit_length() - 1] for c in range(6)]
            transformations.append(new)
            covered |= 1 << new[colors[v]]
        if covered == 63:
            best = active
    return best


def colorings(parents, fixed):
    n = len(parents)
    allowed = [c for c in range(6) if c not in fixed.values()]
    colors = [-1] * n

    def visit(v, mask):
        if v == n:
            if mask == 63:
                yield colors[:]
            return
        for c in ([fixed[v]] if v in fixed else allowed):
            if v and not adjacent(colors[parents[v]], c):
                continue
            colors[v] = c
            yield from visit(v + 1, mask | (1 << c))
    yield from visit(0, 0)


def templates(arcs):
    parents = [-1] + list(range(arcs))
    for leaf_pair in [(0, 1), (0, 2)]:
        yield 'path', parents, {0: leaf_pair[0], arcs: leaf_pair[1]}, None
    for a in range(1, arcs - 1):
        for b in range(1, arcs - a):
            lengths = [a, b, arcs - a - b]
            parents = [-1]
            leaves = []
            for length in lengths:
                previous = 0
                for _ in range(length):
                    parents.append(previous)
                    previous = len(parents) - 1
                leaves.append(previous)
            for leaf_set in [(0, 1, 2), (0, 2, 4)]:
                yield 'Y', parents, dict(zip(leaves, leaf_set)), lengths


def run(max_arcs):
    started = time.monotonic()
    counts = Counter()
    minima = Counter()
    survivors = []
    direct_checks = 0
    for arcs in range(5, max_arcs + 1):
        for kind, parents, fixed, lengths in templates(arcs):
            for colors in colorings(parents, fixed):
                key = f'{kind}:{arcs}'
                counts[key] += 1
                minimum = minimum_arcs(parents, colors)
                minima[f'{key}:minimum={minimum}'] += 1
                # An explicit full-family implementation checks all small maps
                # and every globally minimal survivor, not the same recurrence.
                if arcs <= 7 or minimum == arcs:
                    assert direct_toggle_minimum(parents, colors) == minimum
                    direct_checks += 1
                if minimum == arcs:
                    multiplicities = [colors.count(c) for c in range(6)]
                    survivors.append(dict(kind=kind, arcs=arcs, parents=parents,
                        colors=colors, leg_lengths=lengths,
                        multiplicities=multiplicities))
        print(json.dumps({'arcs_completed': arcs, 'patterns_so_far': sum(counts.values()),
                          'minimal_survivors_so_far': len(survivors)}), flush=True)
    return dict(status='complete_abstract_path_and_Y_toggle_minimum_domain',
        scope='Abstract necessary disk region-tree domain; no physical realization or layer-order claim',
        face_opposites='i xor 1', maximum_arcs=max_arcs,
        exclusive_leaf_color_orbits={'path': [[0, 1], [0, 2]], 'Y': [[0, 1, 2], [0, 2, 4]]},
        all_ordered_positive_Y_leg_lengths_included=True,
        counts=dict(sorted(counts.items())), minimum_histogram=dict(sorted(minima.items())),
        direct_toggle_crosschecks=direct_checks,
        minimal_survivors=survivors,
        survivor_count=len(survivors),
        survivor_arc_histogram=dict(sorted(Counter(x['arcs'] for x in survivors).items())),
        survivor_multiplicity_histogram=dict(sorted(Counter(
            ','.join(map(str, sorted(x['multiplicities'], reverse=True))) for x in survivors).items())),
        bindings={str(SELF.relative_to(ROOT)): hashlib.sha256(SELF.read_bytes()).hexdigest()},
        seconds=round(time.monotonic() - started, 6))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-arcs', type=int, default=12)
    parser.add_argument('--output', default='results/minimal-colored-disk-region-trees-primary-v1.json')
    args = parser.parse_args()
    out = ROOT / args.output
    assert not out.exists(), 'Refusing to overwrite a frozen result'
    result = run(args.max_arcs)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'survivor_count', 'survivor_arc_histogram',
                                          'survivor_multiplicity_histogram', 'seconds')}))
