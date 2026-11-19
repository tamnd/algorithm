# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/additive-attention/. The authors are listed in prov/3X7CGK.jsonl.

import math
import random

import pytest

from additive_attention import additive_attention, backward, keys


def rand_mat(rng, rows, cols):
    return [[rng.uniform(-1, 1) for _ in range(cols)] for _ in range(rows)]


def rand_vec(rng, n):
    return [rng.uniform(-1, 1) for _ in range(n)]


def naive(s, H, W, U, v):
    """The formula written out with plain exp and no max shift."""
    e = []
    for h in H:
        z = [sum(W[t][i] * s[i] for i in range(len(s))) + sum(U[t][i] * h[i] for i in range(len(h)))
             for t in range(len(v))]
        e.append(sum(v[t] * math.tanh(z[t]) for t in range(len(v))))
    w = [math.exp(x) for x in e]
    alpha = [x / sum(w) for x in w]
    c = [sum(alpha[j] * H[j][t] for j in range(len(H))) for t in range(len(H[0]))]
    return c, alpha


def test_page_example():
    s, W, U, v = [1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [1.0, 1.0]
    H = [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]]
    c, alpha, e = additive_attention(s, H, W, U, v)
    assert abs(e[0] - math.tanh(2)) < 1e-15
    assert abs(e[1] - 2 * math.tanh(1)) < 1e-15
    assert e[2] == 0.0
    assert [round(x, 4) for x in alpha] == [0.3194, 0.5588, 0.1218]
    assert [round(x, 4) for x in c] == [0.1976, 0.5588]
    # the largest weight goes to h_2, though s . h_2 = 0 < s . h_1 = 1
    assert max(range(3), key=lambda j: alpha[j]) == 1


def test_against_naive_formula():
    rng = random.Random(1409)
    for _ in range(50):
        a, ds, dh, J = rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 6)
        s, H = rand_vec(rng, ds), [rand_vec(rng, dh) for _ in range(J)]
        W, U, v = rand_mat(rng, a, ds), rand_mat(rng, a, dh), rand_vec(rng, a)
        c, alpha, _ = additive_attention(s, H, W, U, v)
        c2, alpha2 = naive(s, H, W, U, v)
        assert all(abs(x - y) < 1e-12 for x, y in zip(alpha, alpha2))
        assert all(abs(x - y) < 1e-12 for x, y in zip(c, c2))
        assert abs(sum(alpha) - 1) < 1e-12 and min(alpha) >= 0
        c3, _, _ = additive_attention(s, H, W, U, v, K=keys(U, H))
        assert c3 == c


def test_mask_and_degenerate_cases():
    rng = random.Random(3)
    s, H = rand_vec(rng, 3), [rand_vec(rng, 2) for _ in range(4)]
    W, U, v = rand_mat(rng, 5, 3), rand_mat(rng, 5, 2), rand_vec(rng, 5)
    c, alpha, e = additive_attention(s, H, W, U, v, mask=[True, False, True, False])
    assert alpha[1] == 0.0 and alpha[3] == 0.0 and e[1] == float("-inf")
    c2, alpha2, _ = additive_attention(s, [H[0], H[2]], W, U, v)
    assert abs(alpha[0] - alpha2[0]) < 1e-15 and all(abs(x - y) < 1e-15 for x, y in zip(c, c2))
    # v = 0 gives equal weights and the mean of the encoder states
    c0, alpha0, _ = additive_attention(s, H, W, U, [0.0] * 5)
    assert alpha0 == [0.25] * 4
    assert all(abs(c0[t] - sum(h[t] for h in H) / 4) < 1e-15 for t in range(2))
    with pytest.raises(ValueError):
        additive_attention(s, H, W, U, v, mask=[False] * 4)
    # large scores do not overflow
    _, big, _ = additive_attention(s, H, W, U, [1000.0 * x for x in v])
    assert abs(sum(big) - 1) < 1e-12


def test_gradients_by_finite_differences():
    rng = random.Random(2015)
    eps = 1e-6
    for _ in range(4):
        a, ds, dh, J = 3, 2, 3, 4
        s, H = rand_vec(rng, ds), [rand_vec(rng, dh) for _ in range(J)]
        W, U, v, g = rand_mat(rng, a, ds), rand_mat(rng, a, dh), rand_vec(rng, a), rand_vec(rng, dh)
        mask = [True, True, False, True]

        def loss():
            c, _, _ = additive_attention(s, H, W, U, v, mask)
            return sum(x * y for x, y in zip(g, c))

        ds_, dH, dW, dU, dv = backward(g, s, H, W, U, v, mask)
        cells = [(s, None, i, ds_[i]) for i in range(ds)] + [(v, None, t, dv[t]) for t in range(a)]
        cells += [(W[t], None, i, dW[t][i]) for t in range(a) for i in range(ds)]
        cells += [(U[t], None, i, dU[t][i]) for t in range(a) for i in range(dh)]
        cells += [(H[j], None, i, dH[j][i]) for j in range(J) for i in range(dh)]
        for vec, _, i, grad in cells:
            old = vec[i]
            vec[i] = old + eps
            up = loss()
            vec[i] = old - eps
            down = loss()
            vec[i] = old
            assert abs((up - down) / (2 * eps) - grad) < 1e-6
