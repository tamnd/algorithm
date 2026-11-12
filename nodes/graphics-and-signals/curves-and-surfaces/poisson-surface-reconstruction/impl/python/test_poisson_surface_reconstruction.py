# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/poisson-surface-reconstruction/. The authors are listed in prov/6BENWT.jsonl.

import math
from collections import Counter
from fractions import Fraction
from itertools import product

from poisson_surface_reconstruction import (MASS, MIXED, STIFF, conjugate_gradient, divergence_rhs, evaluate,
                                            laplacian, poisson_reconstruction)


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


def signed_volume(verts, tris):
    vol = 0.0
    for a, b, c in tris:
        p, q, r = verts[a], verts[b], verts[c]
        vol += (p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0])
                + p[2] * (q[0] * r[1] - q[1] * r[0])) / 6.0
    return vol


def hat(i, x):
    return max(Fraction(0), 1 - abs(x - i))


def dhat(i, x, side):
    # derivative of the hat at node i on the open interval (side - 1/2 +- 1/2), side in {i - 1, i}
    return Fraction(1) if side == i - 1 else Fraction(-1)


def simpson(f, a, b):
    return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))


def test_one_dimensional_integrals_exact():
    """The stencils are the exact integrals of products of hat functions (h = 1), by Simpson's
    rule on each unit interval, which is exact for the quadratic products."""
    i = 5
    for off in (-1, 0, 1):
        j = i + off
        mass = stiff = mixed = Fraction(0)
        for a in range(i - 1, i + 1):  # the support of phi_i
            lo, hi = Fraction(a), Fraction(a + 1)
            mass += simpson(lambda x: hat(i, x) * hat(j, x), lo, hi)
            if j - 1 <= a <= j:
                stiff += simpson(lambda x: dhat(i, x, a) * dhat(j, x, a), lo, hi)
                mixed += simpson(lambda x: hat(i, x) * dhat(j, x, a), lo, hi)
        assert mass == Fraction(MASS[off]).limit_denominator(100)
        assert stiff == STIFF[off]
        assert mixed == Fraction(MIXED[off])


def exact_system(m, field):
    """Dense L and b over Fraction, from the 1D integrals, for h = 1."""
    fm = {k: Fraction(v).limit_denominator(100) for k, v in MASS.items()}
    fs = {k: Fraction(v) for k, v in STIFF.items()}
    fx = {k: Fraction(v) for k, v in MIXED.items()}
    inner = [(i, j, k) for k in range(1, m - 1) for j in range(1, m - 1) for i in range(1, m - 1)]
    pos = {g: t for t, g in enumerate(inner)}
    L = [[Fraction(0)] * len(inner) for _ in inner]
    b = [Fraction(0)] * len(inner)
    for g in inner:
        for d in product((-1, 0, 1), repeat=3):
            g2 = tuple(g[t] + d[t] for t in range(3))
            if g2 in pos:
                val = sum((fs if a == 0 else fm)[d[0]] * (fs if a == 1 else fm)[d[1]] * (fs if a == 2 else fm)[d[2]]
                          for a in range(3))
                L[pos[g]][pos[g2]] = val
            if all(0 <= g2[t] < m for t in range(3)):
                n = g2[0] + m * (g2[1] + m * g2[2])
                for a in range(3):
                    w = Fraction(1)
                    for t in range(3):
                        w *= fx[-d[t]] if t == a else fm[d[t]]  # integral phi_n d_a phi_g, n = g + d
                    b[pos[g]] += field[a][n] * w
    return inner, L, b


def gauss(L, b):
    n = len(b)
    a = [row[:] + [b[r]] for r, row in enumerate(L)]
    for c in range(n):
        piv = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        for r in range(c + 1, n):
            if a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [a[r][t] - f * a[c][t] for t in range(n + 1)]
    x = [Fraction(0)] * n
    for r in range(n - 1, -1, -1):
        x[r] = (a[r][n] - sum(a[r][t] * x[t] for t in range(r + 1, n))) / a[r][r]
    return x


def test_galerkin_system_and_cg_against_exact_rational_solve():
    m = 6
    field = [[Fraction(0)] * m ** 3 for _ in range(3)]
    vals = {(2, 2, 2): (1, 0, -2), (3, 2, 2): (-1, 1, 0), (2, 3, 3): (0, -3, 1), (3, 3, 2): (2, 2, 1)}
    for (i, j, k), v in vals.items():
        for a in range(3):
            field[a][i + m * (j + m * k)] = Fraction(v[a], 4)
    inner, L, b = exact_system(m, field)
    # the matrix-free float operators agree with the dense exact system
    fb = divergence_rhs([[float(v) for v in comp] for comp in field], m, 1.0)
    for t, g in enumerate(inner):
        assert abs(fb[g[0] + m * (g[1] + m * g[2])] - float(b[t])) < 1e-12
    for t, g in enumerate(inner[:20]):
        e = [0.0] * m ** 3
        e[g[0] + m * (g[1] + m * g[2])] = 1.0
        col = laplacian(e, m, 1.0)
        for s, g2 in enumerate(inner):
            assert abs(col[g2[0] + m * (g2[1] + m * g2[2])] - float(L[s][t])) < 1e-12
    want = gauss(L, b)
    got = conjugate_gradient(lambda v: laplacian(v, m, 1.0), fb, tol=1e-14)
    for t, g in enumerate(inner):
        assert abs(got[g[0] + m * (g[1] + m * g[2])] - float(want[t])) < 1e-10


def fibonacci_sphere(n, center=(0.0, 0.0, 0.0), r=1.0):
    pts, nms = [], []
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        s = math.sqrt(1 - z * z)
        x, y = s * math.cos(golden * i), s * math.sin(golden * i)
        nms.append((x, y, z))
        pts.append((center[0] + r * x, center[1] + r * y, center[2] + r * z))
    return pts, nms


def test_sphere():
    pts, nms = fibonacci_sphere(800, (0.1, -0.2, 0.3), 1.0)
    verts, tris, chi, (origin, h, m, iso) = poisson_reconstruction(pts, nms, depth=4)
    ok, e = mesh_stats(tris)
    assert ok and e == 2
    assert 0 < iso
    assert evaluate(chi, (0.1, -0.2, 0.3), origin, h, m) > iso  # the center is inside
    dists = [math.dist(v, (0.1, -0.2, 0.3)) for v in verts]
    assert max(abs(d - 1) for d in dists) < h  # within one cell of the true sphere
    vol = signed_volume(verts, tris)
    assert abs(vol - 4 / 3 * math.pi) < 0.1 * vol


def test_two_spheres_and_partial_sampling():
    p1, n1 = fibonacci_sphere(400, (0.0, 0.0, 0.0), 1.0)
    p2, n2 = fibonacci_sphere(400, (3.0, 0.4, -0.3), 1.0)
    verts, tris, _, _ = poisson_reconstruction(p1 + p2, n1 + n2, depth=4)
    ok, e = mesh_stats(tris)
    assert ok and e == 4
    # remove a cap of the sphere: the output is still closed, the hole is filled
    pts, nms = fibonacci_sphere(800)
    keep = [i for i, p in enumerate(pts) if p[2] < 0.7]
    verts, tris, _, _ = poisson_reconstruction([pts[i] for i in keep], [nms[i] for i in keep], depth=4)
    ok, e = mesh_stats(tris)
    assert ok and e == 2


def test_edge_cases():
    # flipping all normals turns inside and outside: chi changes sign, so the iso value is negative
    pts, nms = fibonacci_sphere(300)
    _, _, chi, (origin, h, m, iso) = poisson_reconstruction(pts, [tuple(-c for c in n) for n in nms], depth=3)
    assert iso < 0 and evaluate(chi, (0.0, 0.0, 0.0), origin, h, m) < iso
    # zero right hand side gives chi = 0
    assert conjugate_gradient(lambda v: laplacian(v, 5, 1.0), [0.0] * 125) == [0.0] * 125
