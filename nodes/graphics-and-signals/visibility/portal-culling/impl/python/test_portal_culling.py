# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/portal-culling/. The authors are listed in prov/52EA3Z.jsonl.

import random
from fractions import Fraction

from portal_culling import cross, grid_portals, meet, portal_cull

EX_DOORS = {('v', 1, 1), ('v', 2, 1), ('h', 1, 2), ('h', 2, 1), ('v', 3, 1), ('v', 2, 0), ('h', 3, 2)}
EX_EYE = (Fraction(1, 2), Fraction(3, 2))
EX_VIEW = ((4, -1), (4, 1))


def walls(width, height, doors):
    """Each unit edge of the grid that is not a door, as a closed segment."""
    out = []
    for x in range(width + 1):
        for y in range(height):
            if ('v', x, y) not in doors:
                out.append(((x, y), (x, y + 1)))
    for x in range(width):
        for y in range(height + 1):
            if ('h', x, y) not in doors:
                out.append(((x, y), (x + 1, y)))
    return out


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_meet(p, q, a, b):
    """Do the closed segments pq and ab share a point? Exact."""
    o1, o2, o3, o4 = orient(p, q, a), orient(p, q, b), orient(a, b, p), orient(a, b, q)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True
    return ((o1 == 0 and on_segment(p, q, a)) or (o2 == 0 and on_segment(p, q, b))
            or (o3 == 0 and on_segment(a, b, p)) or (o4 == 0 and on_segment(a, b, q)))


def sees(eye, x, wall_list):
    return not any(segments_meet(eye, x, a, b) for a, b in wall_list)


def in_open_cone(cone, d):
    return cross(cone[0], d) > 0 and cross(d, cone[1]) > 0


def witness(eye, cell, cone, wall_list):
    """Find a point of the cell interior that the eye sees along a direction inside the cone."""
    a, b = cone
    for s, t in ((1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)):
        d = (s * a[0] + t * b[0], s * a[1] + t * b[1])
        lo, hi = Fraction(0), None
        ok = True
        for k in range(2):
            if d[k] == 0:
                if not cell[k] < eye[k] < cell[k] + 1:
                    ok = False
                continue
            t0, t1 = Fraction(cell[k] - eye[k], d[k]), Fraction(cell[k] + 1 - eye[k], d[k])
            t0, t1 = min(t0, t1), max(t0, t1)
            lo, hi = max(lo, t0), t1 if hi is None else min(hi, t1)
        if not ok or hi is None or lo >= hi:
            continue
        tm = (lo + hi) / 2
        x = (eye[0] + tm * d[0], eye[1] + tm * d[1])
        if sees(eye, x, wall_list):
            return True
    return False


def test_worked_example():
    portals = grid_portals(4, 3, EX_DOORS)
    visible, visits = portal_cull(portals, (0, 1), EX_EYE, EX_VIEW)
    assert sorted(visible) == [(0, 1), (1, 1), (2, 0), (2, 1), (3, 1), (3, 2)]
    F = Fraction
    assert visits == [
        ((0, 1), ((4, -1), (4, 1))),
        ((1, 1), ((4, -1), (4, 1))),
        ((2, 1), ((4, -1), (4, 1))),
        ((2, 0), ((4, -1), (F(5, 2), F(-1, 2)))),
        ((3, 1), ((F(5, 2), F(-1, 2)), (F(5, 2), F(1, 2)))),
        ((3, 2), ((F(7, 2), F(1, 2)), (F(5, 2), F(1, 2)))),
    ]
    # (1, 2) is behind a door whose cone misses the view; (1, 0) is behind a door that faces away.
    w = walls(4, 3, EX_DOORS)
    for cell, cone in visits[1:]:
        assert witness(EX_EYE, cell, cone, w)


def random_case(rng):
    width, height = rng.randint(2, 6), rng.randint(2, 5)
    doors = set()
    for x in range(1, width):
        for y in range(height):
            if rng.random() < 0.6:
                doors.add(('v', x, y))
    for x in range(width):
        for y in range(1, height):
            if rng.random() < 0.6:
                doors.add(('h', x, y))
    start = (rng.randrange(width), rng.randrange(height))
    eye = (start[0] + Fraction(rng.randint(1, 6), 7), start[1] + Fraction(rng.randint(1, 6), 7))
    while True:
        a = (rng.randint(-5, 5), rng.randint(-5, 5))
        b = (rng.randint(-5, 5), rng.randint(-5, 5))
        if cross(a, b) > 0:
            break
    return width, height, doors, start, eye, (a, b)


def test_never_drops_a_visible_cell_and_each_kept_cell_is_seen():
    rng = random.Random(61)
    pruned = 0
    for case in range(500):
        width, height, doors, start, eye, view = random_case(rng)
        visible, visits = portal_cull(grid_portals(width, height, doors), start, eye, view)
        w = walls(width, height, doors)
        interior = [s for s in w if not (s[0][0] == s[1][0] in (0, width) or s[0][1] == s[1][1] in (0, height))]
        for _ in range(40):
            cell = (rng.randrange(width), rng.randrange(height))
            x = (cell[0] + Fraction(rng.randint(1, 99), 100), cell[1] + Fraction(rng.randint(1, 99), 100))
            d = (x[0] - eye[0], x[1] - eye[1])
            if in_open_cone(view, d) and sees(eye, x, interior):
                assert cell in visible
        for cell, cone in visits[1:]:
            assert witness(eye, cell, cone, interior)
        reach = {start}
        stack = [start]
        portals = grid_portals(width, height, doors)
        while stack:
            for _, _, n in portals[stack.pop()]:
                if n not in reach:
                    reach.add(n)
                    stack.append(n)
        assert visible <= reach
        pruned += len(reach) - len(visible)
    assert pruned > 0


def test_orientation_test_stops_the_walk_back():
    # Without the test of line L5, the walk goes back through the portal it came from, forever.
    portals = grid_portals(2, 1, {('v', 1, 0)})
    eye = (Fraction(1, 2), Fraction(1, 2))
    view = ((1, -1), (1, 1))
    stack, pushes = [((0, 0), view)], 0
    while stack and pushes < 200:
        c, cone = stack.pop()
        for p, q, c2 in portals[c]:
            a, b = (p[0] - eye[0], p[1] - eye[1]), (q[0] - eye[0], q[1] - eye[1])
            if cross(a, b) < 0:
                a, b = b, a  # an unoriented portal
            k = meet(cone, (a, b))
            if k is not None:
                stack.append((c2, k))
                pushes += 1
    assert pushes == 200
    assert portal_cull(portals, (0, 0), eye, view)[0] == {(0, 0), (1, 0)}


def test_edges():
    assert portal_cull(grid_portals(3, 3, set()), (1, 1), (Fraction(3, 2), Fraction(3, 2)), ((1, 0), (0, 1)))[0] == {(1, 1)}
    # A door outside the view cone is not used.
    portals = grid_portals(2, 1, {('v', 1, 0)})
    assert portal_cull(portals, (0, 0), (Fraction(1, 2), Fraction(1, 2)), ((-1, 1), (-1, -1)))[0] == {(0, 0)}
    # A cone that only touches a door at one ray is empty.
    assert meet(((1, 0), (1, 1)), ((1, 1), (0, 1))) is None
    assert meet(((1, 0), (0, 1)), ((1, 1), (-1, 1))) == ((1, 1), (0, 1))
