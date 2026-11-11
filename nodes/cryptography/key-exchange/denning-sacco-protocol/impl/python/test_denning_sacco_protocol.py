# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/denning-sacco-protocol/. The authors are listed in prov/X3KF0J.jsonl.

import secrets

from denning_sacco_protocol import (
    abadi_attack,
    initiator_receive,
    pk_message3,
    pk_receive,
    request,
    responder_receive,
    server_reply,
)

WINDOW = 30  # d1 + d2, in seconds


def keys():
    return {b"A": secrets.token_bytes(32), b"B": secrets.token_bytes(32)}


def test_honest_run() -> None:
    ks = keys()
    a, b = request(b"A", b"B")
    msg2 = server_reply(ks, a, b, clock=1000)
    k, ticket = initiator_receive(ks[b"A"], b"B", msg2, clock=1002, window=WINDOW)
    assert responder_receive(ks[b"B"], ticket, clock=1005, window=WINDOW) == (b"A", k)


def test_old_ticket_is_rejected() -> None:
    """The Needham-Schroeder replay fails: the old ticket's timestamp is out of the window."""
    ks = keys()
    msg2 = server_reply(ks, b"A", b"B", clock=1000)
    _, ticket = initiator_receive(ks[b"A"], b"B", msg2, clock=1001, window=WINDOW)
    assert responder_receive(ks[b"B"], ticket, clock=1000 + 86400, window=WINDOW) is None


def test_replay_inside_the_window_is_accepted() -> None:
    """Timestamps alone do not stop a replay within d1 + d2; B must also remember recent tickets."""
    ks = keys()
    msg2 = server_reply(ks, b"A", b"B", clock=1000)
    _, ticket = initiator_receive(ks[b"A"], b"B", msg2, clock=1001, window=WINDOW)
    first = responder_receive(ks[b"B"], ticket, clock=1002, window=WINDOW)
    second = responder_receive(ks[b"B"], ticket, clock=1020, window=WINDOW)
    assert first == second is not None


def test_wrong_peer_is_rejected() -> None:
    ks = keys()
    ks[b"C"] = secrets.token_bytes(32)
    msg2 = server_reply(ks, b"A", b"C", clock=1000)  # an attacker changed B to C in message 1
    assert initiator_receive(ks[b"A"], b"B", msg2, clock=1000, window=WINDOW) is None


def test_public_key_protocol_honest_run() -> None:
    k = secrets.token_bytes(32)
    for fixed in (False, True):
        m3 = pk_message3(b"A", b"B", k, 1000, fixed)
        assert pk_receive(b"B", m3, 1001, WINDOW, fixed) == (b"A", k)


def test_abadi_attack_on_the_public_key_protocol() -> None:
    k = secrets.token_bytes(32)
    m3 = pk_message3(b"A", b"B", k, 1000, fixed=False)
    forged = abadi_attack(m3, b"B", b"C", 1000)
    # C believes it shares K with A; in fact B (dishonest) knows K too.
    assert pk_receive(b"C", forged, 1003, WINDOW, fixed=False) == (b"A", k)


def test_names_in_the_signature_stop_the_attack() -> None:
    k = secrets.token_bytes(32)
    m3 = pk_message3(b"A", b"B", k, 1000, fixed=True)
    forged = abadi_attack(m3, b"B", b"C", 1000)
    assert pk_receive(b"C", forged, 1003, WINDOW, fixed=True) is None
