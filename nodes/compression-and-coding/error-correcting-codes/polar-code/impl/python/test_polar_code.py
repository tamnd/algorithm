# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polar-code/. The authors are listed in prov/HJNNKN.jsonl.

import itertools
import math
import random
from fractions import Fraction

from polar_code import (NR_SEQUENCE_PREFIX, arikan_encode, bec_bhattacharyya, bit_reverse,
                        crc_remainder, encode, info_set_bec, info_set_nr, polar_transform,
                        sc_decode, scl_decode)


def kron_power(n):
    g = [[1]]
    for _ in range(n):
        m = len(g)
        g = [[g[i % m][j % m] * (1 if (i >= m or j < m) else 0) for j in range(2 * m)]
             for i in range(2 * m)]
    return g


def mat_encode(u, g):
    return [sum(u[i] * g[i][j] for i in range(len(u))) % 2 for j in range(len(u))]


def test_transform_is_kronecker_power():
    rng = random.Random(1)
    for n in range(0, 6):
        g = kron_power(n)
        for _ in range(30):
            u = [rng.randrange(2) for _ in range(1 << n)]
            assert polar_transform(u) == mat_encode(u, g)
            assert polar_transform(polar_transform(u)) == u  # F^(kron n) is its own inverse


def test_row_weights():
    n = 4
    for i in range(16):
        row = polar_transform([int(j == i) for j in range(16)])
        assert sum(row) == 2 ** bin(i).count("1")


def test_min_distance_is_min_row_weight():
    rng = random.Random(8)
    for _ in range(40):
        n = rng.choice((3, 4))
        big = 1 << n
        k = rng.randrange(1, 9)
        info = sorted(rng.sample(range(big), k))
        d = min(sum(encode(m, info, n)) for m in itertools.product((0, 1), repeat=k) if any(m))
        assert d == min(2 ** bin(i).count("1") for i in info)
    polar = info_set_bec(5, 16, 0.5)
    rm = [i for i in range(32) if bin(i).count("1") >= 3]
    assert set(polar) - set(rm) == {24} and set(rm) - set(polar) == {7}


def test_bit_reversal_only_permutes_code_bits():
    rng = random.Random(2)
    n = 4
    for _ in range(50):
        u = [rng.randrange(2) for _ in range(16)]
        x = arikan_encode(u)
        y = polar_transform(u)
        assert x == [y[bit_reverse(j, n)] for j in range(16)]


def test_bec_recursion_values():
    z = bec_bhattacharyya(3, Fraction(1, 2))
    assert z == [Fraction(v, 256) for v in (255, 225, 207, 81, 175, 49, 31, 1)]
    assert info_set_bec(3, 4, 0.5) == [3, 5, 6, 7]
    for n in range(8):
        zs = bec_bhattacharyya(n, Fraction(1, 3))
        assert sum(zs) / len(zs) == Fraction(1, 3)  # the mean is kept at each level


def test_nr_prefix():
    assert NR_SEQUENCE_PREFIX[:10] == [0, 1, 2, 4, 8, 16, 32, 3, 5, 64]
    assert [q for q in NR_SEQUENCE_PREFIX if q < 8] == [0, 1, 2, 4, 3, 5, 6, 7]
    assert info_set_nr(3, 4) == [3, 5, 6, 7]
    assert info_set_nr(4, 8) == [6, 7, 10, 11, 12, 13, 14, 15]
    assert info_set_bec(4, 8, 0.5) == [7, 9, 10, 11, 12, 13, 14, 15]


def test_sc_noiseless_and_scl_list_one():
    rng = random.Random(3)
    n, k = 5, 16
    info = info_set_bec(n, k, 0.5)
    frozen = [i not in info for i in range(32)]
    for _ in range(100):
        msg = [rng.randrange(2) for _ in range(k)]
        x = encode(msg, info, n)
        llr = [(4.0 if b == 0 else -4.0) for b in x]
        u = sc_decode(llr, frozen)
        assert [u[i] for i in info] == msg
        noisy = [2 * (1 - 2 * b + rng.gauss(0, 1)) for b in x]
        assert scl_decode(noisy, frozen, 1) == sc_decode(noisy, frozen)


def test_scl_with_full_list_is_ml():
    rng = random.Random(4)
    n, k = 3, 3
    info = info_set_bec(n, k, 0.5)
    frozen = [i not in info for i in range(8)]
    book = []
    for msg in itertools.product((0, 1), repeat=k):
        u = [0] * 8
        for i, b in zip(info, msg):
            u[i] = b
        book.append((u, polar_transform(u)))
    for _ in range(300):
        llr = [rng.gauss(1.0, 2.0) for _ in range(8)]
        best = max(book, key=lambda c: sum((1 - 2 * b) * l for b, l in zip(c[1], llr)))[0]
        assert scl_decode(llr, frozen, 8) == best


def test_crc_aided_list_beats_sc_on_awgn():
    rng = random.Random(5)
    n, k, r, poly = 6, 32, 6, 0b1000011  # CRC generator x^6 + x + 1
    info = info_set_bec(n, k, 0.5)
    frozen = [i not in info for i in range(64)]
    sigma = 0.8
    err_sc = err_scl = 0
    frames = 250

    def check(u):
        bits = [u[i] for i in info]
        return crc_remainder(bits[:k - r], poly, r) == bits[k - r:]

    for _ in range(frames):
        msg = [rng.randrange(2) for _ in range(k - r)]
        x = encode(msg + crc_remainder(msg, poly, r), info, n)
        llr = [2 * (1 - 2 * b + rng.gauss(0, sigma)) / sigma ** 2 for b in x]
        u = sc_decode(llr, frozen)
        err_sc += [u[i] for i in info][:k - r] != msg
        v = scl_decode(llr, frozen, 8, check)
        err_scl += v is None or [v[i] for i in info][:k - r] != msg
    assert err_scl < err_sc
    assert err_sc > 0


def test_crc_remainder():
    poly, r = 0b10011, 4  # x^4 + x + 1
    rng = random.Random(6)
    for _ in range(100):
        m = [rng.randrange(2) for _ in range(rng.randrange(1, 20))]
        c = m + crc_remainder(m, poly, r)
        val = int("".join(map(str, c)), 2)
        rem = val
        for s in range(len(c) - 1, r - 1, -1):
            if rem >> s & 1:
                rem ^= poly << (s - r)
        assert rem == 0


def test_bec_sc_block_error_below_union_bound():
    # On BEC(eps), SC fails only if some information leaf sees an erasure. A Monte Carlo
    # estimate must stay below the sum of Z over the information set (Arikan, Prop. 2).
    rng = random.Random(7)
    n, k, eps = 7, 32, 0.4
    z = bec_bhattacharyya(n, eps)
    info = info_set_bec(n, k, eps)
    bound = sum(z[i] for i in info)
    frozen = [i not in info for i in range(128)]
    fails, trials = 0, 400
    for _ in range(trials):
        llr = [0.0 if rng.random() < eps else 30.0 for _ in range(128)]
        u = sc_decode(llr, frozen)
        fails += any(u[i] for i in info)
    assert bound < 0.1
    assert fails / trials <= bound + 0.03
    assert math.isclose(sum(z) / 128, eps)
