# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/input-output-linearization/. The authors are listed in prov/VH21RF.jsonl.

import math
import random
from fractions import Fraction

import pytest

import ctlsim
from input_output_linearization import (
    Poly,
    closed_loop,
    io_linearize,
    lie_bracket,
    lie_derivative,
    tracking_control,
    variables,
)


def page_system():
    x1, x2, x3 = variables(3)
    zero = Poly(3)
    f = [x2, x1 * x3 - x2 ** 3, -x3 + x1 ** 2]
    g = [zero, 1 + x1 ** 2, zero]
    return f, g, x1


def random_poly(rng, n, terms=4, deg=3):
    t = {}
    for _ in range(terms):
        e = [0] * n
        for _ in range(rng.randint(0, deg)):
            e[rng.randrange(n)] += 1
        t[tuple(e)] = Fraction(rng.randint(-5, 5), rng.randint(1, 3))
    return Poly(n, t)


def linear_field(A):
    n = len(A)
    xs = variables(n)
    return [sum((Poly.const(n, A[i][j]) * xs[j] for j in range(n)), Poly(n)) for i in range(n)]


def test_page_example():
    f, g, h = page_system()
    x1, x2, x3 = variables(3)
    lin = io_linearize(f, g, h, (0, 0, 0))
    assert lin.status == "ok" and lin.r == 2
    assert lin.xi == [x1, x2]
    assert lin.a == 1 + x1 ** 2
    assert lin.b == x1 * x3 - x2 ** 3


def test_lie_derivative_is_the_directional_derivative():
    # d/dt h(x0 + t v) at t = 0 equals grad h(x0) . v; compute it by
    # substitution into a polynomial in t, without the diff method.
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(1, 4)
        h = random_poly(rng, n)
        f = [random_poly(rng, n) for _ in range(n)]
        x0 = [Fraction(rng.randint(-3, 3), rng.randint(1, 2)) for _ in range(n)]
        v = [fi(x0) for fi in f]
        t = Poly.var(1, 0)
        curve = [Poly.const(1, a) + Poly.const(1, b) * t for a, b in zip(x0, v)]
        along = h(curve)
        along = along if isinstance(along, Poly) else Poly.const(1, along)
        slope = along.terms.get((1,), Fraction(0))
        assert lie_derivative(h, f)(x0) == slope


def test_bracket_identity():
    # L_[f,g] h = L_f L_g h - L_g L_f h, exactly.
    rng = random.Random(5)
    for _ in range(25):
        n = rng.randint(1, 3)
        f = [random_poly(rng, n, 3, 2) for _ in range(n)]
        g = [random_poly(rng, n, 3, 2) for _ in range(n)]
        h = random_poly(rng, n, 3, 3)
        lhs = lie_derivative(h, lie_bracket(f, g))
        rhs = lie_derivative(lie_derivative(h, g), f) - lie_derivative(lie_derivative(h, f), g)
        assert lhs == rhs


def test_bracket_sign():
    # [Ax, b] = -A b for a linear f and a constant g.
    f = linear_field([[0, 1], [-2, -3]])
    g = [Poly(2), Poly.const(2, 1)]
    assert lie_bracket(f, g) == [Poly.const(2, -1), Poly.const(2, 3)]


def test_linear_systems_against_markov_parameters():
    # For x' = A x + B u, y = C x: L_g L_f^k h = C A^k B and L_f^r h = C A^r x.
    rng = random.Random(2024)
    for trial in range(60):
        n = rng.randint(1, 5)
        A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        B = [rng.randint(-1, 1) * rng.randint(0, 1) for _ in range(n)]
        C = [rng.randint(-1, 1) * rng.randint(0, 1) for _ in range(n)]
        if trial % 7 == 0 and n >= 2:
            # input and output on separate decoupled blocks: no input effect
            k = n // 2
            A = [[A[i][j] if (i < k) == (j < k) else 0 for j in range(n)] for i in range(n)]
            B = [B[i] if i < k else 0 for i in range(n)]
            C = [C[i] if i >= k else 0 for i in range(n)]
        xs = variables(n)
        f = linear_field(A)
        g = [Poly.const(n, b) for b in B]
        h = sum((Poly.const(n, c) * x for c, x in zip(C, xs)), Poly(n))
        lin = io_linearize(f, g, h, [0] * n)
        markov = []
        row = C[:]
        for _ in range(n + 1):
            markov.append(sum(a * b for a, b in zip(row, B)))
            row = [sum(row[i] * A[i][j] for i in range(n)) for j in range(n)]
        nz = [k for k in range(n) if markov[k] != 0]
        if not nz:
            assert lin.status == "no input effect"
            continue
        r = nz[0] + 1
        assert lin.status == "ok" and lin.r == r
        assert lin.a == Poly.const(n, markov[r - 1])
        row = C[:]
        for _ in range(r):
            row = [sum(row[i] * A[i][j] for i in range(n)) for j in range(n)]
        assert lin.b == sum((Poly.const(n, c) * x for c, x in zip(row, xs)), Poly(n))


def test_isidori_identity_on_page_example():
    # L_(ad_f^j g) L_f^i h is 0 for i + j <= r - 2 and (-1)^j L_g L_f^(r-1) h for i + j = r - 1.
    f, g, h = page_system()
    lin = io_linearize(f, g, h, (0, 0, 0))
    r = lin.r
    ads = [g]
    for _ in range(r - 1):
        ads.append(lie_bracket(f, ads[-1]))
    for i in range(r):
        for j in range(r - i):
            val = lie_derivative(lin.xi[i], ads[j])
            if i + j <= r - 2:
                assert val.is_zero()
            else:
                assert val == (-1) ** j * lin.a


def test_relative_degree_equal_to_n():
    x1, x2, x3 = variables(3)
    zero = Poly(3)
    f = [x2, x3 + x1 ** 2, x1 * x2]
    g = [zero, zero, 1 + x2 ** 2]
    lin = io_linearize(f, g, x1, (0, 0, 0))
    assert lin.status == "ok" and lin.r == 3
    assert lin.xi == [x1, x2, x3 + x1 ** 2]
    assert lin.a == 1 + x2 ** 2
    assert lin.b == 3 * x1 * x2


def test_undefined_and_no_input_effect():
    y1, y2 = variables(2)
    f = [y2, Poly(2)]
    g = [y1, Poly.const(2, 1)]
    bad = io_linearize(f, g, y1, (0, 1))
    assert bad.status == "undefined" and bad.k == 0 and bad.a == y1
    good = io_linearize(f, g, y1, (1, 0))
    assert good.status == "ok" and good.r == 1
    # y = x2 with x1' = u, x2' = -x2: the input never reaches the output
    f2 = [Poly(2), -y2]
    g2 = [Poly.const(2, 1), Poly(2)]
    none = io_linearize(f2, g2, y2, (0, 0))
    assert none.status == "no input effect"
    with pytest.raises(ValueError):
        tracking_control(none, [1], [math.sin, math.cos])
    with pytest.raises(ValueError):
        io_linearize(f2, g2, y2, (0, 0, 0))


def test_closed_loop_tracking_matches_the_error_equation():
    # RK4 on the closed loop, dt = 0.01 to t = 5 (500 steps). With c = [2, 3]
    # the error obeys e'' + 3 e' + 2 e = 0, and from x(0) = (1, 0, 0) with
    # y_d = sin t the exact error is e(t) = exp(-t). Tolerance 1e-8.
    f, g, h = page_system()
    lin = io_linearize(f, g, h, (0, 0, 0))
    yd = [math.sin, math.cos, lambda t: -math.sin(t)]
    u = tracking_control(lin, [2, 3], yd)
    F = closed_loop(f, g, u)
    dt, t1 = 0.01, 5.0
    steps = round(t1 / dt)
    assert abs(steps * dt - t1) < 1e-12 and steps == 500
    ts, xs, _ = ctlsim.simulate(F, [1.0, 0.0, 0.0], 0.0, t1, dt)
    assert len(ts) == steps + 1
    for t, x in zip(ts, xs):
        assert abs(x[0] - math.sin(t) - math.exp(-t)) < 1e-8
        assert abs(x[1] - math.cos(t) + math.exp(-t)) < 1e-8
        assert abs(x[2]) < 2.0  # the internal state stays bounded
    assert abs(xs[-1][0] - math.sin(5.0)) < 0.0068


def test_sampled_feedback_is_only_approximate():
    # With a zero-order hold of 0.05 s the cancellation is not exact; the
    # error still decays but no longer equals exp(-t).
    f, g, h = page_system()
    lin = io_linearize(f, g, h, (0, 0, 0))
    yd = [math.sin, math.cos, lambda t: -math.sin(t)]
    u = tracking_control(lin, [2, 3], yd)

    def plant(t, x, uu):
        return [float(fi(x)) + float(gi(x)) * uu for fi, gi in zip(f, g)]

    ts, xs, _ = ctlsim.simulate(plant, [1.0, 0.0, 0.0], 0.0, 5.0, 0.01, control=u, hold=0.05)
    worst = max(abs(x[0] - math.sin(t) - math.exp(-t)) for t, x in zip(ts, xs))
    assert 1e-6 < worst < 0.1
    assert abs(xs[-1][0] - math.sin(5.0)) < 0.05
