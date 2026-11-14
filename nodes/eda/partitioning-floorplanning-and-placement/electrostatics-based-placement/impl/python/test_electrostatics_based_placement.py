# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/electrostatics-based-placement/. The authors are listed in prov/KESX1E.jsonl.

import math
import random

from electrostatics_based_placement import (
    bin_density,
    dct2,
    eplace,
    lse_wirelength,
    overflow,
    potential_and_field,
    psi_at,
)


def random_rho(rng, M):
    return [[rng.choice([0.0, 0.25, 0.5, 1.0, 1.5, 2.0]) for _ in range(M)] for _ in range(M)]


def test_bin_density_against_a_direct_sum():
    rng = random.Random(1)
    for _ in range(80):
        M, B = 4, 2.0
        n = rng.randint(1, 7)
        W = [rng.choice([0.5, 1.0, 1.5, 3.0]) for _ in range(n)]
        H = [rng.choice([0.5, 1.0, 2.0]) for _ in range(n)]
        x = [rng.randint(0, 32) / 4 for _ in range(n)]  # multiples of 1/4: the float sums are exact
        y = [rng.randint(0, 32) / 4 for _ in range(n)]
        rho = bin_density(x, y, W, H, M, B)
        for u in range(M):
            for v in range(M):
                direct = 0.0
                for i in range(n):
                    ox = max(0.0, min(x[i] + W[i] / 2, (u + 1) * B) - max(x[i] - W[i] / 2, u * B))
                    oy = max(0.0, min(y[i] + H[i] / 2, (v + 1) * B) - max(y[i] - H[i] / 2, v * B))
                    direct += ox * oy
                assert rho[u][v] == direct / (B * B)


def test_dct_matches_the_direct_formula_and_inverts():
    rng = random.Random(2)
    for M in (1, 2, 3, 5, 8):
        rho = random_rho(rng, M)
        a = dct2(rho)
        for u in range(M):
            for v in range(M):
                cu = (1 if u == 0 else 2) / M
                cv = (1 if v == 0 else 2) / M
                direct = cu * cv * sum(rho[x][y] * math.cos(math.pi * u * (x + 0.5) / M) * math.cos(math.pi * v * (y + 0.5) / M)
                                       for x in range(M) for y in range(M))
                assert abs(a[u][v] - direct) < 1e-12
        for x in range(M):
            for y in range(M):
                back = sum(a[u][v] * math.cos(math.pi * u * (x + 0.5) / M) * math.cos(math.pi * v * (y + 0.5) / M)
                           for u in range(M) for v in range(M))
                assert abs(back - rho[x][y]) < 1e-12
        assert abs(a[0][0] - sum(map(sum, rho)) / (M * M)) < 1e-12


def test_potential_solves_the_poisson_equation_at_the_bin_centers():
    rng = random.Random(3)
    h = 1e-3
    for M in (4, 6):
        rho = random_rho(rng, M)
        mean = sum(map(sum, rho)) / (M * M)
        a, psi, _, _ = potential_and_field(rho, 1.0)
        for x in range(M):
            for y in range(M):
                tx, ty = x + 0.5, y + 0.5
                assert abs(psi_at(a, tx, ty) - psi[x][y]) < 1e-12
                lap = (psi_at(a, tx + h, ty) + psi_at(a, tx - h, ty) + psi_at(a, tx, ty + h)
                       + psi_at(a, tx, ty - h) - 4 * psi_at(a, tx, ty)) / (h * h)
                assert abs(-lap - (rho[x][y] - mean)) < 1e-4


def test_field_is_minus_the_gradient_and_vanishes_on_the_border():
    rng = random.Random(4)
    h = 1e-5
    M, B = 5, 2.0
    rho = random_rho(rng, M)
    a, _, ex, ey = potential_and_field(rho, B)
    for x in range(M):
        for y in range(M):
            tx, ty = x + 0.5, y + 0.5
            dx = (psi_at(a, tx + h, ty) - psi_at(a, tx - h, ty)) / (2 * h) / B
            dy = (psi_at(a, tx, ty + h) - psi_at(a, tx, ty - h)) / (2 * h) / B
            assert abs(ex[x][y] + dx) < 1e-6 and abs(ey[x][y] + dy) < 1e-6
    for t in (0.3, 1.7, 4.2):
        for edge in (0.0, float(M)):
            assert abs(psi_at(a, edge + h, t) - psi_at(a, edge - h, t)) / (2 * h) < 1e-8
            assert abs(psi_at(a, t, edge + h) - psi_at(a, t, edge - h)) / (2 * h) < 1e-8


def test_uniform_density_has_no_field():
    _, psi, ex, ey = potential_and_field([[0.7] * 4 for _ in range(4)], 1.0)
    assert all(abs(v) < 1e-12 for grid in (psi, ex, ey) for row in grid for v in row)


def test_lse_gradient_against_finite_differences():
    rng = random.Random(5)
    h = 1e-6
    for _ in range(30):
        n = rng.randint(1, 5)
        pads = [(rng.uniform(0, 8), rng.uniform(0, 8)) for _ in range(2)]
        nets = [rng.sample(range(n + 2), rng.randint(2, min(4, n + 2))) for _ in range(rng.randint(1, 6))]
        weights = [rng.randint(1, 3) for _ in nets]
        x = [rng.uniform(0, 8) for _ in range(n)]
        y = [rng.uniform(0, 8) for _ in range(n)]
        gamma = rng.choice([0.25, 1.0, 2.0])
        _, gx, gy = lse_wirelength(x, y, nets, weights, pads, gamma)
        for i in range(n):
            for coord, g in ((x, gx), (y, gy)):
                coord[i] += h
                up = lse_wirelength(x, y, nets, weights, pads, gamma)[0]
                coord[i] -= 2 * h
                down = lse_wirelength(x, y, nets, weights, pads, gamma)[0]
                coord[i] += h
                assert abs((up - down) / (2 * h) - g[i]) < 1e-5


def test_placer_spreads_cells_on_fixed_seeds():
    rng = random.Random(14)
    for k in range(4):
        n, M, B = 24, 8, 1.0
        q = 6
        pads = [(0.0, rng.uniform(0, 8)), (8.0, rng.uniform(0, 8)), (rng.uniform(0, 8), 0.0),
                (rng.uniform(0, 8), 8.0), (0.0, rng.uniform(0, 8)), (8.0, rng.uniform(0, 8))]
        nets = [[i, n + rng.randrange(q)] if i == 0 or rng.random() < 0.3 else [i, rng.randrange(i)] for i in range(n)]
        nets += [rng.sample(range(n + q), rng.randint(2, 3)) for _ in range(n)]
        r2 = random.Random(k)
        start = [(4 + r2.uniform(-0.1, 0.1), 4 + r2.uniform(-0.1, 0.1)) for _ in range(n)]
        hist = []
        x, y = eplace(n, nets, pads, [1.0] * n, [1.0] * n, M, B, start=start, history=hist, max_iter=200)
        assert hist[0][0] > 0.5 and hist[-1][0] <= 0.1
        assert overflow(bin_density(x, y, [1.0] * n, [1.0] * n, M, B), n, B) <= 0.1
        assert all(0.5 <= v <= 7.5 for v in x + y)
