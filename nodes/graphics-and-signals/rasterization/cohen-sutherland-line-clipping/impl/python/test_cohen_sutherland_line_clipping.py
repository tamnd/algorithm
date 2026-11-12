# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cohen-sutherland-line-clipping/. The authors are listed in prov/4ASC1H.jsonl.

import random
from fractions import Fraction

import pytest

from cohen_sutherland_line_clipping import (
    BOTTOM,
    LEFT,
    RIGHT,
    TOP,
    clip_with_count,
    cohen_sutherland_line_clipping,
    outcode,
)

WINDOW = (0, 0, 10, 10)


def inside(pt, window):
    xmin, ymin, xmax, ymax = window
    return xmin <= pt[0] <= xmax and ymin <= pt[1] <= ymax


def at(p, q, t):
    return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))


def brute_interval(p, q, window):
    """The exact parameter interval [lo, hi] of the segment inside the window, or None.

    The inside set is a closed interval whose end points are 0, 1 or a parameter
    where the segment meets one of the four window lines. Test each candidate.
    """
    xmin, ymin, xmax, ymax = window
    cands = {Fraction(0), Fraction(1)}
    for axis, values in ((0, (xmin, xmax)), (1, (ymin, ymax))):
        d = q[axis] - p[axis]
        if d != 0:
            for v in values:
                t = Fraction(v - p[axis]) / d
                if 0 <= t <= 1:
                    cands.add(t)
    good = sorted(t for t in cands if inside(at(p, q, t), window))
    if not good:
        return None
    return good[0], good[-1]


def check(p, q, window, rng, samples=40):
    got = cohen_sutherland_line_clipping(p, q, window)
    ref = brute_interval(p, q, window)
    if ref is None:
        assert got is None
        for _ in range(samples):
            t = Fraction(rng.randint(0, 1000), 1000)
            assert not inside(at(p, q, t), window)
        return
    lo, hi = ref
    assert got == (at(p, q, lo), at(p, q, hi))
    for _ in range(samples):
        t = Fraction(rng.randint(0, 1000), 1000)
        assert inside(at(p, q, t), window) == (lo <= t <= hi)


def test_outcodes():
    assert outcode((5, 5), WINDOW) == 0
    assert outcode((-1, 5), WINDOW) == LEFT
    assert outcode((11, -1), WINDOW) == RIGHT | BOTTOM
    assert outcode((-1, 11), WINDOW) == LEFT | TOP
    assert outcode((10, 0), WINDOW) == 0


def test_page_example():
    seg, steps = clip_with_count((-4, 2), (14, 11), WINDOW)
    assert seg == ((0, 4), (10, 9))
    assert steps == 3
    seg, steps = clip_with_count((-2, -6), (12, 15), WINDOW)
    assert seg == ((2, 0), (Fraction(26, 3), 10))
    assert steps == 2
    assert clip_with_count((-2, 8), (3, 14), WINDOW) == (None, 1)
    assert clip_with_count((11, 2), (13, 9), WINDOW) == (None, 0)


def test_four_subdivisions():
    # Both end points lie in corner regions, and each needs two cuts.
    seg, steps = clip_with_count((-3, -1), (13, 11), WINDOW)
    assert steps == 4
    assert seg == ((Fraction(0), Fraction(5, 4)), (Fraction(10), Fraction(35, 4)))


def test_degenerate_and_touching():
    assert cohen_sutherland_line_clipping((3, 4), (3, 4), WINDOW) == ((3, 4), (3, 4))
    assert cohen_sutherland_line_clipping((12, 4), (12, 4), WINDOW) is None
    # A segment through a corner only touches the window.
    assert cohen_sutherland_line_clipping((-5, 15), (5, 5), (0, 0, 10, 10)) == ((0, 10), (5, 5))
    seg = cohen_sutherland_line_clipping((-2, 12), (2, 8), WINDOW)
    assert seg == ((0, 10), (2, 8))
    seg = cohen_sutherland_line_clipping((-2, 12), (0, 10), WINDOW)
    assert seg == ((0, 10), (0, 10))
    # A segment along a window edge.
    assert cohen_sutherland_line_clipping((-3, 0), (13, 0), WINDOW) == ((0, 0), (10, 0))


def test_bad_window():
    with pytest.raises(ValueError):
        cohen_sutherland_line_clipping((0, 0), (1, 1), (5, 0, 1, 1))


def test_random_against_brute_force():
    rng = random.Random(20261113)
    for trial in range(3000):
        w = (rng.randint(-5, 5), rng.randint(-5, 5))
        window = (w[0], w[1], w[0] + rng.randint(0, 8), w[1] + rng.randint(0, 8))
        p = (rng.randint(-15, 15), rng.randint(-15, 15))
        q = (rng.randint(-15, 15), rng.randint(-15, 15))
        if trial % 7 == 0:
            p = (Fraction(rng.randint(-60, 60), 4), Fraction(rng.randint(-60, 60), 3))
        check(p, q, window, rng, samples=10)
        assert clip_with_count(p, q, window)[1] <= 4


def test_direction_kept():
    seg = cohen_sutherland_line_clipping((14, 11), (-4, 2), WINDOW)
    assert seg == ((10, 9), (0, 4))
