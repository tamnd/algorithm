# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/static-test-compaction/. The authors are listed in prov/DV4CEE.jsonl.
"""Static test compaction checked against the exhaustive minimum test set.

All circuits are small enough to enumerate every input vector and every subset
of the useful vectors. Seeds are fixed.
"""

from __future__ import annotations

import random
from itertools import combinations, product

import pytest

from td2net import X, Circuit, completions, random_circuit
from static_test_compaction import (
    compatible,
    detection_masks,
    fill,
    greedy_cover,
    intersect,
    merge_cubes,
    minimum_test_set,
    relax_to_cube,
    reverse_order_fault_simulation,
    set_cover_circuit,
    static_compact,
)


def covers(c, vectors, faults):
    return {f for f in faults if any(c.detects(v, f) for v in vectors)}


def is_subsequence(small, big):
    it = iter(big)
    return all(any(v == w for w in it) for v in small)


def per_fault_cubes(c, rng):
    """One test cube for each detectable fault, in a random order."""
    faults = [f for f in c.faults() if c.detectable(f)]
    rng.shuffle(faults)
    return faults, [relax_to_cube(c, f, rng.choice(c.detecting_vectors(f))) for f in faults]


def dropping_cubes(c, rng):
    """Cubes as an ATPG with fault dropping makes them, after a fill with 0."""
    faults = [f for f in c.faults() if c.detectable(f)]
    rng.shuffle(faults)
    cubes, done = [], set()
    for f in faults:
        if f in done:
            continue
        cube = relax_to_cube(c, f, rng.choice(c.detecting_vectors(f)))
        cubes.append(cube)
        done |= {g for g in faults if c.detects(fill(cube), g)}
    return faults, cubes


def harmonic(d):
    return sum(1.0 / i for i in range(1, d + 1))


def example_circuit():
    return Circuit(
        ["a", "b", "c", "d"],
        [("g", "AND", ["a", "b"]), ("h", "OR", ["c", "d"]), ("z", "NAND", ["g", "h"])],
        ["z"],
    )


def test_cube_operations():
    assert compatible((0, X, 1), (X, 1, 1))
    assert not compatible((0, X, 1), (1, X, X))
    assert intersect((0, X, X), (X, 1, X)) == (0, 1, X)
    assert fill((X, 1, X)) == (0, 1, 0)
    assert fill((X, 1, X), 1) == (1, 1, 1)
    assert merge_cubes([(0, X, X), (1, X, X), (X, 1, X), (1, X, 0)]) == [(0, 1, X), (1, X, 0)]


def test_relax_to_cube_is_a_test_cube():
    rng = random.Random(3)
    for _ in range(40):
        c = random_circuit(rng, rng.randint(2, 4), rng.randint(2, 6))
        for f in c.faults():
            vs = c.detecting_vectors(f)
            if not vs:
                assert relax_to_cube(c, f, c.all_vectors()[0]) is None
                continue
            cube = relax_to_cube(c, f, rng.choice(vs))
            assert all(c.detects(w, f) for w in completions(cube))


@pytest.mark.parametrize("seed", range(6))
def test_reverse_order_keeps_coverage(seed):
    rng = random.Random(100 + seed)
    for _ in range(25):
        c = random_circuit(rng, rng.randint(2, 4), rng.randint(2, 7))
        faults = c.faults()
        vectors = [tuple(rng.randint(0, 1) for _ in c.pi) for _ in range(rng.randint(1, 12))]
        kept = reverse_order_fault_simulation(c, vectors, faults)
        assert covers(c, kept, faults) == covers(c, vectors, faults)
        assert is_subsequence(kept, [tuple(v) for v in vectors])
        # a vector is kept exactly when it detects a fault that no later vector detects
        needed = sum(
            1 for i, v in enumerate(vectors)
            if {f for f in faults if c.detects(v, f)} - covers(c, vectors[i + 1:], faults)
        )
        assert len(kept) == needed


@pytest.mark.parametrize("seed", range(4))
def test_merging_keeps_every_target_fault(seed):
    rng = random.Random(200 + seed)
    for _ in range(30):
        c = random_circuit(rng, rng.randint(3, 4), rng.randint(2, 7))
        faults, cubes = dropping_cubes(c, rng)
        merged = merge_cubes(cubes)
        assert len(merged) <= len(cubes)
        for t in cubes:
            # some merged cube lies inside t, so all its completions detect t's fault
            inside = [u for u in merged if all(a == X or a == b for a, b in zip(t, u))]
            assert inside
        targets = {f for f in faults if any(all(c.detects(w, f) for w in completions(u)) for u in cubes)}
        vectors = [fill(u) for u in merged]
        assert targets <= covers(c, vectors, faults)
        kept = static_compact(c, cubes, faults)
        assert targets <= covers(c, kept, faults)


def test_one_cube_per_fault_keeps_all_faults_and_beats_the_minimum_bound():
    rng = random.Random(7)
    total = [0, 0, 0]
    for _ in range(60):
        c = random_circuit(rng, rng.randint(3, 4), rng.randint(3, 7))
        faults, cubes = per_fault_cubes(c, rng)
        kept = static_compact(c, cubes, faults)
        best = minimum_test_set(c, c.all_vectors(), faults)
        assert covers(c, kept, faults) == set(faults)
        assert covers(c, best, faults) == set(faults)
        assert len(kept) >= len(best)
        total[0] += len(cubes)
        total[1] += len(kept)
        total[2] += len(best)
    assert total[2] <= total[1] < total[0]


def test_minimum_test_set_is_minimum():
    rng = random.Random(11)
    for _ in range(40):
        c = random_circuit(rng, rng.randint(2, 3), rng.randint(2, 5))
        faults = [f for f in c.faults() if c.detectable(f)]
        vectors = c.all_vectors()
        best = minimum_test_set(c, vectors, faults)
        assert covers(c, best, faults) == set(faults)
        for subset in combinations(vectors, len(best) - 1):
            assert covers(c, subset, faults) != set(faults)


def test_greedy_cover_bound():
    rng = random.Random(13)
    for _ in range(60):
        c = random_circuit(rng, rng.randint(3, 4), rng.randint(3, 7))
        faults = [f for f in c.faults() if c.detectable(f)]
        vectors = c.all_vectors()
        greedy = greedy_cover(c, vectors, faults)
        best = minimum_test_set(c, vectors, faults)
        assert covers(c, greedy, faults) == set(faults)
        d = max(bin(m).count("1") for m in detection_masks(c, vectors, faults))
        assert len(best) <= len(greedy) <= harmonic(d) * len(best) + 1e-9


def brute_force_set_cover(m, sets):
    universe = set().union(*sets)
    for size in range(m + 1):
        for pick in combinations(range(m), size):
            if set().union(*(sets[i] for i in pick)) == universe:
                return size
    raise AssertionError("unreachable")


def test_set_cover_reduction():
    rng = random.Random(17)
    for _ in range(60):
        m = rng.randint(2, 5)
        n = rng.randint(1, 5)
        sets = [set(e for e in range(n) if rng.random() < 0.4) for _ in range(m)]
        for e in range(n):
            if not any(e in s for s in sets):
                sets[rng.randrange(m)].add(e)
        if not set().union(*sets):
            continue
        c, faults = set_cover_circuit(m, sets)
        elements = sorted(set().union(*sets))
        # a vector detects y_e/0 exactly when it has one 1, at some x_i with e in S_i
        for v in product((0, 1), repeat=m):
            ones = [i for i in range(m) if v[i]]
            for e, f in zip(elements, faults):
                assert c.detects(v, f) == (len(ones) == 1 and e in sets[ones[0]])
        best = minimum_test_set(c, c.all_vectors(), faults)
        assert len(best) == brute_force_set_cover(m, sets)


def test_example_circuit():
    c = example_circuit()
    faults = c.faults()
    assert len(faults) == 14
    assert all(c.detectable(f) for f in faults)
    best = minimum_test_set(c, c.all_vectors(), faults)
    assert len(best) == 5
    for subset in combinations(c.all_vectors(), 4):
        assert covers(c, subset, faults) != set(faults)
    named = {c.fault_name(f): f for f in faults}
    assert c.detecting_vectors(named["c/0"]) == [(1, 1, 1, 0)]
    assert c.detecting_vectors(named["d/0"]) == [(1, 1, 0, 1)]
    for name in ("c/1", "d/1", "h/1"):
        assert c.detecting_vectors(named[name]) == [(1, 1, 0, 0)]
    assert sorted(best) == [(0, 1, 0, 1), (1, 0, 0, 1), (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0)]


def test_worked_example_of_the_page():
    c = example_circuit()
    faults = c.faults()
    cubes = [(X, X, 0, 0), (1, 1, X, 1), (0, 1, X, 1), (1, 0, X, 1), (1, 1, 1, 0), (1, 1, 0, 0), (1, 1, 0, 1), (X, 0, X, 1)]
    named = {c.fault_name(f): f for f in faults}
    for cube, name in zip(cubes, ("z/0", "a/0", "a/1", "b/1", "c/0", "c/1", "d/0", "g/1")):
        assert all(c.detects(w, named[name]) for w in completions(cube))
    assert merge_cubes(cubes) == [(1, 1, 0, 0), (1, 1, 0, 1), (0, 1, X, 1), (1, 0, X, 1), (1, 1, 1, 0)]
    kept = static_compact(c, cubes, faults)
    assert kept == [(1, 1, 0, 0), (1, 1, 0, 1), (0, 1, 0, 1), (1, 0, 0, 1), (1, 1, 1, 0)]
    only = reverse_order_fault_simulation(c, [fill(u) for u in cubes], faults)
    assert only == [(0, 1, 0, 1), (1, 0, 0, 1), (1, 1, 1, 0), (1, 1, 0, 0), (1, 1, 0, 1), (0, 0, 0, 1)]
    # five faults with pairwise disjoint test sets give the lower bound 5
    independent = [set(c.detecting_vectors(named[n])) for n in ("a/1", "b/1", "c/0", "d/0", "h/1")]
    for p, q in combinations(independent, 2):
        assert not p & q


def test_merging_can_lose_a_chance_detection():
    c = Circuit(["a", "b", "c"], [("g", "NOT", ["a"]), ("h", "NAND", ["b", "g"])], ["h", "c"])
    faults = c.faults()
    cubes = [(1, 1, X), (0, 1, X), (X, X, 1)]
    b1 = (c.line("b"), 1)
    assert c.detecting_vectors(b1) == [(0, 0, 0), (0, 0, 1)]
    assert b1 in covers(c, [fill(u) for u in cubes], faults)
    assert merge_cubes(cubes) == [(1, 1, 1), (0, 1, X)]
    kept = static_compact(c, cubes, faults)
    assert b1 not in covers(c, kept, faults)
