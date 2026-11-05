# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thompson-nfa-simulation/. The authors are listed in prov/X9HKD8.jsonl.

import itertools
import random

import pytest

from thompson_nfa_simulation import _add, full_match, run, search, thompson

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


def trace(pattern, text):
    nfa = thompson(pattern)
    mark = [-1] * nfa.size
    cur = []
    _add(nfa, cur, mark, nfa.start, 0)
    out = [sorted(cur)]
    for i, a in enumerate(text, start=1):
        nxt = []
        for q in cur:
            m = nfa.sym[q]
            if m is not None and m[0] == a:
                _add(nfa, nxt, mark, m[1], i)
        cur = nxt
        out.append(sorted(cur))
    return out


def test_example():
    t = trace("(a|b)*abb", "abab")
    assert t == [
        [0, 2, 4, 6, 7, 8],
        [0, 1, 2, 4, 5, 7, 8, 9, 10],
        [0, 2, 3, 4, 5, 7, 8, 11, 12],
        [0, 1, 2, 4, 5, 7, 8, 9, 10],
        [0, 2, 3, 4, 5, 7, 8, 11, 12],
    ]
    assert not full_match("(a|b)*abb", "abab")
    assert full_match("(a|b)*abb", "babb")
    for w in words("ab", 9):
        assert full_match("(a|b)*abb", w) == w.endswith("abb")
        assert search("abb", w) == ("abb" in w)


def test_pathological_is_fast():
    n = 30
    p = "(a|ε)" * n + "a" * n
    assert full_match(p, "a" * n)
    assert not full_match(p, "a" * (n - 1))
    assert not full_match(p, "a" * (2 * n + 1))
    assert full_match("(a|a)*b", "a" * 5000 + "b")
    assert not full_match("(a|a)*b", "a" * 5000)


def test_edges():
    assert not full_match("∅", "") and not search("∅", "abc")
    assert full_match("ε", "") and not full_match("ε", "a")
    assert search("ε", "") and search("ε", "abc")
    assert full_match("∅*", "") and not full_match("∅*", "a")
    assert full_match("((a*)*)*", "") and full_match("((a*)*)*", "aaa")
    assert not full_match("a", "")
    assert search("b*", "") and not search("a∅", "aaa")


@pytest.mark.parametrize("alpha", ["ab", "abc"])
def test_random_against_brute_force(alpha):
    rng = random.Random(7 + len(alpha))
    for _ in range(400):
        r = rand_re(rng, alpha, 4)
        p = show(r)
        nfa = thompson(p)
        want = lang(r, 5)
        for w in words(alpha, 5):
            assert run(nfa, w) == (w in want), (p, w)
            subs = {w[i:j] for i in range(len(w) + 1) for j in range(i, len(w) + 1)}
            assert run(nfa, w, search=True) == bool(subs & want), (p, w)


def test_long_text_and_deep_pattern():
    p = "(" * 2000 + "ab" + ")*" * 2000
    assert full_match(p, "ab" * 3000)
    assert not full_match(p, "ab" * 3000 + "a")
