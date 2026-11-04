# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balas-additive-algorithm/. The authors are listed in prov/MXCW04.jsonl.

import itertools
import random

import pytest

from balas_additive_algorithm import balas

C = [3, 5, 2, 6, 3]
A = [[-5, 1, 1, -4, -4], [-3, 0, 2, 4, 2], [1, -2, -2, 0, 5]]
B = [-1, -1, 0]


def brute(c, a, b):
    n = len(c)
    best = None
    for x in itertools.product([0, 1], repeat=n):
        if all(sum(r[j] * x[j] for j in range(n)) <= bi for r, bi in zip(a, b)):
            v = sum(cj * xj for cj, xj in zip(c, x))
            if best is None or v < best:
                best = v
    return best


def test_example_of_the_page() -> None:
    stats: dict[str, int] = {}
    trace: list = []
    z, x = balas(C, A, B, stats, trace)
    assert z == 5 and x == [1, 0, 1, 0, 0]
    assert stats == {"nodes": 7}
    assert trace == [
        ((), "branch 0"),
        ((0,), "branch 1"),
        ((0, 1), "feasible"),
        ((0,), "branch 2"),
        ((0, 2), "feasible"),
        ((0,), "fathomed"),
        ((), "fathomed"),
    ]


def test_edge_cases() -> None:
    assert balas([], [], []) == (0, [])
    assert balas([], [[]], [-1]) == (None, None)
    assert balas([4, 1], [], []) == (0, [0, 0])
    assert balas([4, 1], [[-1, -1]], [-1]) == (1, [0, 1])
    assert balas([4, 1], [[-1, -1]], [-3]) == (None, None)
    assert balas([2, 2], [[-1, -1]], [-2]) == (4, [1, 1])


def test_negative_cost_rejected() -> None:
    with pytest.raises(ValueError):
        balas([-1], [], [])


def test_jeroslow_like_parity() -> None:
    # 2 x_1 + ... + 2 x_n = n with n odd, written as two inequalities: no solution.
    n = 7
    a = [[2] * n, [-2] * n]
    assert balas([1] * n, a, [n, -n]) == (None, None)


def test_random_against_brute_force() -> None:
    rng = random.Random(1965)
    for _ in range(800):
        n = rng.randint(0, 10)
        m = rng.randint(0, 4)
        c = [rng.randint(0, 9) for _ in range(n)]
        a = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(m)]
        b = [rng.randint(-8, 4) for _ in range(m)]
        z, x = balas(c, a, b)
        assert z == brute(c, a, b)
        if x is not None:
            assert sum(cj * xj for cj, xj in zip(c, x)) == z
            assert all(sum(r[j] * x[j] for j in range(n)) <= bi for r, bi in zip(a, b))


def test_set_cover() -> None:
    # Cover {1, 2, 3, 4} with sets {1, 2}, {2, 3}, {3, 4}, {1, 4}, {1, 2, 3}: each element row reads -sum x <= -1.
    sets = [{1, 2}, {2, 3}, {3, 4}, {1, 4}, {1, 2, 3}]
    a = [[-1 if e in s else 0 for s in sets] for e in range(1, 5)]
    z, x = balas([1] * 5, a, [-1] * 4)
    assert z == 2 and z == brute([1] * 5, a, [-1] * 4)
