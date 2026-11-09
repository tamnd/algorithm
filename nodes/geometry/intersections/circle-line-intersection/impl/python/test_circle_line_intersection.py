# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circle-line-intersection/. The authors are listed in prov/SGBK99.jsonl.

import random
from fractions import Fraction
from math import isqrt

import pytest

from circle_line_intersection import QuadPoint, circle_line_intersection, intersection_count


def on_line_exactly(q: QuadPoint, a, b, cc) -> bool:
    # a*(bx + s*ux) + b*(by + s*uy) + cc = 0 for s = sqrt(rad): both parts must vanish.
    rational = a * q.base[0] + b * q.base[1] + cc
    radical = a * q.coef[0] + b * q.coef[1]
    return rational == 0 and (q.rad == 0 or radical == 0)


def on_circle_exactly(q: QuadPoint, c, r) -> bool:
    # |base + s*coef - c|^2 = |base - c|^2 + rad*|coef|^2 + 2 s (base - c).coef.
    w = (q.base[0] - c[0], q.base[1] - c[1])
    rational = w[0] ** 2 + w[1] ** 2 + q.rad * (q.coef[0] ** 2 + q.coef[1] ** 2)
    radical = w[0] * q.coef[0] + w[1] * q.coef[1]
    return rational == r * r and (q.rad == 0 or radical == 0)


def brute(c, r, a, b, cc):
    """Count by the quadratic in a parameter along the line, and the rational points if any."""
    # A point of the line: solve with x or y fixed; then move along (-b, a).
    if b != 0:
        p = (Fraction(0), Fraction(-cc, b))
    else:
        p = (Fraction(-cc, a), Fraction(0))
    d = (-b, a)
    w = (p[0] - c[0], p[1] - c[1])
    qa = d[0] ** 2 + d[1] ** 2
    qb = 2 * (w[0] * d[0] + w[1] * d[1])
    qc = w[0] ** 2 + w[1] ** 2 - r * r
    disc = qb * qb - 4 * qa * qc
    count = 0 if disc < 0 else (1 if disc == 0 else 2)
    pts = None
    num, den = disc.numerator, disc.denominator
    if disc >= 0 and isqrt(num) ** 2 == num and isqrt(den) ** 2 == den:
        s = Fraction(isqrt(num), isqrt(den))
        ts = {(-qb + s) / (2 * qa), (-qb - s) / (2 * qa)}
        pts = {(p[0] + t * d[0], p[1] + t * d[1]) for t in ts}
    return count, pts


def check(c, r, a, b, cc):
    res = circle_line_intersection(c, r, a, b, cc)
    count, pts = brute(c, r, a, b, cc)
    assert len(res) == count == intersection_count(c, r, a, b, cc)
    for q in res:
        assert on_line_exactly(q, a, b, cc)
        assert on_circle_exactly(q, c, r)
    if count == 2:
        assert res[0].coef != (0, 0) and res[0].rad > 0  # two distinct points
    if pts is not None:
        assert {q.rational() for q in res} == pts
    return res


def test_example():
    res = check((0, 0), 5, 1, 1, -7)
    assert {q.rational() for q in res} == {(3, 4), (4, 3)}
    res = check((0, 0), 5, 3, 4, -25)
    assert [q.rational() for q in res] == [(3, 4)]
    assert check((0, 0), 5, 1, 0, -6) == []
    res = check((1, 1), 5, 3, 4, -2)
    assert res[0].base == (Fraction(2, 5), Fraction(1, 5)) and res[0].rad == 600
    assert res[0].coef == (Fraction(-4, 25), Fraction(3, 25))
    x, y = res[0].to_float()
    assert res[0].rational() is None and x < 0 < y


def test_degenerate():
    with pytest.raises(ValueError):
        circle_line_intersection((0, 0), 1, 0, 0, 1)
    with pytest.raises(ValueError):
        circle_line_intersection((0, 0), -1, 1, 0, 0)
    assert [q.rational() for q in check((2, 3), 0, 1, -1, 1)] == [(2, 3)]  # point circle on the line
    assert check((2, 3), 0, 1, 1, 0) == []
    assert {q.rational() for q in check((0, 0), 1, 0, 1, 0)} == {(1, 0), (-1, 0)}  # through the center
    assert {q.rational() for q in check((0, 0), 2, 1, 0, -2)} == {(2, 0)}  # vertical tangent


def test_random():
    rng = random.Random(300)
    for case in range(4000):
        k = (2, 5, 30)[case % 3]
        c = (rng.randint(-k, k), rng.randint(-k, k))
        r = rng.randint(0, k)
        a, b = rng.randint(-k, k), rng.randint(-k, k)
        if (a, b) == (0, 0):
            continue
        if case % 4 == 0:
            # A line at an integer distance from the center, often tangent.
            a, b = rng.choice([(3, 4), (4, -3), (0, 1), (1, 0), (5, 12)])
            n = isqrt(a * a + b * b)
            cc = -(a * c[0] + b * c[1]) + rng.choice([-1, 1]) * n * rng.randint(0, r + 1)
        else:
            cc = rng.randint(-k * k, k * k)
        check(c, r, a, b, cc)
