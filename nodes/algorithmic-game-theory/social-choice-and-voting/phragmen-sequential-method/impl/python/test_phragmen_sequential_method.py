# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phragmen-sequential-method/. The authors are listed in prov/EVEFGB.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from agtprefs import check_anonymity, random_approval_profile
from phragmen_sequential_method import phragmen_committee, seq_phragmen


def ballots(*groups):
    """groups of (count, set of candidates) -> an approval profile."""
    return tuple(frozenset(A) for count, A in groups for _ in range(count))


def pjr_violation(P, m, k, W):
    """A group S of at least l n / k voters with l common approvals whose members approve
    fewer than l members of W in total. Supersets of S only help, so the smallest S suffice."""
    n = len(P)
    W = set(W)
    for l in range(1, k + 1):
        size = -(-l * n // k)
        for T in itertools.combinations(range(m), l):
            NT = [i for i, A in enumerate(P) if set(T) <= A]
            for S in itertools.combinations(NT, size):
                if len(set().union(*(P[i] for i in S)) & W) < l:
                    return l, T, S
    return None


def ejr_violation(P, m, k, W):
    n = len(P)
    W = set(W)
    for l in range(1, k + 1):
        for T in itertools.combinations(range(m), l):
            S = [i for i, A in enumerate(P) if set(T) <= A and len(A & W) < l]
            if len(S) * k >= l * n:
                return l, T, S
    return None


def random_instance(rng, mmax=6, nmax=8):
    m = rng.randint(1, mmax)
    n = rng.randint(1, nmax)
    k = rng.randint(1, m)
    return m, n, k, random_approval_profile(rng, m, n, rng.choice([0.2, 0.4, 0.6]))


def test_running_example_of_lackner_and_skowron():
    # Example 2.9: a, ..., g = 0, ..., 6
    P = ballots((3, {0, 1}), (3, {0, 2}), (2, {0, 3}), (1, {1, 2, 5}), (1, {4}), (1, {5}), (1, {6}))
    order, times, loads = seq_phragmen(P, 7, 4)
    t1, t2, t3, t4 = F(1, 8), F(11, 32), F(55, 128), F(5, 8)
    assert order == (0, 1, 2, 3)
    assert times == [t1, t2, t3, t4]
    assert loads == [t2, t2, t2, t3, t3, t3, t4, t4, t3, 0, 0, 0]


def test_second_example_of_lackner_and_skowron():
    # Example 2.12: seq-Phragmen elects c, b, d at 1/5, 1/3 and 29/60
    P = ballots((3, {2, 3}), (2, {0, 1}), (2, {0, 2}), (1, {1, 3}))
    order, times, _ = seq_phragmen(P, 4, 3)
    assert order == (2, 1, 3)
    assert times == [F(1, 5), F(1, 3), F(29, 60)]


def test_ejr_counterexample_of_brill_et_al():
    # Example 6 of Brill, Freeman, Janson and Lackner: a, b = 0, 1 and c_j = j + 1
    c = list(range(2, 14))
    P = ballots((2, {0, 1, c[0]}), (2, {0, 1, c[1]}), (6, set(c)), (5, set(c[1:])), (9, set(c[2:])))
    W = phragmen_committee(P, 14, 12)
    assert W == tuple(c)
    assert ejr_violation(P, 14, 12, W) == (2, (0, 1), [0, 1, 2, 3])
    l, T, S = ejr_violation(P, 14, 12, W)
    # PJR holds: the four voters together approve c_1 and c_2
    assert len(set().union(*(P[i] for i in S)) & set(W)) == 2


def test_proportional_justified_representation():
    rng = random.Random(1)
    for _ in range(300):
        m, n, k, P = random_instance(rng)
        assert pjr_violation(P, m, k, phragmen_committee(P, m, k)) is None


def test_committee_monotone_and_loads():
    rng = random.Random(2)
    for _ in range(200):
        m, n, k, P = random_instance(rng)
        order, times, loads = seq_phragmen(P, m, k)
        assert len(set(order)) == k
        assert seq_phragmen(P, m, k - 1)[0] == order[:-1]
        paid = [t for t in times if t is not None]
        assert paid == sorted(paid)
        assert sum(loads) == len(paid)
        assert all(0 <= y <= (paid[-1] if paid else 0) for y in loads)


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
        W = phragmen_committee(P, parties * k, k)
        assert [sum(1 for c in W if c // k == p) for p in range(parties)] == seats


def test_one_seat_is_approval_voting():
    rng = random.Random(4)
    for _ in range(100):
        m, n, k, P = random_instance(rng)
        score = [sum(1 for A in P if c in A) for c in range(m)]
        assert phragmen_committee(P, m, 1) == (score.index(max(score)),)


def test_unapproved_candidates_and_errors():
    P = ballots((2, {2}),)
    order, times, loads = seq_phragmen(P, 4, 3)
    assert order == (2, 0, 1) and times == [F(1, 2), None, None] and loads == [F(1, 2)] * 2
    assert seq_phragmen((), 2, 2)[0] == (0, 1)
    assert seq_phragmen(P, 4, 0) == ((), [], [0, 0])
    with pytest.raises(ValueError):
        seq_phragmen(P, 2, 3)


def test_anonymous():
    rng = random.Random(5)
    profiles = [random_approval_profile(rng, 5, 5, 0.4) for _ in range(60)]
    assert check_anonymity(lambda P, m: phragmen_committee(P, m, 3), 5, 5, profiles=profiles) is None


def test_larger_instance():
    rng = random.Random(6)
    m, n, k = 40, 300, 15
    P = random_approval_profile(rng, m, n, 0.2)
    order, times, loads = seq_phragmen(P, m, k)
    assert len(set(order)) == k and sum(loads) == k and times == sorted(times)
