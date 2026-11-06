# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-descent-parsing/. The authors are listed in prov/FBHW41.jsonl.

import itertools
import random

import pytest

from recursive_descent_parsing import GrammarError, ParseError, RecursiveDescentParser

EXPR = [
    ("E", ("T", "E'")), ("E'", ("+", "T", "E'")), ("E'", ()),
    ("T", ("F", "T'")), ("T'", ("*", "F", "T'")), ("T'", ()),
    ("F", ("(", "E", ")")), ("F", ("a",)),
]


def spans(prods, w):
    """Independent oracle: the set of (A, i, j) with A =>* w[i:j], by a least fixpoint."""
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
    return known


def derives(prods, start, w):
    return (start, 0, len(w)) in spans(prods, w)


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


def oracle_ll1(prods, start):
    """Independent LL(1) and left-recursion test written from the definitions."""
    nts = {a for a, _ in prods}
    nullable = {a for a in nts if derives(prods, a, ())}
    # left corners: A -> beta X ... with beta nullable
    corner = {a: set() for a in nts}
    for a, r in prods:
        for x in r:
            corner[a].add(x)
            if x not in nullable:
                break
    reach = {}
    for a in nts:
        seen, todo = set(), [a]
        while todo:
            x = todo.pop()
            for y in corner.get(x, ()):
                if y not in seen:
                    seen.add(y)
                    todo.append(y)
        reach[a] = seen
    if any(a in reach[a] for a in nts):
        return False
    first = {a: {t for t in reach[a] if t not in nts} for a in nts}

    def fst(seq):
        out = set()
        for x in seq:
            out |= first[x] if x in nts else {x}
            if x not in nullable:
                return out, False
        return out, True

    follow = {a: set() for a in nts}
    follow[start].add("$")
    for _ in range(len(nts) + 2):
        for a, r in prods:
            for i, x in enumerate(r):
                if x in nts:
                    f, nul = fst(r[i + 1:])
                    follow[x] |= f
                    if nul:
                        follow[x] |= follow[a]
    for a in nts:
        mine = [r for b, r in prods if b == a]
        sets = []
        for r in mine:
            f, nul = fst(r)
            sets.append(f | follow[a] if nul else f)
        for s1, s2 in itertools.combinations(sets, 2):
            if s1 & s2:
                return False
    return True


def random_grammar(rng):
    names = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    terms = ["a", "b", "c"]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = rng.randint(0, 3)
            prods.append((a, tuple(rng.choice(names + terms + terms) for _ in range(k))))
    out = []
    for p in prods:
        if p not in out:
            out.append(p)
    return out


def test_example() -> None:
    p = RecursiveDescentParser(EXPR, "E")
    toks = "a + a * a".split()
    t = p.parse(toks)
    assert tree_ok(t, EXPR, toks)
    assert t[0] == "E" and t[1][0] == ("T", (("F", ("a",)), ("T'", ())))
    assert not p.recognize("a + * a".split())
    assert not p.recognize("( a".split())
    assert not p.recognize([])
    assert p.recognize("( ( a ) ) * a + a".split())


def test_grammar_errors() -> None:
    with pytest.raises(GrammarError):
        RecursiveDescentParser([("E", ("E", "+", "a")), ("E", ("a",))], "E")  # left recursion
    with pytest.raises(GrammarError):
        RecursiveDescentParser([("S", ("a", "b")), ("S", ("a", "c"))], "S")  # common prefix
    with pytest.raises(GrammarError):
        RecursiveDescentParser([("S", ("S", "S")), ("S", ("a",)), ("S", ())], "S")  # ambiguous
    with pytest.raises(GrammarError):
        RecursiveDescentParser([("S", ("A", "a")), ("A", ("a",)), ("A", ())], "S")  # FIRST/FOLLOW clash


def test_empty_input_and_epsilon() -> None:
    p = RecursiveDescentParser([("S", ("a", "S", "b")), ("S", ())], "S")
    assert p.parse([]) == ("S", ())
    assert p.recognize(list("aaabbb"))
    assert not p.recognize(list("aab"))
    unit = RecursiveDescentParser([("S", ("A",)), ("A", ("B",)), ("B", ("b",))], "S")
    assert unit.parse(["b"]) == ("S", (("A", (("B", ("b",)),)),))


def test_random_grammars_against_oracle() -> None:
    rng = random.Random(1968)
    accepted = 0
    tried = 0
    while accepted < 500:
        tried += 1
        g = random_grammar(rng)
        start = g[0][0]
        expect = oracle_ll1(g, start)
        try:
            p = RecursiveDescentParser(g, start)
        except GrammarError:
            assert not expect, g
            continue
        assert expect, g
        accepted += 1
        for n in range(0, 5):
            for w in itertools.product("abc", repeat=n):
                w = list(w)
                want = derives(g, start, w)
                try:
                    t = p.parse(w)
                except ParseError:
                    assert not want, (g, w)
                    continue
                assert want and tree_ok(t, g, w), (g, w)
    assert tried > accepted


def test_deep_nesting() -> None:
    p = RecursiveDescentParser(EXPR, "E")
    n = 5000
    toks = ["("] * n + ["a"] + [")"] * n
    assert p.recognize(toks)
    assert not p.recognize(toks[:-1])
