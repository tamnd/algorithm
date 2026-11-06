# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unit-production-elimination/. The authors are listed in prov/QDYQHJ.jsonl.

import itertools
import random

from unit_production_elimination import eliminate_units, is_unit, nonterminal_set, unit_pairs

NTS = ["S", "A", "B", "C", "D"]


def grammar(text):
    prods = []
    for rule in text.split(";"):
        a, rhs = rule.split("->")
        for alt in rhs.split("|"):
            prods.append((a.strip(), tuple(x for x in alt.split() if x != "eps")))
    return prods


def spans(prods, nts, w):
    """Independent oracle: the set of (X, i, j) with X =>* w[i:j], by a least fixpoint."""
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


def closure_oracle(prods, nts):
    """Reference: the reflexive transitive closure of the unit relation by Warshall."""
    order = sorted(nts)
    r = {(a, b): a == b for a in order for b in order}
    for a, rhs in prods:
        if len(rhs) == 1 and rhs[0] in nts:
            r[(a, rhs[0])] = True
    for k in order:
        for i in order:
            if r[(i, k)]:
                for j in order:
                    if r[(k, j)]:
                        r[(i, j)] = True
    return {(a, rhs) for a in order for b, rhs in prods if r[(a, b)] and not (len(rhs) == 1 and rhs[0] in nts)}


def random_grammar(rng):
    k = rng.randint(1, 5)
    nts = NTS[:k]
    prods = set()
    for a in nts:
        for _ in range(rng.randint(1, 4)):
            r = rng.random()
            if r < 0.35:
                rhs = (rng.choice(nts),)  # unit production, possibly A -> A
            elif r < 0.45:
                rhs = ()
            else:
                n = rng.choice([1, 2, 2, 3])
                rhs = tuple(rng.choice(nts + ["a", "b"]) for _ in range(n))
                if rng.random() < 0.15:
                    rhs = (a,) + rhs  # left recursion
            prods.add((a, rhs))
    prods = sorted(prods)
    rng.shuffle(prods)
    return prods, set(nts)


def test_expression_grammar():
    g = grammar("E -> E + T | T; T -> T * F | F; F -> ( E ) | a")
    out = eliminate_units(g, "E")
    assert set(out) == set(grammar(
        "E -> E + T | T * F | ( E ) | a; T -> T * F | ( E ) | a; F -> ( E ) | a"))
    assert unit_pairs(g, nonterminal_set(g, "E"))["E"] == ["E", "T", "F"]


def test_unit_cycle():
    g = grammar("S -> A | a b; A -> B | a; B -> S | b")
    out = eliminate_units(g, "S")
    expect = set()
    for x in "SAB":
        expect |= {(x, ("a", "b")), (x, ("a",)), (x, ("b",))}
    assert set(out) == expect and len(out) == 9


def test_self_loop_and_empty():
    assert eliminate_units(grammar("S -> S | a"), "S") == [("S", ("a",))]
    assert eliminate_units(grammar("S -> A; A -> eps"), "S") == [("A", ()), ("S", ())]
    assert eliminate_units(grammar("S -> A; A -> A"), "S") == []
    # a terminal on its own is not a unit production
    assert eliminate_units(grammar("S -> a"), "S") == [("S", ("a",))]
    # a declared nonterminal without productions: S -> X is a unit production
    assert eliminate_units(grammar("S -> X | b"), "S", ["X"]) == [("S", ("b",))]


def test_random_against_oracles():
    rng = random.Random(1106)
    words = [w for n in range(5) for w in itertools.product("ab", repeat=n)]
    comparisons = 0
    for trial in range(800):
        prods, declared = random_grammar(rng)
        nts = nonterminal_set(prods, "S", declared)
        out = eliminate_units(prods, "S", declared)
        assert not any(is_unit(rhs, nts) for _, rhs in out)
        assert len(out) == len(set(out))
        assert set(out) == closure_oracle(prods, nts)
        comparisons += 1
        ws = words if trial < 250 else words[:15]
        for w in ws:
            before, after = spans(prods, nts, w), spans(out, nts, w)
            # every nonterminal keeps its language, not only the start symbol
            for x in nts:
                assert ((x, 0, len(w)) in before) == ((x, 0, len(w)) in after)
                comparisons += 1
    assert comparisons >= 500


def test_quadratic_output():
    k = 300
    prods = []
    for i in range(k):
        prods.append((f"A{i}", (f"t{i}",)))
        if i + 1 < k:
            prods.append((f"A{i}", (f"A{i + 1}",)))
    out = eliminate_units(prods, "A0")
    assert len(out) == k * (k + 1) // 2


def test_long_cycle_without_recursion():
    k = 2000
    prods = [(f"A{i}", (f"A{(i + 1) % k}",)) for i in range(k)] + [("A0", ("x", "y"))]
    out = eliminate_units(prods, "A0")
    assert len(out) == k and all(rhs == ("x", "y") for _, rhs in out)
