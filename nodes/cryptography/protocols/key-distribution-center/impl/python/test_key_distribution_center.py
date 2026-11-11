# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-distribution-center/. The authors are listed in prov/ZVT3WS.jsonl.
#
# No official test vectors exist for a generic KDC. The tests check the key
# and message counts against the formulas n and n(n-1)/2, and the behaviour of
# the toy flow.

import random

import pytest

from key_distribution_center import (
    AuthError,
    accept_ticket,
    build_kdc_network,
    build_pairwise_network,
    cost_table,
    dec_json,
    enc_json,
    kdc_session,
    open_sealed,
    read_recorded_ticket,
    seal,
)


@pytest.mark.parametrize("n", [2, 3, 5, 10, 20])
def test_key_counts(n):
    t = cost_table(n, sessions=7)
    assert t["kdc"]["keys_total"] == n
    assert t["kdc"]["keys_per_user"] == 1
    assert t["pairwise"]["keys_total"] == n * (n - 1) // 2
    assert t["pairwise"]["keys_per_user"] == n - 1
    assert t["kdc"]["messages"] == 3 * 7
    assert t["pairwise"]["messages"] == 0


def test_adding_a_user():
    n = 10
    before = build_pairwise_network(n)
    after = build_pairwise_network(n + 1)
    added = len({k for u in after for k in u.long_term.values()}) - len({k for u in before for k in u.long_term.values()})
    assert added == n
    kdc, _ = build_kdc_network(n)
    size = len(kdc.long_term)
    kdc.register("new")
    assert len(kdc.long_term) - size == 1


def test_session_key_agreed_and_fresh():
    kdc, users = build_kdc_network(4)
    rng = random.Random(7)
    seen = set()
    for i in range(30):
        a, b = rng.sample(users, 2)
        k = kdc_session(kdc, a, b, now=100 + i)
        assert a.sessions[b.name] == b.sessions[a.name] == k
        assert k not in seen
        seen.add(k)


def test_aead_rejects_changes():
    k = b"k" * 32
    box = seal(k, b"hello", b"ad")
    assert open_sealed(k, box, b"ad") == b"hello"
    bad = box[:-1] + bytes([box[-1] ^ 1])
    with pytest.raises(AuthError):
        open_sealed(k, bad, b"ad")
    with pytest.raises(AuthError):
        open_sealed(k, box, b"other")
    with pytest.raises(AuthError):
        open_sealed(b"x" * 32, box, b"ad")


def test_reply_bound_to_nonce_and_peer():
    kdc, users = build_kdc_network(3)
    a, b, c = users
    old_reply, _ = kdc.request(a.name, b.name, "n-old", now=10)
    # An attacker replays an old reply to a new request: the nonce does not match.
    r = dec_json(a.long_term["KDC"], old_reply)
    assert r["nonce"] == "n-old" and r["nonce"] != "n-new"
    # A reply made for the pair (A, C) names C, so A sees that it is not for B.
    other, _ = kdc.request(a.name, c.name, "n-x", now=10)
    assert dec_json(a.long_term["KDC"], other)["peer"] == c.name


def test_ticket_expiry_and_sender_name():
    kdc, users = build_kdc_network(3)
    a, b, c = users
    _, ticket = kdc.request(a.name, b.name, "n", now=0, lifetime=60)
    assert len(accept_ticket(b, a.name, ticket, now=60)) == 32
    with pytest.raises(AuthError):
        accept_ticket(b, a.name, ticket, now=61)  # expired
    with pytest.raises(AuthError):
        accept_ticket(b, c.name, ticket, now=10)  # C shows A's ticket as its own
    with pytest.raises(AuthError):
        accept_ticket(c, a.name, ticket, now=10)  # a ticket for B does not open at C
    # A ticket that someone other than the KDC made fails the tag check.
    fake = enc_json(b"z" * 32, {"key": "00" * 32, "peer": a.name, "expiry": 99})
    with pytest.raises(AuthError):
        accept_ticket(b, a.name, fake, now=10)


def test_single_point_of_trust():
    kdc, users = build_kdc_network(5)
    recorded = []
    for i in range(10):
        a, b = users[i % 5], users[(i + 2) % 5]
        nonce = f"n{i}"
        reply, ticket = kdc.request(a.name, b.name, nonce, now=i)
        key = bytes.fromhex(dec_json(a.long_term["KDC"], reply)["key"])
        recorded.append((b.name, ticket, key))
    stolen = dict(kdc.long_term)
    for receiver, ticket, key in recorded:
        assert read_recorded_ticket(stolen, receiver, ticket) == key
    # Without the database, an outsider learns nothing from the same tickets.
    assert all(read_recorded_ticket({}, r, t) is None for r, t, _ in recorded)


def test_single_point_of_failure():
    kdc, users = build_kdc_network(3)
    kdc.up = False
    with pytest.raises(ConnectionError):
        kdc_session(kdc, users[0], users[1], now=5)
    pair = build_pairwise_network(3)
    assert pair[0].long_term["U1"] == pair[1].long_term["U0"]  # pairwise keys still work
