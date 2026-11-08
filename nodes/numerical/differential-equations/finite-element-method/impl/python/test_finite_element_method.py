# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-element-method/. The authors are listed in prov/PAMZX2.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from finite_element_method import (assemble, element_load, element_stiffness,
                                   solve_poisson, structured_mesh)


def cot_stiffness(p):
    """Independent formula: K_ij = -cot(angle opposite edge ij)/2, rows sum to zero."""
    def cot_at(k):
        o, a, b = p[k], p[(k + 1) % 3], p[(k + 2) % 3]
        u = (a[0] - o[0], a[1] - o[1])
        v = (b[0] - o[0], b[1] - o[1])
        return (u[0] * v[0] + u[1] * v[1]) / abs(u[0] * v[1] - u[1] * v[0])
    K = [[0.0] * 3 for _ in range(3)]
    for k in range(3):
        i, j = (k + 1) % 3, (k + 2) % 3
        K[i][j] = K[j][i] = -cot_at(k) / 2
    for i in range(3):
        K[i][i] = -sum(K[i][j] for j in range(3) if j != i)
    return K


def jittered_mesh(rng, nx, ny, amount):
    nodes, tris, boundary = structured_mesh(nx, ny)
    hx, hy = 1.0 / nx, 1.0 / ny
    out = []
    for v, (x, y) in enumerate(nodes):
        if v not in boundary:
            x += rng.uniform(-amount, amount) * hx
            y += rng.uniform(-amount, amount) * hy
        out.append((x, y))
    return out, tris, boundary


def test_reference_element_exact():
    K, area = element_stiffness((Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1)))
    assert area == Fr(1, 2)
    assert K == [[1, Fr(-1, 2), Fr(-1, 2)], [Fr(-1, 2), Fr(1, 2), 0], [Fr(-1, 2), 0, Fr(1, 2)]]
    # orientation does not matter
    K2, _ = element_stiffness((Fr(0), Fr(0)), (Fr(0), Fr(1)), (Fr(1), Fr(0)))
    assert K2 == [[1, Fr(-1, 2), Fr(-1, 2)], [Fr(-1, 2), Fr(1, 2), 0], [Fr(-1, 2), 0, Fr(1, 2)]]


def test_worked_example_one_interior_node():
    nodes, tris, boundary = structured_mesh(2, 2, Fr(0), Fr(1), Fr(0), Fr(1))
    r = solve_poisson(nodes, tris, boundary, lambda x, y: 1, lambda x, y: 0, solver="direct")
    assert r.u[4] == Fr(1, 16) and r.unknowns == 1
    K, F = assemble(nodes, tris, lambda x, y: 1)
    assert K[4] == {0: 0, 1: -1, 3: -1, 4: 4, 5: -1, 7: -1, 8: 0}
    assert F[4] == Fr(1, 4)


def test_random_elements_against_cotangent_formula():
    rng = random.Random(7)
    for _ in range(600):
        p = [(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(3)]
        det = (p[1][0] - p[0][0]) * (p[2][1] - p[0][1]) - (p[2][0] - p[0][0]) * (p[1][1] - p[0][1])
        if abs(det) < 1e-3:
            continue
        K, area = element_stiffness(*p)
        assert area == pytest.approx(abs(det) / 2)
        C = cot_stiffness(p)
        for i in range(3):
            assert sum(K[i]) == pytest.approx(0.0, abs=1e-9)
            for j in range(3):
                assert K[i][j] == pytest.approx(C[i][j], rel=1e-9, abs=1e-9)
                assert K[i][j] == K[j][i]
        # load of f = 1 is area/3 per vertex; of f = x is exact as well
        assert element_load(p[0], p[1], p[2], lambda x, y: 1.0, area) == pytest.approx([area / 3] * 3)
        cx = sum(q[0] for q in p)
        want = [area / 12 * (cx + p[i][0]) for i in range(3)]
        assert element_load(p[0], p[1], p[2], lambda x, y: x, area) == pytest.approx(want)


def test_patch_test_random_meshes_exact_fractions():
    rng = random.Random(11)
    for _ in range(120):
        nx, ny = rng.randint(1, 3), rng.randint(1, 3)
        nodes, tris, boundary = structured_mesh(nx, ny, Fr(0), Fr(1), Fr(0), Fr(1))
        nodes = [(x + (Fr(rng.randint(-3, 3), 16 * nx) if v not in boundary else 0),
                  y + (Fr(rng.randint(-3, 3), 16 * ny) if v not in boundary else 0))
                 for v, (x, y) in enumerate(nodes)]
        a, b, c = (Fr(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(3))
        r = solve_poisson(nodes, tris, boundary, lambda x, y: 0, lambda x, y: a + b * x + c * y,
                          solver="direct")
        assert all(r.u[v] == a + b * x + c * y for v, (x, y) in enumerate(nodes))


def test_patch_test_random_meshes_float_cg():
    rng = random.Random(12)
    for _ in range(400):
        nodes, tris, boundary = jittered_mesh(rng, rng.randint(1, 5), rng.randint(1, 5), 0.3)
        a, b, c = rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-3, 3)
        r = solve_poisson(nodes, tris, boundary, lambda x, y: 0.0, lambda x, y: a + b * x + c * y)
        assert max(abs(r.u[v] - (a + b * x + c * y)) for v, (x, y) in enumerate(nodes)) < 1e-9


def test_convergence_second_order_at_nodes():
    f = lambda x, y: 2 * math.pi ** 2 * math.sin(math.pi * x) * math.sin(math.pi * y)
    errs, energy = [], []
    for m in (4, 8, 16, 32):
        nodes, tris, boundary = structured_mesh(m, m)
        r = solve_poisson(nodes, tris, boundary, f, lambda x, y: 0.0)
        errs.append(max(abs(r.u[k] - math.sin(math.pi * x) * math.sin(math.pi * y))
                        for k, (x, y) in enumerate(nodes)))
        K, _ = assemble(nodes, tris, f)
        q = sum(r.u[i] * v * r.u[j] for i, row in enumerate(K) for j, v in row.items())
        energy.append(math.sqrt(math.pi ** 2 / 2 - q))
    assert errs[0] == pytest.approx(5.181e-2, rel=1e-3)
    for k in range(3):
        assert 3.8 < errs[k] / errs[k + 1] < 4.2
        assert 1.9 < energy[k] / energy[k + 1] < 2.1


def test_edge_cases():
    # one cell: every node is on the boundary, nothing to solve
    nodes, tris, boundary = structured_mesh(1, 1)
    r = solve_poisson(nodes, tris, boundary, lambda x, y: 5.0, lambda x, y: x * y)
    assert r.unknowns == 0 and r.u == [0.0, 0.0, 0.0, 1.0]
    with pytest.raises(ValueError):
        element_stiffness((0, 0), (1, 1), (2, 2))
    with pytest.raises(ValueError):
        structured_mesh(0, 3)
    with pytest.raises(ValueError):
        solve_poisson(*structured_mesh(2, 2), lambda x, y: 1.0, lambda x, y: 0.0, solver="lu")
    # anisotropic rectangle, quadratic solution u = x(1 - x): nodal values are exact in 1D-like data
    nodes, tris, boundary = structured_mesh(6, 2, 0.0, 1.0, 0.0, 3.0)
    r = solve_poisson(nodes, tris, boundary, lambda x, y: 2.0, lambda x, y: x * (1 - x))
    assert all(abs(r.u[v] - x * (1 - x)) < 1e-12 for v, (x, y) in enumerate(nodes))
