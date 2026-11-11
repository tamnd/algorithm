# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signal-protocol/. The authors are listed in prov/EQ8HBA.jsonl.
#
# The Signal specifications (X3DH and Double Ratchet, revision 1, 2016) have
# no test vectors. The local X25519 and Ed25519 copies are checked with
# RFC 7748 Section 5.2 and RFC 8032 Section 7.1 TEST 1, copied by hand. The
# other tests check the protocol's behaviour: agreement, out-of-order
# delivery, forward secrecy, healing after a compromise, and deniability.

import pytest

from signal_protocol import (
    AuthError,
    KeyPair,
    KeyServer,
    User,
    accept_session,
    ed25519_public,
    ed25519_sign,
    ed25519_verify,
    forge_initial_message,
    kdf_ck,
    open_sealed,
    encode_header,
    start_session,
    steal,
    x25519,
    x3dh_kdf,
    dh,
)

h = bytes.fromhex


def test_rfc7748_and_rfc8032_vectors():
    k = h("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
    u = h("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
    assert x25519(k, u) == h("c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552")
    sk = h("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
    pk = h("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
    sig = h("e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b")
    assert ed25519_public(sk) == pk and ed25519_sign(sk, b"") == sig and ed25519_verify(pk, b"", sig)


def pair():
    server, alice, bob = KeyServer(), User("alice"), User("bob")
    server.publish(bob)
    a, init = start_session(alice, server.fetch("bob"), b"hi bob")
    b, first = accept_session(bob, init)
    assert first == b"hi bob"
    return alice, bob, a, b, server


def test_x3dh_agrees_and_conversation_works():
    _, _, a, b, _ = pair()
    for i in range(3):
        assert b.receive(*a.send(b"a%d" % i)) == b"a%d" % i
        assert a.receive(*b.send(b"b%d" % i)) == b"b%d" % i
    assert a.ad == b.ad  # both bind the two identity keys, Alice's first
    assert a.DHr == b.DHs.public  # Alice's next message will be read in Bob's current chain


def test_out_of_order_within_a_chain():
    _, _, a, b, _ = pair()
    msgs = [a.send(b"m%d" % i) for i in range(4)]
    for i in (2, 0, 3, 1):
        assert b.receive(*msgs[i]) == b"m%d" % i
    assert b.skipped == {}


def test_out_of_order_across_ratchet_steps():
    _, _, a, b, _ = pair()
    late = b.send(b"late")
    on_time = b.send(b"on time")
    assert a.receive(*on_time) == b"on time"
    assert b.receive(*a.send(b"reply")) == b"reply"  # both sides move to new ratchet keys
    after = b.send(b"after")
    assert a.receive(*after) == b"after"
    assert a.receive(*late) == b"late"  # kept as a skipped key of the old chain
    with pytest.raises(AuthError):
        a.receive(*late)  # each message key is used once


def test_forged_message_is_rejected_and_state_is_kept():
    _, _, a, b, _ = pair()
    header, ct = a.send(b"x")
    bad = ct[:-1] + bytes([ct[-1] ^ 1])
    with pytest.raises(AuthError):
        b.receive(header, bad)
    assert b.receive(header, ct) == b"x"
    fake_header = (KeyPair().public, 0, 0)  # a new ratchet key from an attacker
    with pytest.raises(AuthError):
        b.receive(fake_header, ct)
    assert b.receive(*a.send(b"y")) == b"y"


def test_signed_prekey_substitution_is_detected():
    server, alice, bob = KeyServer(), User("alice"), User("bob")
    server.publish(bob)
    bundle = server.fetch("bob")
    bundle["spk"] = KeyPair().public  # a malicious server swaps the prekey
    with pytest.raises(AuthError):
        start_session(alice, bundle, b"hi")
    # A server that swaps the signing key too is caught only by comparing safety numbers.
    evil_seed = bytes(32)
    bundle = server.fetch("bob")
    bundle["spk"] = KeyPair().public
    bundle["sign"], bundle["sig"] = ed25519_public(evil_seed), ed25519_sign(evil_seed, bundle["spk"])
    start_session(alice, dict(bundle), b"hi")
    with pytest.raises(AuthError):
        start_session(alice, bundle, b"hi", trusted_sign_key=bob.sign_public)


def test_one_time_prekey_is_used_once():
    server, alice, bob = KeyServer(), User("alice"), User("bob")
    server.publish(bob)
    _, init = start_session(alice, server.fetch("bob"), b"once")
    accept_session(bob, init)
    with pytest.raises(AuthError):
        accept_session(bob, init)  # a replayed initial message


def test_forward_secrecy_of_old_messages():
    _, bob, a, b, _ = pair()
    recorded = [a.send(b"secret %d" % i) for i in range(3)]
    for m in recorded:
        b.receive(*m)
    for i in range(3):  # several ratchet steps
        b.receive(*a.send(b"x"))
        a.receive(*b.send(b"y"))
    stolen = steal(b)
    for m in recorded:
        with pytest.raises(AuthError):
            stolen.receive(*m)
    # The long-term keys do not give SK either, because the one-time prekey was deleted.
    assert 0 not in bob.opks


def attacker_reads_sent(shadow, header, ct):
    """With a copy of the sender's state, derive the key of a message in its current sending chain."""
    ck, mk = shadow.CKs, None
    for _ in range(header[2] - shadow.Ns + 1):
        ck, mk = kdf_ck(ck)
    return open_sealed(mk, ct, shadow.ad + encode_header(header))


def test_compromise_then_healing():
    _, _, a, b, _ = pair()
    b.receive(*a.send(b"before"))
    a.receive(*b.send(b"before reply"))
    shadow = steal(a)  # the attacker copies Alice's whole state
    a1 = a.send(b"a1")
    assert attacker_reads_sent(shadow, *a1) == b"a1"
    b.receive(*a1)
    b1 = b.send(b"b1")
    assert shadow.receive(*b1) == b"b1"  # Bob's reply uses Alice's old ratchet key
    assert a.receive(*b1) == b"b1"
    a2 = a.send(b"a2")  # Alice's new ratchet key is unknown to the attacker
    with pytest.raises(AuthError):
        attacker_reads_sent(shadow, *a2)
    b.receive(*a2)
    b2 = b.send(b"b2")
    with pytest.raises(AuthError):
        shadow.receive(*b2)  # healed
    assert a.receive(*b2) == b"b2"


def test_deniability_bob_can_forge_a_session_from_alice():
    alice, bob = User("alice"), User("bob")
    fake = forge_initial_message(bob, alice.ik.public, b"made by bob")
    s, text = accept_session(bob, fake)
    assert text == b"made by bob" and s.ad[:32] == alice.ik.public


def test_x3dh_needs_all_four_values():
    alice, bob = User("alice"), User("bob")
    ek = KeyPair()
    full = x3dh_kdf(dh(alice.ik, bob.spk.public) + dh(ek, bob.ik.public) + dh(ek, bob.spk.public) + dh(ek, bob.opks[0].public))
    without_opk = x3dh_kdf(dh(bob.spk, alice.ik.public) + dh(bob.ik, ek.public) + dh(bob.spk, ek.public))
    assert full != without_opk
