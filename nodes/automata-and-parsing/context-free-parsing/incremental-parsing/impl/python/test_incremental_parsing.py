# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-parsing/. The authors are listed in prov/3Y0Y57.jsonl.

"""Tests for incremental Earley recognition against a full reparse and a
brute-force derivation oracle."""

import random

from incremental_parsing import (Grammar, accepts, earley_chart, recognize_after_edit,
                                 reparse)

EXPR = [("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("(", "E", ")")), ("T", ("a",))]


def derives(productions, start, w):
    """Brute-force oracle: the least set of (A, i, j) with A =>* w[i:j],
    found by iterating to a fixed point over all spans."""
    n = len(w)
    nts = {a for a, _ in productions}
    known = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            for i in range(n + 1):
                ends = {i}
                for x in rhs:
                    nxt = set()
                    for e in ends:
                        if x in nts:
                            nxt.update(f for f in range(e, n + 1) if (x, e, f) in known)
                        elif e < n and w[e] == x:
                            nxt.add(e + 1)
                    ends = nxt
                for j in ends:
                    if (a, i, j) not in known:
                        known.add((a, i, j))
                        changed = True
    return (start, 0, n) in known


def random_grammar(rng, letters):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            r = rng.random()
            if r < 0.15:
                rhs = ()
            elif r < 0.3:
                rhs = (rng.choice(names),)
            elif r < 0.45:
                rhs = (a,) + tuple(rng.choice(names + letters) for _ in range(rng.randint(1, 2)))
            else:
                rhs = tuple(rng.choice(names + letters) for _ in range(rng.randint(1, 3)))
            if (a, rhs) not in prods:
                prods.append((a, rhs))
    return prods


def test_example_from_the_page():
    g = Grammar(EXPR, "E")
    w = list("a+(a)+a")
    chart = earley_chart(g, w)
    w2, new, recomputed = reparse(g, w, chart, 3, 4, list("a+a"))
    assert "".join(w2) == "a+(a+a)+a"
    assert recomputed == 4
    assert new == earley_chart(g, w2)
    assert new[:4] == chart[:4]
    assert accepts(g, new)


def test_equal_sets_with_a_changed_origin_do_not_anchor():
    # After the edit x -> y, the sets after "a" are equal to the old ones,
    # but their origin 1 points to a set that changed, so they must not be reused.
    prods = [("S", ("x", "A", "c")), ("S", ("y", "A", "d")), ("A", ("a", "A")), ("A", ("z",))]
    g = Grammar(prods, "S")
    w = list("xaazc")
    chart = earley_chart(g, w)
    assert accepts(g, chart)
    w2, new, recomputed = reparse(g, w, chart, 0, 1, ["y"])
    assert new[2] == chart[2]
    assert recomputed == 5
    assert not accepts(g, new)
    assert new == earley_chart(g, w2)


def test_insertion_shifts_the_origin_at_the_edit():
    g = Grammar(EXPR, "E")
    w = list("a+(a)")
    chart = earley_chart(g, w)
    w2, new, recomputed = reparse(g, w, chart, 2, 2, list("a+"))
    assert "".join(w2) == "a+a+(a)"
    assert recomputed == 2
    assert new == earley_chart(g, w2)


def test_empty_input_and_empty_edits():
    g = Grammar([("S", ()), ("S", ("S", "a"))], "S")
    chart = earley_chart(g, [])
    assert accepts(g, chart)
    w2, new, _ = reparse(g, [], chart, 0, 0, [])
    assert w2 == [] and new == chart
    w2, new, _ = reparse(g, [], chart, 0, 0, ["a", "a"])
    assert new == earley_chart(g, w2) and accepts(g, new)
    w2, new2, _ = reparse(g, w2, new, 0, 2, [])
    assert w2 == [] and new2 == chart


def test_random_edits_match_full_reparse_and_oracle():
    rng = random.Random(20261106)
    cases = 0
    reused = 0
    accepted = 0
    for _ in range(700):
        letters = rng.choice([["a"], ["a", "b"]])
        prods = random_grammar(rng, letters)
        g = Grammar(prods, "S")
        w = [rng.choice(letters) for _ in range(rng.randint(0, 6))]
        chart = earley_chart(g, w)
        for _ in range(3):
            p = rng.randint(0, len(w))
            q = rng.randint(p, len(w))
            v = [rng.choice(letters) for _ in range(rng.randint(0, 3))]
            w2, new, recomputed = reparse(g, w, chart, p, q, v)
            assert w2 == w[:p] + v + w[q:]
            assert new == earley_chart(g, w2)
            assert accepts(g, new) == derives(prods, "S", w2)
            assert recognize_after_edit(g, w, chart, p, q, v) == accepts(g, new)
            reused += recomputed < len(w2) - p
            accepted += accepts(g, new)
            cases += 1
            w, chart = w2, new
    assert cases >= 2000
    assert reused > 500
    assert accepted > 250


def test_ambiguous_and_cyclic_grammars():
    rng = random.Random(7)
    grammars = [
        [("S", ("S", "S")), ("S", ("a",)), ("S", ())],
        [("S", ("A",)), ("A", ("S",)), ("A", ("a",)), ("S", ("S", "b"))],
        [("S", ("A", "S", "B")), ("S", ()), ("A", ("a",)), ("A", ()), ("B", ("b",))],
    ]
    for prods in grammars:
        g = Grammar(prods, "S")
        for _ in range(60):
            w = [rng.choice("ab") for _ in range(rng.randint(0, 7))]
            chart = earley_chart(g, w)
            p = rng.randint(0, len(w))
            q = rng.randint(p, len(w))
            v = [rng.choice("ab") for _ in range(rng.randint(0, 3))]
            w2, new, _ = reparse(g, w, chart, p, q, v)
            assert new == earley_chart(g, w2)
            assert accepts(g, new) == derives(prods, "S", w2)


def test_long_input_reuses_the_suffix():
    g = Grammar(EXPR, "E")
    w = list("a" + "+a" * 1500)
    chart = earley_chart(g, w)
    w2, new, recomputed = reparse(g, w, chart, 1000, 1001, list("(a+a)"))
    assert recomputed <= 6
    assert accepts(g, new)
    assert new == earley_chart(g, w2)
