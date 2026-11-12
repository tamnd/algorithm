# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/product-codes/. The authors are listed in prov/XYNQ39.jsonl.

import random
from itertools import combinations

from product_codes import (
    all_codewords, encode, encode_columns_first, even_weight, flatten, hamming74, is_codeword,
    messages, nearest_codeword, repetition, row_column_decode, unflatten,
)


def test_component_codes() -> None:
    h = hamming74()
    assert (h.n, h.k, h.d) == (7, 4, 3)
    assert (repetition(5).d, even_weight(3).d) == (5, 2)


def test_parameters_n1n2_k1k2_d1d2() -> None:
    cases = [(even_weight(3), even_weight(3)), (hamming74(), repetition(3)),
             (even_weight(4), hamming74()), (hamming74(), hamming74())]
    for c1, c2 in cases:
        words = all_codewords(c1, c2)
        assert len(set(words)) == 2 ** (c1.k * c2.k)
        assert min(w.bit_count() for w in words if w) == c1.d * c2.d
    # the [49, 16, 9] code: every array has all rows and columns in the Hamming code
    h = hamming74()
    rng = random.Random(1954)
    for w in rng.sample(all_codewords(h, h), 200):
        assert is_codeword(unflatten(w, 7, 7), h, h)


def test_checks_on_checks() -> None:
    # rows first then columns, or columns first then rows: the same array
    for c1, c2 in [(hamming74(), repetition(3)), (even_weight(3), hamming74())]:
        for msg in messages(c1.k, c2.k):
            a = encode(msg, c1, c2)
            assert a == encode_columns_first(msg, c1, c2)
            assert is_codeword(a, c1, c2)


def test_row_column_corrects_three_errors() -> None:
    # Hamming (x) Hamming: t1 = t2 = 1, so (t1 + 1)(t2 + 1) - 1 = 3 errors are always corrected
    h = hamming74()
    rng = random.Random(7)
    msg = [rng.randrange(16) for _ in range(4)]
    c = encode(msg, h, h)
    cw = flatten(c, 7)
    count = 0
    for w in range(4):
        for pos in combinations(range(49), w):
            e = sum(1 << p for p in pos)
            assert flatten(row_column_decode(unflatten(cw ^ e, 7, 7), h, h), 7) == cw
            count += 1
    assert count == 1 + 49 + 1176 + 18424


def test_row_column_fails_on_a_square_that_ml_corrects() -> None:
    h = hamming74()
    words = all_codewords(h, h)
    c = encode([0b1011, 0b0110, 0b1110, 0b0001], h, h)
    cw = flatten(c, 7)
    # 4 errors on a 2 x 2 square: rows 0, 1 and columns 0, 1
    e = (1 << 0) | (1 << 1) | (1 << 7) | (1 << 8)
    y = cw ^ e
    assert flatten(row_column_decode(unflatten(y, 7, 7), h, h), 7) != cw
    # 4 < 9 / 2, so the nearest codeword is the sent one
    assert nearest_codeword(y, words) == cw


def test_guarantee_with_unequal_components() -> None:
    # C1 = Hamming [7, 4, 3] (t1 = 1), C2 = repetition [5, 1, 5] (t2 = 2): (2)(3) - 1 = 5
    c1, c2 = hamming74(), repetition(5)
    rng = random.Random(1966)
    for _ in range(400):
        msg = [rng.randrange(2) for _ in range(4)]
        cw = flatten(encode(msg, c1, c2), 5)
        e = sum(1 << p for p in rng.sample(range(35), 5))
        assert flatten(row_column_decode(unflatten(cw ^ e, 7, 5), c1, c2), 5) == cw
