# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadric-error-metrics/. The authors are listed in prov/HHFZ8A.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

from quadric_error_metrics import add, error, optimal_position, plane_quadric, simplify


def F(x, den=1000):
    return Fraction(x).limit_denominator(den)


def mesh_stats(tris):
    """(closed manifold?, Euler characteristic) of an oriented triangle mesh."""
    directed = Counter()
    for a, b, c in tris:
        if len({a, b, c}) < 3:
            return False, None
        for u, v in ((a, b), (b, c), (c, a)):
            directed[(u, v)] += 1
    for (u, v), k in directed.items():
        if k != 1 or directed.get((v, u)) != 1:
            return False, None
    link = {}
    for a, b, c in tris:
        for u, v, w in ((a, b, c), (b, c, a), (c, a, b)):
            link.setdefault(u, {})[v] = w
    for u, nxt in link.items():
        start = next(iter(nxt))
        x, steps = start, 0
        while True:
            x = nxt[x]
            steps += 1
            if x == start:
                break
        if steps != len(nxt):
            return False, None
    return True, len(link) - len(directed) // 2 + len(tris)


def sphere_mesh(levels):
    """A subdivided octahedron with rational vertices near the unit sphere."""
    verts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    verts = [tuple(Fraction(x) for x in v) for v in verts]
    tris = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    for _ in range(levels):
        mid = {}

        def m(a, b):
            key = (min(a, b), max(a, b))
            if key not in mid:
                p = tuple((verts[a][t] + verts[b][t]) / 2 for t in range(3))
                s = F(1 / math.sqrt(sum(float(x) ** 2 for x in p)))
                verts.append(tuple(x * s for x in p))
                mid[key] = len(verts) - 1
            return mid[key]
        new = []
        for a, b, c in tris:
            ab, bc, ca = m(a, b), m(b, c), m(c, a)
            new += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
        tris = new
    return verts, tris


def torus_mesh(nu, nv, big=3, small=1):
    verts, tris = [], []
    for i in range(nu):
        for j in range(nv):
            u, v = 2 * math.pi * i / nu, 2 * math.pi * j / nv
            verts.append((F((big + small * math.cos(v)) * math.cos(u)), F((big + small * math.cos(v)) * math.sin(u)),
                          F(small * math.sin(v))))
    for i in range(nu):
        for j in range(nv):
            a, b = i * nv + j, ((i + 1) % nu) * nv + j
            c, d = ((i + 1) % nu) * nv + (j + 1) % nv, i * nv + (j + 1) % nv
            tris += [(a, b, c), (a, c, d)]
    return verts, tris


def cube_mesh(k):
    """The surface of [0, k]^3, each face a k by k grid of squares split into triangles."""
    index, verts, tris = {}, [], []

    def vid(p):
        if p not in index:
            index[p] = len(verts)
            verts.append(tuple(Fraction(x) for x in p))
        return index[p]
    for axis in range(3):
        for side in (0, k):
            for s in range(k):
                for t in range(k):
                    quad = []
                    for ds, dt in ((0, 0), (1, 0), (1, 1), (0, 1)):
                        p = [0, 0, 0]
                        p[axis] = side
                        p[(axis + 1) % 3] = s + ds
                        p[(axis + 2) % 3] = t + dt
                        quad.append(vid(tuple(p)))
                    a, b, c, d = quad
                    if side == 0:
                        a, b, c, d = a, d, c, b  # outward on the low side
                    tris += [(a, b, c), (a, c, d)]
    return verts, tris


def test_quadric_is_sum_of_squared_distances_exact():
    rng = random.Random(1)
    for _ in range(200):
        tri_list = [[tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(3)) for _ in range(3)]
                    for _ in range(rng.randint(1, 5))]
        q = (0,) * 10
        for t in tri_list:
            q = add(q, plane_quadric(*t))
        v = tuple(Fraction(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(3))
        want = Fraction(0)
        for p0, p1, p2 in tri_list:
            u = [p1[i] - p0[i] for i in range(3)]
            w = [p2[i] - p0[i] for i in range(3)]
            n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
            nn = sum(x * x for x in n)
            if nn:
                # distance from v to its orthogonal projection on the plane
                s = sum(n[i] * (v[i] - p0[i]) for i in range(3)) / nn
                proj = [v[i] - s * n[i] for i in range(3)]
                want += sum((v[i] - proj[i]) ** 2 for i in range(3))
        assert error(q, v) == want


def test_optimal_position_exact():
    rng = random.Random(2)
    for _ in range(100):
        q = (0,) * 10
        for _ in range(rng.randint(3, 6)):
            q = add(q, plane_quadric(*[tuple(Fraction(rng.randint(-9, 9)) for _ in range(3)) for _ in range(3)]))
        vi = tuple(Fraction(rng.randint(-5, 5)) for _ in range(3))
        vj = tuple(Fraction(rng.randint(-5, 5)) for _ in range(3))
        v = optimal_position(q, vi, vj)
        e = error(q, v)
        for _ in range(20):
            w = tuple(Fraction(rng.randint(-50, 50), 7) for _ in range(3))
            assert e <= error(q, w)
        assert e <= min(error(q, vi), error(q, vj))
    # two parallel planes: the 3 by 3 part is singular, the best of the three candidates is used
    q = add(plane_quadric((0, 0, 0), (1, 0, 0), (0, 1, 0)), plane_quadric((0, 0, 2), (1, 0, 2), (0, 1, 2)))
    v = optimal_position(q, (0, 0, 0), (Fraction(0), Fraction(0), Fraction(2)))
    assert v == (0, 0, 1) and error(q, v) == 2


def reference(verts, tris, target):
    """Brute force: at each step recompute every edge cost, take the cheapest valid one."""
    pos = {i: v for i, v in enumerate(verts)}
    quad = {i: (0,) * 10 for i in pos}
    for t in tris:
        k = plane_quadric(*(verts[v] for v in t))
        for v in t:
            quad[v] = add(quad[v], k)
    faces = [tuple(t) for t in tris]
    trace = []
    while len(faces) > target:
        edges = sorted({(min(a, b), max(a, b)) for t in faces for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0]))})
        cands = []
        for i, j in edges:
            q = add(quad[i], quad[j])
            v = optimal_position(q, pos[i], pos[j])
            cands.append((error(q, v), i, j, v))
        cands.sort(key=lambda c: c[:3])
        done = False
        for cost, i, j, v in cands:
            fi = [t for t in faces if i in t]
            fj = [t for t in faces if j in t]
            both = [t for t in fi if j in t]
            ni = {u for t in fi for u in t} - {i}
            nj = {u for t in fj for u in t} - {j}
            if ni & nj != {u for t in both for u in t} - {i, j}:
                continue
            if {frozenset(t) - {i} for t in fi} & {frozenset(t) - {j} for t in fj}:
                continue
            ci = Counter(u for t in fi for u in t if u != i)
            cj = Counter(u for t in fj for u in t if u != j)
            bi = {u for u, k in ci.items() if k == 1}
            bj = {u for u, k in cj.items() if k == 1}
            if (bi and bj and len(both) == 2) or bi & bj:
                continue
            ok = True
            for t in fi + fj:
                if t in both:
                    continue
                o = [pos[u] for u in t]
                nw = [v if u in (i, j) else pos[u] for u in t]
                cr = lambda p: [(p[1][1] - p[0][1]) * (p[2][2] - p[0][2]) - (p[1][2] - p[0][2]) * (p[2][1] - p[0][1]),
                                (p[1][2] - p[0][2]) * (p[2][0] - p[0][0]) - (p[1][0] - p[0][0]) * (p[2][2] - p[0][2]),
                                (p[1][0] - p[0][0]) * (p[2][1] - p[0][1]) - (p[1][1] - p[0][1]) * (p[2][0] - p[0][0])]
                if sum(x * y for x, y in zip(cr(o), cr(nw))) <= 0:
                    ok = False
                    break
            if not ok:
                continue
            trace.append((cost, i, j))
            pos[i] = v
            quad[i] = add(quad[i], quad[j])
            faces = [tuple(i if u == j else u for u in t) for t in faces if t not in both]
            done = True
            break
        if not done:
            break
    return trace, faces, pos


def test_greedy_order_matches_brute_force():
    for verts, tris, targets in ((sphere_mesh(1)[0], sphere_mesh(1)[1], (24, 10, 4)),
                                 (torus_mesh(8, 5)[0], torus_mesh(8, 5)[1], (50, 20))):
        for target in targets:
            trace = []
            out_v, out_t = simplify(verts, tris, target, trace)
            want_trace, want_faces, want_pos = reference(verts, tris, target)
            assert trace == want_trace
            keep = sorted({u for t in want_faces for u in t})
            assert out_v == [want_pos[u] for u in keep]
            idx = {u: k for k, u in enumerate(keep)}
            assert sorted(out_t) == sorted(tuple(idx[u] for u in t) for t in want_faces)


def test_topology_is_preserved():
    verts, tris = sphere_mesh(2)  # 128 triangles
    for target in (60, 20, 8):
        v, t = simplify(verts, tris, target)
        ok, chi = mesh_stats(t)
        assert ok and chi == 2 and len(t) <= target
    v, t = simplify(verts, tris, 0)
    assert len(t) == 4 and len(v) == 4  # a tetrahedron cannot be collapsed further
    verts, tris = torus_mesh(10, 6)  # 120 triangles
    for target in (80, 40):
        v, t = simplify(verts, tris, target)
        ok, chi = mesh_stats(t)
        assert ok and chi == 0
    v, t = simplify(verts, tris, 0)
    ok, chi = mesh_stats(t)
    assert ok and chi == 0  # it stops when every collapse would change the topology


def disk_stats(tris):
    """True if the mesh is an oriented surface with one border loop and Euler characteristic 1."""
    directed = Counter()
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            directed[(u, v)] += 1
    if any(k != 1 for k in directed.values()) or any(len(set(t)) < 3 for t in tris):
        return False
    border = {u: v for (u, v) in directed if (v, u) not in directed}
    if not border or len(set(border.values())) != len(border):
        return False
    start, x, steps = next(iter(border)), next(iter(border)), 0
    while True:
        x = border[x]
        steps += 1
        if x == start:
            break
    if steps != len(border):
        return False  # more than one border loop
    edges = {frozenset(e) for e in directed}
    nverts = len({u for t in tris for u in t})
    return nverts - len(edges) + len(tris) == 1


def test_open_mesh_keeps_its_border():
    verts, tris = sphere_mesh(2)
    cap = [t for t in tris if all(verts[u][2] >= 0 for u in t)]  # a half sphere, a disk
    assert disk_stats(cap)
    for target in (40, 10, 1):
        trace = []
        v, t = simplify(verts, cap, target, trace)
        assert disk_stats(t)
        want_trace, _, _ = reference(verts, cap, target)
        assert trace == want_trace


def test_cube_reduces_to_twelve_triangles_with_zero_error():
    verts, tris = cube_mesh(4)
    assert len(tris) == 192
    trace = []
    v, t = simplify(verts, tris, 12, trace)
    assert len(t) == 12 and len(v) == 8
    assert all(cost == 0 for cost, _, _ in trace)
    assert sorted(v) == sorted((Fraction(x), Fraction(y), Fraction(z)) for x in (0, 4) for y in (0, 4) for z in (0, 4))
    ok, chi = mesh_stats(t)
    assert ok and chi == 2


def test_float_input_and_edge_cases():
    verts, tris = sphere_mesh(2)
    fv = [tuple(float(x) for x in p) for p in verts]
    v, t = simplify(fv, tris, 40)
    ok, chi = mesh_stats(t)
    assert ok and chi == 2 and len(t) <= 40
    assert all(abs(math.sqrt(sum(x * x for x in p)) - 1) < 0.3 for p in v)
    v, t = simplify(verts, tris, 10 ** 6)
    assert v == verts and t == [tuple(x) for x in tris]  # nothing to do
    assert simplify([], [], 0) == ([], [])
