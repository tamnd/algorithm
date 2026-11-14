# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-directed-placement/. The authors are listed in prov/82M4RX.jsonl.

import random
from fractions import Fraction

from force_directed_placement import bin_density, energy, force_directed, overflow, springs


def gauss_solve(M, b):
    """Reference: Gaussian elimination with Fractions on a dense matrix."""
    n = len(b)
    a = [list(M[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def random_instance(rng, n, q, extra, lo=1, hi=9):
    pads = [(rng.randint(lo, hi), rng.randint(lo, hi)) for _ in range(q)]
    nets = []
    for i in range(n):  # a net to a pad or to an earlier cell, so every cell is tied to a pad
        nets.append([i, n + rng.randrange(q)] if i == 0 or rng.random() < 0.3 else [i, rng.randrange(i)])
    for _ in range(extra):
        nets.append(rng.sample(range(n + q), min(n + q, rng.randint(2, 3))))
    weights = [rng.randint(1, 3) for _ in nets]
    return nets, pads, weights


def test_relaxation_converges_to_the_gauss_solution():
    rng = random.Random(1979)
    for _ in range(30):
        n = rng.randint(1, 6)
        nets, pads, weights = random_instance(rng, n, rng.randint(1, 3), rng.randint(0, 5))
        adj = springs(n, nets, weights)
        A = [[Fraction(0)] * n for _ in range(n)]
        bx, by = [Fraction(0)] * n, [Fraction(0)] * n
        for i in range(n):
            for j, w in adj[i].items():
                A[i][i] += w
                if j < n:
                    A[i][j] -= w
                else:
                    bx[i] += w * pads[j - n][0]
                    by[i] += w * pads[j - n][1]
        ex, ey = gauss_solve(A, bx), gauss_solve(A, by)
        start = [(5.0, 5.0)] * n
        x, y = force_directed(n, nets, pads, [1] * n, [1] * n, 10, 10, 2, rounds=1, sweeps=400,
                              kappa=0, weights=weights, start=start)
        for i in range(n):
            assert abs(x[i] - ex[i]) < 1e-9 and abs(y[i] - ey[i]) < 1e-9


def test_energy_never_increases_inside_a_round_exact():
    rng = random.Random(82)
    for _ in range(12):
        n = rng.randint(2, 4)
        nets, pads, weights = random_instance(rng, n, 2, 2, lo=0, hi=8)
        rounds, sweeps = 3, 2
        trace = []
        force_directed(n, nets, pads, [1] * n, [1] * n, 8, 8, 2, rounds=rounds, sweeps=sweeps,
                       kappa=Fraction(1, 2), weights=weights, start=[(4, 4)] * n, trace=trace)
        per_round = sweeps * n
        assert len(trace) == rounds * per_round
        for r in range(rounds):
            part = trace[r * per_round:(r + 1) * per_round]
            assert all(a >= b for a, b in zip(part, part[1:]))


def test_one_move_is_the_exact_minimum_along_its_coordinate():
    rng = random.Random(4)
    for _ in range(40):
        n = rng.randint(1, 4)
        nets, pads, weights = random_instance(rng, n, 2, 2)
        adj = springs(n, nets, weights)
        x = [Fraction(rng.randint(1, 9)) for _ in range(n)]
        y = [Fraction(rng.randint(1, 9)) for _ in range(n)]
        ex = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        ey = [Fraction(0)] * n
        i = rng.randrange(n)
        deg = sum(adj[i].values())
        t = (sum(w * (x[j] if j < n else pads[j - n][0]) for j, w in adj[i].items()) + ex[i]) / deg
        x[i] = t
        best = energy(x, y, adj, pads, ex, ey)
        for d in (Fraction(1, 7), Fraction(-1, 3), Fraction(2)):
            x[i] = t + d
            assert energy(x, y, adj, pads, ex, ey) > best


def test_bin_density_against_a_direct_sum():
    rng = random.Random(7)
    for _ in range(60):
        X, Y, B = 8, 6, 2
        n = rng.randint(1, 8)
        W = [rng.randint(1, 3) for _ in range(n)]
        H = [rng.randint(1, 2) for _ in range(n)]
        x = [Fraction(rng.randint(0, 4 * X), 4) for _ in range(n)]
        y = [Fraction(rng.randint(0, 4 * Y), 4) for _ in range(n)]
        D = bin_density(x, y, W, H, X, Y, B)
        for u in range(X // B):
            for v in range(Y // B):
                direct = Fraction(0)
                for i in range(n):
                    ox = max(0, min(x[i] + Fraction(W[i], 2), (u + 1) * B) - max(x[i] - Fraction(W[i], 2), u * B))
                    oy = max(0, min(y[i] + Fraction(H[i], 2), (v + 1) * B) - max(y[i] - Fraction(H[i], 2), v * B))
                    direct += ox * oy
                assert D[u][v] == direct / (B * B)
        inside = sum(max(0, min(x[i] + Fraction(W[i], 2), X) - max(x[i] - Fraction(W[i], 2), 0))
                     * max(0, min(y[i] + Fraction(H[i], 2), Y) - max(y[i] - Fraction(H[i], 2), 0)) for i in range(n))
        assert sum(sum(col) for col in D) * B * B == inside


def test_page_example():
    # pads P = (0, 1) and Q = (6, 1); cells a, b; nets {P, a}, {a, b}, {b, Q}
    nets = [[2, 0], [0, 1], [1, 3]]
    pads = [(0, 1), (6, 1)]
    trace = []
    x, y = force_directed(2, nets, pads, [1, 1], [1, 1], 6, 2, 2, rounds=1, sweeps=3,
                          kappa=0, start=[(3, 1), (3, 1)], trace=trace)
    assert trace == [Fraction(27, 4), Fraction(99, 16), Fraction(387, 64),
                     Fraction(1539, 256), Fraction(6147, 1024), Fraction(24579, 4096)]
    assert x == [Fraction(63, 32), Fraction(255, 64)] and y == [1, 1]


def test_spreading_lowers_overflow_on_fixed_seeds():
    rng = random.Random(5)
    for _ in range(3):
        n = 16
        nets, pads, _ = random_instance(rng, n, 4, n, lo=0, hi=8)
        st = [(4.0, 4.0)] * n
        x0, y0 = force_directed(n, nets, pads, [1] * n, [1] * n, 8, 8, 2, rounds=1, sweeps=20, kappa=0, start=st)
        x1, y1 = force_directed(n, nets, pads, [1] * n, [1] * n, 8, 8, 2, rounds=8, sweeps=20, kappa=0.5, start=st)
        assert overflow(bin_density(x1, y1, [1] * n, [1] * n, 8, 8, 2)) < overflow(bin_density(x0, y0, [1] * n, [1] * n, 8, 8, 2))
