# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiplicative-attention/. The authors are listed in prov/E826M9.jsonl.

import math
import random

import pytest

from multiplicative_attention import aligned_position, attention, attentional_state, backward_general, step


def rand_mat(rng, rows, cols):
    return [[rng.uniform(-1, 1) for _ in range(cols)] for _ in range(rows)]


def rand_vec(rng, n):
    return [rng.uniform(-1, 1) for _ in range(n)]


def eye(n, scale=1.0):
    return [[scale if i == j else 0.0 for j in range(n)] for i in range(n)]


def scaled_dot_product(q, K, V):
    """softmax(q K^T / sqrt(d)) V for one query, with plain exp."""
    d = len(q)
    e = [math.exp(sum(x * y for x, y in zip(q, k)) / math.sqrt(d)) for k in K]
    z = sum(e)
    return [sum(e[j] / z * V[j][i] for j in range(len(K))) for i in range(len(V[0]))]


def test_page_example():
    ht, Hs = [1.0, 0.0], [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]]
    c, a, _ = attention(ht, Hs, "dot")
    assert [round(x, 4) for x in a] == [0.6652, 0.2447, 0.0900]
    assert [round(x, 4) for x in c] == [0.5752, 0.2447]


def test_dot_general_and_scaled():
    rng = random.Random(1508)
    for _ in range(40):
        d, S = rng.randint(1, 5), rng.randint(1, 6)
        ht, Hs = rand_vec(rng, d), [rand_vec(rng, d) for _ in range(S)]
        c1, a1, _ = attention(ht, Hs, "dot")
        c2, a2, _ = attention(ht, Hs, "general", eye(d))
        assert all(abs(x - y) < 1e-14 for x, y in zip(a1 + c1, a2 + c2))
        # general with W_a = I / sqrt(d) is scaled dot-product attention with keys = values = Hs
        c3, a3, _ = attention(ht, Hs, "general", eye(d, 1 / math.sqrt(d)))
        want = scaled_dot_product(ht, Hs, Hs)
        assert all(abs(x - y) < 1e-12 for x, y in zip(c3, want))
        assert abs(sum(a1) - 1) < 1e-12 and min(a1) >= 0


def test_concat_is_additive_form():
    rng = random.Random(7)
    d, S, n = 3, 4, 5
    ht, Hs = rand_vec(rng, d), [rand_vec(rng, d) for _ in range(S)]
    Wa, va = rand_mat(rng, n, 2 * d), rand_vec(rng, n)
    _, a, _ = attention(ht, Hs, "concat", Wa, va)
    e = []
    for hs in Hs:
        z = [sum(Wa[r][i] * ht[i] for i in range(d)) + sum(Wa[r][d + i] * hs[i] for i in range(d))
             for r in range(n)]
        e.append(sum(va[r] * math.tanh(z[r]) for r in range(n)))
    z = sum(math.exp(x) for x in e)
    assert all(abs(x - math.exp(y) / z) < 1e-12 for x, y in zip(a, e))


def test_local_m_window():
    rng = random.Random(11)
    S, d = 30, 2
    ht, Hs = rand_vec(rng, d), [rand_vec(rng, d) for _ in range(S)]
    _, a, p = attention(ht, Hs, "dot", local="m", t=15, D=10)
    assert p == 15.0
    assert all(a[s - 1] == 0.0 for s in range(1, S + 1) if abs(s - 15) > 10)
    assert sum(1 for x in a if x > 0) == 21
    assert abs(sum(a) - 1) < 1e-12
    # near the start the window is cut at position 1
    _, a2, _ = attention(ht, Hs, "dot", local="m", t=2, D=10)
    assert sum(1 for x in a2 if x > 0) == 12
    # local-m with a window that covers everything is global attention
    _, a3, _ = attention(ht, Hs, "dot", local="m", t=15, D=40)
    _, a4, _ = attention(ht, Hs, "dot")
    assert all(abs(x - y) < 1e-15 for x, y in zip(a3, a4))


def test_local_p():
    rng = random.Random(25)
    S, d = 20, 3
    ht, Hs = rand_vec(rng, d), [rand_vec(rng, d) for _ in range(S)]
    Wp, vp = rand_mat(rng, 4, d), rand_vec(rng, 4)
    _, a, p = attention(ht, Hs, "dot", local="p", D=4, Wp=Wp, vp=vp)
    assert 0 <= p <= S and p == aligned_position(ht, S, Wp, vp)
    window = [s for s in range(1, S + 1) if abs(s - p) <= 4]
    # the softmax over the window, times the Gaussian with sigma = D / 2, and not renormalized
    e = [sum(x * y for x, y in zip(ht, Hs[s - 1])) for s in window]
    z = sum(math.exp(x) for x in e)
    for s, x in zip(window, e):
        want = math.exp(x) / z * math.exp(-((s - p) ** 2) / 8)
        assert abs(a[s - 1] - want) < 1e-14
    assert sum(a) < 1


def test_errors():
    with pytest.raises(ValueError):
        attention([1.0], [], "dot")
    with pytest.raises(ValueError):
        attention([1.0], [[1.0]], "cosine")
    with pytest.raises(ValueError):
        attention([1.0], [[1.0], [2.0]], "dot", local="m", t=10, D=2)


def test_gradients_by_finite_differences():
    rng = random.Random(2015)
    eps = 1e-6
    for _ in range(4):
        d, S = 3, 4
        ht, Hs = rand_vec(rng, d), [rand_vec(rng, d) for _ in range(S)]
        Wa, Wc, g = rand_mat(rng, d, d), rand_mat(rng, d, 2 * d), rand_vec(rng, d)

        def loss():
            h, _, _ = step(ht, Hs, Wc, kind="general", Wa=Wa)
            return sum(x * y for x, y in zip(g, h))

        dht, dHs, dWa, dWc = backward_general(g, ht, Hs, Wa, Wc)
        cells = [(ht, i, dht[i]) for i in range(d)]
        cells += [(Hs[s], i, dHs[s][i]) for s in range(S) for i in range(d)]
        cells += [(Wa[i], j, dWa[i][j]) for i in range(d) for j in range(d)]
        cells += [(Wc[i], j, dWc[i][j]) for i in range(d) for j in range(2 * d)]
        for vec, i, grad in cells:
            old = vec[i]
            vec[i] = old + eps
            up = loss()
            vec[i] = old - eps
            down = loss()
            vec[i] = old
            assert abs((up - down) / (2 * eps) - grad) < 1e-6


def test_attentional_state_shape():
    h = attentional_state([0.0, 0.0], [0.0, 0.0], [[1.0] * 4, [0.5] * 4, [0.0] * 4])
    assert h == [0.0, 0.0, 0.0]
