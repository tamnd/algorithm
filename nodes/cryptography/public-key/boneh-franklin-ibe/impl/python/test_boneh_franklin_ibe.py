# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boneh-franklin-ibe/. The authors are listed in prov/BRDGNB.jsonl.
#
# RFC 5091 specifies Boneh-Franklin on other curves with other hash functions, so its values do
# not apply to this toy code, and there are no other official test vectors. The tests check the
# worked example of the page on p = 59, that the right identity decrypts and a wrong one does not,
# the malleability of BasicIdent and the checks of FullIdent, with fixed seeds.
# The curves are NOT secure.

import random

import boneh_franklin_ibe as bf


def test_worked_example_p59() -> None:
    C = bf.TINY
    P = C.generator()
    assert P == (35, 31)
    s = 2
    Ppub = C.mul(s, P)
    assert Ppub == (25, 29)
    params = (C, P, Ppub)
    Q_alice = C.mul(3, P)  # the example takes H1(alice) = 3P
    assert Q_alice == (25, 30)
    d_alice = bf.extract_point(params, s, Q_alice)
    assert d_alice == P  # 6P = P since q = 5
    g = C.pairing(Q_alice, Ppub)
    assert g == (42, 19)  # e(3P, 2P) = e(P, P)^6 = e(P, P)
    assert C.f2_pow(g, 4) == (42, 40)
    M = bytes(range(32))
    U, V = bf.basic_encrypt_point(params, Q_alice, M, 4)
    assert U == (35, 28)
    assert C.pairing(d_alice, U) == (42, 40)
    assert bf.basic_decrypt(params, d_alice, (U, V)) == M
    # Bob, with H1(bob) = P, has the key 2P and computes e(2P, 4P) = e(P, P)^3 instead.
    d_bob = bf.extract_point(params, s, P)
    assert C.pairing(d_bob, U) == (46, 56)
    assert bf.basic_decrypt(params, d_bob, (U, V)) != M


def test_h1_maps_into_g1() -> None:
    C = bf.TOY
    A, B = bf.H1(C, b"alice@example.com"), bf.H1(C, b"bob@example.com")
    assert C.in_g1(A) and C.in_g1(B) and A != B
    assert bf.H1(C, b"alice@example.com") == A


def test_basic_ident_right_and_wrong_identity() -> None:
    rng = random.Random(2001)
    params, s = bf.setup(bf.TOY, rng)
    C, P, Ppub = params
    d_alice = bf.extract(params, s, b"alice@example.com")
    d_bob = bf.extract(params, s, b"bob@example.com")
    # A user can check its key: e(d_ID, P) = e(H1(ID), P_pub).
    assert C.pairing(d_alice, P) == C.pairing(bf.H1(C, b"alice@example.com"), Ppub)
    for _ in range(2):
        M = bytes(rng.getrandbits(8) for _ in range(32))
        ct = bf.basic_encrypt(params, b"alice@example.com", M, rng)
        assert bf.basic_decrypt(params, d_alice, ct) == M
        assert bf.basic_decrypt(params, d_bob, ct) != M


def test_basic_ident_is_malleable() -> None:
    rng = random.Random(7)
    params, s = bf.setup(bf.TOY, rng)
    d = bf.extract(params, s, b"alice")
    M = b"pay bob 0010 dollars, from alice"
    U, V = bf.basic_encrypt(params, b"alice", M, rng)
    delta = bf.xor(b"pay bob 0010", b"pay eve 9990") + bytes(20)
    assert bf.basic_decrypt(params, d, (U, bf.xor(V, delta))) == b"pay eve 9990 dollars, from alice"


def test_full_ident_round_trip_and_rejection() -> None:
    rng = random.Random(2003)
    params, s = bf.setup(bf.TOY, rng)
    C, P, Ppub = params
    d_alice = bf.extract(params, s, b"alice")
    d_bob = bf.extract(params, s, b"bob")
    M = b"attack at dawn, the 32-byte text"
    U, V, W = bf.full_encrypt(params, b"alice", M, rng)
    assert bf.full_decrypt(params, d_alice, (U, V, W)) == M
    assert bf.full_decrypt(params, d_bob, (U, V, W)) is None
    flip = bytes([1]) + bytes(31)
    assert bf.full_decrypt(params, d_alice, (U, bf.xor(V, flip), W)) is None
    assert bf.full_decrypt(params, d_alice, (U, V, bf.xor(W, flip))) is None
    assert bf.full_decrypt(params, d_alice, (C.add(U, P), V, W)) is None
    assert bf.full_decrypt(params, d_alice, ((U[0], (U[1] + 1) % C.p), V, W)) is None
