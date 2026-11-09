# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adadelta/. The authors are listed in prov/V8X117.jsonl.

import math
import random

from adadelta import adadelta


def test_example_trace_linear_slope() -> None:
    # f(x) = 2x, rho = 0.9, eps = 0.01: the steps start at sqrt(eps) c / sqrt((1 - rho) c^2 + eps) and grow.
    xs = adadelta(lambda t, x: [2.0], [0.0], 0.9, 8, eps=0.01)
    want = [0.0, -0.31235, -0.63271, -0.95858, -1.28873, -1.62244, -1.95923, -2.29876, -2.64078]
    for x, w in zip(xs, want):
        assert abs(x[0] - w) <= 5e-6


def test_zero_eps_never_moves() -> None:
    # With eps = 0 the numerator RMS[dx]_0 is 0, so every step is 0: eps is part of the method, not a safeguard.
    r = random.Random(1)
    xs = adadelta(lambda t, x: [r.gauss(0, 1), r.gauss(0, 100)], [0.3, -2.0], 0.95, 50, eps=0.0, eps_g=1e-8)
    assert all(x == [0.3, -2.0] for x in xs)


def test_first_step_formula() -> None:
    for seed in range(20):
        r = random.Random(seed)
        rho, eps, g = r.uniform(0.5, 0.99), 10 ** r.uniform(-8, 0), r.uniform(-50, 50)
        xs = adadelta(lambda t, x: [g], [0.0], rho, 1, eps=eps)
        assert abs(xs[1][0] - (-math.sqrt(eps) * g / math.sqrt((1 - rho) * g * g + eps))) <= 1e-12 * max(1.0, abs(g))


def test_step_bound_every_step() -> None:
    # E[g^2]_t >= (1 - rho) g_t^2, so |dx_t| <= lr sqrt((E[dx^2]_(t-1) + eps) / (1 - rho)).
    for seed in range(10):
        r = random.Random(50 + seed)
        rho, eps, lr = r.choice([0.5, 0.9, 0.95]), 10 ** r.uniform(-6, -1), r.uniform(0.1, 2.0)
        gs = [[r.gauss(0, 10 ** r.randint(-2, 3)) for _ in range(2)] for _ in range(300)]
        xs = adadelta(lambda t, x: gs[t], [0.0, 0.0], rho, 300, eps=eps, lr=lr)
        acc = [0.0, 0.0]
        for t in range(300):
            dx = [b - a for a, b in zip(xs[t], xs[t + 1])]
            for i in range(2):
                assert abs(dx[i]) <= lr * math.sqrt((acc[i] + eps) / (1 - rho)) * (1 + 1e-9)
            acc = [rho * a + (1 - rho) * d * d for a, d in zip(acc, dx)]


def test_invariance_to_loss_and_coordinate_scaling() -> None:
    # h(y) = c f(S y). With eps_x / s_i^2 and eps_g c^2 s_i^2 the iterates satisfy y_t = S^(-1) x_t exactly.
    a = [[3.0, 1.0], [1.0, 2.0]]
    b = [1.0, -4.0]

    def grad_f(x: list[float]) -> list[float]:
        return [sum(a[i][j] * x[j] for j in range(2)) - b[i] + 0.5 * math.tanh(x[i]) for i in range(2)]

    # c and s are powers of 2, so every scaling is exact in floating point and the identity holds to the bit.
    # With other scales it still holds in exact arithmetic, but rounding errors grow along the oscillating path.
    for seed in range(10):
        r = random.Random(seed)
        c, s = 2.0 ** r.randint(-10, 10), [2.0 ** r.randint(-10, 10) for _ in range(2)]
        ex, eg = [10 ** r.uniform(-6, -2) for _ in range(2)], [10 ** r.uniform(-6, -2) for _ in range(2)]
        xs = adadelta(lambda t, x: grad_f(x), [1.0, 1.0], 0.9, 200, eps=ex, eps_g=eg)

        def grad_h(t: int, y: list[float]) -> list[float]:
            g = grad_f([si * yi for si, yi in zip(s, y)])
            return [c * si * gi for si, gi in zip(s, g)]

        ys = adadelta(
            grad_h, [1.0 / si for si in s], 0.9, 200,
            eps=[e / si**2 for e, si in zip(ex, s)], eps_g=[e * c * c * si**2 for e, si in zip(eg, s)],
        )
        for x, y in zip(xs, ys):
            assert all(abs(si * yi - xi) <= 1e-12 * max(1.0, abs(xi)) for si, yi, xi in zip(s, y, x))


def test_constant_gradient_growth_and_limit() -> None:
    rho, eps, c = 0.9, 0.01, 2.0
    # eps_g = 0: |dx_t| >= sqrt(eps (1 + (1 - rho)(t - 1))), so the step grows without bound on a slope.
    xs = adadelta(lambda t, x: [c], [0.0], rho, 2000, eps=eps, eps_g=0.0)
    for t in range(1, 2001):
        assert abs(xs[t][0] - xs[t - 1][0]) >= math.sqrt(eps * (1 + (1 - rho) * (t - 1))) * (1 - 1e-12)
    # One eps in both roots (Zeiler's form): the step tends to |c|, as for gradient descent with step 1.
    xs = adadelta(lambda t, x: [c], [0.0], rho, 100000, eps=eps)
    assert abs(abs(xs[-1][0] - xs[-2][0]) - abs(c)) <= 1e-6


def test_zero_iterations() -> None:
    assert adadelta(lambda t, x: x, [1.0], 0.9, 0) == [[1.0]]
