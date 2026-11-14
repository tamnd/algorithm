# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paving/. The authors are listed in prov/AS3MCY.jsonl.

import math
import random
from fractions import Fraction as F

from mg3geom import boundary_edges, exact, is_valid_planar_mesh, orient2d, twice_area
from paving import classify, is_simple_polygon, pave_row, quad_count_parity


def rect_front(W, H):
    """The counterclockwise boundary of [0, W] x [0, H] with unit spacing."""
    return ([(float(i), 0.0) for i in range(W)] + [(float(W), float(j)) for j in range(H)]
            + [(float(W - i), float(H)) for i in range(W)] + [(0.0, float(H - j)) for j in range(H)])


def round_front(rng, n, radius):
    angles = [2 * math.pi * (i + rng.uniform(-0.2, 0.2)) / n for i in range(n)]
    return [(radius * math.cos(t) * rng.uniform(0.97, 1.03), radius * math.sin(t) * rng.uniform(0.97, 1.03))
            for t in angles]


def inside_quad(q, x):
    return all(orient2d(q[s], q[(s + 1) % 4], x) > 0 for s in range(4))


def check_row(front, points, quads, new_front):
    E = [exact(p) for p in points]
    n = len(front)
    assert is_valid_planar_mesh(E, quads)                        # strictly convex, no inverted quad
    inner = [E[k] for k in new_front]
    assert is_simple_polygon(inner)                               # the new front is simple
    # area identity, exact: the row fills the region between the two fronts
    assert sum(orient2d(E[q[0]], E[q[1]], E[q[2]]) + orient2d(E[q[0]], E[q[2]], E[q[3]]) for q in quads) \
        == twice_area(E[:n]) - twice_area(inner)
    assert twice_area(inner) > 0
    # the boundary of the row is the old front plus the new front reversed
    m = len(new_front)
    expected = {(i, (i + 1) % n) for i in range(n)} | {(new_front[(j + 1) % m], new_front[j]) for j in range(m)}
    assert set(boundary_edges(quads)) == expected
    # parity: 4 Q = 2 E_int + E_bnd, so the fronts keep the parity of their length
    four_q, interior, bnd = quad_count_parity(quads)
    assert four_q == 2 * interior + bnd and bnd == n + m and (n - m) % 2 == 0


def test_square_row_is_the_outer_ring_of_the_grid():
    front = rect_front(4, 4)
    assert classify(front).count("end") == 4
    points, quads, new_front, why = pave_row(front)
    assert why is None and len(quads) == 12
    check_row(front, points, quads, new_front)
    got = {frozenset(points[i] for i in q) for q in quads}
    ring = {frozenset({(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)})
            for x in range(4) for y in range(4) if x in (0, 3) or y in (0, 3)}
    assert got == {frozenset((float(a), float(b)) for a, b in s) for s in ring}
    assert sorted(points[k] for k in new_front) == sorted(
        (float(x), float(y)) for x in (1, 2, 3) for y in (1, 2, 3) if (x, y) != (2, 2))


def test_rows_on_rectangles_and_round_fronts():
    for W, H in ((6, 3), (5, 4), (7, 7)):
        front = rect_front(W, H)
        points, quads, new_front, why = pave_row(front)
        assert why is None and len(quads) == 2 * (W + H) - 4
        check_row(front, points, quads, new_front)
    rng = random.Random(4)
    done = 0
    for _ in range(30):
        front = round_front(rng, rng.randint(12, 24), rng.uniform(3, 6))
        points, quads, new_front, why = pave_row(front)
        if why is None:
            check_row(front, points, quads, new_front)
            done += 1
    assert done >= 20


def test_no_point_is_in_two_quads():
    rng = random.Random(5)
    front = round_front(rng, 16, 4.0)
    points, quads, new_front, why = pave_row(front)
    assert why is None
    E = [exact(p) for p in points]
    for _ in range(4000):
        x = (F(rng.randint(-5000, 5000), 1000), F(rng.randint(-5000, 5000), 1000))
        assert sum(inside_quad([E[i] for i in q], x) for q in quads) <= 1


def test_failure_is_reported():
    # the inner 2 x 2 square: its row ends are neighbours of neighbours
    points, quads, new_front, why = pave_row(rect_front(2, 2))
    assert points is None and "too close" in why
    # a front with a reflex node
    L_shape = [(0.0, 0.0), (2.0, 0.0), (4.0, 0.0), (4.0, 2.0), (2.0, 2.0), (2.0, 4.0), (0.0, 4.0), (0.0, 2.0)]
    points, quads, new_front, why = pave_row(L_shape)
    assert points is None and "reflex" in why
    # a strip of width 1 with nodes 2 apart on the long sides: the rows from both
    # sides are 2 high, they cross, and the new front is not simple
    strip = [(0.0, 0.0), (2.0, 0.0), (4.0, 0.0), (6.0, 0.0), (8.0, 0.0), (8.0, 1 / 3), (8.0, 2 / 3), (8.0, 1.0),
             (6.0, 1.0), (4.0, 1.0), (2.0, 1.0), (0.0, 1.0), (0.0, 2 / 3), (0.0, 1 / 3)]
    points, quads, new_front, why = pave_row(strip)
    assert points is None and "not simple" in why
    # the same strip, 4.5 wide, takes a row
    wide = [(x, y * 4.5) for x, y in strip]
    points, quads, new_front, why = pave_row(wide)
    assert why is None
    check_row(wide, points, quads, new_front)
