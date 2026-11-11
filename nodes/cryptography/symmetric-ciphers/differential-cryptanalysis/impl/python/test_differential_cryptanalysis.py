# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-cryptanalysis/. The authors are listed in prov/7PQPMV.jsonl.

import random

from differential_cryptanalysis import (
    ALPHA,
    BETA,
    characteristic_probability,
    check_trail,
    pairs_needed,
    recover_last_round_bits,
)
from heys_spn import PERM, SUB, ddt, decrypt, encrypt, nibble


def _target(keys: list[int]) -> int:
    return (nibble(keys[4], 2) << 4) | nibble(keys[4], 4)


def test_spn_round_trip() -> None:
    rng = random.Random(1)
    keys = [rng.getrandbits(16) for _ in range(5)]
    for p in range(0, 1 << 16, 251):
        assert decrypt(encrypt(p, keys), keys) == p


def test_ddt_rows_sum_to_16() -> None:
    t = ddt()
    assert t[0][0] == 16
    assert all(sum(row) == 16 for row in t)
    assert t[0xB][0x2] == 8 and t[0x4][0x6] == 6 and t[0x2][0x5] == 6


def test_characteristic() -> None:
    assert check_trail()
    assert characteristic_probability() == 27 / 1024


def test_differential_at_least_characteristic() -> None:
    # Exact count over all 2^16 pairs for one key: the differential 0x0B00 ->
    # 0x0606 (any inner path) holds at least as often as the single trail.
    keys = [0x1234, 0x9ABC, 0x5A5A, 0x0F0F, 0x7777]

    def three_rounds(p: int) -> int:
        x = p
        for r in range(3):
            x = PERM[SUB[x ^ keys[r]]]
        return x

    hits = sum(1 for p in range(1 << 16) if three_rounds(p) ^ three_rounds(p ^ ALPHA) == BETA)
    assert hits / (1 << 16) >= 27 / 1024


def test_recovery_with_predicted_pairs() -> None:
    # N = 8 / p = 303 pairs (about 8 right pairs): recover the 8 key bits of
    # K5 on nibbles 2 and 4 for at least 45 of 50 random keys.
    n = pairs_needed(8)
    assert n == 303
    rng = random.Random(2024)
    ok = 0
    for _ in range(50):
        keys = [rng.getrandbits(16) for _ in range(5)]
        pts = [rng.getrandbits(16) for _ in range(n)]
        best, _ = recover_last_round_bits(lambda p: encrypt(p, keys), n, pts)
        ok += best == _target(keys)
    assert ok >= 45


def test_recovery_with_double_pairs_always_works() -> None:
    n = pairs_needed(16)
    rng = random.Random(7)
    for _ in range(30):
        keys = [rng.getrandbits(16) for _ in range(5)]
        pts = [rng.getrandbits(16) for _ in range(n)]
        best, counts = recover_last_round_bits(lambda p: encrypt(p, keys), n, pts)
        assert best == _target(keys)
        # The right guess counts about N * p right pairs.
        assert counts[best] >= 0.5 * n * characteristic_probability()
