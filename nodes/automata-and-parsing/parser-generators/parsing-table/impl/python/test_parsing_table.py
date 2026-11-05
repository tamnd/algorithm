# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsing-table/. The authors are listed in prov/JQ131J.jsonl.

import itertools
import random

import pytest

from parsing_table import (
    END,
    ParsingTable,
    StepLimit,
    ll1_table,
    ll_parse,
    lr_parse,
    slr_table,
)

LR_EXAMPLE = [("E", ("E", "+", "n")), ("E", ("n",))]
LL_EXAMPLE = [("E", ("n", "E'")), ("E'", ("+", "n", "E'")), ("E'", ())]
AMBIGUOUS = [("E", ("E", "+", "E")), ("E", ("n",))]


def cells(table):
    return {(r, c): table.lookup(r, c) for r in range(table.rows) for c in table.columns if table.lookup(r, c)}


# ---------------------------------------------------------------- oracles


def lang_upto(grammar, max_len):
    """For each nonterminal, every terminal string of length <= max_len it derives."""
    nts = {a for a, _ in grammar}
    lang = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in grammar:
            cur = {()}
            for x in rhs:
                src = lang[x] if x in nts else {(x,)}
                cur = {u + v for u in cur for v in src if len(u) + len(v) <= max_len}
                if not cur:
                    break
            if not cur <= lang[a]:
                lang[a] |= cur
                changed = True
    return lang


def tree_counts(grammar, max_len):
    """Number of parse trees, capped at 2, of each (nonterminal, string) with |string| <= max_len."""
    nts = {a for a, _ in grammar}
    strings = lang_upto(grammar, max_len)
    count = {(a, w): 0 for a in nts for w in strings[a]}

    def seq_count(rhs, w):
        # number of ways rhs derives w, using the current counts; capped at 2
        ways = {0: 1}
        for x in rhs:
            nxt = {}
            for start, c in ways.items():
                for end in range(start, len(w) + 1):
                    piece = w[start:end]
                    if x in nts:
                        k = count.get((x, piece), 0)
                    else:
                        k = 1 if piece == (x,) else 0
                    if k:
                        nxt[end] = min(2, nxt.get(end, 0) + c * k)
            ways = nxt
        return ways.get(len(w), 0)

    changed = True
    while changed:
        changed = False
        for a in nts:
            for w in strings[a]:
                total = min(2, sum(seq_count(rhs, w) for b, rhs in grammar if b == a))
                if total > count[(a, w)]:
                    count[(a, w)] = total
                    changed = True
    return count


def random_grammar(rng):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    terms = ["a", "b"]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.2:
                rhs = ()
            else:
                rhs = tuple(rng.choice(names + terms) for _ in range(rng.randint(1, 3)))
            if (a, rhs) not in prods:
                prods.append((a, rhs))
    return prods, terms


def all_strings(terms, max_len):
    for n in range(max_len + 1):
        yield from itertools.product(terms, repeat=n)


# ---------------------------------------------------------------- worked example


def test_worked_example_lr_table():
    table, prods = slr_table(LR_EXAMPLE)
    assert prods[1:] == LR_EXAMPLE
    assert table.columns == ["+", "n", END, "E"]
    assert cells(table) == {
        (0, "n"): (("shift", 2),),
        (0, "E"): (("goto", 1),),
        (1, "+"): (("shift", 3),),
        (1, END): (("accept",),),
        (2, "+"): (("reduce", 2),),
        (2, END): (("reduce", 2),),
        (3, "n"): (("shift", 4),),
        (4, "+"): (("reduce", 1),),
        (4, END): (("reduce", 1),),
    }
    assert table.entries() == 9
    assert table.conflicts() == []
    assert lr_parse(table, prods, ["n", "+", "n"])
    assert not lr_parse(table, prods, ["n", "+"])
    assert not lr_parse(table, prods, [])


def test_worked_example_ll_table():
    table = ll1_table(LL_EXAMPLE)
    assert table.columns == ["n", "+", END]
    assert cells(table) == {
        (0, "n"): (("predict", 0),),
        (1, "+"): (("predict", 1),),
        (1, END): (("predict", 2),),
    }
    assert ll_parse(table, LL_EXAMPLE, ["n", "+", "n", "+", "n"])
    assert not ll_parse(table, LL_EXAMPLE, ["n", "n"])


def test_conflict_and_resolution():
    table, prods = slr_table(AMBIGUOUS)
    assert table.conflicts() == [(4, "+", (("shift", 3), ("reduce", 1)))]
    with pytest.raises(ValueError):
        lr_parse(table, prods, ["n", "+", "n", "+", "n"])
    table.resolve(lambda r, c, acts: next(a for a in acts if a[0] == "reduce"))
    assert table.conflicts() == []
    assert table.lookup(4, "+") == (("reduce", 1),)
    assert lr_parse(table, prods, ["n", "+", "n", "+", "n"])


# ---------------------------------------------------------------- edge cases


def test_empty_input_and_epsilon():
    g = [("S", ("a", "S")), ("S", ())]
    t, prods = slr_table(g)
    assert t.conflicts() == []
    assert lr_parse(t, prods, [])
    assert lr_parse(t, prods, ["a", "a"])
    lt = ll1_table(g)
    assert lt.conflicts() == []
    assert ll_parse(lt, g, [])
    assert not ll_parse(lt, g, ["b"])


def test_only_epsilon():
    g = [("S", ())]
    t, prods = slr_table(g)
    assert lr_parse(t, prods, [])
    assert not lr_parse(t, prods, ["x"])
    assert ll_parse(ll1_table(g), g, [])


def test_basic_operations():
    t = ParsingTable(["a", "b"], rows=2)
    assert t.lookup(0, "a") == ()
    assert t.lookup(5, "a") == ()
    assert t.lookup(0, "zzz") == ()
    t.add(0, "a", ("shift", 1))
    t.add(0, "a", ("shift", 1))
    assert t.conflicts() == []
    t.add(0, "a", ("reduce", 2))
    assert t.conflicts() == [(0, "a", (("shift", 1), ("reduce", 2)))]
    t.resolve(lambda r, c, acts: None)
    assert t.lookup(0, "a") == ()
    assert t.add_row() == 2
    with pytest.raises(ValueError):
        ParsingTable(["a", "a"])


def test_left_recursion_is_an_ll_conflict():
    g = [("E", ("E", "+", "n")), ("E", ("n",))]
    t = ll1_table(g)
    assert [(r, c) for r, c, _ in t.conflicts()] == [(0, "n")]


# ---------------------------------------------------------------- random


def test_random_operations_match_a_dictionary():
    rng = random.Random(1)
    for _ in range(600):
        cols = ["a", "b", "c", END]
        t = ParsingTable(cols, rows=3)
        oracle = {}
        for _ in range(rng.randint(0, 12)):
            r = rng.randrange(3)
            c = rng.choice(cols)
            act = (rng.choice(["shift", "reduce"]), rng.randrange(3))
            t.add(r, c, act)
            cell = oracle.setdefault((r, c), [])
            if act not in cell:
                cell.append(act)
        for r in range(3):
            for c in cols:
                assert t.lookup(r, c) == tuple(oracle.get((r, c), []))
        expect = sorted((r, cols.index(c)) for (r, c), v in oracle.items() if len(v) > 1)
        assert [(r, cols.index(c)) for r, c, _ in t.conflicts()] == expect
        assert t.entries() == sum(len(v) for v in oracle.values())
        t.resolve(lambda r, c, acts: acts[-1])
        for (r, c), v in oracle.items():
            assert t.lookup(r, c) == (v[-1],)


def test_random_grammars_against_brute_force():
    rng = random.Random(7)
    max_len = 4
    checked = 0
    for _ in range(700):
        g, terms = random_grammar(rng)
        lang = lang_upto(g, max_len)[g[0][0]]
        counts = tree_counts(g, max_len)
        ambiguous = any(v > 1 for (a, _), v in counts.items() if a == g[0][0])
        lr_t, prods = slr_table(g)
        ll_t = ll1_table(g)
        if ambiguous:
            # an ambiguous grammar is neither SLR(1) nor LL(1): both builders must report a conflict
            assert lr_t.conflicts() and ll_t.conflicts()
        if not lr_t.conflicts():
            for w in all_strings(terms, max_len):
                assert lr_parse(lr_t, prods, w, max_steps=1000) == (w in lang), (g, w)
                checked += 1
        else:
            lr_t.resolve(lambda r, c, acts: rng.choice(acts))
            for w in all_strings(terms, max_len):
                try:
                    if lr_parse(lr_t, prods, w, max_steps=200):
                        assert w in lang, (g, w)
                except StepLimit:
                    pass
        if not ll_t.conflicts():
            for w in all_strings(terms, max_len):
                assert ll_parse(ll_t, g, w, max_steps=1000) == (w in lang), (g, w)
                checked += 1
        else:
            ll_t.resolve(lambda r, c, acts: rng.choice(acts))
            for w in all_strings(terms, max_len):
                try:
                    if ll_parse(ll_t, g, w, max_steps=200):
                        assert w in lang, (g, w)
                except StepLimit:
                    pass
    assert checked >= 500
