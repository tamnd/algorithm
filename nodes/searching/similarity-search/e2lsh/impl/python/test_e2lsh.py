# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/e2lsh/. The authors are listed in prov/K84C3G.jsonl.

import math
import random

from e2lsh import E2LSH, collision_probability, euclidean, parameters


def test_known_values() -> None:
    assert abs(collision_probability(1, 4) - 0.8005) < 1e-4
    assert abs(collision_probability(2, 4) - 0.6095) < 1e-4
    assert collision_probability(0, 4) == 1.0
    # p depends only on w/u, and decreases in u
    assert abs(collision_probability(2, 8) - collision_probability(1, 4)) < 1e-12
    ps = [collision_probability(u / 10, 4) for u in range(1, 200)]
    assert all(a > b for a, b in zip(ps, ps[1:]))


def test_rho_below_one_over_c_for_w4() -> None:
    for c in (1.5, 2, 3, 4):
        p1, p2 = collision_probability(1, 4), collision_probability(c, 4)
        assert math.log(1 / p1) / math.log(1 / p2) < 1 / c


def test_collision_probability_monte_carlo() -> None:
    rng = random.Random(11)
    w = 4.0
    for u in (0.5, 1.0, 2.0, 5.0):
        hits = 0
        trials = 20000
        for _ in range(trials):
            a, b = rng.gauss(0, 1), rng.uniform(0, w)
            hits += math.floor(b / w) == math.floor((a * u + b) / w)
        assert abs(hits / trials - collision_probability(u, w)) < 0.015


def test_answers_valid_against_brute_force() -> None:
    rng = random.Random(123)
    for _ in range(500):
        d = rng.randint(1, 4)
        pts = [[rng.uniform(-5, 5) for _ in range(d)] for _ in range(rng.randint(0, 20))]
        idx = E2LSH(pts, rng.randint(1, 3), rng.randint(1, 3), rng.choice((1.0, 2.0, 4.0)), rng)
        q = [rng.uniform(-5, 5) for _ in range(d)]
        r, c = rng.uniform(0.1, 2), 2.0
        got = idx.query(q, c, r)
        if got is not None:
            assert euclidean(q, pts[got]) <= c * r
        if not pts or min(euclidean(q, p) for p in pts) > c * r:
            assert got is None


def test_success_rate() -> None:
    rng = random.Random(6)
    n, d, r, c, w = 50, 8, 1.0, 2.0, 4.0
    k, L = parameters(n, w, r, c)
    ok = 0
    trials = 200
    for _ in range(trials):
        pts = [[rng.gauss(0, 3) for _ in range(d)] for _ in range(n)]
        direction = [rng.gauss(0, 1) for _ in range(d)]
        norm = math.sqrt(sum(x * x for x in direction))
        q = [p + 0.99 * r * x / norm for p, x in zip(pts[0], direction)]
        ok += E2LSH(pts, k, L, w, rng).query(q, c, r) is not None
    assert ok / trials >= 2 / 3 - 1 / math.e
