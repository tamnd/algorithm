# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll-parse-table/. The authors are listed in prov/3BZN2A.jsonl.

import itertools
import random

import pytest

from ll_parse_table import END, LLParseTable

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
    """Oracle: for each symbol, the strings of length <= max_len that it derives."""
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


def ll1_recognize(table, tokens):
    """A small driver used only by the tests: True when the table accepts tokens."""
    stack = [END, table.start]
    toks = list(tokens) + [END]
    i = 0
    steps = 0
    while True:
        steps += 1
        assert steps < 10000
        x = stack.pop()
        a = toks[i]
        if x == END:
            return a == END
        if x not in table.nonterminals:
            if x != a:
                return False
            i += 1
            continue
        p = table.lookup(x, a)
        if p is None:
            return False
        stack.extend(reversed(table.productions[p][1]))


def random_grammar(rng, n_nt, terms, eps_prob=0.2):
    names = ["S", "A", "B", "C"][:n_nt]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = 0 if rng.random() < eps_prob else rng.randint(1, 3)
            prods.append((a, tuple(rng.choice(names + terms) for _ in range(k))))
    return prods


def useful(prods, start):
    """Remove the symbols that derive no terminal string or are not reachable."""
    lang = lang_upto(prods, 0)
    prod_ok = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in prod_ok and all(x in prod_ok or x not in lang for x in rhs):
                prod_ok.add(a)
                changed = True
    p1 = [(a, r) for a, r in prods if a in prod_ok and all(x in prod_ok or x not in lang for x in r)]
    reach = {start}
    changed = True
    while changed:
        changed = False
        for a, r in p1:
            if a in reach:
                for x in r:
                    if x not in reach:
                        reach.add(x)
                        changed = True
    return [(a, r) for a, r in p1 if a in reach]


def min_lengths(prods):
    """The length of a shortest terminal string that each productive nonterminal derives."""
    nts = {a for a, _ in prods}
    best = {}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if all(x in best or x not in nts for x in rhs):
                v = sum(best[x] if x in nts else 1 for x in rhs)
                if a not in best or v < best[a]:
                    best[a] = v
                    changed = True
    return best


def left_recursive(prods, null):
    nts = {a for a, _ in prods}
    edge = {a: set() for a in nts}
    for a, r in prods:
        for x in r:
            if x in nts:
                edge[a].add(x)
            if x not in null:
                break
    for a in nts:
        seen, todo = set(), list(edge[a])
        while todo:
            b = todo.pop()
            if b == a:
                return True
            if b not in seen:
                seen.add(b)
                todo.extend(edge[b])
    return False


def test_example_table():
    t = LLParseTable(EXPR, "E")
    t.check_invariant()
    assert t.null == {"E'", "T'"}
    assert t.first["E"] == t.first["T"] == t.first["F"] == {"(", "id"}
    assert t.follow["E"] == t.follow["E'"] == {")", END}
    assert t.follow["T"] == t.follow["T'"] == {"+", ")", END}
    assert t.follow["F"] == {"+", "*", ")", END}
    expected = {
        ("E", "id"): 0, ("E", "("): 0,
        ("E'", "+"): 1, ("E'", ")"): 2, ("E'", END): 2,
        ("T", "id"): 3, ("T", "("): 3,
        ("T'", "+"): 5, ("T'", "*"): 4, ("T'", ")"): 5, ("T'", END): 5,
        ("F", "id"): 7, ("F", "("): 6,
    }
    assert {k: v[0] for k, v in t.cells.items()} == expected
    assert t.is_ll1() and t.lookup("E", "+") is None
    assert ll1_recognize(t, ["id", "+", "id", "*", "id"])
    assert not ll1_recognize(t, ["id", "+"])


def test_conflicts_and_edges():
    left = [("E", ("E", "+", "a")), ("E", ("a",))]
    t = LLParseTable(left, "E")
    assert t.conflicts() == [("E", "a")]
    with pytest.raises(ValueError):
        t.lookup("E", "a")
    amb = [("S", ("a", "S")), ("S", ("a",))]
    assert LLParseTable(amb, "S").conflicts() == [("S", "a")]
    dangling = [("S", ("i", "S", "E")), ("S", ("x",)), ("E", ("e", "S")), ("E", ())]
    assert LLParseTable(dangling, "S").conflicts() == [("E", "e")]
    only_eps = LLParseTable([("S", ())], "S")
    assert only_eps.lookup("S", END) == 0 and ll1_recognize(only_eps, [])
    unit = LLParseTable([("S", ("A",)), ("A", ("a",))], "S")
    assert unit.is_ll1() and ll1_recognize(unit, ["a"]) and not ll1_recognize(unit, [])
    with pytest.raises(ValueError):
        LLParseTable([("S", ("$",))], "S")


def test_random_against_oracles():
    rng = random.Random(4127)
    terms = ["a", "b"]
    n_ll1 = 0
    for _ in range(600):
        prods = random_grammar(rng, rng.randint(1, 3), terms)
        t = LLParseTable(prods, "S")
        t.check_invariant()
        lang = lang_upto(prods, 6)
        for a in t.nonterminals:
            assert (a in t.null) == (() in lang[a])
            seen = {w[0] for w in lang[a] if w}
            assert seen <= t.first[a]
        # FOLLOW from below: mark one occurrence of A with a fresh terminal
        for a in t.nonterminals:
            marked = lang_upto(prods + [(a, ("#",))], 6)["S"]
            for w in marked:
                for i, x in enumerate(w):
                    if x == "#":
                        nxt = w[i + 1] if i + 1 < len(w) else END
                        if nxt != "#":
                            assert nxt in t.follow[a]
        red = useful(prods, "S")
        if red and left_recursive(red, t.null):
            assert not LLParseTable(red, "S").is_ll1()
        if t.is_ll1():
            n_ll1 += 1
            for m in range(6):
                for w in itertools.product(terms, repeat=m):
                    assert ll1_recognize(t, w) == (w in lang["S"]), (prods, w)
    assert n_ll1 > 50


def test_first_exact_on_small_grammars():
    # On a grammar without useless symbols, FIRST(A) is exactly the set of first letters of L(A).
    rng = random.Random(77)
    checked = 0
    for _ in range(400):
        prods = useful(random_grammar(rng, 2, ["a", "b"]), "S")
        if not prods:
            continue
        t = LLParseTable(prods, "S")
        m = max([1] + list(min_lengths(prods).values()))
        r = max(len(rhs) for _, rhs in prods)
        bound = 1 + len(t.nonterminals) * max(r - 1, 0) * m
        if bound > 7:
            continue
        lang = lang_upto(prods, bound)
        for a in t.nonterminals:
            assert t.first[a] == {w[0] for w in lang[a] if w}
        checked += 1
    assert checked > 100
