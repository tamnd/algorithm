# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operator-precedence-parsing/. The authors are listed in prov/G04W13.jsonl.

import itertools
import random

import pytest

from operator_precedence_parsing import ParseError, build_precedence, op_parse

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


def random_operator_grammar(rng, n_nt, terms):
    names = ["S", "A", "B"][:n_nt]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = rng.randint(1, 4)
            rhs = []
            for _ in range(k):
                if rhs and rhs[-1] in names:
                    rhs.append(rng.choice(terms))
                else:
                    rhs.append(rng.choice(names + terms))
            prods.append((a, tuple(rhs)))
    return prods


def test_expression_grammar():
    t = build_precedence(EXPR, "E")
    assert t.rel[("+", "*")] == "<" and t.rel[("*", "+")] == ">"
    assert t.rel[("+", "+")] == ">" and t.rel[("(", ")")] == "="
    assert ("id", "id") not in t.rel
    assert len(t.rel) == 29
    w = "id * id + id".split()
    tree = op_parse(EXPR, "E", w, t)
    check_tree(EXPR, "E", tree, w)
    assert tree[1][0][0] == "E" and tree[1][1] == "+"
    for bad, pos in [(["id", "id"], 1), (["+"], 1), ([], 0), (["(", "id"], 2), (["id", "+"], 2)]:
        with pytest.raises(ParseError) as e:
            op_parse(EXPR, "E", bad, t)
        assert e.value.position == pos


def test_refused_grammars():
    amb = [("E", ("E", "+", "E")), ("E", ("E", "*", "E")), ("E", ("id",))]
    unary = [("E", ("E", "-", "T")), ("E", ("T",)), ("T", ("-", "T")), ("T", ("id",))]
    adjacent = [("E", ("E", "A", "E")), ("E", ("id",)), ("A", ("+",))]
    empty = [("S", ("a", "S", "b")), ("S", ())]
    for g, s in [(amb, "E"), (unary, "E"), (adjacent, "E"), (empty, "S")]:
        with pytest.raises(ValueError):
            build_precedence(g, s)


def test_units_and_same_right_sides():
    g = [("S", ("A",)), ("S", ("B",)), ("A", ("a",)), ("B", ("a",)), ("A", ("A", "b"))]
    tree = op_parse(g, "S", ["a", "b", "b"])
    check_tree(g, "S", tree, ["a", "b", "b"])
    cyc = [("S", ("A",)), ("A", ("S",)), ("A", ("a",))]
    check_tree(cyc, "S", op_parse(cyc, "S", ["a"]), ["a"])


def test_deep_nesting():
    m = 100000
    w = ["("] * m + ["id"] + [")"] * m
    tree = op_parse(EXPR, "E", w)
    check_tree(EXPR, "E", tree, w)


def test_random_against_brute_force():
    rng = random.Random(20261106)
    grammars = 0
    strings = 0
    for _ in range(4000):
        terms = ["a", "b", "c"][: rng.randint(1, 3)]
        prods = random_operator_grammar(rng, rng.randint(1, 3), terms)
        try:
            table = build_precedence(prods, "S")
        except ValueError:
            continue
        lang = lang_upto(prods, 5)["S"]
        grammars += bool(lang)
        for m in range(6):
            for w in itertools.product(terms, repeat=m):
                strings += 1
                try:
                    tree = op_parse(prods, "S", list(w), table)
                except ParseError as e:
                    assert w not in lang
                    assert 0 <= e.position <= len(w)
                    continue
                assert w in lang
                check_tree(prods, "S", tree, w)
    assert grammars >= 500 and strings >= 5000
