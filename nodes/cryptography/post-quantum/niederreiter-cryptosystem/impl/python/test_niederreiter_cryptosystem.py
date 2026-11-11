# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/niederreiter-cryptosystem/. The authors are listed in prov/3XG2CE.jsonl.
"""Tests for the toy Niederreiter scheme.

There are no official test vectors for these toy parameters, and the Classic
McEliece KAT files do not apply, because this is not Classic McEliece. The
tests check the constant weight encoding against itertools.combinations,
syndrome decoding against a brute force table on a small Goppa code, and the
round trip of encryption and decryption under fixed seeds.
"""

import random
from itertools import combinations
from math import comb

from niederreiter_cryptosystem import (
    FIELD16,
    FIELD64,
    Goppa,
    cw_decode,
    cw_encode,
    decrypt,
    encrypt,
    invert,
    keygen,
    mat_mul,
    mat_vec,
    random_irreducible,
    rank,
)


def test_constant_weight_encoding_is_a_bijection():
    """For n = 10, t = 3 the encoding must hit each weight 3 vector exactly once."""
    n, t = 10, 3
    seen = set()
    for x in range(comb(n, t)):
        e = cw_encode(x, n, t)
        assert bin(e).count("1") == t and e < (1 << n)
        assert cw_decode(e, t) == x
        seen.add(e)
    expected = {sum(1 << i for i in pos) for pos in combinations(range(n), t)}
    assert seen == expected


def test_constant_weight_encoding_is_colex_order():
    """The combinatorial number system lists the subsets in colex order,
    which is the order of the sorted reversed tuples."""
    n, t = 9, 4
    subsets = sorted(combinations(range(n), t), key=lambda p: tuple(reversed(p)))
    for x, pos in enumerate(subsets):
        assert cw_encode(x, n, t) == sum(1 << i for i in pos)


def test_page_example():
    """x = 13, n = 7, t = 3: 13 = C(5,3) + C(3,2) + C(0,1), positions {0, 3, 5}."""
    assert cw_encode(13, 7, 3) == (1 << 0) | (1 << 3) | (1 << 5)
    assert cw_decode(0b101001, 3) == 13


def test_constant_weight_round_trip_large():
    rng = random.Random(7)
    for _ in range(500):
        x = rng.randrange(comb(64, 5))
        assert cw_decode(cw_encode(x, 64, 5), 5) == x


def test_matrix_inverse():
    rng = random.Random(8)
    for _ in range(50):
        r = rng.randint(1, 30)
        while True:
            a = [rng.getrandbits(r) for _ in range(r)]
            if rank(a) == r:
                break
        assert mat_mul(invert(a), a) == [1 << i for i in range(r)]


def test_syndrome_decoding_against_brute_force():
    """On a Goppa code over GF(16) with n = 16 and t = 2, every syndrome of a
    vector of weight at most 2 must decode to that vector."""
    f = FIELD16
    rng = random.Random(5)
    code = Goppa(f, random_irreducible(f, 2, rng), list(range(16)))
    table = {}
    for w in range(3):
        for pos in combinations(range(16), w):
            e = sum(1 << i for i in pos)
            s = mat_vec(code.h, e)
            assert s not in table
            table[s] = e
    assert len(table) == 1 + 16 + comb(16, 2)
    for s, e in table.items():
        assert code.patterson(s) == e


def test_syndrome_decoding_on_gf64():
    f = FIELD64
    rng = random.Random(6)
    code = Goppa(f, random_irreducible(f, 5, rng), rng.sample(range(64), 64))
    for _ in range(500):
        e = sum(1 << i for i in rng.sample(range(64), rng.randint(0, 5)))
        assert code.patterson(mat_vec(code.h, e)) == e


def test_round_trip():
    for seed in (20, 21, 22):
        rng = random.Random(seed)
        pk, sk = keygen(FIELD64, 64, 5, rng)
        pub, n, t = pk
        assert (len(pub), n, t) == (30, 64, 5)
        for _ in range(100):
            x = rng.randrange(comb(n, t))
            s = encrypt(pk, x)
            assert s < (1 << 30)
            assert decrypt(sk, s) == x


def test_syndromes_of_weight_6_are_mostly_rejected():
    """A syndrome of a weight 6 vector has a preimage of weight 5 only when
    the code has a codeword of weight 11 (the minimum distance is at least 11).
    Decryption must be sound (any message it returns encrypts to s) and must
    reject almost all such syndromes."""
    rng = random.Random(23)
    pk, sk = keygen(FIELD64, 64, 5, rng)
    pub, n, t = pk
    rejected = 0
    for _ in range(100):
        e = sum(1 << i for i in rng.sample(range(n), 6))
        s = mat_vec(pub, e)
        x = decrypt(sk, s)
        if x is None:
            rejected += 1
        else:
            assert encrypt(pk, x) == s
            assert bin(cw_encode(x, n, t) ^ e).count("1") >= 11
    assert rejected >= 95
