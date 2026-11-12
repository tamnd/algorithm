# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-checkpointing/. The authors are listed in prov/6X8J45.jsonl.

import math
import random

from gradient_checkpointing import backprop_checkpointed, backprop_full, layer


def chain(rng, n, d):
    Ws = [[[rng.gauss(0, 1.2 / math.sqrt(d)) for _ in range(d)] for _ in range(d)] for _ in range(n)]
    bs = [[rng.uniform(-0.2, 0.2) for _ in range(d)] for _ in range(n)]
    x0 = [rng.uniform(-1, 1) for _ in range(d)]
    return Ws, bs, x0


def loss(Ws, bs, x0):
    x = x0
    for W, b in zip(Ws, bs):
        x = layer(W, b, x)
    return 0.5 * sum(v * v for v in x)


def test_gradients_equal_full_storage_exactly():
    rng = random.Random(11)
    for n in (1, 2, 3, 7, 16, 30):
        Ws, bs, x0 = chain(rng, n, 3)
        gf, dxf, _ = backprop_full(Ws, bs, x0)
        for k in (None, 1, 2, 3, 5, n, n + 4):
            gc, dxc, _ = backprop_checkpointed(Ws, bs, x0, k)
            assert gc == gf and dxc == dxf, (n, k)


def test_full_storage_matches_central_differences():
    rng = random.Random(12)
    Ws, bs, x0 = chain(rng, 6, 2)
    grads, dx0, _ = backprop_full(Ws, bs, x0)
    h = 1e-6
    for l in range(6):
        for i in range(2):
            for j in range(2):
                Ws[l][i][j] += h
                up = loss(Ws, bs, x0)
                Ws[l][i][j] -= 2 * h
                down = loss(Ws, bs, x0)
                Ws[l][i][j] += h
                assert math.isclose(grads[l][0][i][j], (up - down) / (2 * h), rel_tol=1e-6, abs_tol=1e-9)
    for j in range(2):
        a, b = list(x0), list(x0)
        a[j] += h
        b[j] -= h
        assert math.isclose(dx0[j], (loss(Ws, bs, a) - loss(Ws, bs, b)) / (2 * h), rel_tol=1e-6, abs_tol=1e-9)


def test_memory_and_recomputation_counts():
    rng = random.Random(13)
    for n in (1, 2, 4, 9, 10, 17, 50, 100):
        Ws, bs, x0 = chain(rng, n, 2)
        _, _, full = backprop_full(Ws, bs, x0)
        assert full.peak == n and full.evals == n
        for k in (1, 2, 3, 4, 7, 10, 200):
            _, _, c = backprop_checkpointed(Ws, bs, x0, k)
            s = -(-n // k)  # the number of segments, ceil(n / k)
            assert c.peak == s + min(k, n) - 1, (n, k, c.peak)
            assert c.evals == n + (n - s), (n, k)  # one forward pass plus n - s recomputations
            assert c.live == 0


def test_sqrt_n_segments_give_sqrt_n_memory():
    rng = random.Random(14)
    for n in (16, 25, 64, 100, 99):
        Ws, bs, x0 = chain(rng, n, 2)
        _, _, c = backprop_checkpointed(Ws, bs, x0)
        r = math.isqrt(n - 1) + 1  # ceil(sqrt(n))
        assert c.peak <= 2 * r - 1
        assert c.evals <= 2 * n
        if r * r == n:
            assert c.peak == 2 * r - 1 and c.evals == 2 * n - r
