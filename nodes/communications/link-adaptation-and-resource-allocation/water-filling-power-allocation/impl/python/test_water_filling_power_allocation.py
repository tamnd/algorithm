# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/water-filling-power-allocation/. The authors are listed in prov/1Y9CA5.jsonl.

import itertools
import math
import random

import pytest

from water_filling_power_allocation import noise_levels, sum_rate, water_filling, water_level_by_bisection


def test_check_value() -> None:
    p, mu = water_filling([1, 2, 4], 3)
    assert abs(mu - 3) < 1e-12
    assert all(abs(a - b) < 1e-12 for a, b in zip(p, [2, 1, 0]))
    assert abs(sum_rate([1, 2, 4], p) - (math.log2(3) + math.log2(1.5))) < 1e-12
    assert abs(sum_rate([1, 2, 4], p) - 2.169925) < 1e-6


def test_second_example_on_the_page() -> None:
    p, mu = water_filling([0.5, 1, 1.5, 3], 2)
    assert abs(mu - 5 / 3) < 1e-12
    assert abs(p[3]) == 0
    assert abs(sum_rate([0.5, 1, 1.5, 3], p) - 2.625934) < 1e-6
    p, mu = water_filling([1, 2, 4], 10)
    assert abs(mu - 17 / 3) < 1e-12 and min(p) > 0
    p, mu = water_filling([1, 2, 4], 0.5)
    assert abs(mu - 1.5) < 1e-12 and p[1] == 0 and p[2] == 0


def kkt_ok(nu, power, p, mu, tol=1e-9):
    if abs(sum(p) - power) > tol or min(p) < 0:
        return False
    for v, pi in zip(nu, p):
        if pi > 0 and abs(v + pi - mu) > tol:
            return False
        if pi == 0 and v < mu - tol:
            return False
    return True


def test_kkt_and_power_on_random_channels() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 64)
        nu = [rng.expovariate(1.0) + 1e-3 for _ in range(n)]
        power = rng.uniform(0.01, 20)
        p, mu = water_filling(nu, power)
        assert kkt_ok(nu, power, p, mu)
        assert abs(mu - water_level_by_bisection(nu, power)) < 1e-9


def test_order_and_ties() -> None:
    nu = [2.0, 0.5, 2.0, 7.0, 0.5]
    p, mu = water_filling(nu, 4)
    assert kkt_ok(nu, 4, p, mu)
    assert p[0] == p[2] and p[1] == p[4]
    rng = random.Random(3)
    for _ in range(20):
        perm = list(range(5))
        rng.shuffle(perm)
        q, mu2 = water_filling([nu[i] for i in perm], 4)
        assert abs(mu2 - mu) < 1e-12
        assert all(abs(q[j] - p[perm[j]]) < 1e-12 for j in range(5))


def test_against_grid_search() -> None:
    rng = random.Random(5)
    for n in (2, 3):
        for _ in range(6):
            nu = [rng.uniform(0.1, 3) for _ in range(n)]
            power = rng.uniform(0.5, 4)
            p, _ = water_filling(nu, power)
            best = sum_rate(nu, p)
            steps = 120
            grid = 0.0
            for c in itertools.product(range(steps + 1), repeat=n - 1):
                if sum(c) > steps:
                    continue
                q = [power * x / steps for x in c] + [power * (steps - sum(c)) / steps]
                grid = max(grid, sum_rate(nu, q))
            assert grid <= best + 1e-12
            assert best - grid < 1e-3


def test_random_feasible_moves_do_not_help() -> None:
    rng = random.Random(8)
    nu = [rng.uniform(0.1, 2) for _ in range(16)]
    p, _ = water_filling(nu, 5)
    best = sum_rate(nu, p)
    for _ in range(2000):
        i, j = rng.sample(range(16), 2)
        d = rng.uniform(0, p[i]) if p[i] > 0 else 0.0
        q = list(p)
        q[i] -= d
        q[j] += d
        assert sum_rate(nu, q) <= best + 1e-12


def test_gap_and_noise_levels() -> None:
    nu = noise_levels([1 + 1j, 0.5j, 2], 0.5, gap=2.0)
    assert all(abs(a - b) < 1e-12 for a, b in zip(nu, [0.5, 4.0, 0.25]))
    p, _ = water_filling(nu, 1)
    assert p[1] == 0


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        water_filling([], 1)
    with pytest.raises(ValueError):
        water_filling([1, 0], 1)
    with pytest.raises(ValueError):
        water_filling([1], -1)
    assert water_filling([3, 1], 0) == ([0.0, 0.0], 1)
