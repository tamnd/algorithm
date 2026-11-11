# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mqv/. The authors are listed in prov/9AG3KC.jsonl.

import random

from mqv import G, P, Q, avf, kaliski_uks, keypair, mqv_key, mqv_sigma


def test_avf_is_half_length() -> None:
    for r in (0, 1, 2**200 + 5, P - 1):
        v = avf(r)
        assert 2**128 <= v < 2**129  # q has 255 bits, so w = 128
    assert avf(1153, 5) == 33 and avf(2020, 5) == 36


def test_small_example() -> None:
    p, q, g, w = 2039, 1019, 4, 5
    a, b, x, y = 57, 311, 100, 200
    A, B, X, Y = (pow(g, v, p) for v in (a, b, x, y))
    assert (A, B, X, Y) == (1556, 1502, 1153, 2020)
    s_a = mqv_sigma(a, x, X, B, Y, p, q, w)
    s_b = mqv_sigma(b, y, Y, A, X, p, q, w)
    assert s_a == s_b == 1795
    # sigma = g^(s_A * s_B) with s_A = 962 and s_B = 187
    assert pow(g, 962 * 187 % q, p) == 1795


def test_agreement_and_independence_against_a_direct_formula() -> None:
    rng = random.Random(1)
    for _ in range(10):
        (a, A), (b, B) = keypair(rng), keypair(rng)
        x, y = rng.randrange(1, Q), rng.randrange(1, Q)
        X, Y = pow(G, x, P), pow(G, y, P)
        ka = mqv_key("A", "B", True, a, x, B, Y)
        kb = mqv_key("B", "A", False, b, y, A, X)
        assert ka == kb and ka is not None
        # independent check of the exponent: g^((x + d a)(y + e b))
        d, e = avf(X), avf(Y)
        assert mqv_sigma(a, x, X, B, Y) == pow(G, (x + d * a) * (y + e * b) % Q, P)


def test_invalid_values_are_rejected() -> None:
    rng = random.Random(2)
    (a, _), (_, B) = keypair(rng), keypair(rng)
    x = rng.randrange(1, Q)
    non_residue = next(v for v in range(2, 100) if pow(v, Q, P) != 1)  # outside the subgroup
    for bad in (0, 1, P - 1, P, non_residue):
        assert mqv_sigma(a, x, pow(G, x, P), B, bad) is None
        assert mqv_sigma(a, x, pow(G, x, P), bad, pow(G, 5, P)) is None


def test_kaliski_unknown_key_share() -> None:
    rng = random.Random(3)
    (a, A), (b, B) = keypair(rng), keypair(rng)
    x, y = rng.randrange(1, Q), rng.randrange(1, Q)
    X, Y = pow(G, x, P), pow(G, y, P)
    c, E, X_e = kaliski_uks(A, X, rng)
    assert pow(G, c, P) == E  # Eve knows her static key: she can pass a proof of possession
    # A runs with B (sending X); B runs with "E" (receiving X_e); Eve forwards Y to A.
    sig_a = mqv_sigma(a, x, X, B, Y)
    sig_b = mqv_sigma(b, y, Y, E, X_e)
    assert sig_a is not None and sig_a == sig_b
    # With K = KDF(sigma) the keys match: A thinks the peer is B, B thinks it is E. Eve does not know K.
    k_a = mqv_key("A", "B", True, a, x, B, Y, bind=False)
    k_b = mqv_key("B", "E", False, b, y, E, X_e, bind=False)
    assert k_a == k_b
    # With identities and the transcript in the KDF, the keys differ and the attack fails.
    assert mqv_key("A", "B", True, a, x, B, Y) != mqv_key("B", "E", False, b, y, E, X_e)
