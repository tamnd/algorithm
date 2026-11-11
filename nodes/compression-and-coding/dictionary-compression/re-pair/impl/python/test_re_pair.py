# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/re-pair/. The authors are listed in prov/GPGX6R.jsonl.

import itertools
import random

from re_pair import expand, grammar_size, re_pair


def naive_re_pair(text, first=256):
    """Quadratic oracle: recount all pairs by a full scan before each replacement."""
    seq = list(text)
    rules = []
    new = first
    while True:
        counts = {}
        last = {}
        for i in range(len(seq) - 1):
            pair = (seq[i], seq[i + 1])
            if pair[0] == pair[1] and last.get(pair) == i - 1:
                continue  # overlaps the previous occurrence inside a run
            last[pair] = i
            counts[pair] = counts.get(pair, 0) + 1
        best = None
        for pair, c in counts.items():
            if c >= 2 and (best is None or (-c, pair) < (-best[1], best[0])):
                best = (pair, c)
        if best is None:
            return rules, seq
        x, y = best[0]
        out, i = [], 0
        while i < len(seq):
            if i + 1 < len(seq) and seq[i] == x and seq[i + 1] == y:
                out.append(new)
                i += 2
            else:
                out.append(seq[i])
                i += 1
        seq = out
        rules.append((new, x, y))
        new += 1


def _parse_cost(w, phrases):
    d = [0] * (len(w) + 1)
    for i in range(1, len(w) + 1):
        d[i] = d[i - 1] + 1
        for j in range(i - 1):
            if w[j:i] in phrases and d[j] + 1 < d[i]:
                d[i] = d[j] + 1
    return d[len(w)]


def smallest_grammar_size(w):
    """Brute force: try each set of repeated substrings as the expansions of the rules."""
    w = tuple(w)
    n = len(w)
    if n == 0:
        return 0
    cands = sorted({w[i:j] for i in range(n) for j in range(i + 2, n + 1)
                    if sum(w[k:k + j - i] == w[i:j] for k in range(n)) >= 2})
    best = n
    for mask in range(1, 1 << len(cands)):
        d = {cands[t] for t in range(len(cands)) if mask >> t & 1}
        c = _parse_cost(w, d) + sum(_parse_cost(p, d - {p}) for p in d)
        best = min(best, c)
    return best


def lz77_phrases(w):
    """Greedy LZ77 without self-reference: each phrase is one symbol or a copy of earlier text."""
    w = tuple(w)
    i = z = 0
    while i < len(w):
        longest = 0
        for j in range(i):
            k = 0
            while i + k < len(w) and j + k < i and w[j + k] == w[i + k]:
                k += 1
            longest = max(longest, k)
        i += max(longest, 1)
        z += 1
    return z


def fibonacci_word(n):
    a, b = [0], [0, 1]
    while len(b) < n:
        a, b = b, b + a
    return b[:n]


def test_worked_example() -> None:
    w = [ord(c) for c in "xabcabcyabcabc"]
    rules, seq = re_pair(w)
    a, b, c, x, y = map(ord, "abcxy")
    assert rules == [(256, a, b), (257, 256, c), (258, 257, 257)]
    assert seq == [x, 258, y, 258]
    assert grammar_size(rules, seq) == 10
    assert expand(rules, seq) == w


def test_edges() -> None:
    assert re_pair([]) == ([], [])
    assert re_pair([7]) == ([], [7])
    assert re_pair([1, 2]) == ([], [1, 2])
    assert re_pair([5, 5, 5]) == ([], [5, 5, 5])  # one non-overlapping aa only
    assert re_pair([5, 5, 5, 5]) == ([(256, 5, 5)], [256, 256])
    rules, seq = re_pair([0] * 7, 1)
    assert rules == [(1, 0, 0)] and seq == [1, 1, 1, 0]
    rules, seq = re_pair([0] * 1024, 1)
    assert len(rules) == 9 and seq == [9, 9]  # the last pair occurs only once
    assert expand(*re_pair([3] * 1000)) == [3] * 1000


def test_long_runs_and_fibonacci() -> None:
    w = [0] * 50 + [1] * 37 + [0] * 50 + [1] * 37
    assert expand(*re_pair(w, 2)) == w
    f = fibonacci_word(1597)
    rules, seq = re_pair(f, 2)
    assert expand(rules, seq) == f
    assert len(rules) == 13 and len(seq) == 3


def test_random_against_naive() -> None:
    rng = random.Random(4417)
    for _ in range(1500):
        n = rng.randrange(0, 40)
        k = rng.choice([1, 2, 2, 3, 4])
        w = [rng.randrange(k) for _ in range(n)]
        if rng.random() < 0.3:
            w = [s for s in w for _ in range(rng.randrange(1, 5))]
        got = re_pair(w, 10)
        assert got == naive_re_pair(w, 10)
        assert expand(*got) == w


def test_larger_random_round_trip() -> None:
    rng = random.Random(90)
    for _ in range(10):
        n = rng.randrange(1000, 5000)
        base = [rng.randrange(3) for _ in range(rng.randrange(1, 30))]
        w = [s if rng.random() < 0.97 else rng.randrange(256) for s in (base * (n // len(base) + 1))[:n]]
        assert expand(*re_pair(w)) == w


def test_size_bounds_on_tiny_strings() -> None:
    # z <= g* <= size of the Re-Pair grammar, for all binary strings up to length 7
    for n in range(8):
        for w in itertools.product((0, 1), repeat=n):
            g = smallest_grammar_size(w)
            assert lz77_phrases(w) <= g <= grammar_size(*re_pair(w, 2))
