# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dining-cryptographers/. The authors are listed in prov/1FPAEV.jsonl.
#
# DC-nets have no official test vectors. The tests check the output of a
# round, and check anonymity exactly by enumerating every value of every
# key in small cases with 1-bit messages.

import secrets

from dining_cryptographers import (
    KeyGraph,
    dc_round,
    honest_connected,
    send_bytes,
    share_keys,
    view_distribution,
)


def test_the_broadcast_reveals_the_message():
    msg = b"pay the bill"
    for g in (KeyGraph.complete(3), KeyGraph.ring(5), KeyGraph.complete(6)):
        for sender in range(g.n):
            _, out = send_bytes(g, sender, msg)
            assert out == msg


def test_a_round_without_a_sender_gives_zero():
    g = KeyGraph.complete(4)
    _, out = dc_round(g, share_keys(g, 64), {})
    assert out == 0


def test_two_senders_collide():
    g = KeyGraph.complete(4)
    m1, m2 = secrets.randbits(64), secrets.randbits(64)
    _, out = dc_round(g, share_keys(g, 64), {1: m1, 3: m2})
    assert out == m1 ^ m2


def test_three_cryptographers_view_is_the_same_whoever_paid():
    # Chaum's dinner: three diners on a triangle, 1-bit coins, a 1-bit message.
    g = KeyGraph.complete(3)
    me = frozenset({0})
    assert view_distribution(g, me, {1: 1}) == view_distribution(g, me, {2: 1})
    # An outside observer cannot tell any of the three apart.
    nobody = frozenset()
    d = [view_distribution(g, nobody, {s: 1}) for s in range(3)]
    assert d[0] == d[1] == d[2]
    # But a round with no payer looks different: the bits XOR to 0.
    assert view_distribution(g, me, {}) != view_distribution(g, me, {1: 1})


def test_connected_honest_subgraph_hides_the_sender():
    g = KeyGraph(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 4)])
    coalition = frozenset({0, 3})
    assert honest_connected(g, coalition)
    dists = [view_distribution(g, coalition, {s: 1}) for s in (1, 2, 4, 5)]
    assert all(d == dists[0] for d in dists)


def test_disconnected_honest_subgraph_reveals_the_side():
    g = KeyGraph.ring(6)  # without the chord, removing 0 and 3 cuts {1, 2} from {4, 5}
    coalition = frozenset({0, 3})
    assert not honest_connected(g, coalition)
    d1, d2, d4 = (view_distribution(g, coalition, {s: 1}) for s in (1, 2, 4))
    assert d1 == d2  # the sender is hidden inside its component
    assert not set(d1) & set(d4)  # but the component is known for sure


def test_a_dishonest_middle_party_on_a_path_finds_the_sender():
    g = KeyGraph(3, [(1, 0), (0, 2)])
    coalition = frozenset({0})
    d1, d2 = view_distribution(g, coalition, {1: 1}), view_distribution(g, coalition, {2: 1})
    assert not set(d1) & set(d2)


def test_a_jammer_destroys_the_round_undetected():
    g = KeyGraph.complete(5)
    m = secrets.randbits(64) | 1
    junk = secrets.randbits(64) | 2
    ann, out = dc_round(g, share_keys(g, 64), {0: m}, jam={3: junk})
    assert out == m ^ junk != m
    # The sender sees that the round failed, but its view is the same whichever party jammed.
    small = KeyGraph.complete(4)
    me = frozenset({0})
    views = [view_distribution(small, me, {0: 1}, jam={j: 1}) for j in (1, 2, 3)]
    assert views[0] == views[1] == views[2]
