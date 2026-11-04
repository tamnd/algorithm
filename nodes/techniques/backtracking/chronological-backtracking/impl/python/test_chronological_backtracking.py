# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chronological-backtracking/. The authors are listed in prov/5ZHQ6D.jsonl.

import itertools
import random

from chronological_backtracking import chronological_backtracking, solutions


def brute(domains, constraints):
    out = []
    for t in itertools.product(*domains):
        if all(p(t[j], t[i]) for (j, i), p in constraints.items()):
            out.append(list(t))
    return out


def test_example_of_the_page() -> None:
    domains = [[1, 2], [1, 2, 3], [1, 2, 3], [1, 2]]
    constraints = {(1, 2): lambda a, b: a != b, (0, 3): lambda a, b: b < a}
    stats: dict[str, int] = {}
    assert chronological_backtracking(domains, constraints, stats) == [2, 1, 2, 1]
    assert stats == {"assignments": 14, "checks": 24}


def test_edges() -> None:
    assert chronological_backtracking([], {}) == []
    assert list(solutions([], {})) == [[]]
    assert chronological_backtracking([[]], {}) is None
    assert chronological_backtracking([[1], [1]], {(0, 1): lambda a, b: a != b}) is None
    assert list(solutions([[0, 1], [0, 1]], {})) == [[0, 0], [0, 1], [1, 0], [1, 1]]


def test_four_queens_as_csp() -> None:
    n = 4
    cons = {}
    for j in range(n):
        for i in range(j + 1, n):
            cons[(j, i)] = (lambda d: lambda a, b: a != b and abs(a - b) != d)(i - j)
    assert list(solutions([range(1, n + 1)] * n, cons)) == [[2, 4, 1, 3], [3, 1, 4, 2]]


def test_thrashing_family() -> None:
    for d in range(2, 5):
        for m in range(3, 6):
            doms = [[1, 2]] + [list(range(1, d + 1))] * (m - 2) + [[1, 2]]
            stats: dict[str, int] = {}
            sol = chronological_backtracking(doms, {(0, m - 1): lambda a, b: b < a}, stats)
            assert sol == [2] + [1] * (m - 2) + [1]
            # with X_1 = 1 the search assigns every prefix of X_2 .. X_{m-1}
            assert stats["assignments"] >= d ** (m - 2)


def test_random_against_brute_force() -> None:
    rng = random.Random(77)
    for _ in range(800):
        m = rng.randrange(0, 5)
        domains = [rng.sample(range(4), rng.randrange(0, 4)) for _ in range(m)]
        constraints = {}
        for j in range(m):
            for i in range(j + 1, m):
                if rng.random() < 0.5:
                    allowed = {(a, b) for a in range(4) for b in range(4) if rng.random() < 0.6}
                    constraints[(j, i)] = (lambda s: lambda a, b: (a, b) in s)(allowed)
        want = brute(domains, constraints)
        assert list(solutions(domains, constraints)) == want
        assert chronological_backtracking(domains, constraints) == (want[0] if want else None)
