# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miyaguchi-preneel-construction/. The authors are listed in prov/A2T8E9.jsonl.

from miyaguchi_preneel_construction import (
    decrypt,
    encrypt,
    g_fixed,
    iterate,
    mmo,
    mp,
    mp_fixed_points,
)


def test_cipher_inverts() -> None:
    for k in (0, 0x7777):
        assert all(decrypt(k, encrypt(k, x)) == x for x in range(0, 1 << 16, 53))


def test_mp_is_mmo_plus_chaining_value() -> None:
    for h in range(0, 1 << 16, 4111):
        for m in range(0, 1 << 16, 3001):
            assert mp(h, m) == mmo(h, m) ^ h


def test_mmo_g_collisions() -> None:
    # With g_fixed, chaining values that differ only in bits 0 and 1 give the same key.
    # MMO ignores h beyond the key, so they collide for every block; MP still tells them apart.
    h1, h2 = 0x1230, 0x1233
    assert g_fixed(h1) == g_fixed(h2)
    for m in (0, 1, 0xFFFF):
        assert mmo(h1, m, g_fixed) == mmo(h2, m, g_fixed)
        assert mp(h1, m, g_fixed) != mp(h2, m, g_fixed)


def test_fixed_points_need_a_search() -> None:
    # A fixed point of MP at h is a fixed point of the permutation E_h: on average one per key,
    # found only by trying all 2^16 blocks, unlike Davies-Meyer where one decryption suffices.
    total = 0
    for h in (0x0001, 0x0BAD, 0xC0DE):
        pts = mp_fixed_points(h)
        for m in pts:
            assert mp(h, m) == h
        total += len(pts)
    assert total <= 12


def test_iteration() -> None:
    blocks = [0x6162, 0x6380]
    h = 0
    for m in blocks:
        h = mp(h, m)
    assert iterate(mp, 0, blocks) == h
