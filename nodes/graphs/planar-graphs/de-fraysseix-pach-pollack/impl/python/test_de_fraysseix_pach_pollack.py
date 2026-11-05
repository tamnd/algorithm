# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-fraysseix-pach-pollack/. The authors are listed in prov/FQHSKN.jsonl.

import itertools
import random

import pytest

from de_fraysseix_pach_pollack import canonical_ordering, draw


def rot_from_faces(n, inner):
    """Rotation system from the counterclockwise inner triangles.

    The outer face is 0, 1, 2 (counterclockwise), so the outer boundary
    walked with the interior on the right is 0, 2, 1.
    """
    succ = [dict() for _ in range(n)]
    for f in list(inner) + [(0, 2, 1)]:
        for t in range(3):
            x, y, z = f[t - 1], f[t], f[(t + 1) % 3]
            succ[y][z] = x
    rot = []
    for v in range(n):
        start = min(succ[v])
        r = [start]
        w = succ[v][start]
        while w != start:
            r.append(w)
            w = succ[v][w]
        rot.append(r)
    return rot


def random_triangulation(n, rng, flips=0):
    """Rotation system of a random maximal planar graph with outer face 0, 1, 2.

    Vertices are inserted into random inner faces, then random edge flips are
    applied. Faces are kept as counterclockwise triangles.
    """
    faces = [(0, 1, 2)]
    for v in range(3, n):
        i = rng.randrange(len(faces))
        a, b, c = faces[i]
        faces[i] = (a, b, v)
        faces += [(b, c, v), (c, a, v)]
    outer_edges = {frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2))}
    for _ in range(flips):
        dart_face = {}
        for k, f in enumerate(faces):
            for t in range(3):
                dart_face[(f[t], f[(t + 1) % 3])] = k
        k = rng.randrange(len(faces))
        f = faces[k]
        t = rng.randrange(3)
        a, b, c = f[t], f[(t + 1) % 3], f[(t + 2) % 3]
        if frozenset((a, b)) in outer_edges:
            continue
        g = faces[dart_face[(b, a)]]
        d = [x for x in g if x not in (a, b)][0]
        if (c, d) in dart_face or (d, c) in dart_face:
            continue
        faces[k] = (a, d, c)
        faces[dart_face[(b, a)]] = (b, c, d)
    return rot_from_faces(n, faces)


def oracle_drawing(rot, order):
    """The original O(n^2) shift method with explicit sets M(w)."""
    n = len(rot)
    v1, v2, v3 = order[0], order[1], order[2]
    x = [0] * n
    y = [0] * n
    x[v2], x[v3], y[v3] = 2, 1, 1
    contour = [v1, v3, v2]
    move = {v1: {v1, v2, v3}, v3: {v3, v2}, v2: {v2}}
    placed = {v1, v2, v3}
    for v in order[3:]:
        idx = [i for i, w in enumerate(contour) if w in rot[v]]
        p, q = idx[0], idx[-1]
        assert idx == list(range(p, q + 1)), "neighbours not contiguous"
        assert p < q
        for w in move[contour[p + 1]]:
            x[w] += 1
        for w in move[contour[q]]:
            x[w] += 1
        wp, wq = contour[p], contour[q]
        x[v] = (x[wp] + x[wq] + y[wq] - y[wp]) // 2
        y[v] = (x[wq] - x[wp] + y[wp] + y[wq]) // 2
        for i in range(p + 1):
            move[contour[i]].add(v)
        move[v] = {v} | move[contour[p + 1]]
        contour = contour[: p + 1] + [v] + contour[q:]
        placed.add(v)
    return [(x[v], y[v]) for v in range(n)]


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, c):
    return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))


def segments_meet(a, b, c, d):
    d1, d2 = orient(c, d, a), orient(c, d, b)
    d3, d4 = orient(a, b, c), orient(a, b, d)
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        return True
    if d1 == 0 and on_segment(c, d, a):
        return True
    if d2 == 0 and on_segment(c, d, b):
        return True
    if d3 == 0 and on_segment(a, b, c):
        return True
    if d4 == 0 and on_segment(a, b, d):
        return True
    return False


def check_plane(rot, pos):
    n = len(rot)
    assert len(set(pos)) == n, "two vertices share a point"
    edges = [(u, v) for u in range(n) for v in rot[u] if u < v]
    for i, (a, b) in enumerate(edges):
        for c in range(n):
            if c != a and c != b and orient(pos[a], pos[b], pos[c]) == 0 \
                    and on_segment(pos[a], pos[b], pos[c]):
                raise AssertionError("vertex on an edge")
        for (c, d) in edges[i + 1:]:
            if len({a, b, c, d}) < 4:
                continue
            assert not segments_meet(pos[a], pos[b], pos[c], pos[d]), "crossing"


def check_rotation(rot, pos):
    """The drawing realizes the given rotation system (same cyclic orders)."""
    import math
    for v, r in enumerate(rot):
        got = sorted(r, key=lambda w: math.atan2(pos[w][1] - pos[v][1],
                                                 pos[w][0] - pos[v][0]))
        i = got.index(r[0])
        assert got[i:] + got[:i] == r


def check_grid(pos, v1, v2, vn):
    n = len(pos)
    w, h = 2 * n - 4, n - 2
    if n == 3:
        w, h = 2, 1
    for (x, y) in pos:
        assert 0 <= x <= w and 0 <= y <= h
    assert pos[v1] == (0, 0) and pos[v2] == (w, 0)


def test_triangle():
    rot = [[1, 2], [2, 0], [0, 1]]
    pos = draw(rot, 0, 1, 2)
    assert pos == [(0, 0), (2, 0), (1, 1)]


def test_k4():
    # triangle 0, 1, 2 counterclockwise with 3 inside
    rot = [[1, 3, 2], [2, 3, 0], [0, 3, 1], [0, 1, 2]]
    pos = draw(rot, 0, 1, 2)
    assert pos == [(0, 0), (4, 0), (2, 2), (2, 1)]
    check_plane(rot, pos)
    check_rotation(rot, pos)


def test_octahedron():
    import math
    pts = [(0, 0), (10, 0), (5, 9), (5, 2), (6.5, 4), (3.5, 4)]
    adj = [[] for _ in range(6)]
    for i in range(6):
        for j in range(i + 1, 6):
            if (i, j) not in [(0, 4), (1, 5), (2, 3)]:
                adj[i].append(j)
                adj[j].append(i)
    rot = [sorted(adj[u], key=lambda w: math.atan2(pts[w][1] - pts[u][1],
                                                    pts[w][0] - pts[u][0]))
           for u in range(6)]
    order, _, _ = canonical_ordering(rot, 0, 1, 2)
    assert order == [0, 1, 3, 5, 4, 2]
    pos = draw(rot, 0, 1, 2)
    assert pos == [(0, 0), (8, 0), (4, 4), (5, 1), (4, 3), (3, 2)]
    assert pos == oracle_drawing(rot, order)
    check_plane(rot, pos)
    check_rotation(rot, pos)


def test_random_against_oracle():
    rng = random.Random(2024)
    for trial in range(600):
        n = rng.randint(3, 30)
        rot = random_triangulation(n, rng, flips=rng.randint(0, 3 * n))
        pos = draw(rot, 0, 1, 2)
        check_grid(pos, 0, 1, 2)
        if n > 3:
            order, _, _ = canonical_ordering(rot, 0, 1, 2)
            assert sorted(order) == list(range(n))
            assert order[:2] == [0, 1] and order[-1] == 2
            assert pos == oracle_drawing(rot, order)
        if n <= 18:
            check_plane(rot, pos)
            check_rotation(rot, pos)


def test_large():
    rng = random.Random(7)
    n = 20000
    rot = random_triangulation(n, rng)
    pos = draw(rot, 0, 1, 2)
    check_grid(pos, 0, 1, 2)
    assert pos[2] == (n - 2, n - 2)


def test_deep_nesting():
    # vertex v is inserted into the triangle (0, 1, v - 1): a long chain of
    # nested triangles, which makes the contour and the shift tree long
    n = 3000
    faces = [(0, 1, 2)]
    for v in range(3, n):
        faces[0] = (0, 1, v)
        faces += [(1, v - 1, v), (v - 1, 0, v)]
    rot = rot_from_faces(n, faces)
    pos = draw(rot, 0, 1, 2)
    check_grid(pos, 0, 1, 2)
    check_rotation(rot, pos)


def test_rejects_non_triangulations():
    # a single vertex, a single edge, a path (a tree)
    for rot in ([[]], [[1], [0]], [[1], [0, 2], [1]]):
        with pytest.raises(ValueError):
            draw(rot, 0, 1, len(rot) - 1)
    # a star with three leaves: a tree, faces are not triangles
    with pytest.raises(ValueError):
        draw([[1, 2, 3], [0], [0], [0]], 1, 2, 3)
    # K4 with the outer face listed clockwise
    with pytest.raises(ValueError):
        draw([[1, 3, 2], [2, 3, 0], [0, 3, 1], [0, 1, 2]], 0, 2, 1)


def test_k5_and_k33_have_no_plane_rotation():
    # every rotation system of K5 fails, and so does every one of K3,3
    def all_rotations(adj):
        choices = []
        for v, nb in enumerate(adj):
            first, rest = nb[0], nb[1:]
            choices.append([[first] + list(p) for p in itertools.permutations(rest)])
        return itertools.product(*choices)

    k5 = [[w for w in range(5) if w != v] for v in range(5)]
    for rot in all_rotations(k5):
        with pytest.raises(ValueError):
            draw([list(r) for r in rot], 0, 1, 2)
    k33 = [[3, 4, 5]] * 3 + [[0, 1, 2]] * 3
    count = 0
    for rot in all_rotations(k33):
        count += 1
        with pytest.raises(ValueError):
            draw([list(r) for r in rot], 0, 3, 1)
    assert count == 2 ** 6
