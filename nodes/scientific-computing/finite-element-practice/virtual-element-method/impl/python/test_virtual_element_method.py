# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/virtual-element-method/. The authors are listed in prov/EYHGHZ.jsonl.

import math
import random

import scimat
from virtual_element_method import (
    conjugate_gradient,
    element_matrices,
    errors,
    polygon_area,
    polygon_mesh,
    polygon_quadrature,
    solve_vem,
)

SQUARE = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]


def u_sin(x, y):
    return math.sin(math.pi * x) * math.sin(math.pi * y)


def grad_sin(x, y):
    return (math.pi * math.cos(math.pi * x) * math.sin(math.pi * y), math.pi * math.sin(math.pi * x) * math.cos(math.pi * y))


def f_sin(x, y):
    return 2 * math.pi ** 2 * u_sin(x, y)


def random_polygon(rng, m):
    """A convex polygon: m sorted angles on a jittered ellipse."""
    angles = sorted(rng.uniform(0, 2 * math.pi) for _ in range(m))
    a, b = rng.uniform(0.5, 2), rng.uniform(0.5, 2)
    return [(3 + a * math.cos(t), -1 + b * math.sin(t)) for t in angles]


def test_unit_square_hand_example():
    k, pstar, centre, h = element_matrices(SQUARE)
    expected = [[0.75 if i == j else -0.25 for j in range(4)] for i in range(4)]
    assert all(abs(k[i][j] - expected[i][j]) < 1e-14 for i in range(4) for j in range(4))
    assert centre == (0.5, 0.5) and abs(h - math.sqrt(2)) < 1e-15
    # without stabilization the hourglass mode costs no energy
    k0, _, _, _ = element_matrices(SQUARE, tau=0.0)
    hourglass = [1.0, -1.0, 1.0, -1.0]
    assert max(abs(v) for v in scimat.matvec(k0, hourglass)) < 1e-14
    assert max(abs(v) for v in scimat.matvec(k, hourglass)) > 0.9


def test_quadrature_is_exact_to_degree_5():
    pts = [(0.0, 0.0), (2.0, 0.0), (2.0, 1.0), (0.0, 1.0)]
    q = polygon_quadrature(pts)
    for p in range(6):
        for r in range(6 - p):
            exact = 2 ** (p + 1) / (p + 1) / (r + 1)
            assert abs(sum(w * x ** p * y ** r for (x, y), w in q) - exact) < 1e-12


def test_projection_reproduces_linear_polynomials():
    rng = random.Random(5)
    for m in range(3, 10):
        pts = random_polygon(rng, m)
        assert polygon_area(pts) > 0
        k, pstar, centre, h = element_matrices(pts)
        for c0, c1, c2 in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (0.3, -2, 1.5)):
            vals = [c0 + c1 * x + c2 * y for x, y in pts]
            coef = scimat.matvec(pstar, vals)
            # the projection is the polynomial itself
            for x, y in pts:
                p = coef[0] + coef[1] * (x - centre[0]) / h + coef[2] * (y - centre[1]) / h
                assert abs(p - (c0 + c1 * x + c2 * y)) < 1e-12
            # consistency: v^T K p is the exact energy of the projections
            v = [rng.uniform(-1, 1) for _ in range(m)]
            gv = scimat.matvec(pstar, v)
            exact = polygon_area(pts) * (gv[1] / h * c1 + gv[2] / h * c2)
            assert abs(scimat.dot(v, scimat.matvec(k, vals)) - exact) < 1e-11


def test_element_matrix_is_symmetric_with_constants_in_the_kernel():
    rng = random.Random(6)
    for m in (3, 5, 8):
        k, _, _, _ = element_matrices(random_polygon(rng, m))
        assert all(abs(k[i][j] - k[j][i]) < 1e-14 for i in range(m) for j in range(m))
        assert all(abs(sum(row)) < 1e-13 for row in k)


def test_triangle_gives_the_linear_finite_element_matrix():
    tri = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    k, _, _, _ = element_matrices(tri, tau=7.0)
    p1 = [[1.0, -0.5, -0.5], [-0.5, 0.5, 0.0], [-0.5, 0.0, 0.5]]
    assert all(abs(k[i][j] - p1[i][j]) < 1e-14 for i in range(3) for j in range(3))


def test_patch_test_on_polygons_with_hanging_nodes():
    pts, polys, bnd = polygon_mesh(6, seed=2, jitter=0.25, midpoint_prob=0.6)
    assert max(len(p) for p in polys) >= 7

    def lin(x, y):
        return 1 + 2 * x - 3 * y

    for tau in (0.1, 1.0, 10.0):
        u, elements = solve_vem(pts, polys, bnd, lambda x, y: 0.0, lin, tau=tau)
        assert max(abs(u[i] - lin(*p)) for i, p in enumerate(pts)) < 1e-11
        e0, e1, _ = errors(pts, polys, u, elements, lin, lambda x, y: (2.0, -3.0))
        assert e0 < 1e-11 and e1 < 1e-10


def test_convergence_on_square_cells():
    errs = []
    for n in (4, 8, 16):
        pts, polys, bnd = polygon_mesh(n)
        u, elements = solve_vem(pts, polys, bnd, f_sin, lambda x, y: 0.0)
        errs.append(errors(pts, polys, u, elements, u_sin, grad_sin))
    r0 = scimat.observed_order([e[0] for e in errs])
    r1 = scimat.observed_order([e[1] for e in errs])
    assert abs(r0[-1] - 2) < 0.05 and abs(r1[-1] - 1) < 0.05


def test_convergence_on_distorted_polygons():
    errs = []
    for n in (4, 8, 16):
        pts, polys, bnd = polygon_mesh(n, seed=3, jitter=0.2, midpoint_prob=0.5)
        u, elements = solve_vem(pts, polys, bnd, f_sin, lambda x, y: 0.0)
        errs.append(errors(pts, polys, u, elements, u_sin, grad_sin))
    r0 = scimat.observed_order([e[0] for e in errs])
    r1 = scimat.observed_order([e[1] for e in errs])
    assert r0[-1] > 1.9 and r1[-1] > 0.9


def test_stabilization_changes_the_answer_but_not_the_accuracy():
    pts, polys, bnd = polygon_mesh(8, seed=1, jitter=0.2, midpoint_prob=0.5)
    results = []
    for tau in (0.25, 1.0, 4.0):
        u, elements = solve_vem(pts, polys, bnd, f_sin, lambda x, y: 0.0, tau=tau)
        results.append((u, errors(pts, polys, u, elements, u_sin, grad_sin)))
    diff = max(abs(a - b) for a, b in zip(results[0][0], results[2][0]))
    assert diff > 1e-4
    assert all(r[1][1] < 0.45 for r in results)


def test_conjugate_gradient_on_a_small_system():
    a = [{0: 4.0, 1: 1.0}, {0: 1.0, 1: 3.0}]
    x = conjugate_gradient(a, [1.0, 2.0])
    assert abs(x[0] - 1 / 11) < 1e-14 and abs(x[1] - 7 / 11) < 1e-14
