# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-solomon-code/. The authors are listed in prov/G5ZPZ8.jsonl.

import itertools
import random
from math import comb

from gf import GF2m
from reed_solomon_code import (T_AL, T_AL_INV, ccsds_encode, conventional_to_dual, dual_to_conventional,
                               encode_evaluation, encode_systematic, rs_generator, syndromes)

QR = GF2m(8, 0x11D)  # x^8 + x^4 + x^3 + x^2 + 1, ISO/IEC 18004
CCSDS = GF2m(8, 0x187)  # x^8 + x^7 + x^2 + x + 1, CCSDS 131.0-B-5, 4.3.3
F8 = GF2m(3, 0b1011)


def test_qr_generator_10() -> None:
    # Thonky QR code tutorial, "Error Correction Coding", generator for 10 EC codewords:
    # x^10 + a^251 x^9 + a^67 x^8 + a^46 x^7 + a^61 x^6 + a^118 x^5 + a^70 x^4 + a^64 x^3
    # + a^94 x^2 + a^32 x + a^45 (the same table as ISO/IEC 18004 Annex A)
    g = rs_generator(QR, 10, b=0)
    expect_high_to_low = [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]
    assert [QR.log[c] for c in reversed(g)] == expect_high_to_low


def test_qr_hello_world_1m() -> None:
    # Thonky QR code tutorial, "Error Correction Coding": HELLO WORLD, version 1-M.
    data = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    ec = [196, 35, 39, 119, 235, 215, 231, 226, 93, 23]
    c = encode_systematic(QR, list(reversed(data)), rs_generator(QR, 10, b=0))
    sent = list(reversed(c))  # highest power first
    assert sent == data + ec
    assert len(sent) == 26  # a version 1 symbol has 26 codewords


def test_ccsds_generator_annex_g() -> None:
    # CCSDS 131.0-B-5, Annex G, page G-1 (E = 16) and G-2 (E = 8): G_i as powers of alpha
    e16 = [0, 249, 59, 66, 4, 43, 126, 251, 97, 30, 3, 213, 50, 66, 170, 5, 24]
    e8 = [0, 30, 230, 49, 235, 129, 81, 76, 173]
    for e, half in ((16, e16), (8, e8)):
        g = rs_generator(CCSDS, 2 * e, 128 - e, 11)
        logs = [CCSDS.log[c] for c in g]
        assert logs == half + half[-2::-1]  # G_i = G_(2E - i), a self-reciprocal g
    # Annex G, the bit pattern of G_1 = alpha^249 in the conventional basis: 01011011
    assert CCSDS.alpha(249) == 0b01011011


def test_ccsds_dual_basis_annex_f() -> None:
    # Annex F, Example 1: z = 10111001 -> u = 00101010 = alpha^213
    assert dual_to_conventional(0b10111001) == 0b00101010 == CCSDS.alpha(213)
    # Annex F, Example 2: C' = 01011001 = alpha^152 -> C = 11101000
    assert conventional_to_dual(0b01011001) == 0b11101000
    assert CCSDS.alpha(152) == 0b01011001
    # Table F-1, a few rows (power, POLY IN ALPHA, dual basis l0..l7)
    rows = [(0, 0b00000001, 0b01111011), (1, 0b00000010, 0b10101111), (8, 0b10000111, 0b11000000),
            (46, 0b11110000, 0b00001000), (125, 0b11000101, 0b10000000), (254, 0b11000011, 0b10110110)]
    for p, u, z in rows:
        assert CCSDS.alpha(p) == u
        assert conventional_to_dual(u) == z
        assert dual_to_conventional(z) == u
    for u in range(256):
        assert dual_to_conventional(conventional_to_dual(u)) == u
    assert len(set(T_AL)) == 8 and len(set(T_AL_INV)) == 8


def test_ccsds_codeword_properties() -> None:
    rng = random.Random(255)
    for e in (16, 8):
        msg = [rng.randrange(256) for _ in range(255 - 2 * e)]
        sent = ccsds_encode(msg, e)
        assert len(sent) == 255 and sent[: 255 - 2 * e] == msg
        conv = [dual_to_conventional(z) for z in reversed(sent)]
        assert syndromes(CCSDS, conv, 2 * e, 128 - e, 11) == [0] * (2 * e)
    # shortened code: fewer message bytes, same check symbols
    msg = [rng.randrange(256) for _ in range(100)]
    sent = ccsds_encode(msg)
    assert len(sent) == 132
    assert sent[100:] == ccsds_encode([0] * 123 + msg)[223:]


def test_evaluation_view_equals_cyclic_view() -> None:
    # points alpha^0 .. alpha^(n-1) and deg f < k give the cyclic code with zeros alpha^1 .. alpha^(n-k)
    n, k = 7, 3
    points = [F8.alpha(i) for i in range(n)]
    g = rs_generator(F8, n - k, b=1)
    ev = {tuple(encode_evaluation(F8, list(m), points)) for m in itertools.product(range(8), repeat=k)}
    cy = {tuple(encode_systematic(F8, list(m), g)) for m in itertools.product(range(8), repeat=k)}
    assert ev == cy and len(ev) == 8 ** k


def test_mds_weight_distribution() -> None:
    # An MDS code has A_w = C(n, w) sum_{j=0}^{w-d} (-1)^j C(w, j) (q^(w-d+1-j) - 1)
    q = 8
    for n, k in ((7, 3), (7, 2), (7, 4), (6, 2)):
        d = n - k + 1
        # n = 6 is RS(7, 3) shortened by one: the top message symbol is 0 and is not sent
        g = rs_generator(F8, n - k)
        words = [encode_systematic(F8, list(m), g) for m in itertools.product(range(q), repeat=k)]
        assert all(len(w) == n for w in words)
        counts = [0] * (n + 1)
        for w in words:
            counts[sum(1 for s in w if s)] += 1
        for w in range(1, n + 1):
            want = 0 if w < d else comb(n, w) * sum((-1) ** j * comb(w, j) * (q ** (w - d + 1 - j) - 1)
                                                     for j in range(w - d + 1))
            assert counts[w] == want
        assert counts[d] == comb(n, d) * (q - 1)


def test_cyclic_shift() -> None:
    rng = random.Random(9)
    f16 = GF2m(4, 0b10011)
    g = rs_generator(f16, 4)
    for _ in range(100):
        c = encode_systematic(f16, [rng.randrange(16) for _ in range(11)], g)
        shifted = [c[-1]] + c[:-1]
        assert syndromes(f16, shifted, 4) == [0, 0, 0, 0]


def test_any_k_positions_determine_the_codeword() -> None:
    # MDS: the k x k submatrix of the evaluation map on any k points is invertible,
    # so two codewords that agree on k positions are equal.
    n, k = 7, 3
    points = [F8.alpha(i) for i in range(n)]
    seen = {}
    for m in itertools.product(range(8), repeat=k):
        c = encode_evaluation(F8, list(m), points)
        for pos in itertools.combinations(range(n), k):
            key = (pos, tuple(c[i] for i in pos))
            assert key not in seen
            seen[key] = m
