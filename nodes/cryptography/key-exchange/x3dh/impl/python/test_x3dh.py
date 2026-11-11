# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x3dh/. The authors are listed in prov/F1F34V.jsonl.
#
# The X3DH specification has no official test vectors. These tests check
# X25519, HKDF and the Edwards curve code against their RFCs, and X3DH and
# XEdDSA by their properties.

import random

import pytest

from x3dh import (
    BASE_U,
    Bob,
    KeyPair,
    X3DHError,
    alice_send,
    ed25519_public,
    ed25519_sign,
    ed25519_verify,
    encode,
    hkdf,
    x25519,
    xeddsa_sign,
    xeddsa_verify,
)


def h(s: str) -> bytes:
    return bytes.fromhex("".join(s.split()))


def rng_from(seed: int):
    r = random.Random(seed)
    return lambda n: bytes(r.randrange(256) for _ in range(n))


def test_x25519_rfc7748_section_5_2():
    # RFC 7748, Section 5.2, copied by hand.
    assert x25519(
        h("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4"),
        h("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c"),
    ) == h("c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552")
    assert x25519(
        h("4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d"),
        h("e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493"),
    ) == h("95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957")


def test_hkdf_rfc5869_case_1():
    # RFC 5869, Appendix A.1, Test Case 1, copied by hand.
    assert hkdf(bytes([0x0B] * 22), h("000102030405060708090a0b0c"), h("f0f1f2f3f4f5f6f7f8f9"), 42) == h(
        "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865")


def test_edwards_code_rfc8032_test_1():
    # RFC 8032, Section 7.1, TEST 1, copied by hand. It checks the curve code that XEdDSA uses.
    seed = h("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
    pub = h("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
    sig = h("e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b")
    assert ed25519_public(seed) == pub
    assert ed25519_sign(seed, b"") == sig
    assert ed25519_verify(pub, b"", sig)
    assert not ed25519_verify(pub, b"x", sig)


def test_xeddsa_sign_and_verify():
    rb = rng_from(1)
    for _ in range(3):
        k = rb(32)
        u = x25519(k, BASE_U)
        msg = rb(33)
        sig = xeddsa_sign(k, msg, rb(64))
        assert xeddsa_verify(u, msg, sig)
        assert not xeddsa_verify(u, msg + b"!", sig)
        bad = sig[:40] + bytes([sig[40] ^ 1]) + sig[41:]
        assert not xeddsa_verify(u, msg, bad)


def test_same_sk_with_one_time_prekey():
    rb = rng_from(2)
    bob = Bob(rng=rb)
    alice_ik = KeyPair(rb(32))
    sk_a, ad, msg = alice_send(alice_ik, bob.bundle(), b"hello Bob", rng=rb)
    assert msg["opk_id"] is not None
    sk_b = bob.receive(msg)
    assert sk_a == sk_b and len(sk_a) == 32
    assert ad == encode(alice_ik.public) + encode(bob.IK.public) and len(ad) == 66
    assert msg["opk_id"] not in bob.OPK          # the one-time prekey is deleted


def test_same_sk_without_one_time_prekey():
    rb = rng_from(3)
    bob = Bob(rng=rb, n_opk=0)
    alice_ik = KeyPair(rb(32))
    sk_a, _, msg = alice_send(alice_ik, bob.bundle(), b"hi", rng=rb)
    assert msg["opk_id"] is None
    assert bob.receive(msg) == sk_a


def test_bad_signed_prekey_signature_is_rejected():
    rb = rng_from(4)
    bob = Bob(rng=rb)
    bundle = bob.bundle()
    bundle["SPK"] = KeyPair(rb(32)).public       # a server swaps the signed prekey
    with pytest.raises(X3DHError):
        alice_send(KeyPair(rb(32)), bundle, b"x", rng=rb)


def test_wrong_identity_gives_another_key():
    rb = rng_from(5)
    bob = Bob(rng=rb)
    alice_ik = KeyPair(rb(32))
    _, _, msg = alice_send(alice_ik, bob.bundle(), b"x", rng=rb)
    msg["IK"] = KeyPair(rb(32)).public           # Mallory claims to be someone else
    with pytest.raises(X3DHError):
        bob.receive(msg)


def test_replay_without_opk_and_with_opk():
    rb = rng_from(6)
    # Without a one-time prekey a replayed first message gives Bob the same SK again.
    bob = Bob(rng=rb, n_opk=0)
    sk, _, msg = alice_send(KeyPair(rb(32)), bob.bundle(), b"x", rng=rb)
    assert bob.receive(msg) == sk
    assert bob.receive(dict(msg)) == sk
    # With a one-time prekey the replay fails: the prekey is gone.
    bob2 = Bob(rng=rb)
    _, _, msg2 = alice_send(KeyPair(rb(32)), bob2.bundle(), b"x", rng=rb)
    bob2.receive(msg2)
    with pytest.raises(X3DHError):
        bob2.receive(dict(msg2))
