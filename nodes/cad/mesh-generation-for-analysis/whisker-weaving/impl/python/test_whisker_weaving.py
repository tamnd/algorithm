# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whisker-weaving/. The authors are listed in prov/4SHZ6G.jsonl.

import itertools
import random
from collections import deque

import pytest

from mg4geom import EDGE_CLASSES, REF, corners_positive
from whisker_weaving import dual_sheets, edge, hex_faces, pillowed_cube, sheet_euler, voxel_mesh


def rotations():
    """The 24 orientation preserving vertex orders of the reference cube."""
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = [[signs[r] if c == perm[r] else 0 for c in range(3)] for r in range(3)]
            det = (
                m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
            )
            if det != 1:
                continue
            sigma = []
            for c in REF:
                x = [2 * t - 1 for t in c]
                y = [sum(m[r][s] * x[s] for s in range(3)) for r in range(3)]
                sigma.append(REF.index(tuple((t + 1) // 2 for t in y)))
            out.append(sigma)
    return out


ROT = rotations()


def components(nodes, pairs):
    adj = {x: [] for x in nodes}
    for a, b in pairs:
        adj[a].append(b)
        adj[b].append(a)
    seen, out = set(), set()
    for x in adj:
        if x in seen:
            continue
        comp, queue = [], deque([x])
        seen.add(x)
        while queue:
            y = queue.popleft()
            comp.append(y)
            for z in adj[y]:
                if z not in seen:
                    seen.add(z)
                    queue.append(z)
        out.add(frozenset(comp))
    return out


def opposite_pairs(face):
    a, b, c, d = face
    return [(edge(a, b), edge(c, d)), (edge(b, c), edge(d, a))]


def brute_boundary(hexes):
    out = []
    for i, h in enumerate(hexes):
        for f in hex_faces(h):
            if not any(set(f) == set(g) for j, k in enumerate(hexes) if j != i for g in hex_faces(k)):
                out.append(f)
    return out


def check_mesh(points, hexes):
    r = dual_sheets(hexes)
    all_edges = {edge(h[i], h[j]) for h in hexes for cls in EDGE_CLASSES for i, j in cls}
    pairs = [p for h in hexes for f in hex_faces(h) for p in opposite_pairs(f)]
    assert {frozenset(s) for s in r["sheets"]} == components(all_edges, pairs)
    # every hex lies on three sheet crossings, one for each class of four parallel edges
    for h, cr in zip(hexes, r["crossing"]):
        assert len(cr) == 3
        for cls, s in zip(EDGE_CLASSES, cr):
            assert all(r["sheet_of"][edge(h[i], h[j])] == s for i, j in cls)
    bnd = brute_boundary(hexes)
    assert sorted(map(frozenset, bnd), key=sorted) == sorted(map(frozenset, r["boundary"]), key=sorted)
    assert 6 * len(hexes) == 2 * r["interior"] + len(r["boundary"])
    bedges = {e for f in bnd for p in opposite_pairs(f) for e in p}
    bpairs = [p for f in bnd for p in opposite_pairs(f)]
    assert {frozenset(lp) for lp in r["loops"]} == components(bedges, bpairs)
    # the boundary edges of each sheet are a union of loops
    for s, members in enumerate(r["sheets"]):
        own = {e for e in members if e in bedges}
        from_loops = {e for lp, t in zip(r["loops"], r["loop_sheet"]) if t == s for e in lp}
        assert own == from_loops
    # sheets of a voxel mesh are flat: one axis and one slab per sheet
    for members in r["sheets"]:
        sig = set()
        for a, b in members:
            p, q = points[a], points[b]
            axis = next(t for t in range(3) if p[t] != q[t])
            sig.add((axis, min(p[axis], q[axis])))
        assert len(sig) == 1
    return r


def square_complex_euler(squares):
    v, e = set(), set()
    for x, y in squares:
        cs = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        v.update(cs)
        for i in range(4):
            e.add(frozenset((cs[i], cs[(i + 1) % 4])))
    return len(v) - len(e) + len(squares)


def test_two_cubes():
    points, hexes = voxel_mesh([(0, 0, 0), (1, 0, 0)])
    r = check_mesh(points, hexes)
    assert len(r["sheets"]) == 4 and len(r["boundary"]) == 10 and r["interior"] == 1
    assert len(r["loops"]) == 4
    assert [sheet_euler(hexes, r, s) for s in range(4)] == [1, 1, 1, 1]


@pytest.mark.parametrize("n", [(1, 1, 1), (2, 3, 1), (3, 2, 2), (4, 1, 3)])
def test_grid(n):
    n1, n2, n3 = n
    points, hexes = voxel_mesh([(i, j, k) for i in range(n1) for j in range(n2) for k in range(n3)])
    r = check_mesh(points, hexes)
    assert len(r["sheets"]) == n1 + n2 + n3
    assert len(r["boundary"]) == 2 * (n1 * n2 + n2 * n3 + n3 * n1)
    assert len(r["loops"]) == n1 + n2 + n3


def test_pillowed_cube_has_a_closed_sheet():
    points, hexes = pillowed_cube()
    assert all(corners_positive([points[i] for i in h]) for h in hexes)
    r = dual_sheets(hexes)
    assert len(hexes) == 7 and len(r["boundary"]) == 6 and r["interior"] == 18
    assert 6 * 7 == 2 * 18 + 6
    assert len(r["sheets"]) == 4 and len(r["loops"]) == 3
    closed = [s for s in range(4) if s not in r["loop_sheet"]]
    assert len(closed) == 1
    s = closed[0]
    assert sum(c.count(s) for c in r["crossing"]) == 6
    assert sheet_euler(hexes, r, s) == 2  # a sphere: 8 vertices, 12 edges, 6 faces
    assert sorted(sheet_euler(hexes, r, t) for t in range(4)) == [1, 1, 1, 2]


def test_face_shared_by_three_hexes_is_rejected():
    hexes = [[0, 1, 2, 3, 4, 5, 6, 7], [4, 5, 6, 7, 8, 9, 10, 11], [4, 5, 6, 7, 12, 13, 14, 15]]
    with pytest.raises(ValueError):
        dual_sheets(hexes)


def test_random_voxel_meshes():
    rng = random.Random(4061)
    for trial in range(500):
        n = rng.randint(1, 3)
        p = rng.choice([0.3, 0.5, 0.8])
        cells = [(i, j, k) for i in range(n + 1) for j in range(n) for k in range(n) if rng.random() < p]
        if not cells:
            cells = [(0, 0, 0)]
        points, hexes = voxel_mesh(cells)
        perm = list(range(len(points)))
        rng.shuffle(perm)
        points2 = [None] * len(points)
        for old, new in enumerate(perm):
            points2[new] = points[old]
        hexes2 = []
        for h in hexes:
            sigma = rng.choice(ROT)
            hexes2.append([perm[h[sigma[k]]] for k in range(8)])
        for h in hexes2:
            assert corners_positive([points2[i] for i in h])
        r = check_mesh(points2, hexes2)
        # each sheet is a flat slab section, so its Euler characteristic is that of a square complex
        for s, members in enumerate(r["sheets"]):
            a, b = members[0]
            axis = next(t for t in range(3) if points2[a][t] != points2[b][t])
            lo = min(points2[a][axis], points2[b][axis])
            others = [t for t in range(3) if t != axis]
            hex_ids = [i for i, c in enumerate(r["crossing"]) if s in c]
            squares = []
            for i in hex_ids:
                corner = min(points2[v] for v in hexes2[i])
                assert corner[axis] == lo
                squares.append((corner[others[0]], corner[others[1]]))
            assert sheet_euler(hexes2, r, s) == square_complex_euler(squares)
