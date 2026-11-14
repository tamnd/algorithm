# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmp-geodesic-algorithm/. The authors are listed in prov/14F19Q.jsonl.

import heapq
import random
from fractions import Fraction
from math import acos, hypot, pi, sqrt

from mmp_geodesic_algorithm import mmp_geodesic


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return sqrt(dot(a, a))


# ---- meshes ----


def grid(m, rng=None, height=None):
    """The unit square cut into m x m cells, each cut by a diagonal (random if rng is given)."""
    pts = [(i / m, j / m, height(i, j) if height else 0.0) for j in range(m + 1) for i in range(m + 1)]
    faces = []
    for j in range(m):
        for i in range(m):
            a, b, c, d = j * (m + 1) + i, j * (m + 1) + i + 1, (j + 1) * (m + 1) + i + 1, (j + 1) * (m + 1) + i
            if rng is not None and rng.random() < 0.5:
                faces += [(a, b, d), (b, c, d)]
            else:
                faces += [(a, b, c), (a, c, d)]
    return pts, faces


def l_shape():
    """[0, 2]^2 without the open square (1, 2]^2, in cells of size 1/2, with exact coordinates."""
    idx, pts = {}, []
    for j in range(5):
        for i in range(5):
            if not (i > 2 and j > 2):
                idx[(i, j)] = len(pts)
                pts.append((Fraction(i, 2), Fraction(j, 2)))
    faces = []
    for j in range(4):
        for i in range(4):
            if i >= 2 and j >= 2:
                continue
            a, b, c, d = idx[(i, j)], idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]
            faces += [(a, b, c), (a, c, d)] if (i + j) % 2 else [(a, b, d), (b, c, d)]
    return pts, faces


def box(a, b, c):
    """The surface of [0, a] x [0, b] x [0, c] as 12 triangles."""
    pts = [(x, y, z) for z in (0, c) for y in (0, b) for x in (0, a)]
    quads = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    faces = [t for q, r, s, u in quads for t in ((q, r, s), (q, s, u))]
    return pts, faces


def octahedron(sx, sy, sz):
    pts = [(sx, 0, 0), (-sx, 0, 0), (0, sy, 0), (0, -sy, 0), (0, 0, sz), (0, 0, -sz)]
    faces = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    return pts, faces


def icosahedron(sx, sy, sz):
    t = (1 + sqrt(5)) / 2
    raw = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t),
           (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    faces = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
             (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
             (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    return [(sx * x, sy * y, sz * z) for x, y, z in raw], faces


# ---- reference methods ----


def unfolding_distances(P, F, s):
    """Brute force for convex polyhedra: try every face sequence from s whose unfolding still lets a line through."""
    n = len(P)
    ef = {}
    for fid, f in enumerate(F):
        for k in range(3):
            ef.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(fid)
    best = [float("inf")] * n
    best[s] = 0.0

    def cr(a, b):
        return a[0] * b[1] - a[1] * b[0]

    def place(pa, pb, a, b, c):
        """The 2D image of vertex c across the segment pa-pb, on the side away from the origin."""
        u3 = sub(P[b], P[a])
        L = norm(u3)
        w = sub(P[c], P[a])
        x = dot(w, u3) / L
        y = sqrt(max(dot(w, w) - x * x, 0.0))
        ux, uy = (pb[0] - pa[0]) / L, (pb[1] - pa[1]) / L
        vx, vy = -uy, ux
        if vx * pa[0] + vy * pa[1] < 0:
            vx, vy = -vx, -vy
        return (pa[0] + x * ux + y * vx, pa[1] + x * uy + y * vy)

    def visit(fid, a, b, pa, pb, lo, hi, seen):
        h = next((g for g in ef[frozenset((a, b))] if g != fid), None)
        if h is None or h in seen:
            return
        c = next(w for w in F[h] if w != a and w != b)
        pc = place(pa, pb, a, b, c)
        tol = 1e-12 * norm(pc) ** 2
        if cr(lo, pc) >= -tol and cr(pc, hi) >= -tol:
            best[c] = min(best[c], hypot(*pc))
        for x, px, y, py in ((a, pa, c, pc), (c, pc, b, pb)):
            l2, h2 = (px, py) if cr(px, py) > 0 else (py, px)
            nl = l2 if cr(lo, l2) > 0 else lo
            nh = h2 if cr(hi, h2) < 0 else hi
            if cr(nl, nh) > 1e-12 * hypot(*nl) * hypot(*nh):
                visit(h, x, y, px, py, nl, nh, seen | {h})

    for fid, f in enumerate(F):
        if s not in f:
            continue
        k = f.index(s)
        a, b = f[(k + 1) % 3], f[(k + 2) % 3]
        la = norm(sub(P[a], P[s]))
        pa = (la, 0.0)
        w = sub(P[b], P[s])
        x = dot(w, sub(P[a], P[s])) / la
        pb = (x, sqrt(max(dot(w, w) - x * x, 0.0)))
        best[a] = min(best[a], la)
        best[b] = min(best[b], hypot(*pb))
        visit(fid, a, b, pa, pb, pa, pb, {fid})
    return best


def steiner_dijkstra(P, F, s, k):
    """Dijkstra on k extra points per edge, with straight segments across each face (an upper bound)."""
    nodes = [tuple(p) for p in P]
    on_edge = {}
    for f in F:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            e = (min(a, b), max(a, b))
            if e not in on_edge:
                ids = []
                for t in range(1, k + 1):
                    nodes.append(tuple(P[e[0]][c] + (P[e[1]][c] - P[e[0]][c]) * t / (k + 1) for c in range(3)))
                    ids.append(len(nodes) - 1)
                on_edge[e] = ids
    adj = [[] for _ in nodes]
    for f in F:
        ring = list(f)
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            ring += on_edge[(min(a, b), max(a, b))]
        for i in range(len(ring)):
            for j in range(i + 1, len(ring)):
                d = norm(sub(nodes[ring[i]], nodes[ring[j]]))
                adj[ring[i]].append((ring[j], d))
                adj[ring[j]].append((ring[i], d))
    dist = [float("inf")] * len(nodes)
    dist[s] = 0.0
    heap = [(0.0, s)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist[v]:
            continue
        for w, c in adj[v]:
            if d + c < dist[w]:
                dist[w] = d + c
                heapq.heappush(heap, (d + c, w))
    return dist[:len(P)]


def angle_sums(P, F):
    tot = [0.0] * len(P)
    for f in F:
        for k in range(3):
            v, a, b = f[k], f[(k + 1) % 3], f[(k + 2) % 3]
            x, y = sub(P[a], P[v]), sub(P[b], P[v])
            tot[v] += acos(max(-1.0, min(1.0, dot(x, y) / (norm(x) * norm(y)))))
    return tot


# ---- tests ----


def test_flat_grid_is_euclidean() -> None:
    rng = random.Random(1)
    P, F = grid(6, rng)
    for s in (0, 24):
        d = mmp_geodesic(P, F, [s])
        for v, q in enumerate(P):
            assert abs(d[v] - norm(sub(q, P[s]))) < 1e-9
    e = steiner_dijkstra(P, F, 0, 0)
    assert e[len(P) - 1] > sqrt(2) + 1e-3 or e[13] > hypot(1 / 6, 2 / 6) + 1e-3   # the edge graph is worse


def test_l_shape_matches_the_visibility_graph() -> None:
    P2, F = l_shape()
    P = [(float(x), float(y), 0.0) for x, y in P2]
    s = P2.index((Fraction(2), Fraction(0)))
    r = (Fraction(1), Fraction(1))                     # the reflex corner, a border vertex with angle 3 pi / 2

    def visible(p, q):                                 # exact: does segment p-q miss the open square x > 1, y > 1?
        lo, hi = Fraction(0), Fraction(1)
        for c in range(2):
            f0, f1 = p[c], q[c]
            if f0 == f1:
                if f0 <= 1:
                    return True
                continue
            tau = (1 - f0) / (f1 - f0)
            if f1 > f0:
                lo = max(lo, tau)
            else:
                hi = min(hi, tau)
        return lo >= hi

    d = mmp_geodesic(P, F, [s])
    bent = 0
    for v, q in enumerate(P2):
        if visible(P2[s], q):
            ref = hypot(*(float(a - b) for a, b in zip(q, P2[s])))
        else:
            bent += 1
            ref = hypot(*(float(a - b) for a, b in zip(r, P2[s]))) + hypot(*(float(a - b) for a, b in zip(q, r)))
        assert abs(d[v] - ref) < 1e-9
    assert bent == 3                                   # (1, 3/2), (1, 2) and (1/2, 2) must go around the corner


def test_cube_and_box_corners() -> None:
    P, F = box(1, 1, 1)
    d = mmp_geodesic(P, F, [0])
    assert abs(d[7] - sqrt(5)) < 1e-12                 # unfold two faces: a 1 x 2 rectangle
    assert abs(d[3] - sqrt(2)) < 1e-12 and abs(d[1] - 1) < 1e-12
    assert steiner_dijkstra(P, F, 0, 0)[7] > sqrt(5) + 0.1
    P, F = box(1, 2, 3)
    d = mmp_geodesic(P, F, [0])
    assert abs(d[7] - sqrt(18)) < 1e-12                # min of sqrt((1+2)^2+3^2), sqrt((1+3)^2+2^2), sqrt((2+3)^2+1^2)


def test_convex_polyhedra_match_brute_force_unfolding() -> None:
    rng = random.Random(7)
    meshes = [box(1, 1, 1), box(1, 2, 3)]
    for _ in range(3):
        meshes.append(octahedron(*(rng.uniform(0.5, 2) for _ in range(3))))
        meshes.append(icosahedron(*(rng.uniform(0.5, 2) for _ in range(3))))
    for P, F in meshes:
        for s in range(len(P)):
            d = mmp_geodesic(P, F, [s])
            ref = unfolding_distances(P, F, s)
            for v in range(len(P)):
                assert abs(d[v] - ref[v]) < 1e-9 * (1 + ref[v])


def test_terrain_with_saddles_lies_between_the_bounds() -> None:
    rng = random.Random(4)
    h = {(i, j): 0.25 * rng.random() for i in range(6) for j in range(6)}
    P, F = grid(5, rng, lambda i, j: h[(i, j)])
    tot = angle_sums(P, F)
    inner = [v for v in range(len(P)) if 0 < v % 6 < 5 and 0 < v // 6 < 5]
    assert sum(1 for v in inner if tot[v] > 2 * pi + 1e-6) >= 3           # there are saddle vertices
    for s in (0, 14):
        d = mmp_geodesic(P, F, [s])
        coarse, fine = steiner_dijkstra(P, F, s, 1), steiner_dijkstra(P, F, s, 7)     # 7 points include the midpoint
        gap = 0.0
        for v in range(len(P)):
            assert norm(sub(P[v], P[s])) <= d[v] + 1e-12                 # the chord is a lower bound
            assert d[v] <= fine[v] + 1e-9 <= coarse[v] + 2e-9            # Steiner paths are real paths
            gap = max(gap, fine[v] - d[v])
        assert gap < 0.01                                                # measured: 0.0049 and 0.0034


def test_symmetry_and_several_sources() -> None:
    rng = random.Random(9)
    h = {(i, j): 0.3 * rng.random() for i in range(5) for j in range(5)}
    P, F = grid(4, rng, lambda i, j: h[(i, j)])
    table = [mmp_geodesic(P, F, [s]) for s in range(len(P))]
    for a in range(len(P)):
        for b in range(len(P)):
            assert abs(table[a][b] - table[b][a]) < 1e-9                 # a root lost in the trimming shows up here
            for c in range(len(P)):
                assert table[a][c] <= table[a][b] + table[b][c] + 1e-9   # the triangle inequality
    both = mmp_geodesic(P, F, [3, 17])
    for v in range(len(P)):
        assert abs(both[v] - min(table[3][v], table[17][v])) < 1e-12
