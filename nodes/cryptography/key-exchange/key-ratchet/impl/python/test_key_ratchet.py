# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-ratchet/. The authors are listed in prov/EE0J5J.jsonl.

import copy
import random

from key_ratchet import (
    BASE_U,
    DHRatchet,
    SymmetricRatchet,
    chain_step,
    hkdf,
    x25519,
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


def test_both_sides_of_a_chain_agree():
    a, b = SymmetricRatchet(bytes(32)), SymmetricRatchet(bytes(32))
    assert [a.next_key() for _ in range(5)] == [b.next_key() for _ in range(5)]


def test_forward_secrecy_of_the_chain():
    # A thief who takes the chain key after five steps gets no old message key.
    r = SymmetricRatchet(rng_from(1)(32))
    old = [r.next_key() for _ in range(5)]
    stolen = r.ck
    ck, seen = stolen, set()
    for _ in range(50):
        ck, mk = chain_step(ck)
        seen.add(mk)
        seen.add(ck)
    assert not seen & set(old)
    # The thief does get every future key of this chain: the chain alone does not heal.
    assert chain_step(stolen)[1] == r.next_key()


def make_pair(seed: int):
    rb = rng_from(seed)
    root = rb(32)
    a_priv, b_priv = rb(32), rb(32)
    alice = DHRatchet(root, a_priv, x25519(b_priv, BASE_U))
    bob = DHRatchet(root, b_priv, x25519(a_priv, BASE_U))
    return alice, bob, rb


def test_dh_ratchet_agreement():
    alice, bob, rb = make_pair(2)
    for turn in range(6):
        sender, receiver = (alice, bob) if turn % 2 == 0 else (bob, alice)
        pub, ck_send = sender.send_step(rb)
        assert receiver.receive_step(pub) == ck_send
        assert sender.rk == receiver.rk


def test_dh_ratchet_heals_after_compromise():
    alice, bob, rb = make_pair(3)
    eve = copy.deepcopy(alice)                   # Eve copies Alice's full state once
    pub, ck = bob.send_step(rb)
    assert eve.receive_step(pub) == ck           # Bob's next chain: Eve still follows
    assert alice.receive_step(pub) == ck
    pub2, ck2 = alice.send_step(rb)              # Alice uses fresh randomness that Eve does not see
    eve_rng = rng_from(99)
    eve_guess = eve.send_step(eve_rng)[1]
    assert eve_guess != ck2
    assert bob.receive_step(pub2) == ck2
    # From here on, every key depends on the new root key, which Eve does not have.
    pub3, ck3 = bob.send_step(rb)
    assert alice.receive_step(pub3) == ck3
    assert eve.receive_step(pub3) != ck3
