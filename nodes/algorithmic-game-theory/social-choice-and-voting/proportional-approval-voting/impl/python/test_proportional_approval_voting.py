# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proportional-approval-voting/. The authors are listed in prov/95W632.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from agtprefs import check_anonymity, random_approval_profile
from proportional_approval_voting import harmonic, ls_pav, pav, pav_score, seq_pav, swap_gain


def ejr_violation(P, m, k, W):
    """Brute force: an l-cohesive group (|S| >= l n / k, all approve l common candidates)
    whose members each approve fewer than l members of W. Returns None or (l, T, S)."""
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


# Lackner and Skowron, Example 2.5: a, b, c, d = 0, 1, 2, 3.
EXAMPLE = (frozenset({0, 1}),) * 3 + (frozenset({0, 3}),) * 6 + (frozenset({1}),) * 4 \
    + (frozenset({2}),) * 5 + (frozenset({2, 3}),) * 5


def test_harmonic():
    assert harmonic(0) == 0 and harmonic(1) == 1 and harmonic(4) == Fraction(25, 12)


def test_exact_search_and_tie_breaking():
    rng = random.Random(1)
    for _ in range(200):
        m, n, k, P = random_instance(rng)
        W = pav(P, m, k)
        best = max(pav_score(P, V) for V in itertools.combinations(range(m), k))
        assert pav_score(P, W) == best
        assert W == next(V for V in itertools.combinations(range(m), k) if pav_score(P, V) == best)


def test_example_of_lackner_and_skowron():
    m, k = 4, 2
    assert pav(EXAMPLE, m, k) == (0, 2) and pav_score(EXAMPLE, (0, 2)) == 19
    assert seq_pav(EXAMPLE, m, k) == (2, 3) and pav_score(EXAMPLE, (2, 3)) == Fraction(37, 2)
    # the best swap gains only 1/2 < n / k^2 = 23/4, so local search keeps {c, d}
    assert ls_pav(EXAMPLE, m, k) == (2, 3)
    assert ejr_violation(EXAMPLE, m, k, (2, 3)) is None
    for start in itertools.combinations(range(m), k):
        assert ejr_violation(EXAMPLE, m, k, ls_pav(EXAMPLE, m, k, start=start)) is None


def test_pav_satisfies_ejr():
    rng = random.Random(2)
    for _ in range(250):
        m, n, k, P = random_instance(rng)
        assert ejr_violation(P, m, k, pav(P, m, k)) is None


def test_local_search_satisfies_ejr_from_any_start():
    rng = random.Random(3)
    for _ in range(250):
        m, n, k, P = random_instance(rng)
        start = rng.sample(range(m), k)
        W = ls_pav(P, m, k, start=start)
        assert len(set(W)) == k
        assert ejr_violation(P, m, k, W) is None
        assert pav_score(P, W) >= pav_score(P, start)


def test_swap_lemma():
    """If W violates EJR, some swap raises the PAV score by at least n / k^2."""
    rng = random.Random(4)
    seen = 0
    for _ in range(1500):
        m, n, k, P = random_instance(rng)
        if k == m:
            continue
        W = rng.sample(range(m), k)
        if ejr_violation(P, m, k, W) is None:
            continue
        seen += 1
        ballots = [set(A) for A in P]
        cnt = [len(A & set(W)) for A in ballots]
        best = max(swap_gain(ballots, cnt, w, c) for w in W for c in range(m) if c not in W)
        assert best >= Fraction(n, k * k)
        w, c = max(((w, c) for w in W for c in range(m) if c not in W),
                   key=lambda wc: swap_gain(ballots, cnt, *wc))
        V = [x for x in W if x != w] + [c]
        assert pav_score(P, V) - pav_score(P, W) == swap_gain(ballots, cnt, w, c)
    assert seen > 50


def dhondt(votes, k):
    """Seats by the highest averages v / (s + 1); ties to the smaller party index."""
    seats = [0] * len(votes)
    for _ in range(k):
        j = max(range(len(votes)), key=lambda p: (Fraction(votes[p], seats[p] + 1), -p))
        seats[j] += 1
    return seats


def test_party_lists_give_dhondt():
    rng = random.Random(5)
    for _ in range(40):
        parties = rng.randint(1, 3)
        k = rng.randint(1, 4)
        votes = [rng.randint(1, 7) for _ in range(parties)]
        # party p has the candidates p k, ..., p k + k - 1, approved by all its voters
        m = parties * k
        P = tuple(frozenset(range(p * k, p * k + k)) for p in range(parties) for _ in range(votes[p]))
        seats = dhondt(votes, k)
        W = [p * k + s for p in range(parties) for s in range(seats[p])]
        assert pav_score(P, W) == pav_score(P, pav(P, m, k))


def test_one_seat_is_approval_voting():
    rng = random.Random(6)
    for _ in range(100):
        m, n, k, P = random_instance(rng)
        score = [sum(1 for A in P if c in A) for c in range(m)]
        assert pav(P, m, 1) == seq_pav(P, m, 1) == (score.index(max(score)),)


def test_edge_cases():
    assert pav((), 3, 2) == (0, 1)
    assert ls_pav((), 3, 2) == (0, 1)
    assert pav((frozenset({1}),), 2, 0) == ()
    assert ls_pav((frozenset({1}),), 2, 2) == (0, 1)
    with pytest.raises(ValueError):
        pav((), 2, 3)


def test_anonymous():
    rng = random.Random(7)
    profiles = [random_approval_profile(rng, 4, 4, 0.5) for _ in range(40)]
    assert check_anonymity(lambda P, m: pav(P, m, 2), 4, 4, profiles=profiles) is None


def test_larger_local_search():
    rng = random.Random(8)
    m, n, k = 12, 60, 5
    P = random_approval_profile(rng, m, n, 0.3)
    W = ls_pav(P, m, k)
    assert ejr_violation(P, m, k, W) is None
