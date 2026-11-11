# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shamir-three-pass-protocol/. The authors are listed in prov/76HQ6M.jsonl.

import random

import pytest

from shamir_three_pass_protocol import P, legendre, lock, make_lock, three_pass, xor_eavesdrop, xor_three_pass


def test_round_trip() -> None:
    rng = random.Random(1981)
    for _ in range(2):
        alice, bob = make_lock(rng=rng), make_lock(rng=rng)
        m = rng.randrange(2, P - 1)
        wire, out = three_pass(m, alice, bob)
        assert out == m
        assert m not in wire


def test_locks_are_units_and_commute() -> None:
    rng = random.Random(1986)
    a, a_inv = make_lock(rng=rng)
    b, _ = make_lock(rng=rng)
    assert a * a_inv % (P - 1) == 1
    assert a % 2 == 1  # p - 1 is even, so every lock is odd
    x = rng.randrange(2, P - 1)
    assert lock(lock(x, a), b) == lock(lock(x, b), a)
    assert lock(lock(x, a), a_inv) == x


def test_round_trip_with_a_small_prime() -> None:
    p = 1019  # a toy safe prime, 2 * 509 + 1
    rng = random.Random(7)
    for m in range(2, p - 1):
        alice, bob = make_lock(p, rng), make_lock(p, rng)
        assert three_pass(m, alice, bob, p)[1] == m


def test_message_range() -> None:
    rng = random.Random(3)
    alice, bob = make_lock(rng=rng), make_lock(rng=rng)
    for m in (0, 1, P - 1, P):
        with pytest.raises(ValueError):
            three_pass(m, alice, bob)


def test_legendre_symbol_leaks_one_bit() -> None:
    # Every lock is odd, so (m^a | p) = (m | p)^a = (m | p): each message on
    # the wire shows whether m is a square mod p.
    rng = random.Random(5)
    alice, bob = make_lock(rng=rng), make_lock(rng=rng)
    m = rng.randrange(2, P - 1)
    wire, _ = three_pass(m, alice, bob)
    assert all(legendre(c) == legendre(m) for c in wire)
    # The same holds for every message on a toy safe prime.
    p = 1019
    for m in range(2, p - 1):
        alice, bob = make_lock(p, rng), make_lock(p, rng)
        wire, _ = three_pass(m, alice, bob, p)
        assert all(legendre(c, p) == legendre(m, p) for c in wire)


def test_no_authentication_means_anyone_can_play_bob() -> None:
    rng = random.Random(6)
    alice = make_lock(rng=rng)
    mallory = make_lock(rng=rng)
    m = rng.randrange(2, P - 1)
    # Mallory answers Alice's first message with her own lock and so ends
    # with m, as Bob would.
    a, a_inv = alice
    c1 = lock(m, a)
    c2 = lock(c1, mallory[0])
    c3 = lock(c2, a_inv)
    assert lock(c3, mallory[1]) == m


def test_xor_version_round_trips_but_leaks_m() -> None:
    rng = random.Random(1980)
    m = b"attack at dawn!!"
    ka, kb = rng.randbytes(len(m)), rng.randbytes(len(m))
    wire = xor_three_pass(m, ka, kb)
    c1, c2, c3 = wire
    # Bob can unlock: c3 ^ kb = m.
    assert bytes(x ^ y for x, y in zip(c3, kb)) == m
    # But so can anyone who sees the three messages.
    assert xor_eavesdrop(wire) == m
