# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/line-equation-from-segment/. The authors are listed in prov/1VCZP5.jsonl.

import random
from fractions import Fraction
from math import gcd

import pytest

from line_equation_from_segment import (line_through, line_through_from_coeffs,
                                        line_through_rational, oriented_line_through, side)


def collinear(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]) == 0


def is_canonical(l):
    a, b, c = l
    return (a, b) != (0, 0) and gcd(gcd(abs(a), abs(b)), abs(c)) == 1 and (a > 0 or (a == 0 and b > 0))


def test_example():
    assert line_through((1, 2), (4, 6)) == (4, -3, 2)
    assert line_through((2, 2), (6, 8)) == (3, -2, -2)
    assert line_through((3, 1), (3, 5)) == (1, 0, -3)
    assert line_through((5, 2), (1, 2)) == (0, 1, -2)
    assert oriented_line_through((1, 2), (4, 6)) == (-4, 3, -2)
    assert side(oriented_line_through((1, 2), (4, 6)), (0, 0)) == -1  # right of p -> q


def test_degenerate():
    with pytest.raises(ValueError):
        line_through((1, 1), (1, 1))
    with pytest.raises(ValueError):
        line_through_from_coeffs(0, 0, 5)
    assert line_through((0, 0), (0, 7)) == (1, 0, 0)
    assert line_through((0, 0), (-7, 0)) == (0, 1, 0)
    assert line_through((-3, -3), (5, 5)) == (1, -1, 0)
    assert line_through((10**30, 1), (10**30 + 1, 2)) == (1, -1, 1 - 10**30)
    assert line_through_rational((Fraction(1, 2), 0), (0, Fraction(1, 3))) == (2, 3, -1)


def test_random():
    rng = random.Random(1637)
    for case in range(3000):
        r = (2, 5, 1000)[case % 3]
        p = (rng.randint(-r, r), rng.randint(-r, r))
        q = (rng.randint(-r, r), rng.randint(-r, r))
        if p == q:
            continue
        l = line_through(p, q)
        assert is_canonical(l)
        assert side(l, p) == 0 and side(l, q) == 0
        # Other points lie on the line exactly when they are collinear with p and q.
        for _ in range(4):
            s = (rng.randint(-r, r), rng.randint(-r, r))
            assert (side(l, s) == 0) == collinear(p, q, s)
        # Any two distinct points of the line give the same triple, in either order.
        d = (q[0] - p[0], q[1] - p[1])
        g = gcd(abs(d[0]), abs(d[1]))
        step = (d[0] // g, d[1] // g)
        i, j = rng.randint(-5, 5), rng.randint(-5, 5)
        if i != j:
            u = (p[0] + i * step[0], p[1] + i * step[1])
            v = (p[0] + j * step[0], p[1] + j * step[1])
            assert line_through(u, v) == l
        assert line_through(q, p) == l
        # The oriented form is positive on the left of p -> q.
        o = oriented_line_through(p, q)
        s = (rng.randint(-r, r), rng.randint(-r, r))
        cr = d[0] * (s[1] - p[1]) - d[1] * (s[0] - p[0])
        assert side(o, s) == (cr > 0) - (cr < 0)
        # Scaling a triple does not change the canonical form.
        k = rng.choice([-3, -1, 2, 7])
        assert line_through_from_coeffs(k * l[0], k * l[1], k * l[2]) == l
        # Rational points: halve every coordinate, the line is the scaled one.
        hp = (Fraction(p[0], 2), Fraction(p[1], 2))
        hq = (Fraction(q[0], 2), Fraction(q[1], 2))
        assert line_through_rational(hp, hq) == line_through_from_coeffs(2 * l[0], 2 * l[1], l[2])
