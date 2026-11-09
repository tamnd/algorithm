# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-envelope/. The authors are listed in prov/NQC7CW.jsonl.

import random
from fractions import Fraction as F

from convex_envelope import ConvexEnvelope, lower_hull


def brute(xs, fs, x):
    """min over convex combinations of at most two samples with mean x (Caratheodory in 1D)."""
    best = None
    for xi, fi in zip(xs, fs):
        if xi == x:
            best = fi if best is None else min(best, fi)
    for xi, fi in zip(xs, fs):
        for xj, fj in zip(xs, fs):
            if xi < x < xj:
                t = F(x - xi) / (xj - xi)
                v = (1 - t) * fi + t * fj
                best = v if best is None else min(best, v)
    return best


def test_double_well():
    xs = list(range(-3, 4))
    fs = [min((x - 1) ** 2, (x + 1) ** 2) for x in xs]  # 4, 1, 0, 1, 0, 1, 4
    env = ConvexEnvelope(xs, fs)
    assert [env(x) for x in xs] == [4, 1, 0, 0, 0, 1, 4]
    assert env(F(1, 2)) == 0 and env(F(-5, 2)) == F(5, 2)
    assert env(4) is None
    assert lower_hull(list(zip(xs, fs))) == [(-3, 4), (-2, 1), (-1, 0), (1, 0), (2, 1), (3, 4)]


def test_random_against_brute_force():
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randint(1, 10)
        xs = [F(rng.randint(-15, 15), rng.randint(1, 3)) for _ in range(n)]
        fs = [F(rng.randint(-20, 20), rng.randint(1, 3)) for _ in range(n)]
        env = ConvexEnvelope(xs, fs)
        queries = list(xs) + [F(rng.randint(-60, 60), 4) for _ in range(10)]
        for q in queries:
            assert env(q) == brute(xs, fs, q)


def test_envelope_is_convex_and_below():
    rng = random.Random(10)
    for _ in range(100):
        xs = [F(rng.randint(-10, 10)) for _ in range(rng.randint(2, 9))]
        fs = [F(rng.randint(-10, 10)) for _ in xs]
        env = ConvexEnvelope(xs, fs)
        for x, f in zip(xs, fs):
            assert env(x) <= f
        grid = [F(k, 4) for k in range(-40, 41) if env(F(k, 4)) is not None]
        for a, b, c in zip(grid, grid[1:], grid[2:]):
            assert 2 * env(b) <= env(a) + env(c)  # midpoint convexity on an even grid
