# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backstepping/. The authors are listed in prov/W1XYZE.jsonl.

import math
import random
from fractions import Fraction

import ctlsim
from backstepping import (
    Dual,
    backstepping,
    closed_loop,
    eps_part,
    lyapunov,
    new_tag,
    real_part,
    sin,
    virtual_controls,
)

# Simulations: classical RK4 (ctlsim), step DT = 0.01, feedback evaluated
# inside the right side. Tolerances are stated at each check.
DT = 0.01


def steps(T):
    n = round(T / DT)
    assert abs(n * DT - T) < 1e-12
    return n


def page_system():
    # x1' = x1^2 + x2, x2' = u, c = (1, 1).
    f = [lambda xb: xb[0] ** 2, lambda xb: 0]
    g = [lambda xb: 1, lambda xb: 1]
    return f, g, [1, 1]


def vdot_along_closed_loop(f, g, c, x):
    """V' at x along the closed loop, by one more dual direction (exact)."""
    F = closed_loop(f, g, c)
    v = F(0, x)
    t = new_tag()
    xd = [Dual(t, xi, vi) for xi, vi in zip(x, v)]
    _, z = backstepping(f, g, c, xd)
    zr = [real_part(zi, t) for zi in z]
    zd = [eps_part(zi, t) for zi in z]
    return sum(a * b for a, b in zip(zr, zd)), zr


def random_rational(rng, lo=-3, hi=3):
    return Fraction(rng.randint(lo * 12, hi * 12), rng.randint(1, 12))


def random_strict_feedback(rng, n):
    """Random polynomial f_i and g_i = k_i + x_1^2 with k_i > 0."""
    f, g = [], []
    for i in range(n):
        coef = [Fraction(rng.randint(-3, 3)) for _ in range(i + 1)]
        quad = [Fraction(rng.randint(-2, 2)) for _ in range(i + 1)]
        mix = Fraction(rng.randint(-2, 2))
        k = Fraction(rng.randint(1, 3))

        def fi(xb, coef=coef, quad=quad, mix=mix):
            s = 0
            for a, q, xj in zip(coef, quad, xb):
                s = s + a * xj + q * xj * xj
            return s + mix * xb[0] * xb[-1]

        def gi(xb, k=k):
            return k + xb[0] * xb[0]

        f.append(fi)
        g.append(gi)
    return f, g


def test_page_closed_form_exact():
    f, g, c = page_system()
    rng = random.Random(1)
    for _ in range(200):
        x1, x2 = random_rational(rng), random_rational(rng)
        u, z = backstepping(f, g, c, [x1, x2])
        expected = -(x2 + x1 + x1 ** 2) - x1 - (1 + 2 * x1) * (x1 ** 2 + x2)
        assert u == expected
        assert z == [x1, x2 + x1 + x1 ** 2]
        a = virtual_controls(f, g, c, [x1, x2])
        assert a[1] == -x1 - x1 ** 2


def test_lyapunov_derivative_identity_exact():
    # V' = -sum c_i z_i^2 exactly, for random strict feedback systems.
    rng = random.Random(2)
    for n in (1, 2, 3):
        for _ in range(12):
            f, g = random_strict_feedback(rng, n)
            c = [Fraction(rng.randint(1, 4), rng.randint(1, 2)) for _ in range(n)]
            for _ in range(3):
                x = [random_rational(rng, -2, 2) for _ in range(n)]
                vdot, z = vdot_along_closed_loop(f, g, c, x)
                assert vdot == -sum(ci * zi * zi for ci, zi in zip(c, z))


def test_linear_chain_gain():
    # x1' = x2, x2' = u: u = -(1 + c1 c2) x1 - (c1 + c2) x2.
    f = [lambda xb: 0, lambda xb: 0]
    g = [lambda xb: 1, lambda xb: 1]
    rng = random.Random(4)
    for _ in range(50):
        c1, c2 = Fraction(rng.randint(1, 9), 3), Fraction(rng.randint(1, 9), 3)
        x = [random_rational(rng), random_rational(rng)]
        u, _ = backstepping(f, g, [c1, c2], x)
        assert u == -(1 + c1 * c2) * x[0] - (c1 + c2) * x[1]


def charpoly3(M):
    tr = M[0][0] + M[1][1] + M[2][2]
    minors = sum(M[i][i] * M[j][j] - M[i][j] * M[j][i] for i, j in ((0, 1), (0, 2), (1, 2)))
    det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
           - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
           + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    return [1, -tr, minors, -det]


def test_triple_integrator_poles_match_error_system():
    # For a chain of 3 integrators the closed loop is x' = (A - B K) x, which
    # is similar to the error system z' = M z (g_i = 1).
    f = [lambda xb: 0] * 3
    g = [lambda xb: 1] * 3
    c = [Fraction(1), Fraction(2), Fraction(3)]
    K = [-backstepping(f, g, c, [Fraction(int(i == j)) for j in range(3)])[0] for i in range(3)]
    Acl = [[0, 1, 0], [0, 0, 1], [-K[0], -K[1], -K[2]]]
    M = [[-c[0], 1, 0], [-1, -c[1], 1], [0, -1, -c[2]]]
    assert charpoly3(Acl) == charpoly3(M)


def test_simulation_page_example():
    # z' = [[-1, 1], [-1, -1]] z, so V(t) = V(0) exp(-2 t) and
    # z(t) = exp(-t) [[cos t, sin t], [-sin t, cos t]] z(0).
    f, g, c = page_system()
    ts, xs, _ = ctlsim.simulate(closed_loop(f, g, c), [1.0, 0.0], 0.0, 8.0, DT)
    assert len(xs) == steps(8.0) + 1
    vs = [lyapunov(f, g, c, x) for x in xs]
    assert all(vs[i + 1] < vs[i] for i in range(len(vs) - 1))
    for t, x, v in zip(ts, xs, vs):
        assert abs(v - 2.5 * math.exp(-2 * t)) < 1e-8
        _, z = backstepping(f, g, c, x)
        e = math.exp(-t)
        assert abs(z[0] - e * (math.cos(t) + 2 * math.sin(t))) < 1e-8
        assert abs(z[1] - e * (-math.sin(t) + 2 * math.cos(t))) < 1e-8
    table = {1.0: (0.81789, -1.39885, 1.01803), 2.0: (0.18980, -0.46152, 0.63292)}
    for T, (x1, x2, u) in table.items():
        x = xs[steps(T)]
        assert abs(x[0] - x1) < 1e-5 and abs(x[1] - x2) < 1e-5
        assert abs(backstepping(f, g, c, x)[0] - u) < 1e-5
    assert math.hypot(*xs[-1]) < 2e-3


def test_three_states_with_sine_simulation():
    # x1' = sin(x1) + x2, x2' = x1 x2 + (2 + cos x1) x3, x3' = x2^2 + u.
    from backstepping import cos
    f = [lambda xb: sin(xb[0]), lambda xb: xb[0] * xb[1], lambda xb: xb[1] * xb[1]]
    g = [lambda xb: 1, lambda xb: 2 + cos(xb[0]), lambda xb: 1]
    c = [1.0, 1.0, 1.0]
    rng = random.Random(9)
    for _ in range(20):
        x = [rng.uniform(-1, 1) for _ in range(3)]
        vdot, z = vdot_along_closed_loop(f, g, c, x)
        target = -sum(zi * zi for zi in z)
        assert abs(vdot - target) < 1e-9 * (1 + abs(target))
    ts, xs, _ = ctlsim.simulate(closed_loop(f, g, c), [0.5, -0.5, 0.2], 0.0, 12.0, 0.02)
    vs = [lyapunov(f, g, c, x) for x in xs]
    assert all(vs[i + 1] <= vs[i] for i in range(len(vs) - 1))
    assert max(abs(v) for v in xs[-1]) < 1e-3
