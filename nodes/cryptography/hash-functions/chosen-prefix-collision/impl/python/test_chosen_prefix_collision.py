# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chosen-prefix-collision/. The authors are listed in prov/41PGVW.jsonl.

import random

from chosen_prefix_collision import (
    IV,
    chain,
    chosen_prefix_collision,
    near_collision_block,
    toy_compress,
    toy_hash,
)


def blocks(text: bytes) -> list[int]:
    text += b"\x00" * (-len(text) % 4)
    return [int.from_bytes(text[i : i + 4], "big") for i in range(0, len(text), 4)]


def test_two_different_prefixes_collide() -> None:
    p1 = blocks(b"Certificate: CN=good.example ")
    p2 = blocks(b"Certificate: CN=evil.example ")
    assert p1 != p2 and len(p1) == len(p2)
    s1, s2, calls = chosen_prefix_collision(p1, p2)
    m1, m2 = p1 + s1, p2 + s2
    assert m1 != m2
    assert toy_hash(m1) == toy_hash(m2)
    # a common suffix keeps the collision
    tail = blocks(b"valid until 2030")
    assert toy_hash(m1 + tail) == toy_hash(m2 + tail)
    # the cost is near the 24-bit birthday, about 2^13 calls, not the 2^16 of a generic 32-bit attack
    assert calls < 1 << 15
    assert len(s1) <= 5


def test_many_random_prefixes() -> None:
    rng = random.Random(2007)
    for _ in range(20):
        size = rng.randrange(1, 6)
        p1 = [rng.getrandbits(32) for _ in range(size)]
        p2 = [rng.getrandbits(32) for _ in range(size)]
        s1, s2, _ = chosen_prefix_collision(p1, p2)
        assert toy_hash(p1 + s1) == toy_hash(p2 + s2)


def test_near_collision_block_clears_a_window() -> None:
    rng = random.Random(3)
    for _ in range(500):
        u = rng.getrandbits(24)
        t1, t2 = rng.getrandbits(8), rng.getrandbits(8)
        if t1 == t2:
            continue
        h1, h2 = (t1 << 24) | u, (t2 << 24) | u
        b1, b2, g1, g2, _ = near_collision_block(h1, h2)
        assert g1 == toy_compress(h1, b1) and g2 == toy_compress(h2, b2)
        assert g1 & 0xFFFFFF == g2 & 0xFFFFFF
        before = bin(t1 ^ t2).count("1")
        after = bin((g1 ^ g2) >> 24).count("1")
        assert after < before


def test_identical_prefix_is_the_easy_case() -> None:
    # with one prefix the states are equal; one block pair with a difference in c
    # makes a difference, and one near-collision block removes it
    p = blocks(b"same prefix!")
    h = chain(IV, p)
    h1, h2 = toy_compress(h, 0x00000005), toy_compress(h, 0x01000005)
    assert h1 != h2 and h1 & 0xFFFFFF == h2 & 0xFFFFFF
    b1, b2, g1, g2, _ = near_collision_block(h1, h2)
    assert g1 == g2
    assert toy_hash(p + [0x00000005, b1]) == toy_hash(p + [0x01000005, b2])


def test_unequal_lengths_rejected() -> None:
    try:
        chosen_prefix_collision([1], [1, 2])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
