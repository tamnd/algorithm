# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsing-with-derivatives/. The authors are listed in prov/FA07T5.jsonl.

import itertools
import random

from parsing_with_derivatives import (
    EMPTY,
    EPS,
    Deriver,
    from_grammar,
    nullable,
    recognize,
    recognize_naive,
)


def grammar(text):
    prods = []
    for rule in text.split(";"):
        a, rhs = rule.split("->")
        for alt in rhs.split("|"):
            prods.append((a.strip(), tuple(x for x in alt.split() if x != "eps")))
    return prods


def derives_whole(prods, start, w):
    """Oracle: does start derive w? The set of (X, i, j) with X =>* w[i:j], by a
    least fixpoint over all splits."""
    nts = {a for a, _ in prods} | {start}
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
    return (start, 0, n) in known


def random_grammar(rng):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(names + ["a", "b", "a", "b"]) for _ in range(k))))
    return list(dict.fromkeys(prods))


def test_random_grammars_against_brute_force():
    rng = random.Random(2011)
    checked = accepted = 0
    kinds = {"eps": 0, "unit": 0, "left": 0, "cycle": 0, "empty_input_yes": 0, "empty_input_no": 0}
    for _ in range(500):
        g = random_grammar(rng)
        start = g[0][0]
        nts = {a for a, _ in g}
        kinds["eps"] += any(not r for _, r in g)
        kinds["unit"] += any(len(r) == 1 and r[0] in nts for _, r in g)
        kinds["left"] += any(r and r[0] == a for a, r in g)
        kinds["cycle"] += any(r == (a,) for a, r in g)
        for n in range(6):
            for w in itertools.product("ab", repeat=n):
                want = derives_whole(g, start, list(w))
                stats = {}
                got = recognize(g, start, w, stats)
                assert got == want, (g, w)
                # the bound of Adams, Hollenbeck and Might: O(|G| n^3) nodes
                size = sum(len(r) + 1 for _, r in g) + len(nts)
                assert stats["nodes"] <= 4 * size * (n + 1) ** 3
                checked += 1
                accepted += got
                if n == 0:
                    kinds["empty_input_yes" if got else "empty_input_no"] += 1
    assert checked >= 30000 and accepted >= 1500 and checked - accepted >= 2000
    assert min(kinds.values()) >= 50, kinds


def test_page_example():
    g = grammar("S -> S + n | n")
    s = from_grammar(g, "S")
    plus_n = s.a.b  # the node + . n
    assert s.kind == "alt" and s.a.a is s and plus_n.kind == "cat"
    d = Deriver()
    d1 = d.derive(s, "n")
    # S1 = S1 . (+ n) | eps: the memo table ties the cycle
    assert d1.kind == "alt" and d1.a.kind == "cat" and d1.a.a is d1 and d1.a.b is plus_n
    assert d1.b is EPS and nullable(d1) and d.created == 2
    d2 = d.derive(d1, "+")
    # S2 = (S2 . (+ n) | eps . n) | empty
    assert d2.kind == "alt" and d2.b is EMPTY and d2.a.kind == "alt"
    assert d2.a.a.kind == "cat" and d2.a.a.a is d2 and d2.a.a.b is plus_n
    assert d2.a.b.kind == "cat" and d2.a.b.a is EPS and d2.a.b.b.tok == "n"
    assert not nullable(d2) and d.created == 6
    d3 = d.derive(d2, "n")
    # S3 = S3 . (+ n) | eps, the same shape as S1
    assert d3.kind == "alt" and d3.a.a is d3 and d3.a.b is plus_n and d3.b is EPS
    assert nullable(d3) and d.created == 8
    stats = {}
    assert recognize(g, "S", ["n", "+", "n"], stats) and stats["nodes"] == 8
    assert not recognize(g, "S", ["n", "+"])
    assert not recognize(g, "S", [])
    assert not recognize(g, "S", ["+", "n"])


def test_cycles_and_epsilon():
    assert recognize(grammar("S -> S | a"), "S", ["a"])
    assert not recognize(grammar("S -> S | a"), "S", [])
    assert recognize(grammar("S -> S S | eps"), "S", [])
    assert not recognize(grammar("S -> S S | eps"), "S", ["a"])
    assert not recognize(grammar("S -> S"), "S", [])
    assert not recognize(grammar("S -> a S"), "S", ["a", "a"])  # empty language
    assert recognize(grammar("S -> A B; A -> eps | a A; B -> eps | b B"), "S", list("aabbb"))
    assert not recognize(grammar("S -> A B; A -> eps | a A; B -> eps | b B"), "S", list("aba"))


def test_dyck_and_palindromes():
    dyck = grammar("S -> ( S ) S | eps")
    rng = random.Random(5)
    for _ in range(300):
        w = [rng.choice("()") for _ in range(rng.randrange(0, 14))]
        depth, ok = 0, True
        for c in w:
            depth += 1 if c == "(" else -1
            ok = ok and depth >= 0
        assert recognize(dyck, "S", w) == (ok and depth == 0)
    pal = grammar("P -> a P a | b P b | a | b | eps")
    for n in range(9):
        for w in itertools.product("ab", repeat=n):
            assert recognize(pal, "P", w) == (list(w) == list(reversed(w)))


def test_memoization_removes_duplication():
    # L = (a | eps)^k, no recursion: the naive derivative copies the tail twice per nullable head
    k = 12
    g = grammar("S -> " + " ".join(["A"] * k) + "; A -> a | eps")
    for n in range(0, 8):
        w = ["a"] * n
        stats = {}
        got = recognize(g, "S", w, stats)
        ok, built = recognize_naive(from_grammar(g, "S"), w)
        assert got == ok == (n <= k)
        assert stats["nodes"] <= built
    stats = {}
    recognize(g, "S", ["a"] * 6, stats)
    _, built = recognize_naive(from_grammar(g, "S"), ["a"] * 6)
    assert built > 20 * stats["nodes"]


def test_long_inputs_iterative():
    n = 3000
    assert recognize(grammar("S -> a S | eps"), "S", ["a"] * n)
    w = ["n"] + ["+", "n"] * 1500
    assert recognize(grammar("S -> S + n | n"), "S", w)
    assert not recognize(grammar("S -> S + n | n"), "S", w + ["+"])
    nested = ["("] * 300 + [")"] * 300
    assert recognize(grammar("S -> ( S ) S | eps"), "S", nested)
