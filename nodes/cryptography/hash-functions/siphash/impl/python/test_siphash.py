# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/siphash/. The authors are listed in prov/V4BHB1.jsonl.

import random
from collections import Counter

import pytest

from siphash import halfsiphash32, message_words, siphash, siphash_bytes, siphash_state

KEY = bytes(range(16))  # 00 01 ... 0f


def test_paper_appendix_a() -> None:
    # Aumasson and Bernstein, SipHash: a fast short-input PRF, Appendix A (Test values).
    msg = bytes(range(15))
    assert message_words(msg, 8) == [0x0706050403020100, 0x0F0E0D0C0B0A0908]
    v = siphash_state(KEY, msg)
    assert v == [0xF6BCD53893FECFF1, 0x54B9964C7EA0D937, 0x1B38329C099BB55A, 0x1814BB89AD7BE679]
    assert siphash(KEY, msg) == 0xA129CA6149BE45E5


@pytest.mark.parametrize(
    "n, out",
    [
        # SipHash reference repository (github.com/veorq/SipHash), vectors.h,
        # vectors_sip64[n]: key 00..0f, message 00 01 .. (n-1), output bytes.
        (0, "310e0edd47db6f72"),
        (1, "fd67dc93c539f874"),
        (15, "e545be4961ca29a1"),
        (63, "724506eb4c328a95"),
    ],
)
def test_reference_vectors_sip64(n: int, out: str) -> None:
    assert siphash_bytes(KEY, bytes(range(n))).hex() == out


@pytest.mark.parametrize(
    "n, out",
    [
        # vectors.h, vectors_hsip32[n]: HalfSipHash-2-4, key 00..07, 32-bit output.
        (0, "a9359f5b"),
        (1, "27475ab8"),
        (15, "74fe2b97"),
        (63, "59ea4a74"),
    ],
)
def test_reference_vectors_halfsiphash32(n: int, out: str) -> None:
    assert halfsiphash32(KEY[:8], bytes(range(n))).hex() == out


def test_round_counts_matter() -> None:
    msg = b"hello"
    assert siphash(KEY, msg, 1, 3) != siphash(KEY, msg, 2, 4)


def test_wrong_key_changes_output() -> None:
    rng = random.Random(1)
    for _ in range(50):
        k = rng.randbytes(16)
        k2 = bytearray(k)
        k2[rng.randrange(16)] ^= 1 << rng.randrange(8)
        m = rng.randbytes(rng.randrange(0, 40))
        assert siphash(k, m) != siphash(bytes(k2), m)


def test_length_byte_separates_zero_padding() -> None:
    # Without the length byte, "ab" and "ab\x00" would share their last word.
    assert siphash(KEY, b"ab") != siphash(KEY, b"ab\x00")
    assert message_words(b"ab", 8) != message_words(b"ab\x00", 8)


def test_avalanche() -> None:
    rng = random.Random(2)
    total, trials = 0, 400
    for _ in range(trials):
        m = bytearray(rng.randbytes(12))
        a = siphash(KEY, bytes(m))
        m[rng.randrange(12)] ^= 1 << rng.randrange(8)
        total += bin(a ^ siphash(KEY, bytes(m))).count("1")
    assert 29 < total / trials < 35  # about 32 of 64 bits


def _weak_hash(s: bytes) -> int:
    """A sum of bytes: unkeyed and with many easy collisions (a toy, not a real runtime hash)."""
    return sum(s)


def test_hash_flooding_toy() -> None:
    # Attacker: all permutations of one byte string have the same weak hash.
    base = b"abcdefg"
    rng = random.Random(3)
    keys = {bytes(rng.sample(base, len(base))) for _ in range(3000)}
    buckets = 1024
    weak = Counter(_weak_hash(k) % buckets for k in keys)
    assert len(weak) == 1  # every key falls into one bucket: chains of length n
    secret = rng.randbytes(16)  # the table owner picks a secret key
    strong = Counter(siphash(secret, k) % buckets for k in keys)
    assert max(strong.values()) < 15  # keys spread out
