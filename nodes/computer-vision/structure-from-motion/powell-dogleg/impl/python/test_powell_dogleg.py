# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/powell-dogleg/. The authors are listed in prov/GQ5JQ6.jsonl.

import math
import random

from powell_dogleg import cost, dogleg_step, powell_dogleg

T = [0.0, 1.0, 2.0, 3.0]
Y = [2.0 * math.exp(-0.5 * t) for t in T]


def exp_r(x):
    return [x[0] * math.exp(x[1] * t) - y for t, y in zip(T, Y)]


def exp_j(x):
    return [[math.exp(x[1] * t), x[0] * t * math.exp(x[1] * t)] for t in T]


def rosen_r(x):
    return [10.0 * (x[1] - x[0] ** 2), 1.0 - x[0]]


def rosen_j(x):
    return [[-20.0 * x[0], 10.0], [-1.0, 0.0]]


def model(jac, r, h):
    jh = [sum(a * b for a, b in zip(row, h)) for row in jac]
    return cost([ri + v for ri, v in zip(r, jh)])


def test_worked_example_steps():
    jac, r = rosen_j([-1.2, 1.0]), rosen_r([-1.2, 1.0])
    h, kind = dogleg_step(jac, r, 6.0)
    assert kind == "gauss-newton" and abs(h[0] - 2.2) < 1e-12 and abs(h[1] + 4.84) < 1e-12
    h, kind = dogleg_step(jac, r, 1.0)
    assert kind == "dogleg" and abs(math.hypot(*h) - 1.0) < 1e-12
    assert abs(h[0] - 0.5372) < 1e-4 and abs(h[1] + 0.8434) < 1e-4
    h, kind = dogleg_step(jac, r, 0.1)
    assert kind == "steepest" and abs(math.hypot(*h) - 0.1) < 1e-12


def test_step_properties_on_random_models():
    rng = random.Random(23)
    for _ in range(200):
        m, n = rng.randint(3, 6), rng.randint(1, 3)
        jac = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        r = [rng.gauss(0, 1) for _ in range(m)]
        delta = 10 ** rng.uniform(-2, 1)
        h, kind = dogleg_step(jac, r, delta)
        nh = math.sqrt(sum(v * v for v in h))
        assert nh <= delta * (1 + 1e-12)
        g = [sum(jac[k][i] * r[k] for k in range(m)) for i in range(n)]
        ng = math.sqrt(sum(v * v for v in g))
        jg = [sum(a * b for a, b in zip(row, g)) for row in jac]
        # the Cauchy point: the model minimizer along -g inside the region
        t = min(delta / ng, ng * ng / sum(v * v for v in jg))
        cauchy = model(jac, r, [-t * v for v in g])
        assert model(jac, r, h) <= cauchy + 1e-10
        assert model(jac, r, h) <= cost(r) + 1e-12
        if kind != "gauss-newton":
            assert abs(nh - delta) < 1e-9 * max(1.0, delta)


def test_model_decreases_along_the_dog_leg_path():
    rng = random.Random(29)
    for _ in range(50):
        jac = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(4)]
        r = [rng.gauss(0, 1) for _ in range(4)]
        last_len, last_val = -1.0, float("inf")
        for delta in [0.01 * 1.3 ** i for i in range(30)]:
            h, _ = dogleg_step(jac, r, delta)
            nh = math.sqrt(sum(v * v for v in h))
            val = model(jac, r, h)
            assert nh >= last_len - 1e-12 and val <= last_val + 1e-12
            last_len, last_val = nh, val


def test_rosenbrock_converges_with_decreasing_cost():
    x, info = powell_dogleg(rosen_r, rosen_j, [-1.2, 1.0], delta0=1.0)
    assert abs(x[0] - 1.0) < 1e-8 and abs(x[1] - 1.0) < 1e-8
    costs = info["costs"]
    assert all(c1 < c0 for c0, c1 in zip(costs, costs[1:]))
    for kind, nh, delta in info["steps"]:
        assert nh <= delta * (1 + 1e-12)


def test_zero_residual_exact_recovery():
    x, _ = powell_dogleg(exp_r, exp_j, [1.0, 0.0], delta0=0.5)
    assert abs(x[0] - 2.0) < 1e-8 and abs(x[1] + 0.5) < 1e-8


def test_converges_where_gauss_newton_fails():
    lam = -2.0
    r = lambda x: [x[0] + 1.0, lam * x[0] ** 2 + x[0] - 1.0]
    j = lambda x: [[1.0], [2.0 * lam * x[0] + 1.0]]
    x, info = powell_dogleg(r, j, [0.1], delta0=1.0, max_iter=400)
    assert abs(x[0]) < 1e-6
    costs = info["costs"]
    assert all(c1 < c0 for c0, c1 in zip(costs, costs[1:]))
