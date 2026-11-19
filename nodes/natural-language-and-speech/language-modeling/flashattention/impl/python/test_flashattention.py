# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flashattention/. The authors are listed in prov/5X6J97.jsonl.

import math
import random

import pytest

from flashattention import block_sizes, flash_attention, io_count, standard_attention_io
from nlslog import softmax


def rand_matrix(rng, rows, cols, scale=1.0):
    return [[rng.gauss(0.0, scale) for _ in range(cols)] for _ in range(rows)]


def plain_attention(Q, K, V, causal=False):
    """The definition, with the whole row of scores at once and the shared softmax helper."""
    n, m, dk = len(Q), len(K), len(K[0])
    out = []
    for i in range(n):
        js = [j for j in range(m) if not (causal and j > i + m - n)]
        p = softmax([sum(a * b for a, b in zip(Q[i], K[j])) / math.sqrt(dk) for j in js])
        out.append([sum(p[t] * V[j][c] for t, j in enumerate(js)) for c in range(len(V[0]))])
    return out


def close(A, B, tol=1e-9):
    return len(A) == len(B) and all(abs(a - b) <= tol * (1 + abs(b)) for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def test_worked_example():
    Q, K, V = [[1.0]], [[1.0], [3.0], [2.0], [0.0]], [[10.0], [20.0], [30.0], [40.0]]
    O1, _ = flash_attention(Q, K[:2], V[:2], 1, 2)
    assert round(O1[0][0], 4) == 18.808
    O, _ = flash_attention(Q, K, V, 1, 2)
    assert round(O[0][0], 6) == 22.138557
    assert close(O, plain_attention(Q, K, V))


@pytest.mark.parametrize("seed", range(25))
def test_matches_plain_attention(seed):
    rng = random.Random(seed)
    n, m = rng.randint(1, 9), rng.randint(1, 9)
    dk, dv = rng.randint(1, 4), rng.randint(1, 3)
    Q, K, V = rand_matrix(rng, n, dk, 2.0), rand_matrix(rng, m, dk, 2.0), rand_matrix(rng, m, dv)
    B_r, B_c = rng.randint(1, 4), rng.randint(1, 4)
    O, io = flash_attention(Q, K, V, B_r, B_c)
    assert close(O, plain_attention(Q, K, V))
    assert io == io_count(n, m, dk, dv, B_c)
    if m >= n:
        Oc, _ = flash_attention(Q, K, V, B_r, B_c, causal=True)
        assert close(Oc, plain_attention(Q, K, V, causal=True))


@pytest.mark.parametrize("B_r,B_c", [(1, 1), (2, 3), (5, 5), (8, 8), (3, 7)])
def test_block_sizes_do_not_change_the_result(B_r, B_c):
    rng = random.Random(42)
    Q, K, V = rand_matrix(rng, 7, 3), rand_matrix(rng, 7, 3), rand_matrix(rng, 7, 2)
    O, _ = flash_attention(Q, K, V, B_r, B_c, causal=True)
    assert close(O, plain_attention(Q, K, V, causal=True))


def test_large_scores_do_not_overflow():
    Q = [[30.0, 30.0]]
    K = [[-30.0, -30.0], [30.0, 30.0], [29.0, 29.0], [30.0, 29.5]]
    V = [[1.0], [2.0], [3.0], [4.0]]
    O, _ = flash_attention(Q, K, V, 1, 1)
    assert all(math.isfinite(x) for x in O[0])
    assert close(O, plain_attention(Q, K, V))


def test_io_formula_and_its_growth():
    d = 4
    n = 48
    rng = random.Random(3)
    Q, K, V = rand_matrix(rng, n, d), rand_matrix(rng, n, d), rand_matrix(rng, n, d)
    ios = []
    for M in (64, 128, 256, 512):
        B_r, B_c = block_sizes(M, d)
        _, io = flash_attention(Q, K, V, B_r, B_c)
        assert io == io_count(n, n, d, d, B_c)
        ios.append(io)
    assert ios == sorted(ios, reverse=True)
    # With B_c = M / 4d there are T_c = 4 n d / M key blocks, each moving n (3d + 4) numbers,
    # so the leading term is 12 n^2 d^2 / M, plus 16 n^2 d / M for l and m.
    M = 128
    _, B_c = block_sizes(M, d)
    assert B_c == M // (4 * d) and n % B_c == 0
    T_c = 4 * n * d // M
    assert io_count(n, n, d, d, B_c) == 12 * n * n * d * d // M + 4 * n * T_c + n * (d + 2) + 2 * n * d
    # Fewer transfers than plain attention once M is large compared with d^2.
    assert io_count(n, n, d, d, block_sizes(512, d)[1]) < standard_attention_io(n, n, d, d)


def test_block_sizes():
    assert block_sizes(100_000, 64) == (64, 391)
    assert block_sizes(64, 4) == (4, 4)
    with pytest.raises(ValueError):
        block_sizes(0, 4)


def test_errors():
    with pytest.raises(ValueError):
        flash_attention([[1.0]], [[1.0]], [[1.0]], 0, 1)
    with pytest.raises(ValueError):
        flash_attention([[1.0], [1.0]], [[1.0]], [[1.0]], 1, 1, causal=True)
    with pytest.raises(ValueError):
        flash_attention([[1.0, 2.0]], [[1.0]], [[1.0]], 1, 1)
