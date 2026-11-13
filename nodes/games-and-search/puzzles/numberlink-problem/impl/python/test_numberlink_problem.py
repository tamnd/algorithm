# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/numberlink-problem/. The authors are listed in prov/KZXTYY.jsonl.

import random

from numberlink_problem import brute_force, is_solution, solve

PAIRS = [((3, 1), (2, 0)), ((3, 3), (3, 2)), ((0, 1), (2, 2)), ((1, 3), (0, 2)), ((2, 3), (3, 0))]


def canon(sols):
    return sorted(tuple(tuple(path) for path in s) for s in sols)


def test_known_puzzle() -> None:
    sols = solve(5, 5, PAIRS, cover=True)
    assert len(sols) == 1
    grid = [[0] * 5 for _ in range(5)]
    for label, path in enumerate(sols[0], start=1):
        for r, c in path:
            grid[r][c] = label
    assert grid == [[3, 3, 4, 4, 4],
                    [3, 3, 3, 4, 4],
                    [1, 1, 3, 5, 5],
                    [5, 1, 2, 2, 5],
                    [5, 5, 5, 5, 5]]
    assert canon(sols) == canon(brute_force(5, 5, PAIRS, cover=True))
    # Without the cover rule the same terminals allow 4 solutions.
    free = solve(5, 5, PAIRS)
    assert len(free) == 4
    assert canon(free) == canon(brute_force(5, 5, PAIRS))


def test_rules() -> None:
    assert is_solution(1, 3, [((0, 0), (0, 2))], [[(0, 0), (0, 1), (0, 2)]], cover=True)
    assert not is_solution(2, 2, [((0, 0), (0, 1))], [[(0, 0), (0, 1)]], cover=True)
    assert is_solution(2, 2, [((0, 0), (0, 1))], [[(0, 0), (0, 1)]])
    # Two pairs that must cross on a 3 by 3 board have no solution.
    pairs = [((0, 1), (2, 1)), ((1, 0), (1, 2))]
    assert solve(3, 3, pairs) == [] and brute_force(3, 3, pairs) == []


def test_solver_against_brute_force() -> None:
    rng = random.Random(41)
    for _ in range(60):
        h, w = rng.randint(2, 4), rng.randint(2, 4)
        cells = [(r, c) for r in range(h) for c in range(w)]
        k = rng.randint(1, min(3, len(cells) // 2))
        pts = rng.sample(cells, 2 * k)
        pairs = [(pts[2 * i], pts[2 * i + 1]) for i in range(k)]
        for cover in (False, True):
            got = solve(h, w, pairs, cover)
            assert all(is_solution(h, w, pairs, s, cover) for s in got)
            assert canon(got) == canon(brute_force(h, w, pairs, cover))
