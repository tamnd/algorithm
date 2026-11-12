# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-iterative-matching/. The authors are listed in prov/V6ZQKP.jsonl.

import itertools
import math
import random

from parallel_iterative_matching import is_matching, is_maximal, pim

EXAMPLE = [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 0, 1]]


def as_bool(m: list[list[int]]) -> list[list[bool]]:
    return [[bool(x) for x in row] for row in m]


def all_maximal_matchings(req: list[list[bool]]) -> set[tuple[int, ...]]:
    """Every maximal matching of a small request matrix, by enumeration."""
    n = len(req)
    found = set()
    for choice in itertools.product(range(-1, n), repeat=n):
        m = list(choice)
        if is_matching(req, m) and is_maximal(req, m):
            found.add(tuple(m))
    return found


def test_example_trace() -> None:
    match, history = pim(as_bool(EXAMPLE), random.Random(0))
    assert match == [0, 2, 1, 3]
    assert history == [8, 1, 0]


def test_result_is_a_maximal_matching_by_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randrange(1, 5)
        req = [[rng.random() < 0.5 for _ in range(n)] for _ in range(n)]
        maximal = all_maximal_matchings(req)
        match, history = pim(req, rng)
        assert tuple(match) in maximal
        assert history[-1] == 0
        # The unresolved count never grows.
        assert all(b <= a for a, b in zip(history, history[1:]))


def test_three_quarters_resolved_per_iteration_on_average() -> None:
    for n, density, seed in ((4, 1.0, 1), (16, 1.0, 2), (16, 0.3, 3), (32, 0.5, 4)):
        rng = random.Random(seed)
        before = after = 0
        for _ in range(300):
            req = [[rng.random() < density for _ in range(n)] for _ in range(n)]
            _, history = pim(req, rng)
            for a, b in zip(history, history[1:]):
                before += a
                after += b
        assert 1 - after / before >= 0.75


def test_iterations_within_log_bound_on_average() -> None:
    for n in (8, 16, 32):
        rng = random.Random(n)
        full = [[True] * n for _ in range(n)]
        runs = [len(pim(full, rng)[1]) - 1 for _ in range(300)]
        assert sum(runs) / len(runs) <= math.ceil(math.log2(n)) + 4 / 3


def test_one_iteration_on_full_requests_is_about_one_minus_one_over_e() -> None:
    n = 64
    rng = random.Random(9)
    full = [[True] * n for _ in range(n)]
    sizes = [sum(1 for j in pim(full, rng, max_iterations=1)[0] if j >= 0) for _ in range(200)]
    expected = n * (1 - (1 - 1 / n) ** n)
    assert abs(sum(sizes) / len(sizes) - expected) < 1.0
