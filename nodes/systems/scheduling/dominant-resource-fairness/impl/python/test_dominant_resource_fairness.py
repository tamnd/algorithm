# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominant-resource-fairness/. The authors are listed in prov/DB84HW.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from dominant_resource_fairness import dominant_shares, dominant_unit, drf, drf_discrete


def test_paper_example() -> None:
    cap = [9, 18]  # 9 CPUs, 18 GB
    dem = [[1, 4], [3, 1]]  # A: <1 CPU, 4 GB>, B: <3 CPU, 1 GB>
    tasks = drf(cap, dem)
    assert tasks == [3, 2]
    assert dominant_shares(cap, dem, tasks) == [F(2, 3), F(2, 3)]
    used = [sum(t * d[r] for t, d in zip(tasks, dem)) for r in range(2)]
    assert used == [9, 14]  # CPU is used up, 4 GB stay free
    assert drf_discrete(cap, dem) == [3, 2]


def used(cap, dem, x):
    return [sum(x[i] * dem[i][r] for i in range(len(dem))) for r in range(len(cap))]


def random_instance(rng):
    m, n = rng.randrange(1, 4), rng.randrange(1, 4)
    cap = [rng.randrange(1, 13) for _ in range(m)]
    dem = []
    for _ in range(n):
        d = [rng.randrange(0, 5) for _ in range(m)]
        if max(d) == 0:
            d[rng.randrange(m)] = 1
        dem.append(d)
    return cap, dem


def test_properties_on_random_instances() -> None:
    rng = random.Random(13)
    for _ in range(300):
        cap, dem = random_instance(rng)
        n, m = len(dem), len(cap)
        x = drf(cap, dem)
        s = dominant_shares(cap, dem, x)
        u = used(cap, dem, x)
        assert all(u[r] <= cap[r] for r in range(m))  # feasible
        assert all(si >= F(1, n) for si in s)  # sharing incentive
        full = [r for r in range(m) if u[r] == cap[r]]
        for i in range(n):
            # Pareto: every user needs some used-up resource
            assert any(dem[i][r] > 0 for r in full)
            for j in range(n):
                # envy-free: j's bundle gives i at most x_i tasks
                k = min(x[j] * dem[j][r] / dem[i][r] for r in range(m) if dem[i][r] > 0)
                assert k <= x[i]


def test_leximin_against_grid_brute_force() -> None:
    # Every feasible allocation on a grid of dominant shares is at most as
    # good as DRF in the leximin order of the sorted dominant shares.
    rng = random.Random(14)
    for _ in range(40):
        cap, dem = random_instance(rng)
        n = len(dem)
        unit = [dominant_unit(cap, d) for d in dem]
        best = sorted(dominant_shares(cap, dem, drf(cap, dem)))
        grid = [F(k, 12) for k in range(13)]
        top = None
        for shares in itertools.product(grid, repeat=n):
            x = [shares[i] / unit[i] for i in range(n)]
            if all(v <= c for v, c in zip(used(cap, dem, x), cap)):
                assert sorted(shares) <= best
                top = max(top, sorted(shares)) if top else sorted(shares)
        if all((b * 12).denominator == 1 for b in best):
            assert top == best  # DRF itself is on the grid, and it is the best


def test_max_min_property() -> None:
    # If another feasible allocation gives user i more, it gives less to some
    # user j whose DRF share is at most i's.
    rng = random.Random(15)
    for _ in range(200):
        cap, dem = random_instance(rng)
        n = len(dem)
        x = drf(cap, dem)
        s = dominant_shares(cap, dem, x)
        for _ in range(20):
            y = [x[i] * F(rng.randrange(0, 25), 20) for i in range(n)]
            if any(v > c for v, c in zip(used(cap, dem, y), cap)):
                continue
            t = dominant_shares(cap, dem, y)
            for i in range(n):
                if t[i] > s[i]:
                    assert any(s[j] <= s[i] and t[j] < s[j] for j in range(n))


def test_discrete_stops_when_lowest_user_does_not_fit() -> None:
    rng = random.Random(16)
    for _ in range(200):
        cap, dem = random_instance(rng)
        k = drf_discrete(cap, dem)
        u = used(cap, dem, k)
        assert all(a <= c for a, c in zip(u, cap))
        unit = [dominant_unit(cap, d) for d in dem]
        low = min(range(len(dem)), key=lambda i: (k[i] * unit[i], i))
        assert any(u[r] + dem[low][r] > cap[r] for r in range(len(cap)))


def test_edges() -> None:
    assert drf([5], []) == []
    assert drf([10], [[2]]) == [5]
    assert drf([6, 6], [[1, 0], [0, 2]]) == [6, 3]  # no shared resource
    with pytest.raises(ValueError):
        drf([0], [[1]])
    with pytest.raises(ValueError):
        drf([1, 1], [[0, 0]])
