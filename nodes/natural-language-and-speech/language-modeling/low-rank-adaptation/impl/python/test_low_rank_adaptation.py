# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/low-rank-adaptation/. The authors are listed in prov/W05XMM.jsonl.

import math
import random
from fractions import Fraction

import pytest

from low_rank_adaptation import (backward, backward_batch, delta, forward, forward_batch, init, matmul,
                                 matvec, merge, sgd_step, squared_loss, trainable_parameters, unmerge)


def rand_matrix(rng, rows, cols, scale=1.0):
    return [[rng.gauss(0.0, scale) for _ in range(cols)] for _ in range(rows)]


def rand_vector(rng, n, scale=1.0):
    return [rng.gauss(0.0, scale) for _ in range(n)]


def close(u, v, tol):
    return all(abs(a - b) <= tol for a, b in zip(u, v))


def exact_rank(M):
    """Rank of a matrix of integers by Gaussian elimination in Fraction."""
    R = [[Fraction(v) for v in row] for row in M]
    rows, cols = len(R), len(R[0])
    rank, col = 0, 0
    while rank < rows and col < cols:
        piv = next((i for i in range(rank, rows) if R[i][col] != 0), None)
        if piv is None:
            col += 1
            continue
        R[rank], R[piv] = R[piv], R[rank]
        for i in range(rows):
            if i != rank and R[i][col] != 0:
                f = R[i][col] / R[rank][col]
                R[i] = [R[i][j] - f * R[rank][j] for j in range(cols)]
        rank += 1
        col += 1
    return rank


# A worked example of the page: d = 2, k = 3, r = 1, alpha = 2, so s = 2.
W0_EX = [[1.0, 0.0, 2.0], [0.0, 1.0, -1.0]]
A_EX = [[1.0, 2.0, 0.0]]
B_EX = [[0.5], [-1.0]]
X_EX = [1.0, 1.0, 1.0]


def test_worked_example():
    h = forward(W0_EX, A_EX, B_EX, 2.0, X_EX)
    assert h == pytest.approx([6.0, -6.0], abs=1e-12)
    W = merge(W0_EX, A_EX, B_EX, 2.0)
    assert W == [[2.0, 2.0, 2.0], [-2.0, -3.0, -1.0]]
    assert matvec(W, X_EX) == pytest.approx(h, abs=1e-12)


def test_at_init_the_output_is_the_pretrained_output():
    rng = random.Random(1)
    d, k, r = 5, 4, 2
    W0 = rand_matrix(rng, d, k)
    A, B = init(d, k, r, rng, sigma=0.5)
    for _ in range(5):
        x = rand_vector(rng, k)
        assert forward(W0, A, B, 16.0, x) == pytest.approx(matvec(W0, x), abs=1e-15)


def test_at_init_only_B_gets_a_gradient():
    rng = random.Random(2)
    d, k, r = 5, 4, 3
    W0 = rand_matrix(rng, d, k)
    A, B = init(d, k, r, rng, sigma=0.5)
    x, g = rand_vector(rng, k), rand_vector(rng, d)
    gA, gB, _ = backward(W0, A, B, 3.0, x, g)
    assert all(v == 0.0 for row in gA for v in row)
    assert any(abs(v) > 1e-6 for row in gB for v in row)


def test_zero_A_and_zero_B_is_stuck():
    rng = random.Random(3)
    d, k, r = 4, 3, 2
    W0 = rand_matrix(rng, d, k)
    A = [[0.0] * k for _ in range(r)]
    B = [[0.0] * r for _ in range(d)]
    gA, gB, _ = backward(W0, A, B, 1.0, rand_vector(rng, k), rand_vector(rng, d))
    assert all(v == 0.0 for row in gA + gB for v in row)


def test_rank_r_matches_the_full_update_of_the_same_product():
    rng = random.Random(4)
    for d, k, r in [(6, 5, 1), (6, 5, 2), (4, 7, 3), (8, 8, 8)]:
        W0 = rand_matrix(rng, d, k)
        A, B = rand_matrix(rng, r, k), rand_matrix(rng, d, r)
        alpha = 2.0 * r
        D = delta(A, B, alpha)
        for _ in range(4):
            x = rand_vector(rng, k)
            full = [a + b for a, b in zip(matvec(W0, x), matvec(D, x))]
            assert close(forward(W0, A, B, alpha, x), full, 1e-12)


def test_merged_equals_unmerged_and_unmerge_restores_W0():
    rng = random.Random(5)
    d, k, r = 7, 6, 2
    W0 = rand_matrix(rng, d, k)
    A, B = rand_matrix(rng, r, k), rand_matrix(rng, d, r)
    W = merge(W0, A, B, 4.0)
    X = [rand_vector(rng, k) for _ in range(6)]
    for h, x in zip(forward_batch(W0, A, B, 4.0, X), X):
        assert close(h, matvec(W, x), 1e-12)
    back = unmerge(W, A, B, 4.0)
    assert all(close(a, b, 1e-12) for a, b in zip(back, W0))


def test_update_has_rank_at_most_r():
    rng = random.Random(6)
    for d, k, r in [(5, 4, 1), (5, 4, 2), (6, 6, 3), (3, 6, 5)]:
        A = [[rng.randint(-3, 3) for _ in range(k)] for _ in range(r)]
        B = [[rng.randint(-3, 3) for _ in range(r)] for _ in range(d)]
        BA = [[int(v) for v in row] for row in matmul(B, A)]
        assert exact_rank(BA) <= min(r, d, k)
    # Generic integer factors reach rank r exactly.
    A = [[1, 0, 2, 1], [0, 1, 1, 3]]
    B = [[1, 0], [0, 1], [1, 1], [2, -1]]
    assert exact_rank([[int(v) for v in row] for row in matmul(B, A)]) == 2


def test_every_rank_r_update_is_reachable():
    # Delta = P Q with P: d x r and Q: r x k is reached with B = P and A = Q r / alpha.
    rng = random.Random(7)
    d, k, r, alpha = 5, 4, 2, 8.0
    P, Q = rand_matrix(rng, d, r), rand_matrix(rng, r, k)
    target = matmul(P, Q)
    A = [[v * r / alpha for v in row] for row in Q]
    D = delta(A, P, alpha)
    assert all(close(a, b, 1e-12) for a, b in zip(D, target))


def test_parameter_counts():
    assert trainable_parameters(12288, 12288, 1) == 24576
    assert trainable_parameters(12288, 12288, 4) == 98304
    assert 96 * 2 * trainable_parameters(12288, 12288, 1) == 4718592
    assert 96 * 2 * trainable_parameters(12288, 12288, 8) == 37748736


def test_gradients_against_finite_differences():
    rng = random.Random(8)
    d, k, r, alpha = 4, 3, 2, 3.0
    W0 = rand_matrix(rng, d, k)
    A, B = rand_matrix(rng, r, k), rand_matrix(rng, d, r)
    x, c = rand_vector(rng, k), rand_vector(rng, d)

    def loss(A_, B_, x_):
        # A smooth loss of h: sum_i c_i h_i + 0.5 h_i^2, so g_i = c_i + h_i.
        h = forward(W0, A_, B_, alpha, x_)
        return math.fsum(ci * hi + 0.5 * hi * hi for ci, hi in zip(c, h))

    h = forward(W0, A, B, alpha, x)
    g = [ci + hi for ci, hi in zip(c, h)]
    gA, gB, gx = backward(W0, A, B, alpha, x, g)
    eps = 1e-6
    for M, G in ((A, gA), (B, gB)):
        for i in range(len(M)):
            for j in range(len(M[0])):
                old = M[i][j]
                M[i][j] = old + eps
                up = loss(A, B, x)
                M[i][j] = old - eps
                down = loss(A, B, x)
                M[i][j] = old
                assert (up - down) / (2 * eps) == pytest.approx(G[i][j], abs=1e-5)
    for j in range(k):
        xp, xm = list(x), list(x)
        xp[j] += eps
        xm[j] -= eps
        assert (loss(A, B, xp) - loss(A, B, xm)) / (2 * eps) == pytest.approx(gx[j], abs=1e-5)


def test_gradients_are_the_full_gradient_projected():
    # dloss/dDelta = g x^T; then grad_B = s (g x^T) A^T and grad_A = s B^T (g x^T).
    rng = random.Random(9)
    d, k, r, alpha = 5, 4, 2, 2.0
    s = alpha / r
    W0 = rand_matrix(rng, d, k)
    A, B = rand_matrix(rng, r, k), rand_matrix(rng, d, r)
    x, g = rand_vector(rng, k), rand_vector(rng, d)
    gA, gB, _ = backward(W0, A, B, alpha, x, g)
    full = [[gi * xj for xj in x] for gi in g]
    At = [list(col) for col in zip(*A)]
    Bt = [list(col) for col in zip(*B)]
    want_B = [[s * v for v in row] for row in matmul(full, At)]
    want_A = [[s * v for v in row] for row in matmul(Bt, full)]
    assert all(close(a, b, 1e-12) for a, b in zip(gB, want_B))
    assert all(close(a, b, 1e-12) for a, b in zip(gA, want_A))


def test_batch_gradient_is_the_sum_over_tokens():
    rng = random.Random(10)
    d, k, r, alpha = 3, 4, 2, 1.0
    W0 = rand_matrix(rng, d, k)
    A, B = rand_matrix(rng, r, k), rand_matrix(rng, d, r)
    X = [rand_vector(rng, k) for _ in range(3)]
    G = [rand_vector(rng, d) for _ in range(3)]
    gA, gB = backward_batch(W0, A, B, alpha, X, G)
    sA = [[0.0] * k for _ in range(r)]
    for x, g in zip(X, G):
        a, _, _ = backward(W0, A, B, alpha, x, g)
        sA = [[sA[i][j] + a[i][j] for j in range(k)] for i in range(r)]
    assert all(close(a, b, 1e-12) for a, b in zip(gA, sA))


def test_training_fits_a_planted_rank_r_change():
    # The pretrained W0 is frozen; the target layer is W0 + P Q with rank 2.
    rng = random.Random(11)
    d, k, r, alpha = 4, 3, 2, 2.0
    W0 = rand_matrix(rng, d, k)
    P, Q = rand_matrix(rng, d, r), rand_matrix(rng, r, k)
    W_target = [[a + b for a, b in zip(r0, r1)] for r0, r1 in zip(W0, matmul(P, Q))]
    X = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
    Y = [matvec(W_target, x) for x in X]
    A, B = init(d, k, r, rng, sigma=0.5)
    first = None
    for _ in range(1500):
        loss = sgd_step(W0, A, B, alpha, X, Y, lr=0.5)
        first = loss if first is None else first
    final, _ = squared_loss(W0, A, B, alpha, X, Y)
    assert first > 0.05
    assert final < 1e-10
    W = merge(W0, A, B, alpha)
    assert all(close(a, b, 1e-4) for a, b in zip(W, W_target))


def test_shape_errors():
    with pytest.raises(ValueError):
        forward([[1.0, 2.0]], [[1.0]], [[1.0]], 1.0, [1.0, 1.0])
    with pytest.raises(ValueError):
        init(2, 2, 0, random.Random(0))
