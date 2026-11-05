# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fnv-hash/. The authors are listed in prov/GWRZNB.jsonl.

import collections
import itertools
import random

from fnv_hash import OFFSET, PRIME, fnv1, fnv1a, xor_fold

STRINGS = [b"", b"a", b"foobar", b"Hello!\x01\xff\xed"]


def oracle_1a(b: bytes, bits: int) -> int:
    # Unbounded integers, one reduction at the end: the low bits of XOR and of
    # products depend only on the low bits of the operands.
    h = OFFSET[bits]
    for x in b:
        h = (h ^ x) * PRIME[bits]
    return h % (1 << bits)


def test_rfc9923_vectors() -> None:
    assert [fnv1a(s, 32) for s in STRINGS] == [0x811C9DC5, 0xE40C292C, 0xBF9CF968, 0xFD9D3881]
    assert [fnv1a(s + b"\0", 32) for s in STRINGS] == [0x050C5D1F, 0x2B24D044, 0x0C1C9EB8, 0xBF7FF313]
    assert [fnv1a(s, 64) for s in STRINGS] == [
        0xCBF29CE484222325, 0xAF63DC4C8601EC8C, 0x85944171F73967E8, 0xBD51EA7094EE6FA1
    ]
    assert [fnv1a(s + b"\0", 64) for s in STRINGS] == [
        0xAF63BD4C8601B7DF, 0x089BE207B544F1E4, 0x34531CA7168B8F38, 0xA0A0FE4D1127AE93
    ]


def test_offset_basis_is_fnv0_of_signature() -> None:
    sig = b"chongo <Landon Curt Noll> /\\../\\"
    assert len(sig) == 32
    for bits in (32, 64):
        assert fnv1(sig, bits, offset=0) == OFFSET[bits]


def test_trace_foobar() -> None:
    states = [fnv1a(b"foobar"[:i]) for i in range(7)]
    assert states == [0x811C9DC5, 0xE30C2799, 0x6222E842, 0xA9F37ED7, 0x3F5076EF, 0x39AAA18A, 0xBF9CF968]


def test_known_collisions() -> None:
    assert fnv1a("costarring") == fnv1a("liquid") == 0x5E4DAA9D
    assert fnv1a("declinate") == fnv1a("macallums")
    assert fnv1a("altarage") == fnv1a("zinke")
    assert fnv1a("altarages") == fnv1a("zinkes")
    assert fnv1("creamwove") == fnv1("quists")
    assert fnv1a("creamwove") != fnv1a("quists")


def test_low_bits() -> None:
    # Bit 0 is the parity of the low bits of all bytes, XOR bit 0 of the offset.
    rng = random.Random(1)
    for _ in range(500):
        b = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 20)))
        par = (OFFSET[32] & 1) ^ (sum(x & 1 for x in b) & 1)
        assert fnv1a(b) & 1 == par
    # a = 0x61 and q = 0x71 agree modulo 16, so the low 4 bits depend only on the length.
    keys = ["".join(t) for t in itertools.product("aq", repeat=6)]
    assert collections.Counter(fnv1a(k) & 15 for k in keys) == {11: 64}
    assert max(collections.Counter(xor_fold(fnv1a(k), 4) for k in keys).values()) == 6


def random_string(rng: random.Random, alphabet: bytes) -> bytes:
    n = rng.randrange(0, 30)
    if rng.random() < 0.3 and n:
        unit = bytes(rng.choice(alphabet) for _ in range(rng.randrange(1, 4)))
        return (unit * n)[:n]
    return bytes(rng.choice(alphabet) for _ in range(n))


def test_random_against_oracle_and_structure() -> None:
    rng = random.Random(20261106)
    for alphabet in (b"a", b"ab", b"abcd"):
        for _ in range(400):
            x = random_string(rng, alphabet)
            for bits in (32, 64):
                assert fnv1a(x, bits) == oracle_1a(x, bits)
                assert fnv1a(x.decode(), bits) == fnv1a(x, bits)
            # Two strings of one length that differ in exactly one byte never collide.
            if x:
                i = rng.randrange(len(x))
                y = bytearray(x)
                y[i] = rng.choice([c for c in b"abcd" if c != x[i]])
                assert fnv1a(x) != fnv1a(bytes(y))
                assert fnv1(x) != fnv1(bytes(y))
            # Prefix and suffix structure: h(uz) is determined by h(u) and z.
            z = random_string(rng, alphabet)
            assert fnv1a(x + z) == fnv1a(z, offset=fnv1a(x))
            assert fnv1a(x + z, 64) == fnv1a(z, 64, offset=fnv1a(x, 64))


def test_suffix_map_is_injective() -> None:
    # For a fixed suffix z, distinct states stay distinct, so h(uz) = h(vz) iff h(u) = h(v).
    rng = random.Random(5)
    for _ in range(300):
        z = random_string(rng, b"abcd")
        s1, s2 = rng.randrange(1 << 32), rng.randrange(1 << 32)
        if s1 != s2:
            assert fnv1a(z, offset=s1) != fnv1a(z, offset=s2)


def test_sticky_zero_state() -> None:
    # From the state 0, zero bytes keep the state at 0 (the "sticky state" of RFC 9923, Section 1.4).
    for k in range(5):
        assert fnv1a(b"\0" * k, offset=0) == 0
