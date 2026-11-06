# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cfg-to-pda-conversion/. The authors are listed in prov/X117M6.jsonl.

import itertools
import random

import pytest

from cfg_to_pda_conversion import EPS, PDA, cfg_to_pda, cfg_to_pda_final_state, leftmost_run


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


def grammar_member(start, prods, w):
    """Oracle 1: the least fixpoint of {(X, i, j) : X =>* w[i:j]}, exact for every grammar."""
    n = len(w)
    t = {(w[i], i, i + 1) for i in range(n)}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                cur = {i}
                for x in rhs:
                    cur = {j for p in cur for j in range(p, n + 1) if (x, p, j) in t}
                for j in cur:
                    if (a, i, j) not in t:
                        t.add((a, i, j))
                        changed = True
    return (start, 0, n) in t


def to_empty_stack(pda):
    """Generic conversion from acceptance by final state to acceptance by empty stack."""
    if pda.final_states is None:
        return pda
    out = PDA(set(pda.states) | {"p0", "e"}, set(pda.input_alphabet), set(pda.stack_alphabet) | {"X0"})
    for (q, a, x), lst in pda.moves.items():
        for r, push in lst:
            out.add(q, a, x, r, push)
    out.add("p0", EPS, "X0", pda.start_state, (pda.start_symbol, "X0"))
    for y in out.stack_alphabet:
        for q in pda.final_states | {"e"}:
            out.add(q, EPS, y, "e", ())
    out.start_state, out.start_symbol = "p0", "X0"
    return out


def pda_accepts(pda, w):
    """Oracle 2: generic PDA membership by summaries R = {(p, X, r, i, j)} with
    (p, w[i:j], X) |-* (r, eps, eps), computed as a least fixpoint. It works for every PDA,
    including runs whose stack grows without bound."""
    pda = to_empty_stack(pda)
    n = len(w)
    moves = [(p, a, x, r, push) for (p, a, x), lst in pda.moves.items() for r, push in lst]
    summ = set()
    by_start = {}
    changed = True
    while changed:
        changed = False
        for p, a, x, r0, push in moves:
            for i in range(n + 1):
                if a == EPS:
                    j0 = i
                elif i < n and w[i] == a:
                    j0 = i + 1
                else:
                    continue
                cur = {(r0, j0)}
                for y in push:
                    cur = {(r2, j2) for (r1, j1) in cur for (r2, j2) in by_start.get((r1, y, j1), ())}
                    if not cur:
                        break
                for r, j in cur:
                    if (p, x, r, i, j) not in summ:
                        summ.add((p, x, r, i, j))
                        by_start.setdefault((p, x, i), set()).add((r, j))
                        changed = True
    return any((pda.start_state, pda.start_symbol, r, 0, n) in summ for r in pda.states)


def words(alpha, maxlen):
    for k in range(maxlen + 1):
        for t in itertools.product(alpha, repeat=k):
            yield "".join(t)


def rand_grammar(rng):
    nts = ["S", "A", "B"][: rng.randint(1, 3)]
    prods = set()
    for a in nts:
        for _ in range(rng.randint(1, 3)):
            k = rng.randint(0, 3)
            prods.add((a, tuple(rng.choice(nts + ["a", "b"]) for _ in range(k))))
    return "S", sorted(prods)


def test_example_trace():
    s, p = g("S -> a S b | ε")
    pda = cfg_to_pda(s, p, "ab")
    assert pda.states == {"q"} and pda.number_of_moves() == 4
    run = leftmost_run(pda, [("S", ("a", "S", "b")), ("S", ("a", "S", "b")), ("S", ())], "aabb")
    stacks = ["".join(st) for _, _, st in run]
    assert stacks == ["S", "aSb", "Sb", "aSbb", "Sbb", "bb", "b", ""]
    assert [pos for _, pos, _ in run] == [0, 0, 1, 1, 2, 2, 3, 4]
    assert len(run) - 1 == 7  # |w| match moves plus 3 expand moves


def test_bad_derivation_rejected():
    s, p = g("S -> a S b | ε")
    pda = cfg_to_pda(s, p, "ab")
    with pytest.raises(ValueError):
        leftmost_run(pda, [("S", ("a", "S", "b")), ("S", ())], "aabb")
    with pytest.raises(ValueError):
        leftmost_run(pda, [("S", ("b",))], "b")


def test_size():
    s, p = g("E -> E + T | T ; T -> T * F | F ; F -> ( E ) | a")
    pda = cfg_to_pda(s, p, "+*()a")
    assert pda.number_of_moves() == len(p) + 5
    fin = cfg_to_pda_final_state(s, p, "+*()a")
    assert fin.number_of_moves() == len(p) + 5 + 2 and fin.final_states == {"f"}


def test_examples():
    s, p = g("E -> E + T | T ; T -> T * F | F ; F -> ( E ) | a")
    for mode in (cfg_to_pda, cfg_to_pda_final_state):
        pda = mode(s, p, "+*()a")
        for w, ok in [("a", True), ("a+a*a", True), ("(a+a)*a", True), ("a+", False), ("", False), ("(a", False)]:
            assert pda_accepts(pda, w) == ok
    s, p = g("S -> S S | a S b | ε")  # cyclic and ambiguous, empty input
    pda = cfg_to_pda(s, p, "ab")
    assert pda_accepts(pda, "") and pda_accepts(pda, "abab") and not pda_accepts(pda, "ba")


def test_symbol_clash():
    with pytest.raises(ValueError):
        cfg_to_pda("S", [("S", ("a",)), ("a", ())], "a")


def test_random_against_grammar():
    rng = random.Random(20261106)
    checked = 0
    for _ in range(120):
        s, p = rand_grammar(rng)
        e = cfg_to_pda(s, p, "ab")
        f = cfg_to_pda_final_state(s, p, "ab")
        for w in words("ab", 4):
            want = grammar_member(s, p, w)
            assert pda_accepts(e, w) == want, (p, w)
            assert pda_accepts(f, w) == want, (p, w)
            checked += 1
    assert checked >= 500
