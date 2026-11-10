# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longest-processing-time-first/. The authors are listed in prov/NPZATW.jsonl.

import itertools
import random
from fractions import Fraction

from longest_processing_time_first import longest_processing_time_first


def all_load_vectors(p: list[int], m: int) -> list[list[int]]:
    """The load vectors of all assignments (job 0 fixed to machine 0)."""
    if not p:
        return [[0] * m]
    out = []
    for rest in itertools.product(range(m), repeat=len(p) - 1):
        load = [0] * m
        for x, i in zip(p, (0,) + rest):
            load[i] += x
        out.append(load)
    return out


def test_example() -> None:
    p = [2, 3, 4, 6, 2, 2]
    machine, load = longest_processing_time_first(p, 3)
    assert machine == [2, 2, 1, 0, 1, 2]
    assert load == [6, 6, 7]
    assert max(load) == 7


def test_edges() -> None:
    assert longest_processing_time_first([], 2) == ([], [0, 0])
    assert longest_processing_time_first([4], 1) == ([0], [4])
    assert longest_processing_time_first([1, 2, 3], 5)[1] == [3, 2, 1, 0, 0]
    assert max(longest_processing_time_first([5, 5, 5, 5], 2)[1]) == 10


def test_assignment_is_consistent() -> None:
    rng = random.Random(21)
    for _ in range(300):
        m = rng.randrange(1, 5)
        p = [rng.randrange(0, 20) for _ in range(rng.randrange(0, 12))]
        machine, load = longest_processing_time_first(p, m)
        recomputed = [0] * m
        for j, i in enumerate(machine):
            recomputed[i] += p[j]
        assert recomputed == load


def test_against_brute_force() -> None:
    rng = random.Random(22)
    for _ in range(600):
        m = rng.randrange(1, 4)
        p = [rng.randrange(1, 13) for _ in range(rng.randrange(0, 8))]
        vectors = all_load_vectors(p, m)
        opt = min(max(v) for v in vectors)
        alg = max(longest_processing_time_first(p, m)[1])
        assert Fraction(sum(p), m) <= opt and max(p, default=0) <= opt
        assert alg <= (Fraction(4, 3) - Fraction(1, 3 * m)) * opt
        if len(p) <= m or all(3 * x > opt for x in p):
            assert alg == opt


def test_tight_family() -> None:
    for m in range(1, 9):
        p = [k for k in range(m + 1, 2 * m) for _ in range(2)] + [m] * 3
        assert sum(p) == 3 * m * m
        assert max(longest_processing_time_first(p, m)[1]) == 4 * m - 1
        # an optimal schedule: three jobs of length m, and the pairs (2m - i, m + i)
        assert all((2 * m - i) + (m + i) == 3 * m for i in range(1, m))


def test_machine_covering() -> None:
    rng = random.Random(23)
    for _ in range(400):
        m = rng.randrange(1, 4)
        p = [rng.randrange(1, 13) for _ in range(rng.randrange(m, 8))]
        best = max(min(v) for v in all_load_vectors(p, m))
        got = min(longest_processing_time_first(p, m)[1])
        assert got >= Fraction(3 * m - 1, 4 * m - 2) * best
    for m in range(1, 9):
        p = [k for k in range(m + 1, 2 * m) for _ in range(2)] + [m] * (m + 1)
        assert sum(p) == m * (4 * m - 2)
        assert min(longest_processing_time_first(p, m)[1]) == 3 * m - 1
        if m <= 3:
            assert max(min(v) for v in all_load_vectors(p, m)) == 4 * m - 2
            q = [k for k in range(m + 1, 2 * m) for _ in range(2)] + [m] * 3
            assert min(max(v) for v in all_load_vectors(q, m)) == 3 * m
