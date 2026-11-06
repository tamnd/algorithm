# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parse-chart/. The authors are listed in prov/37Y8RW.jsonl.

import itertools
import random

import pytest

from parse_chart import ParseError, chart_parse, fill_chart

EXPR = [
    ("E", ("E", "+", "T")),
    ("E", ("T",)),
    ("T", ("T", "*", "F")),
    ("T", ("F",)),
    ("F", ("(", "E", ")")),
    ("F", ("id",)),
]

def lang_upto(prods, max_len):
    """Oracle: for each nonterminal, the strings of length <= max_len that it derives."""
    nts = {a for a, _ in prods}
    lang = {a: set() for a in nts}

    def of(x):
        return lang[x] if x in nts else {(x,)}

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            cur = {()}
            for x in rhs:
                cur = {u + v for u in cur for v in of(x) if len(u) + len(v) <= max_len}
                if not cur:
                    break
            if not cur <= lang[a]:
                lang[a] |= cur
                changed = True
    return lang


def prefix_lang(prods, max_len):
    """Oracle: for each nonterminal, the prefixes of length <= max_len of the strings it derives.

    Every nonterminal must be productive, so that each symbol after a prefix can be completed.
    """
    nts = {a for a, _ in prods}
    full = lang_upto(prods, max_len)
    pre = {a: set() for a in nts}

    def full_of(x):
        return full[x] if x in nts else {(x,)}

    def pre_of(x):
        return pre[x] if x in nts else {(), (x,)}

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            new = {()}
            cur = {()}
            for x in rhs:
                new |= {u + v for u in cur for v in pre_of(x) if len(u) + len(v) <= max_len}
                cur = {u + v for u in cur for v in full_of(x) if len(u) + len(v) <= max_len}
            if not new <= pre[a]:
                pre[a] |= new
                changed = True
    return pre


def productive_only(prods):
    """Remove the productions that use a nonterminal deriving no terminal string."""
    nts = {a for a, _ in prods}
    good = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in good and all(x in good or x not in nts for x in rhs):
                good.add(a)
                changed = True
    return [(a, r) for a, r in prods if a in good and all(x in good or x not in nts for x in r)]


def check_tree(prods, start, tree, tokens):
    """Iteratively check that tree is a parse tree of tokens with root start."""
    nts = {a for a, _ in prods}
    rules = set(prods)
    assert isinstance(tree, tuple) and tree[0] == start
    leaves = []
    todo = [tree]
    while todo:
        t = todo.pop()
        if isinstance(t, str):
            assert t not in nts
            leaves.append(t)
            continue
        a, kids = t
        labels = tuple(k if isinstance(k, str) else k[0] for k in kids)
        assert (a, labels) in rules
        todo.extend(reversed(kids))
    assert leaves == list(tokens)


def random_grammar(rng, n_nt, terms, eps_prob=0.2):
    names = ["S", "A", "B", "C"][:n_nt]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = 0 if rng.random() < eps_prob else rng.randint(1, 3)
            prods.append((a, tuple(rng.choice(names + terms) for _ in range(k))))
    return prods


def derives(lang, nts, symbols, max_len):
    """The strings of length <= max_len derived by a string of symbols."""
    cur = {()}
    for x in symbols:
        opts = lang[x] if x in nts else {(x,)}
        cur = {u + v for u in cur for v in opts if len(u) + len(v) <= max_len}
    return cur


def test_expression_chart():
    w = "id + id * id".split()
    chart = fill_chart(EXPR, "E", w)
    tree = chart_parse(EXPR, "E", w)
    check_tree(EXPR, "E", tree, w)
    assert [j for j, _ in chart.complete(0, "E")] == [1, 3, 5] or sorted(j for j, _ in chart.complete(0, "E")) == [1, 3, 5]
    assert sorted(j for j, _ in chart.complete(2, "T")) == [3, 5]
    with pytest.raises(ParseError) as e:
        chart_parse(EXPR, "E", ["id", "+", ")", "id"])
    assert e.value.position == 2
    with pytest.raises(ParseError) as e:
        chart_parse(EXPR, "E", [])
    assert e.value.position == 0


def test_empty_cycles_and_ambiguity():
    g = [("S", ("A", "S", "b")), ("S", ()), ("A", ("a",)), ("A", ())]
    for w in [[], ["b"], ["a", "b", "b"], ["a", "a", "b", "b"]]:
        check_tree(g, "S", chart_parse(g, "S", w), w)
    cyc = [("S", ("S",)), ("S", ("S", "S")), ("S", ()), ("S", ("a",))]
    for m in range(6):
        w = ["a"] * m
        check_tree(cyc, "S", chart_parse(cyc, "S", w), w)


def test_long_input():
    g = [("L", ("L", ",", "x")), ("L", ("x",))]
    m = 20000
    w = ["x"] + [",", "x"] * m
    tree = chart_parse(g, "L", w)
    check_tree(g, "L", tree, w)
    assert len(fill_chart(g, "L", w)) < 10 * len(w)
    right = [("R", ("x", ",", "R")), ("R", ("x",))]
    w = ["x"] + [",", "x"] * 500  # right recursion fills a quadratic chart
    check_tree(right, "R", chart_parse(right, "R", w), w)


def test_random_against_brute_force():
    rng = random.Random(20261106)
    checked = 0
    for _ in range(1500):
        terms = ["a", "b"][: rng.randint(1, 2)]
        prods = productive_only(random_grammar(rng, rng.randint(1, 3), terms))
        nts = {a for a, _ in prods}
        if "S" not in nts:
            continue
        lang = lang_upto(prods, 5)
        pre = prefix_lang(prods, 6)["S"]
        for m in range(6):
            for w in itertools.product(terms, repeat=m):
                checked += 1
                chart = fill_chart(prods, "S", list(w))
                for (i, j, (p, d)) in chart.back:
                    assert w[i:j] in derives(lang, nts, prods[p][1][:d], 5)
                try:
                    tree = chart_parse(prods, "S", list(w))
                except ParseError as e:
                    assert w not in lang["S"]
                    i = e.position
                    assert w[:i] in pre and (i == len(w) or w[: i + 1] not in pre)
                    continue
                assert w in lang["S"]
                check_tree(prods, "S", tree, w)
    assert checked >= 20000
