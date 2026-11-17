# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/over-representation-analysis/. The authors are listed in prov/4AHTW8.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from biostoch import hypergeom_pmf
from over_representation_analysis import bh_adjust, hypergeom_upper_tail, ora


def test_matches_enumeration_of_all_selections():
    # The null: every n-subset of the universe is equally likely to be the list.
    for total in range(1, 8):
        for good in range(total + 1):
            members = set(range(good))
            for draws in range(total + 1):
                counts = {}
                for sub in itertools.combinations(range(total), draws):
                    k = len(members.intersection(sub))
                    counts[k] = counts.get(k, 0) + 1
                n_sub = math.comb(total, draws)
                for k in range(-1, draws + 2):
                    brute = Fraction(sum(c for x, c in counts.items() if x >= k), n_sub)
                    assert hypergeom_upper_tail(k, total, good, draws) == brute


def test_equals_one_sided_fisher_from_two_binomials():
    # Condition two independent binomials with the same p on their sum: the
    # conditional law of the first is hypergeometric, for every p.
    for total, good, draws in [(7, 3, 4), (10, 4, 5), (9, 2, 6)]:
        for p in (Fraction(1, 3), Fraction(3, 4)):
            def b(n, i):
                return math.comb(n, i) * p ** i * (1 - p) ** (n - i)
            joint = {i: b(good, i) * b(total - good, draws - i)
                     for i in range(max(0, draws - total + good), min(good, draws) + 1)}
            z = sum(joint.values())
            for k in range(draws + 1):
                cond = sum(v for i, v in joint.items() if i >= k) / z
                assert hypergeom_upper_tail(k, total, good, draws) == cond


def test_agrees_with_the_shared_pmf():
    rng = random.Random(51)
    for _ in range(100):
        total = rng.randint(1, 3000)
        good = rng.randint(0, total)
        draws = rng.randint(0, total)
        k = rng.randint(0, min(good, draws))
        tail = sum(hypergeom_pmf(i, total, good, draws) for i in range(k, min(good, draws) + 1))
        assert math.isclose(float(hypergeom_upper_tail(k, total, good, draws)), tail,
                            rel_tol=1e-8, abs_tol=1e-300)


def test_bh_adjust():
    q = bh_adjust([0.01, 0.04, 0.03, 0.2])
    for x, y in zip(q, [0.04, 0.16 / 3, 0.16 / 3, 0.2]):
        assert math.isclose(x, y, rel_tol=1e-12)
    assert bh_adjust([]) == []
    assert bh_adjust([0.9, 0.8]) == [0.9, 0.9]


def test_page_example():
    universe = ["g%d" % i for i in range(1, 21)]
    selected = ["g1", "g2", "g3", "g4", "g5", "x1"]
    sets = {"A": ["g1", "g2", "g3", "g6"], "B": ["g4", "g7", "g8", "g9", "g10", "g11"],
            "C": ["g12", "g13", "y1"]}
    res = ora(selected, universe, sets)
    assert (res["A"]["k"], res["A"]["K"]) == (3, 4)
    assert res["A"]["p"] == float(Fraction(31, 969))
    assert (res["B"]["k"], res["B"]["K"]) == (1, 6)
    assert res["C"]["K"] == 2 and res["C"]["p"] == 1.0
    assert math.isclose(res["A"]["expected"], 1.0)
    assert ora(selected, universe, sets, min_size=3).keys() == {"A", "B"}


def test_universe_cuts_the_list_and_the_sets():
    full = ora(["a", "b", "z"], ["a", "b", "c", "d"], {"S": ["a", "b", "q"]})
    assert full["S"]["k"] == 2 and full["S"]["K"] == 2
    assert full["S"]["p"] == float(Fraction(1, 6))


def test_errors():
    with pytest.raises(ValueError):
        hypergeom_upper_tail(1, 3, 4, 1)
