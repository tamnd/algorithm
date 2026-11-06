# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epsilon-production-elimination/. The authors are listed in prov/YT0RZM.jsonl.

import itertools
import random

from epsilon_production_elimination import eliminate_epsilon, nullable_set


def language(productions, start, max_len):
    """Independent oracle: every terminal string of length at most max_len that
    start derives, by a least fixed point over sets of short strings."""
    nts = {a for a, _ in productions}
    sets = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            partial = {()}
            for x in rhs:
                opts = sets[x] if x in nts else {(x,)}
                partial = {p + o for p in partial for o in opts if len(p) + len(o) <= max_len}
                if not partial:
                    break
            if not partial <= sets[a]:
                sets[a] |= partial
                changed = True
    return sets.get(start, set())


def nullable_brute(productions):
    nts = {a for a, _ in productions}
    return {a for a in nts if () in language(productions, a, 0)}


def size(productions):
    return sum(len(r) + 1 for _, r in productions)


def random_grammar(rng, max_len=3):
    nts = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    syms = nts + ["a", "b"]
    prods = set()
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.3:
                prods.add((a, ()))
            else:
                prods.add((a, tuple(rng.choice(syms) for _ in range(rng.randint(1, max_len)))))
    return sorted(prods)


def check(g, start):
    for keep in (True, False):
        g2, s2 = eliminate_epsilon(g, start, keep_empty=keep)
        empties = [(a, r) for a, r in g2 if not r]
        nts, lhs2 = {a for a, _ in g}, {a for a, _ in g2}
        assert all(x in lhs2 or x not in nts for _, r in g2 for x in r)
        lang = language(g, start, 5)
        lang2 = language(g2, s2, 5)
        if keep:
            assert lang2 == lang
            if () in lang:
                assert empties == [(s2, ())] and s2 != start
                assert all(s2 not in r for _, r in g2)
            else:
                assert not empties and s2 == start
        else:
            assert not empties and s2 == start
            assert lang2 == lang - {()}


def test_example():
    g = [
        ("S", ("A", "B")),
        ("A", ("a", "A", "A")), ("A", ()),
        ("B", ("b", "B", "B")), ("B", ()),
    ]
    assert nullable_set(g) == {"S", "A", "B"}
    g2, s2 = eliminate_epsilon(g, "S")
    assert s2 == "S'"
    assert g2 == [
        ("S'", ("S",)), ("S'", ()),
        ("S", ("A", "B")), ("S", ("A",)), ("S", ("B",)),
        ("A", ("a", "A", "A")), ("A", ("a", "A")), ("A", ("a",)),
        ("B", ("b", "B", "B")), ("B", ("b", "B")), ("B", ("b",)),
    ]
    check(g, "S")


def test_edge_cases():
    assert eliminate_epsilon([("S", ())], "S") == ([("S'", ())], "S'")
    assert eliminate_epsilon([("S", ())], "S", keep_empty=False) == ([], "S")
    assert eliminate_epsilon([("S", ("a",))], "S") == ([("S", ("a",))], "S")
    g = [("S", ("S", "S")), ("S", ("a",)), ("S", ())]
    check(g, "S")
    g2, _ = eliminate_epsilon(g, "S", keep_empty=False)
    assert g2 == [("S", ("S", "S")), ("S", ("S",)), ("S", ("a",))]


def test_fresh_start_name():
    g = [("S", ("S'", "a")), ("S'", ()), ("S", ())]
    g2, s2 = eliminate_epsilon(g, "S")
    assert s2 == "S''"
    check(g, "S")


def test_exponential_without_binarization():
    k = 6
    g = [("S", tuple(f"A{i}" for i in range(k)))] + [(f"A{i}", ()) for i in range(k)] + [
        (f"A{i}", ("a",)) for i in range(k)
    ]
    g2, _ = eliminate_epsilon(g, "S", keep_empty=False)
    assert sum(1 for a, _ in g2 if a == "S") == 2 ** k - 1


def test_binarized_input_stays_linear():
    rng = random.Random(7)
    for _ in range(300):
        g = random_grammar(rng, max_len=2)
        g2, _ = eliminate_epsilon(g, "S", keep_empty=False)
        assert size(g2) <= 3 * size(g)


def test_random_against_oracle():
    rng = random.Random(20261106)
    for _ in range(600):
        g = random_grammar(rng)
        assert nullable_set(g) == nullable_brute(g)
        check(g, "S")
