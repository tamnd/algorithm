# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sponge-construction/. The authors are listed in prov/12K42P.jsonl.

import hashlib

from sponge_construction import Sponge, inner_collision_attack, shake128_sponge, toy_permutation

MSG = bytes((7 * i + 1) & 255 for i in range(400))


def test_nist_shake128_empty() -> None:
    # NIST, Example Values, SHAKE128_Msg0.pdf: the first 32 output bytes.
    s = shake128_sponge()
    want = "7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26"
    assert s.squeeze(32).hex() == want


def test_absorb_split_at_every_boundary() -> None:
    # Absorbing in two pieces gives the same output for every split point, across the
    # block boundaries at 168 and 336 bytes and next to them.
    want = hashlib.shake_128(MSG[:340]).digest(40)
    for cut in (0, 1, 100, 167, 168, 169, 200, 335, 336, 337, 340):
        s = shake128_sponge()
        s.absorb(MSG[:cut])
        s.absorb(MSG[cut:340])
        assert s.squeeze(40) == want, cut


def test_absorb_byte_by_byte() -> None:
    s = shake128_sponge()
    for b in MSG[:170]:
        s.absorb(bytes([b]))
    assert s.squeeze(16) == hashlib.shake_128(MSG[:170]).digest(16)


def test_squeeze_in_pieces_across_blocks() -> None:
    whole = hashlib.shake_128(b"squeeze").digest(400)
    for sizes in ((1,) * 400, (167, 1, 1, 231), (168, 168, 64), (169, 231), (400,)):
        s = shake128_sponge()
        s.absorb(b"squeeze")
        got = b"".join(s.squeeze(k) for k in sizes)
        assert got == whole, sizes


def test_lengths_at_rate_boundaries() -> None:
    # The padding takes one byte (0x1F | 0x80 = 0x9F) when 167 bytes remain, and a new block at 168.
    for n in (166, 167, 168, 169, 335, 336):
        s = shake128_sponge()
        s.absorb(MSG[:n])
        assert s.squeeze(24) == hashlib.shake_128(MSG[:n]).digest(24), n


def test_inner_collision_on_toy_sponge() -> None:
    perm = toy_permutation()
    m1, m2, tries = inner_collision_attack(perm)
    assert m1 != m2 and len(m1) == len(m2)
    assert tries < 200  # about 2^(c/2) = 2^4 for c = 8 bits
    # Same full state, so every common suffix gives the same output.
    for suffix in (b"", b"x", b"any suffix"):
        a, b = Sponge(perm, 2, 1), Sponge(perm, 2, 1)
        a.absorb(m1 + suffix)
        b.absorb(m2 + suffix)
        assert a.squeeze(8) == b.squeeze(8)
