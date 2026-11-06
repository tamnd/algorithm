# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glr-parsing/. The authors are listed in prov/Z0RM8G.jsonl.

import itertools
import random

from glr_parsing import glr_parse, glr_recognize, lr0_automaton

EXAMPLE = [("S", ("S", "S")), ("S", ("a",))]


def derives(productions, start, w):
    """Independent oracle: least fixpoint of 'A derives w[i:j]' over all spans."""
    nts = {a for a, _ in productions} | {start}
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


def check_tree(productions, start, w, tree):
    """Check without recursion that tree is a parse tree of w from start."""
    prods = {(a, tuple(r)) for a, r in productions}
    assert tree[0] == start
    leaves = []
    stack = [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, str):
            leaves.append(t)
            continue
        a, kids = t
        labels = tuple(k if isinstance(k, str) else k[0] for k in kids)
        assert (a, labels) in prods, (a, labels)
        stack.extend(reversed(kids))
    assert leaves == list(w)


def random_grammar(rng):
    nts = ["S", "A", "B"][: rng.randint(1, 3)]
    syms = nts + ["a", "b"]
    prods = []
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(syms) for _ in range(k))))
    if rng.random() < 0.3:                      # force left recursion
        prods.append(("S", ("S", rng.choice(syms))))
    if rng.random() < 0.2:                      # hidden left recursion and cycles
        prods.append(("S", (rng.choice(nts), "S")))
    return prods


def test_example():
    for k in range(1, 7):
        w = ["a"] * k
        tree = glr_parse(EXAMPLE, "S", w)
        check_tree(EXAMPLE, "S", w, tree)
    assert glr_parse(EXAMPLE, "S", []) is None
    assert glr_parse(EXAMPLE, "S", ["b"]) is None


def test_example_automaton():
    aut = lr0_automaton(EXAMPLE, "S")
    assert len(aut.states) == 4
    conflict = [q for q, s in enumerate(aut.states) if aut.reductions[q] and "a" in aut.goto[q]]
    assert len(conflict) == 1


def test_empty_input_and_epsilon():
    g = [("S", ()), ("S", ("A", "S")), ("A", ())]
    assert glr_recognize(g, "S", [])
    assert not glr_recognize(g, "S", ["a"])
    g2 = [("S", ("A", "S", "b")), ("S", ("a",)), ("A", ())]
    for k in range(5):
        w = ["a"] + ["b"] * k
        assert glr_recognize(g2, "S", w)
        check_tree(g2, "S", w, glr_parse(g2, "S", w))
    assert not glr_recognize(g2, "S", ["b"])


def test_cycles_and_units():
    g = [("S", ("S",)), ("S", ("A",)), ("A", ("S",)), ("A", ("a",)), ("S", ("S", "S"))]
    for k in range(5):
        assert glr_recognize(g, "S", ["a"] * k) == (k >= 1)


def test_start_without_productions():
    assert not glr_recognize([("A", ("a",))], "S", ["a"])
    assert not glr_recognize([], "S", [])


def test_random_against_oracle():
    rng = random.Random(20261106)
    inputs = 0
    for _ in range(250):
        g = random_grammar(rng)
        words = [list(t) for m in range(4) for t in itertools.product("ab", repeat=m)]
        words += [[rng.choice("ab") for _ in range(rng.randint(4, 7))] for _ in range(3)]
        for w in words:
            expect = derives(g, "S", w)
            tree = glr_parse(g, "S", w)
            assert (tree is not None) == expect, (g, w)
            if tree is not None:
                check_tree(g, "S", w, tree)
            inputs += 1
    assert inputs >= 500


def test_long_input_no_recursion_limit():
    g = [("S", ("S", "a")), ("S", ("a", "S")), ("S", ())]
    w = ["a"] * 300
    tree = glr_parse(g, "S", w)
    check_tree(g, "S", w, tree)
