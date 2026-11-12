# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semidefinite-embedding/. The authors are listed in prov/6YS5CD.jsonl.

import math
import random

import pytest

from semidefinite_embedding import (
    centered_gram,
    constraint_pairs,
    jacobi_eigh,
    project_psd_centered,
    semidefinite_embedding,
    solve_mvu_sdp,
)


def arc(n=8, seed=1):
    rng = random.Random(seed)
    ts = [math.pi * i / (n - 1) for i in range(n)]
    return [(math.cos(t), math.sin(t), 0.05 * rng.uniform(-1, 1)) for t in ts]


@pytest.fixture(scope="module")
def arc_solution():
    pts = arc()
    pairs = constraint_pairs(pts, 2)
    targets = [math.dist(pts[i], pts[j]) ** 2 for i, j in pairs]
    k, mu = solve_mvu_sdp(len(pts), pairs, targets, centered_gram(pts))
    return pts, pairs, targets, k, mu


def test_bent_path_unfolds_to_a_line():
    # Only |AB| = 1 and |BC| = 1.5 are constrained, so the optimum puts C opposite A:
    # coordinates -7/6, -1/6, 4/3 and trace(K) = 19/6.
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.5)]
    assert constraint_pairs(pts, 1) == [(0, 1), (1, 2)]
    y, lam, k = semidefinite_embedding(pts, 1, 1)
    assert abs(lam[0] - 19 / 6) < 1e-5 and abs(lam[1]) < 1e-5
    sign = 1 if y[2][0] > 0 else -1
    for (v,), ref in zip(y, (-7 / 6, -1 / 6, 4 / 3)):
        assert abs(sign * v - ref) < 1e-5


def test_local_distances_are_preserved(arc_solution):
    pts, pairs, targets, k, _ = arc_solution
    for (i, j), d in zip(pairs, targets):
        assert abs(k[i][i] + k[j][j] - 2 * k[i][j] - d) < 1e-4


def test_result_is_psd_centered_and_unfolds(arc_solution):
    pts, _, _, k, _ = arc_solution
    n = len(pts)
    lam, _, _ = jacobi_eigh(k)
    assert lam[0] > -1e-9
    assert max(abs(sum(row)) for row in k) < 1e-9
    trace_in = sum(centered_gram(pts)[i][i] for i in range(n))
    assert sum(lam) > trace_in + 1.0
    # The arc becomes almost a line: one eigenvalue holds over 99 percent of the trace.
    assert lam[-1] > 0.99 * sum(lam)


def test_dual_certificate(arc_solution):
    # Weak duality: if J (sum_c mu_c A_c - I) J is PSD, then trace(K) <= sum_c mu_c D_c
    # for every feasible K. A small gap shows that K is close to optimal.
    pts, pairs, targets, k, mu = arc_solution
    n = len(pts)
    z = [[-1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for c, (i, j) in enumerate(pairs):
        z[i][i] += mu[c]
        z[j][j] += mu[c]
        z[i][j] -= mu[c]
        z[j][i] -= mu[c]
    rm = [sum(row) / n for row in z]
    tm = sum(rm) / n
    lam, _, _ = jacobi_eigh([[z[i][j] - rm[i] - rm[j] + tm for j in range(n)] for i in range(n)])
    assert lam[0] > -1e-3
    primal = sum(k[i][i] for i in range(n))
    dual = sum(m * d for m, d in zip(mu, targets))
    assert abs(primal - dual) < 1e-3 * primal


def test_projection_keeps_feasible_matrices_and_removes_negative_parts():
    pts = arc(5, seed=2)
    g = centered_gram(pts)
    p, _ = project_psd_centered(g)
    assert max(abs(a - b) for ra, rb in zip(g, p) for a, b in zip(ra, rb)) < 1e-12
    bad = [[1.0, 2.0, 0.0], [2.0, 1.0, 0.0], [0.0, 0.0, -1.0]]
    q, _ = project_psd_centered(bad)
    lam, _, _ = jacobi_eigh(q)
    assert lam[0] > -1e-12
    assert max(abs(sum(row)) for row in q) < 1e-12
