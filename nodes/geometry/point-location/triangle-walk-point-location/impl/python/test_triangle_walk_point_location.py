# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-walk-point-location/. The authors are listed in prov/47K91B.jsonl.

import random

import pytest

from triangle_walk_point_location import Triangulation, WalkLoops, classify, in_closed, incircle, lawson_delaunay, orient

PINWHEEL = [
    ((12, 1), (5, 7), (7, 1)),
    ((0, 14), (5, 7), (14, 0)),
    ((12, 1), (14, 0), (5, 7)),
    ((14, 0), (12, 1), (0, 0)),
    ((7, 1), (0, 0), (12, 1)),
    ((0, 0), (7, 1), (0, 14)),
    ((5, 7), (0, 14), (7, 1)),
]


def reference(tris, q):
    """Linear scan over the triangles."""
    for i, t in enumerate(tris):
        if in_closed(t, q):
            return classify(t, i, q)
    return ("outside",)


def insert_point(tris, p):
    """Insert p into a triangulation (list of ccw triangles) by splitting the triangle or edge."""
    for t in tris:
        if p in t:
            return
    for k, t in enumerate(tris):
        if in_closed(t, p):
            a, b, c = t
            sides = [orient(a, b, p), orient(b, c, p), orient(c, a, p)]
            if all(s > 0 for s in sides):
                tris[k : k + 1] = [(a, b, p), (b, c, p), (c, a, p)]
                return
            j = sides.index(0)
            u, w = t[j], t[(j + 1) % 3]
            break
    out = []
    for t in tris:
        if u in t and w in t:
            i = t.index(u)
            if t[(i + 1) % 3] == w:
                x = t[(i + 2) % 3]
                out += [(u, p, x), (p, w, x)]
            else:
                x = t[(i + 1) % 3]
                out += [(u, x, p), (x, w, p)]
        else:
            out.append(t)
    tris[:] = out


def random_flips(tris, rng, count):
    for _ in range(count):
        t = rng.choice(tris)
        k = rng.randrange(3)
        a, b, c = t[k], t[(k + 1) % 3], t[(k + 2) % 3]
        other = [s for s in tris if s is not t and a in s and b in s]
        if not other:
            continue
        s = other[0]
        d = next(p for p in s if p != a and p != b)
        if orient(c, d, a) * orient(c, d, b) < 0 and orient(a, b, c) * orient(a, b, d) < 0:
            tris.remove(t)
            tris.remove(s)
            tris += [(c, a, d), (c, d, b)] if orient(c, a, d) > 0 else [(c, d, a), (c, b, d)]


def random_triangulation(rng, g, m, flips):
    """A triangulation of the triangle (0,0), (g,0), (0,g), with random rotations of the stored triangles."""
    tris = [((0, 0), (g, 0), (0, g))]
    for _ in range(m):
        x = rng.randint(1, g - 2)
        y = rng.randint(1, g - 1 - x)
        insert_point(tris, (x, y))
    random_flips(tris, rng, flips)
    tris = [t if orient(*t) > 0 else (t[0], t[2], t[1]) for t in tris]
    return [t[k:] + t[:k] for t in tris for k in [rng.randrange(3)]]


def grid_triangulation(rng, w, h):
    """Unit squares of a grid, each cut by a random diagonal: many collinear and cocircular vertices."""
    tris = []
    for x in range(w):
        for y in range(h):
            a, b, c, d = (x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)
            tris += [(a, b, c), (a, c, d)] if rng.random() < 0.5 else [(a, b, d), (b, c, d)]
    return tris


def is_locally_delaunay(T):
    for (u, w), i in T.owner.items():
        j = T.neighbor(u, w)
        if j is None:
            continue
        t, s = T.tris[i], T.tris[j]
        c = t[(t.index(u) + 2) % 3]
        d = s[(s.index(w) + 2) % 3]
        if incircle(u, w, c, d) > 0:
            return False
    return True


def test_walks_against_linear_scan():
    rng = random.Random(2002)
    for _ in range(60):
        g = rng.randint(3, 12)
        tris = random_triangulation(rng, g, rng.randint(0, 20), rng.randint(0, 30))
        T = Triangulation(tris)
        for x in range(-1, g + 2):
            for y in range(-1, g + 2):
                q = (x, y)
                want = reference(T.tris, q)
                start = rng.randrange(len(tris))
                assert T.straight_walk(q, start) == want
                assert T.steps <= len(tris) and len(set(T.path)) == len(T.path)
                assert T.stochastic_walk(q, rng, start) == want
                try:
                    assert T.visibility_walk(q, start) == want
                except WalkLoops:
                    assert not is_locally_delaunay(T)


def test_lawson_flips_give_a_delaunay_triangulation():
    rng = random.Random(1977)
    for _ in range(30):
        g = rng.randint(4, 20)
        tris = random_triangulation(rng, g, rng.randint(0, 25), rng.randint(0, 40))
        D = Triangulation(lawson_delaunay(tris))
        assert is_locally_delaunay(D)
        assert sum(orient(*t) for t in D.tris) == g * g


def test_visibility_walk_never_loops_in_a_delaunay_triangulation():
    rng = random.Random(1990)
    for _ in range(25):
        g = rng.randint(4, 25)
        T = Triangulation(lawson_delaunay(random_triangulation(rng, g, rng.randint(0, 30), 30)))
        for _ in range(40):
            q = (rng.randint(-2, g + 2), rng.randint(-2, g + 2))
            for start in range(len(T.tris)):
                assert T.visibility_walk(q, start) == reference(T.tris, q)  # raises WalkLoops on a loop
                assert T.steps <= len(T.tris) and len(set(T.path)) == len(T.path)


def test_grids_with_degenerate_points():
    # vertical and horizontal edges, collinear vertices on the walk line, cocircular squares
    rng = random.Random(4)
    for _ in range(8):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        T = Triangulation(grid_triangulation(rng, w, h))
        assert is_locally_delaunay(T)  # every diagonal of a unit square is locally Delaunay
        for x2 in range(-2, 2 * w + 3):
            for y2 in range(-2, 2 * h + 3):
                if x2 % 2 or y2 % 2:
                    continue
                q = (x2 // 2, y2 // 2)
                want = reference(T.tris, q)
                for start in range(0, len(T.tris), 3):
                    assert T.straight_walk(q, start) == want
                    assert T.visibility_walk(q, start) == want
                    assert T.stochastic_walk(q, rng, start) == want


def test_pinwheel_makes_the_visibility_walk_loop():
    T = Triangulation(PINWHEEL)
    assert not is_locally_delaunay(T)
    q = (9, 2)
    with pytest.raises(WalkLoops):
        T.visibility_walk(q, 1)
    assert T.path == [1, 2, 3, 4, 5, 6, 1]
    assert T.straight_walk(q, 1) == ("triangle", 0)
    rng = random.Random(7)
    for _ in range(200):
        assert T.stochastic_walk(q, rng, 1, max_steps=500) == ("triangle", 0)
    D = Triangulation(lawson_delaunay(PINWHEEL))
    for start in range(7):
        assert D.visibility_walk(q, start) == ("triangle", 0)


def test_worked_example_straight_walk():
    T = Triangulation(PINWHEEL)
    assert T.straight_walk((2, 2), 1) == ("triangle", 5)
    assert T.path == [1, 2, 0, 6, 5]
    assert T.straight_walk((10, 1), 1) == ("edge", ((7, 1), (12, 1)))
    assert T.straight_walk((5, 7), 3) == ("vertex", (5, 7))
    assert T.straight_walk((20, 3), 5) == ("outside",)


def test_max_steps_and_bad_input():
    T = Triangulation(PINWHEEL)
    with pytest.raises(RuntimeError):
        T.stochastic_walk((9, 2), random.Random(0), 1, max_steps=0)
    with pytest.raises(ValueError):
        Triangulation([((0, 0), (1, 1), (2, 2))])
