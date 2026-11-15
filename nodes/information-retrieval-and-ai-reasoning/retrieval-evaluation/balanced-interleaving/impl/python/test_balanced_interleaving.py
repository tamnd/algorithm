# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-interleaving/. The authors are listed in prov/8GEA8G.jsonl.

import itertools
import random
from fractions import Fraction

from balanced_interleaving import credit, interleave


def oracle_interleave(a, b, a_first):
    """Closed form: step t touches a at odd t (a first) and b at even t, and the
    loop runs min(2|a| - 1, 2|b|) steps. A document goes in at its first touch."""
    first, second = (a, b) if a_first else (b, a)
    steps = min(2 * len(first) - 1, 2 * len(second))
    touch = {}
    for t in range(1, steps + 1):
        d = first[(t - 1) // 2] if t % 2 == 1 else second[t // 2 - 1]
        touch.setdefault(d, t)
    return sorted(touch, key=touch.get)


def oracle_credit(a, b, shown, clicked):
    if not clicked:
        return 0
    low = max(clicked, key=shown.index)
    k = next(j for j in range(1, max(len(a), len(b)) + 1) if (j <= len(a) and a[j - 1] == low) or (j <= len(b) and b[j - 1] == low))
    ha = len(set(a[:k]) & set(clicked))
    hb = len(set(b[:k]) & set(clicked))
    return (ha > hb) - (ha < hb)


def click_sets(shown, prob):
    """All click sets of a model where position i is clicked with prob(i, doc), independently."""
    n = len(shown)
    for pat in itertools.product((0, 1), repeat=n):
        p = Fraction(1)
        for i, bit in enumerate(pat):
            q = prob(i, shown[i])
            p *= q if bit else 1 - q
        if p:
            yield {shown[i] for i in range(n) if pat[i]}, p


def expected_outcome(a, b, prob):
    total = Fraction(0)
    for a_first in (True, False):
        shown = interleave(a, b, a_first)
        for clicked, p in click_sets(shown, prob):
            total += Fraction(1, 2) * p * credit(a, b, shown, clicked)
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


def test_paper_figure_example():
    a = list("abcdgh")
    b = list("beafgh")
    assert interleave(a, b, True) == list("abecdfgh")
    assert interleave(a, b, False) == list("baecfdgh")
    for a_first in (True, False):
        assert credit(a, b, interleave(a, b, a_first), {"b", "e"}) == -1


def test_trace_on_page():
    a = list("abcd")
    b = list("bcda")
    assert interleave(a, b, True) == list("abcd")
    assert interleave(a, b, False) == list("bacd")


def test_edge_cases():
    assert interleave([], ["x"], True) == []
    assert interleave(["x"], ["x"], False) == ["x"]
    assert interleave(["x"], ["y", "z"], True) == ["x"]
    assert interleave(["x"], ["y", "z"], False) == ["y", "x"]
    assert credit(["x"], ["y"], ["x", "y"], set()) == 0
    assert credit(["x", "y"], ["y", "x"], ["x", "y"], {"x", "y"}) == 0


def test_prefix_property_all_pairs_up_to_five():
    """Each prefix of the shown list is the union of a top ka of a and a top kb of b, |ka - kb| <= 1."""
    for n in range(1, 6):
        docs = list(range(n))
        perms = list(itertools.permutations(docs))
        for a in perms:
            for b in perms:
                for a_first in (True, False):
                    shown = interleave(a, b, a_first)
                    assert sorted(shown) == docs
                    for m in range(len(shown) + 1):
                        top = set(shown[:m])
                        assert any(
                            top == set(a[:ka]) | set(b[:kb])
                            for ka in range(n + 1)
                            for kb in range(max(0, ka - 1), min(n, ka + 1) + 1)
                        )


def test_bias_example_of_radlinski_kurup_joachims():
    """a = (a, b, c, d), b = (b, c, d, a), one click on a uniformly random shown document."""
    a = list("abcd")
    b = list("bcda")
    wins = {1: Fraction(0), -1: Fraction(0), 0: Fraction(0)}
    for a_first in (True, False):
        shown = interleave(a, b, a_first)
        for d in shown:
            wins[credit(a, b, shown, {d})] += Fraction(1, 2) * Fraction(1, len(shown))
    assert wins[-1] == Fraction(3, 4)
    assert wins[1] == Fraction(1, 4)


def test_dominance_without_noise_three_documents():
    """With clicks only on relevant documents, a dominating ranking never loses for n <= 3."""
    for n in range(1, 4):
        docs = list(range(n))
        for rels in itertools.product((0, 1), repeat=n):
            rel = dict(zip(docs, rels))
            for a in itertools.permutations(docs):
                for b in itertools.permutations(docs):
                    if dominates(a, b, rel):
                        assert expected_outcome(list(a), list(b), pbm(rel, 0)) >= 0


def test_dominating_ranking_can_lose():
    """The cases on the page where balanced interleaving prefers the dominated ranking."""
    a, b = list("bcad"), list("cadb")
    rel = {"a": 0, "b": 1, "c": 1, "d": 1}
    assert dominates(a, b, rel)
    assert expected_outcome(a, b, pbm(rel, 0)) == Fraction(-1, 16)
    a, b = list("abc"), list("bca")
    rel = {"a": 1, "b": 1, "c": 0}
    assert dominates(a, b, rel)
    assert expected_outcome(a, b, pbm(rel, 0)) == 0
    assert expected_outcome(a, b, pbm(rel, Fraction(1, 5))) == Fraction(-1, 60)


def test_clear_winner():
    a = list("abcd")
    b = list("dcba")
    rel = {"a": 1, "b": 1, "c": 0, "d": 0}
    assert expected_outcome(a, b, pbm(rel, 0)) > 0
    assert expected_outcome(b, a, pbm(rel, 0)) < 0


def test_random_against_oracle():
    rng = random.Random(8)
    for _ in range(800):
        universe = list(range(rng.randint(1, 8)))
        a = rng.sample(universe, rng.randint(0, len(universe)))
        b = rng.sample(universe, rng.randint(0, len(universe)))
        a_first = rng.random() < 0.5
        shown = interleave(a, b, a_first)
        assert shown == oracle_interleave(a, b, a_first)
        if shown:
            clicked = set(rng.sample(shown, rng.randint(0, len(shown))))
            assert credit(a, b, shown, clicked) == oracle_credit(a, b, shown, clicked)
