# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slr-parsing/. The authors are listed in prov/7X628Y.jsonl.

import itertools
import random

import pytest

from slr_parsing import GrammarConflict, ParseError, SLRTable, parse, slr_table

EXPR = [
    ("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("T", "*", "F")), ("T", ("F",)),
    ("F", ("(", "E", ")")), ("F", ("id",)),
]


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


def is_prefix(prods, start, x):
    """Independent oracle: is x a prefix of some sentence of the grammar?
    pre[(X, p)] means that X derives a string that starts with x[p:]."""
    nts = {a for a, _ in prods}
    n = len(x)
    known = spans(prods, x)
    # productive nonterminals: derive some terminal string (fixpoint)
    productive = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in productive and all(s not in nts or s in productive for s in rhs):
                productive.add(a)
                changed = True
    pre = set()

    def pre_sym(s, p):
        if s in nts:
            return (s, p) in pre
        return p == n or (p == n - 1 and x[p] == s)

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if not all(s not in nts or s in productive for s in rhs):
                continue
            for p in range(n + 1):
                if (a, p) in pre:
                    continue
                cur, ok = {p}, False
                for s in rhs:
                    if any(pre_sym(s, q) for q in cur):
                        ok = True
                        break
                    nxt = set()
                    for q in cur:
                        if s in nts:
                            nxt |= {r for r in range(q, n + 1) if (s, q, r) in known}
                        elif q < n and x[q] == s:
                            nxt.add(q + 1)
                    cur = nxt
                if ok or n in cur:
                    pre.add((a, p))
                    changed = True
    return (start, 0) in pre


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


def random_grammar(rng):
    names = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(names + ["a", "b", "a", "b"]) for _ in range(k))))
    return list(dict.fromkeys(prods))


def test_expression_table_and_trace() -> None:
    t = slr_table(EXPR, "E")
    assert len(t.states) == 12
    assert t.follow["E"] == {"+", ")", "$"} and t.follow["T"] == t.follow["F"] == {"+", "*", ")", "$"}
    trace = []
    tree, red = parse(t, "id * id + id".split(), trace=trace)
    assert [s for s, _, _, _ in trace][:7] == [[0], [0, 5], [0, 3], [0, 2], [0, 2, 7], [0, 2, 7, 5], [0, 2, 7, 10]]
    assert [a[0] for _, _, _, a in trace] == ["shift", "reduce", "reduce", "shift", "shift", "reduce", "reduce",
                                             "reduce", "shift", "shift", "reduce", "reduce", "reduce", "accept"]
    assert red == [5, 3, 5, 2, 1, 5, 3, 0]
    assert tree_ok(tree, EXPR, "id * id + id".split())
    for bad, pos in [("id + * id", 2), ("( id", 2), ("id id", 1), ("", 0), (")", 0)]:
        with pytest.raises(ParseError) as e:
            parse(t, bad.split())
        assert e.value.position == pos


def test_classification_of_page_examples() -> None:
    ok = ["S -> a S b | eps", "S -> S a | eps", "S -> A a | B b ; A -> c ; B -> c", "S -> x S | x"]
    for g in ok:
        assert SLRTable(grammar(g), "S").conflicts == [], g
    lr = SLRTable(grammar("S -> L = R | R ; L -> * R | id ; R -> L"), "S")
    assert [(t, sorted(a[0] for a in acts)) for _, t, acts in lr.conflicts] == [("=", ["reduce", "shift"])]
    eps = SLRTable(grammar("S -> A a A b | B b B a ; A -> eps ; B -> eps"), "S")
    assert [(q, t) for q, t, _ in eps.conflicts] == [(0, "a"), (0, "b")]
    rr = SLRTable(grammar("S -> A a | B b | d A b | e B a ; A -> c ; B -> c"), "S")
    assert sorted(t for _, t, _ in rr.conflicts) == ["a", "b"]
    assert all(all(a[0] == "reduce" for a in acts) for _, _, acts in rr.conflicts)
    dangling = SLRTable(grammar("S -> i E t S | i E t S e S | a ; E -> b"), "S")
    assert [t for _, t, _ in dangling.conflicts] == ["e"] and len(dangling.states) == 10
    with pytest.raises(GrammarConflict):
        slr_table(grammar("E -> E + E | id"), "E")
    # empty language: S derives no terminal string, every input is rejected at once
    t = slr_table(grammar("S -> a S"), "S")
    for w in ([], ["a"], ["a", "a"]):
        with pytest.raises(ParseError) as e:
            parse(t, w)
        assert e.value.position == 0


def test_random_grammars_against_oracles() -> None:
    rng = random.Random(1971)
    checked = accepted = rejected = grammars = conflicted = 0
    kinds = {"eps": 0, "unit": 0, "left": 0}
    for _ in range(700):
        g = random_grammar(rng)
        start = g[0][0]
        table = SLRTable(g, start)
        nts = {a for a, _ in g}
        if table.conflicts:
            conflicted += 1
            # with conflicts the table may fail, but an accepted tree is still right
            for n in range(4):
                for w in itertools.product("ab", repeat=n):
                    try:
                        tree, red = parse(table, w, choose=lambda acts: acts[-1], limit=200)
                    except (ParseError, RuntimeError):
                        continue
                    assert tree_ok(tree, g, w) and is_reverse_rightmost(g, start, red, w)
            continue
        grammars += 1
        kinds["eps"] += any(not r for _, r in g)
        kinds["unit"] += any(len(r) == 1 and r[0] in nts for _, r in g)
        kinds["left"] += any(r and r[0] == a for a, r in g)
        for n in range(6):
            for w in itertools.product("ab", repeat=n):
                w = list(w)
                want = (start, 0, n) in spans(g, w)
                trace = []
                try:
                    tree, red = parse(table, w, trace=trace)
                except ParseError as e:
                    assert not want, (g, w)
                    # the error is at the first token that no sentence allows there
                    first_bad = next((i for i in range(n) if not is_prefix(g, start, w[:i + 1])), n)
                    assert e.position == first_bad, (g, w)
                    rejected += 1
                else:
                    assert want, (g, w)
                    assert tree_ok(tree, g, w) and is_reverse_rightmost(g, start, red, w), (g, w)
                    accepted += 1
                assert len(trace) <= 40 * (n + 1), (g, w)
                checked += 1
    assert grammars >= 200 and conflicted >= 100
    assert checked >= 10000 and accepted >= 800 and rejected >= 10000
    assert min(kinds.values()) >= 30, kinds


def test_long_inputs_do_not_recurse() -> None:
    right = slr_table(grammar("S -> x S | x"), "S")
    tree, red = parse(right, ["x"] * 100000)
    assert len(red) == 100000
    left = slr_table(EXPR, "E")
    w = ["id"] + ["+", "id"] * 50000
    tree, red = parse(left, w)
    assert tree_ok(tree, EXPR, w)
    nested = ["("] * 20000 + ["id"] + [")"] * 20000
    tree, red = parse(left, nested)
    assert tree_ok(tree, EXPR, nested)
