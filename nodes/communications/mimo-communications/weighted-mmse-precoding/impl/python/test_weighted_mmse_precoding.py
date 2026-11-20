# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-mmse-precoding/. The authors are listed in prov/9QVSR3.jsonl.

import math
import random

import cbb
from weighted_mmse_precoding import sinr, weighted_sum_rate, wmmse


def rand_h(rng: random.Random, k: int, m: int) -> list[list[complex]]:
    return [[cbb.cn(rng, 1.0) for _ in range(m)] for _ in range(k)]


def test_example() -> None:
    # Orthogonal channels with gains 4, 1 and 1/4 and weights 1, 2 and 1.5 (the example of the page).
    h = [[2, 0, 0], [0, 1, 0], [0, 0, 0.5]]
    a = [1.0, 2.0, 1.5]
    v, rates = wmmse(h, 3.0, 1.0, weights=a, iters=2000)
    p = [cbb.norm2([row[k] for row in v]) for k in range(3)]
    assert abs(p[0] - 7 / 6) < 1e-6 and abs(p[1] - 11 / 6) < 1e-6 and p[2] < 1e-6
    want = math.log2(1 + 4 * 7 / 6) + 2 * math.log2(1 + 11 / 6)
    assert abs(rates[-1] - want) < 1e-9
    assert abs(rates[0] - weighted_sum_rate(h, cbb.scale(math.sqrt(3 / 5.25), cbb.herm(h)), 1.0, a)) < 1e-12


def test_single_user_is_maximum_ratio_transmission() -> None:
    rng = random.Random(1)
    for m in (1, 3, 8):
        h = rand_h(rng, 1, m)
        v, rates = wmmse(h, 5.0, 0.5)
        assert abs(rates[-1] - math.log2(1 + 5.0 * cbb.norm2(h[0]) / 0.5)) < 1e-10
        assert abs(abs(cbb.matmul(h, v)[0][0]) ** 2 - 5.0 * cbb.norm2(h[0])) < 1e-9


def test_orthogonal_channels_give_weighted_water_filling() -> None:
    # With h_k = g_k e_k, the optimum is p_k = (a_k / lam - 1 / g_k)^+ with sum P.
    rng = random.Random(2)
    for _ in range(2):
        g = [rng.uniform(0.1, 5.0) for _ in range(3)]
        a = [rng.uniform(0.5, 2.0) for _ in range(3)]
        pt = rng.uniform(0.5, 10.0)
        h = [[math.sqrt(g[k]) if i == k else 0.0 for i in range(3)] for k in range(3)]
        lo, hi = 1e-12, 1e3
        for _ in range(200):
            lam = 0.5 * (lo + hi)
            if sum(max(0.0, a[k] / lam - 1 / g[k]) for k in range(3)) > pt:
                lo = lam
            else:
                hi = lam
        p = [max(0.0, a[k] / lam - 1 / g[k]) for k in range(3)]
        want = sum(a[k] * math.log2(1 + g[k] * p[k]) for k in range(3))
        _, rates = wmmse(h, pt, 1.0, weights=a, iters=3000, tol=1e-14)
        assert abs(rates[-1] - want) < 1e-7


def test_monotone_and_power() -> None:
    rng = random.Random(3)
    for k, m in [(2, 2), (3, 4), (4, 4), (3, 6), (8, 8)]:
        h = rand_h(rng, k, m)
        a = [rng.uniform(0.5, 2.0) for _ in range(k)]
        pt = rng.uniform(1.0, 30.0)
        v, rates = wmmse(h, pt, 1.0, weights=a, iters=15, tol=-1.0)
        assert len(rates) == 16
        for t in range(15):
            assert rates[t + 1] >= rates[t] - 1e-12
        assert cbb.norm2(v) <= pt * (1 + 1e-12)
        assert abs(cbb.norm2(v) - pt) < 1e-9 * pt


def test_kkt_at_convergence() -> None:
    # At a stationary point the gradient of the weighted sum rate is lam v for one lam >= 0.
    rng = random.Random(4)
    h = rand_h(rng, 3, 3)
    a = [1.0, 1.5, 0.7]
    v, _ = wmmse(h, 4.0, 1.0, weights=a, iters=3000, tol=1e-15)
    eps = 1e-6
    grad = [[0j] * 3 for _ in range(3)]
    for i in range(3):
        for k in range(3):
            parts = []
            for d in (eps, 1j * eps):
                vp = [row[:] for row in v]
                vm = [row[:] for row in v]
                vp[i][k] += d
                vm[i][k] -= d
                parts.append((weighted_sum_rate(h, vp, 1.0, a) - weighted_sum_rate(h, vm, 1.0, a)) / (2 * eps))
            grad[i][k] = complex(parts[0], parts[1])
    lam = sum((grad[i][k] * v[i][k].conjugate()).real for i in range(3) for k in range(3)) / cbb.norm2(v)
    assert lam > 0
    res = math.sqrt(cbb.norm2(cbb.sub(grad, cbb.scale(lam, v))))
    assert res < 1e-5 * math.sqrt(cbb.norm2(grad))


def test_grid_search_two_users() -> None:
    # For two users, the best beams have the form (I + sum_j lam_j h_j h_j^H / N0)^(-1) h_k with
    # lam_1 + lam_2 = P. A grid over lam_1 and the power split gives a lower bound on the optimum.
    # WMMSE finds a stationary point, which can be a local optimum, so the test keeps the best of 6 starts.
    rng = random.Random(5)
    for _ in range(2):
        h = rand_h(rng, 2, 2)
        a = [1.0, rng.uniform(0.5, 2.0)]
        pt, n0, n = rng.uniform(1.0, 20.0), 1.0, 60
        best = -1.0
        for start in range(6):
            v0 = None
            if start > 0:
                v0 = rand_h(rng, 2, 2)
                v0 = cbb.scale(math.sqrt(pt / cbb.norm2(v0)), v0)
            _, rates = wmmse(h, pt, n0, weights=a, v0=v0, iters=400, tol=1e-11)
            best = max(best, rates[-1])
        cols = cbb.herm(h)
        grid = 0.0
        for i in range(n + 1):
            lam = [pt * i / n, pt * (n - i) / n]
            am = [
                [(1.0 if r == c else 0.0) + sum(lam[j] * cols[r][j] * cols[c][j].conjugate() for j in range(2)) / n0 for c in range(2)]
                for r in range(2)
            ]
            d = cbb.solve(am, cols)
            d = [[d[r][k] / math.sqrt(abs(d[0][k]) ** 2 + abs(d[1][k]) ** 2) for k in range(2)] for r in range(2)]
            g = [[abs(x) ** 2 for x in row] for row in cbb.matmul(h, d)]  # g[q][k] = |h_q^H d_k|^2
            for t in range(n + 1):
                p = [pt * t / n, pt * (n - t) / n]
                s0 = g[0][0] * p[0] / (g[0][1] * p[1] + n0)
                s1 = g[1][1] * p[1] / (g[1][0] * p[0] + n0)
                grid = max(grid, a[0] * math.log2(1 + s0) + a[1] * math.log2(1 + s1))
        assert grid <= best + 1e-9
        assert best - grid < 1e-3


def test_local_optimum() -> None:
    # On this channel the default start converges to a point that serves both users,
    # while serving only user 2 is better. Both points are stationary.
    rng = random.Random(5)
    h = rand_h(rng, 2, 2)
    a = [1.0, rng.uniform(0.5, 2.0)]
    pt = rng.uniform(1.0, 20.0)
    v, rates = wmmse(h, pt, 1.0, weights=a, iters=1000, tol=1e-13)
    assert min(cbb.norm2([row[k] for row in v]) for k in range(2)) > 1.0
    v2 = [[0j, math.sqrt(pt) * complex(h[1][r]).conjugate() / math.sqrt(cbb.norm2(h[1]))] for r in range(2)]
    one_user = weighted_sum_rate(h, v2, 1.0, a)
    assert one_user > rates[-1] + 0.5


def test_sinr_formula() -> None:
    h = [[1, 0], [1, 1]]
    v = [[1, 0], [0, 2]]
    s = sinr(h, v, 0.5)
    assert abs(s[0] - 1 / 0.5) < 1e-12
    assert abs(s[1] - 4 / (1 + 0.5)) < 1e-12
