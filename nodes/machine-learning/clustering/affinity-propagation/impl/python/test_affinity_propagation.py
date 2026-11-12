# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affinity-propagation/. The authors are listed in prov/6S8D6H.jsonl.

import random

import pytest

from affinity_propagation import (
    affinity_propagation,
    availabilities,
    availabilities_naive,
    best_exemplar_set,
    decode,
    is_valid,
    net_similarity,
    responsibilities,
    responsibilities_naive,
    squared_distance_similarity,
)


def close(X, Y, eps=1e-9):
    return all(abs(x - y) <= eps for rx, ry in zip(X, Y) for x, y in zip(rx, ry))


def random_points(rng, n, centers=3):
    cs = [(rng.uniform(-10, 10), rng.uniform(-10, 10)) for _ in range(centers)]
    pts = []
    for i in range(n):
        cx, cy = cs[i % centers]
        pts.append((cx + rng.gauss(0, 1), cy + rng.gauss(0, 1)))
    return pts


def test_fast_updates_equal_the_rules_as_written():
    rng = random.Random(1)
    for _ in range(20):
        n = rng.randint(2, 9)
        S = [[rng.uniform(-5, 0) for _ in range(n)] for _ in range(n)]
        A = [[rng.uniform(-3, 3) for _ in range(n)] for _ in range(n)]
        R = responsibilities(S, A)
        assert close(R, responsibilities_naive(S, A))
        assert close(availabilities(R), availabilities_naive(R))


def test_fixed_point_equations_hold_at_convergence():
    rng = random.Random(2)
    done = 0
    for trial in range(12):
        pts = random_points(rng, rng.randint(6, 14))
        S = squared_distance_similarity(pts)
        ex, labels, R, A, it, conv = affinity_propagation(
            S, damping=0.9, max_iter=4000, tol=1e-10, rng=random.Random(trial))
        if not conv:
            continue
        done += 1
        # with damping, a fixed point m = lam m + (1 - lam) f(m) means m = f(m)
        Sn = S  # the noise is below 1e-9 relative, far under the tolerance below
        assert close(R, responsibilities(Sn, A), 1e-6)
        assert close(A, availabilities(R), 1e-6)
        # the decoded clustering is valid and is a feasible exemplar set
        assert is_valid(labels)
        assert ex == sorted(set(labels))
        assert net_similarity(S, labels) <= best_exemplar_set(S)[0] + 1e-6 if len(S) <= 12 else True
    assert done >= 8


def test_availability_signs():
    rng = random.Random(3)
    n = 7
    R = [[rng.uniform(-4, 4) for _ in range(n)] for _ in range(n)]
    A = availabilities(R)
    for i in range(n):
        for k in range(n):
            if i == k:
                assert A[k][k] >= 0
            else:
                assert A[i][k] <= 0


def test_worked_example():
    S = squared_distance_similarity([[0], [1], [5], [6]])
    assert S[0][0] == -20.5
    A0 = [[0.0] * 4 for _ in range(4)]
    assert responsibilities(S, A0)[0] == [-19.5, 19.5, -24.0, -35.0]
    ex, labels, R, A, it, conv = affinity_propagation(S, tol=1e-12)
    assert conv and ex == [1, 2] and labels == [1, 1, 2, 2]
    assert net_similarity(S, labels) == -43.0 == best_exemplar_set(S)[0]
    assert close(R, [[-9.75, 10.5, -14.25, -25.25], [9.0, -9.75, -6.0, -15.0],
                     [-15.0, -6.0, -9.75, 9.0], [-25.25, -14.25, 10.5, -9.75]], 1e-6)


def test_preference_controls_the_number_of_exemplars():
    pts = [[0], [1], [2], [10], [11], [13], [20], [21]]
    counts = []
    for pref in (-200, None, -0.5):
        S = squared_distance_similarity(pts, pref)
        ex, labels, R, A, it, conv = affinity_propagation(S, tol=1e-12, max_iter=3000)
        assert conv and is_valid(labels)
        assert net_similarity(S, labels) == best_exemplar_set(S)[0]
        counts.append(len(ex))
    assert counts == [2, 3, 8]


def test_no_optimality_guarantee():
    # a converged, non-degenerate run that misses the optimum, for each damping
    S = squared_distance_similarity([[4], [8], [9], [11], [17]], -80)
    assert best_exemplar_set(S) == (-174, [2, 2, 2, 2, 2])
    for damping in (0.5, 0.7, 0.9):
        ex, labels, R, A, it, conv = affinity_propagation(
            S, damping=damping, tol=1e-10, max_iter=5000, rng=random.Random(1))
        assert conv and ex == [3] and labels == [3] * 5
        assert net_similarity(S, labels) == -178
        assert close(R, responsibilities(S, A), 1e-6) and close(A, availabilities(R), 1e-6)
        assert min(abs(A[k][k] + R[k][k]) for k in range(5)) > 30


def test_exact_ties_need_noise():
    # symmetric data: at the fixed point some a(k, k) + r(k, k) are exactly 0
    pts = [[0], [1], [2], [10], [11], [13], [20], [21]]
    S = squared_distance_similarity(pts, -2)
    ex, labels, R, A, it, conv = affinity_propagation(S, tol=1e-12, max_iter=3000)
    assert conv and ex == [1, 5]
    assert sum(1 for k in range(8) if A[k][k] + R[k][k] == 0) == 4
    assert net_similarity(S, labels) == -132
    ex, labels, R, A, it, conv = affinity_propagation(S, max_iter=3000, rng=random.Random(1))
    assert is_valid(labels) and net_similarity(S, labels) == best_exemplar_set(S)[0] == -12


def test_decode_with_no_exemplar_and_bad_damping():
    S = [[-1.0, -2.0], [-2.0, -1.0]]
    Z = [[0.0, 0.0], [0.0, 0.0]]
    assert decode(S, Z, Z) == ([], [-1, -1])
    with pytest.raises(ValueError):
        affinity_propagation(S, damping=0.2)
