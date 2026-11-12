# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-point-scheme/. The authors are listed in prov/YTR0BT.jsonl.

import random
from fractions import Fraction

import pytest

from four_point_scheme import four_point

F = Fraction
SQUARE = [(0, 0), (4, 0), (4, 4), (0, 4)]


def neville(ts, ys, t):
    """The value at t of the polynomial through (ts[i], ys[i])."""
    p = [F(y) for y in ys]
    n = len(ts)
    for k in range(1, n):
        for i in range(n - k):
            p[i] = ((t - ts[i + k]) * p[i] + (ts[i] - t) * p[i + 1]) / (ts[i] - ts[i + k])
    return p[0]


def cubic(coef):
    return lambda t: sum(c * t**k for k, c in enumerate(coef))


def test_page_example():
    one = four_point(SQUARE, 1)
    assert one == [
        (0, 0),
        (2, F(-1, 2)),
        (4, 0),
        (F(9, 2), 2),
        (4, 4),
        (2, F(9, 2)),
        (0, 4),
        (F(-1, 2), 2),
    ]
    two = four_point(SQUARE, 2)
    assert two[1] == (F(29, 32), F(-13, 32))
    assert two[3] == (F(99, 32), F(-13, 32))
    assert len(two) == 16


def test_interpolates_old_points():
    rng = random.Random(1)
    for _ in range(300):
        m = rng.randint(3, 8)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(m)]
        w = F(rng.randint(-4, 6), 32)
        for r in (1, 2, 3):
            out = four_point(pts, r, w)
            assert len(out) == m * 2**r
            assert [out[i * 2**r] for i in range(m)] == pts


def test_dubuc_is_cubic_interpolation():
    rng = random.Random(2)
    for _ in range(500):
        m = rng.randint(4, 8)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(m)]
        out = four_point(pts, 1)
        for i in range(m):
            nb = [pts[(i + k) % m] for k in (-1, 0, 1, 2)]
            want = tuple(neville([-1, 0, 1, 2], [p[c] for p in nb], F(1, 2)) for c in range(2))
            assert out[2 * i + 1] == want


def test_reproduces_cubics():
    rng = random.Random(3)
    for _ in range(300):
        f = cubic([F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(4)])
        n = rng.randint(6, 9)
        pts = [(F(i), f(F(i))) for i in range(n)]
        out = four_point(pts, 2, closed=False)
        for x, y in out:
            assert y == f(x)
        xs = [x for x, _ in out]
        assert all(b - a == F(1, 4) for a, b in zip(xs, xs[1:]))


def test_quadratic_only_for_one_sixteenth():
    # For f(t) = t^2 the new value at 1/2 is 1/2 - 4w, which is 1/4 only for w = 1/16.
    pts = [(-1, 1), (0, 0), (1, 1), (2, 4)]
    for w in [F(0), F(1, 32), F(1, 16), F(1, 10), F(1, 8)]:
        out = four_point(pts, 1, w, closed=False)
        assert out[1] == (F(1, 2), F(1, 2) - 4 * w)
        assert (out[1][1] == F(1, 4)) == (w == F(1, 16))


def test_linear_for_every_w():
    rng = random.Random(4)
    for _ in range(200):
        w = F(rng.randint(-8, 8), 16)
        a, b, c = (rng.randint(-5, 5) for _ in range(3))
        pts = [(F(i), F(a * i + b)) for i in range(c + 10)]
        for x, y in four_point(pts, 1, w, closed=False):
            assert y == a * x + b


def test_zero_tension_is_the_polygon():
    out = four_point(SQUARE, 1, F(0))
    assert out[1] == (2, 0) and out[3] == (4, 2)


def test_open_counts_and_errors():
    out = four_point([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], 1, closed=False)
    assert len(out) == 2 * 5 - 5
    with pytest.raises(ValueError):
        four_point([(0, 0), (1, 1)], 1)
    with pytest.raises(ValueError):
        four_point([(0, 0), (1, 1), (2, 2)], 1, closed=False)
    with pytest.raises(ValueError):
        four_point(SQUARE, -1)
    assert four_point(SQUARE, 0) == SQUARE
