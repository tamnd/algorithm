# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-boosting/. The authors are listed in prov/QJH6MQ.jsonl.

import math
import random

from gradient_boosting import gradient_boost, leaf_of, loss, mean_loss, pseudo_residual, sigmoid

EX_X = [(float(v),) for v in range(1, 7)]
EX_Y = [1.0, 3.0, 2.0, 6.0, 8.0, 4.0]


def reg_data(n: int, rng: random.Random) -> tuple[list[tuple[float, float]], list[float]]:
    xs = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(n)]
    ys = [math.sin(6 * a) + 2 * b * b + rng.gauss(0, 0.1) for a, b in xs]
    return xs, ys


def cls_data(n: int, rng: random.Random) -> tuple[list[tuple[float, float]], list[float]]:
    xs = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    ys = [1.0 if a * b + 0.3 * rng.gauss(0, 1) > 0 else 0.0 for a, b in xs]
    return xs, ys


def test_pseudo_residuals_are_negative_gradients() -> None:
    h = 1e-6
    for kind, y in (("squared", 1.7), ("logistic", 1.0), ("logistic", 0.0)):
        for f in (-2.0, -0.3, 0.0, 0.8, 3.0):
            num = -(loss(kind, y, f + h) - loss(kind, y, f - h)) / (2 * h)
            assert abs(num - pseudo_residual(kind, y, f)) < 1e-6


def test_first_tree_fits_the_residuals_squared_loss() -> None:
    xs, ys = reg_data(40, random.Random(2))
    trace: list = []
    gradient_boost(xs, ys, "squared", 1, nu=1.0, max_depth=1, trace=trace)
    mean = sum(ys) / len(ys)
    r = trace[0]["residuals"]
    assert all(abs(ri - (y - mean)) < 1e-12 for ri, y in zip(r, ys))
    # The stump is the least squares stump of the residuals: compare with brute force.
    left, right = trace[0]["leaves"]
    sse = lambda ids: sum((r[i] - sum(r[j] for j in ids) / len(ids)) ** 2 for i in ids)
    got = sse(left) + sse(right)
    best = math.inf
    for f in range(2):
        for t in sorted(set(x[f] for x in xs))[:-1]:
            a = [i for i in range(len(xs)) if xs[i][f] <= t]
            b = [i for i in range(len(xs)) if xs[i][f] > t]
            best = min(best, sse(a) + sse(b))
    assert abs(got - best) < 1e-9
    for ids, v in zip(trace[0]["leaves"], trace[0]["values"]):
        assert abs(v - sum(r[i] for i in ids) / len(ids)) < 1e-12


def test_deep_first_tree_interpolates_with_nu_one() -> None:
    xs, ys = reg_data(30, random.Random(4))
    model = gradient_boost(xs, ys, "squared", 1, nu=1.0, max_depth=30)
    assert all(abs(model.score(x) - y) < 1e-9 for x, y in zip(xs, ys))


def test_squared_loss_never_increases_for_nu_below_two() -> None:
    xs, ys = reg_data(50, random.Random(6))
    for nu in (0.05, 0.3, 1.0, 1.9):
        trace: list = []
        gradient_boost(xs, ys, "squared", 30, nu=nu, max_depth=2, trace=trace)
        prev = mean_loss("squared", ys, [sum(ys) / len(ys)] * len(ys))
        for t in trace:
            assert t["loss"] <= prev + 1e-12
            prev = t["loss"]


def test_logistic_newton_leaf_and_monotone_loss() -> None:
    xs, ys = cls_data(60, random.Random(8))
    trace: list = []
    model = gradient_boost(xs, ys, "logistic", 40, nu=0.1, max_depth=2, trace=trace)
    p = sum(ys) / len(ys)
    assert abs(sigmoid(model.f0) - p) < 1e-12
    prev = mean_loss("logistic", ys, [model.f0] * len(ys))
    for t in trace:
        assert t["loss"] < prev  # observed for nu = 0.1 on this data; the proof covers nu <= 8 H_j / n_j
        prev = t["loss"]


def test_logistic_sufficient_step_condition() -> None:
    # Proven: in a leaf with Newton value G/H, a step nu <= 8 H / n_leaf does not increase the leaf loss.
    xs, ys = cls_data(50, random.Random(9))
    trace: list = []
    model = gradient_boost(xs, ys, "logistic", 1, nu=1.0, max_depth=2, trace=trace)
    f0 = model.f0
    for ids, v in zip(trace[0]["leaves"], trace[0]["values"]):
        hsum = len(ids) * sigmoid(f0) * (1 - sigmoid(f0))
        for nu in (8 * hsum / len(ids), 4 * hsum / len(ids), 0.01):
            before = sum(loss("logistic", ys[i], f0) for i in ids)
            after = sum(loss("logistic", ys[i], f0 + nu * v) for i in ids)
            assert after <= before + 1e-12


def test_subsample_uses_only_the_drawn_examples() -> None:
    xs, ys = reg_data(40, random.Random(10))
    trace: list = []
    gradient_boost(xs, ys, "squared", 5, nu=0.5, max_depth=2, subsample=0.5, rng=random.Random(11), trace=trace)
    for t in trace:
        assert len(t["ids"]) == 20 and len(set(t["ids"])) == 20
        assert sorted(i for leaf in t["leaves"] for i in leaf) == t["ids"]


def test_worked_example() -> None:
    trace: list = []
    model = gradient_boost(EX_X, EX_Y, "squared", 3, nu=0.5, max_depth=1, trace=trace)
    assert model.f0 == 4.0
    assert trace[0]["residuals"] == [-3.0, -1.0, -2.0, 2.0, 4.0, 0.0]
    assert [sorted(l) for l in trace[0]["leaves"]] == [[0, 1, 2], [3, 4, 5]]
    assert trace[0]["values"] == [-2.0, 2.0]
    assert trace[1]["residuals"] == [-2.0, 0.0, -1.0, 1.0, 3.0, -1.0]
    assert [sorted(l) for l in trace[2]["leaves"]] == [[0], [1, 2, 3, 4, 5]]
    assert [round(v, 10) for v in trace[2]["values"]] == [-1.5, 0.3]
    assert [round(t["loss"], 4) for t in trace] == [1.3333, 0.9583, 0.7896]
    assert [round(model.score(x), 10) for x in EX_X] == [1.75, 2.65, 2.65, 5.65, 5.65, 5.65]
    assert leaf_of(model.trees[0][0], (3.5,)) == 0
