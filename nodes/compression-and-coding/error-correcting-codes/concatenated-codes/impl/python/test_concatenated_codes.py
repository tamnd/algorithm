# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concatenated-codes/. The authors are listed in prov/5CDZ50.jsonl.

import itertools
import random

from concatenated_codes import (HAMMING, Concatenated, justesen, mul, rs_decode, rs_encode,
                                rs_points)


def weight(x: int) -> int:
    return bin(x).count("1")


def test_parts():
    assert sorted(weight(c) for c in HAMMING) == [0] + [3] * 7 + [4] * 7 + [7]
    assert len(set(rs_points(15))) == 15 and 0 not in rs_points(15)
    rng = random.Random(1)
    for n, k in ((6, 3), (15, 7)):
        for _ in range(50):  # errors and erasures: any 2e + s < n - k + 1
            msg = [rng.randrange(16) for _ in range(k)]
            word = rs_encode(msg, n)
            s = rng.randrange(n - k + 1)
            e = (n - k - s) // 2
            pos = rng.sample(range(n), s + e)
            bad = list(word)
            for i in pos[:s]:
                bad[i] = None
            for i in pos[s:]:
                bad[i] ^= rng.randrange(1, 16)
            assert rs_decode(bad, k) == msg


def test_distance_at_least_product_by_enumeration():
    # outer RS [n, k, n - k + 1] over GF(16), inner Hamming [7, 4, 3]
    for n, k, exact in ((5, 2, 12), (6, 3, 12), (7, 3, 15)):
        d = Concatenated(n, k).min_distance()
        assert d >= (n - k + 1) * 3
        assert d == exact  # here the product bound is met with equality


def test_two_stage_decoder_radius():
    code = Concatenated(6, 3)  # D = 4, d = 3: two stages fix every pattern of <= 3 errors
    rng = random.Random(2)
    msg = [rng.randrange(16) for _ in range(3)]
    x = code.encode(msg)
    for w in (1, 2, 3):
        for pos in itertools.combinations(range(42), w):
            e = sum(1 << p for p in pos)
            assert code.decode_two_stage(x ^ e) == msg
    # 2 + 2 errors in two blocks: both inner decisions are wrong and the outer code fails
    e = 0b11 | 0b11 << 7
    assert code.decode_two_stage(x ^ e) != msg
    assert code.decode_gmd(x ^ e) == msg


def test_gmd_corrects_below_half_the_product():
    code = Concatenated(6, 3)  # D d / 2 = 6: GMD fixes every pattern of <= 5 errors
    rng = random.Random(3)
    shapes = [(5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1),
              (4,), (2, 2), (3, 1), (2, 1, 1)]
    for t in range(1500):
        msg = [rng.randrange(16) for _ in range(3)]
        x = code.encode(msg)
        shape = shapes[t % len(shapes)]
        e = 0
        for blk, cnt in zip(rng.sample(range(6), len(shape)), shape):
            for b in rng.sample(range(7), cnt):
                e |= 1 << (7 * blk + b)
        assert code.decode_gmd(x ^ e) == msg
    # with 6 errors the guarantee ends: 0b0000111 is a Hamming codeword, so two such
    # error blocks give two wrong inner symbols that look fully reliable
    x = code.encode([0, 0, 0])
    assert code.decode_gmd(x ^ (0b111 << 28 | 0b111 << 35)) != [0, 0, 0]


def test_justesen_inner_codes_and_distance():
    pts = rs_points(15)
    # Wozencraft ensemble: each (u, v) with u, v nonzero lies in exactly one inner code
    for u in range(1, 16):
        for v in range(1, 16):
            assert sum(mul(a, u) == v for a in pts) == 1
    words = sorted(weight(u | mul(a, u) << 4) for a in pts for u in range(1, 16))
    for k, exact in ((2, 47), (3, 41)):
        dist = justesen(k).min_distance()
        # n - k + 1 nonzero outer symbols give distinct inner words, so d >= that many lightest
        assert dist >= sum(words[:15 - k + 1])
        assert dist == exact
        rng = random.Random(k)
        msg = [rng.randrange(16) for _ in range(k)]
        assert justesen(k).decode_gmd(justesen(k).encode(msg) ^ 0b1011) == msg
