# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adler-32/. The authors are listed in prov/G06YQ1.jsonl.

import random
import zlib

from adler_32 import BASE, NMAX, adler32, adler32_combine, adler32_plain


def test_known_value() -> None:
    # Adler-32 of the ASCII string "Wikipedia" is 0x11E60398 (Wikipedia, "Adler-32", Example);
    # zlib.adler32 gives the same value.
    assert adler32(b"Wikipedia") == 0x11E60398
    assert zlib.adler32(b"Wikipedia") == 0x11E60398


def test_page_trace() -> None:
    s1, s2 = 1, 0
    rows = []
    for d in b"Wikipedia":
        s1 = (s1 + d) % BASE
        s2 = (s2 + s1) % BASE
        rows.append((s1, s2))
    assert rows[-1] == (0x398, 0x11E6) == (920, 4582)
    assert rows[:3] == [(88, 88), (193, 281), (300, 581)]


def test_edges() -> None:
    assert adler32(b"") == 1
    assert adler32(b"\x00") == 0x00010001
    assert adler32(b"\xff" * 10_000) == zlib.adler32(b"\xff" * 10_000)
    assert NMAX == 5552
    n = NMAX
    assert 255 * n * (n + 1) // 2 + (n + 1) * (BASE - 1) <= 2**32 - 1
    n = NMAX + 1
    assert 255 * n * (n + 1) // 2 + (n + 1) * (BASE - 1) > 2**32 - 1


def test_random_against_zlib() -> None:
    rng = random.Random(8101)
    for _ in range(600):
        n = rng.choice([rng.randrange(0, 50), rng.randrange(0, 2000)])
        data = bytes(rng.choice([0, 255, rng.randrange(256)]) for _ in range(n))
        assert adler32(data) == zlib.adler32(data)
        assert adler32_plain(data) == zlib.adler32(data)


def test_long_worst_case_input() -> None:
    data = b"\xff" * (3 * NMAX + 11)
    assert adler32(data) == zlib.adler32(data)


def test_running_value() -> None:
    rng = random.Random(8102)
    for _ in range(300):
        a = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 100)))
        b = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 100)))
        assert adler32(b, adler32(a)) == zlib.adler32(a + b) == zlib.adler32(b, zlib.adler32(a))


def test_combine() -> None:
    rng = random.Random(8103)
    for _ in range(600):
        a = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 200)))
        b = bytes(rng.randrange(256) for _ in range(rng.choice([0, 1, rng.randrange(0, 200), 70000])))
        assert adler32_combine(zlib.adler32(a), zlib.adler32(b), len(b)) == zlib.adler32(a + b)


def test_zero_ff_change_is_detected() -> None:
    # Unlike Fletcher-16 (mod 255), a byte 0x00 -> 0xFF changes s1 by 255, which is not 0 mod 65521.
    rng = random.Random(8104)
    data = bytearray(rng.choice([0, 255]) for _ in range(64))
    c = adler32(bytes(data))
    for i in range(64):
        b = bytearray(data)
        b[i] = 255 - b[i]
        assert adler32(bytes(b)) != c


def test_short_messages_use_few_values() -> None:
    # For 128-byte messages s1 is at most 1 + 255 * 128 = 32641 < 65521, so s1
    # never wraps and its top bit stays 0 (RFC 3309, Section 1).
    assert 1 + 255 * 128 == 32641 < BASE
    rng = random.Random(8105)
    for _ in range(300):
        data = bytes(rng.randrange(256) for _ in range(128))
        assert (adler32(data) & 0xFFFF) < 0x8000
    # All 65536 two-byte messages give 65536 distinct checksums, but s1 takes only 511 values.
    s1_values = {adler32(bytes([x, y])) & 0xFFFF for x in range(256) for y in range(256)}
    assert len(s1_values) == 511
