# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/macwilliams-identity/. The authors are listed in prov/1E7DCT.jsonl.

import random

from macwilliams_identity import (
    dual_code, hamming_code_weights, macwilliams_krawtchouk, macwilliams_transform,
    simplex_generator, span, weight_distribution,
)

GOLAY_G = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]  # x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1


def test_hamming_and_simplex() -> None:
    simplex = span(simplex_generator(3), 2)
    s = weight_distribution(simplex, 7)
    assert s == [1, 0, 0, 0, 7, 0, 0, 0]
    hamming = dual_code(simplex, 7, 2)
    h = weight_distribution(hamming, 7)
    assert h == [1, 0, 0, 7, 7, 0, 0, 1]
    assert macwilliams_transform(s, 2, 8) == h
    assert macwilliams_transform(h, 2, 16) == s
    assert macwilliams_krawtchouk(s, 2, 8) == h
    assert hamming_code_weights(7) == h


def test_long_hamming_codes_from_simplex() -> None:
    # The [31, 26] Hamming code has 2^26 words; its weights come from the 32 words of the dual.
    for r in (4, 5):
        n = 2 ** r - 1
        s = weight_distribution(span(simplex_generator(r), 2), n)
        assert s[0] == 1 and s[2 ** (r - 1)] == n
        assert macwilliams_transform(s, 2, 2 ** r) == hamming_code_weights(n)


def test_random_binary_codes() -> None:
    rng = random.Random(1963)
    for _ in range(40):
        n = rng.randint(3, 10)
        k = rng.randint(1, n - 1)
        gen = [tuple(rng.randrange(2) for _ in range(n)) for _ in range(k)]
        c = span(gen, 2)
        d = dual_code(c, n, 2)
        a, b = weight_distribution(c, n), weight_distribution(d, n)
        assert macwilliams_transform(a, 2, len(c)) == b
        assert macwilliams_transform(b, 2, len(d)) == a
        assert macwilliams_krawtchouk(a, 2, len(c)) == b


def test_random_ternary_and_quinary_codes() -> None:
    rng = random.Random(1977)
    for q, nmax in ((3, 6), (5, 4)):
        for _ in range(20):
            n = rng.randint(2, nmax)
            k = rng.randint(1, n - 1)
            gen = [tuple(rng.randrange(q) for _ in range(n)) for _ in range(k)]
            c = span(gen, q)
            d = dual_code(c, n, q)
            assert len(c) * len(d) == q ** n
            a, b = weight_distribution(c, n), weight_distribution(d, n)
            assert macwilliams_transform(a, q, len(c)) == b
            assert macwilliams_krawtchouk(a, q, len(c)) == b


def test_tetracode_is_formally_self_dual() -> None:
    c = span([(1, 0, 1, 1), (0, 1, 1, 2)], 3)
    a = weight_distribution(c, 4)
    assert a == [1, 0, 0, 8, 0]
    assert macwilliams_transform(a, 3, 9) == a


def test_extended_golay_code() -> None:
    gen = []
    for i in range(12):
        row = [0] * i + GOLAY_G + [0] * (11 - i)
        row.append(sum(row) % 2)  # overall parity bit
        gen.append(tuple(row))
    words = set()
    for m in range(2 ** 12):
        w = [0] * 24
        for i in range(12):
            if (m >> i) & 1:
                w = [x ^ y for x, y in zip(w, gen[i])]
        words.add(tuple(w))
    a = weight_distribution(list(words), 24)
    assert {i: v for i, v in enumerate(a) if v} == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    assert macwilliams_transform(a, 2, 4096) == a  # self-dual
