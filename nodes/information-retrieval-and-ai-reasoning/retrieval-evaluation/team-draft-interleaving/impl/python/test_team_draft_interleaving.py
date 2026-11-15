# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/team-draft-interleaving/. The authors are listed in prov/8FBQBW.jsonl.

import itertools
import random
from fractions import Fraction

from team_draft_interleaving import credit, interleave


def coins_from(bits):
    it = iter(bits)
    return lambda: next(it)


def outcomes(a, b):
    """All results of the coin, as (probability, shown, team_a, team_b), by enumeration."""
    n = len(set(a) | set(b))
    rounds = (n + 1) // 2 + 1
    dist = {}
    for bits in itertools.product((0, 1), repeat=rounds):
        shown, ta, tb = interleave(a, b, coins_from(bits))
        key = (tuple(shown), frozenset(ta))
        p, _, _ = dist.get(key, (Fraction(0), ta, tb))
        dist[key] = (p + Fraction(1, 2**rounds), ta, tb)
    return [(p, list(key[0]), ta, tb) for key, (p, ta, tb) in dist.items()]


def oracle(a, b, bits):
    """Round by round: a coin picks the captain who chooses first in the round."""
    shown, ta, tb = [], set(), set()
    k = 0

    def pick(lst, team):
        d = next(x for x in lst if x not in shown)
        shown.append(d)
        team.add(d)

    def both_left():
        return any(x not in shown for x in a) and any(x not in shown for x in b)

    while both_left():
        first = bits[k]
        k += 1
        order = [(a, ta), (b, tb)] if first == 1 else [(b, tb), (a, ta)]
        pick(*order[0])
        if both_left():
            pick(*order[1])
    return shown, ta, tb


def click_sets(shown, prob):
    for pat in itertools.product((0, 1), repeat=len(shown)):
        p = Fraction(1)
        for i, bit in enumerate(pat):
            q = prob(i, shown[i])
            p *= q if bit else 1 - q
        if p:
            yield {shown[i] for i in range(len(shown)) if pat[i]}, p


def expected_outcome(a, b, prob):
    total = Fraction(0)
    for q, shown, ta, tb in outcomes(a, b):
        for clicked, p in click_sets(shown, prob):
            total += q * p * credit(ta, tb, clicked)
    return total


def pbm(rel, eps):
    return lambda i, d: Fraction(1, i + 1) * (1 if rel[d] else eps)


def dominates(a, b, rel):
    ca = cb = 0
    strict = False
    for x, y in zip(a, b):
        ca += rel[x]
        cb += rel[y]
        if ca < cb:
            return False
        strict = strict or ca > cb
    return strict


def test_paper_example():
    a = list("abcdgh")
    b = list("beafgh")
    shown, ta, tb = interleave(a, b, coins_from([1, 1, 1, 1]))
    assert shown == list("abcedfgh")
    assert ta == set("acdg") and tb == set("befh")
    assert credit(ta, tb, {"b", "e"}) == -1


def test_trace_on_page():
    a = list("abcd")
    b = list("bcda")
    shown, ta, tb = interleave(a, b, coins_from([1, 0]))
    assert shown == list("abcd")
    assert ta == {"a", "d"} and tb == {"b", "c"}
    wins = Fraction(0)
    for q, shown, ta, tb in outcomes(a, b):
        assert [credit(ta, tb, {d}) for d in shown].count(1) == 2
        wins += q * sum(credit(ta, tb, {d}) for d in shown)
    assert wins == 0


def test_edge_cases():
    assert interleave([], ["x"], coins_from([])) == ([], set(), set())
    assert interleave(["x"], ["x"], coins_from([0])) == (["x"], set(), {"x"})
    assert interleave(["x"], ["y", "z"], coins_from([1])) == (["x"], {"x"}, set())
    shown, ta, tb = interleave(["x"], ["y", "z"], coins_from([0]))
    assert shown == ["y", "x"] and ta == {"x"} and tb == {"y"}
    assert credit({"x"}, {"y"}, set()) == 0


def test_pairs_of_positions_and_coin_symmetry_up_to_five():
    """Positions 2m-1 and 2m hold one document of each team, and over the coins each
    position goes to a with probability exactly 1/2."""
    for n in range(1, 6):
        perms = list(itertools.permutations(range(n)))
        for a in perms:
            for b in perms:
                share = [Fraction(0)] * n
                for q, shown, ta, tb in outcomes(a, b):
                    assert len(shown) == n
                    for m in range(0, n - 1, 2):
                        assert (shown[m] in ta) != (shown[m + 1] in ta)
                    for i, d in enumerate(shown):
                        if d in ta:
                            share[i] += q
                assert all(s == Fraction(1, 2) for s in share)


def test_random_clicks_give_a_tie_in_expectation():
    """Any click model on positions that ignores the documents gives expected outcome 0."""
    for n in range(1, 5):
        perms = list(itertools.permutations(range(n)))
        for a in perms:
            for b in perms:
                dist = outcomes(a, b)
                for pat in itertools.product((0, 1), repeat=n):
                    e = Fraction(0)
                    for q, shown, ta, tb in dist:
                        e += q * credit(ta, tb, {shown[i] for i in range(n) if pat[i]})
                    assert e == 0


def test_dominating_ranking_never_loses():
    for n in range(1, 5):
        docs = list(range(n))
        for rels in itertools.product((0, 1), repeat=n):
            rel = dict(zip(docs, rels))
            for a in itertools.permutations(docs):
                for b in itertools.permutations(docs):
                    if dominates(a, b, rel):
                        for eps in ((0, Fraction(1, 5)) if n <= 3 else (0,)):
                            assert expected_outcome(list(a), list(b), pbm(rel, eps)) >= 0


def test_insensitive_case():
    """Hofmann, Whiteson and de Rijke: only d3 is relevant, l2 ranks it higher, yet a tie."""
    l1, l2 = ["d1", "d2", "d3"], ["d2", "d3", "d1"]
    rel = {"d1": 0, "d2": 0, "d3": 1}
    assert dominates(l2, l1, rel)
    assert expected_outcome(l2, l1, pbm(rel, 0)) == 0
    assert expected_outcome(l2, l1, pbm(rel, Fraction(1, 5))) == 0


def test_clear_winner():
    a = list("abcd")
    b = list("dcba")
    rel = {"a": 1, "b": 1, "c": 0, "d": 0}
    assert expected_outcome(a, b, pbm(rel, 0)) > 0


def test_random_against_oracle():
    rng = random.Random(9)
    for _ in range(1000):
        universe = list(range(rng.randint(1, 8)))
        a = rng.sample(universe, rng.randint(0, len(universe)))
        b = rng.sample(universe, rng.randint(0, len(universe)))
        bits = [rng.randint(0, 1) for _ in range(10)]
        shown, ta, tb = interleave(a, b, coins_from(bits))
        assert (shown, ta, tb) == oracle(a, b, bits)
        assert ta | tb == set(shown) and not ta & tb
        clicked = set(rng.sample(shown, rng.randint(0, len(shown))))
        h = len(clicked & ta) - len(clicked & tb)
        assert credit(ta, tb, clicked) == (h > 0) - (h < 0)
