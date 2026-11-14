# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-map-model/. The authors are listed in prov/5REJ5X.jsonl.

import random
from fractions import Fraction as F

from z_map_model import ZMap, lowest_point

EPS = 1e-9


def min_quadratic(a, b, lo, hi):
    """Least value of |a + t b|^2 for t in [lo, hi], exact (a, b are tuples of Fraction)."""
    bb = sum(x * x for x in b)
    t = lo if bb == 0 else min(max(-sum(x * y for x, y in zip(a, b)) / bb, lo), hi)
    return sum((x + t * y) ** 2 for x, y in zip(a, b))


def removed(p, c0, c1, r):
    """Exact test: is the point p in the volume swept by the ball-end tool?

    The tool is the ball of radius r about c(t) plus the half-infinite
    cylinder of radius r above c(t). All numbers are Fractions.
    """
    v = tuple(c1[i] - c0[i] for i in range(3))
    w = tuple(c0[i] - p[i] for i in range(3))
    if min_quadratic(w, v, F(0), F(1)) <= r * r:  # the ball
        return True
    s, dz = v[2], p[2] - c0[2]  # the shank needs c_z(t) <= p_z
    if s == 0:
        if dz < 0:
            return False
        lo, hi = F(0), F(1)
    elif s > 0:
        lo, hi = F(0), min(F(1), dz / s)
    else:
        lo, hi = max(F(0), dz / s), F(1)
    if lo > hi:
        return False
    return min_quadratic(w[:2], v[:2], lo, hi) <= r * r


def check_column(q, c0, c1, r):
    """Compare lowest_point with the exact membership test on the line at q."""
    z = lowest_point(tuple(map(float, q)), tuple(map(float, c0)), tuple(map(float, c1)), float(r))
    if z is None:
        assert not removed((q[0], q[1], F(10 ** 6)), c0, c1, r)
        return
    assert removed((q[0], q[1], F(z + EPS)), c0, c1, r)
    assert not removed((q[0], q[1], F(z - EPS)), c0, c1, r)


def rand_point(rng, lo, hi, den=4):
    return tuple(F(rng.randint(lo * den, hi * den), den) for _ in range(3))


def test_example():
    c0, c1, r = (1.0, 1.0, 3.0), (5.0, 1.0, 1.0), 2.0
    # on the path line the cut is sqrt(1 + m^2) r = sqrt(5) below the axis (slope m = -1/2)
    for x, axis in ((1.0, 3.0), (2.0, 2.5), (3.0, 2.0), (4.0, 1.5)):
        assert abs(lowest_point((x, 1.0), c0, c1, r) - (axis - 5 ** 0.5)) < 1e-12
    # under the end center: the bottom of the end ball
    assert abs(lowest_point((5.0, 1.0), c0, c1, r) - (-1.0)) < 1e-12
    # behind the start and after the end: the end balls
    assert abs(lowest_point((0.0, 1.0), c0, c1, r) - (3.0 - 3 ** 0.5)) < 1e-12
    assert abs(lowest_point((6.0, 1.0), c0, c1, r) - (1.0 - 3 ** 0.5)) < 1e-12
    # a column 2 away from the path line only touches the ball equator
    assert abs(lowest_point((3.0, 3.0), c0, c1, r) - 2.0) < 1e-12
    assert lowest_point((3.0, 3.5), c0, c1, r) is None


def test_lowest_point_against_exact_membership():
    rng = random.Random(5)
    for _ in range(400):
        c0, c1 = rand_point(rng, -3, 3), rand_point(rng, -3, 3)
        if rng.random() < 0.2:
            c1 = (c0[0], c0[1], c1[2])  # a vertical plunge or retract
        if rng.random() < 0.1:
            c1 = (c1[0], c1[1], c0[2])  # a horizontal move
        r = F(rng.randint(2, 8), 4)
        for _ in range(8):
            q = tuple(F(rng.randint(-20, 20), 4) for _ in range(2))
            check_column(q, c0, c1, r)


def test_zmap_cut_against_exact_membership():
    rng = random.Random(17)
    for _ in range(6):
        zm = ZMap(13, 9, 0.5, 3.0, bottom=-4.0)
        moves = [rand_point(rng, 0, 6) for _ in range(4)]
        r = F(rng.randint(2, 6), 4)
        zm.cut_path([tuple(map(float, c)) for c in moves], float(r))
        for i in range(zm.nx):
            for j in range(zm.ny):
                q = (F(i, 2), F(j, 2))
                H = zm.H[i][j]
                def gone(z):
                    p = (q[0], q[1], F(z))
                    return any(removed(p, a, b, r) for a, b in zip(moves, moves[1:]))
                # every point of the column below H is stock, the top is cut or the original top
                if H < 3.0 - EPS:
                    assert gone(H + EPS)
                    if H > -4.0 + EPS:
                        assert not gone(H - EPS)
                else:
                    assert not gone(3.0 - EPS)


def test_volume_and_inside():
    zm = ZMap(4, 3, 1.0, 2.0)
    assert zm.volume() == 4 * 3 * 2.0
    zm.cut_ball_move((0.0, 0.0, 1.5), (3.0, 0.0, 1.5), 0.5)
    assert all(abs(zm.H[i][0] - 1.0) < 1e-12 for i in range(4))
    assert all(zm.H[i][j] == 2.0 for i in range(4) for j in (1, 2))
    assert zm.inside(0, 0, 0.5) and not zm.inside(0, 0, 1.5)
    assert abs(zm.volume() - (24.0 - 4.0)) < 1e-12


def test_cut_is_monotone_and_order_free():
    rng = random.Random(23)
    for _ in range(10):
        moves = [tuple(float(x) for x in rand_point(rng, 0, 5)) for _ in range(5)]
        a, b = ZMap(11, 11, 0.5, 4.0, bottom=-5.0), ZMap(11, 11, 0.5, 4.0, bottom=-5.0)
        a.cut_path(moves, 1.0)
        pairs = list(zip(moves, moves[1:]))
        rng.shuffle(pairs)
        for c0, c1 in pairs:
            b.cut_ball_move(c0, c1, 1.0)
        assert a.H == b.H
