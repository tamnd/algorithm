# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnyder-drawing/. The authors are listed in prov/EKZ3MZ.jsonl.

import math
import random

import pytest

from schnyder_drawing import schnyder_drawing, schnyder_wood, triangulate

Rotation = dict[int, list[int]]
Point = tuple[int, int]


def rotation_from_points(pts: dict[int, Point], edges: list[tuple[int, int]]) -> Rotation:
    adj: Rotation = {v: [] for v in pts}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return {v: sorted(adj[v], key=lambda w: math.atan2(pts[w][1] - pts[v][1], pts[w][0] - pts[v][0]))
            for v in pts}


def orient(a: Point, b: Point, c: Point) -> int:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a: Point, b: Point, p: Point) -> bool:
    return (orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def proper_cross(a: Point, b: Point, c: Point, d: Point) -> bool:
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def edges_of(rot: Rotation) -> list[tuple[int, int]]:
    return [(u, v) for u in rot for v in rot[u] if u < v]


def is_plane_drawing(rot: Rotation, pos: dict[int, Point]) -> bool:
    """Exact check: distinct points, no vertex on another edge, no crossing."""
    if len(set(pos.values())) != len(pos):
        return False
    es = edges_of(rot)
    for u, v in es:
        if any(w != u and w != v and on_segment(pos[u], pos[v], pos[w]) for w in rot):
            return False
    for i, (a, b) in enumerate(es):
        for c, d in es[i + 1:]:
            if len({a, b, c, d}) == 4 and proper_cross(pos[a], pos[b], pos[c], pos[d]):
                return False
    return True


def keeps_rotation(rot: Rotation, pos: dict[int, Point]) -> bool:
    for v, ring in rot.items():
        if len(ring) < 2:
            continue
        got = sorted(ring, key=lambda w: math.atan2(pos[w][1] - pos[v][1], pos[w][0] - pos[v][0]))
        i = got.index(ring[0])
        if got[i:] + got[:i] != ring:
            return False
    return True


def check(rot: Rotation) -> dict[int, Point]:
    pos = schnyder_drawing(rot)
    n = len(rot)
    assert set(pos) == set(rot)
    if n >= 3:
        assert all(0 <= x <= n - 2 and 0 <= y <= n - 2 for x, y in pos.values())
    assert is_plane_drawing(rot, pos)
    assert keeps_rotation(rot, pos)
    return pos


def stacked(rng: random.Random, n: int) -> Rotation:
    rot: Rotation = {0: [1, 2], 1: [2, 0], 2: [0, 1]}
    faces = [(0, 1, 2), (0, 2, 1)]
    for v in range(3, n):
        i = rng.randrange(len(faces))
        x, y, z = faces[i]
        faces[i] = (x, y, v)
        faces += [(y, z, v), (z, x, v)]
        for p, q in ((x, y), (y, z), (z, x)):
            rot[p].insert(rot[p].index(q) + 1, v)
        rot[v] = [x, y, z]
    return rot


def point_graph(rng: random.Random, n: int, keep: float, frame: bool) -> Rotation:
    """Greedy maximal plane graph on random points, then a random subset of edges."""
    pts: dict[int, Point] = {}
    while len(pts) < n:
        p = (rng.randint(0, 40), rng.randint(0, 40))
        if p not in pts.values():
            pts[len(pts)] = p
    if frame:
        pts[n], pts[n + 1], pts[n + 2] = (-500, -500), (500, -499), (0, 500)
    vs = list(pts)
    pairs = [(u, v) for u in vs for v in vs if u < v]
    rng.shuffle(pairs)
    es: list[tuple[int, int]] = []
    for u, v in pairs:
        if any(w != u and w != v and on_segment(pts[u], pts[v], pts[w]) for w in vs):
            continue
        if any(len({u, v, a, b}) == 4 and proper_cross(pts[u], pts[v], pts[a], pts[b]) for a, b in es):
            continue
        es.append((u, v))
    if not frame:
        es = [e for e in es if rng.random() < keep]
    rot = rotation_from_points(pts, es)
    perm = vs[:]
    rng.shuffle(perm)
    return {perm[v]: [perm[w] for w in rot[v]] for v in rng.sample(vs, len(vs))}


OCTAHEDRON = {0: [1, 4, 3, 2], 1: [2, 5, 4, 0], 2: [0, 3, 5, 1],
              3: [0, 4, 5, 2], 4: [0, 1, 5, 3], 5: [4, 1, 2, 3]}


def test_page_example() -> None:
    p1, p2, p3 = schnyder_wood(OCTAHEDRON, (0, 1, 2))
    assert p1 == {3: 0, 4: 0, 5: 3} and p2 == {3: 4, 4: 1, 5: 1} and p3 == {3: 2, 4: 5, 5: 2}
    pos = schnyder_drawing(OCTAHEDRON, (0, 1, 2))
    assert pos == {0: (4, 1), 1: (0, 4), 2: (1, 0), 3: (3, 1), 4: (1, 3), 5: (1, 1)}
    assert is_plane_drawing(OCTAHEDRON, pos) and keeps_rotation(OCTAHEDRON, pos)


def test_small_cases() -> None:
    assert schnyder_drawing({}) == {}
    assert schnyder_drawing({7: []}) == {7: (0, 0)}
    assert schnyder_drawing({0: [1], 1: [0]}) == {0: (0, 0), 1: (1, 0)}
    k4 = {0: [1, 2, 3], 1: [2, 0, 3], 2: [0, 1, 3], 3: [0, 2, 1]}
    assert check(k4) == {0: (2, 1), 1: (1, 0), 2: (0, 2), 3: (1, 1)}
    triangle = {0: [1, 2], 1: [2, 0], 2: [0, 1]}
    check(triangle)
    path = {i: [j for j in (i - 1, i + 1) if 0 <= j < 6] for i in range(6)}
    check(path)
    star = {0: [1, 2, 3, 4, 5], 1: [0], 2: [0], 3: [0], 4: [0], 5: [0]}
    check(star)
    check({v: [] for v in range(5)})


def test_nonplanar_inputs_are_rejected() -> None:
    k5 = {v: [w for w in range(5) if w != v] for v in range(5)}
    k33 = {v: ([3, 4, 5] if v < 3 else [0, 1, 2]) for v in range(6)}
    toroidal_k4 = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
    for rot in (k5, k33, toroidal_k4):
        with pytest.raises(ValueError):
            schnyder_drawing(rot)


def test_schnyder_wood_rule() -> None:
    rng = random.Random(5)
    for _ in range(100):
        rot = stacked(rng, rng.randint(3, 40)) if rng.random() < 0.5 else point_graph(rng, rng.randint(1, 12), 1, True)
        v = next(iter(rot))
        w = rot[v][0]
        outer = (v, rot[w][rot[w].index(v) - 1], w)
        parents = schnyder_wood(rot, outer)
        inner = [u for u in rot if u not in outer]
        colour: dict[tuple[int, int], int] = {}
        for i in range(3):
            assert set(parents[i]) == set(inner)
            for u in inner:
                colour[(u, parents[i][u])] = i
                seen, x = set(), u
                while x in parents[i]:
                    assert x not in seen
                    seen.add(x)
                    x = parents[i][x]
                assert x == outer[i]
        assert len(colour) == 3 * len(inner) and all((b, a) not in colour for a, b in colour)
        for u in inner:  # out 1, in 3, out 2, in 1, out 3, in 2, counterclockwise
            ring = rot[u]
            k = ring.index(parents[0][u])
            word = []
            for x in ring[k:] + ring[:k]:
                word.append(("out", colour[(u, x)]) if (u, x) in colour else ("in", colour[(x, u)]))
            groups = [word[0]] + [t for s, t in zip(word, word[1:]) if s != t]
            assert [g for g in groups if g[0] == "out"] == [("out", 0), ("out", 1), ("out", 2)]
            for s, t in zip(word, word[1:] + word[:1]):
                if s[0] == "out" and t[0] == "in":
                    assert t[1] == (s[1] + 2) % 3
        for i, a in enumerate(outer):
            assert all(colour[(x, a)] == i for x in rot[a] if x in inner)


def test_triangulate() -> None:
    rng = random.Random(3)
    for _ in range(100):
        rot = point_graph(rng, rng.randint(3, 12), rng.random(), False)
        tri = triangulate(rot)
        n = len(rot)
        assert sum(len(a) for a in tri.values()) == 2 * (3 * n - 6)
        for v in rot:
            assert len(set(tri[v])) == len(tri[v])
            kept = [w for w in tri[v] if w in rot[v]]
            if kept:
                i = kept.index(rot[v][0])
                assert kept[i:] + kept[:i] == rot[v]


def test_random_against_oracle() -> None:
    rng = random.Random(2024)
    for trial in range(600):
        kind = trial % 3
        if kind == 0:
            rot = stacked(rng, rng.randint(3, 30))
        elif kind == 1:
            rot = point_graph(rng, rng.randint(1, 12), 1, True)
        else:
            rot = point_graph(rng, rng.randint(1, 14), rng.random(), False)
        check(rot)


def test_large_input() -> None:
    rng = random.Random(1)
    n = 4000
    rot = stacked(rng, n)
    pos = schnyder_drawing(rot)
    corners = {v for v, p in pos.items() if p in ((n - 2, 1), (0, n - 2), (1, 0))}
    assert len(corners) == 3
    assert all(0 <= x <= n - 2 and 0 <= y <= n - 2 for x, y in pos.values())
    faces = set()
    for u in rot:
        for v in rot[u]:
            w = rot[v][rot[v].index(u) - 1]
            faces.add(min((u, v, w), (v, w, u), (w, u, v)))
    assert len(faces) == 2 * n - 4
    for u, v, w in faces:  # every inner face keeps its orientation, the outer one flips
        sign = orient(pos[u], pos[v], pos[w])
        assert sign != 0
        assert (sign < 0) == ({u, v, w} == corners)
