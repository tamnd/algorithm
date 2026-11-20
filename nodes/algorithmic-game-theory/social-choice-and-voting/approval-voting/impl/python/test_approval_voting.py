# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approval-voting/. The authors are listed in prov/2YTCNT.jsonl.

import itertools
import random
from collections import Counter

from agtprefs import (all_profiles, check_anonymity, check_condorcet_consistency,
                      check_neutrality, condorcet_winner, permute_profile, random_approval_profile,
                      random_profile)
from approval_voting import approval, approval_scores, approval_winners, sincere_ballot

A, B, C, D = 0, 1, 2, 3


def all_ballots(m):
    """Every subset of the m candidates, from the empty ballot to the full one."""
    return [frozenset(c) for k in range(m + 1) for c in itertools.combinations(range(m), k)]


def all_approval_profiles(m, n):
    return itertools.product(all_ballots(m), repeat=n)


def place(r, a):
    return r.index(a)


# The worked example: the voters of the plurality page, each approving the candidates above
# the line: 4 voters a | b c, 3 voters b | c a and 2 voters c b | a.
EXAMPLE = (frozenset({A}),) * 4 + (frozenset({B}),) * 3 + (frozenset({C, B}),) * 2


def test_worked_example():
    assert approval_scores(EXAMPLE, 3) == [4, 5, 2]
    assert approval(EXAMPLE, 3) == B
    # Plurality on the same voters elects a; approval finds the Condorcet winner b.
    rankings = ((A, B, C),) * 4 + ((B, C, A),) * 3 + ((C, B, A),) * 2
    assert condorcet_winner(rankings, 3) == B


def test_condorcet_winner_can_lose():
    # 3 voters a > b > c approve {a, b}; 2 voters b > a > c approve {b}. a is the Condorcet
    # winner, but b has 5 approvals to 3.
    rankings = ((A, B, C),) * 3 + ((B, A, C),) * 2
    ballots = (frozenset({A, B}),) * 3 + (frozenset({B}),) * 2
    assert condorcet_winner(rankings, 3) == A
    assert approval_scores(ballots, 3) == [3, 5, 0]
    assert approval(ballots, 3) == B
    # If the three a-voters approve only a, then a wins 3 to 2.
    narrow = (frozenset({A}),) * 3 + (frozenset({B}),) * 2
    assert approval(narrow, 3) == A


def test_matches_counter_on_random_profiles():
    rng = random.Random(31)
    for _ in range(2000):
        m, n = rng.randint(1, 6), rng.randint(0, 12)
        P = random_approval_profile(rng, m, n, rng.random())
        cnt = Counter(a for S in P for a in S)
        s = approval_scores(P, m)
        assert s == [cnt[a] for a in range(m)]
        assert sum(s) == sum(len(S) for S in P)
        W = {a for a in range(m) if cnt[a] == max(s)}
        assert approval_winners(P, m) == W
        assert approval(P, m) == min(W)


def test_edge_cases():
    assert approval((), 3) == 0 and approval_winners((), 3) == {0, 1, 2}
    assert approval((frozenset(),) * 4, 2) == 0
    assert approval((frozenset({1, 2}), frozenset({2, 1})), 3) == 1
    assert approval_winners((frozenset({0, 1, 2}),), 3) == {0, 1, 2}


def test_plurality_ballots_give_plurality():
    # If every voter approves exactly one candidate, approval voting is plurality voting.
    rng = random.Random(32)
    for _ in range(500):
        m, n = rng.randint(1, 5), rng.randint(1, 9)
        P = random_profile(rng, m, n)
        tops = Counter(r[0] for r in P)
        best = max(tops[a] for a in range(m))
        assert approval([sincere_ballot(r, 1) for r in P], m) == min(
            a for a in range(m) if tops[a] == best)


def test_axioms_by_brute_force():
    for m, n in [(3, 2), (3, 3), (4, 2)]:
        domain = list(all_approval_profiles(m, n))
        assert check_anonymity(approval, m, n, profiles=domain) is None
        assert check_neutrality(approval_winners, m, n, profiles=domain) is None
        for P in domain:
            W = approval_winners(P, m)
            # Pareto: if the voters who approve b are a strict subset of those who approve a,
            # then b does not win.
            for a, b in itertools.permutations(range(m), 2):
                fa = {i for i, S in enumerate(P) if a in S}
                fb = {i for i, S in enumerate(P) if b in S}
                if fb < fa:
                    assert b not in W
            # Monotonicity: one more approval for a winner keeps it a winner, and the resolute
            # winner stays the winner.
            w = approval(P, m)
            for i, S in enumerate(P):
                if w not in S:
                    Q = P[:i] + (S | {w},) + P[i + 1:]
                    assert approval(Q, m) == w
    # The resolute rule with the fixed tie-break is not neutral.
    P = (frozenset({A}), frozenset({B}))
    assert approval(permute_profile(P, (1, 0, 2)), 3) != 1


def test_consistency_by_brute_force():
    for n1, n2 in [(1, 1), (1, 2), (2, 2)]:
        checked = 0
        for P1 in all_approval_profiles(3, n1):
            W1 = approval_winners(P1, 3)
            for P2 in all_approval_profiles(3, n2):
                both = W1 & approval_winners(P2, 3)
                if both:
                    assert approval_winners(P1 + P2, 3) == both
                    checked += 1
        assert checked > 0


def test_sincere_ballot_is_dominant_for_dichotomous_preferences():
    # A voter who only cares whether the winner is in the set G cannot gain by any ballot
    # other than G, whatever the other voters do, with the fixed tie-break too.
    for m, others in [(3, 1), (3, 2), (3, 3), (4, 2)]:
        ballots = all_ballots(m)
        for O in all_approval_profiles(m, others):
            winner = {S: approval((S,) + O, m) for S in ballots}
            for G in ballots:
                if winner[G] not in G:
                    assert not any(winner[S] in G for S in ballots)


def undominated_ballots(r, m, others):
    """Ballots that no other ballot weakly dominates, for a voter with ranking r."""
    ballots = all_ballots(m)
    rows = list(all_approval_profiles(m, others))
    res = {S: [place(r, approval((S,) + O, m)) for O in rows] for S in ballots}
    keep = []
    for S in ballots:
        dominated = any(
            all(t <= s for s, t in zip(res[S], res[T])) and res[T] != res[S]
            for T in ballots if T != S)
        if not dominated:
            keep.append(tuple(sorted(S)))
    return sorted(keep)


def test_admissible_ballots_of_brams_and_fishburn():
    # With 3 candidates and a ranking a > b > c, only {a} and {a, b} are undominated, and
    # neither dominates the other, so there is no dominant ballot. With 4 candidates the
    # insincere ballot {a, c} is undominated too.
    assert undominated_ballots((A, B, C), 3, 2) == [(A,), (A, B)]
    assert undominated_ballots((A, B, C, D), 4, 2) == [(A,), (A, B), (A, B, C), (A, C)]


def test_not_condorcet_consistent_with_sincere_thresholds():
    # Voters who approve their top half (rounded up) can still miss the Condorcet winner.
    def top_half(P, m):
        return approval([sincere_ballot(r, (m + 1) // 2) for r in P], m)

    P, c = check_condorcet_consistency(top_half, 3, 3)
    assert top_half(P, 3) != c
    assert any(condorcet_winner(P, 3) is not None for P in all_profiles(3, 3))
