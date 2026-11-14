# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beso-method/. The authors are listed in prov/0GMFJK.jsonl.

import random
from fractions import Fraction as F

from beso_method import Network, beso, brute_force, parallel_bars, sensitivities, series_bars, solve

XMIN = F(1, 1000)


def test_parallel_bars_closed_form() -> None:
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(1, 6)
        lengths = [F(rng.randint(1, 20), rng.randint(1, 4)) for _ in range(n)]
        areas = [F(rng.randint(1, 9), rng.randint(1, 3)) for _ in range(n)]
        u, c = solve(parallel_bars(lengths, areas, 3), [F(1)] * n, 3)
        k = sum(a / L for L, a in zip(lengths, areas))
        assert u[1] == 3 / k  # delta = F / sum(E A_i / L_i)
        assert c == 9 / k  # compliance F^2 / sum(E A_i / L_i)


def test_series_bars_closed_form() -> None:
    rng = random.Random(2)
    for _ in range(50):
        n = rng.randint(1, 6)
        lengths = [F(rng.randint(1, 20), rng.randint(1, 4)) for _ in range(n)]
        areas = [F(rng.randint(1, 9), rng.randint(1, 3)) for _ in range(n)]
        _, c = solve(series_bars(lengths, areas, 2), [F(1)] * n, 3)
        assert c == 4 * sum(L / a for L, a in zip(lengths, areas))  # springs in series


def test_sensitivity_is_minus_one_over_p_times_the_derivative() -> None:
    # alpha_e v_e = -(1/p) dC/dx_e, with dC/dx_e = -p x^(p-1) u_e^T k0 u_e / 2 for C = f^T u / 2.
    # Check against a central difference quotient on a small network, exactly in Fraction.
    net = Network(3, [(0, 1, 2, 1), (1, 2, 1, 2), (0, 2, 3, 1), (0, 1, 1, 1)], [0], {2: 1})
    x = [F(1), F(1, 2), F(3, 4), F(1, 5)]
    p = 3
    u, _ = solve(net, x, p)
    alpha = sensitivities(net, x, u, p)
    h = F(1, 10**6)
    for e in range(4):
        xp, xm = list(x), list(x)
        xp[e] += h
        xm[e] -= h
        dc = (solve(net, xp, p)[1] - solve(net, xm, p)[1]) / (2 * h)  # d(f^T u)/dx_e
        want = -dc / 2 / p  # -(1/p) dC/dx_e with C = f^T u / 2
        assert abs(alpha[e] * net.volume(e) - want) < F(1, 10**8)


def test_equal_areas_keep_the_shortest_bars_which_is_optimal() -> None:
    net = parallel_bars([1, 2, 3, 4, 5, 6], [1] * 6)
    x, hist = beso(net, 10, er=F(1, 10))
    assert [int(v == 1) for v in x] == [1, 1, 1, 1, 0, 0]
    assert hist[-1][1] == 10
    c, mask = brute_force(net, 10)
    assert mask == 0b001111 and hist[-1][2] == c


def test_equal_areas_random_lengths() -> None:
    rng = random.Random(4)
    for _ in range(20):
        lengths = [F(rng.randint(1, 30), 3) for _ in range(rng.randint(2, 7))]
        net = parallel_bars(lengths, [1] * len(lengths))
        target = sum(lengths) * F(rng.randint(2, 8), 10)
        x, hist = beso(net, target)
        c, mask = brute_force(net, target)
        assert hist[-1][2] == c  # the shortest-first prefix is optimal


def test_unequal_areas_are_a_knapsack_where_beso_is_worse() -> None:
    # bar 1: L = 1, A = 1 (stiffness 1, volume 1); bar 2: L = 11/10, A = 10 (stiffness 100/11, volume 11)
    net = parallel_bars([1, F(11, 10)], [1, 10])
    x, hist = beso(net, 11)
    assert [int(v == 1) for v in x] == [1, 0]
    c, mask = brute_force(net, 11)
    assert mask == 0b10
    assert hist[-1][2] > 9 * c  # BESO keeps the bar with the higher energy density, 9 times softer


def random_net(rng):
    pos = [0, 2, 4, 6]
    bars = []
    for _ in range(rng.randint(4, 7)):
        i, j = sorted(rng.sample(range(4), 2))
        bars.append((i, j, pos[j] - pos[i], rng.randint(1, 3)))
    for i in range(3):
        bars.append((i, i + 1, 2, 1))
    return Network(4, bars, [0], {3: 1})


def test_random_networks_feasible_and_not_better_than_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(25):
        net = random_net(rng)
        total = sum(net.volume(e) for e in range(len(net.bars)))
        x, hist = beso(net, total / 2)
        vol = sum(net.volume(e) for e in range(len(net.bars)) if x[e] == 1)
        assert vol <= total / 2
        assert solve(net, x, 3)[1] == hist[-1][2]
        best, _ = brute_force(net, total / 2)
        assert hist[-1][2] >= best
        assert hist[-1][2] <= 4 * best  # measured: at most 3 times worse on this set


def test_volume_schedule() -> None:
    net = parallel_bars([1, 2, 3, 4, 5, 6], [1] * 6)
    _, hist = beso(net, 10, er=F(1, 10))
    targets = [h[0] for h in hist]
    assert targets[:3] == [21, F(189, 10), F(1701, 100)]
    assert all(a >= b for a, b in zip(targets, targets[1:]))
    assert targets[-1] == 10
    assert all(h[1] <= h[0] for h in hist)
