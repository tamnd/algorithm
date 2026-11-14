# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/static-test-compaction/. The authors are listed in prov/DV4CEE.jsonl.
"""Static test compaction of a finished test set.

static_compact merges compatible test cubes, fills the remaining X positions,
and then drops vectors by reverse-order fault simulation. greedy_cover is the
set covering alternative on the detection matrix, and minimum_test_set is the
exact minimum by enumeration, for small inputs only. set_cover_circuit builds
the circuit of the NP-hardness reduction from set cover.

A cube is a tuple over {0, 1, X}. A test cube of a fault is a cube whose every
completion detects the fault.
"""

from __future__ import annotations

from itertools import combinations
from typing import Optional, Sequence

from td2net import X, Circuit, Fault, completions


def compatible(u: Sequence[int], t: Sequence[int]) -> bool:
    """True if no position has 0 in one cube and 1 in the other."""
    return all(a == X or b == X or a == b for a, b in zip(u, t))


def intersect(u: Sequence[int], t: Sequence[int]) -> tuple[int, ...]:
    """The cube of the vectors in both cubes (the cubes must be compatible)."""
    return tuple(b if a == X else a for a, b in zip(u, t))


def merge_cubes(cubes: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
    """First-fit merging: each cube joins the first compatible merged cube."""
    merged: list[tuple[int, ...]] = []  # @line L1
    for t in cubes:  # @line L2
        for i, u in enumerate(merged):
            if compatible(u, t):  # @line L3
                merged[i] = intersect(u, t)
                break
        else:
            merged.append(tuple(t))  # @line L4
    return merged


def fill(cube: Sequence[int], value: int = 0) -> tuple[int, ...]:
    """Replace every X by a fixed value."""
    return tuple(value if v == X else v for v in cube)


def reverse_order_fault_simulation(
    c: Circuit, vectors: Sequence[Sequence[int]], faults: Sequence[Fault]
) -> list[tuple[int, ...]]:
    """Keep a vector only if, simulated last first, it detects a fault not yet detected.

    Returns the kept vectors in their original order.
    """
    remaining = set(faults)  # @line L6
    kept: list[tuple[int, ...]] = []
    for v in reversed(vectors):  # @line L7
        hit = {f for f in remaining if c.detects(v, f)}  # @line L8
        if hit:  # @line L9
            kept.append(tuple(v))
            remaining -= hit
    kept.reverse()
    return kept  # @line L10


def static_compact(c: Circuit, cubes: Sequence[Sequence[int]], faults: Sequence[Fault], value: int = 0) -> list[tuple[int, ...]]:
    """Merge compatible cubes, fill the X positions, then reverse-order fault simulation."""
    merged = merge_cubes(cubes)
    vectors = [fill(u, value) for u in merged]  # @line L5
    return reverse_order_fault_simulation(c, vectors, faults)


def detection_masks(c: Circuit, vectors: Sequence[Sequence[int]], faults: Sequence[Fault]) -> list[int]:
    """One bit mask per vector: bit i is set when the vector detects faults[i]."""
    masks = []
    for v in vectors:
        m = 0
        for i, f in enumerate(faults):
            if c.detects(v, f):
                m |= 1 << i
        masks.append(m)
    return masks


def greedy_cover(c: Circuit, vectors: Sequence[Sequence[int]], faults: Sequence[Fault]) -> list[tuple[int, ...]]:
    """Greedy set cover on the detection matrix: take the vector that detects the most new faults."""
    masks = detection_masks(c, vectors, faults)
    goal = 0
    for m in masks:
        goal |= m
    covered = 0
    chosen: list[int] = []
    while covered != goal:
        best = max(range(len(vectors)), key=lambda i: (bin(masks[i] & ~covered).count("1"), -i))
        chosen.append(best)
        covered |= masks[best]
    return [tuple(vectors[i]) for i in sorted(chosen)]


def minimum_test_set(c: Circuit, vectors: Sequence[Sequence[int]], faults: Sequence[Fault]) -> list[tuple[int, ...]]:
    """Exact by enumeration: a smallest subset of the vectors that detects every fault any of them detects."""
    masks = detection_masks(c, vectors, faults)
    goal = 0
    for m in masks:
        goal |= m
    useful = [i for i, m in enumerate(masks) if m]
    for size in range(len(useful) + 1):
        for subset in combinations(useful, size):
            got = 0
            for i in subset:
                got |= masks[i]
            if got == goal:
                return [tuple(vectors[i]) for i in subset]
    raise AssertionError("unreachable")


def relax_to_cube(c: Circuit, fault: Fault, vector: Sequence[int]) -> Optional[tuple[int, ...]]:
    """Brute force: turn positions of a detecting vector into X while every completion still detects."""
    if not c.detects(vector, fault):
        return None
    cube = list(vector)
    for i in range(len(cube)):
        old = cube[i]
        cube[i] = X
        if not all(c.detects(w, fault) for w in completions(cube)):
            cube[i] = old
    return tuple(cube)


def set_cover_circuit(m: int, sets: Sequence[set[int]]) -> tuple[Circuit, list[Fault]]:
    """The reduction from set cover with m >= 2 sets over the elements 0 .. n-1.

    Inputs x0 .. x_{m-1}; y_e is the OR of the x_i with e in S_i; a = 1 when at
    most one x_i is 1; z_e = y_e AND a. The target faults are y_e stuck-at 0, so
    a vector detects y_e/0 exactly when it has one 1, at an x_i with e in S_i.
    """
    elements = sorted(set().union(*sets))
    inputs = [f"x{i}" for i in range(m)]
    gates: list[tuple[str, str, list[str]]] = []
    pair_names = []
    for i in range(m):
        for j in range(i + 1, m):
            gates.append((f"n{i}_{j}", "NAND", [f"x{i}", f"x{j}"]))
            pair_names.append(f"n{i}_{j}")
    gates.append(("a", "AND" if len(pair_names) > 1 else "BUF", pair_names))
    for e in elements:
        members = [f"x{i}" for i in range(m) if e in sets[i]]
        gates.append((f"y{e}", "OR" if len(members) > 1 else "BUF", members))
        gates.append((f"z{e}", "AND", [f"y{e}", "a"]))
    circuit = Circuit(inputs, gates, [f"z{e}" for e in elements])
    return circuit, [(circuit.line(f"y{e}"), 0) for e in elements]
