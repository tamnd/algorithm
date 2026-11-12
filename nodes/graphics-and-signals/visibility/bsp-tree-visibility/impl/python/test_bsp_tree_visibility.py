# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bsp-tree-visibility/. The authors are listed in prov/Q78XXG.jsonl.

import random
from fractions import Fraction

from bsp_tree_visibility import bsp_front_to_back, bsp_paint, build_bsp, tree_size

W, H = 6, 5


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def hit_triangle(tri, e, s):
    """Solve e + t d = A + u (B - A) + v (C - A) by Cramer's rule; closed triangle, t > 0."""
    a, b, c = [tuple(Fraction(x) for x in p) for p in tri]
    d = tuple(s[k] - e[k] for k in range(3))
    e1 = tuple(b[k] - a[k] for k in range(3))
    e2 = tuple(c[k] - a[k] for k in range(3))
    rhs = tuple(e[k] - a[k] for k in range(3))
    m = det3(e1, e2, tuple(-x for x in d))
    if m == 0:
        return None
    u = det3(rhs, e2, tuple(-x for x in d)) / m
    v = det3(e1, rhs, tuple(-x for x in d)) / m
    t = det3(e1, e2, rhs) / m
    if u >= 0 and v >= 0 and u + v <= 1 and t > 0:
        return t
    return None


def brute(tris, e, w=W, h=H):
    """Nearest hit per pixel over all triangles. None marks a tie."""
    img = [[-1] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            s = (Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2), Fraction(0))
            hits = [(t, k) for k, tri in enumerate(tris) if (t := hit_triangle(tri, e, s)) is not None]
            if hits:
                best = min(t for t, _ in hits)
                win = [k for t, k in hits if t == best]
                img[j][i] = win[0] if len(win) == 1 else None
    return img


def agrees(img, ref):
    return all(r is None or r == g for rr, gg in zip(ref, img) for r, g in zip(rr, gg))


def random_triangle(rng):
    while True:
        tri = [(rng.randint(-2, W + 2), rng.randint(-2, H + 2), rng.randint(-8, -1)) for _ in range(3)]
        a, b, c = tri
        u = [b[k] - a[k] for k in range(3)]
        v = [c[k] - a[k] for k in range(3)]
        if any(x != 0 for x in (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])):
            return tri


def random_eye(rng):
    while True:
        e = (Fraction(rng.randint(-20, 4 * W + 20), 4), Fraction(rng.randint(-20, 4 * H + 20), 4), Fraction(rng.randint(-40, 40), 4))
        if e[2] != 0:
            return e


STRIPS = [
    [(0, 1, -7), (8, 1, -5), (8, 2, -5), (0, 2, -7)],
    [(5, 0, -8), (6, 0, -8), (2, 6, -4), (1, 6, -4)],
    [(1, 0, -4), (2, 0, -4), (7, 6, -10), (6, 6, -10)],
]


def brute_polys(polys, e, w, h):
    """Nearest hit over the fan triangles of convex polygons; a tie needs two polygons."""
    img = [[-1] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            s = (Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2), Fraction(0))
            hits = set()
            for k, p in enumerate(polys):
                for a in range(1, len(p) - 1):
                    t = hit_triangle([p[0], p[a], p[a + 1]], e, s)
                    if t is not None:
                        hits.add((t, k))
            if hits:
                best = min(t for t, _ in hits)
                win = {k for t, k in hits if t == best}
                img[j][i] = win.pop() if len(win) == 1 else None
    return img


def test_worked_example():
    tree = build_bsp(STRIPS)
    assert tree_size(tree) == 6
    above = ["4 12/5 -32/5", "5 0 -8", "108/29 60/29 -176/29", "0 1 -7", "4 3 -6", "1 0 -4"]
    for e, firsts in [((4, 3, 40), above), ((4, 3, -60), above[::-1])]:
        order, img = bsp_paint(tree, e, 8, 6)
        assert [" ".join(map(str, f.verts[0])) for f in order] == firsts
        ref = brute_polys(STRIPS, e, 8, 6)
        assert all(x is not None for row in ref for x in row)
        assert img == ref
        drawn, img2 = bsp_front_to_back(tree, e, 8, 6)
        assert img2 == ref
    rows = ["".join("." if k < 0 else str(k + 1) for k in row) for row in reversed(bsp_paint(tree, (4, 3, 40), 8, 6)[1])]
    assert rows == [".2......", "..2..3..", "...23...", "...2....", ".1311111", ".3...2.."]


def test_one_tree_serves_each_viewpoint():
    rng = random.Random(21)
    for _ in range(40):
        tris = [random_triangle(rng) for _ in range(rng.randint(1, 5))]
        tree = build_bsp(tris)
        for _ in range(3):
            e = random_eye(rng)
            ref = brute(tris, e)
            order, img = bsp_paint(tree, e, W, H)
            assert agrees(img, ref)
            assert len(order) == tree_size(tree)
            _, img2 = bsp_front_to_back(tree, e, W, H)
            assert agrees(img2, ref)


def test_random_scenes_match_brute_force():
    rng = random.Random(22)
    for case in range(500):
        tris = [random_triangle(rng) for _ in range(rng.randint(1, 4))]
        tree = build_bsp(tris)
        e = random_eye(rng)
        order, img = bsp_paint(tree, e, W, H)
        assert agrees(img, brute(tris, e))
        if case % 4:
            continue
        # The order is valid: along each pixel ray, a fragment met earlier in the order is not nearer.
        pts = [(Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2), Fraction(0)) for j in range(H) for i in range(W)]
        for s in pts:
            ts = [hit_triangle_frag(f, e, s) for f in order]
            seen = [t for t in ts if t is not None]
            assert all(seen[k] >= seen[k + 1] for k in range(len(seen) - 1))


def hit_triangle_frag(f, e, s):
    """Fan triangulation of a convex fragment, tested with the independent triangle test."""
    v = f.verts
    hits = [hit_triangle([v[0], v[k], v[k + 1]], e, s) for k in range(1, len(v) - 1)]
    hits = [t for t in hits if t is not None]
    return min(hits) if hits else None


def test_front_to_back_stops_early():
    wall = [[(-5, -5, -1), (20, -5, -1), (20, 20, -1)], [(-5, -5, -1), (20, 20, -1), (-5, 20, -1)]]
    behind = [[(0, 0, -5 - k), (4, 0, -5 - k), (0, 4, -5 - k)] for k in range(5)]
    tris = behind + wall
    tree = build_bsp(tris)
    e = (3, 2, 5)
    drawn, img = bsp_front_to_back(tree, e, W, H)
    assert agrees(img, brute(tris, e))
    assert drawn == 2


def test_wrong_side_gives_front_to_back_paint():
    # Painting in the front-to-back order with overwrites shows the farthest polygon.
    near = [(0, 0, -1), (6, 0, -1), (0, 5, -1)]
    far = [(0, 0, -3), (6, 0, -3), (0, 5, -3)]
    tree = build_bsp([far, near])
    order, img = bsp_paint(tree, (1, 1, 4), W, H)
    assert [f.orig for f in order] == [0, 1]
    assert img[0][0] == 1


def test_edges():
    assert build_bsp([]) is None
    assert bsp_paint(None, (0, 0, 1), 2, 1) == ([], [[-1, -1]])
    tri = [(0, 0, -1), (6, 0, -1), (0, 5, -1)]
    # The eye in the plane of the triangle sees it edge on: no pixel.
    _, img = bsp_paint(build_bsp([tri]), (1, 1, -1), W, H)
    assert all(x == -1 for row in img for x in row)
