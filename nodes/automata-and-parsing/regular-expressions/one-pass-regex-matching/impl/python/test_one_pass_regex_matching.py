# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-pass-regex-matching/. The authors are listed in prov/KX64F8.jsonl.

import itertools
import random

from one_pass_regex_matching import (
    NotOnePass,
    compile_one_pass,
    is_one_pass,
    one_pass_match,
    run_one_pass,
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


def mark(r):
    """Replace the i-th symbol occurrence (from the left) by the letter chr(0x100 + i)."""
    count = [0]
    letters = {}

    def go(x):
        if x[0] == "sym":
            count[0] += 1
            c = chr(0x100 + count[0])
            letters[c] = x[1]
            return ("sym", c)
        if x[0] in ("alt", "cat"):
            return (x[0], go(x[1]), go(x[2]))
        if x[0] == "star":
            return ("star", go(x[1]))
        return x

    return go(r), letters


def positions(r):
    n, stack = 0, [r]
    while stack:
        x = stack.pop()
        if x[0] == "sym":
            n += 1
        elif x[0] in ("alt", "cat", "star"):
            stack.extend(x[1:])
    return n


def brute_one_unambiguous(r, bound):
    """The Brüggemann-Klein and Wood definition, on marked words of length at most bound."""
    marked, letters = mark(r)
    seen = {}
    for x in language(marked, bound):
        for i in range(len(x)):
            key = (x[:i], letters[x[i]])
            if seen.setdefault(key, x[i]) != x[i]:
                return False
    return True


def path_letters(path):
    return "".join(chr(0x100 + p) for p in path)


def check_against_oracle(r, alphabet, bound):
    table = compile_one_pass(r)
    lang = language(r, bound)
    marked, letters = mark(r)
    parses = {}
    for x in language(marked, bound):
        parses.setdefault("".join(letters[c] for c in x), []).append(x)
    for w in words(alphabet, bound):
        path = run_one_pass(table, w)
        assert (path is not None) == (w in lang), (r, w)
        if path is not None:
            assert parses[w] == [path_letters(path)], (r, w, path)


def test_example_cox_pattern():
    r = parse("a*ba*")
    table = compile_one_pass(r)
    assert table.next[0] == {"a": 1, "b": 2}
    assert table.next[1] == {"a": 1, "b": 2}
    assert table.next[2] == {"a": 3}
    assert table.next[3] == {"a": 3}
    assert table.final == frozenset({2, 3})
    assert run_one_pass(table, "aaba") == [1, 1, 2, 3]
    assert run_one_pass(table, "b") == [2]
    assert run_one_pass(table, "aab") == [1, 1, 2]
    assert run_one_pass(table, "abab") is None
    assert run_one_pass(table, "aa") is None


def test_one_pass_and_not():
    yes = ["a*ba*", "a(b|c)", "aa*", "(a*)*", "(a*b*)*", "((a|ε)*)*", "(ab)*b", "a*(b|ε)"]
    no = ["a*a", "ab|ac", "(a|b)*ab", "(a|a)", "a*(a|ε)", "(a|ε)a", "(ab|a)*b", "(ab)*a"]
    for t in yes:
        assert is_one_pass(parse(t)), t
    for t in no:
        assert not is_one_pass(parse(t)), t
        try:
            one_pass_match(parse(t), "a")
        except NotOnePass:
            pass
        else:
            raise AssertionError(t)


def test_edge_cases():
    assert not one_pass_match(EMPTY, "")
    assert not one_pass_match(EMPTY, "a")
    assert one_pass_match(EPS, "")
    assert not one_pass_match(EPS, "a")
    assert one_pass_match(parse("a"), "a")
    assert not one_pass_match(parse("a"), "")
    assert not one_pass_match(parse("∅*a"), "")
    assert one_pass_match(parse("∅*"), "")
    # The dead position 1 is ignored, so the expression is one-pass.
    t = compile_one_pass(parse("a∅|a"))
    assert run_one_pass(t, "a") == [2]
    assert is_one_pass(parse("b|∅a(b|b)"))
    assert is_one_pass(parse("a(b|b)∅|c"))
    assert not is_one_pass(parse("a(b|b)|c"))


def test_deep_inputs():
    n = 4000
    r = ("sym", "a")
    for _ in range(n - 1):
        r = ("cat", r, ("sym", "a"))
    assert one_pass_match(r, "a" * n)
    assert not one_pass_match(r, "a" * (n - 1))
    s = ("sym", "b")
    for _ in range(2000):
        s = ("star", s)
    assert one_pass_match(s, "b" * 5000)
    assert one_pass_match(s, "")
    assert not one_pass_match(s, "ba")


def test_random_against_oracle():
    rng = random.Random(20261106)
    checked = exact = 0
    for i in range(3000):
        alphabet = "ab" if i % 2 == 0 else "abc"
        r = random_regex(rng, alphabet, 4)
        k = positions(r)
        if k > 7:
            continue
        ok = is_one_pass(r)
        if k <= 3:
            assert ok == brute_one_unambiguous(r, 2 * k), r
            exact += 1
        elif not brute_one_unambiguous(r, 5):
            assert not ok, r
        if ok:
            check_against_oracle(r, alphabet, 6 if alphabet == "ab" else 4)
            checked += 1
    assert exact >= 500
    assert checked >= 500


def test_nested_stars_and_empty_word():
    for t in ["(a*)*", "((a*)*b)*", "(a*b*)*", "(ε|a)*", "(∅|a*)*b"]:
        r = parse(t)
        assert is_one_pass(r), t
        check_against_oracle(r, "ab", 7)
