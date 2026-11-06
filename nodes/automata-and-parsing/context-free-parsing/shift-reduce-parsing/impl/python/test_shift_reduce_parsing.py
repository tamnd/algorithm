# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shift-reduce-parsing/. The authors are listed in prov/PZXCZZ.jsonl.

import itertools
import random

import pytest

from shift_reduce_parsing import ParseError, parse, shift_reduce

EXPR = [
    ("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("T", "*", "F")), ("T", ("F",)),
    ("F", ("(", "E", ")")), ("F", ("id",)),
]


def derives(prods, start, w):
    """Independent oracle: does start =>* w? Least fixpoint over spans."""
    nts = {a for a, _ in prods}
    n = len(w)
    known = set()

    def ok(rhs, i, j):
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
        for a, rhs in prods:
            for i in range(n + 1):
                for j in range(i, n + 1):
                    if (a, i, j) not in known and ok(rhs, i, j):
                        known.add((a, i, j))
                        changed = True
    return (start, 0, n) in known


def tree_ok(tree, prods, w):
    pset = {(a, tuple(r)) for a, r in prods}
    leaves, stack = [], [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, str):
            leaves.append(t)
            continue
        a, kids = t
        if (a, tuple(k if isinstance(k, str) else k[0] for k in kids)) not in pset:
            return False
        stack.extend(reversed(kids))
    return leaves == list(w)


def is_reverse_rightmost(prods, start, reductions, w):
    """The reductions, read backwards, must be the steps of a rightmost derivation of w."""
    nts = {a for a, _ in prods}
    form = [start]
    for k in reversed(reductions):
        a, rhs = prods[k]
        idx = [i for i, x in enumerate(form) if x in nts]
        if not idx or form[idx[-1]] != a:
            return False
        i = idx[-1]
        form[i:i + 1] = list(rhs)
    return form == list(w)


def random_grammar(rng):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    terms = ["a", "b"]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(names + terms + terms) for _ in range(k))))
    out = []
    for p in prods:
        if p not in out:
            out.append(p)
    return out


def test_example_trace() -> None:
    trace = []
    toks = "id + id * id".split()
    tree, red = parse(EXPR, "E", toks, trace)
    moves = [a[0] if a[0] != "reduce" else EXPR[a[1]] for _, _, a in trace]
    assert moves == [
        "shift", ("F", ("id",)), ("T", ("F",)), ("E", ("T",)), "shift", "shift",
        ("F", ("id",)), ("T", ("F",)), "shift", "shift", ("F", ("id",)),
        ("T", ("T", "*", "F")), ("E", ("E", "+", "T")), "accept",
    ]
    assert len(red) == 8 and is_reverse_rightmost(EXPR, "E", red, toks)
    assert tree_ok(tree, EXPR, toks)
    with pytest.raises(ParseError):
        parse(EXPR, "E", "id + * id".split())
    with pytest.raises(ParseError):
        parse(EXPR, "E", [])


def test_greedy_decider_can_fail() -> None:
    """The driver is only as good as its decisions: reducing whenever a right
    side is on top fails on id + id * id, which is in the language."""

    def greedy(symbols, pos):
        for k, (a, r) in enumerate(EXPR):
            if r and tuple(symbols[len(symbols) - len(r):]) == r:
                return ("reduce", k)
        if symbols == ["E"] and pos == 5:
            return ("accept",)
        return ("shift",) if pos < 5 else ("error",)

    with pytest.raises(ParseError):
        shift_reduce("id + id * id".split(), EXPR, greedy)


def test_ambiguous_epsilon_and_cycles() -> None:
    g = [("S", ("S", "S")), ("S", ("a",)), ("S", ())]  # ambiguous, epsilon, left recursive
    for n in range(5):
        w = ["a"] * n
        tree, red = parse(g, "S", w)
        assert tree_ok(tree, g, w) and is_reverse_rightmost(g, "S", red, w)
    cyc = [("S", ("A",)), ("A", ("S",)), ("A", ("b",)), ("S", ("S", "a"))]  # unit cycle S => A => S
    tree, red = parse(cyc, "S", ["b", "a", "a"])
    assert tree_ok(tree, cyc, ["b", "a", "a"])
    with pytest.raises(ParseError):
        parse(cyc, "S", ["a"])
    eps = [("S", ())]
    assert parse(eps, "S", [])[0] == ("S", ())


def test_random_grammars_against_oracle() -> None:
    rng = random.Random(1965)
    checked = accepted = 0
    kinds = {"eps": 0, "unit": 0, "left": 0}
    for _ in range(400):
        g = random_grammar(rng)
        start = g[0][0]
        kinds["eps"] += any(not r for _, r in g)
        kinds["unit"] += any(len(r) == 1 and r[0] in {a for a, _ in g} for _, r in g)
        kinds["left"] += any(r and r[0] == a for a, r in g)
        for n in range(0, 5):
            for w in itertools.product("ab", repeat=n):
                w = list(w)
                want = derives(g, start, w)
                try:
                    tree, red = parse(g, start, w)
                except ParseError:
                    assert not want, (g, w)
                else:
                    assert want, (g, w)
                    assert tree_ok(tree, g, w), (g, w)
                    assert is_reverse_rightmost(g, start, red, w), (g, w)
                    accepted += 1
                checked += 1
    assert checked >= 500 and accepted >= 1000
    assert min(kinds.values()) >= 50, kinds
