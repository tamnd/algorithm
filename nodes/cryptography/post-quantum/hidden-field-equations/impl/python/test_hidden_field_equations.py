# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-field-equations/. The authors are listed in prov/N046XB.jsonl.
"""Tests for toy HFE, C* and Patarin's linearization attack. There are no
official test vectors for HFE or C*: the schemes were never standardized and
the toy sizes are our own. The tests check the hand example of the page,
compare the field and root finding code with brute force, and check round
trips and the attack under fixed seeds."""

import random

from hidden_field_equations import (
    MODULI,
    Field,
    QuadraticMap,
    central_eval,
    cstar_decrypt,
    cstar_keygen,
    decrypt,
    encrypt,
    keygen,
    linearization_relations,
    patarin_attack,
    roots,
)


def clmul_reduce(a, b, modulus, n):
    """Independent oracle: carry-less product, then long division."""
    p = 0
    for i in range(n):
        if (b >> i) & 1:
            p ^= a << i
    for i in range(2 * n - 2, n - 1, -1):
        if (p >> i) & 1:
            p ^= modulus << (i - n)
    return p


def gf2_poly_mod(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def test_moduli_are_irreducible():
    for n, f in MODULI.items():
        assert f.bit_length() == n + 1
        for g in range(2, 1 << (n // 2 + 1)):
            assert gf2_poly_mod(f, g) != 0, (n, g)


def test_field_against_oracle():
    rng = random.Random(1)
    for n in (7, 11, 16):
        F = Field(n, MODULI[n])
        for _ in range(500):
            a, b = rng.getrandbits(n), rng.getrandbits(n)
            assert F.mul(a, b) == clmul_reduce(a, b, MODULI[n], n)
        a = 1 + rng.randrange((1 << n) - 1)
        assert F.mul(a, F.inv(a)) == 1


def test_page_example_cstar_gf8():
    """GF(8) = GF(2)[t]/(t^3 + t + 1), theta = 1: X^3 with X = t is t + 1,
    and (t + 1)^5 = t. Patarin's relation A B^2 = A^4 B holds with both
    sides equal to 1."""
    F = Field(3, 0b1011)
    A, B = 0b010, 0b011
    assert F.pow(A, 3) == B
    assert F.pow(B, 5) == A
    assert F.mul(A, F.pow(B, 2)) == F.mul(F.pow(A, 4), B) == 1


def horner(F, f, x):
    v = 0
    for c in reversed(f):
        v = F.mul(v, x) ^ c
    return v


def test_roots_against_brute_force():
    rng = random.Random(2)
    F = Field(7, MODULI[7])
    for k in range(500):
        if k % 2:
            f = [1]
            for r in rng.sample(range(128), rng.randint(1, 5)):
                f = [a ^ b for a, b in zip([0] + f, [F.mul(r, c) for c in f] + [0])]
        else:
            f = [rng.randrange(128) for _ in range(rng.randint(2, 7))] + [1 + rng.randrange(127)]
        brute = [x for x in range(128) if horner(F, f, x) == 0]
        assert roots(F, f) == brute


def test_public_key_is_the_composition():
    rng = random.Random(3)
    P, sk = keygen(11, 24, 5, rng)
    for _ in range(500):
        x = rng.getrandbits(11)
        assert P(x) == sk.T(central_eval(sk.F, sk.central, sk.S(x)))


def test_hfe_round_trip():
    rng = random.Random(4)
    for n, d, r, count in [(11, 24, 5, 30), (16, 24, 8, 15)]:
        P, sk = keygen(n, d, r, rng)
        for _ in range(count):
            m = rng.getrandbits(n - r)
            assert decrypt(sk, encrypt(P, m, r)) == m


def test_cstar_is_a_bijection_and_decrypts():
    rng = random.Random(5)
    P, sk = cstar_keygen(7, 1, rng)
    images = [P(x) for x in range(128)]
    assert sorted(images) == list(range(128))
    assert all(cstar_decrypt(sk, y) == x for x, y in enumerate(images))


def test_patarin_attack_decrypts_cstar():
    rng = random.Random(6)
    for n, theta in [(7, 1), (9, 1), (11, 2)]:
        P, sk = cstar_keygen(n, theta, rng)
        rel = linearization_relations(P, n, rng)     # public key only
        assert len(rel) >= n
        for _ in range(50):
            x = rng.getrandbits(n)
            assert patarin_attack(P, n, rel, P(x)) == x


def test_no_linearization_relations_for_toy_hfe():
    """The relation comes from the monomial shape of C*; a random HFE
    central polynomial of degree 24 at n = 11 gives none."""
    rng = random.Random(7)
    P, _ = keygen(11, 24, 5, rng)
    assert linearization_relations(P, 11, rng) == []
    assert isinstance(P, QuadraticMap)
