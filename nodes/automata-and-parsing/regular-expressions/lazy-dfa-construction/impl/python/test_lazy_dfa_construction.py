# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-dfa-construction/. The authors are listed in prov/1VRZ3Y.jsonl.

import itertools
import random

from lazy_dfa_construction import (
    LazyDFA,
    glushkov_nfa,
    lazy_dfa_match,
    lazy_dfa_search,
    thompson_nfa,
)

EMPTY = ("empty",)
EPS = ("eps",)


def parse(text):
    """Parse | , concatenation, *, parentheses, ε and ∅ into the tuple form."""
    pos = 0

    def peek():
        return text[pos] if pos < len(text) else None

    def p_alt():
        nonlocal pos
        r = p_cat()
        while peek() == "|":
            pos += 1
            r = ("alt", r, p_cat())
        return r

    def p_cat():
        items = []
        while peek() is not None and peek() not in "|)":
            items.append(p_rep())
        if not items:
            return EPS
        r = items[0]
        for x in items[1:]:
            r = ("cat", r, x)
        return r

    def p_rep():
        nonlocal pos
        r = p_atom()
        while peek() == "*":
            pos += 1
            r = ("star", r)
        return r

    def p_atom():
        nonlocal pos
        c = peek()
        pos += 1
        if c == "(":
            r = p_alt()
            assert peek() == ")"
            pos += 1
            return r
        if c == "ε":
            return EPS
        if c == "∅":
            return EMPTY
        return ("sym", c)

    r = p_alt()
    assert pos == len(text)
    return r


def language(r, bound):
    """All strings of L(r) of length at most bound, by enumeration."""
    t = r[0]
    if t == "empty":
        return set()
    if t == "eps":
        return {""}
    if t == "sym":
        return {r[1]} if bound >= 1 else set()
    if t == "alt":
        return language(r[1], bound) | language(r[2], bound)
    if t == "cat":
        a, b = language(r[1], bound), language(r[2], bound)
        return {x + y for x in a for y in b if len(x) + len(y) <= bound}
    body = language(r[1], bound) - {""}
    result, frontier = {""}, {""}
    while frontier:
        frontier = {x + y for x in frontier for y in body if len(x) + len(y) <= bound} - result
        result |= frontier
    return result


def words(alphabet, bound):
    for k in range(bound + 1):
        for t in itertools.product(alphabet, repeat=k):
            yield "".join(t)


def random_regex(rng, alphabet, depth):
    if depth == 0 or rng.random() < 0.25:
        x = rng.random()
        if x < 0.08:
            return EMPTY
        if x < 0.18:
            return EPS
        return ("sym", rng.choice(alphabet))
    k = rng.random()
    if k < 0.35:
        return ("alt", random_regex(rng, alphabet, depth - 1), random_regex(rng, alphabet, depth - 1))
    if k < 0.75:
        return ("cat", random_regex(rng, alphabet, depth - 1), random_regex(rng, alphabet, depth - 1))
    return ("star", random_regex(rng, alphabet, depth - 1))


def l_n(n):
    ab = ("alt", ("sym", "a"), ("sym", "b"))
    r = ("cat", ("star", ab), ("sym", "a"))
    for _ in range(n - 1):
        r = ("cat", r, ab)
    return r


def test_example_glushkov_trace():
    d = LazyDFA(glushkov_nfa(parse("(a|b)*ab")))
    assert [sorted(s) for s in d.trace("abab")] == [[0], [1, 3], [2, 4], [1, 3], [2, 4]]
    assert d.built == 3
    assert d.computed == 3
    assert d.accepts("abab")
    assert d.computed == 3  # the second run uses only cached transitions


def test_example_thompson():
    r = parse("(a|b)*ab")
    nfa = thompson_nfa(r)
    assert len(nfa.eps) == 16
    d = LazyDFA(nfa)
    assert d.accepts("abab")
    assert d.built == 3
    assert not d.accepts("aba")


def test_example_blowup_and_flush():
    rng = random.Random(7)
    text = "".join(rng.choice("ab") for _ in range(3000))
    r = l_n(12)
    full = LazyDFA(glushkov_nfa(r))
    assert full.accepts(text) == (text[-12] == "a")
    assert full.built <= len(text) + 1
    small = LazyDFA(glushkov_nfa(r), capacity=100)
    assert small.accepts(text) == full.accepts(text)
    assert small.flushes > 0
    assert len(small.states) <= 100


def test_full_dfa_size_of_l_n():
    for n in range(1, 9):
        d = LazyDFA(glushkov_nfa(l_n(n)))
        todo = [d.start()]
        seen = {todo[0].nfa_set}
        while todo:
            s = todo.pop()
            for c in "ab":
                t = d.step(s, c)
                if t.nfa_set not in seen:
                    seen.add(t.nfa_set)
                    todo.append(t)
        assert len(seen) == 2**n + 1


def test_edge_cases():
    for nfa_of in (thompson_nfa, glushkov_nfa):
        assert not LazyDFA(nfa_of(EMPTY)).accepts("")
        assert not LazyDFA(nfa_of(EMPTY)).accepts("a")
        assert LazyDFA(nfa_of(EPS)).accepts("")
        assert not LazyDFA(nfa_of(EPS)).accepts("a")
        assert LazyDFA(nfa_of(parse("(a*)*"))).accepts("")
        assert LazyDFA(nfa_of(parse("(a*)*"))).accepts("aaa")
        assert not LazyDFA(nfa_of(parse("(a*)*b"))).accepts("aaa")
    assert lazy_dfa_search(EPS, "ab") == [0, 1, 2]
    assert lazy_dfa_search(EMPTY, "ab") == []
    assert lazy_dfa_search(parse("ab*a"), "babbaa") == [5, 6]
    for cap in (1, 2, 3):
        assert lazy_dfa_match(parse("(a|b)*ab"), "abab", capacity=cap)


def test_long_inputs_without_recursion():
    chain = ("sym", "a")
    for _ in range(3000):
        chain = ("cat", chain, ("sym", "a"))
    assert lazy_dfa_match(chain, "a" * 3001)
    assert not lazy_dfa_match(chain, "a" * 3000)
    right = ("sym", "a")
    for _ in range(3000):
        right = ("cat", ("sym", "a"), right)
    assert lazy_dfa_match(right, "a" * 3001)
    assert lazy_dfa_match(parse("(a|b)*a"), "ab" * 50000 + "a")


def test_random_against_enumeration():
    rng = random.Random(2024)
    cases = 0
    for alphabet in ("ab", "abc"):
        for _ in range(350):
            r = random_regex(rng, alphabet, rng.randint(0, 4))
            lang = language(r, 5)
            nfas = (thompson_nfa(r), glushkov_nfa(r))
            for cap in (None, 1, 2, 5):
                ds = [LazyDFA(nfa, cap) for nfa in nfas]
                for w in words(alphabet, 5):
                    for d in ds:
                        assert d.accepts(w) == (w in lang), (r, w, cap)
            cases += 1
    assert cases >= 500


def test_random_search_against_enumeration():
    rng = random.Random(99)
    for _ in range(300):
        alphabet = rng.choice(("ab", "abc"))
        r = random_regex(rng, alphabet, rng.randint(0, 4))
        lang = language(r, 7)
        text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
        want = [i for i in range(len(text) + 1) if any(text[j:i] in lang for j in range(i + 1))]
        for cap in (None, 1, 3):
            assert lazy_dfa_search(r, text, capacity=cap) == want, (r, text, cap)


def test_random_nested_stars():
    rng = random.Random(5)
    for _ in range(200):
        alphabet = rng.choice(("ab", "abc"))
        r = random_regex(rng, alphabet, 3)
        for _ in range(rng.randint(1, 3)):
            r = ("star", ("alt", r, EPS) if rng.random() < 0.5 else r)
        lang = language(r, 5)
        d = LazyDFA(thompson_nfa(r), capacity=2)
        for w in words(alphabet, 5):
            assert d.accepts(w) == (w in lang), (r, w)
