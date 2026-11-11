# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clmul-crc-folding/. The authors are listed in prov/W0AB8H.jsonl.

import binascii
import random

from clmul_crc_folding import (
    Count, barrett, clmul, constants, crc32_fold, crc32_iso_hdlc, crc32c, poly_mod, reflected_constants,
)

RNG = random.Random(2009)


def crc_bitwise(data: bytes, poly: int, refin: bool) -> int:
    """Reference CRC with init and xorout all ones, refout = refin."""
    reg = 0xFFFFFFFF
    for byte in data:
        if refin:
            byte = int(f"{byte:08b}"[::-1], 2)
        for i in range(7, -1, -1):
            f = ((byte >> i) & 1) ^ (reg >> 31)
            reg = (reg << 1) & 0xFFFFFFFF
            if f:
                reg ^= poly
    if refin:
        reg = int(f"{reg:032b}"[::-1], 2)
    return reg ^ 0xFFFFFFFF


def test_constants_match_white_paper() -> None:
    # Gopal et al., Fast CRC computation for generic polynomials using
    # PCLMULQDQ instruction, Intel, December 2009: the constants of the
    # IEEE 802.3 example (normal domain), copied by hand.
    c = constants(0x04C11DB7)
    assert c["P"] == 0x104C11DB7
    assert c["k1"] == 0x8833794C  # x^(4*128+64) mod P
    assert c["k2"] == 0xE6228B11  # x^(4*128) mod P
    assert c["k3"] == 0xC5B9CD4C  # x^(128+64) mod P
    assert c["k4"] == 0xE8A45605  # x^128 mod P
    assert c["k5"] == 0xF200AA66  # x^96 mod P
    assert c["k6"] == 0x490D678D  # x^64 mod P
    assert c["mu"] == 0x104D101DF  # floor(x^64 / P)
    # The gzip example (bit-reflected), copied by hand.
    r = reflected_constants(0x04C11DB7)
    assert r == {
        "P": 0x1DB710641, "k1": 0x154442BD4, "k2": 0x1C6E41596, "k3": 0x1751997D0,
        "k4": 0x0CCAA009E, "k5": 0x163CD6124, "k6": 0x1DB710640, "mu": 0x1F7011641,
    }


def test_clmul() -> None:
    assert clmul(0b1011, 0b101) == 0b100111
    for _ in range(200):
        a, b = RNG.getrandbits(64), RNG.getrandbits(64)
        r = clmul(a, b)
        assert r.bit_length() <= 127
        assert clmul(b, a) == r


def test_barrett_is_exact() -> None:
    for poly in (0x04C11DB7, 0x1EDC6F41):
        c = constants(poly)
        for _ in range(2000):
            t = RNG.getrandbits(64)
            assert barrett(t, c, Count()) == poly_mod(t, c["P"])


def test_iso_hdlc_random_lengths() -> None:
    for n in list(range(0, 70)) + [RNG.randrange(70, 3000) for _ in range(30)]:
        data = bytes(RNG.randrange(256) for _ in range(n))
        assert crc32_iso_hdlc(data) == binascii.crc32(data), n


def test_crc32c_random_lengths() -> None:
    assert crc32c(b"123456789") == 0xE3069283  # reveng catalogue, CRC-32/ISCSI
    assert crc32c(bytes(32)) == 0x8A9136AA  # RFC 3720, Appendix B.4
    for n in list(range(0, 70)) + [RNG.randrange(70, 2000) for _ in range(15)]:
        data = bytes(RNG.randrange(256) for _ in range(n))
        assert crc32c(data) == crc_bitwise(data, 0x1EDC6F41, True), n


def test_not_reflected_crc() -> None:
    # CRC-32/BZIP2: refin = refout = false, check 0xFC891918 (reveng).
    assert crc32_fold(b"123456789", 0x04C11DB7, 0xFFFFFFFF, False, False, 0xFFFFFFFF) == 0xFC891918
    for n in (5, 64, 300):
        data = bytes(RNG.randrange(256) for _ in range(n))
        assert crc32_fold(data, 0x04C11DB7, 0xFFFFFFFF, False, False, 0xFFFFFFFF) == crc_bitwise(
            data, 0x04C11DB7, False
        )


def test_clmul_count() -> None:
    # 1024 bytes = 64 chunks of 128 bits: 15 rounds of fold-by-4 (8 clmul
    # each), 3 folds 4 -> 1 (2 each), then 2 for x^32 and 2 for Barrett.
    cnt = Count()
    crc32_iso_hdlc(bytes(1024), cnt)
    assert cnt.clmul == 15 * 8 + 3 * 2 + 2 + 2
