# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/majority-logic-decoding/. The authors are listed in prov/PD1H78.jsonl.

import random
from itertools import combinations
from math import comb

from majority_logic_decoding import (
    cyclic_generator_rows, dual_words, monomials_of_degree, one_step_decode, orthogonal_checks,
    reed_decode, rm_encode, span,
)


def random_poly(r: int, m: int, rng: random.Random) -> set:
    return {s for l in range(r + 1) for s in monomials_of_degree(l, m) if rng.random() < 0.5}


def test_reed_decoder_without_errors() -> None:
    rng = random.Random(1954)
    for m in range(1, 7):
        for r in range(m + 1):
            for _ in range(5):
                f = random_poly(r, m, rng)
                assert reed_decode(rm_encode(f, m), r, m) == f


def test_reed_decoder_exhaustive() -> None:
    # every error pattern of weight up to t = 2^(m - r - 1) - 1, on a random codeword
    rng = random.Random(1963)
    cases = [(0, 2), (0, 3), (1, 3), (0, 4), (1, 4), (2, 4), (2, 5), (3, 5), (4, 6)]
    for r, m in cases:
        n = 1 << m
        t = (1 << (m - r - 1)) - 1
        f = random_poly(r, m, rng)
        c = rm_encode(f, m)
        count = 0
        for w in range(t + 1):
            for pos in combinations(range(n), w):
                y = list(c)
                for p in pos:
                    y[p] ^= 1
                assert reed_decode(y, r, m) == f
                count += 1
        assert count == sum(comb(n, w) for w in range(t + 1))


def test_reed_decoder_random_errors_longer_codes() -> None:
    rng = random.Random(2017)
    for r, m in [(1, 5), (1, 6), (2, 6), (1, 7), (2, 7), (3, 7)]:
        n = 1 << m
        t = (1 << (m - r - 1)) - 1
        for _ in range(20):
            f = random_poly(r, m, rng)
            y = rm_encode(f, m)
            for p in rng.sample(range(n), t):
                y[p] ^= 1
            assert reed_decode(y, r, m) == f


def test_radius_is_tight() -> None:
    # y = half of the support of the minimum weight word x_0 x_1 ... x_(r-1) is at distance
    # 2^(m - r - 1) from both that word and from 0. The decoder returns one of them, so one of
    # the two error patterns of weight t + 1 is not corrected.
    for r, m in [(1, 3), (1, 4), (2, 5), (1, 6)]:
        n = 1 << m
        t1 = 1 << (m - r - 1)
        mono = tuple(range(r))
        c = rm_encode({mono}, m)
        support = [p for p, v in enumerate(c) if v]
        y = [0] * n
        for p in support[:t1]:
            y[p] = 1
        assert sum(y) == t1 and sum(a != b for a, b in zip(y, c)) == t1
        assert reed_decode(y, r, m) in (set(), {mono})


def test_one_step_bch_15_7() -> None:
    n = 15
    g = 0b111010001  # g(x) = 1 + x^4 + x^6 + x^7 + x^8, the (15, 7, 5) BCH code
    rows = cyclic_generator_rows(g, n)
    code = span(rows)
    assert len(set(code)) == 128
    assert min(c.bit_count() for c in code if c) == 5
    checks = orthogonal_checks(dual_words(rows, n), n - 1, 4)
    assert checks is not None and len(checks) == 4
    rng = random.Random(1963)
    for c in rng.sample(code, 4):
        for w in range(3):  # J = 4 orthogonal checks correct floor(J / 2) = 2 errors
            for pos in combinations(range(n), w):
                e = sum(1 << p for p in pos)
                assert one_step_decode(c ^ e, checks, n) == c


def test_one_step_hamming_dual() -> None:
    # A cyclic [7, 3, 4] simplex code. Its dual, a Hamming code, gives J = 3 checks
    # orthogonal on a position, so one-step decoding corrects floor(3 / 2) = 1 error.
    n = 7
    g = 0b10111  # 1 + x + x^2 + x^4 generates the [7, 3, 4] code
    rows = cyclic_generator_rows(g, n)
    code = span(rows)
    assert min(c.bit_count() for c in code if c) == 4
    checks = orthogonal_checks(dual_words(rows, n), n - 1, 3)
    assert checks is not None
    for c in code:
        for p in range(n):
            assert one_step_decode(c ^ (1 << p), checks, n) == c
