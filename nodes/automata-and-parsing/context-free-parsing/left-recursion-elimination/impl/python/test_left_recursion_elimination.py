# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-recursion-elimination/. The authors are listed in prov/KFFADV.jsonl.

import random

from left_recursion_elimination import eliminate_left_recursion, prepare

EXPR = [
    ("E", ("E", "+", "T")), ("E", ("T",)),
    ("T", ("T", "*", "F")), ("T", ("F",)),
    ("F", ("(", "E", ")")), ("F", ("id",)),
]


def lang_upto(prods, max_len):
    """Oracle: for each nonterminal, the strings of length <= max_len that it derives."""
    nts = {a for a, _ in prods}
    lang = {a: set() for a in nts}

    def of(x):
        return lang[x] if x in nts else {(x,)}

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            cur = {()}
            for x in rhs:
                cur = {u + v for u in cur for v in of(x) if len(u) + len(v) <= max_len}
                if not cur:
                    break
            if not cur <= lang[a]:
                lang[a] |= cur
                changed = True
    return lang


def is_left_recursive(prods):
    """True when some nonterminal A has A =>+ A beta, found on the left-corner graph."""
    nts = {a for a, _ in prods}
    null = set()
    changed = True
    while changed:
        changed = False
        for a, r in prods:
            if a not in null and all(x in null for x in r):
                null.add(a)
                changed = True
    edge = {a: set() for a in nts}
    for a, r in prods:
        for x in r:
            if x in nts:
                edge[a].add(x)
            if x not in null:
                break
    for a in nts:
        seen, todo = set(), list(edge[a])
        while todo:
            b = todo.pop()
            if b == a:
                return True
            if b not in seen:
                seen.add(b)
                todo.extend(edge[b])
    return False


def random_grammar(rng, n_nt, terms):
    names = ["S", "A", "B", "C"][:n_nt]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            r = rng.random()
            if r < 0.15:
                rhs = ()
            elif r < 0.3:
                rhs = (rng.choice(names),)  # unit production, maybe a cycle
            elif r < 0.5:
                rhs = (a,) + tuple(rng.choice(names + terms) for _ in range(rng.randint(1, 2)))
            else:
                rhs = tuple(rng.choice(names + terms) for _ in range(rng.randint(1, 3)))
            prods.append((a, rhs))
    return prods


def test_expression_grammar():
    out, start = eliminate_left_recursion(EXPR, "E")
    assert start == "E"
    assert sorted(out) == sorted([
        ("E", ("T", "E'")), ("E'", ("+", "T", "E'")), ("E'", ()),
        ("T", ("F", "T'")), ("T'", ("*", "F", "T'")), ("T'", ()),
        ("F", ("(", "E", ")")), ("F", ("id",)),
    ])


def test_indirect_and_empty():
    g = [("S", ("A", "a")), ("S", ("b",)), ("A", ("A", "c")), ("A", ("S", "d")), ("A", ())]
    out, start = eliminate_left_recursion(g, "S")
    assert not is_left_recursive(out)
    assert lang_upto(out, 8)[start] == lang_upto(g, 8)["S"]
    # empty language, a pure cycle, the empty string only
    assert eliminate_left_recursion([("S", ("S", "a"))], "S")[0] == []
    out, start = eliminate_left_recursion([("S", ("S",)), ("S", ("a",))], "S")
    assert out == [("S", ("a",))]
    out, start = eliminate_left_recursion([("S", ())], "S")
    assert lang_upto(out, 3)[start] == {()}


def test_prepare():
    prods, has_empty = prepare([("S", ("A", "B")), ("A", ("B",)), ("B", ("A",)), ("B", ("b",)), ("A", ())], "S")
    assert has_empty
    assert all(r for _, r in prods)
    assert not any(len(r) == 1 and r[0] == a for a, r in prods)


def test_exponential_growth_depends_on_order():
    m = 8
    g = [("A0", ("a",))]
    for i in range(1, m):
        g += [(f"A{i}", (f"A{i - 1}", "x")), (f"A{i}", (f"A{i - 1}", "y"))]
    fwd, _ = eliminate_left_recursion(g, "A0")
    rev, _ = eliminate_left_recursion(list(reversed(g)), f"A{m - 1}")
    count = lambda ps, a: sum(1 for b, _ in ps if b == a)
    assert count(fwd, f"A{m - 1}") == 2 ** (m - 1)
    assert count(rev, f"A{m - 1}") == 2
    assert lang_upto(fwd, 9)["A7"] == lang_upto(rev, 9)["A7"] == lang_upto(g, 9)["A7"]


def test_random_against_brute_force():
    rng = random.Random(2024)
    terms = ["a", "b"]
    n_lr = 0
    for _ in range(2000):
        g = random_grammar(rng, rng.randint(1, 4), terms)
        if is_left_recursive(g):
            n_lr += 1
        out, start = eliminate_left_recursion(g, "S")
        assert not is_left_recursive(out), (g, out)
        assert lang_upto(out, 7).get(start, set()) == lang_upto(g, 7)["S"], (g, out)
        assert all(not r or r[0] != a for a, r in out)
    assert n_lr > 700
