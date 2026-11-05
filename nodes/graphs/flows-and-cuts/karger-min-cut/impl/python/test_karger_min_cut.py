# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karger-min-cut/. The authors are listed in prov/981JCR.jsonl.

import itertools
import math
import random

from karger_min_cut import contract, karger_min_cut

# two triangles with doubled edges, joined by c-d and b-e (a..f = 0..5)
EXAMPLE = [(0, 1), (0, 1), (0, 2), (0, 2), (1, 2), (1, 2),
           (3, 4), (3, 4), (3, 5), (3, 5), (4, 5), (4, 5),
           (2, 3), (1, 4)]


def brute(n, edges):
    """Independent oracle: the minimum over all 2^(n-1) - 1 cuts that hold vertex 0."""
    best = None
    for r in range(0, n - 1):
        for rest in itertools.combinations(range(1, n), r):
            s = {0, *rest}
            k = sum(1 for u, v in edges if (u in s) != (v in s))
            best = k if best is None else min(best, k)
    return best


def cut_of(edges, s):
    return sum(1 for u, v in edges if (u in s) != (v in s))


def test_example() -> None:
    k, s = karger_min_cut(6, EXAMPLE, 200, random.Random(1))
    assert k == 2 and s == {0, 1, 2}


def test_one_run_is_always_a_cut() -> None:
    rng = random.Random(7)
    for _ in range(200):
        s, k = contract(6, EXAMPLE, rng)
        assert 0 in s and 0 < len(s) < 6
        assert k == cut_of(EXAMPLE, s) and k >= 2


def test_success_rate_meets_the_bound() -> None:
    rng = random.Random(11)
    runs = 3000
    hits = sum(1 for _ in range(runs) if contract(6, EXAMPLE, rng)[1] == 2)
    assert hits / runs >= 2 / (6 * 5)


def test_disconnected_and_two_vertices() -> None:
    k, s = karger_min_cut(4, [(0, 1), (2, 3)], 1, random.Random(3))
    assert k == 0 and s == {0, 1}
    assert karger_min_cut(3, [], 1, random.Random(3))[0] == 0
    assert karger_min_cut(2, [(0, 1), (0, 1), (0, 1)], 1, random.Random(3)) == (3, {0})
    assert karger_min_cut(2, [(0, 0), (1, 1)], 1, random.Random(3)) == (0, {0})


def test_self_loops_are_ignored() -> None:
    edges = [(0, 0), (0, 1), (1, 2), (2, 2), (2, 0), (2, 3)]
    assert karger_min_cut(4, edges, 50, random.Random(5))[0] == 1


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(2, 7)
        m = rng.randint(0, 14)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        trials = math.ceil(n * (n - 1) / 2 * math.log(1e6))
        k, s = karger_min_cut(n, edges, trials, rng)
        assert k == cut_of(edges, s)
        assert k == brute(n, edges)
