# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instant-runoff-voting/. The authors are listed in prov/P7TC87.jsonl.

import itertools
import random

from agtprefs import (all_profiles, all_rankings, check_anonymity, check_condorcet_consistency,
                      check_monotonicity, check_neutrality, check_pareto, condorcet_winner,
                      find_manipulation, margins, permute_profile, prefers, random_profile)
from instant_runoff_voting import instant_runoff, instant_runoff_rounds

A, B, C, D = 0, 1, 2, 3


def naive_irv(profile, m):
    """Recount every ballot from scratch in each round, with the same tie rules."""
    cont = set(range(m))
    while True:
        count = {a: 0 for a in cont}
        for r in profile:
            tops = [a for a in r if a in cont]
            if tops:
                count[tops[0]] += 1
        active = sum(count.values())
        for a in sorted(cont):
            if 2 * count[a] > active or len(cont) == 1:
                return a
        low = min(count.values())
        cont.remove(max(a for a in cont if count[a] == low))


def put_winners(profile, m):
    """The winners under every way of breaking elimination ties (parallel universes)."""
    out = set()

    def run(cont):
        if len(cont) == 1:
            out.update(cont)
            return
        count = {a: 0 for a in cont}
        for r in profile:
            tops = [a for a in r if a in cont]
            if tops:
                count[tops[0]] += 1
        low = min(count.values())
        for x in [a for a in cont if count[a] == low]:
            run(cont - {x})

    run(frozenset(range(m)))
    return frozenset(out)


def condorcet_loser(P, m):
    M = margins(P, m)
    for a in range(m):
        if all(M[a][b] < 0 for b in range(m) if b != a):
            return a
    return None


def multisets(m, n):
    return [tuple(c) for c in itertools.combinations_with_replacement(all_rankings(m), n)]


# The worked example: the nine voters of the plurality page.
EXAMPLE = ((A, B, C),) * 4 + ((B, C, A),) * 3 + ((C, B, A),) * 2


def test_worked_example():
    w, rounds = instant_runoff_rounds(EXAMPLE, 3)
    assert rounds == [([4, 3, 2], C), ([4, 5, 0], -1)]
    assert w == B == condorcet_winner(EXAMPLE, 3)


def test_matches_naive_recount():
    rng = random.Random(41)
    for _ in range(3000):
        m, n = rng.randint(1, 6), rng.randint(0, 11)
        if rng.random() < 0.5:
            P = random_profile(rng, m, n)
        else:  # truncated ballots
            P = tuple(tuple(rng.sample(range(m), rng.randint(0, m))) for _ in range(n))
        assert instant_runoff(P, m) == naive_irv(P, m)


def test_early_stop_equals_running_to_the_end():
    # Stopping at a majority of the continuing ballots gives the same winner as eliminating
    # until one candidate is left.
    def to_the_end(P, m):
        cont = set(range(m))
        while len(cont) > 1:
            count = {a: sum(1 for r in P if [x for x in r if x in cont][:1] == [a]) for a in cont}
            low = min(count.values())
            cont.remove(max(a for a in cont if count[a] == low))
        return cont.pop()

    rng = random.Random(42)
    for _ in range(1500):
        m, n = rng.randint(1, 6), rng.randint(1, 11)
        P = random_profile(rng, m, n)
        assert instant_runoff(P, m) == to_the_end(P, m)


def test_rounds_are_consistent():
    rng = random.Random(43)
    for _ in range(500):
        m, n = rng.randint(1, 6), rng.randint(1, 11)
        P = random_profile(rng, m, n)
        w, rounds = instant_runoff_rounds(P, m)
        out = set()
        for count, x in rounds:
            assert all(count[a] == 0 for a in out)
            assert sum(count) == n  # full rankings are never exhausted
            if x >= 0:
                assert count[x] == min(count[a] for a in range(m) if a not in out)
                out.add(x)
        assert len(rounds) <= m and w not in out


def test_edge_cases():
    assert instant_runoff((), 3) == 0
    assert instant_runoff(((), ()), 2) == 0
    assert instant_runoff(((0,),), 1) == 0
    assert instant_runoff(((1, 0), (0, 1)), 2) == 0  # a final tie goes to the smaller index
    assert instant_runoff(((2,), (1,), (1,)), 3) == 1  # truncated ballots


def test_majority_and_condorcet_loser_criteria():
    for m, n in [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3)]:
        for P in all_profiles(m, n):
            w = instant_runoff(P, m)
            for a in range(m):
                if 2 * sum(1 for r in P if r[0] == a) > n:
                    assert w == a
            assert w != condorcet_loser(P, m)
            assert w in put_winners(P, m)


def test_axioms_by_brute_force():
    for m, n in [(3, 3), (3, 4), (4, 2), (4, 3)]:
        assert check_anonymity(instant_runoff, m, n) is None
        assert check_pareto(instant_runoff, m, n) is None
        assert check_neutrality(put_winners, m, n) is None
    # The resolute rule with the fixed tie-break is not neutral.
    assert check_neutrality(instant_runoff, 3, 2) is not None


def test_two_candidates_is_majority_rule():
    for n in range(1, 8):
        for P in all_profiles(2, n):
            k = sum(1 for r in P if r[0] == 0)
            assert instant_runoff(P, 2) == (0 if 2 * k >= n else 1)
        assert find_manipulation(instant_runoff, 2, n) is None


def test_not_condorcet_consistent():
    # The center squeeze: b beats a and c in pairs, but has the fewest first places.
    P = ((A, B, C),) * 2 + ((B, A, C),) + ((C, B, A),) * 2
    assert condorcet_winner(P, 3) == B
    assert instant_runoff_rounds(P, 3) == (A, [([2, 1, 2], B), ([3, 0, 2], -1)])
    found = check_condorcet_consistency(instant_runoff, 3, 3)
    assert found is not None and instant_runoff(found[0], 3) != found[1]


def test_not_monotone():
    # With 3 candidates, the smallest failure of monotonicity by a one-place raise has 7
    # voters, and it goes through a tie.
    for n in range(1, 7):
        assert check_monotonicity(instant_runoff, 3, n, profiles=multisets(3, n)) is None
    P, Q, w = check_monotonicity(instant_runoff, 3, 7, profiles=multisets(3, 7))
    assert instant_runoff(P, 3) == w != instant_runoff(Q, 3)
    # A failure with no ties: 6 a > b > c, 2 b > a > c, 4 b > c > a, 5 c > a > b. a wins.
    # If the 2 voters b > a > c move a to the top, b drops below c and c wins.
    P = ((A, B, C),) * 6 + ((B, A, C),) * 2 + ((B, C, A),) * 4 + ((C, A, B),) * 5
    Q = ((A, B, C),) * 8 + ((B, C, A),) * 4 + ((C, A, B),) * 5
    assert instant_runoff_rounds(P, 3) == (A, [([6, 6, 5], C), ([11, 6, 0], -1)])
    assert instant_runoff_rounds(Q, 3) == (C, [([8, 4, 5], B), ([8, 0, 9], -1)])


def test_no_show_paradox():
    # 2 a > c > b, 4 b > c > a, 3 c > b > a: c wins. Two more voters a > c > b make b win,
    # and they prefer c to b, so they do better by staying home.
    P = ((A, C, B),) * 2 + ((B, C, A),) * 4 + ((C, B, A),) * 3
    assert instant_runoff_rounds(P, 3) == (C, [([2, 4, 3], A), ([0, 4, 5], -1)])
    Q = P + ((A, C, B),) * 2
    assert instant_runoff_rounds(Q, 3) == (B, [([4, 4, 3], C), ([4, 7, 0], -1)])
    assert prefers((A, C, B), C, B)


def test_manipulable():
    P, i, s = find_manipulation(instant_runoff, 3, 3)
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], instant_runoff(Q, 3), instant_runoff(P, 3))


def test_renaming_and_put_on_ties():
    # With 3 voters and one first place each, the tie rule decides; the parallel-universe
    # correspondence returns every candidate.
    P = ((A, B, C), (B, C, A), (C, A, B))
    assert put_winners(P, 3) == {A, B, C}
    pi = (2, 0, 1)
    assert put_winners(permute_profile(P, pi), 3) == {pi[a] for a in put_winners(P, 3)}
