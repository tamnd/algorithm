# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lalr-parsing/. The authors are listed in prov/2JWXYX.jsonl.

import itertools
import random

import pytest

from lalr_parsing import END, lalr_parse, lalr_recognize, lalr_table

DRAGON = [
    ("S", ("L", "=", "R")), ("S", ("R",)),
    ("L", ("*", "R")), ("L", ("id",)),
    ("R", ("L",)),
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


def canonical_lr1_merged(prods):
    """Independent oracle: the canonical LR(1) collection, built item by item with
    single lookahead symbols, then merged by core. prods is the augmented list
    (production 0 is S' -> S). Returns {core: {item: lookaheads}}."""
    nts = {a for a, _ in prods}

    def first_seq(seq):
        # FIRST of a sequence by brute force over a fixed point of FIRST sets
        out = set()
        for x in seq:
            if x not in nts:
                out.add(x)
                return out, False
            out |= FIRST[x]
            if x not in NULL:
                return out, False
        return out, True

    NULL, FIRST = set(), {a: set() for a in nts}
    for _ in range(len(prods) + 2):
        for a, rhs in prods:
            f, all_null = first_seq(rhs)
            FIRST[a] |= f
            if all_null:
                NULL.add(a)

    def closure(items):
        items = set(items)
        while True:
            new = set()
            for p, d, la in items:
                rhs = prods[p][1]
                if d < len(rhs) and rhs[d] in nts:
                    f, all_null = first_seq(rhs[d + 1:])
                    looks = f | ({la} if all_null else set())
                    for q, (b, _) in enumerate(prods):
                        if b == rhs[d]:
                            for t in looks:
                                new.add((q, 0, t))
            if new <= items:
                return frozenset(items)
            items |= new

    start = closure({(0, 0, END)})
    states, todo = {start}, [start]
    while todo:
        st = todo.pop()
        syms = {prods[p][1][d] for p, d, _ in st if d < len(prods[p][1])}
        for x in syms:
            nxt = closure({(p, d + 1, la) for p, d, la in st if d < len(prods[p][1]) and prods[p][1][d] == x})
            if nxt not in states:
                states.add(nxt)
                todo.append(nxt)
    merged = {}
    for st in states:
        core = frozenset((p, d) for p, d, _ in st)
        m = merged.setdefault(core, {})
        for p, d, la in st:
            m.setdefault((p, d), set()).add(la)
    return merged


def tree_ok(tree, productions, start, w):
    prods = {(a, tuple(r)) for a, r in productions}
    if tree[0] != start:
        return False
    leaves, stack = [], [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, str):
            leaves.append(t)
            continue
        label, kids = t
        if (label, tuple(k if isinstance(k, str) else k[0] for k in kids)) not in prods:
            return False
        stack.extend(reversed(kids))
    return leaves == list(w)


def closure_items(table, s):
    """All LR(0) items of state s with their LALR(1) lookaheads, recomputed from the table."""
    from lalr_parsing import _closure1, _first_sets
    prods, nts = table.productions, table.nonterminals
    by_lhs = {a: [p for p, (b, _) in enumerate(prods) if b == a] for a in nts}
    nullable, first = _first_sets(prods, nts)
    return _closure1({it: table.lookahead[(s, it)] for it in table.kernels[s]}, prods, by_lhs, nts, nullable, first)


def check_against_lr1(productions, start):
    t = lalr_table(productions, start)
    merged = canonical_lr1_merged(t.productions)
    cores = {}
    for s in range(len(t.kernels)):
        items = closure_items(t, s)
        cores[frozenset(items)] = {it: la for it, la in items.items()}
    assert set(cores) == set(merged)
    for core, items in merged.items():
        assert cores[core] == items
    return t


def reduced(prods, start):
    """True when every nonterminal derives some terminal string and is reachable."""
    nts = {a for a, _ in prods}
    gen, changed = set(), True
    while changed:
        changed = False
        for a, r in prods:
            if a not in gen and all(x in gen or x not in nts for x in r):
                gen.add(a)
                changed = True
    reach, todo = {start}, [start]
    while todo:
        a = todo.pop()
        for b, r in prods:
            if b == a:
                for x in r:
                    if x in nts and x not in reach:
                        reach.add(x)
                        todo.append(x)
    return gen == nts and reach == nts


def random_grammar(rng):
    nts = ["S", "A", "B"][: rng.randint(1, 3)]
    syms = nts + ["a", "b", "c"]
    prods = set()
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.15:
                prods.add((a, ()))
            else:
                prods.add((a, tuple(rng.choice(syms) for _ in range(rng.randint(1, 3)))))
    return sorted(prods)


def test_dragon_example():
    t = lalr_table(DRAGON, "S")
    assert len(t.kernels) == 10 and not t.conflicts()
    # state 2 holds S -> L . = R and R -> L . ; the reduction is on $ only
    s2 = t.goto[(0, "L")]
    assert t.lookahead[(s2, (5, 1))] == {END}
    assert t.action[(s2, "=")] == {("shift", t.goto[(s2, "=")])}
    assert lalr_parse(t, ["id", "=", "*", "id"]) == (
        "S", (("L", ("id",)), "=", ("R", (("L", ("*", ("R", (("L", ("id",)),)))),))))
    assert lalr_parse(t, ["id", "="]) is None
    check_against_lr1(DRAGON, "S")


def test_lr1_not_lalr1():
    g = [
        ("S", ("a", "A", "d")), ("S", ("b", "B", "d")), ("S", ("a", "B", "e")), ("S", ("b", "A", "e")),
        ("A", ("c",)), ("B", ("c",)),
    ]
    t = check_against_lr1(g, "S")
    kinds = [sorted(k for k, _ in acts) for _, _, acts in t.conflicts()]
    assert kinds == [["reduce", "reduce"], ["reduce", "reduce"]]


def test_ambiguous_has_conflict():
    g = [("E", ("E", "+", "E")), ("E", ("a",))]
    assert lalr_table(g, "E").conflicts()
    with pytest.raises(ValueError):
        lalr_recognize(g, "E", ["a"])


def test_left_and_right_recursion_and_empty():
    left = [("S", ("S", "a")), ("S", ())]
    right = [("S", ("a", "S")), ("S", ())]
    for g in (left, right):
        t = lalr_table(g, "S")
        assert not t.conflicts()
        for m in range(0, 50):
            tree = lalr_parse(t, ["a"] * m)
            assert tree is not None and tree_ok(tree, g, "S", ["a"] * m)
        assert lalr_parse(t, ["b"]) is None


def test_long_input():
    g = [("S", ("a", "S")), ("S", ("a",))]
    w = ["a"] * 5000
    assert tree_ok(lalr_parse(lalr_table(g, "S"), w), g, "S", w)


def test_random_against_oracles():
    rng = random.Random(20261106)
    words = [list(t) for m in range(5) for t in itertools.product("abc", repeat=m)]
    lalr_count = checked = 0
    for _ in range(2000):
        g = random_grammar(rng)
        if not reduced(g, "S"):
            continue
        t = check_against_lr1(g, "S")
        if t.conflicts():
            continue
        lalr_count += 1
        for w in [[]] + rng.sample(words, 8):
            tree = lalr_parse(t, w)
            assert (tree is not None) == derives(g, "S", w), (g, w)
            if tree is not None:
                assert tree_ok(tree, g, "S", w)
            checked += 1
    assert lalr_count >= 100 and checked >= 500
