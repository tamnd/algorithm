# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bike/. The authors are listed in prov/H257TC.jsonl.
"""Tests for the toy BIKE-shaped KEM.

This is not the BIKE specification, so the official BIKE KAT files do not
apply, and there are no official test vectors for these toy parameters. The
tests check the ring arithmetic against a naive oracle, the counters against
direct counting, the round trip of the KEM, implicit rejection, and the
decoding failure rate under fixed seeds.
"""

import random

from bike import (
    D,
    R,
    T_ERR,
    Block,
    bgf,
    bit_flip,
    decaps,
    encaps,
    hash_k,
    inverse,
    keygen,
    mul_sparse,
    random_sparse,
    support,
    threshold,
)


def naive_mul(a, b, r):
    """Schoolbook product in GF(2)[x] / (x^r - 1), coefficient by coefficient."""
    out = [0] * r
    for i in range(r):
        if (a >> i) & 1:
            for j in range(r):
                if (b >> j) & 1:
                    out[(i + j) % r] ^= 1
    return sum(bit << i for i, bit in enumerate(out))


def test_multiplication_against_naive_oracle():
    rng = random.Random(1)
    for _ in range(500):
        r = rng.choice([5, 7, 11, 13])
        a, b = rng.getrandbits(r), rng.getrandbits(r)
        assert mul_sparse(a, support(b), r) == naive_mul(a, b, r)


def test_inverse_of_odd_weight_polynomials():
    """For r prime with 2 primitive modulo r, every polynomial of odd weight
    below r is invertible modulo x^r - 1."""
    rng = random.Random(2)
    for r in (11, 13, 19, 29):
        for _ in range(50):
            w = rng.randrange(1, r, 2)
            a = random_sparse(r, w, rng)
            assert naive_mul(a, inverse(a, r), r) == 1
    for _ in range(5):
        a = random_sparse(R, D, rng)
        assert mul_sparse(inverse(a, R), support(a), R) == 1


def test_counters_against_direct_count():
    rng = random.Random(3)
    for r in (13, 101, R):
        h = random_sparse(r, 7, rng)
        blk = Block(h, r)
        for _ in range(5):
            s = rng.getrandbits(r)
            ctr = blk.counters(s)
            for j in range(r):
                column = mul_sparse(1 << j, blk.supp, r)   # column j of the circulant block
                assert ctr[j] == bin(column & s).count("1")


def test_page_example():
    """r = 7, h0 = 1 + x + x^3, h1 = 1 + x^2 + x^3, e = (x^2, 0)."""
    r = 7
    h0, h1 = Block(0b1011, r), Block(0b1101, r)
    s = mul_sparse(1 << 2, h0.supp, r)
    assert s == (1 << 2) | (1 << 3) | (1 << 5)
    assert list(h0.counters(s)) == [1, 1, 3, 1, 1, 1, 1]
    assert list(h1.counters(s)) == [2, 1, 2, 2, 0, 1, 1]


def test_threshold_range():
    for s_weight in range(1, D * T_ERR + 1, 7):
        thr = threshold(s_weight, R, D, T_ERR)
        assert (D + 1) // 2 <= thr <= D + 1


def test_decoder_on_zero_and_single_errors():
    rng = random.Random(4)
    h0, h1 = Block(random_sparse(R, D, rng), R), Block(random_sparse(R, D, rng), R)
    assert bgf(0, h0, h1, T_ERR) == (0, 0)
    for _ in range(5):
        j = rng.randrange(R)
        assert bgf(mul_sparse(1 << j, h1.supp, R), h0, h1, T_ERR) == (0, 1 << j)


def test_round_trip():
    rng = random.Random(5)
    for _ in range(10):
        pk, sk = keygen(rng)
        for _ in range(4):
            c, k = encaps(pk, rng)
            assert decaps(sk, c) == k


def test_implicit_rejection():
    rng = random.Random(6)
    pk, sk = keygen(rng)
    sigma = sk[2]
    for _ in range(5):
        (c0, c1), k = encaps(pk, rng)
        bad1 = (c0, bytes([c1[0] ^ 1]) + c1[1:])
        assert decaps(sk, bad1) == hash_k(sigma, bad1[0], bad1[1], R) != k
        bad0 = (c0 ^ (1 << rng.randrange(R)), c1)
        assert decaps(sk, bad0) == hash_k(sigma, bad0[0], bad0[1], R) != k


def failures(t, trials, seed, decoder):
    rng = random.Random(seed)
    count = 0
    for i in range(trials):
        if i % 25 == 0:
            h0 = Block(random_sparse(R, D, rng), R)
            h1 = Block(random_sparse(R, D, rng), R)
        e = sum(1 << p for p in rng.sample(range(2 * R), t))
        e0, e1 = e & ((1 << R) - 1), e >> R
        s = mul_sparse(e0, h0.supp, R) ^ mul_sparse(e1, h1.supp, R)
        if decoder(s, h0, h1, t) != (e0, e1):
            count += 1
    return count


def test_failure_rate_at_the_toy_weight():
    """At t = 18 the toy decoder should almost never fail."""
    assert failures(T_ERR, 150, 7, bgf) <= 2


def test_failure_rate_grows_with_the_error_weight_and_bgf_beats_plain_flipping():
    """At t = 24 failures are frequent, and BGF fails less often than plain
    bit flipping with the same number of iterations, on the same instances."""
    f_bgf = failures(24, 100, 8, bgf)
    f_bf = failures(24, 100, 8, bit_flip)
    assert 3 <= f_bgf < f_bf
