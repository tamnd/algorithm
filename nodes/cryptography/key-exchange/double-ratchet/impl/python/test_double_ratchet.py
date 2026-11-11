# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-ratchet/. The authors are listed in prov/EJKDEP.jsonl.
#
# The Double Ratchet specification has no official test vectors. These tests
# check X25519 and HKDF against their RFCs, and the ratchet by its properties.

import copy
import random

import pytest

from double_ratchet import (
    AuthError,
    concat,
    decrypt,
    KeyPair,
    TooManySkipped,
    hkdf,
    kdf_ck,
    ratchet_decrypt,
    ratchet_encrypt,
    ratchet_init_alice,
    ratchet_init_bob,
    x25519,
)

AD = b"AD from X3DH: IK_A || IK_B"


def h(s: str) -> bytes:
    return bytes.fromhex("".join(s.split()))


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


def make_pair(seed: int):
    rng = random.Random(seed)

    def rb(n):
        return bytes(rng.randrange(256) for _ in range(n))

    SK = rb(32)
    bob_spk = KeyPair(rb(32))
    alice = ratchet_init_alice(SK, bob_spk.public, rng=rb)
    bob = ratchet_init_bob(SK, bob_spk)
    return alice, bob, rb


def test_in_order_both_directions():
    alice, bob, rb = make_pair(1)
    for i in range(3):
        hd, ct = ratchet_encrypt(alice, b"a%d" % i, AD)
        assert ratchet_decrypt(bob, hd, ct, AD, rng=rb) == b"a%d" % i
    for i in range(2):
        hd, ct = ratchet_encrypt(bob, b"b%d" % i, AD)
        assert ratchet_decrypt(alice, hd, ct, AD, rng=rb) == b"b%d" % i
    hd, ct = ratchet_encrypt(alice, b"again", AD)
    assert hd.pn == 3 and hd.n == 0
    assert ratchet_decrypt(bob, hd, ct, AD, rng=rb) == b"again"


def test_out_of_order_and_across_ratchet_steps():
    alice, bob, rb = make_pair(2)
    m = [ratchet_encrypt(alice, b"m%d" % i, AD) for i in range(4)]
    assert ratchet_decrypt(bob, *m[2], AD, rng=rb) == b"m2"    # m0, m1 are skipped and stored
    assert len(bob.MKSKIPPED) == 2
    reply = ratchet_encrypt(bob, b"r0", AD)
    assert ratchet_decrypt(alice, *reply, AD, rng=rb) == b"r0"
    late = ratchet_encrypt(alice, b"new chain", AD)
    assert ratchet_decrypt(bob, *late, AD, rng=rb) == b"new chain"   # m3 skipped via PN
    assert ratchet_decrypt(bob, *m[0], AD, rng=rb) == b"m0"
    assert ratchet_decrypt(bob, *m[3], AD, rng=rb) == b"m3"
    assert ratchet_decrypt(bob, *m[1], AD, rng=rb) == b"m1"
    assert bob.MKSKIPPED == {}


def test_lost_messages_do_not_block():
    alice, bob, rb = make_pair(3)
    for i in range(5):
        hd, ct = ratchet_encrypt(alice, b"x%d" % i, AD)
        if i in (1, 3):
            continue  # lost in the network
        assert ratchet_decrypt(bob, hd, ct, AD, rng=rb) == b"x%d" % i
    assert len(bob.MKSKIPPED) == 2


def test_replay_is_rejected():
    alice, bob, rb = make_pair(4)
    hd, ct = ratchet_encrypt(alice, b"once", AD)
    assert ratchet_decrypt(bob, hd, ct, AD, rng=rb) == b"once"
    with pytest.raises(AuthError):
        ratchet_decrypt(bob, hd, ct, AD, rng=rb)


def test_max_skip():
    alice, bob, rb = make_pair(5)
    bob.max_skip = 10
    msgs = [ratchet_encrypt(alice, b"%d" % i, AD) for i in range(12)]
    with pytest.raises(TooManySkipped):
        ratchet_decrypt(bob, *msgs[11], AD, rng=rb)        # would skip 11 keys
    assert bob.Nr == 0 and bob.MKSKIPPED == {}             # state rolled back
    assert ratchet_decrypt(bob, *msgs[10], AD, rng=rb) == b"10"   # skips exactly 10


def test_tampered_ciphertext_and_state_rollback():
    alice, bob, rb = make_pair(6)
    hd, ct = ratchet_encrypt(alice, b"hello", AD)
    bad = ct[:-1] + bytes([ct[-1] ^ 1])
    before = copy.deepcopy(bob.__dict__)
    with pytest.raises(AuthError):
        ratchet_decrypt(bob, hd, bad, AD, rng=rb)
    assert bob.__dict__.keys() == before.keys() and bob.Nr == before["Nr"] and bob.DHr == before["DHr"]
    assert ratchet_decrypt(bob, hd, ct, AD, rng=rb) == b"hello"


def test_forward_secrecy_of_chain():
    # An attacker who steals Bob's state after m0 and m1 are read cannot read them:
    # their message keys are deleted and the chain key only goes forward.
    alice, bob, rb = make_pair(7)
    m0 = ratchet_encrypt(alice, b"secret 0", AD)
    m1 = ratchet_encrypt(alice, b"secret 1", AD)
    ratchet_decrypt(bob, *m0, AD, rng=rb)
    ratchet_decrypt(bob, *m1, AD, rng=rb)
    stolen = copy.deepcopy(bob)
    for m in (m0, m1):
        with pytest.raises(AuthError):
            ratchet_decrypt(stolen, *m, AD, rng=rb)
    # The chain key moves by a one-way step: no message key of the past comes out.
    ck = stolen.CKr
    future = set()
    for _ in range(5):
        ck, mk = kdf_ck(ck)
        future.add(mk)
    assert len(future) == 5


def test_post_compromise_healing():
    # The attacker copies Alice's full state, then only watches the network.
    alice, bob, rb = make_pair(8)
    attacker_rng = random.Random(99)
    eve = copy.deepcopy(alice)
    m0 = ratchet_encrypt(alice, b"before healing", AD)
    # With the copied sending chain key, Eve reads m0: the compromise works.
    _, mk = kdf_ck(eve.CKs)
    assert decrypt(mk, m0[1], concat(AD, m0[0])) == b"before healing"
    ratchet_decrypt(bob, *m0, AD, rng=rb)
    # Bob answers with a fresh ratchet key; Alice answers with a fresh one too.
    r = ratchet_encrypt(bob, b"reply", AD)
    ratchet_decrypt(alice, *r, AD, rng=rb)
    m1 = ratchet_encrypt(alice, b"after healing", AD)
    # Eve sees r and m1 on the wire, but she does not know Alice's new private key.
    eve_rng = lambda n: bytes(attacker_rng.randrange(256) for _ in range(n))  # noqa: E731
    ratchet_decrypt(eve, *r, AD, rng=eve_rng)  # Eve can read r: she holds the old DHs
    with pytest.raises(AuthError):
        ratchet_decrypt(eve, *m1, AD, rng=eve_rng)
    assert ratchet_decrypt(bob, *m1, AD, rng=rb) == b"after healing"
