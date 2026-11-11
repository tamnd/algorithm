# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/attribute-based-encryption/. The authors are listed in prov/Q5ZTFT.jsonl.
#
# There are no official test vectors for GPSW KP-ABE. The tests check the exponent arithmetic of
# the worked example of the page (modulo 11), decryption for satisfied policies, failure for
# unsatisfied ones, and that two colluding users cannot combine their keys, with fixed seeds.
# The curve is NOT secure.

import random

import attribute_based_encryption as abe

C = abe.TOY


def test_worked_example_exponents_mod_11() -> None:
    r = 11
    t = {"A": 2, "B": 3, "C": 5}
    y, s = 7, 4
    q_root = lambda x: (7 + 3 * x) % r
    assert q_root(0) == y and q_root(1) == 10 and q_root(2) == 2
    # Leaf exponents d_x = q_x(0) / t_a; the OR node has the constant polynomial 2.
    d = {"A": 10 * pow(2, -1, r) % r, "B": 2 * pow(3, -1, r) % r, "C": 2 * pow(5, -1, r) % r}
    assert d == {"A": 5, "B": 8, "C": 7}
    E = {a: s * t[a] % r for a in ("A", "C")}
    assert E == {"A": 8, "C": 9}
    F_A = d["A"] * E["A"] % r
    F_C = d["C"] * E["C"] % r
    assert (F_A, F_C) == (7, 8) == (s * 10 % r, s * 2 % r)
    assert abe.lagrange_at_zero(1, [1, 2], r) == 2 and abe.lagrange_at_zero(2, [1, 2], r) == 10
    root = (2 * F_A + 10 * F_C) % r
    assert root == 6 == y * s % r


def policy():
    # A AND (B OR C), the policy of the worked example.
    return abe.AND(abe.attr("A"), abe.OR(abe.attr("B"), abe.attr("C")))


def test_satisfied_and_unsatisfied_policies() -> None:
    rng = random.Random(2006)
    pk, msk = abe.setup(C, "ABCDE", rng)
    key = abe.keygen(C, pk, msk, policy(), rng)
    M = C.f2_pow(pk["Y"], 12345)  # a message in GT
    for attrs, ok in ((["A", "C"], True), (["A", "B", "E"], True), (["A", "D"], False), (["B", "C"], False)):
        assert abe.satisfies(policy(), attrs) == ok
        ct = abe.encrypt(C, pk, attrs, M, rng)
        assert (abe.decrypt(C, key, ct) == M) == ok
        if not ok:
            assert abe.decrypt(C, key, ct) is None


def test_threshold_gate_two_of_three() -> None:
    rng = random.Random(2005)
    pk, msk = abe.setup(C, "ABCD", rng)
    pol = abe.threshold(2, abe.attr("A"), abe.attr("B"), abe.attr("C"))
    key = abe.keygen(C, pk, msk, pol, rng)
    M = C.f2_pow(pk["Y"], 777)
    assert abe.decrypt(C, key, abe.encrypt(C, pk, ["A", "C"], M, rng)) == M
    assert abe.decrypt(C, key, abe.encrypt(C, pk, ["B", "C", "D"], M, rng)) == M
    assert abe.decrypt(C, key, abe.encrypt(C, pk, ["C", "D"], M, rng)) is None


def test_collusion_fails() -> None:
    rng = random.Random(2007)
    pk, msk = abe.setup(C, "ABCD", rng)
    # Alice holds A AND C, Bob holds D AND B. The ciphertext has {A, B}: neither key is satisfied.
    alice = abe.keygen(C, pk, msk, abe.AND(abe.attr("A"), abe.attr("C")), rng)
    bob = abe.keygen(C, pk, msk, abe.AND(abe.attr("D"), abe.attr("B")), rng)
    M = C.f2_pow(pk["Y"], 31337)
    ct = abe.encrypt(C, pk, ["A", "B"], M, rng)
    assert abe.decrypt(C, alice, ct) is None and abe.decrypt(C, bob, ct) is None
    # Alice's A share is q1(1) of her polynomial; Bob's B share is q2(2) of his. Pooling them fails.
    assert abe.collude(C, alice, 0, 1, bob, 1, 2, ct, "A", "B") != M
    # The same pooling inside one key works: a key for A AND B decrypts.
    carol = abe.keygen(C, pk, msk, abe.AND(abe.attr("A"), abe.attr("B")), rng)
    assert abe.collude(C, carol, 0, 1, carol, 1, 2, ct, "A", "B") == M == abe.decrypt(C, carol, ct)
