# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hochbaum-shmoys-ptas/. The authors are listed in prov/KC7QKZ.jsonl.

import random
from fractions import Fraction

import pytest

from hochbaum_shmoys_ptas import _configurations, dual_test, hochbaum_shmoys


def makespan(p, m, sigma):
    load = [0] * m
    for j, i in enumerate(sigma):
        assert 0 <= i < m
        load[i] += p[j]
    return max(load)


def brute_opt(p, m):
    """Least makespan by depth-first search with pruning."""
    best = [sum(p) + 1]
    load = [0] * m
    order = sorted(p, reverse=True)

    def go(j):
        if j == len(order):
            best[0] = min(best[0], max(load))
            return
        seen = set()
        for i in range(m):
            if load[i] in seen or load[i] + order[j] >= best[0]:
                continue
            seen.add(load[i])
            load[i] += order[j]
            go(j + 1)
            load[i] -= order[j]

    go(0)
    return best[0]


def test_page_example():
    p = [5, 5, 5, 1, 1]
    assert dual_test(p, 2, 3, 9) is None
    for T in (10, 11, 13):
        assert dual_test(p, 2, 3, T) is not None
    sigma, T = hochbaum_shmoys(p, 2, 3)
    assert T == 10
    assert makespan(p, 2, sigma) == 10 == brute_opt(p, 2)


def test_ratio_against_brute_force():
    rng = random.Random(1987)
    for _ in range(300):
        n, m, k = rng.randint(1, 8), rng.randint(1, 3), rng.randint(1, 3)
        p = [rng.randint(1, 20) for _ in range(n)]
        sigma, T = hochbaum_shmoys(p, m, k)
        opt = brute_opt(p, m)
        assert T <= opt
        assert makespan(p, m, sigma) <= (1 + Fraction(1, k)) * T


def test_dual_test_contract():
    """A failure proves OPT > T, and a success has makespan at most (1 + 1/k) T."""
    rng = random.Random(55)
    for _ in range(150):
        n, m, k = rng.randint(1, 7), rng.randint(1, 3), rng.randint(1, 3)
        p = [rng.randint(1, 15) for _ in range(n)]
        opt = brute_opt(p, m)
        for T in range(max(p), 2 * opt + 1):
            sigma = dual_test(p, m, k, T)
            if sigma is None:
                assert opt > T
            else:
                assert makespan(p, m, sigma) <= (1 + Fraction(1, k)) * T


def test_configurations_hold_at_most_k_long_jobs():
    for k in range(1, 5):
        sizes = list(range(k, k * k + 1))
        for c in _configurations(sizes, k * k):
            assert sum(a * s for a, s in zip(c, sizes)) <= k * k
            assert 1 <= sum(c) <= k


def test_edges():
    assert hochbaum_shmoys([], 3, 2) == ([], 0)
    sigma, T = hochbaum_shmoys([7], 3, 2)
    assert makespan([7], 3, sigma) == 7 and T == 7
    sigma, _ = hochbaum_shmoys([4, 4, 4, 4], 4, 2)
    assert makespan([4, 4, 4, 4], 4, sigma) == 4
    with pytest.raises(ValueError):
        hochbaum_shmoys([1], 0, 2)
    with pytest.raises(ValueError):
        hochbaum_shmoys([1], 1, 0)
