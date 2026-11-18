# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modal-reduction/. The authors are listed in prov/CSEPNJ.jsonl.
"""Tests of linear modal reduction on a small grid mesh.

The stiffness is checked against the gradient of the linear energy, the
eigenpairs against the residual, M-orthonormality and the trace identities,
and the modal simulation against the full simulation of the same linear
system. A free body has exactly the three rigid modes. A large rotation
mode changes the area and the St. Venant-Kirchhoff energy, which the linear
modes do not see.
"""

import math
import random

from anim import num_grad
from modal_reduction import (
    generalized_eigen,
    jacobi_eigen,
    lame,
    mesh_area,
    modal_basis,
    project,
    reconstruct,
    setup,
    simulate_full,
    simulate_modal,
    stvk_energy,
)

MU, LAM = lame(1.0, 0.3)


def matvec(a, x):
    return [sum(r[j] * x[j] for j in range(len(x))) for r in a]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def test_lame_values():
    assert abs(MU - 0.384615) < 1e-6
    assert abs(LAM - 0.576923) < 1e-6


def test_stiffness_is_hessian_of_linear_energy():
    nodes, tris, k, m, free = setup(4, 3, 1.5, 1.0, 1.0, 0.3, 1.0, False)
    n = len(k)
    assert all(abs(k[i][j] - k[j][i]) < 1e-12 for i in range(n) for j in range(n))
    rng = random.Random(1)
    u = [rng.uniform(-1, 1) for _ in range(n)]

    def energy(x):
        return 0.5 * dot(x, matvec(k, x))

    # the quadratic energy 1/2 u^T K u equals the linear elastic energy of the mesh
    def lin_energy(x):
        total = 0.0
        for t in tris:
            p = [nodes[v] for v in t]
            dm = [[p[1][0] - p[0][0], p[2][0] - p[0][0]], [p[1][1] - p[0][1], p[2][1] - p[0][1]]]
            a = (dm[0][0] * dm[1][1] - dm[0][1] * dm[1][0]) / 2.0
            ia = [[dm[1][1] / (2 * a), -dm[0][1] / (2 * a)], [-dm[1][0] / (2 * a), dm[0][0] / (2 * a)]]
            ds = [[x[2 * t[1]] - x[2 * t[0]], x[2 * t[2]] - x[2 * t[0]]], [x[2 * t[1] + 1] - x[2 * t[0] + 1], x[2 * t[2] + 1] - x[2 * t[0] + 1]]]
            h = [[sum(ds[i][c] * ia[c][j] for c in range(2)) for j in range(2)] for i in range(2)]
            e = [[0.5 * (h[i][j] + h[j][i]) for j in range(2)] for i in range(2)]
            tr = e[0][0] + e[1][1]
            total += a * (MU * sum(v * v for row in e for v in row) + 0.5 * LAM * tr * tr)
        return total

    assert abs(energy(u) - lin_energy(u)) < 1e-12
    g = num_grad(lin_energy, u)
    assert max(abs(a - b) for a, b in zip(g, matvec(k, u))) < 1e-6


def test_jacobi_against_trace_and_residual():
    rng = random.Random(2)
    n = 7
    b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    a = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
    vals, vecs = jacobi_eigen(a)
    assert abs(sum(vals) - sum(a[i][i] for i in range(n))) < 1e-12
    assert abs(sum(v * v for v in vals) - sum(x * x for row in a for x in row)) < 1e-10
    for lam, v in zip(vals, vecs):
        av = matvec(a, v)
        assert max(abs(av[i] - lam * v[i]) for i in range(n)) < 1e-10
        assert abs(dot(v, v) - 1.0) < 1e-12


def test_generalized_eigenpairs():
    for fix in (False, True):
        nodes, tris, k, m, free = setup(5, 3, 2.0, 1.0, 1.0, 0.3, 1.0, fix)
        n = len(k)
        lams, phis = generalized_eigen(k, m)
        assert lams == sorted(lams)
        for lam, phi in zip(lams, phis):
            kp = matvec(k, phi)
            assert max(abs(kp[i] - lam * m[i] * phi[i]) for i in range(n)) < 1e-9
        for a in range(n):
            for b in range(a, n):
                mab = sum(phis[a][i] * m[i] * phis[b][i] for i in range(n))
                assert abs(mab - (1.0 if a == b else 0.0)) < 1e-10
        minv_k = [[k[i][j] / m[i] for j in range(n)] for i in range(n)]
        tr1 = sum(minv_k[i][i] for i in range(n))
        tr2 = sum(minv_k[i][j] * minv_k[j][i] for i in range(n) for j in range(n))
        assert abs(sum(lams) - tr1) < 1e-9 * tr1
        assert abs(sum(x * x for x in lams) - tr2) < 1e-9 * tr2


def test_free_body_has_three_rigid_modes():
    nodes, tris, k, m, free = setup(5, 3, 2.0, 1.0, 1.0, 0.3, 1.0, False)
    lams, phis = generalized_eigen(k, m)
    assert all(abs(x) < 1e-10 for x in lams[:3])
    assert lams[3] > 1.0
    # the zero modes span the translations and the linearized rotation (-y, x)
    rigid = [[1.0, 0.0] * len(nodes), [0.0, 1.0] * len(nodes), [c for p in nodes for c in (-p[1], p[0])]]
    for w in rigid:
        coef = [sum(phi[i] * m[i] * w[i] for i in range(len(w))) for phi in phis[:3]]
        back = reconstruct(phis[:3], coef)
        assert max(abs(a - b) for a, b in zip(back, w)) < 1e-9
    _, _, kf, mf, _ = setup(5, 3, 2.0, 1.0, 1.0, 0.3, 1.0, True)
    assert min(generalized_eigen(kf, mf)[0]) > 0.05


def test_full_basis_matches_full_simulation():
    nodes, tris, k, m, free = setup(5, 3, 2.0, 1.0, 1.0, 0.3, 1.0, True)
    n = len(k)
    rng = random.Random(3)
    f = [rng.uniform(-0.1, 0.1) for _ in range(n)]
    u0 = [rng.uniform(-0.05, 0.05) for _ in range(n)]
    v0 = [rng.uniform(-0.05, 0.05) for _ in range(n)]
    om2, modes = modal_basis(k, m, n)
    mu0 = [m[i] * u0[i] for i in range(n)]
    mv0 = [m[i] * v0[i] for i in range(n)]
    h, steps = 0.05, 200
    shapes, _ = simulate_modal(modes, om2, f, h, steps, project(modes, mu0), project(modes, mv0))
    full = simulate_full(k, m, f, h, steps, u0, v0)
    assert max(abs(a - b) for s, t in zip(shapes, full) for a, b in zip(s, t)) < 1e-9
    assert max(abs(x) for x in full[-1]) > 1e-2


def test_truncated_basis_keeps_its_modes_exactly():
    nodes, tris, k, m, free = setup(5, 3, 2.0, 1.0, 1.0, 0.3, 1.0, True)
    n = len(k)
    om2, modes = modal_basis(k, m, n)
    rng = random.Random(4)
    f = [rng.uniform(-0.1, 0.1) for _ in range(n)]
    h, steps, r = 0.05, 120, 6
    full = simulate_full(k, m, f, h, steps)
    shapes, q = simulate_modal(modes[:r], om2[:r], f, h, steps)
    q_full = project(modes[:r], [m[i] * full[-1][i] for i in range(n)])
    assert max(abs(a - b) for a, b in zip(q, q_full)) < 1e-9
    # the error is the part of the full shape in the dropped modes
    q_rest = project(modes[r:], [m[i] * full[-1][i] for i in range(n)])
    rest = reconstruct(modes[r:], q_rest)
    err = [a - b for a, b in zip(full[-1], shapes[-1])]
    assert max(abs(a - b) for a, b in zip(err, rest)) < 1e-9
    assert max(abs(x) for x in err) > 1e-6


def test_static_load_converges_with_more_modes():
    nodes, tris, k, m, free = setup(5, 3, 2.0, 1.0, 1.0, 0.3, 1.0, True)
    n = len(k)
    om2, modes = modal_basis(k, m, n)
    f = [0.0 if i % 2 == 0 else -0.01 * m[i] for i in range(n)]
    g = project(modes, f)
    exact = reconstruct(modes, [g[i] / om2[i] for i in range(n)])
    ku = matvec(k, exact)
    assert max(abs(a - b) for a, b in zip(ku, f)) < 1e-12
    errs = []
    for r in (1, 3, 6, 12, n):
        approx = reconstruct(modes[:r], [g[i] / om2[i] for i in range(r)])
        errs.append(math.sqrt(sum(m[i] * (approx[i] - exact[i]) ** 2 for i in range(n))))
    assert all(errs[i + 1] <= errs[i] + 1e-15 for i in range(len(errs) - 1))
    assert errs[-1] < 1e-12 and errs[0] > 0.0


def test_large_rotation_mode_is_not_rigid():
    nodes, tris, k, m, free = setup(5, 3, 2.0, 1.0, 1.0, 0.3, 1.0, False)
    area = 2.0
    rot = [c for p in nodes for c in (-p[1], p[0])]
    for theta in (0.1, 0.5, 1.0):
        u = [theta * x for x in rot]
        assert abs(0.5 * dot(u, matvec(k, u))) < 1e-10
        assert abs(mesh_area(nodes, tris, u) - area * (1.0 + theta * theta)) < 1e-12
        e = stvk_energy(nodes, tris, u, MU, LAM)
        assert abs(e - area * (MU + LAM) * theta ** 4 / 2.0) < 1e-12
