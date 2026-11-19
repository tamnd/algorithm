# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grouped-query-attention/. The authors are listed in prov/VQPZ6C.jsonl.

import math
import random

import pytest

from grouped_query_attention import grouped_query_attention, group_of, kv_cache_entries, mean_pool_heads
from nlslog import softmax


def rand_matrix(rng, rows, cols, scale=1.0):
    return [[rng.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]


def oracle(Xq, Xkv, WQ, WK, WV, WO, h, g, causal=False):
    """Multi-head attention written entry by entry, where head r reads the key and value columns of group r // (h // g)."""
    d = len(Xq[0])
    dk, dv = len(WQ[0]) // h, len(WV[0]) // g
    n, M = len(Xq), len(Xkv)
    out = [[0.0] * len(WO[0]) for _ in range(n)]
    for r in range(h):
        s = r * g // h

        def proj(X, W, size, i, a):
            return [sum(X[i][t] * W[t][a * size + c] for t in range(d)) for c in range(size)]

        for i in range(n):
            q = proj(Xq, WQ, dk, i, r)
            visible = [j for j in range(M) if not causal or j <= i + M - n]
            scores = [sum(a * b for a, b in zip(q, proj(Xkv, WK, dk, j, s))) / math.sqrt(dk) for j in visible]
            p = softmax(scores)
            head = [sum(p[t] * proj(Xkv, WV, dv, j, s)[c] for t, j in enumerate(visible)) for c in range(dv)]
            for c in range(dv):
                for e in range(len(WO[0])):
                    out[i][e] += head[c] * WO[r * dv + c][e]
    return out


def close(A, B, tol=1e-9):
    return all(abs(a - b) <= tol * (1 + abs(b)) for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def random_case(rng):
    g = rng.choice([1, 2, 3])
    h = g * rng.choice([1, 2, 3])
    d, dk, dv = rng.randint(1, 5), rng.randint(1, 3), rng.randint(1, 3)
    M = rng.randint(1, 5)
    n = rng.randint(1, M)
    return dict(
        Xq=rand_matrix(rng, n, d),
        Xkv=rand_matrix(rng, M, d),
        WQ=rand_matrix(rng, d, h * dk),
        WK=rand_matrix(rng, d, g * dk),
        WV=rand_matrix(rng, d, g * dv),
        WO=rand_matrix(rng, h * dv, d),
        h=h,
        g=g,
    )


def repeat_heads(W, h, g):
    """Copy the column block of each group to every query head in it: d x (g c) to d x (h c)."""
    c = len(W[0]) // g
    return [[row[(r // (h // g)) * c + u] for r in range(h) for u in range(c)] for row in W]


def test_worked_example():
    # h = 4 query heads, g = 2 groups, d = d_k = d_v = 1 per head; tokens 0 and 1
    X = [[1.0], [2.0]]
    WQ = [[1.0, 0.0, 1.0, 0.0]]
    WK = [[1.0, 0.5]]
    WV = [[1.0, -1.0]]
    WO = [[1.0], [1.0], [1.0], [1.0]]
    assert [group_of(r, 4, 2) for r in range(4)] == [0, 0, 1, 1]
    O = grouped_query_attention(X, X, WQ, WK, WV, WO, 4, 2, causal=True)
    # token 0 sees key 0 only: heads give 1, 1, -1, -1
    assert round(O[0][0], 6) == 0.0
    # token 1: head 0 has scores 2 and 4 on values 1 and 2, head 2 has 1 and 2 on -1 and -2,
    # heads 1 and 3 have query 0 and give the means 1.5 and -1.5
    sig = lambda x: 1 / (1 + math.exp(-x))
    assert O[1][0] == pytest.approx((1 + sig(2)) + 1.5 - (1 + sig(1)) - 1.5)
    assert round(O[1][0], 6) == 0.149738
    # without the mask, token 0 also sees key 1
    O = grouped_query_attention(X, X, WQ, WK, WV, WO, 4, 2)
    assert O[0][0] == pytest.approx(sig(1) - sig(0.5))
    assert round(O[0][0], 6) == 0.108599


@pytest.mark.parametrize("seed", range(12))
def test_against_oracle(seed):
    rng = random.Random(seed)
    c = random_case(rng)
    causal = rng.random() < 0.5
    got = grouped_query_attention(c["Xq"], c["Xkv"], c["WQ"], c["WK"], c["WV"], c["WO"], c["h"], c["g"], causal)
    assert close(got, oracle(c["Xq"], c["Xkv"], c["WQ"], c["WK"], c["WV"], c["WO"], c["h"], c["g"], causal))


@pytest.mark.parametrize("seed", range(8))
def test_equals_multi_head_with_repeated_keys_and_values(seed):
    rng = random.Random(100 + seed)
    c = random_case(rng)
    h, g = c["h"], c["g"]
    got = grouped_query_attention(c["Xq"], c["Xkv"], c["WQ"], c["WK"], c["WV"], c["WO"], h, g)
    WK, WV = repeat_heads(c["WK"], h, g), repeat_heads(c["WV"], h, g)
    mha = grouped_query_attention(c["Xq"], c["Xkv"], c["WQ"], WK, WV, c["WO"], h, h)
    assert close(got, mha)


@pytest.mark.parametrize("seed", range(5))
def test_mean_pool_keeps_a_model_whose_group_heads_agree(seed):
    rng = random.Random(200 + seed)
    c = random_case(rng)
    h, g = c["h"], c["g"]
    WK, WV = repeat_heads(c["WK"], h, g), repeat_heads(c["WV"], h, g)
    assert close(mean_pool_heads(WK, h, g), c["WK"])
    assert close(mean_pool_heads(WV, h, g), c["WV"])
    # pooling to h groups changes nothing, pooling to 1 group averages all heads
    assert mean_pool_heads(WK, h, h) == WK
    one = mean_pool_heads(c["WK"], g, 1)
    dk = len(c["WK"][0]) // g
    assert close(one, [[sum(row[s * dk + u] for s in range(g)) / g for u in range(dk)] for row in c["WK"]])


def test_cache_size():
    # 8 query heads of size 128: MHA, GQA with 2 groups, MQA
    assert kv_cache_entries(32, 4096, 8, 128, 128) == 2 * 32 * 4096 * 8 * 128
    assert kv_cache_entries(32, 4096, 2, 128, 128) * 4 == kv_cache_entries(32, 4096, 8, 128, 128)
    assert kv_cache_entries(32, 4096, 1, 128, 128) * 8 == kv_cache_entries(32, 4096, 8, 128, 128)


def test_errors():
    X = [[1.0]]
    with pytest.raises(ValueError):
        grouped_query_attention(X, X, [[1.0] * 4], [[1.0] * 3], [[1.0] * 3], [[1.0]] * 4, 4, 3)
    with pytest.raises(ValueError):
        grouped_query_attention(X, X, [[1.0] * 4], [[1.0] * 2], [[1.0] * 2], [[1.0]] * 4, 4, 0)
    with pytest.raises(ValueError):
        grouped_query_attention(X, X, [[1.0] * 4], [[1.0] * 4], [[1.0] * 2], [[1.0]] * 4, 4, 2)
    with pytest.raises(ValueError):
        grouped_query_attention([[1.0], [1.0]], X, [[1.0] * 2], [[1.0]], [[1.0]], [[1.0]] * 2, 2, 1, causal=True)
    with pytest.raises(ValueError):
        mean_pool_heads([[1.0] * 6], 3, 2)
