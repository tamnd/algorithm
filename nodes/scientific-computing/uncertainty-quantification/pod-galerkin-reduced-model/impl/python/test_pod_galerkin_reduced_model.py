# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pod-galerkin-reduced-model/. The authors are listed in prov/9GPP7P.jsonl.
import math
import random

import pytest

from pod_galerkin_reduced_model import backward_euler, heat_matrix, jacobi_eigen, pod_basis, pod_galerkin
from scimat import matmul, matvec, norm2, scale, transpose


def diff(x, y):
    return [a - b for a, b in zip(x, y)]


def proj_error(states, v):
    vt = transpose(v)
    return sum(norm2(diff(x, matvec(v, matvec(vt, x)))) ** 2 for x in states)


def heat_example():
    n, dt, steps = 60, 0.002, 20
    grid = [(j + 1) / (n + 1) for j in range(n)]
    x0 = [1.0 if 0.2 <= x <= 0.4 else 0.0 for x in grid]
    f = [1.0] * n
    a = heat_matrix(n)
    return a, f, x0, dt, steps, backward_euler(a, f, x0, dt, steps)


def test_hand_example():
    s = [[1, 1], [1, 1], [1, -1]]  # snapshots (1, 1, 1) and (1, 1, -1)
    v, lam = pod_basis(s, 2)
    assert lam[0] == pytest.approx(4.0) and lam[1] == pytest.approx(2.0)
    v1 = [row[0] for row in v]
    v2 = [row[1] for row in v]
    sgn = 1.0 if v1[0] > 0 else -1.0
    assert [sgn * x for x in v1] == pytest.approx([1 / math.sqrt(2), 1 / math.sqrt(2), 0.0], abs=1e-12)
    assert [abs(x) for x in v2] == pytest.approx([0.0, 0.0, 1.0], abs=1e-12)
    a = heat_matrix(3)
    assert sum(v1[i] * matvec(a, v1)[i] for i in range(3)) == pytest.approx(-16.0)
    assert proj_error([[1, 1, 1], [1, 1, -1]], [[x] for x in v1]) == pytest.approx(2.0)


def test_jacobi_against_definition():
    rng = random.Random(7)
    m = 7
    b = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(m)]
    c = matmul(transpose(b), b)
    lam, w = jacobi_eigen(c)
    assert all(lam[i] >= lam[i + 1] for i in range(m - 1))
    for i in range(m):
        assert norm2(diff(matvec(c, w[i]), scale(lam[i], w[i]))) < 1e-10
        for j in range(m):
            assert sum(x * y for x, y in zip(w[i], w[j])) == pytest.approx(1.0 if i == j else 0.0, abs=1e-12)
    assert sum(lam) == pytest.approx(sum(c[i][i] for i in range(m)))


def test_projection_error_is_sum_of_discarded_eigenvalues():
    a, f, x0, dt, steps, full = heat_example()
    s = transpose(full)
    for r in range(1, 7):
        v, lam = pod_basis(s, r)
        vt = transpose(v)
        g = matmul(vt, v)
        for i in range(r):
            for j in range(r):
                assert g[i][j] == pytest.approx(1.0 if i == j else 0.0, abs=1e-9)
        assert proj_error(full, v) == pytest.approx(sum(lam[r:]), rel=1e-8, abs=1e-12)


def test_error_falls_as_r_grows_and_obeys_the_bound():
    a, f, x0, dt, steps, full = heat_example()
    s = transpose(full)
    errs = []
    for r in range(1, 8):
        rom, v, lam = pod_galerkin(a, f, x0, dt, steps, s, r)
        errs.append(max(norm2(diff(x, y)) for x, y in zip(full, rom)))
        # ||V^T x_K - z_K|| <= dt sum_k ||A rho_k|| with rho_k = x_k - V V^T x_k
        vt = transpose(v)
        theta = norm2(diff(matvec(vt, full[-1]), matvec(vt, rom[-1])))
        rho = [diff(x, matvec(v, matvec(vt, x))) for x in full]
        assert theta <= dt * sum(norm2(matvec(a, rk)) for rk in rho[1:]) * (1 + 1e-9) + 1e-12
    assert all(errs[i + 1] < errs[i] for i in range(len(errs) - 1))
    assert errs[0] == pytest.approx(1.8074, rel=1e-3)
    assert errs[-1] < 1e-3 * errs[0]


def test_exact_on_a_rank_two_trajectory():
    n, dt, steps = 12, 0.01, 15
    grid = [(j + 1) / (n + 1) for j in range(n)]
    x0 = [math.sin(math.pi * x) for x in grid]
    f = [3.0 * math.sin(2 * math.pi * x) for x in grid]
    a = heat_matrix(n)
    full = backward_euler(a, f, x0, dt, steps)
    rom, v, lam = pod_galerkin(a, f, x0, dt, steps, transpose(full), 2)
    assert lam[2] < 1e-12 * lam[0]
    assert max(norm2(diff(x, y)) for x, y in zip(full, rom)) < 1e-10
    with pytest.raises(ValueError):
        pod_basis(transpose(full), 3)


def test_random_snapshots_against_direct_projection():
    rng = random.Random(2025)
    for _ in range(5):
        n = rng.randint(5, 9)
        m = rng.randint(2, 5)  # m <= n, so S has rank m
        s = [[rng.gauss(0, 1) for _ in range(m)] for _ in range(n)]
        states = transpose(s)
        for r in range(1, m + 1):
            v, lam = pod_basis(s, r)
            assert proj_error(states, v) == pytest.approx(sum(lam[r:]), rel=1e-9, abs=1e-10)
        # a basis from a random orthonormal set never beats POD (Schmidt-Eckart-Young)
        q = [[rng.gauss(0, 1)] for _ in range(n)]
        nq = norm2([row[0] for row in q])
        q = [[row[0] / nq] for row in q]
        assert proj_error(states, q) >= sum(lam[1:]) - 1e-10


def test_bad_rank_is_rejected():
    s = [[1.0, 2.0], [2.0, 4.0]]  # rank one
    with pytest.raises(ValueError):
        pod_basis(s, 0)
    with pytest.raises(ValueError):
        pod_basis(s, 2)
