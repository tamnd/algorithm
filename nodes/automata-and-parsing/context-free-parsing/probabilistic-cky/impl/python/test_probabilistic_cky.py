# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-cky/. The authors are listed in prov/W4N6QS.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from probabilistic_cky import (
    best_chart,
    check_cnf,
    inside_probability,
    tree_probability,
    tree_yield,
    viterbi_cky,
)

ASTRO = [
    ("S", ("NP", "VP"), F(1)),
    ("PP", ("P", "NP"), F(1)),
    ("VP", ("V", "NP"), F(7, 10)),
    ("VP", ("VP", "PP"), F(3, 10)),
    ("P", ("with",), F(1)),
    ("V", ("saw",), F(1)),
    ("NP", ("NP", "PP"), F(4, 10)),
    ("NP", ("astronomers",), F(1, 10)),
    ("NP", ("ears",), F(18, 100)),
    ("NP", ("saw",), F(4, 100)),
    ("NP", ("stars",), F(18, 100)),
    ("NP", ("telescopes",), F(1, 10)),
]


def all_trees(rules, start, w):
    """Brute force: enumerate every leftmost derivation of w, with an explicit stack.

    In Chomsky normal form no symbol other than an empty start derives the empty
    string, so a sentential form longer than w can be dropped. Returns the list
    of the probabilities of the derivations, one per parse tree.
    """
    nts = {a for a, _, _ in rules}
    by_lhs = {}
    for a, rhs, q in rules:
        by_lhs.setdefault(a, []).append((rhs, q))
    n = len(w)
    out = []
    stack = [((start,), 1)]
    while stack:
        form, p = stack.pop()
        k = 0
        while k < len(form) and form[k] not in nts:
            k += 1
        if tuple(form[:k]) != tuple(w[:k]):
            continue
        if k == len(form):
            if len(form) == n:
                out.append(p)
            continue
        for rhs, q in by_lhs[form[k]]:
            new = form[:k] + rhs + form[k + 1:]
            if len(new) <= n or (n == 0 and len(new) == 0):
                stack.append((new, p * q))
    return out


def random_grammar(rng):
    """A random weighted grammar in CNF over the nonterminals S, A, B, C and the terminals a, b.

    It may be ambiguous, left or right recursive, have S on right sides, or have
    S -> epsilon (only when S is on no right side). The weights are proper
    probabilities most of the time and arbitrary nonnegative weights otherwise.
    """
    nts = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    allow_s_rhs = rng.random() < 0.5
    rhs_nts = nts if allow_s_rhs else [x for x in nts if x != "S"] or ["S"]
    if not allow_s_rhs and rhs_nts == ["S"]:
        allow_s_rhs = True
    shapes = []
    for a in nts:
        for t in "ab":
            if rng.random() < 0.5:
                shapes.append((a, (t,)))
        for b, c in itertools.product(rhs_nts, repeat=2):
            if rng.random() < 0.3:
                shapes.append((a, (b, c)))
    if not allow_s_rhs and rng.random() < 0.4:
        shapes.append(("S", ()))
    if rng.random() < 0.2 and shapes:
        shapes.append(rng.choice(shapes))  # a duplicate production
    proper = rng.random() < 0.8
    weights = [F(rng.randint(0, 6), 1) if not proper else F(rng.randint(1, 6)) for _ in shapes]
    rules = []
    if proper:
        total = {}
        for (a, _), q in zip(shapes, weights):
            total[a] = total.get(a, 0) + q
        for (a, rhs), q in zip(shapes, weights):
            rules.append((a, rhs, q / total[a]))
    else:
        for (a, rhs), q in zip(shapes, weights):
            rules.append((a, rhs, q / 3))
    # Make sure every right-side nonterminal is a left side, as CNF requires here.
    lhs = {a for a, _, _ in rules}
    return [r for r in rules if all(x in lhs or x in "ab" for x in r[1])]


def check_answer(rules, start, w, got_p, got_tree, trees):
    if not trees or max(trees) == 0:
        assert got_tree is None or got_p == 0
        return
    want = max(trees)
    assert got_p == want
    assert got_tree is not None
    assert got_tree[0] == start
    assert tree_yield(got_tree) == list(w)
    assert tree_probability(rules, got_tree) == want


def test_random_grammars_against_enumeration():
    rng = random.Random(20261106)
    comparisons = 0
    nonempty = 0
    while comparisons < 3000:
        rules = random_grammar(rng)
        try:
            check_cnf(rules, "S")
        except ValueError:
            continue
        if not any(a == "S" for a, _, _ in rules):
            continue
        for n in range(0, 6):
            for w in itertools.product("ab", repeat=n):
                if n >= 4 and rng.random() < 0.6:
                    continue
                trees = all_trees(rules, "S", w)
                p, tree = viterbi_cky(rules, "S", w)
                check_answer(rules, "S", w, p, tree, trees)
                assert inside_probability(rules, "S", w) == sum(trees, F(0))
                if trees and max(trees) > 0:
                    nonempty += 1
                    lp, ltree = viterbi_cky(rules, "S", w, log_space=True)
                    assert math.isclose(lp, math.log(max(trees)), rel_tol=1e-9, abs_tol=1e-9)
                    assert tree_yield(ltree) == list(w)
                comparisons += 1
    assert nonempty > 200


def test_astronomers_example():
    w = "astronomers saw stars with ears".split()
    p, tree = viterbi_cky(ASTRO, "S", w)
    assert p == F(9072, 10**7)
    assert inside_probability(ASTRO, "S", w) == F(15876, 10**7)
    assert p / inside_probability(ASTRO, "S", w) == F(4, 7)
    # The best tree attaches "with ears" to "stars".
    vp = tree[1][1]
    assert vp[0] == "VP" and vp[1][0][0] == "V" and vp[1][1][0] == "NP"
    assert vp[1][1][1][0][0] == "NP" and vp[1][1][1][1][0] == "PP"
    chart = best_chart(ASTRO, "S", w)
    assert chart[1][2] == {"VP": F(126, 1000)}
    assert chart[3][4] == {"PP": F(18, 100)}
    assert chart[0][2] == {"S": F(126, 10**4)}
    assert chart[2][4] == {"NP": F(1296, 10**5)}
    assert chart[1][4] == {"VP": F(9072, 10**6)}
    assert chart[0][1] == {} and chart[0][3] == {}
    assert chart[0][4] == {"S": F(9072, 10**7)}
    assert len(all_trees(ASTRO, "S", w)) == 2


def test_floats_match_fractions():
    floats = [(a, r, float(q)) for a, r, q in ASTRO]
    w = "astronomers saw stars with ears".split()
    p, _ = viterbi_cky(floats, "S", w)
    assert math.isclose(p, 0.0009072)


def test_empty_input():
    g = [("S", (), F(1, 4)), ("S", ("A", "A"), F(3, 4)), ("A", ("a",), F(1))]
    assert viterbi_cky(g, "S", []) == (F(1, 4), ("S", ()))
    assert inside_probability(g, "S", []) == F(1, 4)
    g2 = [("S", ("a",), F(1))]
    assert viterbi_cky(g2, "S", []) == (0, None)
    assert viterbi_cky(g2, "S", [], log_space=True) == (-math.inf, None)
    assert inside_probability(g2, "S", []) == 0


def test_no_parse():
    g = [("S", ("A", "B"), F(1)), ("A", ("a",), F(1)), ("B", ("b",), F(1))]
    assert viterbi_cky(g, "S", list("ba")) == (0, None)
    assert viterbi_cky(g, "S", list("abc")) == (0, None)
    assert viterbi_cky(g, "S", list("ab")) == (F(1), ("S", (("A", ("a",)), ("B", ("b",)))))


def test_rejects_non_cnf():
    bad = [
        [("S", ("A",), F(1)), ("A", ("a",), F(1))],  # unit production
        [("S", ("A", "A"), F(1)), ("A", (), F(1))],  # empty production of a non-start symbol
        [("S", ("a", "S"), F(1, 2)), ("S", ("a",), F(1, 2))],  # terminal in a binary rule
        [("S", ("S", "S"), F(1, 2)), ("S", (), F(1, 2))],  # S -> epsilon with S on a right side
        [("S", ("a",), F(-1))],  # negative probability
        [("S", ("A", "B", "C"), F(1))],  # long right side
    ]
    for g in bad:
        with pytest.raises(ValueError):
            viterbi_cky(g, "S", ["a"])


def test_ties_and_ambiguity():
    # S -> S S | a with equal halves: every binary tree of a^n has the same probability.
    g = [("S", ("S", "S"), F(1, 2)), ("S", ("a",), F(1, 2))]
    catalan = [1, 1, 2, 5, 14, 42]
    for n in range(1, 7):
        p, tree = viterbi_cky(g, "S", ["a"] * n)
        assert p == F(1, 2) ** (2 * n - 1)
        assert inside_probability(g, "S", ["a"] * n) == catalan[n - 1] * p
        assert tree_yield(tree) == ["a"] * n


def test_log_space_avoids_underflow():
    # A right-branching grammar: S -> A S | a with tiny lexical probabilities.
    g = [("S", ("A", "S"), 0.5), ("S", ("a",), 0.5), ("A", ("a",), 1e-3)]
    n = 150
    w = ["a"] * n
    p, _ = viterbi_cky(g, "S", w)
    assert p == 0.0  # the product 0.5^150 * 1e-447 underflows a double
    lp, tree = viterbi_cky(g, "S", w, log_space=True)
    want = (n - 1) * (math.log(0.5) + math.log(1e-3)) + math.log(0.5)
    assert math.isclose(lp, want, rel_tol=1e-12)
    depth, t = 0, tree
    while len(t[1]) == 2:
        t = t[1][1]
        depth += 1
    assert depth == n - 1
    assert tree_yield(tree) == w
