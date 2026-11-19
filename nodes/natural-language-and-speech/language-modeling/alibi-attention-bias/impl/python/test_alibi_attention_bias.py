# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alibi-attention-bias/. The authors are listed in prov/FKDFWV.jsonl.

import math
import random

import pytest

from alibi_attention_bias import alibi_attention, alibi_bias, alibi_slopes


def rand_matrix(rng, rows, cols, scale=1.0):
    return [[rng.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]


def oracle(Q, K, V, bias):
    """Full score matrix plus a bias matrix, then a log-sum-exp softmax per row."""
    dk = len(K[0])
    out = []
    for i, q in enumerate(Q):
        s = [sum(a * b for a, b in zip(q, k)) / math.sqrt(dk) + bias[i][j] for j, k in enumerate(K)]
        mu = max(s)
        lse = mu + math.log(sum(math.exp(x - mu) for x in s if x != float("-inf")))
        p = [math.exp(x - lse) if x != float("-inf") else 0.0 for x in s]
        out.append([sum(p[j] * V[j][c] for j in range(len(V))) for c in range(len(V[0]))])
    return out


def close(A, B, tol=1e-9):
    return all(abs(a - b) <= tol * (1 + abs(b)) for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def test_worked_example():
    Q = [[0.0]] * 4
    K = [[0.0]] * 4
    V = [[0.0], [1.0], [2.0], [3.0]]
    O = alibi_attention(Q, K, V, 0.5)
    assert [round(r[0], 6) for r in O] == [0.0, 0.622459, 1.320157, 2.084576]
    # with slope 0 every visible key gets the same weight
    assert [r[0] for r in alibi_attention(Q, K, V, 0.0)] == pytest.approx([0.0, 0.5, 1.0, 1.5])


def test_slopes():
    assert alibi_slopes(8) == [2.0 ** -k for k in range(1, 9)]
    s16 = alibi_slopes(16)
    assert s16 == pytest.approx([2.0 ** (-k / 2) for k in range(1, 17)])
    # 16 heads interleave the 8 slopes with their geometric means
    assert s16[1::2] == pytest.approx(alibi_slopes(8))
    s12 = alibi_slopes(12)
    assert s12[:8] == alibi_slopes(8)
    assert s12[8:] == pytest.approx([2.0 ** -0.5, 2.0 ** -1.5, 2.0 ** -2.5, 2.0 ** -3.5])
    for h in range(1, 40):
        s = alibi_slopes(h)
        assert len(s) == h and len(set(s)) == h and all(0 < x < 1 for x in s)


@pytest.mark.parametrize("seed", range(12))
def test_against_bias_matrix_oracle(seed):
    rng = random.Random(seed)
    M = rng.randint(1, 9)
    n = rng.randint(1, M)
    dk, dv = rng.randint(1, 5), rng.randint(1, 4)
    Q, K, V = rand_matrix(rng, n, dk), rand_matrix(rng, M, dk), rand_matrix(rng, M, dv)
    slope = rng.choice(alibi_slopes(8))
    assert close(alibi_attention(Q, K, V, slope), oracle(Q, K, V, alibi_bias(n, M, slope)))


@pytest.mark.parametrize("seed", range(8))
def test_row_shift_gives_the_same_output(seed):
    """Adding slope * p_i to row i turns the bias into +slope * j; the softmax does not change."""
    rng = random.Random(100 + seed)
    M = rng.randint(1, 9)
    n = rng.randint(1, M)
    Q, K, V = rand_matrix(rng, n, 3), rand_matrix(rng, M, 3), rand_matrix(rng, M, 2)
    slope = rng.uniform(0, 1)
    shift = M - n
    key_only = [[slope * j if j <= i + shift else float("-inf") for j in range(M)] for i in range(n)]
    assert close(alibi_attention(Q, K, V, slope), oracle(Q, K, V, key_only))


@pytest.mark.parametrize("seed", range(8))
def test_bias_depends_only_on_distance_and_cache_rows_match(seed):
    rng = random.Random(200 + seed)
    M = rng.randint(1, 6)
    t = rng.randint(1, 5)
    slope = rng.choice(alibi_slopes(8))
    small, big = alibi_bias(M, M, slope), alibi_bias(M + t, M + t, slope)
    assert all(small[i][j] == big[i + t][j + t] for i in range(M) for j in range(M))
    # with a key-value cache (n < M) the rows equal the last rows of the full run
    Q, K, V = rand_matrix(rng, M, 3), rand_matrix(rng, M, 3), rand_matrix(rng, M, 2)
    n = rng.randint(1, M)
    assert close(alibi_attention(Q[M - n :], K, V, slope), alibi_attention(Q, K, V, slope)[M - n :])


@pytest.mark.parametrize("seed", range(8))
def test_far_keys_get_small_weight(seed):
    """If every |q . k| / sqrt(d_k) <= B, the weight on a key at distance r is at most exp(2B - m r)."""
    rng = random.Random(300 + seed)
    M, dk = 30, 4
    Q = rand_matrix(rng, M, dk, 0.5)
    K = rand_matrix(rng, M, dk, 0.5)
    slope = rng.choice([0.5, 0.25, 0.125])
    B = max(abs(sum(a * b for a, b in zip(q, k))) / math.sqrt(dk) for q in Q for k in K)
    i = M - 1
    for j in range(M):
        V = [[1.0 if t == j else 0.0] for t in range(M)]
        w = alibi_attention(Q, K, V, slope)[i][0]
        assert w <= math.exp(2 * B - slope * (i - j)) + 1e-12


def test_large_slope_attends_to_self_and_rows_sum_to_one():
    rng = random.Random(7)
    Q, K, V = rand_matrix(rng, 5, 3), rand_matrix(rng, 5, 3), rand_matrix(rng, 5, 2)
    O = alibi_attention(Q, K, V, 1000.0)
    assert close(O, V, 1e-9)
    ones = [[1.0] for _ in range(5)]
    assert all(r[0] == pytest.approx(1.0) for r in alibi_attention(Q, K, ones, 0.3))


def test_errors():
    with pytest.raises(ValueError):
        alibi_slopes(0)
    with pytest.raises(ValueError):
        alibi_attention([[1.0], [1.0]], [[1.0]], [[1.0]], 0.5)
    with pytest.raises(ValueError):
        alibi_attention([[1.0]], [[1.0]], [[1.0]], -0.5)
    with pytest.raises(ValueError):
        alibi_attention([[1.0, 2.0]], [[1.0]], [[1.0]], 0.5)
