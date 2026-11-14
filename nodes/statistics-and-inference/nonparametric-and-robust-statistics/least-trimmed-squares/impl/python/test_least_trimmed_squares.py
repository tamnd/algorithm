# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-trimmed-squares/. The authors are listed in prov/DQP8F6.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from least_trimmed_squares import (
    c_step, default_h, design, fast_lts, lts_exact, objective, ols,
)

PAGE_X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PAGE_Y = [3, 5, 8, 9, 11, 14, 15, 2, 1, 0]


def F(rows):
    return [[Fraction(v) for v in r] for r in rows]


def test_page_example() -> None:
    X, y = F(design(PAGE_X)), [Fraction(v) for v in PAGE_Y]
    h = default_h(10, 2)
    assert h == 6
    b, q = lts_exact(X, y)
    assert b == [Fraction(142, 161), Fraction(333, 161)]
    assert q == Fraction(114, 161)
    # C-steps from the pair {1, 2} stop at a local minimum.
    b = ols(X, y, [0, 1])
    assert b == [1, 2] and objective(X, y, b, h) == 1
    b = c_step(X, y, b, h)
    assert b == [Fraction(89, 70), Fraction(69, 35)]
    assert objective(X, y, b, h) == Fraction(57, 70)
    assert c_step(X, y, b, h) == b
    # From the bad pair {8, 9} they stop at a fit of the bad points.
    b = ols(X, y, [7, 8])
    assert b == [10, -1] and objective(X, y, b, h) == 19
    b = c_step(X, y, b, h)
    assert objective(X, y, b, h) == Fraction(1625, 87)
    assert c_step(X, y, b, h) == b
    # No start from a pair reaches the global minimum on these data.
    for P in combinations(range(10), 2):
        b = ols(X, y, list(P))
        q = objective(X, y, b, h)
        while True:
            b2 = c_step(X, y, b, h)
            q2 = objective(X, y, b2, h)
            if q2 >= q:
                break
            b, q = b2, q2
        assert q > Fraction(114, 161)
    # So FAST-LTS returns the good local minimum, an upper bound.
    assert fast_lts(design(PAGE_X), PAGE_Y, starts=50)[1] == Fraction(57, 70)


def test_c_step_never_increases() -> None:
    rng = random.Random(41)
    for _ in range(300):
        n = rng.randint(3, 12)
        X = F(design(rng.sample(range(-20, 20), n)))
        y = [Fraction(rng.randint(-20, 20)) for _ in range(n)]
        h = rng.randint(2, n)
        b = [Fraction(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(2)]
        assert objective(X, y, c_step(X, y, b, h), h) <= objective(X, y, b, h)


def test_exact_is_the_minimum() -> None:
    rng = random.Random(42)
    for _ in range(40):
        n = rng.randint(4, 10)
        X = F(design(rng.sample(range(-10, 10), n)))
        y = [Fraction(rng.randint(-10, 10)) for _ in range(n)]
        h = default_h(n, 2)
        b, q = lts_exact(X, y)
        assert objective(X, y, b, h) == q
        # No line on a grid, and no fixed point of the C-steps, does better.
        for _ in range(100):
            g = [Fraction(rng.randint(-40, 40), 4), Fraction(rng.randint(-20, 20), 4)]
            assert objective(X, y, g, h) >= q
        # The optimum is a fixed point in value.
        assert objective(X, y, c_step(X, y, b, h), h) == q


def test_fast_lts_against_enumeration() -> None:
    rng = random.Random(43)
    hits = 0
    trials = 30
    for t in range(trials):
        n = rng.randint(6, 12)
        x = rng.sample(range(0, 30), n)
        y = [2 * v + 1 + rng.randint(-2, 2) for v in x]
        for i in rng.sample(range(n), (n - 1) // 3):
            y[i] = rng.randint(-60, 60)
        exact = lts_exact(design(x), y)[1]
        got = fast_lts(design(x), y, starts=20, rng=random.Random(t))[1]
        assert got >= exact
        hits += got == exact
    assert hits >= trials // 2


def test_quadratic_model() -> None:
    rng = random.Random(44)
    for _ in range(10):
        n = rng.randint(6, 9)
        x = rng.sample(range(-6, 7), n)
        X = [[1, v, v * v] for v in x]
        y = [v * v - 2 * v + 3 for v in x]
        y[0] += 50
        b, q = lts_exact(X, y)
        assert q == 0 and b == [3, -2, 1]
        b2, q2 = fast_lts(X, y, starts=40, rng=random.Random(n))
        assert q2 == 0 and b2 == [3, -2, 1]


def test_exact_fit_with_majority_on_a_line() -> None:
    x = list(range(10))
    y = [3 - 2 * v for v in x]
    for i, v in zip((1, 4, 6, 9), (100, -50, 77, 0)):
        y[i] = v
    b, q = fast_lts(design(x), y, starts=30)
    assert q == 0 and b == [3, -2]
