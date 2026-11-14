# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-fairing/. The authors are listed in prov/6F02H1.jsonl.

import random
from fractions import Fraction as Fr

from implicit_fairing import explicit_step, implicit_fairing
from mp2mesh import (boundary_vertices, dot, grid_mesh, icosphere, neighbours, norm, octahedron, signed_volume,
                     stiffness_matrix, sub)


def close(a, b, eps=1e-9):
    return all(abs(u - v) <= eps for p, q in zip(a, b) for u, v in zip(p, q))


def noisy_sphere(level, seed, amp=0.1):
    rng = random.Random(seed)
    p, f = icosphere(level)
    return [tuple((1 + amp * (rng.random() - 0.5)) * c for c in q) for q in p], f


# ---- brute force for the cotangent matrix: the Dirichlet energy of the linear interpolant ----


def dirichlet_energy(points, faces, u):
    """1/2 of the sum over triangles of area * |grad u|^2, from the Gram matrix of two edges."""
    e = 0.0
    for a, b, c in faces:
        e1, e2 = sub(points[b], points[a]), sub(points[c], points[a])
        g11, g12, g22 = dot(e1, e1), dot(e1, e2), dot(e2, e2)
        det = g11 * g22 - g12 * g12
        d1, d2 = u[b] - u[a], u[c] - u[a]
        grad2 = (g22 * d1 * d1 - 2 * g12 * d1 * d2 + g11 * d2 * d2) / det
        e += 0.5 * (det ** 0.5 / 2) * grad2
    return e


def test_stiffness_matrix_is_the_hessian_of_the_dirichlet_energy() -> None:
    p, f = noisy_sphere(0, 3, 0.4)
    n = len(p)
    C = stiffness_matrix(p, f)

    def unit(*idx):
        u = [0.0] * n
        for i in idx:
            u[i] = 1.0
        return u

    for i in range(n):
        assert abs(C[i].get(i, 0.0) - 2 * dirichlet_energy(p, f, unit(i))) < 1e-12
        for j in range(n):
            if j != i:
                cij = dirichlet_energy(p, f, unit(i, j)) - dirichlet_energy(p, f, unit(i)) - dirichlet_energy(p, f, unit(j))
                assert abs(C[i].get(j, 0.0) - cij) < 1e-12


def test_octahedron_uniform_exact() -> None:
    p, f = octahedron()
    p = [tuple(Fr(c) for c in q) for q in p]
    for dt in (Fr(1, 2), Fr(1), Fr(3)):
        for steps in (1, 2):
            x = implicit_fairing(p, f, dt, steps, "uniform", solver="dense")
            assert x == [tuple(c / (1 + dt) ** steps for c in q) for q in p]


def test_octahedron_cotan() -> None:
    p, f = octahedron()
    for dt in (0.25, 1.0, 4.0):
        s = 1 / (1 + 2 * dt)                       # the first step
        x = implicit_fairing(p, f, dt, 1)
        assert close(x, [tuple(s * c for c in q) for q in p], 1e-12)
        s2 = s * s * s / (s * s + 2 * dt)          # the mass is taken again at the smaller size
        x = implicit_fairing(p, f, dt, 2)
        assert close(x, [tuple(s2 * c for c in q) for q in p], 1e-12)


def test_explicit_blows_up_implicit_does_not() -> None:
    p, f = octahedron()
    p = [tuple(Fr(c) for c in q) for q in p]
    assert explicit_step(p, f, Fr(3)) == [tuple(-2 * c for c in q) for q in p]
    assert implicit_fairing(p, f, Fr(3), 1, "uniform", solver="dense") == [tuple(c / 4 for c in q) for q in p]


def test_cg_against_dense_solver() -> None:
    p, f = noisy_sphere(1, 5)
    for w in ("cotan", "uniform"):
        a = implicit_fairing(p, f, 0.05, 2, w)
        b = implicit_fairing(p, f, 0.05, 2, w, solver="dense")
        assert close(a, b, 1e-9)
    rng = random.Random(8)
    g, gf = grid_mesh(4, 4)
    g = [(a, b, rng.uniform(-0.3, 0.3)) for a, b, _ in g]
    for w in ("cotan", "uniform"):
        assert close(implicit_fairing(g, gf, 0.5, 1, w), implicit_fairing(g, gf, 0.5, 1, w, solver="dense"), 1e-9)


def test_maximum_principle_and_weighted_centroid_exact() -> None:
    rng = random.Random(2)
    p, f = icosphere(0)
    p = [tuple(Fr(round(c * 32), 32) + Fr(rng.randrange(-4, 5), 64) for c in q) for q in p]
    nb = neighbours(len(p), f)
    for dt in (Fr(1, 10), Fr(10)):
        x = implicit_fairing(p, f, dt, 1, "uniform", solver="dense")
        for k in range(3):
            lo, hi = min(q[k] for q in p), max(q[k] for q in p)
            assert all(lo <= q[k] <= hi for q in x)
            assert sum(len(nb[i]) * x[i][k] for i in range(len(p))) == sum(len(nb[i]) * p[i][k] for i in range(len(p)))


def test_planar_mesh_is_fixed_with_cotan_weights() -> None:
    rng = random.Random(6)
    g, gf = grid_mesh(5, 5)
    g = [(a + rng.uniform(-0.15, 0.15), b + rng.uniform(-0.15, 0.15), 0.0) if 0 < a < 5 and 0 < b < 5 else (a, b, c)
         for a, b, c in g]
    x = implicit_fairing(g, gf, 10.0, 2, "cotan")
    assert close(x, g, 1e-9)
    y = implicit_fairing(g, gf, 10.0, 2, "uniform")
    assert max(norm(sub(a, b)) for a, b in zip(y, g)) > 0.05     # the uniform weights slide in the plane
    assert all(q[2] == 0.0 for q in y)


def test_border_fixed() -> None:
    rng = random.Random(4)
    g, gf = grid_mesh(4, 3)
    g = [(a, b, rng.uniform(-1, 1)) for a, b, _ in g]
    for w in ("cotan", "uniform"):
        x = implicit_fairing(g, gf, 2.0, 3, w)
        for v in boundary_vertices(gf):
            assert x[v] == g[v]


def test_sphere_shrinks_like_mean_curvature_flow() -> None:
    p, f = icosphere(2)
    for dt in (0.01, 1.0, 10.0):
        x = implicit_fairing(p, f, dt, 1)
        r = 1 / (1 + 2 * dt)                     # the smooth sphere: x' = x / (1 + 2 dt / r^2)
        assert all(abs(norm(q) - r) < 0.02 * r for q in x)
    q, f = noisy_sphere(2, 1)
    v0 = signed_volume(q, f)
    x = implicit_fairing(q, f, 0.01, 1, keep_volume=True)
    assert abs(signed_volume(x, f) - v0) < 1e-12


def test_noise_is_damped() -> None:
    q, f = noisy_sphere(2, 1)

    def spread(x):
        r = [norm(v) for v in x]
        m = sum(r) / len(r)
        return (sum((a - m) ** 2 for a in r) / len(r)) ** 0.5 / m

    prev = spread(q)
    for dt in (0.001, 0.003, 0.01):
        s = spread(implicit_fairing(q, f, dt, 1, keep_volume=True))
        assert s < prev                          # measured: 0.0285, 0.0275, 0.0257, 0.0215
        prev = s
