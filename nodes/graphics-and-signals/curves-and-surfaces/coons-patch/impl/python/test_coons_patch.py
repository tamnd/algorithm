# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coons-patch/. The authors are listed in prov/JG5HXQ.jsonl.

import random
from fractions import Fraction
from math import comb

import pytest

from coons_patch import bezier, coons_bezier_net, coons_point


def rp(rng, dim=3):
    return tuple(Fraction(rng.randint(-12, 12), rng.randint(1, 4)) for _ in range(dim))


def random_boundary(rng, m, n):
    p00, p10, p01, p11 = rp(rng), rp(rng), rp(rng), rp(rng)
    a = [p00] + [rp(rng) for _ in range(m - 1)] + [p10]
    b = [p01] + [rp(rng) for _ in range(m - 1)] + [p11]
    c = [p00] + [rp(rng) for _ in range(n - 1)] + [p01]
    d = [p10] + [rp(rng) for _ in range(n - 1)] + [p11]
    return a, b, c, d


def param(rng):
    return Fraction(rng.randint(0, 20), 20)


def bernstein_sum(net, u, v):
    m, n = len(net) - 1, len(net[0]) - 1
    return tuple(sum(comb(m, i) * u ** i * (1 - u) ** (m - i) * comb(n, j) * v ** j * (1 - v) ** (n - j)
                     * net[i][j][k] for i in range(m + 1) for j in range(n + 1))
                 for k in range(len(net[0][0])))


# The boundary of the biquadratic patch of the Bezier patch page.
A = [(0, 0, 0), (1, 0, 1), (2, 0, 0)]      # c0(u) = S(u, 0)
B = [(0, 2, 0), (1, 2, 1), (2, 2, 0)]      # c1(u) = S(u, 1)
C = [(0, 0, 0), (0, 1, 1), (0, 2, 0)]      # d0(v) = S(0, v)
D = [(2, 0, 0), (2, 1, 1), (2, 2, 0)]      # d1(v) = S(1, v)


def test_worked_example():
    h = Fraction(1, 2)
    s = coons_point(bezier(A), bezier(B), bezier(C), bezier(D), h, h)
    assert s == (1, 1, 1)
    net = coons_bezier_net(A, B, C, D)
    assert net[1][1] == (1, 1, 2)
    assert bernstein_sum(net, h, h) == s


def test_boundaries_exact():
    rng = random.Random(71)
    for _ in range(60):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        a, b, c, d = random_boundary(rng, m, n)
        c0, c1, d0, d1 = bezier(a), bezier(b), bezier(c), bezier(d)
        for _ in range(4):
            t = param(rng)
            assert coons_point(c0, c1, d0, d1, t, 0) == c0(t)
            assert coons_point(c0, c1, d0, d1, t, 1) == c1(t)
            assert coons_point(c0, c1, d0, d1, 0, t) == d0(t)
            assert coons_point(c0, c1, d0, d1, 1, t) == d1(t)


def test_bezier_net_equals_coons_formula():
    rng = random.Random(72)
    for _ in range(40):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        a, b, c, d = random_boundary(rng, m, n)
        net = coons_bezier_net(a, b, c, d)
        assert [net[i][0] for i in range(m + 1)] == a
        assert [net[i][n] for i in range(m + 1)] == b
        assert net[0] == c and net[m] == d
        for _ in range(4):
            u, v = param(rng), param(rng)
            assert bernstein_sum(net, u, v) == coons_point(bezier(a), bezier(b), bezier(c), bezier(d), u, v)


def test_straight_edges_give_bilinear_patch():
    rng = random.Random(73)
    for _ in range(30):
        p00, p10, p01, p11 = rp(rng), rp(rng), rp(rng), rp(rng)
        line = lambda p, q: (lambda t: tuple((1 - t) * x + t * y for x, y in zip(p, q)))
        u, v = param(rng), param(rng)
        s = coons_point(line(p00, p10), line(p01, p11), line(p00, p01), line(p10, p11), u, v)
        bil = tuple((1 - u) * (1 - v) * a + u * (1 - v) * b + (1 - u) * v * c + u * v * d
                    for a, b, c, d in zip(p00, p10, p01, p11))
        assert s == bil


def test_reproduces_ruled_surface():
    """A surface linear in v is rebuilt exactly from its four boundary curves."""
    rng = random.Random(74)
    for _ in range(30):
        top = [rp(rng) for _ in range(4)]
        bot = [rp(rng) for _ in range(4)]
        ca, cb = bezier(top), bezier(bot)
        surf = lambda u, v: tuple((1 - v) * x + v * y for x, y in zip(ca(u), cb(u)))
        d0 = lambda v: surf(0, v)
        d1 = lambda v: surf(1, v)
        u, v = param(rng), param(rng)
        assert coons_point(ca, cb, d0, d1, u, v) == surf(u, v)


def test_ruled_part_alone_misses_two_edges():
    c0, c1, d0, d1 = bezier(A), bezier(B), bezier(C), bezier(D)
    ruled = lambda u, v: tuple((1 - v) * x + v * y for x, y in zip(c0(u), c1(u)))
    h = Fraction(1, 2)
    assert ruled(0, h) != d0(h)            # the ruled surface ignores d0 and d1
    assert coons_point(c0, c1, d0, d1, 0, h) == d0(h)


def test_corner_mismatch():
    bad = [(0, 0, 0), (0, 1, 1), (0, 2, 1)]
    with pytest.raises(ValueError):
        coons_point(bezier(A), bezier(B), bezier(bad), bezier(D), 0, 0)
    with pytest.raises(ValueError):
        coons_bezier_net(A, B, bad, D)
