# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plurality-voting/. The authors are listed in prov/WM09B3.jsonl.

import itertools
import math
import random
from collections import Counter

import agtprefs
from agtprefs import (all_profiles, all_rankings, check_anonymity, check_condorcet_consistency,
                      check_monotonicity, check_neutrality, check_pareto, condorcet_winner,
                      find_manipulation, is_single_peaked_on, kendall_tau, lex_tiebreak, margins,
                      pairwise, permute_profile, position, prefers, random_approval_profile,
                      random_profile, weak_condorcet_winners)
from plurality_voting import plurality, plurality_scores, plurality_winners

A, B, C, D = 0, 1, 2, 3

# The worked example of the page: 4 voters a > b > c, 3 voters b > c > a, 2 voters c > b > a.
EXAMPLE = ((A, B, C),) * 4 + ((B, C, A),) * 3 + ((C, B, A),) * 2
CYCLE = ((A, B, C), (B, C, A), (C, A, B))


# ---------------------------------------------------------------- the shared helper


def test_helper_counts_rankings_and_profiles():
    for m in range(0, 6):
        rs = all_rankings(m)
        assert len(rs) == math.factorial(m)
        assert len(set(rs)) == len(rs)
        assert rs == sorted(rs)
    assert sum(1 for _ in all_profiles(3, 2)) == 36
    assert sum(1 for _ in all_profiles(2, 3)) == 8


def test_helper_condorcet_cycle_check_value():
    M = margins(CYCLE, 3)
    assert M[A][B] == 1 and M[B][C] == 1 and M[C][A] == 1
    assert M[B][A] == -1 and M[C][B] == -1 and M[A][C] == -1
    assert condorcet_winner(CYCLE, 3) is None
    assert weak_condorcet_winners(CYCLE, 3) == frozenset()


def test_helper_pairwise_matches_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        m, n = rng.randint(1, 5), rng.randint(0, 6)
        P = random_profile(rng, m, n)
        N = pairwise(P, m)
        M = margins(P, m)
        for a in range(m):
            assert N[a][a] == 0
            for b in range(m):
                if a != b:
                    assert N[a][b] == sum(1 for r in P if prefers(r, a, b))
                    assert N[a][b] + N[b][a] == n
                    assert M[a][b] == -M[b][a]
        cw = [a for a in range(m) if all(2 * N[a][b] > n for b in range(m) if b != a)]
        assert condorcet_winner(P, m) == (cw[0] if cw else None)
        weak = {a for a in range(m) if all(2 * N[a][b] >= n for b in range(m) if b != a)}
        assert weak_condorcet_winners(P, m) == weak
        if cw:
            assert weak == {cw[0]}


def test_helper_positions_kendall_and_tiebreak():
    rng = random.Random(12)
    for _ in range(300):
        m = rng.randint(1, 6)
        r1 = tuple(rng.sample(range(m), m))
        r2 = tuple(rng.sample(range(m), m))
        for a in range(m):
            assert r1[position(r1, a)] == a
        want = sum(1 for a, b in itertools.combinations(range(m), 2)
                   if prefers(r1, a, b) != prefers(r2, a, b))
        assert kendall_tau(r1, r2) == want == kendall_tau(r2, r1)
        assert kendall_tau(r1, r1) == 0
        assert kendall_tau(r1, tuple(reversed(r1))) == m * (m - 1) // 2
    assert lex_tiebreak({3, 1, 2}) == 1


def _single_peaked_brute(r, axis):
    where = {a: i for i, a in enumerate(axis)}
    peak = where[r[0]]
    for x, y in itertools.permutations(r, 2):
        px, py = where[x], where[y]
        # On one side of the peak, the candidate closer to the peak must be preferred.
        if (py < px <= peak or peak <= px < py) and not prefers(r, x, y):
            return False
    return True


def test_helper_single_peaked_matches_definition():
    for m in range(1, 6):
        for axis in itertools.permutations(range(m)):
            if m == 5 and axis != tuple(range(m)):
                continue
            count = 0
            for r in all_rankings(m):
                ok = is_single_peaked_on((r,), axis)
                assert ok == _single_peaked_brute(r, axis)
                count += ok
            # A known count: 2^(m - 1) rankings are single-peaked on a fixed axis.
            assert count == 2 ** (m - 1)
    assert is_single_peaked_on(((1, 0, 2), (2, 1, 0)), (0, 1, 2))
    assert not is_single_peaked_on(((1, 0, 2), (0, 2, 1)), (0, 1, 2))


def test_helper_random_profiles_and_permutation():
    rng = random.Random(13)
    P = random_profile(rng, 4, 50)
    assert len(P) == 50 and all(sorted(r) == [0, 1, 2, 3] for r in P)
    Q = random_approval_profile(random.Random(14), 5, 400, 0.3)
    assert all(isinstance(b, frozenset) and b <= set(range(5)) for b in Q)
    share = sum(len(b) for b in Q) / (5 * 400)
    assert abs(share - 0.3) < 0.05
    assert random_profile(random.Random(7), 3, 5) == random_profile(random.Random(7), 3, 5)
    pi = (2, 0, 1)
    assert permute_profile(((0, 1, 2),), pi) == ((2, 0, 1),)
    assert permute_profile((frozenset({0, 2}),), pi) == (frozenset({2, 1}),)


def dictator(P, m):
    return P[0][0] if P else 0


def constant(P, m):
    return 0


def test_helper_checkers_on_dictatorship_and_constant_rule():
    for m, n in [(3, 2), (3, 3), (2, 3)]:
        # A dictatorship is neutral, Pareto, monotone and strategyproof, but not anonymous.
        assert check_anonymity(dictator, m, n) is not None
        assert check_neutrality(dictator, m, n) is None
        assert check_pareto(dictator, m, n) is None
        assert check_monotonicity(dictator, m, n) is None
        assert find_manipulation(dictator, m, n) is None
        # A constant rule is anonymous, monotone and strategyproof, but not neutral or Pareto.
        assert check_anonymity(constant, m, n) is None
        assert check_neutrality(constant, m, n) is not None
        assert check_pareto(constant, m, n) is not None
        assert check_monotonicity(constant, m, n) is None
        assert find_manipulation(constant, m, n) is None
    # With 3 voters, voter 0 can be outvoted by a majority that prefers b to the dictator's a.
    P, c = check_condorcet_consistency(dictator, 3, 3)
    assert condorcet_winner(P, 3) == c != P[0][0]


def test_helper_counterexamples_are_real():
    P, Q = check_anonymity(dictator, 3, 2)
    assert sorted(P) == sorted(Q) and dictator(P, 3) != dictator(Q, 3)
    P, pi = check_neutrality(constant, 3, 2)
    assert constant(permute_profile(P, pi), 3) != pi[constant(P, 3)]
    P, a, b = check_pareto(constant, 3, 2)
    assert b == 0 and all(prefers(r, a, b) for r in P)

    def anti_plurality_top(P, m):  # elects the candidate with the fewest first places
        s = plurality_scores(P, m)
        return min(range(m), key=lambda a: (s[a], a))

    P, Q, w = check_monotonicity(anti_plurality_top, 3, 2)
    assert anti_plurality_top(P, 3) == w != anti_plurality_top(Q, 3)
    P, i, s = find_manipulation(anti_plurality_top, 3, 2)
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], anti_plurality_top(Q, 3), anti_plurality_top(P, 3))


# ---------------------------------------------------------------- plurality voting


def test_worked_example():
    assert plurality_scores(EXAMPLE, 3) == [4, 3, 2]
    assert plurality(EXAMPLE, 3) == A
    # b is the Condorcet winner, and the plurality winner a is the Condorcet loser.
    assert condorcet_winner(EXAMPLE, 3) == B
    M = margins(EXAMPLE, 3)
    assert M[A][B] == -1 and M[A][C] == -1 and M[B][C] == 5
    # The two voters c > b > a gain by voting b > c > a.
    lie = ((A, B, C),) * 4 + ((B, C, A),) * 5
    assert plurality(lie, 3) == B


def test_matches_counter_on_random_profiles():
    rng = random.Random(21)
    for _ in range(2000):
        m, n = rng.randint(1, 6), rng.randint(0, 12)
        P = random_profile(rng, m, n)
        tops = Counter(r[0] for r in P)
        s = plurality_scores(P, m)
        assert s == [tops[a] for a in range(m)]
        assert sum(s) == n
        best = max(s)
        W = {a for a in range(m) if tops[a] == best}
        assert plurality_winners(P, m) == W
        assert plurality(P, m) == min(W)


def test_edge_cases():
    assert plurality((), 3) == 0 and plurality_winners((), 3) == {0, 1, 2}
    assert plurality(((0,),), 1) == 0
    assert plurality(((2, 1, 0), (1, 2, 0)), 3) == 1  # a tie of 1 and 2 goes to 1
    assert plurality_winners(CYCLE, 3) == {A, B, C} and plurality(CYCLE, 3) == A


def test_axioms_by_brute_force():
    for m, n in [(3, 3), (3, 4), (4, 2)]:
        assert check_anonymity(plurality, m, n) is None
        assert check_anonymity(plurality_winners, m, n) is None
        assert check_neutrality(plurality_winners, m, n) is None
        assert check_pareto(plurality, m, n) is None
        assert check_monotonicity(plurality, m, n) is None
        assert check_monotonicity(plurality_winners, m, n) is None
    # The resolute rule with the fixed tie-break is not neutral.
    P, pi = check_neutrality(plurality, 3, 2)
    assert plurality(permute_profile(P, pi), 3) != pi[plurality(P, 3)]


def test_failures_by_search():
    # Not Condorcet consistent, and open to manipulation, for 3 candidates.
    P, c = check_condorcet_consistency(plurality, 3, 3)
    assert plurality(P, 3) != c
    P, i, s = find_manipulation(plurality, 3, 3)
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], plurality(Q, 3), plurality(P, 3))
    # With 3 candidates, a Condorcet loser can win alone (no tie) only with 7 or more voters.
    def condorcet_loser(P, m):
        M = margins(P, m)
        losers = [a for a in range(m) if all(M[a][b] < 0 for b in range(m) if b != a)]
        return losers[0] if losers else None

    def loser_wins_alone(P):
        W = plurality_winners(P, 3)
        return len(W) == 1 and condorcet_loser(P, 3) in W

    for n in range(1, 7):
        assert not any(loser_wins_alone(P) for P in all_profiles(3, n))
    smallest = ((A, B, C),) * 3 + ((B, C, A),) * 2 + ((C, B, A),) * 2
    assert loser_wins_alone(smallest)
    # With the tie-break, 3 voters suffice: a, b and c each have one first place, and a wins.
    tied = ((A, B, C), (B, C, A), (C, B, A))
    assert plurality(tied, 3) == A == condorcet_loser(tied, 3)


def test_consistency_by_brute_force():
    # If two groups of voters have overlapping winner sets, the joined group elects the overlap.
    for n1, n2 in [(1, 1), (1, 2), (2, 2)]:
        groups1 = list(all_profiles(3, n1))
        groups2 = list(all_profiles(3, n2))
        checked = 0
        for P1 in groups1:
            W1 = plurality_winners(P1, 3)
            for P2 in groups2:
                both = W1 & plurality_winners(P2, 3)
                if both:
                    assert plurality_winners(P1 + P2, 3) == both
                    checked += 1
        assert checked > 0


def test_two_candidates_is_majority_rule():
    for n in range(1, 8):
        for P in all_profiles(2, n):
            k = sum(1 for r in P if r[0] == 0)
            assert plurality(P, 2) == (0 if 2 * k >= n else 1)
        assert find_manipulation(plurality, 2, n) is None
        assert check_condorcet_consistency(plurality, 2, n) is None


def test_helper_module_has_no_rule():
    names = {x for x in dir(agtprefs) if not x.startswith("_")}
    assert not any("plurality" in x or "borda" in x for x in names)
