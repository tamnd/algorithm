# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-normalization/. The authors are listed in prov/88JWRJ.jsonl.

import math
import random
from fractions import Fraction as F

from weight_normalization import (data_dependent_init, dot, logistic_grad, logistic_loss, norm, train_unit,
                                  weight, wn_grads, wn_grads_exact)


def toy(rng: random.Random, n: int = 40, d: int = 3):
    w_true = [1.5, -2.0, 0.5]
    xs = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n)]
    ys = [1 if dot(w_true, x) + 0.3 * rng.gauss(0.0, 1.0) > 0 else 0 for x in xs]
    return xs, ys


def test_weight_has_norm_g_and_direction_v() -> None:
    w = weight([3.0, 4.0], 2.0)
    assert w == [1.2, 1.6]
    assert math.isclose(norm(weight([1.0, -7.0, 2.0], 0.3)), 0.3)


def test_hand_example_exactly() -> None:
    v, g, gw = [F(3), F(4)], F(2), [F(1), F(0)]
    gg, gv = wn_grads_exact(v, g, gw, F(5))
    assert gg == F(3, 5)
    assert gv == [F(32, 125), F(-24, 125)]
    assert gv[0] * v[0] + gv[1] * v[1] == 0
    v2 = [a - b for a, b in zip(v, gv)]
    assert sum(x * x for x in v2) == 25 + sum(x * x for x in gv)


def test_gradient_wrt_v_is_orthogonal_to_v() -> None:
    rng = random.Random(0)
    for _ in range(20):
        d = rng.randint(2, 6)
        v = [rng.gauss(0.0, 1.0) for _ in range(d)]
        gw = [rng.gauss(0.0, 1.0) for _ in range(d)]
        _, gv = wn_grads(v, rng.uniform(-3.0, 3.0), gw)
        assert abs(dot(gv, v)) < 1e-12 * (1 + norm(gv) * norm(v))


def test_gradients_match_central_differences() -> None:
    xs, ys = toy(random.Random(1))
    v, g, b = [0.4, -1.1, 0.7], 1.7, 0.2
    gw, _ = logistic_grad(weight(v, g), b, xs, ys)
    gg, gv = wn_grads(v, g, gw)
    f = lambda vv, gg_: logistic_loss(weight(vv, gg_), b, xs, ys)
    h = 1e-6
    assert abs((f(v, g + h) - f(v, g - h)) / (2 * h) - gg) < 1e-8
    for j in range(3):
        vp, vm = v[:], v[:]
        vp[j] += h
        vm[j] -= h
        assert abs((f(vp, g) - f(vm, g)) / (2 * h) - gv[j]) < 1e-8


def test_scaling_v_keeps_w_and_divides_the_gradient() -> None:
    v, g, gw = [0.4, -1.1, 0.7], 1.7, [0.3, 0.2, -0.5]
    _, gv = wn_grads(v, g, gw)
    _, gv5 = wn_grads([5 * x for x in v], g, gw)
    assert all(math.isclose(a, b) for a, b in zip(weight(v, g), weight([5 * x for x in v], g)))
    assert all(math.isclose(a, 5 * b) for a, b in zip(gv, gv5))


def test_norm_of_v_grows_under_gradient_descent() -> None:
    xs, ys = toy(random.Random(2))
    v, g = [0.4, -1.1, 0.7], 1.0
    for _ in range(50):
        gw, _ = logistic_grad(weight(v, g), 0.0, xs, ys)
        gg, gv = wn_grads(v, g, gw)
        new = [a - 0.5 * c for a, c in zip(v, gv)]
        assert math.isclose(dot(new, new), dot(v, v) + 0.25 * dot(gv, gv), rel_tol=1e-12)
        assert dot(new, new) >= dot(v, v)
        v, g = new, g - 0.5 * gg


def test_data_dependent_init_standardizes_preactivations() -> None:
    xs, _ = toy(random.Random(3))
    v = [0.3, 0.1, -0.2]
    g, b = data_dependent_init(v, xs)
    pre = [dot(weight(v, g), x) + b for x in xs]
    mu = sum(pre) / len(pre)
    var = sum((p - mu) ** 2 for p in pre) / len(pre)
    assert abs(mu) < 1e-12 and math.isclose(var, 1.0, rel_tol=1e-12)


def test_training_lowers_the_loss() -> None:
    xs, ys = toy(random.Random(4))
    losses = train_unit(xs, ys, 300, 0.5, random.Random(5))
    assert losses[-1] < 0.5 * losses[0]
