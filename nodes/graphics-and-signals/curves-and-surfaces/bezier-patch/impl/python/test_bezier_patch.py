# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-patch/. The authors are listed in prov/NCXHRX.jsonl.

import random
from fractions import Fraction
from math import comb

import pytest

from bezier_patch import (de_casteljau, patch_derivative, patch_point,
                          patch_point_bilinear, split_u)


def bernstein(n, i, t):
    return comb(n, i) * t ** i * (1 - t) ** (n - i) if 0 <= i <= n else 0


def dbernstein(n, i, t):
    """The exact derivative of B_i^n, from the power form of each term."""
    if n == 0:
        return 0
    return n * (bernstein(n - 1, i - 1, t) - bernstein(n - 1, i, t))


def bernstein_sum(net, u, v, du=0, dv=0):
    """The direct double sum of P_ij B_i^m(u) B_j^n(v), or of its derivative."""
    m, n = len(net) - 1, len(net[0]) - 1
    fu = dbernstein if du else bernstein
    fv = dbernstein if dv else bernstein
    out = [0] * len(net[0][0])
    for i in range(m + 1):
        bu = fu(m, i, u)
        for j in range(n + 1):
            w = bu * fv(n, j, v)
            for k, x in enumerate(net[i][j]):
                out[k] += w * x
    return tuple(out)


def random_net(rng, m, n, dim=3):
    return [[tuple(Fraction(rng.randint(-20, 20), rng.randint(1, 6)) for _ in range(dim))
             for _ in range(n + 1)] for _ in range(m + 1)]


def rand_param(rng):
    return Fraction(rng.randint(0, 24), 24)


def test_worked_example():
    net = [[(0, 0, 0), (0, 1, 1), (0, 2, 0)],
           [(1, 0, 1), (1, 1, 4), (1, 2, 1)],
           [(2, 0, 0), (2, 1, 1), (2, 2, 0)]]
    net = [[tuple(Fraction(x) for x in p) for p in row] for row in net]
    h = Fraction(1, 2)
    assert [de_casteljau(row, h) for row in net] == [(0, 1, Fraction(1, 2)), (1, 1, Fraction(5, 2)),
                                                    (2, 1, Fraction(1, 2))]
    assert patch_point(net, h, h) == (1, 1, Fraction(3, 2))
    assert patch_point(net, Fraction(1, 4), Fraction(1, 2)) == (Fraction(1, 2), 1, Fraction(5, 4))
    assert patch_derivative(net, h, h, 1, 0) == (2, 0, 0)
    assert patch_derivative(net, h, h, 0, 1) == (0, 2, 0)
    assert patch_derivative(net, h, h, 1, 1) == (0, 0, 0)
    assert patch_derivative(net, h, h, 2, 0) == (0, 0, -8)
    assert patch_derivative(net, Fraction(1, 4), h, 0, 2) == (0, 0, -7)


def test_against_bernstein_sum_exact():
    rng = random.Random(51)
    for _ in range(120):
        m, n = rng.randint(0, 4), rng.randint(0, 4)
        net = random_net(rng, m, n)
        u, v = rand_param(rng), rand_param(rng)
        ref = bernstein_sum(net, u, v)
        assert patch_point(net, u, v) == ref
        assert patch_point_bilinear(net, u, v) == ref


def test_derivatives_exact():
    rng = random.Random(52)
    for _ in range(60):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        net = random_net(rng, m, n)
        u, v = rand_param(rng), rand_param(rng)
        for du, dv in ((1, 0), (0, 1), (1, 1)):
            assert patch_derivative(net, u, v, du, dv) == bernstein_sum(net, u, v, du, dv)


def test_corners_and_boundary_curves():
    rng = random.Random(53)
    for _ in range(40):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        net = random_net(rng, m, n)
        assert patch_point(net, 0, 0) == net[0][0]
        assert patch_point(net, 1, 1) == net[m][n]
        t = rand_param(rng)
        assert patch_point(net, 0, t) == de_casteljau(net[0], t)
        assert patch_point(net, t, 1) == de_casteljau([row[n] for row in net], t)


def test_convex_hull_box():
    rng = random.Random(54)
    for _ in range(40):
        net = random_net(rng, rng.randint(1, 4), rng.randint(1, 4))
        pts = [p for row in net for p in row]
        p = patch_point(net, rand_param(rng), rand_param(rng))
        for k in range(3):
            assert min(q[k] for q in pts) <= p[k] <= max(q[k] for q in pts)


def test_split_reproduces_patch():
    rng = random.Random(55)
    for _ in range(30):
        m, n = rng.randint(1, 4), rng.randint(1, 3)
        net = random_net(rng, m, n)
        c = Fraction(rng.randint(1, 9), 10)
        left, right = split_u(net, c)
        for _ in range(4):
            s, v = rand_param(rng), rand_param(rng)
            assert patch_point(left, s, v) == patch_point(net, c * s, v)
            assert patch_point(right, s, v) == patch_point(net, c + (1 - c) * s, v)


def test_float_close_to_exact():
    rng = random.Random(56)
    net = random_net(rng, 3, 3)
    fnet = [[tuple(float(x) for x in p) for p in row] for row in net]
    for _ in range(20):
        u, v = rand_param(rng), rand_param(rng)
        exact = bernstein_sum(net, u, v)
        approx = patch_point(fnet, float(u), float(v))
        assert all(abs(a - float(b)) < 1e-12 for a, b in zip(approx, exact))


def test_bad_net():
    with pytest.raises(ValueError):
        patch_point([[(0, 0)], [(0, 0), (1, 1)]], 0, 0)
    with pytest.raises(ValueError):
        patch_point([], 0, 0)
