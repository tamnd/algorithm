# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/needham-schroeder-protocol/. The authors are listed in prov/9NTM5E.jsonl.

import secrets

from needham_schroeder_protocol import (
    Initiator,
    PkParty,
    Responder,
    Server,
    dec,
    denning_sacco_replay,
    enc,
    lowe_attack,
    run_nssk,
)


def setup(fixed: bool = False):
    k_as, k_bs = secrets.token_bytes(32), secrets.token_bytes(32)
    server = Server({b"A": k_as, b"B": k_bs})
    return server, Initiator(b"A", k_as), Responder(b"B", k_bs, fixed)


def test_toy_cipher_round_trip_and_integrity() -> None:
    k = secrets.token_bytes(32)
    box = enc(k, b"x", b"yz")
    assert dec(k, box) == [b"x", b"yz"]
    assert dec(secrets.token_bytes(32), box) is None
    assert dec(k, box[:-1] + bytes([box[-1] ^ 1])) is None


def test_honest_nssk_run() -> None:
    server, a, b = setup()
    assert run_nssk(server, a, b)
    assert b.accepted == (b"A", a.key)


def test_wrong_nonce_in_reply_is_rejected() -> None:
    server, a, _ = setup()
    a.request(b"B")
    reply = server.handle(b"A", b"B", b"\x00" * 16)  # an old reply for another nonce
    assert a.receive(reply) is None


def test_denning_sacco_replay_with_a_compromised_old_key() -> None:
    server, a, b = setup()
    a.request(b"B")
    old_ticket = a.receive(server.handle(b"A", b"B", a.na))
    old_key = a.key  # this session key leaks later
    b2 = Responder(b"B", b.k_bs)
    assert denning_sacco_replay(b2, old_ticket, old_key)
    assert b2.accepted == (b"A", old_key)  # B believes it shares the old key with A


def test_the_1987_fix_stops_the_replay() -> None:
    server, a, b = setup(fixed=True)
    assert run_nssk(server, a, b)
    old_ticket = enc(b.k_bs, a.key, b"A", b.nb_fix)  # the ticket of that run
    b2 = Responder(b"B", b.k_bs, fixed=True)
    assert not denning_sacco_replay(b2, old_ticket, a.key)


def test_honest_nspk_and_nsl_runs() -> None:
    for fix in (False, True):
        alice, bob = PkParty(b"A", fix), PkParty(b"B", fix)
        m3 = alice.step3(bob.step2(alice.start(b"B")))
        assert bob.finish(m3)
        assert alice.done[1:] == bob.done[1:] and alice.done[0] == b"B" and bob.done[0] == b"A"


def test_lowe_attack_on_nspk() -> None:
    alice, bob = PkParty(b"A"), PkParty(b"B")
    bob_fooled, learned = lowe_attack(alice, bob)
    assert bob_fooled
    assert bob.na in learned and bob.nb in learned  # Eve knows both nonces of Bob's run "with Alice"


def test_lowe_fix_stops_the_attack() -> None:
    alice, bob = PkParty(b"A", lowe_fix=True), PkParty(b"B", lowe_fix=True)
    bob_fooled, learned = lowe_attack(alice, bob)
    assert not bob_fooled and bob.done is None
