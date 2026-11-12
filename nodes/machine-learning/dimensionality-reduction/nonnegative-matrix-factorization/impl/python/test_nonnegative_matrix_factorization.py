# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonnegative-matrix-factorization/. The authors are listed in prov/N3ZBGQ.jsonl.

import random

import pytest

from nonnegative_matrix_factorization import (
    frobenius_loss,
    kl_loss,
    matmul,
    nmf,
    random_init,
    update_h_frobenius,
    update_h_kl,
    update_w_frobenius,
    update_w_kl,
)

W0 = [[1, 0], [2, 1], [0, 1], [1, 3]]
H0 = [[1, 2, 0, 1], [0, 1, 2, 1]]
SQUARE = [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1]]


def random_matrix(rng: random.Random, m: int, n: int) -> list:
    return [[rng.random() * 3 for _ in range(n)] for _ in range(m)]


def test_frobenius_loss_never_increases_at_any_half_step() -> None:
    rng = random.Random(1)
    for _ in range(3):
        v = random_matrix(rng, 6, 5)
        w, h = random_init(6, 5, 3, rng)
        prev = frobenius_loss(v, w, h)
        for _ in range(100):
            h = update_h_frobenius(v, w, h)
            cur = frobenius_loss(v, w, h)
            assert cur <= prev * (1 + 1e-12)
            prev = cur
            w = update_w_frobenius(v, w, h)
            cur = frobenius_loss(v, w, h)
            assert cur <= prev * (1 + 1e-12)
            prev = cur


def test_kl_loss_never_increases() -> None:
    rng = random.Random(2)
    v = random_matrix(rng, 5, 6)
    w, h = random_init(5, 6, 2, rng)
    prev = kl_loss(v, w, h)
    for _ in range(100):
        h = update_h_kl(v, w, h)
        cur = kl_loss(v, w, h)
        assert cur <= prev * (1 + 1e-12)
        prev = cur
        w = update_w_kl(v, w, h)
        cur = kl_loss(v, w, h)
        assert cur <= prev * (1 + 1e-12)
        prev = cur


def test_factors_stay_nonnegative_and_zeros_stay_zero() -> None:
    rng = random.Random(3)
    v = random_matrix(rng, 5, 4)
    w, h = random_init(5, 4, 2, rng)
    w[0][1] = 0.0
    h[1][2] = 0.0
    w2, h2, losses = nmf(v, 2, rng, iters=200, init=(w, h))
    assert all(x >= 0 for row in w2 for x in row)
    assert all(x >= 0 for row in h2 for x in row)
    assert w2[0][1] == 0.0 and h2[1][2] == 0.0
    assert all(b <= a * (1 + 1e-12) for a, b in zip(losses, losses[1:]))


def test_exact_factorization_is_a_fixed_point_and_is_found() -> None:
    v = matmul(W0, H0)
    w = [[float(x) for x in row] for row in W0]
    h = [[float(x) for x in row] for row in H0]
    for new, old in zip(update_h_frobenius(v, w, h), h):
        assert new == pytest.approx(old)
    for new, old in zip(update_w_frobenius(v, w, h), w):
        assert new == pytest.approx(old)
    start = ([[1.0, 1.0] for _ in range(4)], [[1.0, 0.5, 0.5, 1.0], [0.5, 1.0, 1.0, 0.5]])
    _, _, losses = nmf(v, 2, random.Random(0), iters=1000, init=start)
    assert losses[0] == pytest.approx(60.0)
    assert losses[-1] < 1e-3


def test_nonnegative_rank_can_exceed_rank() -> None:
    # The square matrix has rank 3 (row 1 + row 4 = row 2 + row 3), but no
    # nonnegative rank-3 factorization fits it exactly.
    r = SQUARE
    assert [a + d for a, d in zip(r[0], r[3])] == [b + c for b, c in zip(r[1], r[2])]
    minor = [row[:3] for row in r[:3]]
    det = (minor[0][0] * (minor[1][1] * minor[2][2] - minor[1][2] * minor[2][1])
           - minor[0][1] * (minor[1][0] * minor[2][2] - minor[1][2] * minor[2][0])
           + minor[0][2] * (minor[1][0] * minor[2][1] - minor[1][1] * minor[2][0]))
    assert det != 0
    for seed in range(4):
        _, _, l3 = nmf(r, 3, random.Random(seed), iters=1500)
        assert l3[-1] > 0.5
    _, _, l4 = nmf(r, 4, random.Random(9), iters=3000)
    assert l4[-1] < 0.05


def test_negative_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        nmf([[1.0, -1.0], [0.0, 1.0]], 1, random.Random(0))
