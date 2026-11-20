# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/method-of-equal-shares/. The authors are listed in prov/KK2YJY.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from agtprefs import check_anonymity, random_approval_profile
from method_of_equal_shares import equal_shares, equal_shares_order, equal_shares_phase1, rho


def ballots(*groups):
    return tuple(frozenset(A) for count, A in groups for _ in range(count))


def ejr_violation(P, m, k, W):
    n = len(P)
    W = set(W)
    for l in range(1, k + 1):
        for T in itertools.combinations(range(m), l):
            S = [i for i, A in enumerate(P) if set(T) <= A and len(A & W) < l]
            if S and len(S) * k >= l * n:
                return l, T, S
    return None


def random_instance(rng, mmax=6, nmax=8):
    m = rng.randint(1, mmax)
    n = rng.randint(1, nmax)
    k = rng.randint(1, m)
    return m, n, k, random_approval_profile(rng, m, n, rng.choice([0.2, 0.4, 0.6]))


def test_rho():
    assert rho([F(1), F(1)], 1) == F(1, 2)
    assert rho([F(1, 10), F(1), F(1)], 1) == F(9, 20)
    assert rho([F(1, 4), F(1, 4)], 1) is None
    assert rho([F(1, 2), F(1, 2)], 1) == F(1, 2)
    rng = random.Random(1)
    for _ in range(300):
        b = [F(rng.randint(0, 6), rng.randint(1, 4)) for _ in range(rng.randint(1, 5))]
        cost = F(rng.randint(1, 8), rng.randint(1, 3))
        r = rho(b, cost)
        if sum(b) < cost:
            assert r is None
            continue
        assert sum(min(r, x) for x in b) == cost
        assert sum(min(r - F(1, 10 ** 6), x) for x in b) < cost


def test_running_example_of_lackner_and_skowron():
    # Example 2.11: a, ..., g = 0, ..., 6, k = 4
    P = ballots((3, {0, 1}), (3, {0, 2}), (2, {0, 3}), (1, {1, 2, 5}), (1, {4}), (1, {5}), (1, {6}))
    order, rhos, x = equal_shares_phase1(P, 7, 4)
    assert order == [0] and rhos == [F(1, 8)]
    assert x == [F(1, 3) - F(1, 8)] * 8 + [F(1, 3)] * 4
    order, phase1, times = equal_shares_order(P, 7, 4)
    assert order == (0, 1, 2, 3) and phase1 == 1
    assert times == [F(1, 96), F(37, 384), F(7, 24)]


def test_second_example_of_lackner_and_skowron():
    # Example 2.12: a, b, c, d = 0, 1, 2, 3, k = 3
    P = ballots((3, {2, 3}), (2, {0, 1}), (2, {0, 2}), (1, {1, 3}))
    order, rhos, x = equal_shares_phase1(P, 4, 3)
    assert order == [2, 0] and rhos == [F(1, 5), F(13, 40)]
    assert x == [F(7, 40)] * 3 + [F(1, 20)] * 2 + [0, 0] + [F(3, 8)]
    order, phase1, times = equal_shares_order(P, 4, 3)
    assert order == (2, 0, 3) and phase1 == 2 and times == [F(1, 40)]
    assert equal_shares(P, 4, 3) == (0, 2, 3)


def test_ejr_after_phase_one_and_after_completion():
    rng = random.Random(2)
    for _ in range(300):
        m, n, k, P = random_instance(rng)
        order, _, x = equal_shares_phase1(P, m, k)
        assert len(order) <= k and all(b >= 0 for b in x)
        assert sum(x) == k - len(order)
        assert ejr_violation(P, m, k, order) is None
        W = equal_shares(P, m, k)
        assert len(W) == k and set(order) <= set(W)


def test_party_lists_give_dhondt():
    rng = random.Random(3)
    for _ in range(60):
        parties = rng.randint(1, 4)
        k = rng.randint(1, 5)
        votes = [rng.randint(1, 9) for _ in range(parties)]
        P = ballots(*((votes[p], set(range(p * k, p * k + k))) for p in range(parties)))
        seats = [0] * parties
        for _ in range(k):
            j = max(range(parties), key=lambda p: (F(votes[p], seats[p] + 1), -p))
            seats[j] += 1
        W = equal_shares(P, parties * k, k)
        assert [sum(1 for c in W if c // k == p) for p in range(parties)] == seats


def test_budgeting_with_costs():
    rng = random.Random(4)
    for _ in range(200):
        m, n, k, P = random_instance(rng)
        costs = [rng.randint(1, 5) for _ in range(m)]
        budget = rng.randint(1, 12)
        order, rhos, x = equal_shares_phase1(P, m, budget, costs)
        assert sum(costs[c] for c in order) + sum(x) == budget
        assert rhos == sorted(rhos)
        # every bought project was affordable at a price no voter exceeds
        y = [F(budget, n)] * n
        for c, r in zip(order, rhos):
            pay = [min(r, y[i]) if c in P[i] else 0 for i in range(n)]
            assert sum(pay) == costs[c]
            y = [a - b for a, b in zip(y, pay)]
        assert y == x
        # nothing left is affordable
        for c in range(m):
            if c not in order:
                assert sum(x[i] for i in range(n) if c in P[i]) < costs[c]
    with pytest.raises(ValueError):
        equal_shares_phase1(P, m, 1, [0] * m)


def test_unit_costs_match_the_committee_version():
    rng = random.Random(5)
    for _ in range(100):
        m, n, k, P = random_instance(rng)
        assert equal_shares_phase1(P, m, k, [1] * m) == equal_shares_phase1(P, m, k)


def test_edge_cases():
    assert equal_shares((), 3, 2) == (0, 1)
    assert equal_shares((frozenset(),), 3, 2) == (0, 1)
    assert equal_shares((frozenset({2}),), 3, 0) == ()
    with pytest.raises(ValueError):
        equal_shares((), 2, 3)


def test_anonymous():
    rng = random.Random(6)
    profiles = [random_approval_profile(rng, 5, 5, 0.4) for _ in range(60)]
    assert check_anonymity(lambda P, m: equal_shares(P, m, 3), 5, 5, profiles=profiles) is None


def test_larger_instance():
    rng = random.Random(7)
    m, n, k = 30, 200, 10
    P = random_approval_profile(rng, m, n, 0.2)
    order, phase1, times = equal_shares_order(P, m, k)
    assert len(set(order)) == k and phase1 <= k
