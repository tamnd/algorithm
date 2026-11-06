# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earley-parser/. The authors are listed in prov/X30PDD.jsonl.

import itertools
import random

from earley_parser import earley_chart, earley_parse, earley_recognize, nullable_set

EXAMPLE = [
    ("E", ("E", "+", "T")), ("E", ("T",)),
    ("T", ("a",)), ("T", ()),
]


def derives(productions, start, w):
    """Independent oracle: least fixpoint of 'A derives w[i:j]' over all spans."""
    nts = {a for a, _ in productions}
    n = len(w)
    known = set()

    def seq(rhs, i, j):
        ends = {i}
        for x in rhs:
            nxt = set()
            for p in ends:
                if x in nts:
                    nxt |= {q for q in range(p, j + 1) if (x, p, q) in known}
                elif p < j and w[p] == x:
                    nxt.add(p + 1)
            ends = nxt
        return j in ends

    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            for i in range(n + 1):
                for j in range(i, n + 1):
                    if (a, i, j) not in known and seq(rhs, i, j):
                        known.add((a, i, j))
                        changed = True
    return (start, 0, n) in known


def naive_items(productions, start, w):
    """Independent oracle for the chart: close the three Earley rules
    (predict, scan, complete) by brute force until nothing changes."""
    nts = {a for a, _ in productions}
    n = len(w)
    items = {(p, 0, 0, 0) for p, (a, _) in enumerate(productions) if a == start}
    changed = True
    while changed:
        changed = False
        new = set()
        for p, dot, i, j in items:
            rhs = productions[p][1]
            if dot == len(rhs):
                a = productions[p][0]
                for q, qd, qi, qj in items:
                    r = productions[q][1]
                    if qj == i and qd < len(r) and r[qd] == a:
                        new.add((q, qd + 1, qi, j))
            elif rhs[dot] in nts:
                for q, (b, _) in enumerate(productions):
                    if b == rhs[dot]:
                        new.add((q, 0, j, j))
            elif j < n and w[j] == rhs[dot]:
                new.add((p, dot + 1, i, j + 1))
        if not new <= items:
            items |= new
            changed = True
    sets = [set() for _ in range(n + 1)]
    for p, dot, i, j in items:
        sets[j].add((p, dot, i))
    return sets


def tree_ok(tree, productions, start, w):
    """The tree has root start, uses only productions and its leaves spell w."""
    prods = {(a, tuple(r)) for a, r in productions}
    if tree[0] != start:
        return False
    leaves = []
    stack = [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, str):
            leaves.append(t)
            continue
        label, kids = t
        rhs = tuple(k if isinstance(k, str) else k[0] for k in kids)
        if (label, rhs) not in prods:
            return False
        stack.extend(reversed(kids))
    return leaves == list(w)


def random_grammar(rng):
    nts = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    syms = nts + ["a", "b"]
    prods = set()
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.2:
                prods.add((a, ()))
            else:
                prods.add((a, tuple(rng.choice(syms) for _ in range(rng.randint(1, 3)))))
    return sorted(prods)


def test_example_chart():
    w = ["a", "+", "a"]
    chart = earley_chart(EXAMPLE, "E", w)
    assert chart == [
        [(0, 0, 0), (1, 0, 0), (0, 1, 0), (2, 0, 0), (3, 0, 0), (1, 1, 0)],
        [(2, 1, 0), (1, 1, 0), (0, 1, 0)],
        [(0, 2, 0), (2, 0, 2), (3, 0, 2), (0, 3, 0), (0, 1, 0)],
        [(2, 1, 2), (0, 3, 0), (0, 1, 0)],
    ]
    assert earley_recognize(EXAMPLE, "E", w)
    tree = earley_parse(EXAMPLE, "E", w)
    assert tree == ("E", (("E", (("T", ("a",)),)), "+", ("T", ("a",))))


def test_edge_cases():
    g = [("S", ("a", "S")), ("S", ())]
    assert earley_recognize(g, "S", [])
    assert earley_parse(g, "S", []) == ("S", ())
    assert earley_recognize(g, "S", list("aaaa"))
    assert not earley_recognize(g, "S", ["b"])
    assert not earley_recognize([("S", ("a",))], "S", [])
    assert not earley_recognize([("A", ("a",))], "S", ["a"])
    assert earley_parse([("A", ("a",))], "S", ["a"]) is None
    assert nullable_set([("S", ("A", "B")), ("A", ()), ("B", ("A",))])[0] == {"S", "A", "B"}


def test_cycles_and_hidden_empty():
    g = [("S", ("S",)), ("S", ("A", "S", "b")), ("S", ("a",)), ("A", ()), ("A", ("A", "A"))]
    for m in range(5):
        w = ["a"] + ["b"] * m
        assert earley_recognize(g, "S", w)
        assert tree_ok(earley_parse(g, "S", w), g, "S", w)
    assert not earley_recognize(g, "S", ["b"])


def test_ambiguous_and_left_recursive():
    g = [("S", ("S", "S")), ("S", ("a",))]
    for m in range(1, 9):
        w = ["a"] * m
        assert tree_ok(earley_parse(g, "S", w), g, "S", w)
    left = [("S", ("S", "a")), ("S", ())]
    right = [("S", ("a", "S")), ("S", ())]
    for m in range(0, 30):
        w = ["a"] * m
        assert earley_recognize(left, "S", w) and earley_recognize(right, "S", w)


def test_long_input_no_recursion_limit():
    g = [("S", ("a", "S")), ("S", ("a",))]
    w = ["a"] * 3000
    tree = earley_parse(g, "S", w)
    assert tree_ok(tree, g, "S", w)


def test_random_against_oracles():
    rng = random.Random(20261106)
    words = [list(t) for m in range(5) for t in itertools.product("ab", repeat=m)]
    checked = 0
    for _ in range(700):
        g = random_grammar(rng)
        for w in [[]] + rng.sample(words, 5):
            expect = derives(g, "S", w)
            assert earley_recognize(g, "S", w) == expect, (g, w)
            tree = earley_parse(g, "S", w)
            assert (tree is not None) == expect
            if expect:
                assert tree_ok(tree, g, "S", w), (g, w, tree)
            if len(w) <= 3:
                assert [set(s) for s in earley_chart(g, "S", w)] == naive_items(g, "S", w)
            checked += 1
    assert checked >= 500
