# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planar-face-finding/. The authors are listed in prov/X3Q68V.jsonl.

import random

from planar_face_finding import planar_face_finding, rotation_from_points


def orient(a, b, c) -> int:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, p) -> bool:
    return orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_conflict(p, q, r, s) -> bool:
    """True if the closed segments pq and rs meet anywhere other than at a shared end."""
    shared = {p, q} & {r, s}
    if shared:
        if len(shared) == 2:
            return True
        # one shared end: a conflict only if they overlap along a line
        o = shared.pop()
        a = q if p == o else p
        b = s if r == o else r
        return orient(o, a, b) == 0 and (a[0] - o[0]) * (b[0] - o[0]) + (a[1] - o[1]) * (b[1] - o[1]) > 0
    d1, d2 = orient(p, q, r), orient(p, q, s)
    d3, d4 = orient(r, s, p), orient(r, s, q)
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        return True
    return on_segment(p, q, r) or on_segment(p, q, s) or on_segment(r, s, p) or on_segment(r, s, q)


def random_plane_graph(rng: random.Random, n: int, tries: int):
    pts: dict[int, tuple[int, int]] = {}
    used = set()
    while len(pts) < n:
        p = (rng.randint(0, 12), rng.randint(0, 12))
        if p not in used:
            used.add(p)
            pts[len(pts)] = p
    edges: list[tuple[int, int]] = []
    for _ in range(tries if n >= 2 else 0):
        u, v = rng.sample(range(n), 2)
        if (u, v) in edges or (v, u) in edges:
            continue
        p, q = pts[u], pts[v]
        if any(on_segment(p, q, pts[w]) for w in pts if w not in (u, v)):
            continue
        if any(segments_conflict(p, q, pts[a], pts[b]) for a, b in edges):
            continue
        edges.append((u, v))
    return pts, edges


def components(n: int, edges) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)
    return len({find(v) for v in range(n)})


def twice_area(pts, walk) -> int:
    return sum(pts[walk[i]][0] * pts[walk[(i + 1) % len(walk)]][1] - pts[walk[(i + 1) % len(walk)]][0] * pts[walk[i]][1] for i in range(len(walk)))


def test_page_example() -> None:
    pts = {0: (0, 0), 1: (4, 0), 2: (4, 4), 3: (0, 4), 4: (2, 6), 5: (3, 1)}
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (3, 4), (0, 2), (1, 5)]
    rot = rotation_from_points(pts, edges)
    assert rot == {0: [1, 2, 3], 1: [2, 5, 0], 2: [4, 3, 0, 1], 3: [2, 4, 0], 4: [3, 2], 5: [1]}
    assert planar_face_finding(rot) == [[0, 1, 5, 1, 2], [0, 2, 3], [0, 3, 4, 2, 1], [2, 4, 3]]


def test_k4_planar_and_toroidal() -> None:
    planar = {0: [1, 3, 2], 1: [2, 3, 0], 2: [0, 3, 1], 3: [0, 1, 2]}
    faces = planar_face_finding(planar)
    assert sorted(len(f) for f in faces) == [3, 3, 3, 3]
    torus = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
    assert sorted(len(f) for f in planar_face_finding(torus)) == [4, 8]


def test_k5_and_k33_have_no_planar_rotation() -> None:
    import itertools

    def all_rotations(adj):
        vs = list(adj)
        opts = [[[adj[v][0], *p] for p in itertools.permutations(adj[v][1:])] for v in vs]
        for combo in itertools.product(*opts):
            yield dict(zip(vs, combo))

    k5 = {v: [w for w in range(5) if w != v] for v in range(5)}
    assert max(len(planar_face_finding(r)) for r in all_rotations(k5)) == 5  # 5 - 10 + 5 = 0
    k33 = {v: ([3, 4, 5] if v < 3 else [0, 1, 2]) for v in range(6)}
    assert max(len(planar_face_finding(r)) for r in all_rotations(k33)) == 3  # 6 - 9 + 3 = 0


def test_small_cases() -> None:
    assert planar_face_finding({}) == []
    assert planar_face_finding({7: []}) == [[7]]
    assert planar_face_finding({0: [1], 1: [0]}) == [[0, 1]]
    star = {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
    assert [len(f) for f in planar_face_finding(star)] == [6]
    path = {i: [j for j in (i - 1, i + 1) if 0 <= j < 6] for i in range(6)}
    assert [len(f) for f in planar_face_finding(path)] == [10]
    cycle = {i: [(i + 1) % 5, (i - 1) % 5] for i in range(5)}
    assert sorted(len(f) for f in planar_face_finding(cycle)) == [5, 5]


def test_random_drawings_against_euler_and_area() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        n = rng.randint(1, 9)
        pts, edges = random_plane_graph(rng, n, rng.randint(0, 30))
        rot = rotation_from_points(pts, edges)
        faces = planar_face_finding(rot)
        m, c = len(edges), components(n, edges)
        isolated = sum(1 for v in rot if not rot[v])
        dart_faces = [f for f in faces if len(rot[f[0]]) > 0]
        # each dart lies on exactly one face
        assert sum(len(f) for f in dart_faces) == 2 * m
        # Euler's formula, face by face of each component: n - m + f = 2c
        assert n - m + len(faces) == 2 * c
        assert len(faces) - isolated == len(dart_faces)
        # each component with an edge has exactly one walk that is not counterclockwise (its outer face)
        outer = sum(1 for f in dart_faces if twice_area(pts, f) <= 0)
        assert outer == c - isolated
