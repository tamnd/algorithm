# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raptor-codes/. The authors are listed in prov/GTWFNH.jsonl.

import math
import random
from fractions import Fraction

from raptor_codes import (DEG_D, DEG_F, RaptorCode, degree, gray_of_weight, intermediate_symbols,
                          is_prime, lt_neighbors, popcount, precode_rows, rfc5053_params,
                          success_rate)


def test_params_by_hand_and_by_definition():
    # worked by hand from RFC 5053 Section 5.4.2.3
    assert rfc5053_params(4) == (4, 5, 5, 14)
    assert rfc5053_params(1000) == (46, 59, 13, 1072)
    assert rfc5053_params(8192) == (129, 211, 16, 8419)
    for k in range(4, 400):
        x, s, h, l = rfc5053_params(k)
        assert x * (x - 1) >= 2 * k and (x - 1) * (x - 2) < 2 * k
        lo = math.ceil(0.01 * k) + x
        assert s >= lo and is_prime(s) and not any(is_prime(t) for t in range(lo, s))
        assert math.comb(h, math.ceil(h / 2)) >= k + s
        assert math.comb(h - 1, math.ceil((h - 1) / 2)) < k + s
        assert l == k + s + h


def test_precode_structure():
    assert precode_rows(4)[:5] == [0b11001, 0b100011, 0b1000111, 0b10001110, 0b100001100]
    assert gray_of_weight(3, 9) == [7, 13, 14, 11, 25, 26, 28, 21, 22]
    for k in (4, 37, 150):
        _, s, h, l = rfc5053_params(k)
        rows = precode_rows(k)
        assert len(rows) == s + h
        for i in range(k):  # each source symbol enters exactly 3 LDPC symbols
            assert sum(rows[b] >> i & 1 for b in range(s)) == 3
        for j in range(k + s):  # each column of the Half part has weight ceil(H/2)
            assert sum(rows[s + t] >> j & 1 for t in range(h)) == math.ceil(h / 2)
        rng = random.Random(k)
        c = intermediate_symbols([rng.getrandbits(32) for _ in range(k)])
        for row in rows:  # the intermediate symbols satisfy every constraint
            acc = 0
            for i in range(l):
                if row >> i & 1:
                    acc ^= c[i]
            assert acc == 0


def test_degree_table_and_lt_generator():
    probs = [Fraction(DEG_F[j] - DEG_F[j - 1], 1 << 20) for j in range(1, 8)]
    assert sum(probs) == 1
    mean = sum(p * d for p, d in zip(probs, DEG_D[1:]))
    assert abs(float(mean) - 4.6314) < 1e-4
    assert [degree(v) for v in (0, 10240, 10241, 491581, 491582, 1048575)] == [1, 1, 2, 2, 3, 40]
    l, lp = 233, 233  # 233 is prime
    l2, lp2 = 230, 233
    for d, a, b in ((40, 7, 3), (11, 1, 232), (4, 232, 231), (300, 5, 0)):
        for ll, p in ((l, lp), (l2, lp2)):
            nb = lt_neighbors(d, a, b, ll, p)
            assert len(nb) == min(d, ll) and len(set(nb)) == len(nb)
            assert all(0 <= i < ll for i in nb)


def test_round_trip_and_wrong_answers_never():
    rng = random.Random(3)
    code = RaptorCode(1000, key=5)
    source = [rng.getrandbits(32) for _ in range(1000)]
    esis = rng.sample(range(50000), 1010)
    assert code.decode(esis, code.encode(source, esis)) == source
    for t in range(30):  # with too few symbols the decoder may fail, but it never lies
        code = RaptorCode(60, key=t)
        src = [rng.getrandbits(16) for _ in range(60)]
        esis = rng.sample(range(5000), 58 + t % 5)
        got = code.decode(esis, code.encode(src, esis))
        assert got is None or got == src


def test_success_rate_against_overhead():
    k, trials, seed = 200, 40, 1
    extras = (0, 2, 5, 10)
    raptor = [success_rate(k, e, trials, seed) for e in extras]
    lt_only = [success_rate(k, e, trials, seed, precode=False) for e in extras]
    assert raptor == [0.2, 0.725, 0.975, 1.0]
    # the same degree table without a precode leaves source symbols uncovered
    assert lt_only == [0.0, 0.0, 0.025, 0.1]
    # peeling alone stalls: the RFC 5053 design expects elimination on the leftover rows
    assert success_rate(k, 50, trials, seed, peel_only=True) == 0.075
    assert popcount(0b1011) == 3
