# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-contouring/. The authors are listed in prov/B0HXQ1.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

from dual_contouring import _jacobi_eigen, dual_contouring, solve_qef


def tris_of(quads):
    out = []
    for a, b, c, d in quads:
        out.append((a, b, c))
        out.append((a, c, d))
    return out


def directed_balance(quads):
    """Each undirected quad edge is used equally often in both directions."""
    cnt = Counter()
    for q in quads:
        for t in range(4):
            cnt[(q[t], q[(t + 1) % 4])] += 1
    return all(cnt[(a, b)] == cnt[(b, a)] for (a, b) in cnt), cnt


def mesh_stats(nv, tris):
    """(closed manifold?, Euler characteristic) of an oriented triangle mesh."""
    directed = Counter()
    for a, b, c in tris:
        if len({a, b, c}) < 3:
            return False, None
        for u, v in ((a, b), (b, c), (c, a)):
            directed[(u, v)] += 1
    for (u, v), m in directed.items():
        if m != 1 or directed.get((v, u)) != 1:
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
    used = len(link)
    edges = len(directed) // 2
    return True, used - edges + len(tris)


def signed_volume(verts, tris):
    vol = 0.0
    for a, b, c in tris:
        p, q, r = verts[a], verts[b], verts[c]
        vol += (p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0])
                + p[2] * (q[0] * r[1] - q[1] * r[0])) / 6.0
    return vol


def exact_least_squares(points, normals):
    """Unique minimizer of sum (n . (x - p))^2 by Fraction Gaussian elimination."""
    nf = [tuple(Fraction(v) for v in n) for n in normals]
    pf = [tuple(Fraction(v) for v in p) for p in points]
    m = [[sum(n[i] * n[j] for n in nf) for j in range(3)] + [sum(n[i] * (n[0] * p[0] + n[1] * p[1] + n[2] * p[2])
                                                               for n, p in zip(nf, pf))] for i in range(3)]
    for col in range(3):
        piv = next(r for r in range(col, 3) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        for r in range(3):
            if r != col and m[r][col] != 0:
                fac = m[r][col] / m[col][col]
                m[r] = [m[r][t] - fac * m[col][t] for t in range(4)]
    return tuple(m[i][3] / m[i][i] for i in range(3))


def test_jacobi_eigen():
    rng = random.Random(1)
    for _ in range(200):
        b = [[rng.uniform(-2, 2) for _ in range(3)] for _ in range(3)]
        a = [[sum(b[k][i] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        vals, vecs = _jacobi_eigen(a)
        for lam, e in zip(vals, vecs):
            ae = [sum(a[i][j] * e[j] for j in range(3)) for i in range(3)]
            assert all(abs(ae[i] - lam * e[i]) < 1e-9 for i in range(3))
            assert abs(sum(x * x for x in e) - 1) < 1e-12
        for i in range(3):
            for j in range(i + 1, 3):
                assert abs(sum(vecs[i][t] * vecs[j][t] for t in range(3))) < 1e-9


def test_qef_full_rank_matches_exact_rational():
    rng = random.Random(2)
    for _ in range(200):
        k = rng.randint(3, 7)
        normals, points = [], []
        for _ in range(k):
            v = [rng.randint(-5, 5) for _ in range(3)]
            while v == [0, 0, 0]:
                v = [rng.randint(-5, 5) for _ in range(3)]
            normals.append(tuple(Fraction(x) for x in v))
            points.append(tuple(Fraction(rng.randint(-20, 20), 4) for _ in range(3)))
        ata = [[sum(n[i] * n[j] for n in normals) for j in range(3)] for i in range(3)]
        det = (ata[0][0] * (ata[1][1] * ata[2][2] - ata[1][2] * ata[2][1])
               - ata[0][1] * (ata[1][0] * ata[2][2] - ata[1][2] * ata[2][0])
               + ata[0][2] * (ata[1][0] * ata[2][1] - ata[1][1] * ata[2][0]))
        vals, _ = _jacobi_eigen([[float(x) for x in row] for row in ata])
        if det == 0 or min(vals) < 0.05 * max(vals):
            continue  # truncation would act; the exact unique minimizer is not the target
        want = exact_least_squares(points, normals)
        got = solve_qef([tuple(map(float, p)) for p in points], [tuple(map(float, n)) for n in normals], tol=0.1)
        assert all(abs(got[i] - float(want[i])) < 1e-9 for i in range(3))


def test_qef_rank_deficient_keeps_mass_point():
    # two planes x = 1 and y = 2: the minimizers form a line; pick the point nearest the mass point
    pts = [(1.0, 0.3, 0.7), (1.0, 0.9, 0.1), (0.4, 2.0, 0.5)]
    nms = [(1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    x = solve_qef(pts, nms)
    m = [sum(p[i] for p in pts) / 3 for i in range(3)]
    assert abs(x[0] - 1) < 1e-12 and abs(x[1] - 2) < 1e-12 and abs(x[2] - m[2]) < 1e-12
    # one normal direction: the mass point is a minimizer, so it is the answer
    pts = [(0.2, 0.0, 0.0), (-1.0, 0.9, 0.0), (1.7, 0.3, 1.5)]
    nms = [(0.6, 0.8, 0.0), (0.6, 0.8, 0.0), (0.6, 0.8, 0.0)]
    x = solve_qef(pts, nms)
    assert all(abs(x[i] - sum(p[i] for p in pts) / 3) < 1e-12 for i in range(3))
    # nearly parallel normals: truncation keeps the vertex near the mass point
    x = solve_qef([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], [(0.0, 1.0, 0.0), (0.001, 0.9999995, 0.0)])
    assert abs(x[0] - 0.5) < 1e-3 and abs(x[1]) < 1e-3


def box_field(cx, cy, cz, r):
    def f(x, y, z):
        return max(abs(x - cx), abs(y - cy), abs(z - cz)) - r

    def g(x, y, z):
        d = (x - cx, y - cy, z - cz)
        k = max(range(3), key=lambda t: abs(d[t]))
        out = [0.0, 0.0, 0.0]
        out[k] = math.copysign(1.0, d[k])
        return tuple(out)
    return f, g


def test_box_corners_and_edges_are_kept():
    cx = cy = cz = 3.85
    r = 2.55  # the box [1.3, 6.4]^3, corners inside cells, not on grid planes
    f, g = box_field(cx, cy, cz, r)
    verts, quads = dual_contouring(f, g, (0.0, 0.0, 0.0), 1.0, 8)
    for v in verts:
        assert abs(f(*v)) < 1e-9  # every vertex lies on the box surface
    corners = {(a, b, d) for a in (1.3, 6.4) for b in (1.3, 6.4) for d in (1.3, 6.4)}
    found = {tuple(round(t, 9) for t in v) for v in verts}
    assert corners <= found
    # vertices on the 12 box edges: two coordinates at the extremes
    on_edges = [v for v in verts if sum(min(abs(t - 1.3), abs(t - 6.4)) < 1e-9 for t in v) == 2]
    assert len(on_edges) == 12 * 4  # 4 interior cells along each edge of length 5.1
    ok, chi = mesh_stats(len(verts), tris_of(quads))
    assert ok and chi == 2
    assert abs(signed_volume(verts, tris_of(quads)) - 5.1 ** 3) < 1e-9


def test_plane_is_exact():
    nrm = (0.48, 0.6, 0.64)  # a unit vector
    def f(x, y, z):
        return nrm[0] * x + nrm[1] * y + nrm[2] * z - 2.0

    def g(x, y, z):
        return nrm
    verts, quads = dual_contouring(f, g, (0.0, 0.0, 0.0), 0.5, 8)
    assert quads
    for v in verts:
        assert abs(f(*v)) < 1e-12
    for a, b, c, d in quads:  # every quad is flat and its normal points along the gradient
        p, q, r = verts[a], verts[b], verts[c]
        u = [q[i] - p[i] for i in range(3)]
        w = [r[i] - p[i] for i in range(3)]
        cr = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        assert sum(cr[i] * nrm[i] for i in range(3)) > 0


def sphere(cx, cy, cz, r):
    def f(x, y, z):
        return math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) - r

    def g(x, y, z):
        d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
        return ((x - cx) / d, (y - cy) / d, (z - cz) / d)
    return f, g


def test_sphere_torus_two_spheres():
    f, g = sphere(5.1, 4.9, 5.05, 3.3)
    verts, quads = dual_contouring(f, g, (0.0, 0.0, 0.0), 1.0, 10)
    ok, chi = mesh_stats(len(verts), tris_of(quads))
    assert ok and chi == 2
    assert max(abs(f(*v)) for v in verts) < 0.15  # at most 0.15 h from the sphere
    vol = signed_volume(verts, tris_of(quads))
    assert abs(vol - 4 / 3 * math.pi * 3.3 ** 3) < 0.05 * vol

    def ft(x, y, z):
        q = math.sqrt((x - 8.1) ** 2 + (y - 7.9) ** 2) - 5.0
        return math.sqrt(q * q + (z - 8.05) ** 2) - 2.0

    def gt(x, y, z):
        rho = math.sqrt((x - 8.1) ** 2 + (y - 7.9) ** 2)
        q = rho - 5.0
        d = math.sqrt(q * q + (z - 8.05) ** 2)
        return (q / d * (x - 8.1) / rho, q / d * (y - 7.9) / rho, (z - 8.05) / d)
    # with h = 1 the top circle of the tube is 0.05 above the grid plane z = 10, which gives
    # ambiguous faces and edges in 4 quads; with h = 1/2 the mesh is a manifold
    verts, quads = dual_contouring(ft, gt, (0.0, 0.0, 0.0), 1.0, 16)
    assert not mesh_stats(len(verts), tris_of(quads))[0]
    assert directed_balance(quads)[0]
    verts, quads = dual_contouring(ft, gt, (0.0, 0.0, 0.0), 0.5, 32)
    ok, chi = mesh_stats(len(verts), tris_of(quads))
    assert ok and chi == 0

    fa, ga = sphere(3.1, 3.9, 4.05, 2.2)
    fb, gb = sphere(9.1, 8.1, 7.95, 2.4)

    def f2(x, y, z):
        return min(fa(x, y, z), fb(x, y, z))

    def g2(x, y, z):
        return ga(x, y, z) if fa(x, y, z) < fb(x, y, z) else gb(x, y, z)
    verts, quads = dual_contouring(f2, g2, (0.0, 0.0, 0.0), 1.0, 13)
    ok, chi = mesh_stats(len(verts), tris_of(quads))
    assert ok and chi == 4


def trilinear(vals, n):
    """A callable trilinear interpolant of vals[i][j][k] on [0, n]^3, with its gradient."""
    def cellof(x, y, z):
        i = min(max(int(math.floor(x)), 0), n - 1)
        j = min(max(int(math.floor(y)), 0), n - 1)
        k = min(max(int(math.floor(z)), 0), n - 1)
        return i, j, k, x - i, y - j, z - k

    def f(x, y, z):
        i, j, k, u, v, w = cellof(x, y, z)
        s = 0.0
        for a in (0, 1):
            for b in (0, 1):
                for d in (0, 1):
                    s += vals[i + a][j + b][k + d] * (u if a else 1 - u) * (v if b else 1 - v) * (w if d else 1 - w)
        return s

    def g(x, y, z):
        i, j, k, u, v, w = cellof(x, y, z)
        out = [0.0, 0.0, 0.0]
        for a in (0, 1):
            for b in (0, 1):
                for d in (0, 1):
                    val = vals[i + a][j + b][k + d]
                    fu, fv, fw = (u if a else 1 - u), (v if b else 1 - v), (w if d else 1 - w)
                    du, dv, dw = (1 if a else -1), (1 if b else -1), (1 if d else -1)
                    out[0] += val * du * fv * fw
                    out[1] += val * fu * dv * fw
                    out[2] += val * fu * fv * dw
        if out == [0.0, 0.0, 0.0]:
            out = [1.0, 0.0, 0.0]
        return tuple(out)
    return f, g


def test_random_grids_against_brute_force():
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(2, 5)
        vals = [[[rng.choice([-3, -1, 2, 5]) if 0 < i < n and 0 < j < n and 0 < k < n else 5
                  for k in range(n + 1)] for j in range(n + 1)] for i in range(n + 1)]
        f, g = trilinear(vals, n)
        verts, quads = dual_contouring(f, g, (0.0, 0.0, 0.0), 1.0, n, c=0.5)
        # brute force: one quad per grid edge with a sign change, one vertex per cell with one
        active, cells = 0, set()
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(n + 1):
                    for a in range(3):
                        q = [i, j, k]
                        q[a] += 1
                        if q[a] <= n and (vals[i][j][k] < 0.5) != (vals[q[0]][q[1]][q[2]] < 0.5):
                            active += 1
                            b1, b2 = (a + 1) % 3, (a + 2) % 3
                            for o1 in (-1, 0):
                                for o2 in (-1, 0):
                                    cl = [i, j, k]
                                    cl[b1] += o1
                                    cl[b2] += o2
                                    if all(0 <= cl[t] < n for t in range(3)):
                                        cells.add(tuple(cl))
        assert len(quads) == active and len(verts) == len(cells)
        balanced, cnt = directed_balance(quads)
        assert balanced  # the quad mesh is closed (the boundary of a union of dual cubes)
        for (a, b), m in cnt.items():
            assert m in (1, 2)  # an edge is in 2 quads, or in 4 at an ambiguous face
        for v, cl in zip(verts, sorted(cells)):
            assert all(cl[t] - 1e-12 <= v[t] <= cl[t] + 1 + 1e-12 for t in range(3))


def test_ambiguous_face_gives_a_non_manifold_edge():
    # inside grid points (1,1,1) and (1,2,2): diagonal on a face, no inside edge between them
    n = 3
    vals = [[[5.0] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]
    vals[1][1][1] = -3.0
    vals[1][2][2] = -3.0
    f, g = trilinear(vals, n)
    verts, quads = dual_contouring(f, g, (0.0, 0.0, 0.0), 1.0, n, c=0.5)
    assert len(quads) == 12
    balanced, cnt = directed_balance(quads)
    assert balanced
    assert max(cnt.values()) == 2  # one directed edge in two quads: four quads meet at one edge
    ok, _ = mesh_stats(len(verts), tris_of(quads))
    assert not ok


def test_edge_cases():
    f, g = sphere(0.0, 0.0, 0.0, 100.0)
    assert dual_contouring(f, g, (0.0, 0.0, 0.0), 1.0, 3) == ([], [])  # all inside
    f, g = sphere(50.0, 50.0, 50.0, 1.0)
    assert dual_contouring(f, g, (0.0, 0.0, 0.0), 1.0, 3) == ([], [])  # all outside
    # one inside grid point gives a closed cube of 6 quads around it
    f, g = sphere(1.0, 1.0, 1.0, 0.5)
    verts, quads = dual_contouring(f, g, (0.0, 0.0, 0.0), 1.0, 2)
    assert len(verts) == 8 and len(quads) == 6
    ok, chi = mesh_stats(len(verts), tris_of(quads))
    assert ok and chi == 2
    assert signed_volume(verts, tris_of(quads)) > 0
