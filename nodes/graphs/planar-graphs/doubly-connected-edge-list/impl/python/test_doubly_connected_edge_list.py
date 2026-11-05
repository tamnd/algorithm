# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doubly-connected-edge-list/. The authors are listed in prov/69ZYTE.jsonl.

import math
import random

from doubly_connected_edge_list import DCEL

# ---- independent oracles ----


def rotation_from_points(pts, edges):
    """Rotation system of a straight-line drawing: neighbours sorted by angle."""
    adj = [[] for _ in pts]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    rot = []
    for u, nb in enumerate(adj):
        x, y = pts[u]
        rot.append(sorted(nb, key=lambda v: math.atan2(pts[v][1] - y, pts[v][0] - x)))
    return rot


def trace_faces(rot):
    """Face cycles of a rotation system as lists of darts (u, v), traced with dicts."""
    seen = set()
    out = []
    for u in range(len(rot)):
        for v in rot[u]:
            if (u, v) in seen:
                continue
            cyc = []
            a, b = u, v
            while (a, b) not in seen:
                seen.add((a, b))
                cyc.append((a, b))
                r = rot[b]
                c = r[(r.index(a) - 1) % len(r)]
                a, b = b, c
            out.append(cyc)
    return out


def canon(cycle):
    """A rotation-invariant key of a cyclic list."""
    if not cycle:
        return ()
    k = min(range(len(cycle)), key=lambda i: cycle[i:] + cycle[:i])
    return tuple(cycle[k:] + cycle[:k])


def dcel_faces(d):
    out = []
    for f in d.faces():
        b = d.face_boundary(f)
        out.append(canon([(d.origin[h], d.origin[h ^ 1]) for h in b]))
    return sorted(out)


def oracle_faces(rot):
    cycles = trace_faces(rot)
    if not cycles:  # a graph with no edge has one face with an empty boundary
        return [()]
    return sorted(canon(c) for c in cycles)


def same_cyclic(a, b):
    return len(a) == len(b) and (not a or canon(list(a)) == canon(list(b)))


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def segments_cross(p, q, r, s):
    """True when closed segments pq and rs meet at a point that is not a shared end."""
    shared = {p, q} & {r, s}
    if shared:
        # two segments with a common end meet elsewhere only if collinear and overlapping
        o = q if p in shared else p
        t = s if r in shared else r
        c = p if p in shared else q
        return orient(c, o, t) == 0 and (o[0] - c[0]) * (t[0] - c[0]) + (o[1] - c[1]) * (t[1] - c[1]) > 0
    d1, d2 = orient(p, q, r), orient(p, q, s)
    d3, d4 = orient(r, s, p), orient(r, s, q)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True

    def on(a, b, c):
        return orient(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])

    return on(p, q, r) or on(p, q, s) or on(r, s, p) or on(r, s, q)


def connected(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)
    return len({find(x) for x in range(n)}) == 1


# ---- fixed cases ----

K4_POINTS = [(0, 0), (4, 0), (2, 3), (2, 1)]
K4_EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def test_page_example_k4():
    rot = rotation_from_points(K4_POINTS, K4_EDGES)
    assert rot == [[1, 3, 2], [2, 3, 0], [0, 3, 1], [0, 1, 2]]
    d = DCEL.from_rotation(rot)
    d.check_invariant()
    assert d.num_edges() == 6 and len(d.faces()) == 4
    assert all(len(d.face_boundary(f)) == 3 for f in d.faces())
    assert dcel_faces(d) == oracle_faces(rot)
    for v in range(4):
        assert same_cyclic(d.neighbors(v), rot[v])
    # split no face of K4 is possible; delete edge 2-3 and add it back
    h = next(x for x in range(12) if (d.origin[x], d.origin[x ^ 1]) == (3, 2))
    d.join_faces(h)
    d.check_invariant()
    assert len(d.faces()) == 3
    assert sorted(len(d.face_boundary(f)) for f in d.faces()) == [3, 3, 4]


def test_single_vertex():
    d = DCEL.from_rotation([[]])
    d.check_invariant()
    assert d.faces() == [0] and d.face_boundary(0) == [] and d.neighbors(0) == []
    d2 = DCEL()
    d2.check_invariant()
    h = d2.add_leaf(-1)
    d2.check_invariant()
    assert d2.face_boundary(0) == [h, h ^ 1]


def test_tree_has_one_face():
    rot = [[1, 2, 3], [0], [0], [0, 4], [3]]
    d = DCEL.from_rotation(rot)
    d.check_invariant()
    assert len(d.faces()) == 1
    assert len(d.face_boundary(d.faces()[0])) == 8


def test_cube():
    pts = [(0, 0), (6, 0), (6, 6), (0, 6), (2, 2), (4, 2), (4, 4), (2, 4)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    rot = rotation_from_points(pts, edges)
    d = DCEL.from_rotation(rot)
    d.check_invariant()
    assert len(d.faces()) == 6
    assert all(len(d.face_boundary(f)) == 4 for f in d.faces())


def test_nonplanar_rotations_fail_euler():
    k5 = [[v for v in range(5) if v != u] for u in range(5)]
    k33 = [[3, 4, 5]] * 3 + [[0, 1, 2]] * 3
    for rot in (k5, k33):
        d = DCEL.from_rotation(rot)
        assert dcel_faces(d) == oracle_faces(rot)
        try:
            d.check_invariant()
        except AssertionError:
            continue
        raise AssertionError("a non-planar graph passed the Euler check")


def test_split_face_square():
    rot = [[1, 3], [2, 0], [3, 1], [0, 2]]
    d = DCEL.from_rotation(rot)
    f = d.faces()[0]
    b = d.face_boundary(f)
    a = next(x for x in b if d.origin[x] == 0)
    c = next(x for x in b if d.origin[x] == 2)
    h = d.split_face(a, c)
    d.check_invariant()
    assert len(d.faces()) == 3
    assert len(d.face_boundary(d.face[h])) == 3 and len(d.face_boundary(d.face[h ^ 1])) == 3


# ---- randomized ----


def random_geometric(rng):
    n = rng.randint(1, 8)
    pts = []
    while len(pts) < n:
        p = (rng.randint(0, 12), rng.randint(0, 12))
        if p not in pts:
            pts.append(p)
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    rng.shuffle(pairs)
    edges = []
    for u, v in pairs:
        if rng.random() < 0.3:
            continue
        if all(not segments_cross(pts[u], pts[v], pts[a], pts[b]) for a, b in edges):
            edges.append((u, v))
    return pts, edges


def test_random_straight_line_drawings():
    rng = random.Random(1)
    done = 0
    while done < 600:
        pts, edges = random_geometric(rng)
        if not connected(len(pts), edges):
            continue
        rot = rotation_from_points(pts, edges)
        d = DCEL.from_rotation(rot)
        d.check_invariant()
        assert dcel_faces(d) == oracle_faces(rot)
        assert len(d.faces()) == len(edges) - len(pts) + 2
        for v in range(len(pts)):
            assert same_cyclic(d.neighbors(v), rot[v])
        done += 1


def test_random_operations():
    rng = random.Random(2)
    for _ in range(500):
        d = DCEL()
        edges = set()
        for _ in range(rng.randint(1, 25)):
            op = rng.random()
            live = [h for h in range(len(d.origin)) if d.origin[h] != -1]
            if not live or op < 0.35:
                a = rng.choice(live) if live else -1
                h = d.add_leaf(a)
                edges.add(frozenset((d.origin[h], d.origin[h ^ 1])))
            elif op < 0.75:
                f = rng.choice(d.faces())
                b = d.face_boundary(f)
                a, c = rng.choice(b), rng.choice(b)
                u, v = d.origin[a], d.origin[c]
                if u == v or frozenset((u, v)) in edges:
                    continue
                h = d.split_face(a, c)
                edges.add(frozenset((u, v)))
            else:
                cand = [h for h in live if d.face[h] != d.face[h ^ 1]]
                if not cand:
                    continue
                h = rng.choice(cand)
                edges.discard(frozenset((d.origin[h], d.origin[h ^ 1])))
                d.join_faces(h)
            d.check_invariant()
            rot = [d.neighbors(v) for v in range(d.num_vertices())]
            got = {frozenset((u, v)) for u in range(len(rot)) for v in rot[u]}
            assert got == edges
            assert dcel_faces(d) == oracle_faces(rot)
