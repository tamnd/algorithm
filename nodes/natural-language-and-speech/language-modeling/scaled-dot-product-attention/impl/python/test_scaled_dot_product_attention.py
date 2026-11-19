# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scaled-dot-product-attention/. The authors are listed in prov/YMRYDZ.jsonl.

import math
import random

import pytest

from nlslog import softmax
from scaled_dot_product_attention import attention, attention_weights

Q_EX = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0]]
K_EX = [[2, 2, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1]]
V_EX = [[1, 0], [0, 1], [1, 1]]


def rand_matrix(rng, rows, cols, scale=1.0):
    return [[rng.gauss(0.0, scale) for _ in range(cols)] for _ in range(rows)]


def oracle(Q, K, V, visible):
    """Scores by the definition, weights from the shared softmax helper."""
    dk = len(K[0])
    out = []
    for i, q in enumerate(Q):
        idx = [j for j in range(len(K)) if visible(i, j)]
        scores = [sum(a * b for a, b in zip(q, K[j])) / math.sqrt(dk) for j in idx]
        p = softmax(scores)
        out.append([sum(p[t] * V[j][c] for t, j in enumerate(idx)) for c in range(len(V[0]))])
    return out


def close(A, B, tol=1e-9):
    return all(abs(a - b) <= tol * (1 + abs(b)) for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def test_worked_example():
    O, P = attention_weights(Q_EX, K_EX, V_EX)
    assert [round(x, 5) for x in P[0]] == [0.66524, 0.24473, 0.09003]
    assert [round(x, 5) for x in O[0]] == [0.75527, 0.33476]
    assert [round(x, 5) for x in O[1]] == [0.78806, 0.78806]
    assert [round(x, 5) for x in O[2]] == [0.72593, 0.54814]


def test_worked_example_causal():
    O, P = attention_weights(Q_EX, K_EX, V_EX, causal=True)
    assert P[0] == [1.0, 0.0, 0.0]
    assert P[1] == [0.5, 0.5, 0.0]
    assert [round(x, 5) for x in O[2]] == [0.72593, 0.54814]


@pytest.mark.parametrize("seed", range(20))
def test_against_oracle(seed):
    rng = random.Random(seed)
    n, m, dk, dv = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 5), rng.randint(1, 4)
    Q, K, V = rand_matrix(rng, n, dk), rand_matrix(rng, m, dk), rand_matrix(rng, m, dv)
    assert close(attention(Q, K, V), oracle(Q, K, V, lambda i, j: True))
    mask = [[rng.random() < 0.6 for _ in range(m)] for _ in range(n)]
    for row in mask:
        row[rng.randrange(m)] = True
    assert close(attention(Q, K, V, mask=mask), oracle(Q, K, V, lambda i, j: mask[i][j]))
    if m >= n:
        shift = m - n
        assert close(attention(Q, K, V, causal=True), oracle(Q, K, V, lambda i, j: j <= i + shift))


@pytest.mark.parametrize("seed", range(10))
def test_weights_are_a_distribution_and_output_is_convex(seed):
    rng = random.Random(100 + seed)
    n, m = rng.randint(1, 5), rng.randint(1, 7)
    Q, K, V = rand_matrix(rng, n, 3, 2.0), rand_matrix(rng, m, 3, 2.0), rand_matrix(rng, m, 2)
    O, P = attention_weights(Q, K, V)
    for i in range(n):
        assert all(p >= 0 for p in P[i])
        assert abs(math.fsum(P[i]) - 1) < 1e-12
        for c in range(2):
            col = [V[j][c] for j in range(m)]
            assert min(col) - 1e-12 <= O[i][c] <= max(col) + 1e-12


@pytest.mark.parametrize("seed", range(10))
def test_permutation_equivariance(seed):
    rng = random.Random(200 + seed)
    n, m = rng.randint(2, 5), rng.randint(2, 5)
    Q, K, V = rand_matrix(rng, n, 3), rand_matrix(rng, m, 3), rand_matrix(rng, m, 2)
    O = attention(Q, K, V)
    pq = list(range(n))
    rng.shuffle(pq)
    assert close(attention([Q[i] for i in pq], K, V), [O[i] for i in pq])
    pk = list(range(m))
    rng.shuffle(pk)
    assert close(attention(Q, [K[j] for j in pk], [V[j] for j in pk]), O)


@pytest.mark.parametrize("seed", range(10))
def test_causal_output_ignores_later_keys(seed):
    rng = random.Random(300 + seed)
    n = rng.randint(2, 6)
    Q, K, V = rand_matrix(rng, n, 3), rand_matrix(rng, n, 3), rand_matrix(rng, n, 2)
    O = attention(Q, K, V, causal=True)
    t = rng.randrange(n)
    K2 = [row[:] if j <= t else [rng.gauss(0, 5) for _ in row] for j, row in enumerate(K)]
    V2 = [row[:] if j <= t else [rng.gauss(0, 5) for _ in row] for j, row in enumerate(V)]
    O2 = attention(Q, K2, V2, causal=True)
    assert close(O2[: t + 1], O[: t + 1], 0.0)


def test_large_scores_do_not_overflow():
    Q = [[1000.0, 0.0]]
    K = [[1000.0, 0.0], [999.0, 0.0], [-1000.0, 0.0]]
    V = [[1.0], [2.0], [3.0]]
    O, P = attention_weights(Q, K, V)
    assert all(math.isfinite(p) for p in P[0])
    assert P[0][0] == pytest.approx(1.0)
    assert O[0][0] == pytest.approx(1.0)


def test_shift_invariance():
    rng = random.Random(7)
    Q, K, V = rand_matrix(rng, 1, 4), rand_matrix(rng, 5, 4), rand_matrix(rng, 5, 3)
    # Adding the same vector to every key adds q . u / sqrt(d) to every score of the row.
    u = [rng.gauss(0, 3) for _ in range(4)]
    K2 = [[a + b for a, b in zip(row, u)] for row in K]
    assert close(attention(Q, K2, V), attention(Q, K, V), 1e-9)


def test_dot_product_variance_is_d():
    rng = random.Random(11)
    d, trials = 64, 3000
    sq = 0.0
    for _ in range(trials):
        q = [rng.gauss(0, 1) for _ in range(d)]
        k = [rng.gauss(0, 1) for _ in range(d)]
        sq += sum(a * b for a, b in zip(q, k)) ** 2
    assert abs(sq / trials / d - 1) < 0.1


def test_errors():
    with pytest.raises(ValueError):
        attention([[1.0]], [[1.0], [2.0]], [[1.0]])
    with pytest.raises(ValueError):
        attention([[1.0, 2.0]], [[1.0]], [[1.0]])
    with pytest.raises(ValueError):
        attention([[1.0]], [[1.0]], [[1.0]], mask=[[False]])
    with pytest.raises(ValueError):
        attention([[1.0], [2.0]], [[1.0]], [[1.0]], causal=True)
    with pytest.raises(ValueError):
        attention([], [[1.0]], [[1.0]])
