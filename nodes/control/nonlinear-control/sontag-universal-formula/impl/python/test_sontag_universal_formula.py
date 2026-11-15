# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sontag-universal-formula/. The authors are listed in prov/B75HKW.jsonl.

import math
import random

import ctlsim
from sontag_universal_formula import closed_loop, sontag_feedback, sontag_gain

# Simulations: classical RK4 (ctlsim), step dt = 0.01, feedback evaluated
# inside the right side. Tolerances are stated at each check.
DT = 0.01


def steps(T):
    n = round(T / DT)
    assert abs(n * DT - T) < 1e-12
    return n


def scalar_system(c, d):
    return (lambda x: [c * x[0]]), (lambda x: [[d]]), (lambda x: [x[0]])


def page_system():
    def f(x):
        return [-x[0] + x[0] * x[0] * x[1], 0.0]

    def g(x):
        return [[0.0], [1.0]]

    def grad_V(x):
        return [x[0], x[1]]

    return f, g, grad_V


def test_check_value_scalar():
    # x' = x + u, V = x^2 / 2: a = x^2, b = x, u = -(1 + sqrt 2) x.
    f, g, gv = scalar_system(1.0, 1.0)
    k = sontag_feedback(f, g, gv)
    for x in [-3.0, -0.5, 0.25, 1.0, 7.0]:
        assert abs(k([x])[0] + (1 + math.sqrt(2)) * x) < 1e-12 * max(1.0, abs(x))
    assert k([0.0]) == [0.0]
    # Closed loop x' = -sqrt(2) x, so x(2) = exp(-2 sqrt 2).
    _, xs, _ = ctlsim.simulate(closed_loop(f, g, gv), [1.0], 0.0, 2.0, DT)
    assert len(xs) == steps(2.0) + 1
    assert abs(xs[-1][0] - math.exp(-2 * math.sqrt(2))) < 1e-9


def test_scalar_gain_equals_lq_gain():
    # x' = c x + u with V = x^2 / 2 gives u = -(c + sqrt(c^2 + 1)) x, the
    # gain of the scalar CARE with q = r = 1 (P = c + sqrt(c^2 + 1)).
    rng = random.Random(11)
    for _ in range(50):
        c = rng.uniform(-5, 5)
        x = rng.uniform(-4, 4)
        if abs(x) < 1e-3:
            continue
        f, g, gv = scalar_system(c, 1.0)
        u = sontag_feedback(f, g, gv)([x])[0]
        P = c + math.sqrt(c * c + 1)
        assert abs(P * P - 2 * c * P - 1) < 1e-9 * (1 + P * P)
        assert abs(u + P * x) < 1e-9 * (1 + abs(P * x))


def test_derivative_identity_and_quadratic():
    # a + b.u = -sqrt(a^2 + |b|^4) and beta phi^2 - 2 a phi - beta = 0.
    rng = random.Random(7)
    for _ in range(2000):
        m = rng.randint(1, 3)
        a = rng.choice([-1, 1]) * 10 ** rng.uniform(-6, 3)
        b = [rng.choice([-1, 1]) * 10 ** rng.uniform(-3, 2) for _ in range(m)]
        u = sontag_gain(a, b)
        beta = sum(bj * bj for bj in b)
        s = math.sqrt(a * a + beta * beta)
        vdot = a + sum(bj * uj for bj, uj in zip(b, u))
        assert abs(vdot + s) <= 1e-12 * (abs(a) + s) * 10
        phi = -u[0] / b[0]
        assert phi > 0
        assert abs(beta * phi * phi - 2 * a * phi - beta) <= 1e-10 * (beta * phi * phi + abs(a) * phi + beta)


def test_zero_b_gives_zero_input():
    assert sontag_gain(-2.0, [0.0, 0.0]) == [0.0, 0.0]
    assert sontag_gain(0.0, [0.0]) == [0.0]


def test_stable_form_when_a_negative():
    # The naive (a + sqrt(a^2 + beta^2)) / beta returns 0 here in floating
    # point. The true value is beta / (1 + sqrt(1 + beta^2)), about 5e-9.
    a, beta = -1.0, 1e-8
    naive = (a + math.sqrt(a * a + beta * beta)) / beta
    assert naive == 0.0
    u = sontag_gain(a, [math.sqrt(beta)])
    phi = -u[0] / math.sqrt(beta)
    exact = beta / (1 + math.sqrt(1 + beta * beta))
    assert abs(phi - exact) < 1e-12 * exact


def test_page_example_trace():
    f, g, gv = page_system()
    k = sontag_feedback(f, g, gv)
    assert abs(k([2.0, 1.0])[0] + (4 + math.sqrt(17))) < 1e-12
    _, xs, _ = ctlsim.simulate(closed_loop(f, g, gv), [2.0, 1.0], 0.0, 10.0, DT)
    V = [(x[0] ** 2 + x[1] ** 2) / 2 for x in xs]
    assert all(V[i + 1] < V[i] for i in range(len(V) - 1))
    table = {1.0: (1.84232, 0.40220), 2.0: (1.23857, 0.37134), 4.0: (0.26436, 0.25125), 6.0: (0.03733, 0.07237)}
    for T, (x1, x2) in table.items():
        x = xs[steps(T)]
        assert abs(x[0] - x1) < 1e-5 and abs(x[1] - x2) < 1e-5
    assert math.hypot(*xs[-1]) < 3e-3


def test_small_control_property_on_page_example():
    # For |x| <= 0.5, x1 x2 < 1, so a <= 0 and |k(x)| <= |b| = |x2| <= |x|.
    f, g, gv = page_system()
    k = sontag_feedback(f, g, gv)
    rng = random.Random(3)
    for _ in range(2000):
        r = 0.5 * rng.random()
        t = rng.uniform(0, 2 * math.pi)
        x = [r * math.cos(t), r * math.sin(t)]
        assert abs(k(x)[0]) <= abs(x[1]) + 1e-15


def test_no_small_control_property_gives_unbounded_feedback():
    # x' = x + x^2 u, V = x^2 / 2: u = -(1 + sqrt(1 + x^8)) / x.
    k = sontag_feedback(lambda x: [x[0]], lambda x: [[x[0] ** 2]], lambda x: [x[0]])
    for x in [1.0, 0.1, 0.01, 1e-3]:
        u = k([x])[0]
        assert abs(u + (1 + math.sqrt(1 + x ** 8)) / x) < 1e-9 * abs(u)
        assert abs(u) >= 2 / x * (1 - 1e-12)


def test_double_integrator_with_lq_lyapunov_function():
    # V = x^T P x with the LQR solution P = [[sqrt 3, 1], [1, sqrt 3]].
    r3 = math.sqrt(3)
    P = [[r3, 1.0], [1.0, r3]]

    def V(x):
        return sum(x[i] * P[i][j] * x[j] for i in range(2) for j in range(2))

    f = lambda x: [x[1], 0.0]
    g = lambda x: [[0.0], [1.0]]
    gv = lambda x: [2 * (P[0][0] * x[0] + P[0][1] * x[1]), 2 * (P[1][0] * x[0] + P[1][1] * x[1])]
    _, xs, _ = ctlsim.simulate(closed_loop(f, g, gv), [1.0, 0.0], 0.0, 15.0, DT)
    vs = [V(x) for x in xs]
    assert all(vs[i + 1] < vs[i] for i in range(len(vs) - 1))
    assert math.hypot(*xs[-1]) < 1e-3


def test_two_inputs():
    # x' = u with u in R^2 and V = |x|^2 / 2: a = 0, b = x, u = -x.
    k = sontag_feedback(lambda x: [0.0, 0.0], lambda x: [[1.0, 0.0], [0.0, 1.0]], lambda x: list(x))
    rng = random.Random(5)
    for _ in range(100):
        x = [rng.uniform(-2, 2), rng.uniform(-2, 2)]
        u = k(x)
        assert abs(u[0] + x[0]) < 1e-12 and abs(u[1] + x[1]) < 1e-12
