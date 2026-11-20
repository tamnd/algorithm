# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-ratio-transmission/. The authors are listed in prov/17KZND.jsonl.

import cmath
import math
import random

import cbb
from maximum_ratio_transmission import conjugate_beamforming, mrt_mimo, mrt_vector, principal_vector, sinr


def rand_vec(rng: random.Random, n: int) -> list[complex]:
    return [cbb.cn(rng, 1.0) for _ in range(n)]


def snr(h: list[complex], x: list[complex], n0: float) -> float:
    return abs(cbb.dot(h, x)) ** 2 / n0


def test_example_vector() -> None:
    h = [1 + 1j, 2, -1j]
    x = mrt_vector(h, 1.0)
    assert abs(cbb.norm2(x) - 1.0) < 1e-12
    assert abs(snr(h, x, 1.0) - 7.0) < 1e-12
    assert abs(cbb.db(7.0) - 8.451) < 5e-4
    # Antenna selection: all power on the strongest antenna, |h_2|^2 = 4.
    sel = max(abs(v) ** 2 for v in h)
    assert abs(sel - 4.0) < 1e-12
    # Equal-phase sending: x = (1, 1, 1) / sqrt(3).
    eq = [1 / math.sqrt(3)] * 3
    assert abs(snr(h, eq, 1.0) - 3.0) < 1e-12


def test_mrt_beats_every_unit_vector() -> None:
    # Cauchy-Schwarz: |h^H x|^2 <= ||h||^2 ||x||^2, with equality for x along h.
    rng = random.Random(1)
    for m in range(1, 9):
        h = rand_vec(rng, m)
        best = snr(h, mrt_vector(h, 1.0), 1.0)
        assert abs(best - cbb.norm2(h)) < 1e-10
        for _ in range(200):
            x = rand_vec(rng, m)
            x = cbb.scale(1 / math.sqrt(cbb.norm2(x)), x)
            assert snr(h, x, 1.0) <= best + 1e-10


def test_grid_search_two_antennas() -> None:
    # Every unit vector of C^2 is, up to a common phase, (cos a, sin a e^(j b)).
    rng = random.Random(2)
    for _ in range(3):
        h = rand_vec(rng, 2)
        best = cbb.norm2(h)
        grid = 0.0
        for i in range(201):
            a = math.pi / 2 * i / 200
            for k in range(200):
                b = 2 * math.pi * k / 200
                x = [math.cos(a), math.sin(a) * cmath.exp(1j * b)]
                grid = max(grid, snr(h, x, 1.0))
        assert grid <= best + 1e-12
        assert best - grid < 1e-3 * best


def test_principal_vector_example() -> None:
    lam, v = principal_vector([[1, 1], [0, 1]])
    assert abs(lam - (3 + math.sqrt(5)) / 2) < 1e-12
    assert abs(lam - 2.618) < 5e-4
    assert abs(cbb.norm2(v) - 1) < 1e-12


def test_principal_vector_when_the_largest_column_misses_it() -> None:
    # H^H H = e1 e1^T + 1.1 u u^T with u = (0, 1, 1) / sqrt(2). The largest column of
    # H^H H is e1, which is orthogonal to u, so one start from it would return 1.0.
    a = math.sqrt(0.55)
    lam, v = principal_vector([[1, 0, 0], [0, a, a]])
    assert abs(lam - 1.1) < 1e-12
    assert abs(abs(v[1]) - 1 / math.sqrt(2)) < 1e-9 and abs(v[0]) < 1e-9


def test_mimo_gain_is_top_eigenvalue() -> None:
    rng = random.Random(3)
    for m, n in [(2, 2), (3, 2), (2, 4), (4, 4)]:
        for _ in range(5):
            h = [rand_vec(rng, n) for _ in range(m)]
            x, comb, lam = mrt_mimo(h, 1.0)
            g = cbb.matmul(cbb.herm(h), h)
            gv = cbb.matvec(g, x)
            assert max(abs(a - lam * b) for a, b in zip(gv, x)) < 1e-9
            # The combined gain |c^H H x|^2 equals lambda_max.
            assert abs(abs(cbb.dot(comb, cbb.matvec(h, x))) ** 2 - lam) < 1e-9
            # No unit vector gives more: ||H x||^2 <= lambda_max.
            for _ in range(50):
                z = rand_vec(rng, n)
                z = cbb.scale(1 / math.sqrt(cbb.norm2(z)), z)
                assert cbb.norm2(cbb.matvec(h, z)) <= lam + 1e-9
            # The trace bound: lambda_max >= tr(G) / n.
            assert lam >= sum(g[i][i].real for i in range(n)) / n - 1e-9


def test_bpsk_error_rate_matches_two_branch_mrc() -> None:
    # MRT with M = 2 in i.i.d. Rayleigh fading has the same SNR law as MRC with L = 2.
    rng = random.Random(4)
    p_total, n0 = 10.0, 1.0
    mu = math.sqrt(10.0 / 11.0)
    exact = ((1 - mu) / 2) ** 2 * (1 + 2 * (1 + mu) / 2)
    assert abs(exact - 1.5991e-3) < 5e-7
    n, errors = 100000, 0
    s0 = math.sqrt(n0 / 2)
    for _ in range(n):
        h = [complex(rng.gauss(0, 0.7071067811865476), rng.gauss(0, 0.7071067811865476)) for _ in range(2)]
        nrm = math.sqrt(abs(h[0]) ** 2 + abs(h[1]) ** 2)
        s = 1.0 if rng.random() < 0.5 else -1.0
        # y = h^H x + w with x = sqrt(P) h / ||h|| s, so y = sqrt(P) ||h|| s + w.
        y = math.sqrt(p_total) * nrm * s + rng.gauss(0, s0)
        if (y >= 0) != (s > 0):
            errors += 1
    lo, hi = cbb.wilson(errors, n)
    assert lo <= exact <= hi
    assert exact * n >= 100


def test_conjugate_beamforming_power_and_orthogonal_users() -> None:
    rng = random.Random(5)
    hs = [rand_vec(rng, 8) for _ in range(4)]
    w = conjugate_beamforming(hs, 6.0)
    assert abs(cbb.norm2(w) - 6.0) < 1e-9
    # Orthogonal channels: no interference, SINR_k = (P/K) ||h_k||^2 / N0.
    hs = [[2.0, 0, 0], [0, 1j, 0], [0, 0, 1 - 1j]]
    w = conjugate_beamforming(hs, 3.0)
    got = sinr(hs, w, 0.5)
    for k in range(3):
        assert abs(got[k] - 1.0 * cbb.norm2(hs[k]) / 0.5) < 1e-12


def test_favorable_propagation_mean() -> None:
    # For independent isotropic unit vectors in C^M, E|u^H v|^2 = 1/M.
    rng = random.Random(6)
    for m in (2, 4, 8):
        t = 4000
        acc = 0.0
        for _ in range(t):
            u, v = rand_vec(rng, m), rand_vec(rng, m)
            acc += abs(cbb.dot(u, v)) ** 2 / (cbb.norm2(u) * cbb.norm2(v))
        mean = acc / t
        # |u^H v|^2 is Beta(1, M - 1), with standard deviation below 1/M.
        assert abs(mean - 1 / m) < 5 * (1 / m) / math.sqrt(t)
