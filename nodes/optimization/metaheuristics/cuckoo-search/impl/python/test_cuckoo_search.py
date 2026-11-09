# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuckoo-search/. The authors are listed in prov/TQA8RV.jsonl.

import math
import random
import statistics

from cuckoo_search import cuckoo_search, de_move, levy_move, levy_step, mantegna_sigma, rastrigin, sphere


def test_mantegna_sigma() -> None:
    assert math.isclose(mantegna_sigma(1.5), 0.6965745025576967, rel_tol=1e-12)
    assert math.isclose(mantegna_sigma(1.0), 1.0, rel_tol=1e-12)  # Gamma(2) sin(pi/2) / (Gamma(1) 1 2^0) = 1
    assert math.isclose(mantegna_sigma(2.0), 0.0, abs_tol=1e-7)  # sin(pi) = 0: the Gaussian limit degenerates


def test_levy_step_is_the_mantegna_ratio() -> None:
    beta = 1.5
    r1, r2 = random.Random(1), random.Random(1)
    for _ in range(200):
        s = levy_step(beta, r1)
        u = r2.gauss(0.0, mantegna_sigma(beta))
        v = r2.gauss(0.0, 1.0)
        assert s == u / abs(v) ** (1 / beta)
    rng = random.Random(2)
    steps = [levy_step(beta, rng) for _ in range(40000)]
    assert abs(statistics.median(steps)) < 0.03  # symmetric about 0
    # Heavy tail: P(|s| > 10) is about 1 percent here, while a normal law with the same median of |s| gives almost 0.
    big = sum(abs(s) > 10 for s in steps) / len(steps)
    assert 0.003 < big < 0.03


def test_levy_move_leaves_the_best_point_fixed() -> None:
    rng = random.Random(3)
    g = [0.5, -1.0, 2.0]
    for _ in range(100):
        assert levy_move(g, g, 0.01, 1.5, rng) == g
    x = [1.5, -1.0, 4.0]
    y = levy_move(x, g, 0.01, 1.5, rng)
    assert y[1] == x[1]  # zero distance to the best in this coordinate gives a zero step


def test_de_move_and_its_mask() -> None:
    x, xp, xq = [1.0, 2.0, 3.0], [0.0, 4.0, -2.0], [2.0, 1.0, 2.0]
    assert de_move(x, xp, xq, 0.5, [True, False, True]) == [0.0, 2.0, 1.0]
    assert de_move(x, xp, xq, 0.5, [False, False, False]) == x
    assert de_move(x, xp, xp, 0.9, [True, True, True]) == x  # equal partners: no change


def test_nests_only_improve() -> None:
    seen = []

    def check(t, x, fx):
        assert fx == [rastrigin(p) for p in x]
        assert all(-5.12 <= v <= 5.12 for p in x for v in p)
        seen.append(fx)

    _, fg, hist = cuckoo_search(rastrigin, [-5.12] * 3, [5.12] * 3, 8, 0.25, 0.01, 1.5, 150, random.Random(4), check)
    for prev, cur in zip(seen, seen[1:]):
        assert all(c <= p for p, c in zip(prev, cur))
    assert all(hist[t + 1] <= hist[t] for t in range(len(hist) - 1))
    assert fg == min(seen[-1])


def test_fixed_seed_on_sphere_and_rastrigin() -> None:
    g, fg, _ = cuckoo_search(sphere, [-5.12] * 5, [5.12] * 5, 15, 0.25, 0.01, 1.5, 500, random.Random(0))
    assert fg < 1e-9 and fg == sphere(g)
    g, fg, _ = cuckoo_search(rastrigin, [-5.12] * 2, [5.12] * 2, 15, 0.25, 0.01, 1.5, 500, random.Random(0))
    assert fg < 1e-7 and all(abs(v) < 1e-4 for v in g)
