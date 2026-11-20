# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chamberlin-courant-rule/. The authors are listed in prov/EKGPRX.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from agtprefs import all_rankings, check_anonymity, is_single_peaked_on, random_profile
from chamberlin_courant_rule import (
    cc_single_peaked,
    chamberlin_courant,
    greedy_cc,
    misrepresentation,
    satisfaction,
)


def random_sp_ranking(rng, axis):
    """A random ranking single-peaked on the axis: a random peak, then grow left or right."""
    m = len(axis)
    lo = hi = rng.randrange(m)
    r = [axis[lo]]
    while len(r) < m:
        if hi == m - 1 or (lo > 0 and rng.random() < 0.5):
            lo -= 1
            r.append(axis[lo])
        else:
            hi += 1
            r.append(axis[hi])
    return tuple(r)


def random_sp_profile(rng, m, n):
    axis = tuple(rng.sample(range(m), m))
    return axis, tuple(random_sp_ranking(rng, axis) for _ in range(n))


def optimum(profile, m, k):
    return min(misrepresentation(profile, m, W) for W in itertools.combinations(range(m), k))


def test_exact_search_and_tie_breaking():
    rng = random.Random(1)
    for _ in range(150):
        m = rng.randint(1, 6)
        n = rng.randint(1, 6)
        k = rng.randint(1, m)
        P = random_profile(rng, m, n)
        W = chamberlin_courant(P, m, k)
        best = optimum(P, m, k)
        assert len(W) == k and misrepresentation(P, m, W) == best
        first = next(V for V in itertools.combinations(range(m), k) if misrepresentation(P, m, V) == best)
        assert W == first
        assert satisfaction(P, m, W) == n * (m - 1) - best


def test_dp_matches_exact_search_on_random_single_peaked_profiles():
    rng = random.Random(2)
    for _ in range(300):
        m = rng.randint(1, 7)
        n = rng.randint(0, 7)
        axis, P = random_sp_profile(rng, m, n)
        assert is_single_peaked_on(P, axis)
        for k in range(1, m + 1):
            W, cost = cc_single_peaked(P, m, k, axis)
            assert len(set(W)) == k
            assert cost == misrepresentation(P, m, W) == optimum(P, m, k)
            assert cc_single_peaked(P, m, k, axis[::-1])[1] == cost


def test_dp_on_every_small_single_peaked_profile():
    m, axis = 4, (0, 1, 2, 3)
    R = [r for r in all_rankings(m) if is_single_peaked_on((r,), axis)]
    assert len(R) == 2 ** (m - 1)
    for P in itertools.product(R, repeat=3):
        for k in range(1, m + 1):
            assert cc_single_peaked(P, m, k, axis)[1] == optimum(P, m, k)


def test_greedy_guarantee():
    rng = random.Random(3)
    for _ in range(200):
        m = rng.randint(2, 7)
        n = rng.randint(1, 8)
        k = rng.randint(1, m)
        P = random_profile(rng, m, n)
        g = satisfaction(P, m, greedy_cc(P, m, k))
        opt = n * (m - 1) - optimum(P, m, k)
        assert Fraction(g) >= (1 - (1 - Fraction(1, k)) ** k) * opt
        assert g <= opt


def test_greedy_can_miss_the_optimum():
    P = ((0, 1, 2, 3, 4), (1, 0, 2, 3, 4), (2, 3, 1, 4, 0), (3, 2, 4, 1, 0), (4, 3, 2, 1, 0))
    assert chamberlin_courant(P, 5, 1) == (2,)
    assert greedy_cc(P, 5, 2) == (0, 2)
    assert misrepresentation(P, 5, (0, 2)) == 4
    assert chamberlin_courant(P, 5, 2) == (0, 3)
    assert misrepresentation(P, 5, (0, 3)) == 3
    Q = ((3, 1, 2, 0), (0, 3, 1, 2), (2, 1, 0, 3))
    assert greedy_cc(Q, 4, 2) == (0, 1) and misrepresentation(Q, 4, (0, 1)) == 2
    assert chamberlin_courant(Q, 4, 2) == (2, 3) and misrepresentation(Q, 4, (2, 3)) == 1


def test_one_seat_is_the_borda_winner():
    rng = random.Random(4)
    for _ in range(100):
        m = rng.randint(1, 6)
        n = rng.randint(1, 6)
        P = random_profile(rng, m, n)
        borda = [sum(m - 1 - r.index(c) for r in P) for c in range(m)]
        assert chamberlin_courant(P, m, 1) == (borda.index(max(borda)),)


def test_full_committee_and_errors():
    P = ((2, 0, 1), (1, 0, 2))
    assert misrepresentation(P, 3, chamberlin_courant(P, 3, 3)) == 0
    assert satisfaction(P, 3, ()) == 0
    with pytest.raises(ValueError):
        chamberlin_courant(P, 3, 0)
    with pytest.raises(ValueError):
        cc_single_peaked(P, 3, 4, (2, 0, 1))


def test_page_example():
    axis = (0, 1, 2, 3, 4)
    P = ((0, 1, 2, 3, 4), (1, 0, 2, 3, 4), (2, 3, 1, 4, 0), (3, 2, 4, 1, 0), (4, 3, 2, 1, 0))
    assert is_single_peaked_on(P, axis)
    W, cost = cc_single_peaked(P, 5, 2, axis)
    assert cost == 3 and misrepresentation(P, 5, W) == 3
    assert chamberlin_courant(P, 5, 2) == (0, 3)
    assert satisfaction(P, 5, (0, 3)) == 17


def test_anonymous():
    rng = random.Random(5)
    profiles = [random_profile(rng, 4, 3) for _ in range(40)]
    rule = lambda P, m: chamberlin_courant(P, m, 2)
    assert check_anonymity(rule, 4, 3, profiles=profiles) is None


def test_large_single_peaked_instance():
    rng = random.Random(6)
    axis, P = random_sp_profile(rng, 30, 200)
    W, cost = cc_single_peaked(P, 30, 5, axis)
    assert cost == misrepresentation(P, 30, W)
    g = greedy_cc(P, 30, 5)
    assert misrepresentation(P, 30, g) >= cost
