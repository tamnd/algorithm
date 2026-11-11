# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/checksum/. The authors are listed in prov/B82EKR.jsonl.

import random

from checksum import crc8, crc32, flip, lrc, miss_rates, parity, sum8


def test_check_values() -> None:
    data = b"123456789"
    assert crc8(data) == 0xF4  # reveng catalogue, CRC-8/SMBUS check
    assert crc32(data) == 0xCBF43926  # reveng catalogue, CRC-32/ISO-HDLC check
    assert sum8(data) == 0xDD  # 0x31 + ... + 0x39 = 0x1DD
    assert lrc(data) == 0x31
    assert parity(b"\x01\x02") == 0 and parity(b"\x07") == 1


def test_double_errors_exhaustive() -> None:
    rng = random.Random(7)
    msg = rng.randbytes(32)
    n = len(msg) * 8
    for p in range(n):
        for q in range(p + 1, n):
            bad = flip(msg, [p, q])
            same_col = p % 8 == q % 8
            bit_p = (msg[p // 8] >> (7 - p % 8)) & 1
            bit_q = (msg[q // 8] >> (7 - q % 8)) & 1
            assert parity(bad) == parity(msg)  # parity misses every double error
            assert (lrc(bad) == lrc(msg)) == same_col
            # The sum cancels for opposite flips in one column, and always in
            # the top bit, where 128 + 128 = 256.
            assert (sum8(bad) == sum8(msg)) == (same_col and (bit_p != bit_q or p % 8 == 0))
            assert (crc8(bad) == crc8(msg)) == ((q - p) % 127 == 0)


def test_harness_with_fixed_seed() -> None:
    t = 3000
    res = miss_rates(t, 64, seed=2024)
    assert all(v == 0 for v in res["single"].values())
    assert res["double"]["parity"] == t and res["double"]["crc32"] == 0
    for name, want in (("lrc", 63 / 511), ("sum8", 63 / 511 * 9 / 16), ("crc8", 774 / 130816)):
        sigma = (want * (1 - want) / t) ** 0.5
        assert abs(res["double"][name] / t - want) < 5 * sigma, name
    for name in ("lrc", "sum8", "crc8", "crc32"):
        assert res["burst 2-8"][name] == 0
    assert abs(res["burst 9-32"]["parity"] / t - 0.5) < 0.05
    assert res["burst 9-32"]["crc8"] < 3 * t / 256 and res["burst 9-32"]["crc32"] == 0
