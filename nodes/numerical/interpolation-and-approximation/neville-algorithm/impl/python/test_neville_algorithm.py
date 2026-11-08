# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neville-algorithm/. The authors are listed in prov/BNE6XG.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from neville_algorithm import neville, neville_extrapolate, neville_table


def lagrange_value(x, y, t):
    """Independent oracle: the Lagrange formula in exact arithmetic."""
    s = F(0)
    for i in range(len(x)):
        li = F(1)
        for j in range(len(x)):
            if j != i:
                li *= F(t - x[j]) / (x[i] - x[j])
        s += y[i] * li
    return s


def test_page_example():
    x = [F(v) for v in (0, 1, 2, 4, 5)]
    y = [F(2) ** int(v) for v in x]
    assert neville(x, y, F(3)) == F(79, 10)
    tab = neville_table(x, y, F(3))
    assert tab[1] == [4, 6, 10, 0]
    assert tab[2] == [7, F(26, 3), F(20, 3)]
    assert tab[3] == [F(33, 4), F(23, 3)]
    assert tab[4] == [F(79, 10)]


def test_single_and_two_nodes():
    assert neville([F(3)], [F(7)], F(100)) == 7
    # two nodes: the straight line
    assert neville([F(1), F(3)], [F(2), F(6)], F(10)) == 20
    assert neville([1.0, 3.0], [2.0, 6.0], 2.0) == 4.0


def test_at_node_is_exact():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(1, 12)
        x = rng.sample(range(-50, 50), n + 1)
        x = [F(v, 7) for v in x]
        y = [F(rng.randint(-99, 99), rng.randint(1, 9)) for _ in x]
        for i in range(n + 1):
            assert neville(x, y, x[i]) == y[i]


def test_random_against_lagrange_exact():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(0, 10)
        x = [F(v, 3) for v in rng.sample(range(-60, 60), n + 1)]
        y = [F(rng.randint(-50, 50), rng.randint(1, 5)) for _ in x]
        t = F(rng.randint(-300, 300), 11)
        assert neville(x, y, t) == lagrange_value(x, y, t)


def test_polynomials_reproduced_exactly():
    rng = random.Random(3)
    for _ in range(60):
        deg = rng.randint(0, 8)
        c = [F(rng.randint(-9, 9)) for _ in range(deg + 1)]
        n = rng.randint(deg, deg + 4)
        x = [F(v, 2) for v in rng.sample(range(-40, 40), n + 1)]
        f = lambda s: sum(ck * s ** k for k, ck in enumerate(c))
        y = [f(v) for v in x]
        for t in (F(-17, 3), F(0), F(5, 7), F(31, 2)):
            assert neville(x, y, t) == f(t)


def test_constant_data_float():
    rng = random.Random(4)
    for _ in range(50):
        n = rng.randint(1, 20)
        x = [math.cos((2 * i + 1) * math.pi / (2 * n + 2)) for i in range(n + 1)]
        rng.shuffle(x)
        val = rng.uniform(-5, 5)
        t = rng.uniform(-1, 1)
        assert abs(neville(x, [val] * (n + 1), t) - val) <= 1e-13 * abs(val) * n


def test_order_of_nodes_does_not_matter():
    rng = random.Random(5)
    for _ in range(50):
        n = rng.randint(1, 9)
        x = [F(v) for v in rng.sample(range(-30, 30), n + 1)]
        y = [F(rng.randint(-20, 20)) for _ in x]
        t = F(rng.randint(-90, 90), 13)
        perm = list(range(n + 1))
        rng.shuffle(perm)
        assert neville(x, y, t) == neville([x[i] for i in perm], [y[i] for i in perm], t)


def test_float_matches_exact_at_chebyshev_points():
    rng = random.Random(6)
    for n in (5, 10, 20, 40):
        x = [math.cos((2 * i + 1) * math.pi / (2 * n + 2)) for i in range(n + 1)]
        y = [1 / (1 + 25 * v * v) for v in x]
        xf = [F(v) for v in x]
        yf = [F(v) for v in y]
        for _ in range(10):
            t = rng.uniform(-1, 1)
            exact = lagrange_value(xf, yf, F(t))
            assert abs(neville(x, y, t) - float(exact)) < 1e-13


def test_jump_and_pole_data_interpolated_exactly():
    # a step: the interpolant is wild, but it is the right polynomial
    x = [F(i - 5) for i in range(11)]
    y = [F(0) if v < 0 else F(1) for v in x]
    for t in (F(-9, 2), F(1, 3), F(47, 10)):
        assert neville(x, y, t) == lagrange_value(x, y, t)
    # a pole just outside [-1, 1]
    x = [F(2 * i - 8, 8) for i in range(9)]
    y = [1 / (F(101, 100) - v) for v in x]
    for t in (F(-1, 3), F(9, 10)):
        assert neville(x, y, t) == lagrange_value(x, y, t)


def test_last_column_difference_estimates_error():
    x = [k / 8 for k in range(9)]
    y = [math.exp(v) for v in x]
    t = 0.53
    tab = neville_table(x, y, t)
    err = abs(tab[8][0] - math.exp(t))
    est = abs(tab[7][0] - tab[7][1])
    assert err < 1e-11 and est < 1e-7 and err < est


def test_richardson_extrapolation():
    # A(h) = sin(h)/h = 1 - h^2/6 + ..., extrapolate in h^2 to h = 0
    h = [0.5 / 2 ** k for k in range(5)]
    a = [math.sin(v) / v for v in h]
    val = neville_extrapolate([v * v for v in h], a)
    assert abs(val - 1.0) < 1e-14
    assert abs(a[-1] - 1.0) > 1e-4


def test_errors():
    with pytest.raises(ValueError):
        neville([], [], 0)
    with pytest.raises(ValueError):
        neville([1, 2], [1], 0)
    with pytest.raises(ValueError):
        neville([1, 1], [1, 2], 0)
    with pytest.raises(ValueError):
        neville_table([0, 0], [1, 1], 0)
