# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-ascent-parsing/. The authors are listed in prov/K7ZEFB.jsonl.

import itertools
import random

import pytest

from recursive_ascent_parsing import (
    END,
    GrammarConflict,
    ParseError,
    RecursiveAscentParser,
    slr_table,
)

EXPR = [
    ("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("T", "*", "F")), ("T", ("F",)),
    ("F", ("(", "E", ")")), ("F", ("id",)),
]
SMALL = [("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("n",))]


def grammar(text):
    prods = []
    for rule in text.split(";"):
        a, rhs = rule.split("->")
        for alt in rhs.split("|"):
            prods.append((a.strip(), tuple(x for x in alt.split() if x != "eps")))
    return prods


def spans(prods, w):
    """Independent oracle: the set of (X, i, j) with X =>* w[i:j], by a least fixpoint."""
    nts = {a for a, _ in prods}
    n, known = len(w), set()

    def ends(rhs, i, j):
        cur = {i}
        for x in rhs:
            nxt = set()
            for p in cur:
                if x in nts:
                    nxt |= {q for q in range(p, j + 1) if (x, p, q) in known}
                elif p < j and w[p] == x:
                    nxt.add(p + 1)
            cur = nxt
        return cur

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                for j in range(i, n + 1):
                    if (a, i, j) not in known and j in ends(rhs, i, j):
                        known.add((a, i, j))
                        changed = True
    return known


def tree_ok(tree, prods, w):
    pset = set(prods)
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
    nts = {a for a, _ in prods}
    form = [start]
    for k in reversed(reductions):
        a, rhs = prods[k]
        idx = [i for i, x in enumerate(form) if x in nts]
        if not idx or form[idx[-1]] != a:
            return False
        form[idx[-1]:idx[-1] + 1] = list(rhs)
    return form == list(w)


def table_driven(prods, start, w):
    """Reference: the ordinary table-driven LR driver on the same table. Returns
    (accepted, reductions, error position, number of shifts and gotos)."""
    action, goto, _ = slr_table(prods, start)
    w = list(w) + [END]
    stack, i, red, pushes = [0], 0, [], 0
    while True:
        act = action.get((stack[-1], w[i]))
        if act is None:
            return False, red, i, pushes
        if act[0] == "shift":
            stack.append(act[1])
            i += 1
            pushes += 1
        elif act[0] == "reduce":
            a, rhs = prods[act[1]]
            del stack[len(stack) - len(rhs):]
            stack.append(goto[stack[-1], a])
            red.append(act[1])
            pushes += 1
        else:
            return True, red, None, pushes


def random_grammar(rng):
    names = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(names + ["a", "b", "a", "b"]) for _ in range(k))))
    return list(dict.fromkeys(prods))


def test_random_grammars_against_oracles():
    rng = random.Random(1988)
    checked = accepted = rejected = grammars = conflicted = 0
    kinds = {"eps": 0, "unit": 0, "left": 0, "eps_input": 0}
    for _ in range(700):
        g = random_grammar(rng)
        start = g[0][0]
        try:
            parser = RecursiveAscentParser(g, start)
        except GrammarConflict:
            conflicted += 1
            continue
        grammars += 1
        nts = {a for a, _ in g}
        kinds["eps"] += any(not r for _, r in g)
        kinds["unit"] += any(len(r) == 1 and r[0] in nts for _, r in g)
        kinds["left"] += any(r and r[0] == a for a, r in g)
        for n in range(6):
            for w in itertools.product("ab", repeat=n):
                w = list(w)
                want = (start, 0, n) in spans(g, w)
                ok, ref_red, ref_pos, pushes = table_driven(g, start, w)
                trace = []
                try:
                    tree, red = parser.parse(w, trace=trace)
                except ParseError as e:
                    assert not want and not ok, (g, w)
                    assert e.position == ref_pos, (g, w)
                    rejected += 1
                else:
                    assert want and ok, (g, w)
                    assert tree[0] == start
                    assert tree_ok(tree, g, w) and is_reverse_rightmost(g, start, red, w), (g, w)
                    assert red == ref_red, (g, w)
                    # one call for every shift and goto of the table-driven parser, plus state 0
                    assert len(trace) == pushes + 1, (g, w)
                    accepted += 1
                    kinds["eps_input"] += n == 0
                checked += 1
    assert grammars >= 200 and conflicted >= 100
    assert checked >= 10000 and accepted >= 800 and rejected >= 5000
    assert min(kinds.values()) >= 30, kinds


def test_expression_grammar():
    p = RecursiveAscentParser(EXPR, "E")
    w = ["id", "+", "id", "*", "(", "id", "+", "id", ")"]
    tree, red = p.parse(w)
    assert tree_ok(tree, EXPR, w) and is_reverse_rightmost(EXPR, "E", red, w)
    assert p.nstates == 12
    with pytest.raises(ParseError) as e:
        p.parse(["id", "+", "*", "id"])
    assert e.value.position == 2
    with pytest.raises(ParseError) as e:
        p.parse([])
    assert e.value.position == 0


def test_page_example_trace():
    p = RecursiveAscentParser(SMALL, "E")
    trace = []
    tree, red = p.parse(["n", "+", "n"], trace=trace)
    assert red == [2, 1, 2, 0]
    assert tree == ("E", (("E", (("T", ("n",)),)), "+", ("T", ("n",))))
    assert p.nstates == 6
    assert trace == [0, 3, 2, 1, 4, 3, 5, 1]


def test_ambiguous_grammars_conflict():
    for text, start in [
        ("E -> E + E | id", "E"),
        ("S -> S S | a | eps", "S"),
        ("S -> i S | i S e S | x", "S"),
        ("S -> A | B; A -> a; B -> a", "S"),
    ]:
        with pytest.raises(GrammarConflict):
            RecursiveAscentParser(grammar(text), start)


def test_empty_input_and_epsilon():
    g = grammar("S -> a S b | eps")
    p = RecursiveAscentParser(g, "S")
    assert p.parse([]) == (("S", ()), [1])
    tree, red = p.parse(list("aabb"))
    assert tree_ok(tree, g, "aabb")
    with pytest.raises(ParseError) as e:
        p.parse(list("aab"))
    assert e.value.position == 3


def test_deep_inputs_do_not_recurse():
    right = RecursiveAscentParser(grammar("S -> x S | x"), "S")
    tree, red = right.parse(["x"] * 100000)
    assert len(red) == 100000
    left = RecursiveAscentParser(EXPR, "E")
    nested = ["("] * 20000 + ["id"] + [")"] * 20000
    tree, red = left.parse(nested)
    assert tree_ok(tree, EXPR, nested)
    w = ["id"] + ["+", "id"] * 50000
    tree, red = left.parse(w)
    assert len(red) == 2 * 50001 + 1 + 50000
