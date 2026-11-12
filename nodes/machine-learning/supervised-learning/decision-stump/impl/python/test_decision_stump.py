# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-stump/. The authors are listed in prov/H1E126.jsonl.

import itertools
import random
from fractions import Fraction as F

from decision_stump import Stump, best_stump, weighted_error


def brute_force(X, y, w):
    """Least error over every threshold (each data value, and minus infinity) and every leaf pair."""
    classes = sorted(set(y))
    best = None
    for j in range(len(X[0])):
        for theta in [None] + sorted(set(x[j] for x in X)):
            for a, b in itertools.product(classes, repeat=2):
                e = 0
                for xi, yi, wi in zip(X, y, w):
                    pred = a if theta is not None and xi[j] <= theta else b
                    e += wi if pred != yi else 0
                best = e if best is None or e < best else best
    return best


EX_X = [(1, 5), (2, 3), (3, 6), (4, 1), (5, 4), (6, 2)]
EX_Y = [1, 1, -1, 1, -1, -1]


def test_page_example():
    s = best_stump(EX_X, EX_Y)
    assert s == Stump(1, 0, 2, 1, -1)
    assert weighted_error(s, EX_X, EX_Y, [1] * 6) == 1


def test_page_example_weighted():
    w = [F(1, 10)] * 3 + [F(4, 10)] + [F(1, 10)] * 2
    s = best_stump(EX_X, EX_Y, w)
    assert s.error == brute_force(EX_X, EX_Y, w) == F(1, 10)
    assert s == Stump(F(1, 10), 0, 4, 1, -1)


def test_xor_has_no_edge():
    X = [(0, 0), (0, 1), (1, 0), (1, 1)]
    y = [0, 1, 1, 0]
    assert best_stump(X, y).error == 2


def test_single_example_and_all_equal():
    assert best_stump([(3,)], ["a"]) == Stump(0, -1, None, "a", "a")
    s = best_stump([(1, 1)] * 4, ["a", "b", "b", "a"])
    assert s.j == -1 and s.error == 2


def test_against_brute_force():
    rng = random.Random(1997)
    for trial in range(600):
        n, d, k = rng.randint(1, 9), rng.randint(1, 3), rng.randint(2, 3)
        X = [tuple(rng.randint(0, 4) for _ in range(d)) for _ in range(n)]
        y = [rng.randrange(k) for _ in range(n)]
        w = [F(rng.randint(0, 5), 7) for _ in range(n)]
        s = best_stump(X, y, w)
        assert s.error == brute_force(X, y, w)
        assert weighted_error(s, X, y, w) == s.error


def test_float_data():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(2, 12)
        X = [(rng.random(), rng.random()) for _ in range(n)]
        y = [rng.choice((-1, 1)) for _ in range(n)]
        w = [rng.random() for _ in range(n)]
        s = best_stump(X, y, w)
        assert abs(s.error - brute_force(X, y, w)) < 1e-9
