# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranked-pairs/. The authors are listed in prov/XQFZVT.jsonl.

import random
from itertools import combinations, permutations

from agtprefs import (all_rankings, check_anonymity, check_condorcet_consistency,
                      check_monotonicity, check_neutrality, check_pareto, condorcet_winner,
                      find_manipulation, margins, permute_profile, prefers, random_profile)
from ranked_pairs import locked_edges, margin_matrix, pair_order, ranked_pairs, ranked_pairs_ranking

A, B, C, D = 0, 1, 2, 3

# The worked example of the page: 26 voters in four groups.
EXAMPLE = ((A, B, C, D),) * 3 + ((C, D, A, B),) * 6 + ((B, C, D, A),) * 11 + ((C, A, B, D),) * 6


def smith_set(P, m):
    M = margins(P, m)
    for size in range(1, m + 1):
        for S in combinations(range(m), size):
            if all(M[a][b] > 0 for a in S for b in range(m) if b not in S):
                return frozenset(S)
    return frozenset()


def naive_ranked_pairs(P, m, tiebreak):
    """Lock pairs one by one and test for a cycle by a fresh depth-first search each time."""
    M = margins(P, m)
    place = {a: i for i, a in enumerate(tiebreak)}
    pairs = sorted(((x, y) for x in range(m) for y in range(m) if x != y and M[x][y] >= 0),
                   key=lambda e: (-M[e[0]][e[1]], place[e[0]], place[e[1]]))
    succ = {x: set() for x in range(m)}

    def reaches(u, v):
        seen, stack = {u}, [u]
        while stack:
            z = stack.pop()
            if z == v:
                return True
            for w in succ[z]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        return False

    for x, y in pairs:
        if not reaches(y, x):
            succ[x].add(y)
    return tuple(sorted(range(m), key=lambda x: -sum(reaches(x, y) for y in range(m))))


def stack_rankings(P, m, tiebreak):
    """All rankings with the stack property of Zavist and Tideman, by brute force."""
    M = margins(P, m)
    place = {a: i for i, a in enumerate(tiebreak)}

    def key(x, y):
        return (-M[x][y], place[x], place[y])

    out = []
    for r in all_rankings(m):
        ok = True
        for i in range(m):
            for j in range(i + 1, m):
                bound = key(r[j], r[i])
                reach = {i}
                for t in range(i + 1, j + 1):
                    if any(key(r[s], r[t]) <= bound for s in reach):
                        reach.add(t)
                if j not in reach:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(r)
    return out


def rp_all_tiebreaks(P, m):
    """The winners of ranked pairs over every tie-breaking ranking of the candidates."""
    return frozenset(ranked_pairs(P, m, t) for t in permutations(range(m)))


def test_example():
    M = margin_matrix(EXAMPLE, 4)
    assert M[A][B] == 4 and M[C][A] == 20 and M[D][A] == 8
    assert M[B][C] == 2 and M[B][D] == 14 and M[C][D] == 26
    assert condorcet_winner(EXAMPLE, 4) is None
    assert [(x, y) for _, x, y in pair_order(M, (0, 1, 2, 3))] == [(C, D), (C, A), (B, D), (D, A),
                                                                   (A, B), (B, C)]
    assert locked_edges(EXAMPLE, 4) == [(C, D), (C, A), (B, D), (D, A), (B, C)]
    assert ranked_pairs_ranking(EXAMPLE, 4) == (B, C, D, A)
    assert ranked_pairs(EXAMPLE, 4) == B
    assert rp_all_tiebreaks(EXAMPLE, 4) == frozenset({B})


def test_edge_cases():
    assert ranked_pairs_ranking((), 1) == (0,)
    assert ranked_pairs_ranking((), 3) == (0, 1, 2)
    assert ranked_pairs_ranking((), 3, (2, 0, 1)) == (2, 0, 1)
    assert ranked_pairs_ranking(((2, 0, 1),), 3) == (2, 0, 1)
    cycle = ((A, B, C), (B, C, A), (C, A, B))
    assert ranked_pairs_ranking(cycle, 3) == (A, B, C)
    # With the tie-break c, b, a the pairs are locked in the order (c, a), (b, c), (a, b).
    assert ranked_pairs_ranking(cycle, 3, (2, 1, 0)) == (B, C, A)


def test_matches_naive_and_stack_property():
    rng = random.Random(1)
    for _ in range(250):
        m, n = rng.randint(1, 5), rng.randint(0, 8)
        P = random_profile(rng, m, n)
        t = tuple(rng.sample(range(m), m))
        r = ranked_pairs_ranking(P, m, t)
        assert r == naive_ranked_pairs(P, m, t)
        assert sorted(r) == list(range(m))
        for x, y in locked_edges(P, m, t):
            assert prefers(r, x, y)
        if m <= 4:
            assert stack_rankings(P, m, t) == [r]


def test_smith_set_comes_first():
    rng = random.Random(2)
    for _ in range(300):
        m, n = rng.randint(1, 6), rng.randint(1, 9)
        P = random_profile(rng, m, n)
        S = smith_set(P, m)
        r = ranked_pairs_ranking(P, m, tuple(rng.sample(range(m), m)))
        assert set(r[:len(S)]) == S


def test_axioms_on_full_domains():
    for m, n in ((2, 3), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2)):
        assert check_anonymity(ranked_pairs, m, n) is None
        assert check_pareto(ranked_pairs, m, n) is None
        assert check_condorcet_consistency(ranked_pairs, m, n) is None
        assert check_monotonicity(ranked_pairs, m, n) is None
        assert check_neutrality(rp_all_tiebreaks, m, n) is None


def test_axioms_on_random_profiles():
    for m, n, seed in ((4, 5, 3), (5, 6, 4), (6, 7, 5)):
        rng = random.Random(seed)
        Ps = [random_profile(rng, m, n) for _ in range(120)]
        assert check_anonymity(ranked_pairs, m, n, Ps) is None
        assert check_pareto(ranked_pairs, m, n, Ps) is None
        assert check_condorcet_consistency(ranked_pairs, m, n, Ps) is None
        assert check_monotonicity(ranked_pairs, m, n, Ps) is None


def test_neutral_when_the_tie_break_is_renamed():
    rng = random.Random(6)
    for _ in range(300):
        m, n = rng.randint(1, 6), rng.randint(0, 8)
        P = random_profile(rng, m, n)
        t = tuple(rng.sample(range(m), m))
        pi = tuple(rng.sample(range(m), m))
        r = ranked_pairs_ranking(P, m, t)
        renamed = ranked_pairs_ranking(permute_profile(P, pi), m, tuple(pi[a] for a in t))
        assert renamed == tuple(pi[a] for a in r)


def test_resolute_rule_is_not_neutral():
    assert ranked_pairs(((A, B), (B, A)), 2) == A
    assert check_neutrality(ranked_pairs, 2, 2) is not None


def test_manipulation_exists():
    found = find_manipulation(ranked_pairs, 3, 3)
    assert found is not None
    P, i, s = found
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], ranked_pairs(Q, 3), ranked_pairs(P, 3))


def test_large_input():
    rng = random.Random(7)
    P = random_profile(rng, 40, 25)
    r = ranked_pairs_ranking(P, 40)
    assert sorted(r) == list(range(40))
    M = margin_matrix(P, 40)
    assert all(M[a][b] == -M[b][a] for a in range(40) for b in range(40))
