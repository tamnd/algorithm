# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr-parse-table/. The authors are listed in prov/B3QKMP.jsonl.

import itertools
import random

import pytest

from lr_parse_table import END, ParseError, build_table, lr_parse

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


def test_expression_grammar_tables():
    with pytest.raises(ValueError):
        build_table(EXPR, "E", "nope")
    t0 = build_table(EXPR, "E", "lr0")
    assert len(t0.action) == 12 and len(t0.conflicts) > 0
    slr = build_table(EXPR, "E", "slr")
    assert len(slr.action) == 12 and slr.conflicts == []
    lr1 = build_table(EXPR, "E", "lr1")
    assert len(lr1.action) == 22 and lr1.conflicts == []
    n_action = sum(len(r) for r in slr.action)
    n_goto = sum(len(r) for r in slr.goto)
    assert (n_action, n_goto) == (36, 9)
    toks = ["id", "+", "id", "*", "id"]
    for t in (slr, lr1):
        tree = lr_parse(t, toks)
        check_tree(EXPR, "E", tree, toks)
        assert tree[1][1] == "+"
        for bad, pos in ((["id", "id"], 1), (["+"], 0), (["id", "+"], 2), ([], 0),
                         (["(", "id", "$", ")"], 2)):
            with pytest.raises(ParseError) as e:
                lr_parse(t, bad)
            assert e.value.position == pos
    with pytest.raises(ValueError):
        lr_parse(t0, toks)


def test_lookahead_classes():
    # LR(1) but not SLR(1): the textbook L = R grammar
    g = [("S", ("L", "=", "R")), ("S", ("R",)), ("L", ("*", "R")), ("L", ("id",)), ("R", ("L",))]
    assert build_table(g, "S", "slr").conflicts
    assert build_table(g, "S", "lr1").conflicts == []
    # empty productions and the empty input
    g2 = [("S", ("a", "S", "b")), ("S", ())]
    assert build_table(g2, "S", "lr0").conflicts
    t = build_table(g2, "S", "slr")
    assert lr_parse(t, []) == ("S", [])
    check_tree(g2, "S", lr_parse(t, ["a", "a", "b", "b"]), ["a", "a", "b", "b"])


def test_deep_input_has_no_recursion_limit():
    t = build_table(EXPR, "E", "slr")
    n = 100000
    toks = ["("] * n + ["id"] + [")"] * n
    check_tree(EXPR, "E", lr_parse(t, toks), toks)


def test_random_against_brute_force():
    rng = random.Random(7741)
    terms = ["a", "b"]
    counts = {"lr0": 0, "slr": 0, "lr1": 0}
    for _ in range(2500):
        prods = productive_only(random_grammar(rng, rng.randint(1, 4), terms))
        if not any(a == "S" for a, _ in prods):
            continue
        tables = {k: build_table(prods, "S", k) for k in counts}
        ok = {k: not t.conflicts for k, t in tables.items()}
        # each method accepts at least the grammars of the weaker one
        assert ok["slr"] or not ok["lr0"]
        assert ok["lr1"] or not ok["slr"]
        bound = 6
        lang = lang_upto(prods, bound)
        prefixes = prefix_lang(prods, bound + 1)["S"]
        for k, t in tables.items():
            if not ok[k]:
                continue
            counts[k] += 1
            for m in range(bound + 1):
                for w in itertools.product(terms, repeat=m):
                    if w in lang["S"]:
                        check_tree(prods, "S", lr_parse(t, list(w)), w)
                    else:
                        with pytest.raises(ParseError) as e:
                            lr_parse(t, list(w))
                        i = e.value.position
                        assert w[:i] in prefixes, (k, prods, w, i)
                        assert w[:i + 1] not in prefixes or i == len(w), (k, prods, w, i)
    assert min(counts.values()) >= 500, counts
