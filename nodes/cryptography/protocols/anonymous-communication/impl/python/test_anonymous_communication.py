# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anonymous-communication/. The authors are listed in prov/5V20J4.jsonl.
#
# Onion routing has no official test vectors for a toy network like this one.
# The X25519 copy is checked with RFC 7748 Section 5.2, copied by hand. The
# other tests check what each relay sees, and run a timing correlation attack
# against simulated local parties only.

import random

import pytest

from anonymous_communication import (
    BASE_U,
    AuthError,
    Cell,
    Client,
    Destination,
    Network,
    Relay,
    timing_experiment,
    x25519,
)


def test_rfc7748_x25519():
    k = bytes.fromhex("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
    u = bytes.fromhex("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
    assert x25519(k, u) == bytes.fromhex("c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552")
    assert len(x25519(bytes(32), BASE_U)) == 32


def one_circuit():
    net = Network(random.Random(7))
    guard, middle, exit_ = Relay("guard"), Relay("middle"), Relay("exit")
    alice, site = Client("alice"), Destination("site", echo=True)
    net.add(guard, middle, exit_, alice, site)
    circ = alice.build(net, [guard, middle, exit_], 0.0)
    secret = b"GET /secret-page"
    alice.send(net, circ, "site", secret, 1.0)
    net.run()
    return net, (guard, middle, exit_), alice, site, secret


def test_message_and_reply_cross_the_circuit():
    net, _, alice, site, secret = one_circuit()
    assert [(src, data) for _, src, data in site.received] == [("exit", secret)]
    assert [data for _, data in alice.replies] == [b"re: " + secret]


def test_each_relay_sees_only_its_neighbors():
    net, (guard, middle, exit_), alice, site, _ = one_circuit()
    assert [h.seen for h in guard.hops] == [{"alice", "middle"}]
    assert [h.seen for h in middle.hops] == [{"guard", "exit"}]
    assert [h.seen for h in exit_.hops] == [{"middle", "site"}]
    # The destination sees only the exit.
    assert {src for _, src, _ in site.received} == {"exit"}


def test_only_the_exit_link_carries_the_plaintext():
    net, _, _, _, secret = one_circuit()
    for e in net.log:
        inside = (e.src, e.dst) in {("exit", "site"), ("site", "exit")}
        assert (secret in e.payload) == inside


def test_circuit_ids_differ_on_each_link():
    net = Network(random.Random(3))
    relays = [Relay("r0"), Relay("r1"), Relay("r2")]
    alice = Client("alice")
    site = Destination("site")
    net.add(*relays, alice, site)
    circ = alice.build(net, relays, 0.0)
    net.run()
    assert relays[0].hops[0].prev_id == circ.circ_id
    ids = [relays[0].hops[0].next_id, relays[1].hops[0].next_id]
    assert circ.circ_id not in ids and ids[0] != ids[1]


def test_a_changed_cell_is_rejected():
    net = Network(random.Random(5))
    guard, middle, exit_ = Relay("guard"), Relay("middle"), Relay("exit")
    alice = Client("alice")
    net.add(guard, middle, exit_, alice, Destination("site"))
    circ = alice.build(net, [guard, middle, exit_], 0.0)
    net.run()
    alice.send(net, circ, "site", b"hello", 1.0)
    _, _, src, dst, cell = net.queue.pop()
    bad = Cell(cell.circ_id, cell.kind, bytes([cell.payload[0] ^ 1]) + cell.payload[1:])
    with pytest.raises(AuthError):
        guard.receive(net, 1.1, src, bad)


def test_timing_correlation_breaks_a_low_latency_network():
    n = 16
    success = timing_experiment(n_clients=n, hold_mean=0.0, seed=1)
    assert success >= 0.9  # chance is 1/16


def test_long_random_delays_defeat_the_same_attack():
    n = 16
    success = timing_experiment(n_clients=n, hold_mean=1.0, seed=1)
    assert success <= 0.35
