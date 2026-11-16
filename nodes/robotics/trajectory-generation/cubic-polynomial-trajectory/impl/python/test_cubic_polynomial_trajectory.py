# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cubic-polynomial-trajectory/. The authors are listed in prov/HEFVQT.jsonl.
"""Tests: exact end conditions, the check values, a second method, and the minimum acceleration property."""

import random
from fractions import Fraction as F

from cubic_polynomial_trajectory import cubic_coeffs, cubic_eval, cubic_via, via_eval


def solve(m, b):
    """Gauss-Jordan elimination in exact arithmetic (the second method)."""
    n = len(m)
    a = [[F(x) for x in m[i]] + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def poly_mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def poly_der(p):
    return [i * p[i] for i in range(1, len(p))] or [F(0)]


def integral_sq(p, T):
    sq = poly_mul(p, p)
    return sum(c * T ** (i + 1) / (i + 1) for i, c in enumerate(sq))


def test_end_conditions_exact():
    rng = random.Random(1)
    for _ in range(200):
        q0, v0, q1, v1 = (F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(4))
        T = F(rng.randint(1, 40), rng.randint(1, 9))
        a = cubic_coeffs(q0, v0, q1, v1, T)
        s, ds, _ = cubic_eval(a, F(0))
        e, de, _ = cubic_eval(a, T)
        assert (s, ds, e, de) == (q0, v0, q1, v1)


def test_check_values():
    a = cubic_coeffs(F(0), F(0), F(1), F(0), F(1))
    assert a == (0, 0, 3, -2)
    assert cubic_eval(a, F(1, 2))[1] == F(3, 2)
    assert cubic_eval(a, F(0))[2] == 6
    assert cubic_eval(a, F(1))[2] == -6
    # The velocity is a parabola, so its maximum on a grid is at t = 1/2.
    grid = [cubic_eval(a, F(k, 1000))[1] for k in range(1001)]
    assert max(grid) == F(3, 2)
    # Scaling: distance D in time T gives peak velocity 1.5 D / T and end acceleration 6 D / T^2.
    a = cubic_coeffs(F(1), F(0), F(4), F(0), F(2))
    assert cubic_eval(a, F(1))[1] == F(3, 2) * 3 / 2
    assert cubic_eval(a, F(0))[2] == 6 * F(3) / 4


def test_against_linear_solve():
    rng = random.Random(2)
    for _ in range(100):
        q0, v0, q1, v1 = (F(rng.randint(-20, 20)) for _ in range(4))
        T = F(rng.randint(1, 10), rng.randint(1, 4))
        m = [[1, 0, 0, 0], [0, 1, 0, 0], [1, T, T * T, T ** 3], [0, 1, 2 * T, 3 * T * T]]
        assert list(cubic_coeffs(q0, v0, q1, v1, T)) == solve(m, [q0, v0, q1, v1])


def test_minimum_squared_acceleration():
    # Any other C^1 path with the same end positions and velocities is q + eta,
    # with eta = t^2 (T - t)^2 r(t). Its cost exceeds the cubic's cost by the cost of eta.
    rng = random.Random(3)
    for _ in range(40):
        T = F(rng.randint(1, 5))
        a = list(cubic_coeffs(F(rng.randint(-5, 5)), F(rng.randint(-5, 5)), F(rng.randint(-5, 5)), F(rng.randint(-5, 5)), T))
        base = integral_sq(poly_der(poly_der(a)), T)
        bump = poly_mul(poly_mul([F(0), F(0), F(1)], poly_mul([T, F(-1)], [T, F(-1)])), [F(rng.randint(-3, 3)) for _ in range(3)])
        if all(c == 0 for c in bump):
            continue
        other = [x + y for x, y in zip(a + [F(0)] * (len(bump) - len(a)), bump)]
        cost = integral_sq(poly_der(poly_der(other)), T)
        assert cost == base + integral_sq(poly_der(poly_der(bump)), T)
        assert cost > base


def test_float_inputs():
    a = cubic_coeffs(0.0, 0.0, 1.0, 0.0, 2.0)
    q, dq, _ = cubic_eval(a, 2.0)
    assert abs(q - 1.0) < 1e-12 and abs(dq) < 1e-12


def test_via_points_continuity():
    pts = [F(0), F(2), F(1), F(3)]
    vel = [F(0), F(1), F(-1, 2), F(0)]
    ts = [F(0), F(1), F(3), F(4)]
    segs = cubic_via(pts, vel, ts)
    for k in range(1, 3):
        left = cubic_eval(segs[k - 1][1], ts[k] - ts[k - 1])
        right = cubic_eval(segs[k][1], F(0))
        assert left[0] == right[0] == pts[k]
        assert left[1] == right[1] == vel[k]
    assert via_eval(segs, F(4))[0] == 3
    assert via_eval(segs, F(0))[0] == 0


def test_bad_input():
    for bad in (0, -1):
        try:
            cubic_coeffs(0, 0, 1, 0, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("T <= 0 must fail")
