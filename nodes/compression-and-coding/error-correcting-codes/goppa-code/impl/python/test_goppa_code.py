# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goppa-code/. The authors are listed in prov/WVJW9K.jsonl.

import itertools
import random

import pytest

from gf import GF2m
from goppa_code import (binary_parity_check, decode, goppa_basis, is_codeword, parity_check,
                        patterson, syndrome)

F16 = GF2m(4, 0x13)  # x^4 + x + 1
F32 = GF2m(5, 0x25)  # x^5 + x^2 + 1

# Gamma(L, g) with L = GF(16) and g = x^2 + x + alpha^3, irreducible over GF(16)
SUP16 = [0] + [F16.alpha(i) for i in range(15)]
G16 = [F16.alpha(3), 1, 1]
# L = GF(32) and g = x^3 + alpha x + 1, a cubic with no root in GF(32), so irreducible
SUP32 = list(range(32))
G32 = [1, F32.alpha(1), 0, 1]


def bits(v: int, n: int) -> list[int]:
    return [(v >> j) & 1 for j in range(n)]


def span(basis: list[int]) -> list[int]:
    out = [0]
    for b in basis:
        out += [v ^ b for v in out]
    return out


def test_example_16_8_5() -> None:
    assert all(F16.peval(G16, a) for a in SUP16)
    basis = goppa_basis(F16, SUP16, G16)
    assert len(basis) == 8  # k = n - m t = 16 - 8
    words = span(basis)
    weights = sorted(bin(v).count("1") for v in words)
    assert weights[0] == 0 and weights[1] == 5  # d = 5 = 2t + 1
    for v in words:
        assert is_codeword(F16, SUP16, G16, bits(v, 16))


def test_parity_check_matches_syndrome() -> None:
    rng = random.Random(1970)
    rows = binary_parity_check(F16, SUP16, G16)
    h = parity_check(F16, SUP16, G16)
    assert len(h) == 2 and len(rows) == 8
    for _ in range(600):
        v = rng.getrandbits(16)
        by_matrix = all(bin(r & v).count("1") % 2 == 0 for r in rows)
        assert by_matrix == is_codeword(F16, SUP16, G16, bits(v, 16))


def test_patterson_exhaustive_t2() -> None:
    rng = random.Random(4)
    words = span(goppa_basis(F16, SUP16, G16))
    for v in [0] + rng.sample(words, 3):
        c = bits(v, 16)
        for w in range(3):
            for pos in itertools.combinations(range(16), w):
                y = list(c)
                for i in pos:
                    y[i] ^= 1
                assert patterson(F16, SUP16, G16, y) == list(pos)
                assert decode(F16, SUP16, G16, y) == c


def test_patterson_exhaustive_t3() -> None:
    basis = goppa_basis(F32, SUP32, G32)
    assert len(basis) == 32 - 5 * 3
    rng = random.Random(1975)
    v = 0
    for b in basis:
        if rng.random() < 0.5:
            v ^= b
    c = bits(v, 32)
    assert is_codeword(F32, SUP32, G32, c)
    for w in range(4):
        for pos in itertools.combinations(range(32), w):
            y = list(c)
            for i in pos:
                y[i] ^= 1
            assert patterson(F32, SUP32, G32, y) == list(pos)


def test_against_syndrome_table() -> None:
    # brute force: all errors of weight <= t have distinct syndromes (so d >= 2t + 1),
    # and Patterson decodes a word exactly when its syndrome is in the table
    table = {}
    for w in range(4):
        for pos in itertools.combinations(range(32), w):
            e = [0] * 32
            for i in pos:
                e[i] = 1
            key = tuple(syndrome(F32, SUP32, G32, e))
            assert key not in table
            table[key] = list(pos)
    rng = random.Random(203)
    words = goppa_basis(F32, SUP32, G32)
    hits = 0
    for _ in range(600):
        v = 0
        for b in words:
            if rng.random() < 0.5:
                v ^= b
        y = bits(v, 32)
        for i in rng.sample(range(32), rng.randrange(0, 6)):
            y[i] ^= 1
        expected = table.get(tuple(syndrome(F32, SUP32, G32, y)))
        out = decode(F32, SUP32, G32, y)
        if expected is None:
            assert out is None
        else:
            hits += 1
            fixed = list(y)
            for i in expected:
                fixed[i] ^= 1
            assert out == fixed
    assert 200 < hits < 600


def test_bch_is_a_goppa_code() -> None:
    # L = (alpha^0, alpha^-1, ..., alpha^-14), g = x^4: the narrow sense BCH [15, 7, 5] code
    sup = [F16.alpha(-i) for i in range(15)]
    basis = goppa_basis(F16, sup, [0, 0, 0, 0, 1])
    assert len(basis) == 7
    bch_g = 0b111010001  # x^8 + x^7 + x^6 + x^4 + 1
    goppa_words = set(span(basis))
    for i in range(7):
        assert (bch_g << i) in goppa_words
    # and in general Gamma(L, x^r) is {c : c(alpha^j) = 0 for j = 1 .. r}
    rng = random.Random(15)
    for r in (2, 4, 6):
        b = goppa_basis(F16, sup, [0] * r + [1])
        for v in span(b)[:64] + [rng.getrandbits(15) for _ in range(100)]:
            c = bits(v, 15)
            by_roots = all(F16.peval(c, F16.alpha(j)) == 0 for j in range(1, r + 1))
            assert by_roots == is_codeword(F16, sup, [0] * r + [1], c)


def test_squarefree_g_and_its_square_give_the_same_binary_code() -> None:
    g2 = F16.pmul(G16, G16)
    a = set(span(goppa_basis(F16, SUP16, G16)))
    b = set(span(goppa_basis(F16, SUP16, g2)))
    assert a == b


def test_invalid_parameters() -> None:
    with pytest.raises(ValueError):
        parity_check(F16, SUP16, [0, 1])  # g = x has the root 0 in L
    with pytest.raises(ValueError):
        parity_check(F16, [1, 1, 2], G16)
