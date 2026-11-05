# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glushkov-automaton/. The authors are listed in prov/0FZKDT.jsonl.

import itertools
import random

from glushkov_automaton import accepts, glushkov

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


def count_symbols(r):
    stack, k = [r], 0
    while stack:
        x = stack.pop()
        if x[0] == "sym":
            k += 1
        elif x[0] in ("alt", "cat", "star"):
            stack.extend(x[1:])
    return k


def is_deterministic(g):
    return all(len({g.symbol[q] for q in s}) == len(s) for s in g.succ)


def test_example_page():
    g = glushkov(parse("(a|b)*ab"))
    assert g.symbol == ["", "a", "b", "a", "b"]
    assert g.succ == [[1, 2, 3], [1, 2, 3], [1, 2, 3], [4], []]
    assert g.accepting == {4}
    assert len(g.transitions()) == 10
    current, seen = {0}, []
    for c in "abab":
        current = {q for p in current for q in g.succ[p] if g.symbol[q] == c}
        seen.append(sorted(current))
    assert seen == [[1, 3], [2, 4], [1, 3], [2, 4]]
    assert accepts(g, "abab")
    assert not accepts(g, "aba")


def test_example_determinism():
    g1 = glushkov(parse("(a|b)*a"))
    g2 = glushkov(parse("b*a(b*a)*"))
    assert not is_deterministic(g1)
    assert is_deterministic(g2)
    assert g2.succ == [[1, 2], [1, 2], [3, 4], [3, 4], [3, 4]]
    for w in words("ab", 8):
        assert accepts(g1, w) == accepts(g2, w) == w.endswith("a")


def test_example_star_normal_form():
    g = glushkov(parse("(a*b*)*"))
    assert g.succ == [[1, 2], [1, 2], [1, 2]]
    assert g.accepting == {0, 1, 2}
    h = glushkov(parse("(a|b)*"))
    assert g.transitions() == h.transitions()


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
        g = glushkov(parse(text))
        assert all(accepts(g, w) for w in yes)
        assert not any(accepts(g, w) for w in no)
    assert glushkov(parse("∅")).succ == [[]]
    assert glushkov(parse("ε")).accepting == {0}


def test_deep_expression_without_recursion():
    deep = ("sym", "a")
    for _ in range(5000):
        deep = ("cat", EPS, deep)
    g = glushkov(deep)
    assert len(g.symbol) == 2
    assert accepts(g, "a") and not accepts(g, "")
    long = ("star", ("alt", ("sym", "a"), ("sym", "b")))
    assert accepts(glushkov(long), "ab" * 20000)


def test_random_against_enumeration():
    rng = random.Random(20261106)
    for trial in range(900):
        alphabet = "ab" if trial % 2 else "abc"
        bound = 6 if alphabet == "ab" else 4
        r = random_regex(rng, alphabet, rng.randint(0, 5))
        g = glushkov(r)
        k = count_symbols(r)
        assert len(g.symbol) == len(g.succ) == k + 1
        assert len(g.transitions()) <= k * k + k
        assert all(0 not in s for s in g.succ)
        expected = language(r, bound)
        for w in words(alphabet, bound):
            assert accepts(g, w) == (w in expected)


def test_random_nested_stars():
    rng = random.Random(7)
    for _ in range(300):
        r = random_regex(rng, "ab", 3)
        for _ in range(rng.randint(1, 3)):
            r = ("star", ("alt", r, EPS)) if rng.random() < 0.5 else ("star", r)
        g = glushkov(r)
        expected = language(r, 6)
        for w in words("ab", 6):
            assert accepts(g, w) == (w in expected)
