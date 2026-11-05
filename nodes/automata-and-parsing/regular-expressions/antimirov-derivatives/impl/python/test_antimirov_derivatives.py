# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/antimirov-derivatives/. The authors are listed in prov/B0378X.jsonl.

import itertools
import random

from antimirov_derivatives import PDAutomaton, antimirov_match, symbol_occurrences

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


def names(a, xs):
    return sorted(a.terms.show(x) for x in xs)


def test_example():
    a = PDAutomaton(parse("(a|b)*ab"))
    t = a.terms
    r = a.start
    assert names(a, a.states) == ["(a | b)*ab", "b", "ε"]
    assert names(a, t.partial(r, "a")) == ["(a | b)*ab", "b"]
    assert names(a, t.partial(r, "b")) == ["(a | b)*ab"]
    assert names(a, a.final) == ["ε"]
    assert a.transitions() == 4
    assert [w for w in words("ab", 4) if a.accepts(w)] == ["ab", "aab", "bab", "aaab", "abab", "baab", "bbab"]


def test_bound_is_reached():
    a = PDAutomaton(parse("(a|ε)(a|ε)a"))
    assert len(a.states) == symbol_occurrences(parse("(a|ε)(a|ε)a")) + 1 == 4


def test_quadratic_transitions():
    for n in range(1, 8):
        letters = "abcdefg"[:n]
        a = PDAutomaton(parse("".join(c + "*" for c in letters)))
        assert len(a.states) == n
        assert a.transitions() == n * (n + 1) // 2


def test_edge_cases():
    assert not antimirov_match(EMPTY, "")
    assert antimirov_match(EPS, "")
    assert not antimirov_match(EPS, "a")
    assert antimirov_match(parse("a*"), "")
    assert antimirov_match(parse("((a*)*)*"), "aaa")
    assert not antimirov_match(parse("a∅"), "a")
    assert not antimirov_match(parse("∅*a"), "")
    assert antimirov_match(parse("∅*a"), "a")
    assert not antimirov_match(parse("ab"), "abc")
    assert len(PDAutomaton(parse("a∅|b")).states) <= 3
    assert len(PDAutomaton(EMPTY).states) == 1


def test_deep_inputs():
    n = 4000
    r = ("sym", "a")
    for _ in range(n - 1):
        r = ("cat", r, ("sym", "a"))
    assert antimirov_match(r, "a" * n)
    assert not antimirov_match(r, "a" * (n - 1))
    s = ("sym", "a")
    for _ in range(n):
        s = ("star", s)
    assert antimirov_match(s, "aaa")
    u = ("sym", "b")
    for _ in range(n):
        u = ("alt", ("sym", "a"), u)
    assert antimirov_match(u, "b")
    assert len(PDAutomaton(u).states) == 2


def test_random_against_enumeration():
    rng = random.Random(1996)
    cases = 0
    for alphabet, bound in (("ab", 6), ("abc", 4)):
        for _ in range(400):
            r = random_regex(rng, alphabet, rng.randint(0, 5))
            want = language(r, bound)
            a = PDAutomaton(r)
            k = symbol_occurrences(r)
            assert len(a.states) <= k + 1
            for w in words(alphabet, bound):
                assert a.accepts(w) == (w in want), (r, w)
            cases += 1
    assert cases >= 500


def test_states_denote_quotients():
    rng = random.Random(7)
    for _ in range(300):
        alphabet = rng.choice(["ab", "abc"])
        bound = 5 if alphabet == "ab" else 3
        r = random_regex(rng, alphabet, rng.randint(0, 4))
        a = PDAutomaton(r)
        lang = language(r, bound + 1)
        for x in a.states:
            for c in alphabet:
                union = set()
                for y in a.terms.partial(x, c):
                    union |= {w for w in words(alphabet, bound) if a.accepts_from(y, w)}
                from_x = {w for w in words(alphabet, bound + 1) if a.accepts_from(x, w)}
                assert union == {w[1:] for w in from_x if w[:1] == c and len(w) <= bound + 1}
        assert {w for w in words(alphabet, bound + 1) if a.accepts_from(a.start, w)} == lang


def as_tuple(terms, x):
    node = terms.node[x]
    kind = ("empty", "eps", "sym", "alt", "cat", "star")[node[0]]
    if kind in ("empty", "eps"):
        return (kind,)
    if kind == "sym":
        return ("sym", node[1])
    return (kind,) + tuple(as_tuple(terms, c) for c in node[1:])


def test_each_state_against_its_term():
    rng = random.Random(11)
    for _ in range(300):
        alphabet = rng.choice(["ab", "abc"])
        bound = 5 if alphabet == "ab" else 3
        r = random_regex(rng, alphabet, rng.randint(0, 5))
        a = PDAutomaton(r)
        for x in a.states:
            want = language(as_tuple(a.terms, x), bound)
            got = {w for w in words(alphabet, bound) if a.accepts_from(x, w)}
            assert got == want
            assert (x in a.final) == ("" in want)
