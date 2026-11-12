# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-accumulation/. The authors are listed in prov/H2P10E.jsonl.

import random
from fractions import Fraction as F

from gradient_accumulation import (
    accumulated_grad,
    batchnorm_grad,
    batchnorm_loss_grad,
    mse_grad,
    split,
    train_with_accumulation,
)


def data(n, seed):
    rng = random.Random(seed)
    return [([F(rng.randint(-9, 9)), F(rng.randint(-9, 9)), F(1)], F(rng.randint(-20, 20))) for _ in range(n)]


def test_equal_micro_batches_give_the_full_gradient_exactly() -> None:
    batch = data(12, 1)
    w = [F(1, 3), F(-2, 7), F(5)]
    full = mse_grad(w, batch)
    for m in (1, 2, 3, 4, 6, 12):
        micro = split(batch, [12 // m] * m)
        assert accumulated_grad(mse_grad, w, micro, "equal") == full
        assert accumulated_grad(mse_grad, w, micro, "size") == full


def test_unequal_sizes_need_size_weights() -> None:
    batch = data(10, 2)
    w = [F(1), F(1), F(0)]
    full = mse_grad(w, batch)
    micro = split(batch, [7, 3])
    assert accumulated_grad(mse_grad, w, micro, "size") == full
    assert accumulated_grad(mse_grad, w, micro, "equal") != full


def test_summing_without_scaling_is_m_times_too_large() -> None:
    batch = data(8, 3)
    w = [F(0), F(1), F(-1)]
    micro = split(batch, [2, 2, 2, 2])
    summed = [sum(c) for c in zip(*(mse_grad(w, b) for b in micro))]
    assert summed == [4 * g for g in mse_grad(w, batch)]


def test_training_with_accumulation_equals_large_batch_sgd() -> None:
    batches = [data(8, 10 + k) for k in range(5)]
    w0 = [F(0), F(0), F(0)]
    lr = F(1, 200)
    accumulated = train_with_accumulation(mse_grad, w0, batches, [3, 3, 2], lr)
    w, large = w0, [w0]
    for b in batches:
        w = [a - lr * g for a, g in zip(w, mse_grad(w, b))]
        large.append(w)
    assert accumulated == large


# Batch norm counterexample. With w = (1, 0) the pre-activation is x_1. The
# micro-batches {-7, -1, 1, 7} and {17, 23, 25, 31} both have standard
# deviation 5, the whole batch has mean 12 and standard deviation 13, so every
# statistic is rational and the gradients are exact Fractions.
X1 = [-7, -1, 1, 7, 17, 23, 25, 31]
X2 = [1, 0, 2, 1, 0, 1, 1, 2]
Y = [-1, 0, 1, 0, 1, -1, 1, 0]
BN_BATCH = [([F(a), F(b)], F(c)) for a, b, c in zip(X1, X2, Y)]
W = [F(1), F(0)]


def test_batch_norm_statistics_are_rational() -> None:
    loss, _ = batchnorm_loss_grad(W, BN_BATCH)
    assert loss == F(139, 104)
    assert [batchnorm_loss_grad(W, b)[0] for b in split(BN_BATCH, [4, 4])] == [F(7, 10), F(9, 4)]


def test_accumulation_with_batch_norm_is_not_the_large_batch_gradient() -> None:
    micro = split(BN_BATCH, [4, 4])
    full = batchnorm_grad(W, BN_BATCH)
    acc = accumulated_grad(batchnorm_grad, W, micro)
    assert full == [F(0), F(15, 4394)]
    assert acc == [F(0), F(-27, 1000)]
    # Not only different: the second component has the opposite sign.
    assert acc != full and acc[1] * full[1] < 0


def test_without_batch_norm_the_same_split_is_exact() -> None:
    micro = split(BN_BATCH, [4, 4])
    assert accumulated_grad(mse_grad, W, micro) == mse_grad(W, BN_BATCH)


def test_accumulation_with_batch_norm_is_the_ghost_batch_gradient() -> None:
    # It is the exact gradient of the mean of the micro-batch losses, each
    # micro-batch normalized on its own (ghost batch normalization).
    micro = split(BN_BATCH, [4, 4])

    def ghost_loss(w):
        return sum(batchnorm_loss_grad(w, b)[0] for b in micro) / len(micro)

    acc = [float(g) for g in accumulated_grad(batchnorm_grad, W, micro)]
    h = 1e-6
    for k in range(2):
        wp = [float(a) + (h if i == k else 0) for i, a in enumerate(W)]
        wm = [float(a) - (h if i == k else 0) for i, a in enumerate(W)]
        assert abs((ghost_loss(wp) - ghost_loss(wm)) / (2 * h) - acc[k]) < 1e-6


def test_batchnorm_gradient_matches_finite_differences() -> None:
    rng = random.Random(4)
    batch = [([rng.gauss(0, 1) for _ in range(3)], rng.gauss(0, 1)) for _ in range(6)]
    w = [rng.gauss(0, 1) for _ in range(3)]
    _, g = batchnorm_loss_grad(w, batch)
    h = 1e-6
    for k in range(3):
        wp = [a + (h if i == k else 0) for i, a in enumerate(w)]
        wm = [a - (h if i == k else 0) for i, a in enumerate(w)]
        num = (batchnorm_loss_grad(wp, batch)[0] - batchnorm_loss_grad(wm, batch)[0]) / (2 * h)
        assert abs(num - g[k]) < 1e-6
