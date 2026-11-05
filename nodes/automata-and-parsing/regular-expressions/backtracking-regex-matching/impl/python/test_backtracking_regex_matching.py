# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backtracking-regex-matching/. The authors are listed in prov/AA2R4Q.jsonl.

import itertools
import random

from backtracking_regex_matching import backtracking_match

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


def test_example_one_backtrack():
    stats = {}
    assert backtracking_match(parse("(a|ab)c"), "abc", stats)
    assert stats["steps"] == 9
    for w in words("abc", 4):
        assert backtracking_match(parse("(a|ab)c"), w) == (w in {"ac", "abc"})


def test_example_empty_iteration_cut():
    stats = {}
    assert backtracking_match(parse("(a|ε)*b"), "ab", stats)
    assert stats["steps"] == 12
    for w in words("ab", 6):
        assert backtracking_match(parse("(a|ε)*b"), w) == (w == "a" * (len(w) - 1) + "b")


def test_example_exponential_counts():
    for n in range(1, 13):
        s1, s2 = {}, {}
        assert not backtracking_match(parse("(a|a)*b"), "a" * n, s1)
        assert not backtracking_match(parse("(a*)*b"), "a" * n, s2)
        assert s1["steps"] == 12 * 2**n - 6
        assert s2["steps"] == 9 * 2**n - 3
    stats = {}
    assert backtracking_match(parse("(a|a)*b"), "a" * 20 + "b", stats)
    assert stats["steps"] == 87


def test_edge_cases():
    assert not backtracking_match(EMPTY, "")
    assert not backtracking_match(EMPTY, "a")
    assert backtracking_match(EPS, "")
    assert not backtracking_match(EPS, "a")
    assert backtracking_match(("star", EMPTY), "")
    assert not backtracking_match(("star", EMPTY), "a")
    assert backtracking_match(("star", EPS), "")
    assert not backtracking_match(("star", EPS), "b")
    assert backtracking_match(parse("((a*)*)*"), "")
    assert backtracking_match(parse("((a*)*)*"), "aaaa")
    assert not backtracking_match(parse("((a*)*)*"), "ab")
    assert backtracking_match(parse("(ε|∅)*a"), "a")
    assert not backtracking_match(parse("a∅|∅"), "a")


def test_long_text_without_recursion():
    n = 20000
    assert backtracking_match(parse("(a|b)*c"), "ab" * n + "c")
    assert not backtracking_match(parse("a*"), "a" * n + "b")
    deep = ("sym", "a")
    for _ in range(3000):
        deep = ("cat", EPS, deep)
    assert backtracking_match(deep, "a")


def test_random_against_enumeration():
    rng = random.Random(20261106)
    for trial in range(900):
        alphabet = "ab" if trial % 2 else "abc"
        bound = 6 if alphabet == "ab" else 4
        r = random_regex(rng, alphabet, rng.randint(0, 5))
        expected = language(r, bound)
        for w in words(alphabet, bound):
            assert backtracking_match(r, w) == (w in expected)


def test_random_nested_stars():
    rng = random.Random(7)
    for _ in range(300):
        r = random_regex(rng, "ab", 3)
        for _ in range(rng.randint(1, 3)):
            r = ("star", ("alt", r, EPS)) if rng.random() < 0.5 else ("star", r)
        expected = language(r, 6)
        for w in words("ab", 6):
            assert backtracking_match(r, w) == (w in expected)
