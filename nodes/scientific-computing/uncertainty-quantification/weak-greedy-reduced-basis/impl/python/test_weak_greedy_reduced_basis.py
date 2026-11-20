# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-greedy-reduced-basis/. The authors are listed in prov/3WNNGB.jsonl.
import math
import random

import pytest

from scimat import dot, matvec, solve
from weak_greedy_reduced_basis import ReducedBasis, combine, fe_model, tridiag_solve, weak_greedy

N = 99
MU_BAR = 10.0
AQ, F = fe_model(N)
X = combine(AQ, [1.0, MU_BAR])
TRAIN = [10 ** (i / 20) for i in range(41)]  # 41 points, log-spaced in [1, 100]


def x_norm(v):
    return math.sqrt(dot(v, matvec(X, v)))


def dist_to_basis(rb, u):
    """X-distance of u to the span of the X-orthonormal basis."""
    w = list(u)
    for z in rb.z:
        c = dot(z, matvec(X, w))
        w = [wi - c * zi for wi, zi in zip(w, z)]
    return x_norm(w)


def test_tridiagonal_solver_against_dense():
    rng = random.Random(5)
    a = combine(AQ, [1.0, 7.0])
    b = [rng.gauss(0, 1) for _ in range(N)]
    assert tridiag_solve(a, b) == pytest.approx(solve(a, b), rel=1e-9, abs=1e-12)


def test_strong_greedy_hand_example():
    # the strong greedy step with the true distance, on three vectors in R^3
    vecs = [(2.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 1.0, 0.5)]
    basis, sigmas = [], []
    for _ in range(3):
        d = []
        for v in vecs:
            w = list(v)
            for b in basis:
                c = sum(x * y for x, y in zip(b, w))
                w = [x - c * y for x, y in zip(w, b)]
            d.append(math.sqrt(sum(x * x for x in w)))
        k = max(range(3), key=lambda i: d[i])
        sigmas.append(d[k])
        w = list(vecs[k])
        for b in basis:
            c = sum(x * y for x, y in zip(b, w))
            w = [x - c * y for x, y in zip(w, b)]
        basis.append([x / d[k] for x in w])
    assert sigmas == pytest.approx([2.0, math.sqrt(1.25), math.sqrt(0.2)])


def test_example_run():
    rb, chosen, eps = weak_greedy(AQ, F, X, MU_BAR, TRAIN, 1e-6, 20)
    assert chosen == pytest.approx([1.0, 100.0, 10 ** 0.6, 10 ** 1.65, 10 ** 1.85])
    assert eps[0] == pytest.approx(2.047, rel=1e-3)
    assert eps[-1] <= 1e-6 < eps[-2]
    assert all(eps[i + 1] < eps[i] for i in range(len(eps) - 1))
    # at termination the true error on the training set is below the tolerance
    for mu in TRAIN:
        c, d = rb.online(mu)
        err = x_norm([a - b for a, b in zip(rb.truth(mu), rb.lift(c))])
        assert err <= d * (1 + 1e-9) + 1e-12 <= 1e-6 + 1e-12


def test_weak_greedy_property():
    # dist(u(mu_(j+1)), X_j) >= max over train of dist(u(mu), X_j) / kappa, kappa = max (gamma / alpha_LB)^2 = 100
    truths = [ReducedBasis(AQ, F, X, MU_BAR).truth(mu) for mu in TRAIN]
    rb, chosen, eps = weak_greedy(AQ, F, X, MU_BAR, TRAIN, 1e-6, 20)
    partial = ReducedBasis(AQ, F, X, MU_BAR)
    for mu in chosen:
        best = max(dist_to_basis(partial, u) for u in truths)
        picked = dist_to_basis(partial, partial.truth(mu))
        assert picked >= best / 100.0
        partial.add(partial.truth(mu))


def test_termination_on_a_small_training_set():
    rng = random.Random(9)
    for _ in range(3):
        train = sorted(rng.uniform(1.0, 100.0) for _ in range(3))
        rb, chosen, eps = weak_greedy(AQ, F, X, MU_BAR, train, 1e-6, 50)
        assert len(chosen) <= len(train)
        assert len(set(chosen)) == len(chosen)
        assert eps[-1] <= 1e-6


def test_r_max_stops_the_loop():
    rb, chosen, eps = weak_greedy(AQ, F, X, MU_BAR, TRAIN, 0.0, 2)
    assert len(chosen) == 2 and len(eps) == 3
