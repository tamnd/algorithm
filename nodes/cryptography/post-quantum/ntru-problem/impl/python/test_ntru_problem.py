# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntru-problem/. The authors are listed in prov/C899GW.jsonl.
"""Tests for toy NTRU key generation, encryption and the lattice attack.

These are toy parameters of our own choice (n = 11, 13, 17, p = 3, q = 128),
not the parameter sets of HPS 1998 or of the NIST submission, so there are
no official test vectors. With q = 128 and d <= 5, every coefficient of
p r g + f m has absolute value at most 8 d + 1 < 64, so decryption never fails.
"""

import random

from ntru_problem import (
    center,
    cmul,
    decrypt,
    encrypt,
    has_key_shape,
    inverse_mod_power_of_two,
    inverse_mod_prime,
    is_rotation,
    keygen,
    lattice_attack,
    lll,
    ntru_lattice_basis,
    ternary,
)

Q = 128
SIZES = ((11, 3), (13, 4), (17, 5))


def test_inverses():
    rng = random.Random(1)
    count = 0
    for _ in range(500):
        n = rng.choice((7, 11, 13))
        f = [rng.randint(-1, 1) for _ in range(n)]
        for mod, inv in ((3, inverse_mod_prime(f, 3)), (Q, inverse_mod_power_of_two(f, Q)), (2, inverse_mod_prime(f, 2))):
            if inv is None:
                continue
            count += 1
            one = [1] + [0] * (n - 1)
            assert cmul(f, inv, mod) == one
    assert count > 300


def test_not_invertible_when_divisible_by_x_minus_1():
    # f(1) = 0 mod 3 means x - 1 divides f mod 3.
    f = [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert inverse_mod_prime(f, 3) is None
    assert inverse_mod_power_of_two(f, Q) is None


def test_public_key_relation():
    rng = random.Random(2)
    for n, d in SIZES:
        h, f, g, fp = keygen(n, Q, d, rng)
        hp = [pow(3, -1, Q) * x % Q for x in h]
        assert center(cmul(f, hp, Q), Q) == g  # f h' = g mod q
        assert cmul(f, fp, 3) == [1] + [0] * (n - 1)


def test_encrypt_decrypt_round_trip():
    rng = random.Random(3)
    for n, d in SIZES:
        h, f, g, fp = keygen(n, Q, d, rng)
        for _ in range(100):
            m = [rng.randint(-1, 1) for _ in range(n)]
            r = ternary(n, d, d, rng)
            assert decrypt(encrypt(h, m, r, Q), f, fp, Q) == m


def test_lll_on_small_basis():
    # A basis of Z^2 (determinant 1) with long vectors reduces to unit vectors.
    red = lll([[89, 144], [233, 377]])
    assert sorted(sum(x * x for x in v) for v in red) == [1, 1]
    # LLL keeps the lattice: the determinant is unchanged up to sign.
    red = lll([[201, 37], [1648, 297]])
    det = red[0][0] * red[1][1] - red[0][1] * red[1][0]
    assert abs(det) == abs(201 * 297 - 37 * 1648)


def test_lattice_contains_key_and_u():
    rng = random.Random(4)
    n, d = 11, 3
    h, f, g, _ = keygen(n, Q, d, rng)
    hp = [pow(3, -1, Q) * x % Q for x in h]
    B = ntru_lattice_basis(hp, Q)
    # (f, g) = sum f_i row_i + (multiples of q rows); check by f h' = g mod q.
    assert center(cmul(f, hp, Q), Q) == g
    # (u, 0): u h' = h'(1) u and h'(1) = 0 mod q.
    assert sum(hp) % Q == 0
    assert len(B) == 2 * n


def test_attack_recovers_key_up_to_rotation():
    exact = 0
    total = 0
    for n, d in SIZES:
        for seed in range(12):
            rng = random.Random(1000 + 97 * n + seed)
            h, f, g, fp = keygen(n, Q, d, rng)
            res = lattice_attack(h, Q, d)
            total += 1
            if res is None:
                continue
            F, G = res
            assert has_key_shape(F, G, d)
            if is_rotation(F, G, f, g):
                exact += 1
            # A key equal to +- x^i (f, g) decrypts, with its own inverse mod 3.
            Fp = inverse_mod_prime(F, 3)
            if Fp is None:
                continue
            for _ in range(10):
                m = [rng.randint(-1, 1) for _ in range(n)]
                r = ternary(n, d, d, rng)
                e = encrypt(h, m, r, Q)
                if is_rotation(F, G, f, g):
                    assert decrypt(e, F, Fp, Q) == m
    assert exact >= total - 3
