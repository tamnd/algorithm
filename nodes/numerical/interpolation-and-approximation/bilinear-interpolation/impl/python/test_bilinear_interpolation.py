# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-interpolation/. The authors are listed in prov/15TKW4.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from bilinear_interpolation import bilinear_interpolation, bilinear_sorted


def solve4(rows, rhs):
    m = [r[:] + [b] for r, b in zip(rows, rhs)]
    for c in range(4):
        p = next(r for r in range(c, 4) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(4):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return [m[i][4] / m[i][i] for i in range(4)]


def oracle(xs, ys, table, x, y):
    """Fit c0 + c1 x + c2 y + c3 x y to the four corners of the cell, exactly."""
    order_x = sorted(range(len(xs)), key=lambda i: xs[i])
    order_y = sorted(range(len(ys)), key=lambda j: ys[j])
    sx = [xs[i] for i in order_x]
    sy = [ys[j] for j in order_y]
    i = 0
    while i < len(sx) - 2 and x >= sx[i + 1]:
        i += 1
    j = 0
    while j < len(sy) - 2 and y >= sy[j + 1]:
        j += 1
    rows, rhs = [], []
    for a in (i, i + 1):
        for b in (j, j + 1):
            px, py = sx[a], sy[b]
            rows.append([F(1), px, py, px * py])
            rhs.append(table[order_x[a]][order_y[b]])
    c = solve4(rows, rhs)
    return c[0] + c[1] * x + c[2] * y + c[3] * x * y


def test_page_example():
    xs, ys = [F(0), F(1)], [F(0), F(1)]
    table = [[F(1), F(2)], [F(3), F(6)]]
    assert bilinear_interpolation(xs, ys, table, F(1, 4), F(1, 2)) == F(9, 4)
    saddle = [[F(0), F(1)], [F(1), F(0)]]
    for t in [F(k, 10) for k in range(11)]:
        assert bilinear_interpolation(xs, ys, saddle, t, t) == 2 * t - 2 * t * t


def test_random_against_exact_oracle():
    rng = random.Random(1964)
    for _ in range(600):
        m, n = rng.randint(2, 6), rng.randint(2, 6)
        xs = [F(v, 3) for v in rng.sample(range(-30, 31), m)]
        ys = [F(v, 2) for v in rng.sample(range(-30, 31), n)]
        table = [[F(rng.randint(-50, 50), rng.randint(1, 5)) for _ in ys] for _ in xs]
        x = min(xs) + (max(xs) - min(xs)) * F(rng.randint(-20, 120), 100)
        y = min(ys) + (max(ys) - min(ys)) * F(rng.randint(-20, 120), 100)
        assert bilinear_interpolation(xs, ys, table, x, y) == oracle(xs, ys, table, x, y)


def test_reproduces_q1_and_hits_nodes():
    rng = random.Random(1971)
    for _ in range(100):
        c = [F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(4)]
        q = lambda x, y: c[0] + c[1] * x + c[2] * y + c[3] * x * y
        xs = [F(v, 4) for v in rng.sample(range(-40, 41), rng.randint(2, 7))]
        ys = [F(v, 5) for v in rng.sample(range(-40, 41), rng.randint(2, 7))]
        table = [[q(a, b) for b in ys] for a in xs]
        for _ in range(5):
            x, y = F(rng.randint(-60, 60), 7), F(rng.randint(-60, 60), 9)
            assert bilinear_interpolation(xs, ys, table, x, y) == q(x, y)
    # floating point: grid values are returned exactly at grid points
    for _ in range(100):
        xs = sorted(rng.sample([rng.uniform(-5, 5) for _ in range(40)], 6))
        ys = sorted(rng.sample([rng.uniform(-5, 5) for _ in range(40)], 5))
        table = [[rng.uniform(-1e3, 1e3) for _ in ys] for _ in xs]
        for i, a in enumerate(xs):
            for j, b in enumerate(ys):
                assert bilinear_sorted(xs, ys, table, a, b) == table[i][j]


def test_max_principle_and_unsorted():
    rng = random.Random(1983)
    for _ in range(200):
        xs = [rng.uniform(-3, 3) for _ in range(4)]
        ys = [rng.uniform(-3, 3) for _ in range(3)]
        table = [[rng.uniform(-1, 1) for _ in ys] for _ in xs]
        x = rng.uniform(min(xs), max(xs))
        y = rng.uniform(min(ys), max(ys))
        v = bilinear_interpolation(xs, ys, table, x, y)
        flat = [w for r in table for w in r]
        assert min(flat) - 1e-12 <= v <= max(flat) + 1e-12
        # reversing the order of the input changes nothing
        rx = list(reversed(range(4)))
        v2 = bilinear_interpolation([xs[i] for i in rx], ys, [table[i] for i in rx], x, y)
        assert abs(v - v2) <= 1e-12


def test_error_bound():
    f = lambda x, y: math.exp(x + y)
    for n in (2, 4, 8, 16, 32):
        g = [k / n for k in range(n + 1)]
        table = [[f(a, b) for b in g] for a in g]
        pts = [k / (5 * n) for k in range(5 * n + 1)]
        err = max(abs(f(a, b) - bilinear_sorted(g, g, table, a, b)) for a in pts for b in pts)
        assert err <= 2 * (1 / n) ** 2 / 8 * math.e ** 2 + 1e-12


def test_edges():
    # one coordinate on an axis: linear in the other variable
    assert bilinear_interpolation([F(2)], [F(0), F(4)], [[F(1), F(9)]], F(7), F(1)) == 3
    assert bilinear_interpolation([F(0), F(4)], [F(5)], [[F(1)], [F(9)]], F(1), F(-3)) == 3
    assert bilinear_interpolation([F(2)], [F(5)], [[F(8)]], F(0), F(0)) == 8
    with pytest.raises(ValueError):
        bilinear_interpolation([0.0, 0.0], [0.0, 1.0], [[1.0, 2.0], [3.0, 4.0]], 0.5, 0.5)
    with pytest.raises(ValueError):
        bilinear_interpolation([0.0, 1.0], [0.0, 1.0], [[1.0, 2.0]], 0.5, 0.5)
    # extrapolation continues the end cell
    xs, ys = [F(0), F(1), F(2)], [F(0), F(1)]
    table = [[F(0), F(1)], [F(1), F(3)], [F(2), F(5)]]
    assert bilinear_interpolation(xs, ys, table, F(3), F(2)) == oracle(xs, ys, table, F(3), F(2))
