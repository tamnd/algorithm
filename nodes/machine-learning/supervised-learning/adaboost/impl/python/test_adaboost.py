# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaboost/. The authors are listed in prov/F7R3H9.jsonl.

import math
import random

from adaboost import adaboost, best_stump, predict, stump_predict, thresholds, vote, weighted_error

EXAMPLE_X = [(float(v),) for v in range(1, 11)]
EXAMPLE_Y = [1, 1, -1, -1, -1, 1, 1, 1, -1, -1]


def circle_data(n: int, rng: random.Random) -> tuple[list[tuple[float, float]], list[int]]:
    xs = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    ys = [1 if a * a + b * b < 0.5 else -1 for a, b in xs]
    return xs, ys


def test_best_stump_is_optimal() -> None:
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randrange(2, 12)
        xs = [(float(rng.randrange(5)), float(rng.randrange(5))) for _ in range(n)]
        ys = [rng.choice((-1, 1)) for _ in range(n)]
        w = [rng.random() for _ in range(n)]
        s, e = best_stump(xs, ys, w)
        assert abs(weighted_error(s, xs, ys, w) - e) < 1e-9
        brute = min(weighted_error((f, t, g), xs, ys, w) for f in range(2) for t in thresholds(xs, f) for g in (-1, 1))
        assert abs(e - brute) < 1e-9
        assert e <= sum(w) / 2 + 1e-9


def test_training_error_below_bound_every_round() -> None:
    xs, ys = circle_data(150, random.Random(1))
    _, hist, _ = adaboost(xs, ys, 120)
    assert len(hist) == 120
    for r in hist:
        assert abs(r.z - 2 * math.sqrt(r.eps * (1 - r.eps))) < 1e-9
        assert r.train_error <= r.prod_z + 1e-12
        assert r.prod_z <= r.exp_bound + 1e-12


def test_product_of_z_is_mean_exponential_loss() -> None:
    xs, ys = circle_data(100, random.Random(5))
    model, hist, _ = adaboost(xs, ys, 30)
    mean_exp = sum(math.exp(-y * vote(model, x)) for x, y in zip(xs, ys)) / len(xs)
    assert abs(mean_exp - hist[-1].prod_z) < 1e-9


def test_last_stump_has_error_one_half_after_update() -> None:
    xs, ys = circle_data(80, random.Random(7))
    model, hist, dists = adaboost(xs, ys, 25)
    for t, (_, s) in enumerate(model):
        assert abs(weighted_error(s, xs, ys, dists[t + 1]) - 0.5) < 1e-9
        assert abs(sum(dists[t + 1]) - 1) < 1e-9


def test_alpha_minimizes_z() -> None:
    for eps in (0.05, 0.2, 0.37, 0.49):
        alpha = 0.5 * math.log((1 - eps) / eps)
        z = lambda a: (1 - eps) * math.exp(-a) + eps * math.exp(a)
        lo, hi = 0.0, 5.0
        for _ in range(200):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            lo, hi = (lo, m2) if z(m1) < z(m2) else (m1, hi)
        assert abs(lo - alpha) < 1e-6
        assert abs(z(alpha) - 2 * math.sqrt(eps * (1 - eps))) < 1e-12


def test_example_trace() -> None:
    model, hist, _ = adaboost(EXAMPLE_X, EXAMPLE_Y, 3)
    assert [r.stump for r in hist] == [(0, 2.5, -1), (0, 8.5, -1), (0, 5.5, 1)]
    assert [abs(r.eps - e) < 1e-12 for r, e in zip(hist, (3 / 10, 3 / 14, 2 / 11))] == [True] * 3
    assert [r.train_error for r in hist] == [0.3, 0.3, 0.0]
    assert [round(r.prod_z, 4) for r in hist] == [0.9165, 0.7521, 0.5802]
    assert all(predict(model, x) == y for x, y in zip(EXAMPLE_X, EXAMPLE_Y))


def test_perfect_stump_and_no_edge() -> None:
    xs = [(0.0,), (1.0,), (2.0,), (3.0,)]
    model, hist, _ = adaboost(xs, [-1, -1, 1, 1], 5)
    assert len(hist) == 1 and model == [(1.0, (0, 1.5, 1))]
    model, hist, _ = adaboost([(0.0,), (0.0,)], [1, -1], 5)
    assert hist == [] and model == []
    assert stump_predict((0, 1.5, 1), (2.0,)) == 1
