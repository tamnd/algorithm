# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grep/. The authors are listed in prov/B1JFJE.jsonl.

import itertools
import random

from grep import NFA, grep, line_matches, thompson

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


def has_substring_in(line, lang):
    n = len(line)
    return any(line[i:j] in lang for i in range(n + 1) for j in range(i, n + 1))


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


def test_example_from_the_page():
    nfa = NFA()
    for _ in range(3):
        nfa.new_state()
    nfa.sym[0] = ("a", 1)
    nfa.eps[1] = []
    nfa.start, nfa.accept = 0, 2
    # On the page, state 1 has moves on b and on c. This NFA class allows one
    # symbol move per state, so state 1 reaches one state for each by epsilon-moves.
    b_state = nfa.new_state()
    c_state = nfa.new_state()
    nfa.eps[1] = [b_state, c_state]
    nfa.sym[b_state] = ("b", 1)
    nfa.sym[c_state] = ("c", 2)
    assert line_matches(nfa, "xabbcx")
    assert not line_matches(nfa, "abab")
    assert line_matches(nfa, "ac")
    lines = ["xabbcx", "abab", "ac"]
    assert grep(parse("ab*c"), lines) == ["xabbcx", "ac"]
    assert grep(parse("ab*c"), lines, invert=True) == ["abab"]


def test_no_exponential_case():
    r = parse("(a|a)*b")
    assert len(thompson(r).eps) == 12
    assert grep(r, ["a" * 20, "a" * 5000, "a" * 20 + "b"]) == ["a" * 20 + "b"]


def test_edge_cases():
    assert grep(EMPTY, ["", "a", "ab"]) == []
    assert grep(EPS, ["", "a", "ab"]) == ["", "a", "ab"]
    assert grep(parse("a*"), ["", "b", "c"]) == ["", "b", "c"]
    assert grep(("star", EMPTY), ["", "z"]) == ["", "z"]
    assert grep(parse("a"), ["", "b", "ba"]) == ["ba"]
    assert grep(parse("((a*)*b)*c"), ["xc", "abab", "aabbc"]) == ["xc", "aabbc"]
    assert grep(parse("ab"), []) == []
    deep = ("sym", "a")
    for _ in range(3000):
        deep = ("cat", EPS, ("star", deep)) if _ % 2 else ("alt", EMPTY, deep)
    assert grep(deep, ["", "b"]) == ["", "b"]


def test_random_against_brute_force():
    rng = random.Random(20261106)
    for trial in range(800):
        alphabet = "ab" if trial % 2 else "abc"
        bound = 6 if alphabet == "ab" else 4
        r = random_regex(rng, alphabet, rng.randint(0, 5))
        lang = language(r, bound)
        lines = list(words(alphabet, bound))
        expected = [x for x in lines if has_substring_in(x, lang)]
        assert grep(r, lines) == expected
        assert grep(r, lines, invert=True) == [x for x in lines if x not in set(expected)]
