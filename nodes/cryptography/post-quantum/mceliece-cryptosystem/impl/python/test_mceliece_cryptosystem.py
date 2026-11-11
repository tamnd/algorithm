# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mceliece-cryptosystem/. The authors are listed in prov/060YA3.jsonl.
"""Tests for the toy McEliece scheme.

This is not Classic McEliece, so the Classic McEliece KAT files do not apply,
and there are no official test vectors for these toy parameters. The tests
check the field and polynomial arithmetic, check Patterson decoding against
brute force decoding on a small Goppa code, and check the round trip of
encryption and decryption under fixed seeds.
"""

import random
from itertools import combinations

from mceliece_cryptosystem import (
    FIELD16,
    FIELD64,
    Goppa,
    decrypt,
    encrypt,
    is_irreducible,
    keygen,
    nullspace,
    peval,
    pinv_mod,
    pmod,
    pmul,
    psqrt_mod,
    random_irreducible,
    vec_mat,
)


def parity(x):
    return bin(x).count("1") & 1


def test_field_axioms():
    f = FIELD64
    for a in range(1, 64):
        assert f.mul(a, f.inv(a)) == 1
    rng = random.Random(1)
    for _ in range(300):
        a, b, c = rng.randrange(64), rng.randrange(64), rng.randrange(64)
        assert f.mul(a, b ^ c) == f.mul(a, b) ^ f.mul(a, c)
        assert f.mul(f.mul(a, b), c) == f.mul(a, f.mul(b, c))


def test_irreducibility_against_root_search():
    """Over GF(16), a polynomial of degree 2 or 3 is irreducible if and only if it has no root."""
    f = FIELD16
    rng = random.Random(2)
    for _ in range(500):
        d = rng.choice([2, 3])
        g = [rng.randrange(16) for _ in range(d)] + [1]
        has_root = any(peval(f, g, x) == 0 for x in range(16))
        assert is_irreducible(f, g) == (not has_root)


def test_inverse_and_square_root_modulo_g():
    f = FIELD64
    rng = random.Random(3)
    g = random_irreducible(f, 5, rng)
    for _ in range(200):
        a = [rng.randrange(64) for _ in range(5)]
        while a and a[-1] == 0:
            a.pop()
        if not a:
            continue
        assert pmod(f, pmul(f, a, pinv_mod(f, a, g)), g) == [1]
        r = psqrt_mod(f, a, g)
        assert pmod(f, pmul(f, r, r), g) == a


def test_parity_check_and_generator_are_orthogonal():
    f = FIELD64
    rng = random.Random(4)
    g = random_irreducible(f, 5, rng)
    code = Goppa(f, g, rng.sample(range(64), 64))
    gen = nullspace(code.h, 64)
    assert len(gen) >= 64 - 6 * 5
    for row in gen:
        assert all(parity(row & hr) == 0 for hr in code.h)
        assert code.syndrome_poly(row) == []


def test_patterson_against_brute_force():
    """On the Goppa code over GF(16) with n = 16 and t = 2, Patterson must
    return the unique error of weight <= 2 that brute force finds."""
    f = FIELD16
    rng = random.Random(5)
    g = random_irreducible(f, 2, rng)
    code = Goppa(f, g, list(range(16)))
    table = {}
    for w in range(3):
        for pos in combinations(range(16), w):
            e = sum(1 << i for i in pos)
            key = tuple(code.syndrome_poly(e))
            assert key not in table  # the code corrects 2 errors
            table[key] = e
    gen = nullspace(code.h, 16)
    for _ in range(500):
        c = vec_mat(rng.getrandbits(len(gen)), gen)
        e = sum(1 << i for i in rng.sample(range(16), rng.randint(0, 2)))
        y = c ^ e
        assert code.patterson(y) == table[tuple(code.syndrome_poly(y))] == e


def test_patterson_corrects_t_errors_on_gf64():
    f = FIELD64
    rng = random.Random(6)
    g = random_irreducible(f, 5, rng)
    code = Goppa(f, g, rng.sample(range(64), 64))
    gen = nullspace(code.h, 64)
    for _ in range(300):
        c = vec_mat(rng.getrandbits(len(gen)), gen)
        e = sum(1 << i for i in rng.sample(range(64), rng.randint(0, 5)))
        assert code.patterson(c ^ e) == e


def test_round_trip():
    for seed in (10, 11, 12):
        rng = random.Random(seed)
        pk, sk = keygen(FIELD64, 64, 5, rng)
        pub, n, t = pk
        k = len(pub)
        assert (n, t) == (64, 5) and k == 34
        for _ in range(100):
            msg = rng.getrandbits(k)
            c = encrypt(pk, msg, rng)
            assert decrypt(sk, c) == msg


def test_too_many_errors_do_not_decrypt_to_the_message():
    rng = random.Random(13)
    pk, sk = keygen(FIELD64, 64, 5, rng)
    pub, n, t = pk
    bad = 0
    for _ in range(100):
        msg = rng.getrandbits(len(pub))
        e = sum(1 << i for i in rng.sample(range(n), 8))
        if decrypt(sk, vec_mat(msg, pub) ^ e) != msg:
            bad += 1
    assert bad >= 95
