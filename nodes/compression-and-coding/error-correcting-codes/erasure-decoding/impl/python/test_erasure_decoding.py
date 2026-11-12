# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/erasure-decoding/. The authors are listed in prov/GWSB3B.jsonl.

import itertools
import random

from erasure_decoding import (correctable, decode, encode, null_space, reed_solomon_generator,
                              solve_mod_p)

# Hamming [7, 4, 3]: column j of H is the binary form of j + 1, least significant bit on top.
H7 = [[((j + 1) >> r) & 1 for j in range(7)] for r in range(3)]


def codewords(h, n, p):
    return [c for c in itertools.product(range(p), repeat=n)
            if all(sum(a * b for a, b in zip(row, c)) % p == 0 for row in h)]


def brute(book, y):
    fits = [c for c in book if all(v is None or v == cv for v, cv in zip(y, c))]
    return list(fits[0]) if len(fits) == 1 else None


def test_hamming_every_erasure_pattern():
    book = codewords(H7, 7, 2)
    assert len(book) == 16
    good = {e: 0 for e in range(8)}
    for c in book:
        for mask in range(128):
            er = [j for j in range(7) if mask >> j & 1]
            y = [None if j in er else c[j] for j in range(7)]
            got = decode(H7, y, 2)
            assert got == brute(book, y)
            assert (got is not None) == correctable(H7, er, 2)
            if c == book[0] and got is not None:
                good[len(er)] += 1
    assert [good[e] for e in range(8)] == [1, 7, 21, 28, 0, 0, 0, 0]


def test_worked_example():
    y = [None, 1, 1, None, 0, None, 0]
    assert decode(H7, y, 2) == [1, 1, 1, 0, 0, 0, 0]
    assert decode(H7, [None, None, None, 0, 0, 0, 0], 2) is None


def test_reed_solomon_any_k_positions():
    p, n, k = 13, 8, 4
    g = reed_solomon_generator(n, k, p)
    h = null_space(g, p)
    assert len(h) == n - k
    rng = random.Random(1)
    m = [rng.randrange(p) for _ in range(k)]
    c = encode(m, g, p)
    for er in itertools.combinations(range(n), n - k):
        y = [None if j in er else c[j] for j in range(n)]
        assert decode(h, y, p) == c
    for er in itertools.combinations(range(n), n - k + 1):
        assert not correctable(h, er, p)


def test_random_codes_match_brute_force():
    rng = random.Random(2)
    for p, n, k in ((2, 6, 3), (3, 5, 2), (5, 4, 2)):
        for _ in range(4):
            g = [[rng.randrange(p) for _ in range(n)] for _ in range(k)]
            h = null_space(g, p)
            book = codewords(h, n, p)
            for _ in range(60):
                c = list(rng.choice(book))
                y = [None if rng.random() < 0.5 else v for v in c]
                er = [j for j, v in enumerate(y) if v is None]
                got = decode(h, y, p)
                assert got == brute(book, y)
                assert (got is not None) == correctable(h, er, p)


def test_random_binary_full_rank_probability():
    # Probability that a random r x e binary matrix has rank e is prod (1 - 2^(i - r)).
    rng = random.Random(3)
    r, e, trials = 10, 8, 4000
    exact = 1.0
    for i in range(e):
        exact *= 1 - 2.0 ** (i - r)
    hits = 0
    for _ in range(trials):
        a = [[rng.randrange(2) for _ in range(e)] for _ in range(r)]
        hits += solve_mod_p(a, [0] * r, 2)[1] == e
    assert abs(hits / trials - exact) < 0.03
    assert exact >= 1 - 2.0 ** (e - r)
