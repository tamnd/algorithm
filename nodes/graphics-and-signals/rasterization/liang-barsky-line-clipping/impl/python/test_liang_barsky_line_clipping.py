# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liang-barsky-line-clipping/. The authors are listed in prov/CW3RQ3.jsonl.

import random
from fractions import Fraction

import pytest

from liang_barsky_line_clipping import clip_parameters, liang_barsky_line_clipping

WINDOW = (0, 0, 10, 10)


def inside(pt, window):
    xmin, ymin, xmax, ymax = window
    return xmin <= pt[0] <= xmax and ymin <= pt[1] <= ymax


def at(p, q, t):
    return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))


def brute_interval(p, q, window):
    """The exact parameter interval of the segment inside the window, or None.

    The inside set is a closed interval whose end points are 0, 1 or a parameter
    where the segment meets one of the four window lines. Test each candidate
    point exactly, with no entering or leaving logic.
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


def test_page_example():
    assert clip_parameters((-3, -1), (13, 11), WINDOW) == (Fraction(3, 16), Fraction(13, 16))
    assert liang_barsky_line_clipping((-3, -1), (13, 11), WINDOW) == (
        (0, Fraction(5, 4)),
        (10, Fraction(35, 4)),
    )
    # Rejected when the entering parameter passes the leaving one.
    assert clip_parameters((-2, 8), (3, 14), WINDOW) is None


def test_parallel_cases():
    assert liang_barsky_line_clipping((-3, 4), (13, 4), WINDOW) == ((0, 4), (10, 4))
    assert liang_barsky_line_clipping((-3, 12), (13, 12), WINDOW) is None
    assert liang_barsky_line_clipping((5, -2), (5, 3), WINDOW) == ((5, 0), (5, 3))
    assert liang_barsky_line_clipping((3, 4), (3, 4), WINDOW) == ((3, 4), (3, 4))
    assert liang_barsky_line_clipping((12, 4), (12, 4), WINDOW) is None
    # On a window edge counts as inside.
    assert liang_barsky_line_clipping((-3, 10), (13, 10), WINDOW) == ((0, 10), (10, 10))


def test_corner_touch():
    assert liang_barsky_line_clipping((-2, 12), (0, 10), WINDOW) == ((0, 10), (0, 10))
    assert liang_barsky_line_clipping((-5, 5), (5, 15), WINDOW) == ((0, 10), (0, 10))


def test_bad_window():
    with pytest.raises(ValueError):
        liang_barsky_line_clipping((0, 0), (1, 1), (0, 5, 1, 1))


def test_random_against_brute_force():
    rng = random.Random(1984)
    for trial in range(4000):
        x0, y0 = rng.randint(-5, 5), rng.randint(-5, 5)
        window = (x0, y0, x0 + rng.randint(0, 8), y0 + rng.randint(0, 8))
        p = (rng.randint(-15, 15), rng.randint(-15, 15))
        q = (rng.randint(-15, 15), rng.randint(-15, 15))
        if trial % 5 == 0:
            q = (Fraction(rng.randint(-60, 60), 7), Fraction(rng.randint(-60, 60), 2))
        if trial % 11 == 0:
            q = (p[0], q[1])  # vertical
        got = liang_barsky_line_clipping(p, q, window)
        ref = brute_interval(p, q, window)
        if ref is None:
            assert got is None
        else:
            assert got == (at(p, q, ref[0]), at(p, q, ref[1]))
        lo_hi = clip_parameters(p, q, window)
        for _ in range(10):
            t = Fraction(rng.randint(0, 997), 997)
            expect = lo_hi is not None and lo_hi[0] <= t <= lo_hi[1]
            assert inside(at(p, q, t), window) == expect


def test_direction_kept():
    assert liang_barsky_line_clipping((13, 11), (-3, -1), WINDOW) == (
        (10, Fraction(35, 4)),
        (0, Fraction(5, 4)),
    )
