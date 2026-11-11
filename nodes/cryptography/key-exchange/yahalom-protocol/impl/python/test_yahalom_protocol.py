# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yahalom-protocol/. The authors are listed in prov/00SN4E.jsonl.

import secrets

from yahalom_protocol import Initiator, Responder, Server, dec, enc, run


def setup():
    k_as, k_bs = secrets.token_bytes(32), secrets.token_bytes(32)
    return Initiator(b"A", k_as), Responder(b"B", k_bs), Server({b"A": k_as, b"B": k_bs})


def test_honest_run() -> None:
    a, b, s = setup()
    assert run(a, b, s)
    assert a.accepted[0] == b"B" and b.accepted[0] == b"A" and a.accepted[1] == b.accepted[1]


def test_initiator_rejects_a_reply_for_another_nonce() -> None:
    a, b, s = setup()
    a.message1(b"B")
    msg3 = s.message3(b.message2((b"A", b"\x00" * 16)))  # the server answered another request
    assert a.message4(msg3) is None


def test_old_ticket_and_old_key_do_not_pass_without_the_new_nonce() -> None:
    """The Needham-Schroeder replay fails here: Eve has an old ticket and its key, but not B's new Nb."""
    a, b, s = setup()
    old_ticket = s.message3(b.message2(a.message1(b"B")))[1]  # a ticket that Eve recorded ...
    old_k = dec(b.k_bs, old_ticket)[1]  # ... whose key she later learned
    b.message2((b"A", secrets.token_bytes(16)))  # Eve starts a new run with B as A
    guess = secrets.token_bytes(16)
    assert not b.finish((old_ticket, enc(old_k, guess)))


def test_secrecy_of_nb_depends_on_k() -> None:
    """If the session key of a run leaks, the eavesdropper also learns Nb of that run (Paulson, 2001)."""
    a, b, s = setup()
    msg3 = s.message3(b.message2(a.message1(b"B")))
    ticket, proof = a.message4(msg3)
    assert b.finish((ticket, proof))
    leaked_k = a.accepted[1]
    assert dec(leaked_k, proof) == [b.nb]


def test_tampered_ticket_is_rejected() -> None:
    a, b, s = setup()
    msg3 = s.message3(b.message2(a.message1(b"B")))
    ticket, proof = a.message4(msg3)
    bad = ticket[:20] + bytes([ticket[20] ^ 1]) + ticket[21:]
    assert not b.finish((bad, proof))
