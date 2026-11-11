# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xxhash/. The authors are listed in prov/SK12VS.jsonl.

import random

import pytest

from xxhash import M32, P32_3, P32_4, P32_5, canonical32, canonical64, xxh32, xxh64

PRIME32 = 2654435761
PRIME64 = 11400714785074694797


def sanity_buffer(n: int) -> bytes:
    """XSUM_fillTestBuffer of cli/xsum_sanity_check.c in the xxHash repository."""
    gen, out = PRIME32, bytearray()
    for _ in range(n):
        out.append(gen >> 56)
        gen = (gen * PRIME64) & ((1 << 64) - 1)
    return bytes(out)


# cli/xsum_sanity_check.c, the tables XSUM_XXH32_testdata and XSUM_XXH64_testdata:
# (input length, seed, result).
XXH32_DATA = [
    (0, 0, 0x02CC5D05), (0, PRIME32, 0x36B78AE7), (1, 0, 0xCF65B03E), (1, PRIME32, 0xB4545AA4),
    (14, 0, 0x1208E7E2), (14, PRIME32, 0x6AF1D1FE), (222, 0, 0x5BD11DBD), (222, PRIME32, 0x58803C5F),
]
XXH64_DATA = [
    (0, 0, 0xEF46DB3751D8E999), (0, PRIME32, 0xAC75FDA2929B17EF), (1, 0, 0xE934A84ADB052768),
    (1, PRIME32, 0x5014607643A9B4C3), (4, 0, 0x9136A0DCA57457EE), (14, 0, 0x8282DCC4994E35C8),
    (14, PRIME32, 0xC3BD6BF63DEB6DF0), (222, 0, 0xB641AE8CB691C174), (222, PRIME32, 0x20CB8AB7AE10C14A),
]


@pytest.mark.parametrize("n,seed,want", XXH32_DATA)
def test_xxh32_sanity_vectors(n: int, seed: int, want: int) -> None:
    assert xxh32(sanity_buffer(n), seed) == want


@pytest.mark.parametrize("n,seed,want", XXH64_DATA)
def test_xxh64_sanity_vectors(n: int, seed: int, want: int) -> None:
    assert xxh64(sanity_buffer(n), seed) == want


def test_canonical_form_is_big_endian() -> None:
    assert canonical32(0x02CC5D05) == bytes.fromhex("02cc5d05")
    assert canonical64(0xEF46DB3751D8E999) == bytes.fromhex("ef46db3751d8e999")


def _unxorshift(h: int, s: int) -> int:
    x = h
    for _ in range(32 // s + 1):
        x = h ^ (x >> s)
    return x


def invert_xxh32_4_bytes(h: int, seed: int) -> bytes:
    """Find the 4-byte input with XXH32 value h: every step for such inputs can be undone."""
    h = _unxorshift(h, 16)
    h = (h * pow(P32_3, -1, 1 << 32)) & M32
    h = _unxorshift(h, 13)
    h = (h * pow(0x85EBCA77, -1, 1 << 32)) & M32
    h = _unxorshift(h, 15)
    h = (h * pow(P32_4, -1, 1 << 32)) & M32
    h = ((h >> 17) | (h << 15)) & M32
    lane = ((h - (seed + P32_5 + 4)) * pow(P32_3, -1, 1 << 32)) & M32
    return lane.to_bytes(4, "little")


def test_not_preimage_resistant() -> None:
    # xxHash is not cryptographic: for 4-byte inputs the whole hash is a bijection
    # that can be inverted directly, with or without a known seed.
    rng = random.Random(1)
    for _ in range(20):
        x = rng.randbytes(4)
        seed = rng.getrandbits(32)
        assert invert_xxh32_4_bytes(xxh32(x, seed), seed) == x
    target = 0xDEADBEEF
    assert xxh32(invert_xxh32_4_bytes(target, 0), 0) == target


def test_collision_with_known_seed() -> None:
    # Each stripe round is a bijection of its lane, so a change in stripe 0 can be cancelled
    # in stripe 1: two different 32-byte inputs get the same XXH32 value.
    seed, p1, p2 = 12345, 0x9E3779B1, 0x85EBCA77
    x = bytearray(sanity_buffer(32))
    y = bytearray(x)
    y[0] ^= 0x01

    def after_first(lane: int) -> int:
        a = (seed + p1 + p2 + lane * p2) & M32
        return ((((a << 13) | (a >> 19)) & M32) * p1) & M32

    ax = after_first(int.from_bytes(x[0:4], "little"))
    ay = after_first(int.from_bytes(y[0:4], "little"))
    l1 = int.from_bytes(x[16:20], "little")
    y[16:20] = ((l1 + (ax - ay) * pow(p2, -1, 1 << 32)) & M32).to_bytes(4, "little")
    assert x != y
    assert xxh32(bytes(x), seed) == xxh32(bytes(y), seed)


def test_seed_changes_output() -> None:
    assert xxh64(b"hello", 0) != xxh64(b"hello", 1)
    assert xxh32(b"hello", 0) != xxh32(b"hello", 1)


def test_all_tail_paths_and_stripe_boundaries() -> None:
    data = sanity_buffer(100)
    seen32, seen64 = set(), set()
    for n in range(0, 100):
        seen32.add(xxh32(data[:n]))
        seen64.add(xxh64(data[:n]))
    assert len(seen32) == 100 and len(seen64) == 100


def test_avalanche_xxh64() -> None:
    rng = random.Random(7)
    total, trials = 0, 0
    for _ in range(40):
        msg = bytearray(rng.randbytes(40))
        base = xxh64(bytes(msg))
        bit = rng.randrange(320)
        msg[bit // 8] ^= 1 << (bit % 8)
        total += bin(base ^ xxh64(bytes(msg))).count("1")
        trials += 1
    assert 28 <= total / trials <= 36  # about 32 of 64 bits
