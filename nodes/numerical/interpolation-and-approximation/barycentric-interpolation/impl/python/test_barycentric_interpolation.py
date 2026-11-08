# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barycentric-interpolation/. The authors are listed in prov/6W7GGA.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from barycentric_interpolation import (
    add_node,
    barycentric_eval,
    barycentric_interpolation,
    barycentric_weights,
    chebyshev1_points_and_weights,
    chebyshev2_points_and_weights,
)


def vandermonde_solve(xs, ys):
    """Oracle: monomial coefficients by exact Gauss-Jordan elimination."""
    n1 = len(xs)
    a = [[F(x) ** k for k in range(n1)] + [F(y)] for x, y in zip(xs, ys)]
    for c in range(n1):
        r = next(r for r in range(c, n1) if a[r][c] != 0)
        a[c], a[r] = a[r], a[c]
        for r in range(n1):
            if r != c and a[r][c] != 0:
                m = a[r][c] / a[c][c]
                a[r] = [p - m * q for p, q in zip(a[r], a[c])]
    return [a[k][n1] / a[k][k] for k in range(n1)]


def horner(c, t):
    s = F(0)
    for ck in reversed(c):
        s = s * t + ck
    return s


def test_example_page():
    xs = [F(0), F(1), F(2), F(4)]
    ys = [F(1), F(2), F(4), F(16)]
    assert barycentric_weights(xs) == [F(-1, 8), F(1, 3), F(-1, 4), F(1, 24)]
    assert barycentric_interpolation(xs, ys, F(3)) == F(33, 4)


def test_edges():
    assert barycentric_interpolation([F(2)], [F(7)], F(100)) == 7
    assert barycentric_interpolation([F(0), F(2)], [F(1), F(5)], F(1)) == 3
    with pytest.raises(ValueError):
        barycentric_interpolation([F(1), F(2), F(1)], [F(0), F(1), F(2)], F(0))
    with pytest.raises(ValueError):
        barycentric_interpolation([], [], F(0))
    with pytest.raises(ValueError):
        barycentric_interpolation([1.0, 2.0], [1.0], 0.0)
    xs = [0.1, 0.7, -0.3]
    ys = [3.0, -1.0, 2.5]
    for x, y in zip(xs, ys):
        assert barycentric_interpolation(xs, ys, x) == y


def test_random_against_vandermonde():
    rng = random.Random(1945)
    count = 0
    while count < 500:
        n1 = rng.randint(1, 8)
        xs = [F(v, rng.randint(1, 6)) for v in rng.sample(range(-40, 41), n1)]
        if len(set(xs)) != n1:
            continue
        ys = [F(rng.randint(-60, 60), rng.randint(1, 9)) for _ in range(n1)]
        c = vandermonde_solve(xs, ys)
        for x, y in zip(xs, ys):
            assert barycentric_interpolation(xs, ys, x) == y
        t = F(rng.randint(-50, 50), rng.randint(1, 7))
        assert barycentric_interpolation(xs, ys, t) == horner(c, t)
        count += 1


def test_polynomials_reproduced_and_order_free():
    xs = [F(3), F(-1), F(7, 2), F(0), F(1, 3), F(-5, 2)]
    ys = [x ** 5 - 3 * x ** 2 + 1 for x in xs]
    t = F(-9, 4)
    v = barycentric_interpolation(xs, ys, t)
    assert v == t ** 5 - 3 * t ** 2 + 1
    perm = [2, 0, 5, 1, 4, 3]
    assert barycentric_interpolation([xs[i] for i in perm], [ys[i] for i in perm], t) == v
    assert barycentric_interpolation(xs, [F(4)] * 6, F(11, 7)) == 4


def test_weights_scale_invariant():
    xs = [F(-2), F(0), F(1), F(5)]
    ys = [F(1), F(-3), F(2), F(7)]
    w = barycentric_weights(xs)
    for t in [F(1, 2), F(-7, 3), F(9)]:
        assert barycentric_eval(xs, [F(-13, 4) * v for v in w], ys, t) == barycentric_eval(xs, w, ys, t)


def test_add_node_matches_recomputation():
    rng = random.Random(1984)
    for _ in range(100):
        pool = rng.sample(range(-30, 31), 7)
        xs = [F(pool[0], 3)]
        w = barycentric_weights(xs)
        for v in pool[1:]:
            add_node(xs, w, F(v, 3))
            assert w == barycentric_weights(xs)
    with pytest.raises(ValueError):
        add_node([F(1)], [F(1)], F(1))


def test_chebyshev_closed_form_weights():
    for n in range(1, 30):
        for pts in (chebyshev2_points_and_weights, chebyshev1_points_and_weights):
            xs, w = pts(n)
            wc = barycentric_weights(xs)
            r = [a / b for a, b in zip(wc, w)]
            assert all(abs(v / r[0] - 1) < 1e-12 for v in r)
    xs, _ = chebyshev2_points_and_weights(10)
    assert xs[5] == 0.0 and all(xs[j] == -xs[10 - j] for j in range(11))


def test_chebyshev_convergence_observed():
    def runge(x):
        return 1 / (1 + 25 * x * x)
    grid = [math.cos(math.pi * (k + 0.5) / 500) for k in range(500)]
    errs = {}
    for n in (20, 40, 80, 160, 1000):
        xs, w = chebyshev2_points_and_weights(n)
        ys = [runge(x) for x in xs]
        errs[n] = max(abs(runge(t) - barycentric_eval(xs, w, ys, t)) for t in grid)
    assert 1e-2 < errs[20] < 3e-2
    assert 1e-4 < errs[40] < 1e-3
    assert errs[160] < 1e-13 and errs[1000] < 1e-13


def gamma(k, u):
    return k * u / (1 - k * u)


def test_rounding_error_bound():
    # |p_hat - p| <= ((1+u) g(3n+3) S_y + (u + g(3n+2) S_1)|p|) / (1 - g(3n+2) S_1),
    # where p, S_y, S_1 are computed exactly from the stored floats.
    rng = random.Random(2004)
    u = F(1, 2 ** 53)
    for trial in range(300):
        n1 = rng.randint(1, 16)
        if trial % 2:
            xs = sorted(set(rng.uniform(-1, 1) for _ in range(n1)))
        else:
            xs, _ = chebyshev2_points_and_weights(n1 - 1)
        n = len(xs) - 1
        ys = [rng.uniform(-10, 10) for _ in xs]
        t = rng.uniform(-1, 1)
        if t in xs:
            continue
        p_hat = F(barycentric_interpolation(xs, ys, t))
        fx, fy, ft = [F(x) for x in xs], [F(y) for y in ys], F(t)
        wx = barycentric_weights(fx)
        om = math.prod(ft - x for x in fx)
        ell = [om * wj / (ft - x) for wj, x in zip(wx, fx)]
        p = sum(e * y for e, y in zip(ell, fy))
        s_y = sum(abs(e * y) for e, y in zip(ell, fy))
        s_1 = sum(abs(e) for e in ell)
        g2, g3 = gamma(3 * n + 2, u), gamma(3 * n + 3, u)
        assert g2 * s_1 < 1
        bound = ((1 + u) * g3 * s_y + (u + g2 * s_1) * abs(p)) / (1 - g2 * s_1)
        assert abs(p_hat - p) <= bound
