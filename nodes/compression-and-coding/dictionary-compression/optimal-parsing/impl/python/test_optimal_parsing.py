# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-parsing/. The authors are listed in prov/2HK8NC.jsonl.

import random

from optimal_parsing import INF, flexible_parse, greedy_parse, optimal_parse


def brute_min(t, words, cost=lambda w: 1):
    """Minimum cost over all parses, enumerated with an explicit stack."""
    words = set(words)
    longest = max((len(w) for w in words), default=0)
    best = INF
    stack = [(0, 0)]
    while stack:
        i, c = stack.pop()
        if i == len(t):
            best = min(best, c)
            continue
        for k in range(1, min(longest, len(t) - i) + 1):
            w = t[i:i + k]
            if w in words:
                stack.append((i + k, c + cost(w)))
    return best


def random_dictionary(rng, alphabet, prefix_closed: bool):
    words = {bytes([c]) for c in alphabet}
    for _ in range(rng.randrange(1, 8)):
        w = bytes(rng.choice(alphabet) for _ in range(rng.randrange(2, 6)))
        if prefix_closed:
            words.update(w[:k] for k in range(1, len(w) + 1))
        else:
            words.add(w)
    return words


def test_page_examples() -> None:
    d = {b"a", b"b", b"c", b"d", b"ab", b"bc", b"bcd"}
    assert greedy_parse(b"abcd", d) == [b"ab", b"c", b"d"]
    assert flexible_parse(b"abcd", d) == [b"a", b"bcd"]
    assert optimal_parse(b"abcd", d) == (2, [b"a", b"bcd"])

    costs = {b"a": 2, b"b": 2, b"ab": 5}
    assert greedy_parse(b"ab", costs) == [b"ab"]
    assert flexible_parse(b"ab", costs) == [b"ab"]
    assert optimal_parse(b"ab", costs, costs.get) == (4, [b"a", b"b"])

    d = {b"a", b"b", b"ab", b"ba", b"bab"}
    assert optimal_parse(b"abab", d) == (2, [b"a", b"bab"])
    assert greedy_parse(b"abab", d) == [b"ab", b"ab"]


def test_edges() -> None:
    d = {b"a", b"aa", b"aaa"}
    assert optimal_parse(b"", d) == (0, [])
    assert optimal_parse(b"a", d) == (1, [b"a"])
    assert optimal_parse(b"a" * 10, d)[0] == 4
    assert optimal_parse(b"a" * 3000, d)[0] == 1000
    assert optimal_parse(b"ab", d) == (INF, [])
    assert greedy_parse(b"ab", d) is None
    assert flexible_parse(b"aaaa", {b"aaa", b"aa"}) == [b"aa", b"aa"]
    assert greedy_parse(b"aaaa", {b"aaa", b"aa"}) is None


def test_dp_equals_brute_force() -> None:
    rng = random.Random(1974)
    for _ in range(400):
        alphabet = b"ab" if rng.random() < 0.5 else b"abc"
        words = random_dictionary(rng, alphabet, prefix_closed=False)
        if rng.random() < 0.3:  # a dictionary without some single symbols
            words.discard(alphabet[:1])
        costs = {w: rng.randrange(1, 20) for w in words}
        t = bytes(rng.choice(alphabet) for _ in range(rng.randrange(13)))
        c, phrases = optimal_parse(t, words, costs.get)
        assert c == brute_min(t, words, costs.get)
        if c < INF:
            assert b"".join(phrases) == t and sum(costs[w] for w in phrases) == c
        g = greedy_parse(t, words)
        if g is not None:
            assert sum(costs[w] for w in g) >= c


def test_flexible_parsing_is_optimal_for_prefix_closed() -> None:
    rng = random.Random(1999)
    for _ in range(400):
        alphabet = b"ab" if rng.random() < 0.5 else b"abc"
        words = random_dictionary(rng, alphabet, prefix_closed=True)
        t = bytes(rng.choice(alphabet) for _ in range(rng.randrange(40)))
        fp = flexible_parse(t, words)
        assert b"".join(fp) == t and all(w in words for w in fp)
        assert len(fp) == optimal_parse(t, words)[0]
        assert len(greedy_parse(t, words)) >= len(fp)


def test_flexible_parsing_can_fail_without_prefix_closure() -> None:
    rng = random.Random(6)
    worse = 0
    for _ in range(400):
        words = random_dictionary(rng, b"ab", prefix_closed=False)
        t = bytes(rng.choice(b"ab") for _ in range(rng.randrange(20)))
        fp = flexible_parse(t, words)
        worse += len(fp) > optimal_parse(t, words)[0]
    assert worse > 0
