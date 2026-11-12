# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frenet-frame/. The authors are listed in prov/CY1Y34.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from frenet_frame import (
    cross,
    curvature_squared,
    dot,
    double_reflection,
    frenet,
    signed_curvature,
    torsion,
)


def helix(a, b):
    C = lambda t: (a * math.cos(t), a * math.sin(t), b * t)
    d1 = lambda t: (-a * math.sin(t), a * math.cos(t), b)
    d2 = lambda t: (-a * math.cos(t), -a * math.sin(t), 0.0)
    d3 = lambda t: (a * math.sin(t), -a * math.cos(t), 0.0)
    return C, d1, d2, d3


def close(u, v, tol=1e-12):
    return all(abs(x - y) <= tol for x, y in zip(u, v))


def test_helix_closed_forms():
    for a, b in ((1.0, 1.0), (2.0, 0.5), (0.5, -1.5)):
        C, d1, d2, d3 = helix(a, b)
        c = math.hypot(a, b)
        for t in (0.0, 0.7, 2.0, -3.1):
            T, N, B, k, tau = frenet(d1(t), d2(t), d3(t))
            assert abs(k - a / (a * a + b * b)) < 1e-14
            assert abs(tau - b / (a * a + b * b)) < 1e-14
            assert close(T, (-a * math.sin(t) / c, a * math.cos(t) / c, b / c))
            assert close(N, (-math.cos(t), -math.sin(t), 0.0))
            assert close(B, (b * math.sin(t) / c, -b * math.cos(t) / c, a / c))


def test_circle():
    for r in (0.5, 3.0):
        for t in (0.0, 1.0, 4.0):
            d1 = (-r * math.sin(t), r * math.cos(t), 0.0)
            d2 = (-r * math.cos(t), -r * math.sin(t), 0.0)
            d3 = (r * math.sin(t), -r * math.cos(t), 0.0)
            T, N, B, k, tau = frenet(d1, d2, d3)
            assert abs(k - 1 / r) < 1e-14 and tau == 0
            assert close(B, (0.0, 0.0, 1.0))
            assert abs(signed_curvature(d1[:2], d2[:2]) - 1 / r) < 1e-14


def test_exact_twisted_cubic():
    # C(t) = (t, t^2, t^3): tau = 3 / (9 t^4 + 9 t^2 + 1), kappa^2 = 4 (9 t^4 + 9 t^2 + 1) / (1 + 4 t^2 + 9 t^4)^3
    for t in (F(0), F(1), F(-2, 3), F(5, 7)):
        d1, d2, d3 = (F(1), 2 * t, 3 * t * t), (F(0), F(2), 6 * t), (F(0), F(0), F(6))
        q = 9 * t ** 4 + 9 * t ** 2 + 1
        assert torsion(d1, d2, d3) == 3 / q
        assert curvature_squared(d1, d2) == 4 * q / (1 + 4 * t ** 2 + 9 * t ** 4) ** 3


def test_parametrization_invariance_exact():
    # kappa and tau do not change under t = phi(u); checked exactly for phi(u) = u^2 + u at u > 0
    rng = random.Random(1)
    for _ in range(50):
        coef = [[F(rng.randint(-4, 4)) for _ in range(4)] for _ in range(3)]
        u = F(rng.randint(1, 5), rng.randint(1, 4))
        t, p1, p2 = u * u + u, 2 * u + 1, F(2)

        def ders(x):
            d1 = tuple(c[1] + 2 * c[2] * x + 3 * c[3] * x * x for c in coef)
            d2 = tuple(2 * c[2] + 6 * c[3] * x for c in coef)
            d3 = tuple(6 * c[3] for c in coef)
            return d1, d2, d3

        a1, a2, a3 = ders(t)
        if dot(cross(a1, a2), cross(a1, a2)) == 0:
            continue
        # chain rule for the reparametrized curve (phi''' = 0)
        b1 = tuple(p1 * x for x in a1)
        b2 = tuple(p1 * p1 * y + p2 * x for x, y in zip(a1, a2))
        b3 = tuple(p1 ** 3 * z + 3 * p1 * p2 * y for y, z in zip(a2, a3))
        assert curvature_squared(b1, b2) == curvature_squared(a1, a2)
        assert torsion(b1, b2, b3) == torsion(a1, a2, a3)


def test_frenet_serret_equations_numerically():
    # dT/ds = kappa N, dN/ds = -kappa T + tau B, dB/ds = -tau N on a random cubic, by central differences
    rng = random.Random(2)
    for _ in range(10):
        coef = [[rng.uniform(-2, 2) for _ in range(4)] for _ in range(3)]
        d = lambda x: (tuple(c[1] + 2 * c[2] * x + 3 * c[3] * x * x for c in coef),
                       tuple(2 * c[2] + 6 * c[3] * x for c in coef),
                       tuple(6 * c[3] for c in coef))
        t, h = rng.uniform(-1, 1), 1e-5
        try:
            T, N, B, k, tau = frenet(*d(t))
            Tp, Np, Bp, _, _ = frenet(*d(t + h))
            Tm, Nm, Bm, _, _ = frenet(*d(t - h))
        except ValueError:
            continue
        v = math.sqrt(dot(d(t)[0], d(t)[0]))
        ds = 2 * h * v
        dT = tuple((p - m) / ds for p, m in zip(Tp, Tm))
        dN = tuple((p - m) / ds for p, m in zip(Np, Nm))
        dB = tuple((p - m) / ds for p, m in zip(Bp, Bm))
        tol = 1e-5 * (1 + k + abs(tau))
        assert close(dT, tuple(k * x for x in N), tol)
        assert close(dN, tuple(-k * x + tau * y for x, y in zip(T, B)), tol)
        assert close(dB, tuple(-tau * x for x in N), tol)


def test_fails_where_curvature_is_zero():
    with pytest.raises(ValueError):
        frenet((1.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 1.0, 0.0))  # a line
    with pytest.raises(ValueError):
        frenet((1.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 6.0, 0.0))  # the inflection of (t, t^3)
    with pytest.raises(ValueError):
        torsion((F(1), F(0), F(0)), (F(3), F(0), F(0)), (F(0), F(0), F(1)))


def test_normal_flips_at_an_inflection():
    # (t, t^3, 0): N and B turn over as t crosses 0
    left = frenet((1.0, 3e-4, 0.0), (0.0, -0.06, 0.0), (0.0, 6.0, 0.0))
    right = frenet((1.0, 3e-4, 0.0), (0.0, 0.06, 0.0), (0.0, 6.0, 0.0))
    assert dot(left[1], right[1]) < -0.99 and dot(left[2], right[2]) < -0.99


def test_double_reflection_on_helix():
    a, b = 1.0, 1.0
    C, d1, d2, d3 = helix(a, b)
    tau = b / (a * a + b * b)
    end = 2 * math.pi
    errors = []
    for n in (16, 32, 64):
        ts = [end * k / n for k in range(n + 1)]
        tans = [frenet(d1(t), d2(t), d3(t))[0] for t in ts]
        rs = double_reflection([C(t) for t in ts], tans, frenet(d1(0), d2(0), d3(0))[1])
        for t, T, r in zip(ts, tans, rs):
            assert abs(dot(T, r)) < 1e-12 and abs(dot(r, r) - 1) < 1e-12
        _, N, B, _, _ = frenet(d1(end), d2(end), d3(end))
        s = math.hypot(a, b) * end
        # exact RMF: r = cos(tau s) N - sin(tau s) B
        ref = tuple(math.cos(tau * s) * x - math.sin(tau * s) * y for x, y in zip(N, B))
        errors.append(math.dist(rs[-1], ref))
    assert errors[-1] < 2e-7
    # fourth order: the error falls by about 16 when the step halves
    assert 12 < errors[0] / errors[1] < 20 and 12 < errors[1] / errors[2] < 20


def test_double_reflection_on_a_line_and_plane_curve():
    pts = [(k * 1.0, 2.0 * k, 0.0) for k in range(10)]
    t = tuple(x / math.sqrt(5) for x in (1.0, 2.0, 0.0))
    rs = double_reflection(pts, [t] * 10, (0.0, 0.0, 1.0))
    assert all(close(r, (0.0, 0.0, 1.0)) for r in rs)
    # on a plane curve the RMF keeps the binormal direction (0, 0, 1) as its reference vector
    ts = [-1 + 2 * k / 50 for k in range(51)]
    pts = [(x, x ** 3, 0.0) for x in ts]
    tans = [tuple(c / math.hypot(1, 3 * x * x) for c in (1.0, 3 * x * x, 0.0)) for x in ts]
    rs = double_reflection(pts, tans, (0.0, 0.0, 1.0))
    assert all(close(r, (0.0, 0.0, 1.0), 1e-12) for r in rs)


def test_page_example():
    T, N, B, k, tau = frenet((1.0, 2.0, 3.0), (0.0, 2.0, 6.0), (0.0, 0.0, 6.0))
    assert abs(k - math.sqrt(76 / 14 ** 3)) < 1e-15 and abs(tau - 3 / 19) < 1e-15
    assert close([round(x, 4) for x in B], (0.6882, -0.6882, 0.2294))
