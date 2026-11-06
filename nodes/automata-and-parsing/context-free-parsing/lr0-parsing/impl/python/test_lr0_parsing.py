# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr0-parsing/. The authors are listed in prov/37Z7NT.jsonl.

import itertools
import random

import pytest

from lr0_parsing import END, ParseError, build_lr0, lr0_parse

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


def test_list_example():
    # L -> L , x | x is LR(0) once S' -> L $ is used
    g = [("L", ("L", ",", "x")), ("L", ("x",))]
    t = build_lr0(g, "L")
    assert len(t.states) == 6
    toks = ["x", ",", "x", ",", "x"]
    tree = lr0_parse(g, "L", toks, t)
    check_tree(g, "L", tree, toks)
    assert tree == ("L", [("L", [("L", ["x"]), ",", "x"]), ",", "x"])
    for bad, pos in ((["x", "x"], 1), ([",", "x"], 0), (["x", ","], 2), ([], 0),
                     (["x", "$", "x"], 1)):
        with pytest.raises(ParseError) as e:
            lr0_parse(g, "L", bad, t)
        assert e.value.position == pos


def test_conflicts_are_refused():
    expr = [("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("T", "*", "F")), ("T", ("F",)),
            ("F", ("(", "E", ")")), ("F", ("id",))]
    with pytest.raises(ValueError):
        build_lr0(expr, "E")
    with pytest.raises(ValueError):  # right recursion needs lookahead
        build_lr0([("L", ("x", ",", "L")), ("L", ("x",))], "L")
    with pytest.raises(ValueError):  # ambiguous
        build_lr0([("E", ("E", "+", "E")), ("E", ("a",))], "E")
    with pytest.raises(ValueError):  # a cycle of unit productions
        build_lr0([("S", ("A",)), ("A", ("S",)), ("A", ("a",))], "S")


def test_empty_productions_and_empty_input():
    g = [("S", ("A", "a")), ("A", ())]
    tree = lr0_parse(g, "S", ["a"])
    assert tree == ("S", [("A", []), "a"])
    g2 = [("S", ("S", "a")), ("S", ())]
    assert lr0_parse(g2, "S", []) == ("S", [])
    assert lr0_parse(g2, "S", ["a", "a"]) == ("S", [("S", [("S", []), "a"]), "a"])
    with pytest.raises(ValueError):  # reduce S -> ε or shift a: needs lookahead
        build_lr0([("S", ("a", "S", "b")), ("S", ())], "S")


def test_deep_input_has_no_recursion_limit():
    g = [("S", ("(", "S", ")")), ("S", ("x",))]
    n = 200000
    toks = ["("] * n + ["x"] + [")"] * n
    tree = lr0_parse(g, "S", toks)
    check_tree(g, "S", tree, toks)


def test_random_against_brute_force():
    rng = random.Random(4127)
    terms = ["a", "b"]
    tested = 0
    for _ in range(6000):
        prods = productive_only(random_grammar(rng, rng.randint(1, 4), terms))
        if not any(a == "S" for a, _ in prods):
            continue
        try:
            table = build_lr0(prods, "S")
        except ValueError:
            continue
        tested += 1
        bound = 6
        lang = lang_upto(prods, bound)
        prefixes = prefix_lang(prods, bound + 1)["S"]
        for m in range(bound + 1):
            for w in itertools.product(terms, repeat=m):
                if w in lang["S"]:
                    check_tree(prods, "S", lr0_parse(prods, "S", list(w), table), w)
                else:
                    with pytest.raises(ParseError) as e:
                        lr0_parse(prods, "S", list(w), table)
                    i = e.value.position
                    # valid prefix property: the tokens before the error start a sentence
                    assert w[:i] in prefixes, (prods, w, i)
                    assert w[:i + 1] not in prefixes or i == len(w), (prods, w, i)
    assert tested >= 500
