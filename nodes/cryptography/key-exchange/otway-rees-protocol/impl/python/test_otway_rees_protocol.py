# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/otway-rees-protocol/. The authors are listed in prov/GDNTC9.jsonl.

import secrets

from otway_rees_protocol import Party, Server, type_flaw_attack

A, B = b"alice___", b"bob_____"


def setup(typed: bool):
    k_as, k_bs = secrets.token_bytes(32), secrets.token_bytes(32)
    return Party(A, k_as, typed), Party(B, k_bs, typed), Server({A: k_as, B: k_bs}, typed)


def run(alice, bob, server) -> bool:
    msg3 = server.message3(bob.message2(alice.message1(B)))
    msg4 = bob.message3_received(msg3) if msg3 else None
    return msg4 is not None and alice.message4_received(msg4)


def test_honest_runs() -> None:
    for typed in (False, True):
        alice, bob, server = setup(typed)
        assert run(alice, bob, server)
        assert alice.accepted[0] == B and bob.accepted[0] == A
        assert alice.accepted[1] == bob.accepted[1] and len(alice.accepted[1]) == 32


def test_server_rejects_mismatched_names() -> None:
    alice, bob, server = setup(True)
    m, a, b, box_a, box_b = bob.message2(alice.message1(B))
    assert server.message3((m, b"eve_____", b, box_a, box_b)) is None


def test_type_flaw_attack_without_typing() -> None:
    alice, _, _ = setup(False)
    k = type_flaw_attack(alice, B)
    # Alice accepts M | A | B as the key with Bob: every value is public.
    assert k == alice.m + A + B


def test_type_tags_stop_the_attack() -> None:
    alice, _, _ = setup(True)
    assert type_flaw_attack(alice, B) is None and alice.accepted is None
