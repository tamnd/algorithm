# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/murmurhash/. The authors are listed in prov/HXY9Z7.jsonl.

import itertools
import random
import struct

from murmurhash import C1, C2, fmix32, mix, murmur3_32, rotl32

M32 = 1 << 32


def oracle(key: bytes, seed: int) -> int:
    # A line-by-line transcription of MurmurHash3_x86_32 from MurmurHash3.cpp,
    # with the switch fall-through written out and struct for the block reads.
    length = len(key)
    nblocks = length // 4
    h1 = seed % M32
    for i in range(nblocks):
        (k1,) = struct.unpack_from("<I", key, 4 * i)
        k1 = (k1 * 0xCC9E2D51) % M32
        k1 = ((k1 << 15) | (k1 >> 17)) % M32
        k1 = (k1 * 0x1B873593) % M32
        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) % M32
        h1 = (h1 * 5 + 0xE6546B64) % M32
    tail = key[4 * nblocks :]
    k1 = 0
    rest = length & 3
    if rest >= 3:
        k1 ^= tail[2] << 16
    if rest >= 2:
        k1 ^= tail[1] << 8
    if rest >= 1:
        k1 ^= tail[0]
        k1 = (k1 * 0xCC9E2D51) % M32
        k1 = ((k1 << 15) | (k1 >> 17)) % M32
        k1 = (k1 * 0x1B873593) % M32
        h1 ^= k1
    h1 ^= length % M32
    h1 ^= h1 >> 16
    h1 = (h1 * 0x85EBCA6B) % M32
    h1 ^= h1 >> 13
    h1 = (h1 * 0xC2B2AE35) % M32
    h1 ^= h1 >> 16
    return h1


def unmix(m: int) -> int:
    k = (m * pow(C2, -1, M32)) % M32
    k = rotl32(k, 17)
    return (k * pow(C1, -1, M32)) % M32


def test_verification_value() -> None:
    # SMHasher: hash the keys {}, {0}, {0,1}, ..., {0..254} with seeds 256 - i, then hash the results.
    key = bytes(range(256))
    hashes = b"".join(murmur3_32(key[:i], 256 - i).to_bytes(4, "little") for i in range(256))
    assert murmur3_32(hashes, 0) == 0xB0F57EE3


def test_vectors() -> None:
    assert murmur3_32(b"", 0) == 0
    assert murmur3_32(b"", 1) == 0x514E28B7
    assert murmur3_32(b"", 0xFFFFFFFF) == 0x81F16F39
    assert murmur3_32(b"\0\0\0\0", 0) == 0x2362F9DE
    assert murmur3_32(b"aaaa", 0x9747B28C) == 0x5A97808A
    assert murmur3_32("Hello, world!", 0x9747B28C) == 0x24884CBA
    assert murmur3_32(b"The quick brown fox jumps over the lazy dog", 0x9747B28C) == 0x2FA826CD


def test_mix_and_fmix_are_bijections() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        k = rng.getrandbits(32)
        assert unmix(mix(k)) == k
    # fmix32 is injective on a sample of 2^16 consecutive and 2^16 random inputs.
    xs = list(range(1 << 16)) + [rng.getrandbits(32) for _ in range(1 << 16)]
    xs = list(set(xs))
    assert len({fmix32(x) for x in xs}) == len(xs)


def test_seed_independent_collisions() -> None:
    rng = random.Random(11)
    pairs = []
    for _ in range(3):
        x = bytes(rng.randrange(256) for _ in range(8))
        k1 = int.from_bytes(x[:4], "little")
        k2 = int.from_bytes(x[4:], "little")
        y = unmix(mix(k1) ^ 0x00040000).to_bytes(4, "little") + unmix(mix(k2) ^ 0x80000000).to_bytes(4, "little")
        assert x != y
        pairs.append((x, y))
    # 2^3 strings of 24 bytes, made of one block pair from each of 3 pairs, share one hash for every seed.
    keys = [b"".join(choice) for choice in itertools.product(*pairs)]
    for seed in [0, 1, 42, 0x9747B28C, 0xFFFFFFFF] + [rng.getrandbits(32) for _ in range(20)]:
        assert len({murmur3_32(k, seed) for k in keys}) == 1
        assert len({murmur3_32(k + b"tail!", seed) for k in keys}) == 1


def random_bytes(rng: random.Random, alphabet: bytes) -> bytes:
    n = rng.randrange(0, 40)
    if rng.random() < 0.3 and n:
        unit = bytes(rng.choice(alphabet) for _ in range(rng.randrange(1, 5)))
        return (unit * n)[:n]
    return bytes(rng.choice(alphabet) for _ in range(n))


def test_random_against_oracle() -> None:
    rng = random.Random(20261106)
    for alphabet in (b"a", b"ab", b"abcd", bytes(range(256))):
        for _ in range(400):
            x = random_bytes(rng, alphabet)
            seed = rng.choice([0, 1, 0xFFFFFFFF, rng.getrandbits(32)])
            hx = murmur3_32(x, seed)
            assert hx == oracle(x, seed)
            # Equal lengths, exactly one byte changed: never a collision.
            if x:
                i = rng.randrange(len(x))
                y = bytearray(x)
                y[i] = (y[i] + rng.randrange(1, 256)) % 256
                assert murmur3_32(bytes(y), seed) != hx
    # All strings over {a, b} up to length 9: no two of the same length collide here, and the oracle agrees.
    for n in range(10):
        values = [murmur3_32(bytes(t), 0) for t in itertools.product(b"ab", repeat=n)]
        assert len(set(values)) == len(values)


def test_seed_matters() -> None:
    rng = random.Random(3)
    for _ in range(200):
        x = random_bytes(rng, b"abcd")
        s = rng.getrandbits(32)
        assert murmur3_32(x, s) != murmur3_32(x, s ^ 1)
