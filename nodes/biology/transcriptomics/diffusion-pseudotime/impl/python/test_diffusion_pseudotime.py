# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-pseudotime/. The authors are listed in prov/0RVW5J.jsonl.

import math
import random

import pytest

from diffusion_pseudotime import (
    accumulated_matrix,
    diffusion_pseudotime,
    dpt_distance,
    spd_inverse,
    transition_matrix,
)
from rq3lin import inverse, jacobi_eigh, matmul


def spearman(a, b):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for k, i in enumerate(order):
            r[i] = k
        return r

    ra, rb = ranks(a), ranks(b)
    n = len(a)
    return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))


def random_cells(rng, n, d=2):
    return [[rng.random() for _ in range(d)] for _ in range(n)]


def test_page_example():
    pts = [(0,), (1,), (2,), (3,), (4,)]
    Ts, psi0 = transition_matrix(pts, 1.0)
    assert math.isclose(Ts[0][1], 0.7038, abs_tol=5e-5)
    assert math.isclose(Ts[1][2], 0.3312, abs_tol=5e-5)
    tau = diffusion_pseudotime(pts, 0, 1.0)
    want = [0.0, 0.5877, 1.0140, 1.9329, 1.9833]
    assert all(math.isclose(a, b, abs_tol=5e-5) for a, b in zip(tau, want))
    assert tau == sorted(tau)


def test_transition_matrix_facts():
    rng = random.Random(1)
    for _ in range(10):
        pts = random_cells(rng, rng.randint(3, 15))
        n = len(pts)
        Ts, psi0 = transition_matrix(pts, 0.3)
        assert all(math.isclose(Ts[i][j], Ts[j][i]) for i in range(n) for j in range(n))
        # psi0 is a unit eigenvector of eigenvalue 1.
        assert math.isclose(sum(v * v for v in psi0), 1.0)
        Tp = [sum(Ts[i][j] * psi0[j] for j in range(n)) for i in range(n)]
        assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(Tp, psi0))
        # The walk T = Z^(-1/2) Ts Z^(1/2) has rows that sum to 1; psi0 is proportional to sqrt(z).
        T = [[Ts[i][j] * psi0[j] / psi0[i] for j in range(n)] for i in range(n)]
        assert all(math.isclose(sum(row), 1.0) for row in T)
        assert all(v >= 0 for row in T for v in row)
        # Every other eigenvalue lies strictly inside (-1, 1).
        vals, _ = jacobi_eigh(Ts)
        assert math.isclose(vals[0], 1.0, abs_tol=1e-10)
        assert all(-1 < v < 1 - 1e-9 for v in vals[1:])


def test_accumulated_matrix_is_the_series():
    rng = random.Random(2)
    for _ in range(5):
        pts = random_cells(rng, 6)
        Ts, psi0 = transition_matrix(pts, 0.5)
        n = len(pts)
        P = [[psi0[i] * psi0[j] for j in range(n)] for i in range(n)]
        B = [[Ts[i][j] - P[i][j] for j in range(n)] for i in range(n)]
        total = [[0.0] * n for _ in range(n)]
        power = [row[:] for row in B]
        for _ in range(3000):
            total = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(total, power)]
            power = matmul(power, B)
            if max(abs(v) for row in power for v in row) < 1e-15:
                break
        M = accumulated_matrix(Ts, psi0)
        assert all(math.isclose(M[i][j], total[i][j], abs_tol=1e-9) for i in range(n) for j in range(n))


def test_eigen_formula():
    rng = random.Random(3)
    for _ in range(5):
        pts = random_cells(rng, 10, 3)
        Ts, psi0 = transition_matrix(pts, 0.4)
        M = accumulated_matrix(Ts, psi0)
        vals, vecs = jacobi_eigh(Ts)
        for a in range(10):
            for b in range(10):
                s = sum((lam / (1 - lam)) ** 2 * (v[a] - v[b]) ** 2 for lam, v in zip(vals[1:], vecs[1:]))
                assert math.isclose(dpt_distance(M, a, b), math.sqrt(s), rel_tol=1e-7, abs_tol=1e-9)


def test_pseudometric_and_invariance():
    rng = random.Random(4)
    pts = random_cells(rng, 12)
    M = accumulated_matrix(*transition_matrix(pts, 0.3))
    D = [[dpt_distance(M, a, b) for b in range(12)] for a in range(12)]
    for a in range(12):
        assert D[a][a] == 0.0
        for b in range(12):
            assert math.isclose(D[a][b], D[b][a])
            for c in range(12):
                assert D[a][c] <= D[a][b] + D[b][c] + 1e-12
    # The same cells in another order, rotated and moved, give the same pseudotimes.
    perm = list(range(12))
    rng.shuffle(perm)
    c, s = math.cos(0.7), math.sin(0.7)
    moved = [[c * pts[i][0] - s * pts[i][1] + 5, s * pts[i][0] + c * pts[i][1] - 2] for i in perm]
    tau = diffusion_pseudotime(pts, 0, 0.3)
    tau2 = diffusion_pseudotime(moved, perm.index(0), 0.3)
    assert all(math.isclose(tau2[j], tau[perm[j]], rel_tol=1e-8, abs_tol=1e-10) for j in range(12))


def test_spd_inverse_matches_general_inverse():
    rng = random.Random(5)
    pts = random_cells(rng, 9)
    Ts, psi0 = transition_matrix(pts, 0.3)
    A = [[(1.0 if i == j else 0.0) - Ts[i][j] + psi0[i] * psi0[j] for j in range(9)] for i in range(9)]
    X, Y = spd_inverse(A), inverse(A)
    assert all(math.isclose(X[i][j], Y[i][j], abs_tol=1e-10) for i in range(9) for j in range(9))


def test_noisy_line_measured():
    """A measurement: 80 cells near a line in 5 dimensions, noise 0.05 per coordinate, sigma 0.2."""
    rng = random.Random(4)
    t = [rng.random() for _ in range(80)]
    pts = [[s * 3 + rng.gauss(0, 0.05), s * 2 + rng.gauss(0, 0.05)] + [rng.gauss(0, 0.05) for _ in range(3)] for s in t]
    root = min(range(80), key=lambda i: t[i])
    assert spearman(diffusion_pseudotime(pts, root, 0.2), t) > 0.99


def test_horseshoe_measured():
    """A measurement: cells on an arc of 1.7 pi, so the two ends are close in space but far along the arc."""
    rng = random.Random(7)
    t = [rng.random() for _ in range(80)]
    pts = [[math.cos(1.7 * math.pi * s) + rng.gauss(0, 0.02), math.sin(1.7 * math.pi * s) + rng.gauss(0, 0.02)] for s in t]
    root = min(range(80), key=lambda i: t[i])
    euclid = [math.dist(pts[root], p) for p in pts]
    assert spearman(diffusion_pseudotime(pts, root, 0.2), t) > 0.99
    assert spearman(euclid, t) < 0.7


def test_errors():
    with pytest.raises(ValueError):
        transition_matrix([(0,), (1,)], 1.0)
    with pytest.raises(ValueError):
        transition_matrix([(0,), (1,), (2,)], 0.0)
    with pytest.raises(ValueError):
        transition_matrix([(0,), (1,), (1000,)], 0.01)
    with pytest.raises(ValueError):
        diffusion_pseudotime([(0,), (1,), (2,)], 3, 1.0)
