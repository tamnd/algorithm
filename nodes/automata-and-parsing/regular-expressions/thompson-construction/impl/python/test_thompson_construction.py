# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thompson-construction/. The authors are listed in prov/WDNKY8.jsonl.

import itertools
import random

import pytest

from thompson_construction import accepts, thompson, to_postfix

# A brute-force reference: the language of an expression up to a length bound,
# computed from a small recursive parser on short random patterns only.


def parse(p):
    p = p.replace(" ", "")
    i = 0

    def alt():
        nonlocal i
        r = cat()
        while i < len(p) and p[i] == "|":
            i += 1
            r = ("alt", r, cat())
        return r

    def cat():
        r = None
        while i < len(p) and p[i] not in "|)":
            x = star()
            r = x if r is None else ("cat", r, x)
        return r

    def star():
        nonlocal i
        r = atom()
        while i < len(p) and p[i] == "*":
            i += 1
            r = ("star", r)
        return r

    def atom():
        nonlocal i
        c = p[i]
        i += 1
        if c == "(":
            r = alt()
            i += 1
            return r
        return ("eps",) if c == "ε" else ("empty",) if c == "∅" else ("sym", c)

    return alt()


def lang(r, n):
    t = r[0]
    if t == "empty":
        return set()
    if t == "eps":
        return {""}
    if t == "sym":
        return {r[1]}
    if t == "alt":
        return lang(r[1], n) | lang(r[2], n)
    if t == "cat":
        a, b = lang(r[1], n), lang(r[2], n)
        return {x + y for x in a for y in b if len(x + y) <= n}
    base = lang(r[1], n) - {""}
    out, frontier = {""}, {""}
    while frontier:
        frontier = {x + y for x in frontier for y in base if len(x + y) <= n} - out
        out |= frontier
    return out


def size(r):
    return 1 + sum(size(x) for x in r[1:] if isinstance(x, tuple))


def show(r):
    t = r[0]
    if t in ("eps", "empty"):
        return "ε" if t == "eps" else "∅"
    if t == "sym":
        return r[1]
    if t == "star":
        return "(" + show(r[1]) + ")*"
    op = "|" if t == "alt" else ""
    return "(" + show(r[1]) + op + show(r[2]) + ")"


def rand_re(rng, alpha, depth):
    if depth == 0 or rng.random() < 0.25:
        k = rng.random()
        return ("empty",) if k < 0.1 else ("eps",) if k < 0.2 else ("sym", rng.choice(alpha))
    k = rng.random()
    if k < 0.35:
        return ("alt", rand_re(rng, alpha, depth - 1), rand_re(rng, alpha, depth - 1))
    if k < 0.7:
        return ("cat", rand_re(rng, alpha, depth - 1), rand_re(rng, alpha, depth - 1))
    return ("star", rand_re(rng, alpha, depth - 1))


def words(alpha, n):
    for k in range(n + 1):
        for t in itertools.product(alpha, repeat=k):
            yield "".join(t)


def check_shape(nfa, m):
    assert nfa.size <= 2 * m
    moves = sum(len(e) for e in nfa.eps) + sum(x is not None for x in nfa.sym)
    assert moves <= 4 * m
    incoming = [0] * nfa.size
    for q in range(nfa.size):
        out = list(nfa.eps[q]) + ([nfa.sym[q][1]] if nfa.sym[q] else [])
        assert len(out) <= 2
        assert not (nfa.sym[q] and nfa.eps[q])
        for r in out:
            incoming[r] += 1
    assert incoming[nfa.start] == 0
    assert not nfa.eps[nfa.accept] and nfa.sym[nfa.accept] is None


def test_example():
    nfa = thompson("(a|b)*abb")
    assert nfa.size == 14 and nfa.start == 6 and nfa.accept == 13
    assert nfa.sym[0] == ("a", 1) and nfa.sym[2] == ("b", 3)
    assert nfa.eps[4] == [0, 2] and nfa.eps[5] == [4, 7] and nfa.eps[6] == [4, 7]
    assert nfa.eps[7] == [8] and nfa.eps[9] == [10] and nfa.eps[11] == [12]
    for w in words("ab", 8):
        assert accepts(nfa, w) == w.endswith("abb")


def test_edges():
    assert not accepts(thompson("∅"), "")
    assert accepts(thompson("ε"), "") and not accepts(thompson("ε"), "a")
    assert accepts(thompson("∅*"), "") and not accepts(thompson("∅*"), "a")
    assert accepts(thompson("((a*)*)*"), "aaaa")
    assert not accepts(thompson("(ab*)*"), "b")  # the shortcut star would accept it
    for bad in ["", "|a", "a|", "*", "(a", "a)", "()", "a(|b)"]:
        with pytest.raises(ValueError):
            to_postfix(bad)


@pytest.mark.parametrize("alpha", ["ab", "abc"])
def test_random_against_brute_force(alpha):
    rng = random.Random(len(alpha))
    for _ in range(400):
        r = rand_re(rng, alpha, 4)
        p = show(r)
        assert parse(p) is not None
        nfa = thompson(p)
        check_shape(nfa, size(parse(p)))
        want = lang(r, 5)
        for w in words(alpha, 5):
            assert accepts(nfa, w) == (w in want), (p, w)


def test_deep_nesting_needs_no_recursion():
    p = "(" * 3000 + "a" + ")*" * 3000
    nfa = thompson(p)
    assert accepts(nfa, "aaa") and not accepts(nfa, "b")
    long = "a" * 5000
    assert accepts(thompson(long), long)
