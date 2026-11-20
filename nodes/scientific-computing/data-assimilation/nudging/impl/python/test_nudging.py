# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nudging/. The authors are listed in prov/A44WD4.jsonl.

import math
import random

from nudging import gain, lorenz96, nudge, rk4_step, time_interpolant

N, F, DT = 40, 8.0, 0.01


def rmse(a, b):
    return math.sqrt(sum((u - v) ** 2 for u, v in zip(a, b)) / len(a))


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def lorenz96_truth(steps, seed=1):
    f = lorenz96(F)
    x = [F + (0.01 if j == 0 else 0.0) for j in range(N)]
    for _ in range(1000):  # spin-up onto the attractor
        x = rk4_step(lambda t, z: f(z), 0.0, x, DT)
    truth = [x]
    for _ in range(steps):
        truth.append(rk4_step(lambda t, z: f(z), 0.0, truth[-1], DT))
    rng = random.Random(seed)
    x0 = [v + rng.gauss(0, 3) for v in truth[0]]
    return f, truth, [k * DT for k in range(steps + 1)], x0


def test_scalar_linear_exact_solution():
    # dx/dt = -a x + g (y - x) with a constant y.
    a, g, y, x0, dt = 0.7, 2.5, 3.0, -1.0, 0.01
    path = nudge(lambda x: [-a * x[0]], [x0], [[1.0]], [[g]], lambda t: [y], dt, 300)
    xe = g * y / (a + g)
    for k in (0, 50, 300):
        exact = xe + (x0 - xe) * math.exp(-(a + g) * k * dt)
        assert abs(path[k][0] - exact) < 1e-7  # RK4 error for (a + g) dt = 0.032


def test_zero_gain_is_the_free_run():
    f, truth, times, x0 = lorenz96_truth(50)
    G = [[0.0] * N for _ in range(N)]
    path = nudge(f, x0, identity(N), G, time_interpolant(times, truth), DT, 50)
    free = [list(map(float, x0))]
    for _ in range(50):
        free.append(rk4_step(lambda t, z: f(z), 0.0, free[-1], DT))
    assert path == free


def test_rotation_error_decays_at_rate_g():
    # f(x) = A x with A skew-symmetric; truth is a rotation, observed exactly.
    g, dt = 1.5, 0.01
    f = lambda x: [x[1], -x[0]]
    truth = lambda t: [math.cos(t), -math.sin(t)]
    x0 = [3.0, 2.0]
    path = nudge(f, x0, identity(2), gain(identity(2), g), truth, dt, 400)
    e0 = math.hypot(x0[0] - 1.0, x0[1])
    for k in (100, 200, 400):
        xt = truth(k * dt)
        e = math.hypot(path[k][0] - xt[0], path[k][1] - xt[1])
        assert abs(e - math.exp(-g * k * dt) * e0) < 1e-8


def test_error_bound_for_large_gain():
    # Theorem: with H = I and G = g I, |e(t)| <= exp((4M - 1 - g) t) |e(0)| for M = max |x^t_j|.
    steps = 300
    f, truth, times, x0 = lorenz96_truth(steps)
    M = max(max(abs(v) for v in s) for s in truth)
    g = 4 * M
    path = nudge(f, x0, identity(N), gain(identity(N), g), time_interpolant(times, truth), DT, steps)
    e0 = math.sqrt(sum((a - b) ** 2 for a, b in zip(path[0], truth[0])))
    for k in range(0, steps + 1, 10):
        e = math.sqrt(sum((a - b) ** 2 for a, b in zip(path[k], truth[k])))
        assert e <= math.exp((4 * M - 1 - g) * k * DT) * e0 + 1e-4


def test_error_identity_bound():
    # e^T (f(x^t + e) - f(x^t)) <= (4 max|x^t_j| - 1) |e|^2 for Lorenz-96.
    rng = random.Random(5)
    f = lorenz96(F)
    for _ in range(300):
        n = rng.randint(4, 12)
        xt = [rng.uniform(-10, 10) for _ in range(n)]
        e = [rng.uniform(-10, 10) for _ in range(n)]
        lhs = sum(ei * (a - b) for ei, a, b in zip(e, f([u + v for u, v in zip(xt, e)]), f(xt)))
        rhs = (4 * max(abs(v) for v in xt) - 1) * sum(v * v for v in e)
        assert lhs <= rhs + 1e-9


def test_lorenz96_synchronizes_with_full_observations():
    steps = 500
    f, truth, times, x0 = lorenz96_truth(steps)
    y = time_interpolant(times, truth)
    path = nudge(f, x0, identity(N), gain(identity(N), 5.0), y, DT, steps)
    assert rmse(path[0], truth[0]) > 2.0
    assert rmse(path[steps], truth[steps]) < 5e-3
    free = nudge(f, x0, identity(N), gain(identity(N), 0.0), y, DT, steps)
    assert rmse(free[steps], truth[steps]) > 1.0


def test_noisy_observations_error_below_observation_error():
    steps, sigma = 1500, 1.0
    f, truth, times, x0 = lorenz96_truth(steps)
    rng = random.Random(7)
    otimes = times[::5]
    ovals = [[v + rng.gauss(0, sigma) for v in truth[5 * i]] for i in range(len(otimes))]
    path = nudge(f, x0, identity(N), gain(identity(N), 5.0), time_interpolant(otimes, ovals), DT, steps)
    e = [rmse(path[k], truth[k]) for k in range(500, steps + 1)]
    assert sum(e) / len(e) < 0.6 * sigma


def test_time_interpolant():
    y = time_interpolant([0.0, 0.5, 1.0], [[0.0, 1.0], [1.0, 1.0], [3.0, 0.0]])
    assert y(-1.0) == [0.0, 1.0]
    assert y(0.25) == [0.5, 1.0]
    assert y(0.75) == [2.0, 0.5]
    assert y(2.0) == [3.0, 0.0]
