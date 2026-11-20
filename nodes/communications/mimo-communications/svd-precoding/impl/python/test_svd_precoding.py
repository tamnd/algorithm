# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svd-precoding/. The authors are listed in prov/8XKR8Q.jsonl.

import math
import random

import cbb
from svd_precoding import logdet_rate, rate, receive, svd, svd_precode, water_fill


def rand_h(rng: random.Random, m: int, n: int) -> list[list[complex]]:
    return [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]


def max_abs(a: list[list[complex]]) -> float:
    return max(abs(x) for row in a for x in row)


def test_svd_reconstructs_the_matrix() -> None:
    rng = random.Random(1)
    for m, n in [(2, 2), (3, 2), (2, 3), (4, 4), (8, 5), (3, 8)]:
        for _ in range(5):
            a = rand_h(rng, m, n)
            u, s, v = svd(a)
            assert all(s[i] >= s[i + 1] for i in range(n - 1))
            us = [[u[i][k] * s[k] for k in range(n)] for i in range(m)]
            back = cbb.matmul(us, cbb.herm(v))
            assert max_abs(cbb.sub(back, a)) < 1e-10
            vhv = cbb.matmul(cbb.herm(v), v)
            assert max_abs(cbb.sub(vhv, cbb.eye(n))) < 1e-10
            r = min(m, n)
            ur = [row[:r] for row in u]
            assert max_abs(cbb.sub(cbb.matmul(cbb.herm(ur), ur), cbb.eye(r))) < 1e-10


def test_svd_singular_values_match_eigenvalues_of_gram() -> None:
    # For a 2 by 2 matrix the squared singular values are the roots of t^2 - tr t + det = 0.
    rng = random.Random(2)
    for _ in range(20):
        a = rand_h(rng, 2, 2)
        g = cbb.matmul(cbb.herm(a), a)
        tr = (g[0][0] + g[1][1]).real
        dt = cbb.det(g).real
        disc = math.sqrt(max(tr * tr - 4 * dt, 0.0))
        _, s, _ = svd(a)
        assert abs(s[0] ** 2 - (tr + disc) / 2) < 1e-10
        assert abs(s[1] ** 2 - (tr - disc) / 2) < 1e-10


def test_water_fill_check_value() -> None:
    p = water_fill([1.0, 0.5, 0.25], 3.0)
    assert max(abs(a - b) for a, b in zip(p, [2.0, 1.0, 0.0])) < 1e-12
    r = sum(math.log2(1 + g * q) for g, q in zip([1.0, 0.5, 0.25], p))
    assert abs(r - 2.1699) < 5e-5


def test_water_fill_kkt() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 8)
        g = [rng.uniform(0.01, 10.0) for _ in range(n)]
        pt = rng.uniform(0.01, 20.0)
        p = water_fill(g, pt)
        assert abs(sum(p) - pt) < 1e-9
        assert min(p) >= 0.0
        on = [i for i in range(n) if p[i] > 0]
        mu = p[on[0]] + 1 / g[on[0]]
        for i in range(n):
            if p[i] > 0:
                assert abs(p[i] + 1 / g[i] - mu) < 1e-9
            else:
                assert 1 / g[i] >= mu - 1e-9


def test_identity_check_value() -> None:
    h = cbb.eye(2)
    f, u, s, p = svd_precode(h, 10.0, 1.0)
    assert abs(rate(s, p, 1.0) - 5.1699) < 5e-5
    assert abs(cbb.norm2(f) - 10.0) < 1e-9


def test_worked_example() -> None:
    h = [[2, 1], [1, 2]]
    f, u, s, p = svd_precode(h, 2.0, 1.0)
    assert abs(s[0] - 3) < 1e-12 and abs(s[1] - 1) < 1e-12
    assert abs(p[0] - 13 / 9) < 1e-12 and abs(p[1] - 5 / 9) < 1e-12
    assert abs(rate(s, p, 1.0) - math.log2(14 * 14 / 9)) < 1e-12
    assert abs(rate(s, p, 1.0) - 4.4448) < 5e-5


def test_precoder_diagonalizes_and_meets_power() -> None:
    rng = random.Random(4)
    for m, n in [(2, 2), (4, 2), (2, 4), (4, 4), (8, 8)]:
        for _ in range(3):
            h = rand_h(rng, m, n)
            pt, n0 = rng.uniform(0.5, 20.0), rng.uniform(0.1, 2.0)
            f, u, s, p = svd_precode(h, pt, n0)
            assert abs(cbb.norm2(f) - pt) < 1e-9
            d = cbb.matmul(cbb.herm(u), cbb.matmul(h, f))
            r = len(s)
            for i in range(r):
                for k in range(r):
                    want = s[i] * math.sqrt(p[i]) if i == k else 0.0
                    assert abs(d[i][k] - want) < 1e-9
            q = cbb.matmul(f, cbb.herm(f))
            assert abs(rate(s, p, n0) - logdet_rate(h, q, n0)) < 1e-9


def test_receiver_recovers_streams_without_noise() -> None:
    rng = random.Random(5)
    h = rand_h(rng, 3, 3)
    f, u, s, p = svd_precode(h, 3.0, 0.01)
    d = [complex(rng.choice([-1, 1]), rng.choice([-1, 1])) for _ in range(len(s))]
    z = receive(cbb.matvec(h, cbb.matvec(f, d)), u)
    for i in range(len(s)):
        if p[i] > 0:
            assert abs(z[i] / (s[i] * math.sqrt(p[i])) - d[i]) < 1e-9


def random_cov(rng: random.Random, n: int, pt: float) -> list[list[complex]]:
    a = rand_h(rng, n, n)
    q = cbb.matmul(a, cbb.herm(a))
    tr = sum(q[i][i].real for i in range(n))
    return cbb.scale(pt / tr, q)


def test_beats_random_covariances() -> None:
    # The SVD precoder reaches the capacity, so no input covariance of trace P does better.
    rng = random.Random(6)
    for _ in range(10):
        h = rand_h(rng, 3, 3)
        f, u, s, p = svd_precode(h, 5.0, 1.0)
        best = rate(s, p, 1.0)
        for _ in range(40):
            assert logdet_rate(h, random_cov(rng, 3, 5.0), 1.0) <= best + 1e-9


def test_power_split_grid() -> None:
    # Two eigenmodes: the water-filling split beats every split on a fine grid.
    rng = random.Random(7)
    for _ in range(10):
        h = rand_h(rng, 2, 2)
        pt, n0 = rng.uniform(0.1, 10.0), 1.0
        f, u, s, p = svd_precode(h, pt, n0)
        best = rate(s, p, n0)
        grid = max(rate(s, [pt * t / 2000, pt * (1 - t / 2000)], n0) for t in range(2001))
        assert best >= grid - 1e-12
        assert best - grid < 1e-5
