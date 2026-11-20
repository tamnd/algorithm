# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-programming-power-control/. The authors are listed in prov/BD2KKJ.jsonl.

import math
import random

import pytest

from geometric_programming_power_control import (
    gp_solve,
    gp_value,
    high_sinr_rate,
    least_powers,
    max_min_sinr,
    min_total_power,
    monomial,
    sca_sum_rate,
    sinr,
    sum_rate,
)

G = [[1.0, 0.1, 0.2], [0.2, 1.0, 0.1], [0.1, 0.1, 1.0]]
NOISE = [0.1, 0.1, 0.1]
STRONG = [[1.0, 0.8], [0.9, 1.0]]


def random_case(rng: random.Random, k: int, cross: float):
    g = [[rng.uniform(0.5, 1.5) if i == j else cross * rng.random() for j in range(k)] for i in range(k)]
    noise = [rng.uniform(0.05, 0.2) for _ in range(k)]
    return g, noise


def feasible(g, noise, pmax, gmin, p, slack=1e-9):
    s = sinr(g, noise, p)
    return all(a >= b * (1 - slack) for a, b in zip(s, gmin)) and all(a <= b * (1 + slack) for a, b in zip(p, pmax))


def test_teaching_solver_on_a_textbook_gp() -> None:
    # Minimize x + y subject to 1/(x y) <= 1: the answer is x = y = 1 with value 2.
    obj = [monomial(1.0, [1.0, 0.0]) + monomial(1.0, [0.0, 1.0])]
    cons = [monomial(1.0, [-1.0, -1.0])]
    y = gp_solve(obj, cons, [1.0, 1.0])
    assert abs(math.exp(y[0]) - 1.0) < 1e-8 and abs(math.exp(y[1]) - 1.0) < 1e-8
    assert abs(math.exp(gp_value(obj, y)) - 2.0) < 1e-9
    with pytest.raises(ValueError):
        gp_solve(obj, cons, [-1.0, -1.0])


def test_min_power_is_the_foschini_miljanic_point() -> None:
    p = min_total_power(G, NOISE, [2.0] * 3, [1.0] * 3)
    assert all(abs(a - b) < 1e-9 for a, b in zip(p, [42 / 95, 43 / 95, 36 / 95]))
    rng = random.Random(1)
    done = 0
    while done < 8:
        k = rng.randint(2, 4)
        g, noise = random_case(rng, k, 0.3)
        gamma = [rng.uniform(0.5, 2.0) for _ in range(k)]
        q = least_powers(g, [1.01 * v for v in gamma], noise)
        if q is None or max(q) > 5.0:
            continue
        p = min_total_power(g, noise, gamma, [10.0] * k)
        assert all(abs(a - b) <= 1e-7 * b for a, b in zip(p, least_powers(g, gamma, noise)))
        done += 1


def bisect_max_min(g, noise, pmax):
    lo, hi = 0.0, min(g[i][i] * pmax[i] / noise[i] for i in range(len(g)))
    for _ in range(100):
        t = 0.5 * (lo + hi)
        p = least_powers(g, [t] * len(g), noise)
        if p is not None and all(a <= b for a, b in zip(p, pmax)):
            lo = t
        else:
            hi = t
    return lo


def test_max_min_matches_bisection() -> None:
    t, p = max_min_sinr([[1.0, 0.5], [0.2, 1.0]], [0.1, 0.1], [1.2, 1.2])
    assert abs(t - 2.378957121765) < 1e-7
    t, p = max_min_sinr(G, NOISE, [1.0] * 3)
    assert abs(t - bisect_max_min(G, NOISE, [1.0] * 3)) < 1e-7
    assert max(sinr(G, NOISE, p)) - min(sinr(G, NOISE, p)) < 1e-6
    rng = random.Random(2)
    for _ in range(6):
        k = rng.randint(2, 4)
        g, noise = random_case(rng, k, 0.6)
        pmax = [rng.uniform(0.5, 2.0) for _ in range(k)]
        t, p = max_min_sinr(g, noise, pmax)
        assert abs(t - bisect_max_min(g, noise, pmax)) <= 1e-7 * t
        assert min(sinr(g, noise, p)) >= t * (1 - 1e-8)


def test_high_sinr_gp_is_global_by_grid() -> None:
    g = [[1.0, 0.3, 0.6], [0.5, 1.0, 0.2], [0.7, 0.4, 1.0]]
    noise = [0.05, 0.1, 0.08]
    pmax = [1.0, 0.8, 1.2]
    gmin = [0.5, 0.5, 0.5]
    p = high_sinr_rate(g, noise, pmax, gmin)
    assert feasible(g, noise, pmax, gmin, p)
    best_gp = sum(math.log(s) for s in sinr(g, noise, p))
    steps = 24
    best_grid = -math.inf
    axes = [[pmax[i] * 10 ** (-2.0 * a / (steps - 1)) for a in range(steps)] for i in range(3)]
    for a in axes[0]:
        for b in axes[1]:
            for c in axes[2]:
                q = [a, b, c]
                s = sinr(g, noise, q)
                if min(x / y for x, y in zip(s, gmin)) >= 1.0:
                    best_grid = max(best_grid, sum(math.log(x) for x in s))
    assert best_gp >= best_grid - 1e-9
    assert best_gp - best_grid < 0.05


def test_sca_is_monotone_and_feasible() -> None:
    rng = random.Random(4)
    for _ in range(5):
        k = rng.randint(2, 4)
        g, noise = random_case(rng, k, 0.8)
        pmax = [1.0] * k
        gmin = [0.2] * k
        if least_powers(g, [0.21] * k, noise) is None or max(least_powers(g, [0.21] * k, noise)) >= 1.0:
            continue
        p, rates = sca_sum_rate(g, noise, pmax, gmin)
        assert all(b >= a - 1e-9 for a, b in zip(rates, rates[1:]))
        assert feasible(g, noise, pmax, gmin, p, 1e-7)
        assert abs(rates[-1] - sum_rate(g, noise, p)) < 1e-12


def test_sca_page_example() -> None:
    p, rates = sca_sum_rate(G, NOISE, [1.0] * 3, [1.0] * 3)
    assert abs(rates[0] - 3.0215865) < 1e-6
    assert abs(rates[-1] - 5.7301871) < 1e-6
    assert all(abs(v - 1.0) < 1e-6 for v in p)


def test_sca_two_links_against_brute_force() -> None:
    # Weak coupling: one local optimum, and SCA from the default start finds it.
    g = [[1.0, 0.1], [0.15, 1.0]]
    noise = [0.1, 0.1]
    pmax = [1.0, 1.0]
    p, rates = sca_sum_rate(g, noise, pmax, [0.1, 0.1])
    grid = max(sum_rate(g, noise, [a / 100, b / 100]) for a in range(1, 101) for b in range(1, 101))
    assert rates[-1] >= grid - 1e-9 and rates[-1] - grid < 1e-6
    # Strong coupling: SCA stops at a local optimum with link 1 at its minimum.
    gmin = [0.1, 0.1]
    p, rates = sca_sum_rate(STRONG, noise, pmax, gmin)
    assert abs(p[0] - 0.09) < 1e-6 and abs(p[1] - 1.0) < 1e-6
    assert abs(rates[-1] - 2.8434509) < 1e-6
    for d0 in (-1e-3, 1e-3):
        for d1 in (-1e-3, 0.0):
            q = [p[0] + d0, p[1] + d1]
            if feasible(STRONG, noise, pmax, gmin, q, 0.0):
                assert sum_rate(STRONG, noise, q) <= rates[-1] + 1e-9
    # The global optimum, found on a grid, has link 2 at its minimum instead.
    best = max(
        (sum_rate(STRONG, noise, [a / 100, b / 100]), a, b)
        for a in range(1, 101)
        for b in range(1, 101)
        if min(sinr(STRONG, noise, [a / 100, b / 100])) >= 0.1
    )
    assert abs(best[0] - 2.8502216) < 1e-6 and best[1:] == (100, 10)
