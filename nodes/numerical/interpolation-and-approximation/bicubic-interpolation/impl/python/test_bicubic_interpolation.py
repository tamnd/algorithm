# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bicubic-interpolation/. The authors are listed in prov/4YZAGC.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from bicubic_interpolation import axis_weights, bicubic_interpolation, bicubic_sorted


def parabola_slope(xs, ys, m):
    """Independent three-point slope: derivative at xs[m] of the Newton parabola."""
    n = len(xs) - 1
    if n == 1:
        return (ys[1] - ys[0]) / (xs[1] - xs[0])
    a, b, c = (0, 1, 2) if m == 0 else (n - 2, n - 1, n) if m == n else (m - 1, m, m + 1)
    d1 = (ys[b] - ys[a]) / (xs[b] - xs[a])
    d2 = ((ys[c] - ys[b]) / (xs[c] - xs[b]) - d1) / (xs[c] - xs[a])
    z = xs[m]
    return d1 + d2 * ((z - xs[a]) + (z - xs[b]))


def hermite_1d(xs, ys, t):
    """Independent oracle in one variable: solve for the cubic coefficients directly."""
    i = 0
    while i < len(xs) - 2 and t >= xs[i + 1]:
        i += 1
    x0, x1 = xs[i], xs[i + 1]
    d0, d1 = parabola_slope(xs, ys, i), parabola_slope(xs, ys, i + 1)
    h = x1 - x0
    # cubic c0 + c1 u + c2 u^2 + c3 u^3 in u = t - x0
    c0, c1 = ys[i], d0
    delta = (ys[i + 1] - ys[i]) / h
    c2 = (3 * delta - 2 * d0 - d1) / h
    c3 = (d0 + d1 - 2 * delta) / (h * h)
    u = t - x0
    return c0 + u * (c1 + u * (c2 + u * c3))


def oracle(xs, ys, table, x, y):
    px = sorted(range(len(xs)), key=lambda k: xs[k])
    py = sorted(range(len(ys)), key=lambda k: ys[k])
    sx, sy = [xs[k] for k in px], [ys[k] for k in py]
    col = [hermite_1d(sy, [table[a][b] for b in py], y) for a in px]
    return hermite_1d(sx, col, x)


def test_page_example():
    g = [F(k) for k in range(4)]
    table = [[F(a * a + b) for b in range(4)] for a in range(4)]
    assert bicubic_interpolation(g, g, table, F(3, 2), F(3, 2)) == F(15, 4)
    table[1][2] += 1
    assert bicubic_interpolation(g, g, table, F(3, 2), F(3, 2)) == F(15, 4) + F(81, 256)
    w = axis_weights(g + [F(4), F(5)], 2, F(5, 2))
    assert [c for _, c in w] == [F(-1, 16), F(9, 16), F(9, 16), F(-1, 16)]


def test_keys_kernel_on_uniform_grid():
    g = [F(k) for k in range(9)]
    for k in range(101):
        s = F(k, 100)
        w = [c for _, c in axis_weights(g, 4, 4 + s)]
        keys = [(-s ** 3 + 2 * s ** 2 - s) / 2, (3 * s ** 3 - 5 * s ** 2 + 2) / 2,
                (-3 * s ** 3 + 4 * s ** 2 + s) / 2, (s ** 3 - s ** 2) / 2]
        assert w == keys
        assert sum(abs(c) for c in w) == 1 + s * (1 - s)


def test_random_against_oracle():
    rng = random.Random(1981)
    for _ in range(500):
        m, n = rng.randint(2, 6), rng.randint(2, 6)
        xs = [F(v, 3) for v in rng.sample(range(-30, 31), m)]
        ys = [F(v, 2) for v in rng.sample(range(-30, 31), n)]
        table = [[F(rng.randint(-50, 50), rng.randint(1, 5)) for _ in ys] for _ in xs]
        x = min(xs) + (max(xs) - min(xs)) * F(rng.randint(-20, 120), 100)
        y = min(ys) + (max(ys) - min(ys)) * F(rng.randint(-20, 120), 100)
        assert bicubic_interpolation(xs, ys, table, x, y) == oracle(xs, ys, table, x, y)


def test_reproduces_biquadratics_and_nodes():
    rng = random.Random(1974)
    for _ in range(60):
        c = [[F(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(3)] for _ in range(3)]
        q = lambda x, y: sum(c[a][b] * x ** a * y ** b for a in range(3) for b in range(3))
        xs = [F(v, 4) for v in rng.sample(range(-40, 41), rng.randint(3, 7))]
        ys = [F(v, 5) for v in rng.sample(range(-40, 41), rng.randint(3, 7))]
        table = [[q(a, b) for b in ys] for a in xs]
        for _ in range(4):
            x, y = F(rng.randint(-60, 60), 7), F(rng.randint(-60, 60), 9)
            assert bicubic_interpolation(xs, ys, table, x, y) == q(x, y)
    # not exact on cubics in general
    xs = [F(k) for k in range(5)]
    table = [[F(a) ** 3 for _ in range(3)] for a in range(5)]
    assert bicubic_interpolation(xs, xs[:3], table, F(1, 2), F(1)) != F(1, 8)
    # grid values are returned exactly at grid points
    for _ in range(30):
        xs = sorted(rng.uniform(-5, 5) for _ in range(6))
        ys = sorted(rng.uniform(-5, 5) for _ in range(5))
        table = [[rng.uniform(-1e3, 1e3) for _ in ys] for _ in xs]
        for i, a in enumerate(xs):
            for j, b in enumerate(ys):
                assert abs(bicubic_sorted(xs, ys, table, a, b) - table[i][j]) <= 1e-12 * 1e3


def test_c1_across_cells():
    rng = random.Random(1878)
    xs = sorted(F(v, 3) for v in rng.sample(range(-30, 31), 6))
    ys = sorted(F(v, 2) for v in rng.sample(range(-30, 31), 5))
    table = [[F(rng.randint(-9, 9)) for _ in ys] for _ in xs]
    eps = F(1, 10 ** 6)
    for k in range(1, len(xs) - 1):
        for y in (ys[1] + F(1, 7), ys[2] - F(1, 5)):
            x = xs[k]
            v = bicubic_sorted(xs, ys, table, x, y)
            left = (v - bicubic_sorted(xs, ys, table, x - eps, y)) / eps
            right = (bicubic_sorted(xs, ys, table, x + eps, y) - v) / eps
            assert abs(left - right) < F(1, 1000)


def test_third_order_and_overshoot():
    f = lambda x, y: math.sin(2 * x) * math.exp(y)
    pts = [(k + 0.37) / 40 for k in range(40)]
    errs = []
    for n in (4, 8, 16):
        g = [k / n for k in range(n + 1)]
        table = [[f(a, b) for b in g] for a in g]
        errs.append(max(abs(f(a, b) - bicubic_sorted(g, g, table, a, b)) for a in pts for b in pts))
    for a, b in zip(errs, errs[1:]):
        assert 5 < a / b < 11
    xs = [float(k) for k in range(6)]
    step = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
    table = [[v, v] for v in step]
    vals = [bicubic_sorted(xs, [0.0, 1.0], table, 1 + t / 300, 0.5) for t in range(301)]
    assert abs(min(vals) + 2 / 27) < 1e-6


def test_edges():
    assert bicubic_interpolation([F(2)], [F(0), F(4)], [[F(1), F(9)]], F(7), F(1)) == 3
    assert bicubic_interpolation([F(2)], [F(5)], [[F(8)]], F(0), F(0)) == 8
    # three nodes on an axis: the interpolating parabola
    xs = [F(0), F(1), F(3)]
    table = [[F(v)] * 2 for v in (1, 0, 4)]
    p = lambda t: 1 - 2 * t + t * t
    for t in [F(1, 2), F(2), F(5, 2), F(-1)]:
        assert bicubic_interpolation(xs, [F(0), F(1)], table, t, F(1, 3)) == p(t)
    with pytest.raises(ValueError):
        bicubic_interpolation([0.0, 1.0], [2.0, 2.0], [[1.0, 2.0], [3.0, 4.0]], 0.5, 0.5)
    with pytest.raises(ValueError):
        bicubic_interpolation([0.0, 1.0], [0.0], [[1.0, 2.0], [3.0]], 0.5, 0.5)
