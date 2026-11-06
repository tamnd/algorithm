# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inside-outside-algorithm/. The authors are listed in prov/9H2A1G.jsonl.

"""Tests for the inside-outside algorithm against enumeration of all parse trees."""

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from inside_outside_algorithm import (em_step, expected_counts, inside_chart,
                                      outside_chart)

EXAMPLE = {
    ("S", ("S", "S")): Fraction(1, 2),
    ("S", ("a",)): Fraction(1, 2),
}


def all_trees(theta, start, w):
    """Every parse tree of w, as (probability, Counter of rules, list of
    (A, i, j) nodes). Plain enumeration over spans; only for short w."""
    if not w:
        p = theta.get((start, ()), 0)
        return [(p, Counter({(start, ()): 1}), [])] if p else []
    memo = {}

    def trees(a, i, j):
        key = (a, i, j)
        if key in memo:
            return memo[key]
        out = []
        for (lhs, rhs), p in theta.items():
            if lhs != a or p == 0:
                continue
            if len(rhs) == 1 and j == i + 1 and rhs[0] == w[i]:
                out.append((p, Counter({(lhs, rhs): 1}), [(a, i, j)]))
            if len(rhs) == 2:
                for k in range(i + 1, j):
                    for pl, cl, nl in trees(rhs[0], i, k):
                        for pr, cr, nr in trees(rhs[1], k, j):
                            out.append((p * pl * pr, cl + cr + Counter({(lhs, rhs): 1}),
                                        [(a, i, j)] + nl + nr))
        memo[key] = out
        return out

    return trees(start, 0, len(w))


def random_pcfg(rng, with_eps):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    inner = [x for x in names if x != "S"] if with_eps else names
    weights = {}
    for a in names:
        rules = set()
        rules.add((rng.choice("ab"),))
        if inner:
            for _ in range(rng.randint(0, 3)):
                rules.add((rng.choice(inner), rng.choice(inner)))
        if a == "S" and with_eps:
            rules.add(())
            if not inner:
                rules.add(("b",))
        for rhs in rules:
            weights[(a, rhs)] = Fraction(rng.randint(1, 4))
    theta = {}
    for (a, rhs), wgt in weights.items():
        tot = sum(v for (b, _), v in weights.items() if b == a)
        theta[(a, rhs)] = wgt / tot
    return theta


def test_example_from_the_page():
    w = ["a", "a", "a"]
    z, counts = expected_counts(EXAMPLE, "S", w)
    assert z == Fraction(1, 16)
    assert counts[("S", ("S", "S"))] == 2
    assert counts[("S", ("a",))] == 3
    inside = inside_chart(EXAMPLE, "S", w)
    assert inside[0][2]["S"] == Fraction(1, 8)
    outside = outside_chart(EXAMPLE, "S", inside, 3)
    assert outside[0][1]["S"] == Fraction(1, 8)
    assert outside[1][2]["S"] == Fraction(1, 8)
    new, lik = em_step(EXAMPLE, "S", [w])
    assert lik == [Fraction(1, 16)]
    assert new[("S", ("S", "S"))] == Fraction(2, 5)
    assert new[("S", ("a",))] == Fraction(3, 5)


def test_random_grammars_match_tree_enumeration():
    rng = random.Random(20261106)
    checked = 0
    positive = 0
    for _ in range(600):
        with_eps = rng.random() < 0.3
        theta = random_pcfg(rng, with_eps)
        w = [rng.choice("ab") for _ in range(rng.randint(0, 5))]
        trees = all_trees(theta, "S", w)
        z_brute = sum(p for p, _, _ in trees)
        z, counts = expected_counts(theta, "S", w)
        assert z == z_brute
        if z:
            positive += 1
            brute = Counter()
            for p, c, _ in trees:
                for r, m in c.items():
                    brute[r] += p * m / z
            assert dict(brute) == counts
            if w:
                n = len(w)
                inside = inside_chart(theta, "S", w)
                outside = outside_chart(theta, "S", inside, n)
                spans = Counter()
                for p, _, nodes in trees:
                    for node in nodes:
                        spans[node] += p
                for i in range(n):
                    for j in range(i + 1, n + 1):
                        for a in {x for x, _ in theta}:
                            got = inside[i][j].get(a, 0) * outside[i][j].get(a, 0)
                            assert got == spans[(a, i, j)]
        else:
            assert counts == {}
        checked += 1
    assert checked == 600
    assert positive > 120


def test_em_never_lowers_the_likelihood():
    rng = random.Random(99)
    runs = 0
    while runs < 60:
        theta = {r: float(p) for r, p in random_pcfg(rng, False).items()}
        corpus = [[rng.choice("ab") for _ in range(rng.randint(1, 6))] for _ in range(4)]
        _, lik = em_step(theta, "S", corpus)
        if any(z == 0 for z in lik):
            continue
        runs += 1
        last = sum(math.log(z) for z in lik)
        for _ in range(8):
            theta, lik = em_step(theta, "S", corpus)
            now = sum(math.log(z) for z in lik)
            assert now >= last - 1e-9
            last = now
        sums = Counter()
        for (a, _), p in theta.items():
            sums[a] += p
        for a, s in sums.items():
            assert abs(s - 1) < 1e-9


def test_empty_sentence_and_zero_probability():
    theta = {("S", ()): Fraction(1, 3), ("S", ("A", "A")): Fraction(2, 3), ("A", ("a",)): Fraction(1)}
    z, counts = expected_counts(theta, "S", [])
    assert z == Fraction(1, 3) and counts == {("S", ()): 1}
    z, counts = expected_counts(theta, "S", ["a"])
    assert z == 0 and counts == {}
    new, lik = em_step(theta, "S", [[], ["a", "a"], ["b"]])
    assert lik == [Fraction(1, 3), Fraction(2, 3), 0]
    assert new[("S", ())] == Fraction(1, 2) and new[("A", ("a",))] == 1


def test_rejects_grammars_outside_the_normal_form():
    with pytest.raises(ValueError):
        expected_counts({("S", ("A",)): 1.0, ("A", ("a",)): 1.0}, "S", ["a"])
    with pytest.raises(ValueError):
        expected_counts({("S", ()): 0.5, ("S", ("S", "S")): 0.5}, "S", [])


def test_long_sentence_in_floats():
    theta = {("S", ("S", "S")): 0.4, ("S", ("a",)): 0.6}
    w = ["a"] * 60
    z, counts = expected_counts(theta, "S", w)
    assert z > 0
    assert abs(counts[("S", ("a",))] - 60) < 1e-6
    assert abs(counts[("S", ("S", "S"))] - 59) < 1e-6
