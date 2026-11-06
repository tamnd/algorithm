# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chomsky-normal-form-conversion/. The authors are listed in prov/P1WQJZ.jsonl.

import itertools
import random

import pytest

from chomsky_normal_form_conversion import grammar_size, is_cnf, nullable_set, to_cnf


def g(text):
    """'S -> a S b | ε ; A -> ...' into (start, productions)."""
    prods, start = [], None
    for part in text.split(";"):
        lhs, rhs = part.split("->")
        lhs = lhs.strip()
        start = start or lhs
        for alt in rhs.split("|"):
            prods.append((lhs, tuple(x for x in alt.split() if x != "ε")))
    return start, prods


def fixpoint_member(start, prods, w):
    """Oracle for any grammar: the least set of (X, i, j) with X =>* w[i:j], by naive iteration.

    It handles ε-productions, unit productions and cycles, and it does not use any normal form.
    """
    n = len(w)
    terms = {x for _, r in prods for x in r} - {a for a, _ in prods}
    derives = {(w[i], i, i + 1) for i in range(n)}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                # all end positions j reachable by matching rhs from i
                ends = {i}
                for x in rhs:
                    nxt = set()
                    for k in ends:
                        if x in terms:
                            if k < n and w[k] == x:
                                nxt.add(k + 1)
                        else:
                            for j in range(k, n + 1):
                                if (x, k, j) in derives:
                                    nxt.add(j)
                    ends = nxt
                for j in ends:
                    if (a, i, j) not in derives:
                        derives.add((a, i, j))
                        changed = True
    return (start, 0, n) in derives


def cyk(start, prods, w):
    """Oracle for the output: the CYK algorithm, which is valid only for Chomsky normal form."""
    n = len(w)
    if n == 0:
        return (start, ()) in set(prods)
    t = [[set() for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(n):
        for a, r in prods:
            if r == (w[i],):
                t[i][i + 1].add(a)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length
            for k in range(i + 1, j):
                for a, r in prods:
                    if len(r) == 2 and r[0] in t[i][k] and r[1] in t[k][j]:
                        t[i][j].add(a)
    return start in t[0][n]


def words(alphabet, max_len):
    for k in range(max_len + 1):
        for tup in itertools.product(alphabet, repeat=k):
            yield "".join(tup)


def random_grammar(rng, alphabet="ab"):
    nts = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    prods = set()
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3, 4])
            prods.add((a, tuple(rng.choice(nts + list(alphabet)) for _ in range(k))))
    return "S", sorted(prods)


def check_equivalent(start, prods, terminals, max_len):
    s0, out = to_cnf(start, prods, terminals)
    assert is_cnf(s0, out, terminals)
    alphabet = sorted(terminals)
    count = 0
    for w in words(alphabet, max_len):
        expected = fixpoint_member(start, prods, w)
        assert cyk(s0, out, w) == expected, (prods, w)
        assert fixpoint_member(s0, out, w) == expected, (prods, w)
        count += 1
    return count


def test_example_a_n_b_n():
    s0, out = to_cnf(*g("S -> a S b | ε"), {"a", "b"})
    assert s0 == "S0"
    assert set(out) == {
        ("S0", ()), ("S0", ("T_a", "S_1")), ("S", ("T_a", "S_1")),
        ("S_1", ("S", "T_b")), ("S_1", ("b",)), ("T_a", ("a",)), ("T_b", ("b",)),
    }
    assert grammar_size(out) == 16


def test_example_with_units_and_eps():
    start, prods = g("S -> A S A | a B ; A -> B | S ; B -> b | ε")
    assert grammar_size(prods) == 14
    s0, out = to_cnf(start, prods, {"a", "b"})
    assert len(out) == 19 and grammar_size(out) == 50
    assert set(p for p in out if p[0] == "A") == {
        ("A", ("b",)), ("A", ("A", "S_1")), ("A", ("T_a", "B")), ("A", ("S", "A")), ("A", ("a",)),
    }
    assert nullable_set(prods) == {"A", "B"}
    check_equivalent(start, prods, {"a", "b"}, 7)


@pytest.mark.parametrize("text, terminals", [
    ("S -> ε", "a"),
    ("S -> S", "a"),
    ("S -> S S | ε", "a"),
    ("S -> A ; A -> B ; B -> A | a", "a"),
    ("S -> A B ; A -> a ; B -> B b", "ab"),
    ("S -> S a | ε", "ab"),
    ("E -> E + E | E * E | ( E ) | a", "+*()a"),
    ("E -> E + T | T ; T -> T * F | F ; F -> ( E ) | a", "+*()a"),
    ("S -> a S b | S S | ε", "ab"),
    ("S -> a S a | b S b | a | b | ε", "ab"),
    ("S -> A A A A ; A -> a | ε", "a"),
])
def test_named_grammars(text, terminals):
    start, prods = g(text)
    max_len = 5 if len(terminals) <= 2 else 4
    check_equivalent(start, prods, set(terminals), max_len)


def test_empty_language():
    s0, out = to_cnf(*g("S -> A ; A -> a A"), {"a"})
    assert out == []
    assert not cyk(s0, out, "") and not cyk(s0, out, "a")


def test_start_on_right_side_and_eps():
    s0, out = to_cnf(*g("S -> S S | a | ε"), {"a"})
    assert (s0, ()) in out
    assert all(s0 not in r for _, r in out)


def test_names_do_not_clash():
    start, prods = g("S -> S0 T_a S_1 ; S0 -> a ; T_a -> b ; S_1 -> a S0 | ε")
    s0, out = to_cnf(start, prods, {"a", "b"})
    assert s0 not in {"S", "S0", "T_a", "S_1"}
    check_equivalent(start, prods, {"a", "b"}, 5)


def test_terminal_on_left_side_rejected():
    with pytest.raises(ValueError):
        to_cnf("S", [("a", ("S",)), ("S", ("a",))], {"a"})


def test_size_family_g_k():
    # S -> A1 ... Ak, Ai -> a | ε: the output stays polynomial (DEL after BIN).
    sizes = []
    for k in (2, 4, 6, 8, 40):
        prods = [("S", tuple(f"A{i}" for i in range(1, k + 1)))]
        prods += [(f"A{i}", r) for i in range(1, k + 1) for r in (("a",), ())]
        s0, out = to_cnf("S", prods, {"a"})
        sizes.append(grammar_size(out))
    assert sizes[:4] == [10, 33, 68, 115]
    assert sizes[4] < 40 * 40 * 3


def test_quadratic_unit_chain():
    # A1 -> A2 -> ... -> Ak, and Ak has k binary productions: every Ai receives all k.
    k = 30
    prods = [("S", tuple(f"A{i}" for i in range(1, k + 1)))]
    prods += [(f"A{i}", (f"A{i + 1}",)) for i in range(1, k)]
    prods += [(f"A{k}", (f"B{j}", f"B{j}")) for j in range(1, k + 1)]
    prods += [(f"B{j}", ("b",)) for j in range(1, k + 1)]
    s0, out = to_cnf("S", prods, {"b"})
    binary_of_a = [p for p in out if p[0].startswith("A") and "_" not in p[0] and len(p[1]) == 2]
    assert len(binary_of_a) == k * k
    assert grammar_size(out) <= 60 * grammar_size(prods) ** 2


def test_large_inputs_no_recursion():
    n = 5000
    prods = [("S", tuple(["a"] * n))]  # one long right side
    prods += [(f"U{i}", (f"U{i + 1}",)) for i in range(n)] + [(f"U{n}", ("a",))]
    prods += [("S", ("U0",))]
    s0, out = to_cnf("S", prods, {"a"})
    assert is_cnf(s0, out, {"a"})
    assert (s0, ("a",)) in out


def test_random_against_oracles():
    rng = random.Random(20261106)
    grammars = 0
    inputs = 0
    for _ in range(400):
        alphabet = rng.choice(["a", "ab", "ab", "abc"])
        start, prods = random_grammar(rng, alphabet)
        max_len = {1: 6, 2: 5, 3: 3}[len(alphabet)]
        inputs += check_equivalent(start, prods, set(alphabet), max_len)
        s0, out = to_cnf(start, prods, set(alphabet))
        assert grammar_size(out) <= 60 * grammar_size(prods) ** 2
        grammars += 1
    assert grammars == 400 and inputs >= 500
