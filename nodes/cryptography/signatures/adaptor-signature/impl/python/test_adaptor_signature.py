# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptor-signature/. The authors are listed in prov/ZMDYYY.jsonl.

import random

from adaptor_signature import (
    G,
    N,
    adapt,
    extract,
    has_even_y,
    keygen,
    point_add,
    point_mul,
    pre_sign,
    pre_verify,
    schnorr_verify,
    xbytes,
)


def test_adapt_gives_a_bip340_signature_and_extract_finds_the_witness() -> None:
    rng = random.Random(2017)
    seen_parities = set()
    for _ in range(6):
        d, pub = keygen(rng.randrange(1, N))
        t = rng.randrange(1, N)
        stmt = point_mul(G, t)
        msg = b"tx %d" % rng.randrange(1000)
        presig = pre_sign(d, pub, msg, stmt, rng)
        seen_parities.add(has_even_y(point_add(presig[0], stmt)))
        assert pre_verify(pub, msg, stmt, presig)
        sig = adapt(presig, stmt, t)
        assert schnorr_verify(msg, xbytes(pub), sig)
        assert extract(sig, presig, stmt) == t
    assert seen_parities == {True, False}  # both branches of the parity rule ran


def test_pre_signature_is_not_a_signature_and_binds_the_statement() -> None:
    rng = random.Random(5)
    d, pub = keygen(rng.randrange(1, N))
    t = rng.randrange(1, N)
    stmt = point_mul(G, t)
    presig = pre_sign(d, pub, b"m", stmt, rng)
    as_sig = xbytes(point_add(presig[0], stmt)) + presig[1].to_bytes(32, "big")
    assert not schnorr_verify(b"m", xbytes(pub), as_sig)
    assert not pre_verify(pub, b"m", point_mul(G, t + 1), presig)
    assert not pre_verify(pub, b"other", stmt, presig)
    # Adapting with a wrong witness gives an invalid signature.
    assert not schnorr_verify(b"m", xbytes(pub), adapt(presig, stmt, t + 1))


def test_atomic_swap() -> None:
    rng = random.Random(42)
    a_sec, a_pub = keygen(rng.randrange(1, N))  # Alice
    b_sec, b_pub = keygen(rng.randrange(1, N))  # Bob
    t = rng.randrange(1, N)  # Alice's secret witness
    stmt = point_mul(G, t)
    tx_a = b"chain A: Alice pays Bob 1 coin"
    tx_b = b"chain B: Bob pays Alice 5 tokens"
    # Each side pre-signs the payment it makes, under the same statement T.
    pre_a = pre_sign(a_sec, a_pub, tx_a, stmt, rng)
    pre_b = pre_sign(b_sec, b_pub, tx_b, stmt, rng)
    assert pre_verify(a_pub, tx_a, stmt, pre_a) and pre_verify(b_pub, tx_b, stmt, pre_b)
    # Alice claims her tokens: she adapts Bob's pre-signature and publishes it.
    sig_b = adapt(pre_b, stmt, t)
    assert schnorr_verify(tx_b, xbytes(b_pub), sig_b)
    # Bob sees sig_b on chain B, extracts t, and claims his coin on chain A.
    t_bob = extract(sig_b, pre_b, stmt)
    sig_a = adapt(pre_a, stmt, t_bob)
    assert schnorr_verify(tx_a, xbytes(a_pub), sig_a)
