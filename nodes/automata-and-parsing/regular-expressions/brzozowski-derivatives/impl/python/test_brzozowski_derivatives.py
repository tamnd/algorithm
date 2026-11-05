# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brzozowski-derivatives/. The authors are listed in prov/XAA52M.jsonl.

import itertools
import random

from brzozowski_derivatives import Builder, derivative_dfa, derivative_match

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


def test_example_page():
    b = Builder()
    r = b.build(parse("(a|b)*ab"))
    shown = []
    for c in "bab":
        r = b.derivative(r, c)
        shown.append((b.show(r), b.nullable[r]))
    assert shown == [("(a|b)*ab", False), ("(ε|(a|b)*a)b", False), ("ε|(a|b)*ab", True)]
    assert derivative_match(parse("(a|b)*ab"), "bab")
    assert not derivative_match(parse("(a|b)*ab"), "ba")


def test_example_dfa_sizes():
    sizes = {}
    for text in ["(a|b)*ab", "(a|b)*a(a|b)(a|b)", "(a*)*b", "(a|a)*"]:
        states, delta, accepting = derivative_dfa(parse(text), "ab")
        sizes[text] = len(states)
    assert sizes == {"(a|b)*ab": 3, "(a|b)*a(a|b)(a|b)": 8, "(a*)*b": 3, "(a|a)*": 2}


def test_edge_cases():
    for text, yes, no in [
        ("∅", [], ["", "a"]),
        ("ε", [""], ["a"]),
        ("∅*", [""], ["a"]),
        ("ε*", [""], ["b"]),
        ("((a*)*)*", ["", "aaaa"], ["ab"]),
        ("(ε|∅)*a", ["a"], ["", "aa"]),
        ("a∅|∅", [], ["a", ""]),
    ]:
        r = parse(text)
        assert all(derivative_match(r, w) for w in yes)
        assert not any(derivative_match(r, w) for w in no)
    assert not derivative_match(parse("ab"), "ac")


def test_deep_and_long_without_recursion():
    right = ("sym", "a")
    for _ in range(20000):
        right = ("cat", ("sym", "a"), right)
    assert derivative_match(right, "a" * 20001)
    assert not derivative_match(right, "a" * 20000)
    left = ("sym", "a")
    for _ in range(1500):
        left = ("cat", left, ("sym", "a"))
    assert derivative_match(left, "a" * 1501)
    assert derivative_match(parse("(a|b)*a(a|b)(a|b)"), "ab" * 20000 + "abb")


def dfa_accepts(dfa, w):
    states, delta, accepting = dfa
    q = 0
    for c in w:
        q = delta[q][c]
    return q in accepting


def test_random_against_enumeration():
    rng = random.Random(20261106)
    for trial in range(900):
        alphabet = "ab" if trial % 2 else "abc"
        bound = 6 if alphabet == "ab" else 4
        r = random_regex(rng, alphabet, rng.randint(0, 5))
        expected = language(r, bound)
        b = Builder()
        dfa = derivative_dfa(r, alphabet)
        for w in words(alphabet, bound):
            assert derivative_match(r, w, b) == (w in expected)
            assert dfa_accepts(dfa, w) == (w in expected)


def test_random_nested_stars():
    rng = random.Random(7)
    for _ in range(300):
        r = random_regex(rng, "ab", 3)
        for _ in range(rng.randint(1, 3)):
            r = ("star", ("alt", r, EPS)) if rng.random() < 0.5 else ("star", r)
        expected = language(r, 6)
        b = Builder()
        for w in words("ab", 6):
            assert derivative_match(r, w, b) == (w in expected)
