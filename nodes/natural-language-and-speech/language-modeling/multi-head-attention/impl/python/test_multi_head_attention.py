# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-head-attention/. The authors are listed in prov/YXWRTE.jsonl.

import math
import random

import pytest

from multi_head_attention import attention, multi_head_attention, parameter_count
from nlslog import softmax

X_EX = [[2, 0, 0, 0], [2, 0, 0, 2], [0, 2, 2, 0]]
I4 = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def rand_matrix(rng, rows, cols, scale=1.0):
    return [[rng.gauss(0.0, scale) for _ in range(cols)] for _ in range(rows)]


def oracle(Xq, Xkv, WQ, WK, WV, WO, h, causal=False):
    """Sum over heads of head_r times the rows of W_O that belong to head r, with every entry by its formula."""
    n, m, d = len(Xq), len(Xkv), len(WO[0])
    dk, dv = len(WQ[0]) // h, len(WV[0]) // h
    out = [[0.0] * d for _ in range(n)]
    for r in range(h):
        def proj(X, W, size, i, a):
            return sum(X[i][t] * W[t][r * size + a] for t in range(len(W)))
        for i in range(n):
            js = [j for j in range(m) if not (causal and j > i + m - n)]
            scores = [
                sum(proj(Xq, WQ, dk, i, a) * proj(Xkv, WK, dk, j, a) for a in range(dk)) / math.sqrt(dk) for j in js
            ]
            p = softmax(scores)
            head = [sum(p[t] * proj(Xkv, WV, dv, j, b) for t, j in enumerate(js)) for b in range(dv)]
            for c in range(d):
                out[i][c] += sum(head[b] * WO[r * dv + b][c] for b in range(dv))
    return out


def close(A, B, tol=1e-9):
    return len(A) == len(B) and all(abs(a - b) <= tol * (1 + abs(b)) for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def random_case(rng):
    h = rng.choice([1, 2, 3])
    dk, dv = rng.randint(1, 3), rng.randint(1, 3)
    d = rng.randint(1, 5)
    n, m = rng.randint(1, 5), rng.randint(1, 5)
    return (
        rand_matrix(rng, n, d),
        rand_matrix(rng, m, d),
        rand_matrix(rng, d, h * dk),
        rand_matrix(rng, d, h * dk),
        rand_matrix(rng, d, h * dv),
        rand_matrix(rng, h * dv, d),
        h,
    )


def test_worked_example():
    out = multi_head_attention(X_EX, X_EX, I4, I4, I4, I4, 2)
    got = [[round(x, 5) for x in row] for row in out]
    assert got[0] == [1.94259, 0.05741, 0.66667, 0.66667]
    assert got[1] == [1.94259, 0.05741, 0.10571, 1.78857]
    assert got[2] == [0.21143, 1.78857, 1.78857, 0.10571]


@pytest.mark.parametrize("seed", range(20))
def test_against_per_head_sum(seed):
    rng = random.Random(seed)
    Xq, Xkv, WQ, WK, WV, WO, h = random_case(rng)
    assert close(multi_head_attention(Xq, Xkv, WQ, WK, WV, WO, h), oracle(Xq, Xkv, WQ, WK, WV, WO, h))
    if len(Xkv) >= len(Xq):
        assert close(
            multi_head_attention(Xq, Xkv, WQ, WK, WV, WO, h, causal=True),
            oracle(Xq, Xkv, WQ, WK, WV, WO, h, causal=True),
        )


@pytest.mark.parametrize("seed", range(5))
def test_one_head_is_attention_of_projections(seed):
    rng = random.Random(50 + seed)
    n, d = 4, 3
    X = rand_matrix(rng, n, d)
    WQ, WK, WV, WO = (rand_matrix(rng, d, d) for _ in range(4))

    def mm(A, B):
        return [[sum(A[i][t] * B[t][c] for t in range(len(B))) for c in range(len(B[0]))] for i in range(len(A))]

    want = mm(attention(mm(X, WQ), mm(X, WK), mm(X, WV)), WO)
    assert close(multi_head_attention(X, X, WQ, WK, WV, WO, 1), want)


@pytest.mark.parametrize("seed", range(10))
def test_self_attention_is_permutation_equivariant(seed):
    rng = random.Random(100 + seed)
    n, d, h = rng.randint(2, 5), 4, 2
    X = rand_matrix(rng, n, d)
    WQ, WK, WV, WO = (rand_matrix(rng, d, d) for _ in range(4))
    out = multi_head_attention(X, X, WQ, WK, WV, WO, h)
    perm = list(range(n))
    rng.shuffle(perm)
    Xp = [X[i] for i in perm]
    assert close(multi_head_attention(Xp, Xp, WQ, WK, WV, WO, h), [out[i] for i in perm])


@pytest.mark.parametrize("seed", range(10))
def test_causal_rows_ignore_later_tokens(seed):
    rng = random.Random(200 + seed)
    n, d, h = rng.randint(2, 5), 4, 2
    X = rand_matrix(rng, n, d)
    WQ, WK, WV, WO = (rand_matrix(rng, d, d) for _ in range(4))
    out = multi_head_attention(X, X, WQ, WK, WV, WO, h, causal=True)
    t = rng.randrange(n)
    Y = [row[:] if i <= t else [rng.gauss(0, 3) for _ in row] for i, row in enumerate(X)]
    out2 = multi_head_attention(Y, Y, WQ, WK, WV, WO, h, causal=True)
    assert close(out2[: t + 1], out[: t + 1], 1e-12)


def test_parameter_count():
    assert parameter_count(512, 8, 64, 64) == 4 * 512 * 512
    assert parameter_count(512, 8, 64, 64, bias=True) == 4 * 512 * 512 + 4 * 512
    assert parameter_count(6, 3, 2, 1) == 2 * 6 * 6 + 2 * 3 * 6


def test_errors():
    rng = random.Random(1)
    X = rand_matrix(rng, 2, 4)
    W = rand_matrix(rng, 4, 4)
    with pytest.raises(ValueError):
        multi_head_attention(X, X, W, W, W, W, 3)
    with pytest.raises(ValueError):
        multi_head_attention(X, X, W, W, W, W, 0)
    with pytest.raises(ValueError):
        multi_head_attention(X, X, W, W, W, rand_matrix(rng, 3, 4), 2)
    with pytest.raises(ValueError):
        multi_head_attention(X, X[:1], W, W, W, W, 2, causal=True)
