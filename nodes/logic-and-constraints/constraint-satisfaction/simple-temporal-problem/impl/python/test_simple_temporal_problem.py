# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-temporal-problem/. The authors are listed in prov/CNEAFW.jsonl.

import itertools
import math
import random

from simple_temporal_problem import minimal_network, satisfies, solve

INF = math.inf

# The page example: X0 = 7:00, X1 leave home, X2 arrive at work, X3 the meeting.
EXAMPLE = [(0, 1, 0, 30), (1, 2, 30, 40), (2, 3, 10, 20), (0, 3, 60, 65)]


def test_page_example():
    d = minimal_network(4, EXAMPLE)
    bounds = {(i, j): (-d[j][i], d[i][j]) for i in range(4) for j in range(4) if i < j}
    assert bounds == {
        (0, 1): (0, 25),
        (0, 2): (40, 55),
        (0, 3): (60, 65),
        (1, 2): (30, 40),
        (1, 3): (40, 60),
        (2, 3): (10, 20),
    }
    times = solve(4, EXAMPLE)
    assert satisfies(times, EXAMPLE)
    late = EXAMPLE[:3] + [(0, 3, 30, 35)]
    assert minimal_network(4, late) is None and solve(4, late) is None


def brute(n, cons, h):
    """All integer solutions with X_0 = 0 and 0 <= X_i <= h."""
    out = []
    for rest in itertools.product(range(h + 1), repeat=n - 1):
        t = (0,) + rest
        if satisfies(t, cons):
            out.append(t)
    return out


def test_against_brute_force():
    rng = random.Random(1991)
    consistent = 0
    for _ in range(600):
        n = rng.randint(1, 5)
        h = rng.randint(1, 6)
        # The horizon: 0 <= X_i - X_0 <= h for every point.
        cons = [(0, i, 0, h) for i in range(1, n)]
        for _ in range(rng.randint(0, 6)):
            if n < 2:
                break
            i, j = rng.sample(range(n), 2)
            a = rng.randint(-h, h)
            b = rng.randint(a - 1, h)  # b = a - 1 makes an empty interval
            if rng.random() < 0.2:
                a = -INF
            elif rng.random() < 0.2:
                b = INF
            cons.append((i, j, a, b))
        sols = brute(n, cons, h)
        d = minimal_network(n, cons)
        t = solve(n, cons)
        if not sols:
            assert d is None and t is None
            continue
        consistent += 1
        assert d is not None and t is not None and satisfies(t, cons)
        # The minimal network: every implied bound is reached by an integer solution.
        for i in range(n):
            for j in range(n):
                diffs = [s[j] - s[i] for s in sols]
                assert max(diffs) == d[i][j]
                assert min(diffs) == -d[j][i]
    assert consistent > 200


def test_edges():
    assert minimal_network(0, []) == []
    assert solve(0, []) == []
    assert solve(2, []) == [0, 0]
    assert minimal_network(2, [(0, 1, 3, 2)]) is None
