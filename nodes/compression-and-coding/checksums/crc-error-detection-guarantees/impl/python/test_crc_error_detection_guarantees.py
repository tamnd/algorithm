# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crc-error-detection-guarantees/. The authors are listed in prov/Y8VC6W.jsonl.

import random

from crc_error_detection_guarantees import (
    burst_miss_count, bursts_missed_at_positions, deg, is_missed, missed_patterns_all, period, pmod,
)

RNG = random.Random(1961)
SMBUS = 0x107  # CRC-8/SMBUS, (x + 1)(x^7 + x^6 + x^5 + x^4 + x^3 + x^2 + 1)
PRIM8 = 0x14D  # primitive of degree 8, no factor x + 1
ARC = 0x18005  # CRC-16/ARC, (x + 1)(x^15 + x + 1)
CCITT = 0x11021  # CRC-16 of ITU-T V.41, (x + 1) times a primitive of degree 15
GENS = [SMBUS, PRIM8, ARC, CCITT]


def test_single_errors() -> None:
    for g in GENS:
        assert not any(is_missed(1 << i, g) for i in range(300))


def test_odd_weight_errors_exhaustive() -> None:
    n = 20
    for g in (SMBUS, ARC, CCITT):  # each has the factor x + 1
        missed = missed_patterns_all(g, n)
        # The missed patterns are the nonzero codewords: 2^(n - r) - 1 of them.
        assert len(missed) == 2 ** (n - deg(g)) - 1
        assert all(bin(e).count("1") % 2 == 0 for e in missed)
    missed = missed_patterns_all(PRIM8, n)
    assert any(bin(e).count("1") % 2 == 1 for e in missed)  # no x + 1: odd errors slip through


def test_double_errors_and_period() -> None:
    assert period(SMBUS, 1000) == 127
    assert period(PRIM8, 1000) == 255
    assert period(ARC, 40000) == 32767
    assert period(CCITT, 40000) == 32767
    for g, e, limit in ((SMBUS, 127, 600), (PRIM8, 255, 800)):
        for j in range(1, limit):
            assert is_missed((1 << j) | 1, g) == (j % e == 0)
    # For the 16-bit generators walk x^j mod G for all j up to 70000.
    for g in (ARC, CCITT):
        s, r = 1, deg(g)
        for j in range(1, 70000):
            s <<= 1
            if s >> r:
                s ^= g
            assert (s == 1) == (j % 32767 == 0)


def test_bursts_exhaustive() -> None:
    for g, max_b in ((SMBUS, 16), (PRIM8, 16), (ARC, 20), (CCITT, 20)):
        r = deg(g)
        for b in range(1, max_b + 1):
            missed, total = burst_miss_count(g, b)
            if b <= r:
                assert missed == 0
            elif b == r + 1:
                assert missed == 1 and total == 2 ** (r - 1)
            else:
                assert missed * 2**r == total


def test_bursts_at_every_position() -> None:
    n = 40
    for b in range(1, 13):
        missed, _ = burst_miss_count(SMBUS, b)
        assert bursts_missed_at_positions(SMBUS, n, b) == (n - b + 1) * missed


def crc16_ibm3740(data: bytes) -> int:
    """CRC-16/IBM-3740 (CCITT-FALSE): poly 0x1021, init 0xFFFF, no reflection."""
    reg = 0xFFFF
    for byte in data:
        for i in range(7, -1, -1):
            f = ((byte >> i) & 1) ^ (reg >> 15)
            reg = (reg << 1) & 0xFFFF
            if f:
                reg ^= 0x1021
    return reg


def test_real_crc_misses_exactly_the_multiples() -> None:
    # The receiver of a CRC with init 0xFFFF accepts a corrupted codeword
    # exactly when G divides the error, whatever the message.
    assert crc16_ibm3740(b"123456789") == 0x29B1  # reveng catalogue check
    for trial in range(400):
        msg = bytes(RNG.randrange(256) for _ in range(6))
        cw = int.from_bytes(msg + crc16_ibm3740(msg).to_bytes(2, "big"), "big")
        if trial % 2:
            # e = q * G for a random nonzero q of degree < 47: must be missed
            q, e = RNG.getrandbits(47) or 1, 0
            for i in range(47):
                if (q >> i) & 1:
                    e ^= CCITT << i
        else:
            e = RNG.getrandbits(64) or 1
        bad = (cw ^ e).to_bytes(8, "big")
        accepted = crc16_ibm3740(bad[:6]) == int.from_bytes(bad[6:], "big")
        assert accepted == (pmod(e, CCITT) == 0)
