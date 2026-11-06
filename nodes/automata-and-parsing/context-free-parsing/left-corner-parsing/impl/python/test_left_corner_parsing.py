# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-corner-parsing/. The authors are listed in prov/P8PFGP.jsonl.

import itertools
import random

from left_corner_parsing import left_corner_chart, left_corner_closure, left_corner_recognize

EXAMPLE = [("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("a",))]


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


def random_grammar(rng):
    nts = ["S", "A", "B"][: rng.randint(1, 3)]
    syms = nts + ["a", "b"]
    prods = []
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(syms) for _ in range(k))))
    if rng.random() < 0.3:                      # left recursion
        prods.append(("S", ("S", rng.choice(syms))))
    if rng.random() < 0.2:                      # hidden left recursion and cycles
        prods.append(("S", (rng.choice(nts), "S")))
    return prods


def test_example_chart():
    w = ["a", "+", "a"]
    chart, done = left_corner_chart(EXAMPLE, "E", w)
    show = [sorted((c, i, p, d) for c, i, p, d in col) for col in chart]
    assert show[0] == []
    assert show[1] == [("E", 0, 0, 1), ("E", 0, 1, 1), ("E", 0, 2, 1)]
    assert show[2] == [("E", 0, 0, 2)]
    assert show[3] == [("E", 0, 0, 1), ("E", 0, 0, 3), ("T", 2, 2, 1)]
    assert done == {("E", 0): {1, 3}, ("T", 2): {3}}
    assert left_corner_closure(EXAMPLE, "E") == {"E": {"E", "T"}, "T": {"T"}}
    assert left_corner_recognize(EXAMPLE, "E", w)
    assert not left_corner_recognize(EXAMPLE, "E", ["a", "+"])


def test_empty_input_and_epsilon():
    g = [("S", ()), ("S", ("A", "S")), ("A", ())]
    assert left_corner_recognize(g, "S", [])
    assert not left_corner_recognize(g, "S", ["a"])
    g2 = [("S", ("A", "A", "a")), ("A", ())]
    assert left_corner_recognize(g2, "S", ["a"])
    assert not left_corner_recognize(g2, "S", [])


def test_cycles_units_and_no_productions():
    g = [("S", ("S",)), ("S", ("A",)), ("A", ("S",)), ("A", ("a",)), ("S", ("S", "S"))]
    for k in range(5):
        assert left_corner_recognize(g, "S", ["a"] * k) == (k >= 1)
    assert not left_corner_recognize([("A", ("a",))], "S", ["a"])
    assert not left_corner_recognize([], "S", [])


def test_random_against_oracle():
    rng = random.Random(20261106)
    inputs = 0
    for _ in range(300):
        g = random_grammar(rng)
        words = [list(t) for m in range(4) for t in itertools.product("ab", repeat=m)]
        words += [[rng.choice("ab") for _ in range(rng.randint(4, 7))] for _ in range(3)]
        for w in words:
            assert left_corner_recognize(g, "S", w) == derives(g, "S", w), (g, w)
            inputs += 1
    assert inputs >= 500


def test_long_inputs_no_recursion_limit():
    right = [("S", ("a", "S")), ("S", ("b",))]
    left = [("S", ("S", "a")), ("S", ("b",))]
    n = 3000
    assert left_corner_recognize(right, "S", ["a"] * n + ["b"])
    assert not left_corner_recognize(right, "S", ["a"] * n)
    assert left_corner_recognize(left, "S", ["b"] + ["a"] * n)
