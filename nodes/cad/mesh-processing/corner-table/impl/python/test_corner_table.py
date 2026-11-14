# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/corner-table/. The authors are listed in prov/FBTW3E.jsonl.

import random

from corner_table import CornerTable, next_corner, prev_corner, triangle

# ---- brute force: compare every pair of corners ----


def brute_opposite(tris):
    V = [v for t in tris for v in t]
    O = []
    for c in range(len(V)):
        a, b = V[next_corner(c)], V[prev_corner(c)]
        found = [d for d in range(len(V)) if triangle(d) != triangle(c)
                 and V[next_corner(d)] == b and V[prev_corner(d)] == a]
        assert len(found) <= 1
        O.append(found[0] if found else -1)
    return O


def brute_fans(tris, v):
    """The fans of v: classes of the triangles at v, joined when they share an edge at v."""
    at = [t for t in range(len(tris)) if v in tris[t]]
    parent = {t: t for t in at}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in at:
        for j in at:
            if i < j and len((set(tris[i]) & set(tris[j])) - {v}) == 1:
                parent[find(i)] = find(j)
    classes = {}
    for t in at:
        classes.setdefault(find(t), set()).add(t)
    return list(classes.values())


# ---- meshes ----


def tetrahedron():
    return 4, [(0, 2, 1), (0, 1, 3), (1, 2, 3), (0, 3, 2)]


def octahedron():
    # 0, 1: poles; 2..5: equator counterclockwise seen from pole 0
    eq = [2, 3, 4, 5]
    tris = []
    for i in range(4):
        a, b = eq[i], eq[(i + 1) % 4]
        tris += [(0, a, b), (1, b, a)]
    return 6, tris


def grid(rng, a, b, torus):
    """An a by b grid of squares, each cut by a random diagonal; glued to a torus or not."""
    nx, ny = (a, b) if torus else (a + 1, b + 1)

    def idx(i, j):
        return (i % nx) * ny + (j % ny)

    tris = []
    for i in range(a):
        for j in range(b):
            p, q, r, s = idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)
            if rng.random() < 0.5:
                tris += [(p, q, r), (p, r, s)]
            else:
                tris += [(p, q, s), (q, r, s)]
    return nx * ny, tris


def scramble(rng, n, tris):
    perm = list(range(n))
    rng.shuffle(perm)
    out = []
    for t in tris:
        k = rng.randrange(3)
        t = t[k:] + t[:k]
        out.append(tuple(perm[v] for v in t))
    rng.shuffle(out)
    return n, out


def check(n, tris):
    ct = CornerTable(n, tris)
    assert ct.O == brute_opposite(tris)
    for c in range(len(ct.V)):
        if ct.O[c] != -1:
            assert ct.O[ct.O[c]] == c
            if ct.swing(c) != -1:
                assert ct.V[ct.swing(c)] == ct.V[c]
                assert ct.unswing(ct.swing(c)) == c
    for v in range(n):
        fans = brute_fans(tris, v)
        if not fans:
            assert ct.C[v] == -1
            continue
        assert len(fans) == 1
        r = ct.ring(ct.C[v])
        assert {triangle(c) for c in r} == fans[0] and len(r) == len(fans[0])
        assert all(ct.V[c] == v for c in r)
        for x, y in zip(r, r[1:]):  # consecutive triangles share the edge after the first
            assert ct.V[prev_corner(x)] == ct.V[next_corner(y)]
        nb = ct.vertex_neighbors(v)
        assert set(nb) == {w for t in fans[0] for w in tris[t]} - {v}
    return ct


# ---- tests ----


def test_page_example_tetrahedron():
    n, tris = tetrahedron()
    ct = check(n, tris)
    assert ct.V == [0, 2, 1, 0, 1, 3, 1, 2, 3, 0, 3, 2]
    assert ct.O == [8, 5, 10, 7, 11, 1, 9, 3, 0, 6, 2, 4]
    assert ct.swing(0) == 3 and ct.swing(3) == 9 and ct.swing(9) == 0
    assert ct.ring(0) == [0, 3, 9]
    assert ct.vertex_neighbors(0) == [2, 1, 3]
    assert list(ct.border_corners()) == []


def test_octahedron_and_border():
    check(*octahedron())
    n, tris = 4, [(0, 1, 2), (0, 2, 3)]  # a square of two triangles
    ct = check(n, tris)
    assert ct.O == [-1, 5, -1, -1, -1, 1]
    assert ct.vertex_neighbors(0) == [1, 2, 3]
    assert ct.ring(4) == [4, 2] and ct.ring(2) == [4, 2]
    assert ct.vertex_neighbors(2) == [3, 0, 1]
    assert ct.ring(3) == [0, 3]


def test_rejects_bad_orientation_and_non_manifold_edges():
    for tris in ([(0, 1, 2), (0, 1, 3)], [(0, 1, 2), (1, 0, 3), (0, 1, 4)]):
        try:
            CornerTable(5, tris)
        except ValueError:
            continue
        raise AssertionError(tris)


def test_non_manifold_vertex_gives_one_fan():
    tris = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (0, 6, 5), (0, 7, 6), (0, 8, 7), (0, 5, 8)]
    ct = CornerTable(9, tris)
    assert ct.O == brute_opposite(tris)
    assert len(ct.ring(0)) == 4 and len(ct.ring(12)) == 4
    assert {triangle(c) for c in ct.ring(0)} == {0, 1, 2, 3}


def test_random_grids():
    rng = random.Random(2001)
    for it in range(500):
        a, b = rng.randint(3, 5), rng.randint(3, 5)
        n, tris = grid(rng, a, b, torus=it % 2 == 0)
        n, tris = scramble(rng, n, tris)
        ct = check(n, tris)
        border = sum(1 for _ in ct.border_corners())
        assert border == (0 if it % 2 == 0 else 2 * (a + b))
