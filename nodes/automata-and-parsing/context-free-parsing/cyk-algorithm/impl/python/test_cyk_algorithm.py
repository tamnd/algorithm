# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyk-algorithm/. The authors are listed in prov/0KFTGG.jsonl.

import itertools
import random

import pytest

from cyk_algorithm import cyk_parse, cyk_recognize, cyk_table

EXAMPLE = [
    ("S", ("A", "B")), ("S", ("B", "C")),
    ("A", ("B", "A")), ("A", ("a",)),
    ("B", ("C", "C")), ("B", ("b",)),
    ("C", ("A", "B")), ("C", ("a",)),
]


def derives(productions, start, w):
    """Independent oracle: least fixpoint of 'A derives w[i:j]' over all spans.
    Works for any grammar, with empty, unit and left-recursive productions."""
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


def tree_ok(tree, productions, w):
    """The tree uses only productions and its leaves spell w."""
    prods = {(a, tuple(r)) for a, r in productions}
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


def to_cnf(productions, start, terminals):
    """Textbook conversion used to feed general grammars to CYK."""
    prods = [(a, tuple(r)) for a, r in productions] + [("S0", (start,))]
    fresh = itertools.count()
    # terminals inside long right sides
    out = []
    for a, r in prods:
        if len(r) >= 2:
            r = tuple(("T_" + x) if x in terminals else x for x in r)
        out.append((a, r))
    out += [("T_" + t, (t,)) for t in terminals]
    # binarize
    prods, out = out, []
    for a, r in prods:
        while len(r) > 2:
            n = f"N{next(fresh)}"
            out.append((a, (r[0], n)))
            a, r = n, r[1:]
        out.append((a, r))
    # remove empty productions
    nullable = set()
    changed = True
    while changed:
        changed = False
        for a, r in out:
            if a not in nullable and all(x in nullable for x in r):
                nullable.add(a)
                changed = True
    prods, out = out, set()
    for a, r in prods:
        for keep in itertools.product([True, False], repeat=len(r)):
            if any(not k and x not in nullable for k, x in zip(keep, r)):
                continue
            nr = tuple(x for k, x in zip(keep, r) if k)
            if nr:
                out.add((a, nr))
    nts = {a for a, _ in prods}
    # remove unit productions
    unit = {a: {a} for a in nts}
    changed = True
    while changed:
        changed = False
        for a, r in out:
            if len(r) == 1 and r[0] in nts:
                for x in list(unit):
                    if a in unit[x] and r[0] not in unit[x]:
                        unit[x].add(r[0])
                        changed = True
    final = set()
    for x in nts:
        for a, r in out:
            if a in unit[x] and not (len(r) == 1 and r[0] in nts):
                final.add((x, r))
    if "S0" in nullable:
        final.add(("S0", ()))
    # drop productions that mention a nonterminal with no productions
    while True:
        lhs = {a for a, _ in final}
        bad = {(a, r) for a, r in final if any(x not in lhs and x not in terminals for x in r)}
        if not bad:
            break
        final -= bad
    return sorted(final), "S0"


def random_grammar(rng):
    nts = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    prods = []
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(nts + ["a", "b"]) for _ in range(k))))
    return prods


def random_cnf(rng):
    nts = ["S", "A", "B", "C", "D"][: rng.randint(1, 5)]
    prods = set()
    for a in nts:
        for _ in range(rng.randint(1, 4)):
            if rng.random() < 0.35:
                prods.add((a, (rng.choice("ab"),)))
            else:
                prods.add((a, (rng.choice(nts), rng.choice(nts))))
    for a in nts:
        prods.add((a, (rng.choice("ab"),)))
    return sorted(prods)


def test_example_table():
    T, _ = cyk_table(EXAMPLE, "S", "baaba")
    rows = {1: ["B", "AC", "AC", "B", "AC"], 2: ["AS", "B", "CS", "AS"], 3: ["", "B", "B"], 4: ["", "ACS"], 5: ["ACS"]}
    for length, want in rows.items():
        got = ["".join(sorted(T[i][i + length - 1])) for i in range(5 - length + 1)]
        assert got == want
    assert cyk_recognize(EXAMPLE, "S", "baaba")
    tree = cyk_parse(EXAMPLE, "S", "baaba")
    assert tree == ("S", (("B", ("b",)), ("C", (("A", ("a",)), ("B", (("C", (("A", ("a",)), ("B", ("b",)))), ("C", ("a",))))))))


def test_edges():
    assert not cyk_recognize(EXAMPLE, "S", "")
    assert cyk_parse(EXAMPLE, "S", "") is None
    assert cyk_recognize([("S", ()), ("S", ("a",))], "S", "")
    assert cyk_parse([("S", ()), ("S", ("a",))], "S", "") == ("S", ())
    assert not cyk_recognize(EXAMPLE, "S", "a")
    assert cyk_recognize(EXAMPLE, "S", "ab")
    assert not cyk_recognize(EXAMPLE, "S", "c")
    with pytest.raises(ValueError):
        cyk_recognize([("S", ("A",)), ("A", ("a",))], "S", "a")  # unit production
    with pytest.raises(ValueError):
        cyk_recognize([("S", ("a", "S")), ("S", ("a",))], "S", "aa")  # terminal in a pair
    with pytest.raises(ValueError):
        cyk_recognize([("S", ()), ("S", ("S", "S")), ("S", ("a",))], "S", "a")


def test_long_input_iterative_tree():
    g = [("S", ("A", "S")), ("S", ("a",)), ("A", ("a",))]
    w = "a" * 120
    tree = cyk_parse(g, "S", w)
    assert tree is not None and tree_ok(tree, g, w)


def test_random_cnf_against_oracle():
    rng = random.Random(7)
    for _ in range(400):
        g = random_cnf(rng)
        for _ in range(4):
            w = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
            want = derives(g, "S", w)
            assert cyk_recognize(g, "S", w) == want
            tree = cyk_parse(g, "S", w)
            assert (tree is not None) == want
            if tree is not None:
                assert tree_ok(tree, g, w)


def test_random_general_grammars_via_cnf():
    rng = random.Random(11)
    for _ in range(400):
        g = random_grammar(rng)
        cnf, s0 = to_cnf(g, "S", {"a", "b"})
        for length in range(0, 6):
            w = "".join(rng.choice("ab") for _ in range(length))
            want = derives(g, "S", w)
            if not cnf:
                assert not want
                continue
            assert cyk_recognize(cnf, s0, w) == want
            tree = cyk_parse(cnf, s0, w)
            assert (tree is not None) == want
            if tree is not None:
                assert tree_ok(tree, cnf, w)


def test_ambiguous_and_left_recursive():
    # S -> S S | a in CNF is left recursive and ambiguous
    g = [("S", ("S", "S")), ("S", ("a",))]
    for n in range(1, 9):
        assert cyk_recognize(g, "S", "a" * n)
    assert not cyk_recognize(g, "S", "ab")
