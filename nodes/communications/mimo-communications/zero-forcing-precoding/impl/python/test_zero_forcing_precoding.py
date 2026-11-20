# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-forcing-precoding/. The authors are listed in prov/3A1WH4.jsonl.

import math
import random

import cbb
from zero_forcing_precoding import sinr, sum_rate, water_fill, zf_precoder


def rand_h(rng: random.Random, k: int, m: int) -> list[list[complex]]:
    return [[cbb.cn(rng, 1.0) for _ in range(m)] for _ in range(k)]


def test_example() -> None:
    h = [[2, 1], [1, 1]]
    w, q, c = zf_precoder(h, 10.0, 1.0)
    assert max(abs(a - b) for a, b in zip(c, [2.0, 5.0])) < 1e-12
    assert max(abs(a - b) for a, b in zip(q, [6.5, 3.5])) < 1e-12
    s = sinr(h, w, 1.0)
    assert abs(s[0] - 3.25) < 1e-12 and abs(s[1] - 0.7) < 1e-12
    assert abs(sum_rate(h, w, 1.0) - math.log2(4.25 * 1.7)) < 1e-12
    assert abs(sum_rate(h, w, 1.0) - 2.853) < 5e-4
    w, _, _ = zf_precoder(h, 10.0, 1.0, "equal")
    assert abs(sum_rate(h, w, 1.0) - math.log2(3.5 * 2)) < 1e-12
    w, _, _ = zf_precoder(h, 10.0, 1.0, "inversion")
    assert abs(sum_rate(h, w, 1.0) - 2 * math.log2(1 + 10 / 7)) < 1e-12
    assert abs(sum_rate(h, w, 1.0) - 2.560) < 5e-4


def test_zero_interference_and_power() -> None:
    rng = random.Random(1)
    for k, m in [(1, 1), (2, 2), (2, 4), (3, 3), (4, 8), (8, 8)]:
        for mode in ("waterfill", "equal", "inversion"):
            h = rand_h(rng, k, m)
            pt, n0 = rng.uniform(0.5, 50.0), rng.uniform(0.1, 2.0)
            w, q, c = zf_precoder(h, pt, n0, mode)
            assert abs(cbb.norm2(w) - pt) < 1e-9
            e = cbb.matmul(h, w)
            for i in range(k):
                for j in range(k):
                    if i != j:
                        assert abs(e[i][j]) < 1e-9
                assert abs(abs(e[i][i]) ** 2 - q[i] / c[i]) < 1e-9 * max(1.0, q[i] / c[i])
            if mode == "inversion":
                s = sinr(h, w, n0)
                assert max(s) - min(s) < 1e-9 * max(s)


def test_noise_gain_is_diagonal_of_inverse() -> None:
    rng = random.Random(2)
    h = rand_h(rng, 3, 5)
    _, _, c = zf_precoder(h, 1.0, 1.0)
    g_inv = cbb.inv(cbb.matmul(h, cbb.herm(h)))
    for k in range(3):
        assert abs(c[k] - g_inv[k][k].real) < 1e-10


def test_pseudoinverse_columns_have_minimum_norm() -> None:
    # Any other column with h_k^H w = 1 and h_j^H w = 0 for j != k is b_k plus a null space vector, and is longer.
    rng = random.Random(3)
    h = rand_h(rng, 2, 5)
    w, q, c = zf_precoder(h, 2.0, 1.0, "equal")
    b0 = [w[i][0] / math.sqrt(q[0] / c[0]) for i in range(5)]
    hh = cbb.herm(h)
    pinv_h = cbb.matmul(hh, cbb.inv(cbb.matmul(h, hh)))
    proj = cbb.sub(cbb.eye(5), cbb.matmul(pinv_h, h))
    for _ in range(50):
        z = [cbb.cn(rng, 1.0) for _ in range(5)]
        other = cbb.add(b0, cbb.matvec(proj, z))
        hv = cbb.matvec(h, other)
        assert abs(hv[0] - 1) < 1e-9 and abs(hv[1]) < 1e-9
        assert cbb.norm2(other) >= c[0] - 1e-9


def test_water_fill_kkt() -> None:
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(1, 8)
        g = [rng.uniform(0.01, 10.0) for _ in range(n)]
        pt = rng.uniform(0.01, 20.0)
        p = water_fill(g, pt)
        assert abs(sum(p) - pt) < 1e-9 and min(p) >= 0.0
        mu = max(p[i] + 1 / g[i] for i in range(n) if p[i] > 0)
        for i in range(n):
            if p[i] > 0:
                assert abs(p[i] + 1 / g[i] - mu) < 1e-9
            else:
                assert 1 / g[i] >= mu - 1e-9


def test_power_split_grid_two_and_three_users() -> None:
    # With the ZF beams fixed, water-filling beats every power split on a grid.
    rng = random.Random(5)
    for k in (2, 3):
        for _ in range(4):
            h = rand_h(rng, k, 4)
            pt, n0 = rng.uniform(1.0, 20.0), 1.0
            w, q, c = zf_precoder(h, pt, n0)
            best = sum_rate(h, w, n0)
            steps = 400 if k == 2 else 60
            grid = 0.0
            for i in range(steps + 1):
                for j in range(steps + 1 - i if k == 3 else 1):
                    if k == 2:
                        split = [pt * i / steps, pt * (1 - i / steps)]
                    else:
                        split = [pt * i / steps, pt * j / steps, pt * (steps - i - j) / steps]
                    r = sum(math.log2(1 + s / (ck * n0)) for s, ck in zip(split, c))
                    grid = max(grid, r)
            assert best >= grid - 1e-12
            assert best - grid < 1e-2


def test_mean_snr_gain_in_rayleigh_fading() -> None:
    # 1 / c_k is Gamma with shape M - K + 1 and scale 1 in i.i.d. CN(0, 1) fading.
    rng = random.Random(6)
    for k, m in [(2, 2), (2, 4), (3, 6)]:
        t = 1000
        acc = acc2 = 0.0
        for _ in range(t):
            _, _, c = zf_precoder(rand_h(rng, k, m), 1.0, 1.0, "equal")
            acc += 1 / c[0]
            acc2 += (1 / c[0]) ** 2
        mean = acc / t
        shape = m - k + 1
        assert abs(mean - shape) < 5 * math.sqrt(shape / t)
        # The Gamma variance equals its shape.
        assert abs(acc2 / t - mean * mean - shape) < 0.4 * shape


def test_orthogonal_channels_give_matched_beams() -> None:
    h = [[2, 0, 0], [0, 0, 1j]]
    w, q, c = zf_precoder(h, 2.0, 1.0, "equal")
    # Column k is parallel to h_k: |h_k^H w_k|^2 = ||h_k||^2 ||w_k||^2.
    for k in range(2):
        col = [w[i][k] for i in range(3)]
        hk = [complex(v).conjugate() for v in h[k]]
        assert abs(abs(cbb.dot(hk, col)) ** 2 - cbb.norm2(hk) * cbb.norm2(col)) < 1e-12
