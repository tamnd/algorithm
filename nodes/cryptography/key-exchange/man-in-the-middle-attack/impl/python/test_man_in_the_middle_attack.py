# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/man-in-the-middle-attack/. The authors are listed in prov/0ZCK64.jsonl.

import random

import pytest

from man_in_the_middle_attack import (
    G,
    P,
    Q,
    Mallory,
    Network,
    sas,
    schnorr_keygen,
    schnorr_sign,
    schnorr_verify,
    send_message,
    signed_dh,
    unauthenticated_dh,
)


def test_toy_group() -> None:
    assert P == 2 * Q + 1
    assert pow(G, Q, P) == 1


def test_honest_network_gives_one_key() -> None:
    rng = random.Random(1)
    net = Network()
    ka, kb = unauthenticated_dh(net, rng)
    assert ka == kb
    assert send_message(net, ka, kb, b"hello Bob, from Alice", 1) == b"hello Bob, from Alice"


def test_mallory_shares_a_key_with_each_side_and_reads_and_changes_traffic() -> None:
    rng = random.Random(2)
    mallory = Mallory(rng)
    net = Network(hook=mallory.hook)
    ka, kb = unauthenticated_dh(net, rng)
    assert ka != kb
    assert mallory.key_alice == ka
    assert mallory.key_bob == kb
    got = send_message(net, ka, kb, b"pay 10 to Alice", 7)
    assert mallory.read == [b"pay 10 to Alice"]
    assert got == b"pay 10 to Mallory"  # Bob decrypts without error and sees the change


def test_sas_comparison_detects_mallory() -> None:
    rng = random.Random(3)
    ka, kb = unauthenticated_dh(Network(), rng)
    assert sas(ka) == sas(kb)
    detected = 0
    for seed in range(20):
        r = random.Random(100 + seed)
        mallory = Mallory(r)
        ka, kb = unauthenticated_dh(Network(hook=mallory.hook), r)
        detected += sas(ka) != sas(kb)
    assert detected == 20  # a 20-bit SAS misses with chance about 2^-20 per run


def test_schnorr_toy_signature() -> None:
    rng = random.Random(4)
    s, y = schnorr_keygen(rng)
    sig = schnorr_sign(s, b"m", rng)
    assert schnorr_verify(y, b"m", sig)
    assert not schnorr_verify(y, b"n", sig)


def test_signature_on_the_exchange_detects_mallory() -> None:
    rng = random.Random(5)
    bob = schnorr_keygen(rng)
    ka, kb = signed_dh(Network(), bob, rng)
    assert ka == kb
    mallory = Mallory(rng)
    with pytest.raises(ValueError):
        signed_dh(Network(hook=mallory.hook), bob, rng)
