# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll1-parsing/. The authors are listed in prov/DYEHVA.jsonl.

import itertools
import random

import pytest

from ll1_parsing import END, ParseError, build_table, ll1_parse

EXPR = [
    ("E", ("T", "E'")),
    ("E'", ("+", "T", "E'")),
    ("E'", ()),
    ("T", ("F", "T'")),
    ("T'", ("*", "F", "T'")),
    ("T'", ()),
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


def test_expression_example():
    toks = ["id", "+", "id", "*", "id"]
    tree = ll1_parse(EXPR, "E", toks)
    check_tree(EXPR, "E", tree, toks)
    assert tree == ("E", [("T", [("F", ["id"]), ("T'", [])]),
                          ("E'", ["+", ("T", [("F", ["id"]), ("T'", ["*", ("F", ["id"]), ("T'", [])])]),
                                  ("E'", [])])])
    with pytest.raises(ParseError) as e:
        ll1_parse(EXPR, "E", ["id", "+", ")"])
    assert e.value.position == 2
    with pytest.raises(ParseError) as e:
        ll1_parse(EXPR, "E", ["id", "id"])
    assert e.value.position == 1
    with pytest.raises(ParseError) as e:
        ll1_parse(EXPR, "E", [])
    assert e.value.position == 0
    with pytest.raises(ParseError):
        ll1_parse(EXPR, "E", ["id", END, "+", "id"])


def test_not_ll1_grammars_are_refused():
    with pytest.raises(ValueError):
        build_table([("E", ("E", "+", "a")), ("E", ("a",))], "E")  # left recursion
    with pytest.raises(ValueError):
        build_table([("S", ("i", "S", "E")), ("S", ("x",)), ("E", ("e", "S")), ("E", ())], "S")
    with pytest.raises(ValueError):
        build_table([("S", ("a", "S")), ("S", ("a",))], "S")  # needs left factoring
    with pytest.raises(ValueError):
        build_table([("S", ("S",)), ("S", ("a",))], "S")  # a cycle, so ambiguous


def test_empty_input_and_unit_productions():
    g = [("S", ("A", "B")), ("A", ("a",)), ("A", ()), ("B", ("C",)), ("C", ("b",)), ("C", ())]
    assert ll1_parse(g, "S", []) == ("S", [("A", []), ("B", [("C", [])])])
    for toks in ([], ["a"], ["b"], ["a", "b"]):
        check_tree(g, "S", ll1_parse(g, "S", toks), toks)
    with pytest.raises(ParseError):
        ll1_parse(g, "S", ["b", "a"])


def test_deep_input_has_no_recursion_limit():
    n = 200000
    toks = ["("] * n + ["id"] + [")"] * n
    tree = ll1_parse(EXPR, "E", toks)
    check_tree(EXPR, "E", tree, toks)


def test_random_against_brute_force():
    rng = random.Random(9031)
    terms = ["a", "b"]
    tested = 0
    for _ in range(3000):
        prods = productive_only(random_grammar(rng, rng.randint(1, 4), terms))
        if not any(a == "S" for a, _ in prods):
            continue
        try:
            table = build_table(prods, "S")
        except ValueError:
            continue
        tested += 1
        bound = 6
        lang = lang_upto(prods, bound)
        prefixes = prefix_lang(prods, bound + 1)["S"]
        for m in range(bound + 1):
            for w in itertools.product(terms, repeat=m):
                if w in lang["S"]:
                    check_tree(prods, "S", ll1_parse(prods, "S", list(w), table), w)
                else:
                    with pytest.raises(ParseError) as e:
                        ll1_parse(prods, "S", list(w), table)
                    i = e.value.position
                    # valid prefix property: the tokens before the error start a sentence
                    assert w[:i] in prefixes, (prods, w, i)
                    assert w[:i + 1] not in prefixes or i == len(w), (prods, w, i)
    assert tested >= 500
