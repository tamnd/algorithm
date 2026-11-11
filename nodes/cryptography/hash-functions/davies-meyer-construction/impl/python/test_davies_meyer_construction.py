# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davies-meyer-construction/. The authors are listed in prov/MYQDY5.jsonl.

from davies_meyer_construction import (
    brs_collision_bound,
    collision_search,
    davies_meyer,
    decrypt,
    encrypt,
    fixed_point,
    no_feed_forward,
    preimage_without_feed_forward,
)


def test_toy_cipher_is_a_permutation() -> None:
    # decrypt inverts encrypt, so each E_k is injective, hence a permutation of 16-bit values.
    for k in (0, 0x1234, 0xFFFF):
        assert all(decrypt(k, encrypt(k, x)) == x for x in range(0, 1 << 16, 37))


def test_fixed_point_for_every_block() -> None:
    # One decryption per block gives a fixed point; a random function would need about 2^16 tries.
    for m in range(0, 1 << 16, 4099):
        h = fixed_point(m)
        assert davies_meyer(h, m) == h


def test_fixed_point_expands_messages() -> None:
    # If the chain reaches h = E_m^(-1)(0), the block m can be repeated with no effect on the chain.
    m = 0xBEEF
    h = fixed_point(m)
    x = h
    for _ in range(5):
        x = davies_meyer(x, m)
    assert x == h


def test_feed_forward_is_needed() -> None:
    target = 0x0F0F
    for m in (1, 2, 3, 0xABCD):
        h = preimage_without_feed_forward(target, m)
        assert no_feed_forward(h, m) == target
    # With the feed-forward, the same trick does not give the target.
    assert davies_meyer(preimage_without_feed_forward(target, 7), 7) != target


def test_birthday_collision_within_bound_scale() -> None:
    # On 16 bits the BRS bound reaches 1/2 near q = 181; the search finds a collision near there.
    found = []
    for h in (0x0000, 0x1111, 0x2222, 0x3333):
        m1, m2, q = collision_search(h)
        assert m1 != m2 and davies_meyer(h, m1) == davies_meyer(h, m2)
        found.append(q)
    assert max(found) < 2000
    assert brs_collision_bound(181) < 0.51 and brs_collision_bound(1 << 8) == 1.0
