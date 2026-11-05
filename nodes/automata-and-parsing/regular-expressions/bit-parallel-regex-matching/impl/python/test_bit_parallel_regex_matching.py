# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-parallel-regex-matching/. The authors are listed in prov/045TZR.jsonl.

import itertools
import random

from bit_parallel_regex_matching import bit_parallel_match, bit_parallel_search, compile_matcher, run

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


def search_oracle(r, text, bound):
    lang = language(r, bound)
    return [e for e in range(len(text) + 1) if any(text[s:e] in lang for s in range(e + 1))]


def test_example_page():
    mt = compile_matcher(parse("(a|b)*ab"))
    assert mt.masks == {"a": 0b01010, "b": 0b10100}
    assert mt.final == 0b10000
    d, seen = 1, []
    for c in "abab":
        d = mt.step(d, c)
        seen.append(format(d, "05b"))
    assert seen == ["01010", "10100", "01010", "10100"]
    assert bit_parallel_match(parse("(a|b)*ab"), "abab")
    assert not bit_parallel_match(parse("(a|b)*ab"), "aba")


def test_example_search():
    assert bit_parallel_search(parse("ab*a"), "babbaa") == [5, 6]
    assert bit_parallel_search(parse("a*"), "ba") == [0, 1, 2]


def test_chunk_sizes_agree():
    rng = random.Random(3)
    for _ in range(200):
        r = random_regex(rng, "ab", 4)
        mts = [compile_matcher(r, b) for b in (1, 2, 3, 5, 8, 12)]
        for w in words("ab", 5):
            assert len({run(mt, w) for mt in mts}) == 1


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
        assert all(bit_parallel_match(r, w) for w in yes)
        assert not any(bit_parallel_match(r, w) for w in no)
    assert not bit_parallel_match(parse("ab"), "ac")
    assert bit_parallel_search(parse("∅"), "ab") == []
    assert bit_parallel_search(parse("ε"), "ab") == [0, 1, 2]


def test_many_positions_and_long_text():
    k = 300
    r = ("sym", "a")
    for i in range(1, k):
        r = ("cat", r, ("sym", "ab"[i % 2]))
    target = "".join("ab"[i % 2] for i in range(k))
    assert bit_parallel_match(r, target)
    assert not bit_parallel_match(r, target[:-1])
    assert bit_parallel_search(r, "b" + target + "a") == [k + 1]
    star = parse("(a|b)*a(a|b)(a|b)(a|b)")
    text = "ab" * 20000 + "abbb"
    assert bit_parallel_match(star, text)
    assert not bit_parallel_match(star, "ab" * 20000 + "bbbb")


def test_random_against_enumeration():
    rng = random.Random(20261106)
    for trial in range(900):
        alphabet = "ab" if trial % 2 else "abc"
        bound = 6 if alphabet == "ab" else 4
        r = random_regex(rng, alphabet, rng.randint(0, 5))
        mt = compile_matcher(r, rng.choice([1, 2, 3, 4, 8]))
        expected = language(r, bound)
        for w in words(alphabet, bound):
            assert run(mt, w) == (w in expected)


def test_random_search_against_enumeration():
    rng = random.Random(11)
    for trial in range(500):
        alphabet = "ab" if trial % 2 else "abc"
        r = random_regex(rng, alphabet, rng.randint(0, 4))
        text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
        assert bit_parallel_search(r, text, rng.choice([2, 8])) == search_oracle(r, text, len(text))


def test_random_nested_stars():
    rng = random.Random(7)
    for _ in range(300):
        r = random_regex(rng, "ab", 3)
        for _ in range(rng.randint(1, 3)):
            r = ("star", ("alt", r, EPS)) if rng.random() < 0.5 else ("star", r)
        mt = compile_matcher(r)
        expected = language(r, 6)
        for w in words("ab", 6):
            assert run(mt, w) == (w in expected)
