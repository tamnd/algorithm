# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/speck/. The authors are listed in prov/7HAM9F.jsonl.

import random

from speck import PARAMS, speck_decrypt, speck_encrypt, speck_key_schedule

# Test vectors from the appendix of Beaulieu et al., ePrint 2013/404.
# Each entry: (block bits, key bits, key words l[m-2]..l[0] k[0], plaintext (x, y), ciphertext (x, y)).
VECTORS = [
    (32, 64, [0x1918, 0x1110, 0x0908, 0x0100], (0x6574, 0x694C), (0xA868, 0x42F2)),
    (48, 72, [0x121110, 0x0A0908, 0x020100], (0x20796C, 0x6C6172), (0xC049A5, 0x385ADC)),
    (64, 96, [0x13121110, 0x0B0A0908, 0x03020100], (0x74614620, 0x736E6165), (0x9F7952EC, 0x4175946C)),
    (
        64,
        128,
        [0x1B1A1918, 0x13121110, 0x0B0A0908, 0x03020100],
        (0x3B726574, 0x7475432D),
        (0x8C6FA548, 0x454E028B),
    ),
    (
        128,
        128,
        [0x0F0E0D0C0B0A0908, 0x0706050403020100],
        (0x6C61766975716520, 0x7469206564616D20),
        (0xA65D985179783265, 0x7860FEDF5C570D18),
    ),
    (
        128,
        256,
        [0x1F1E1D1C1B1A1918, 0x1716151413121110, 0x0F0E0D0C0B0A0908, 0x0706050403020100],
        (0x65736F6874206E49, 0x202E72656E6F6F70),
        (0x4109010405C0F53E, 0x4EEEB48D9C188F43),
    ),
]


def test_paper_vectors() -> None:
    for bb, kb, key, pt, ct in VECTORS:
        assert speck_encrypt(pt, key, bb, kb) == ct
        assert speck_decrypt(ct, key, bb, kb) == pt


def test_round_trip_all_parameter_sets() -> None:
    rng = random.Random(1)
    for (bb, kb), (n, m, rounds) in PARAMS.items():
        for _ in range(5):
            key = [rng.getrandbits(n) for _ in range(m)]
            pt = (rng.getrandbits(n), rng.getrandbits(n))
            assert speck_decrypt(speck_encrypt(pt, key, bb, kb), key, bb, kb) == pt
            assert len(speck_key_schedule(key, bb, kb)) == rounds


def test_key_schedule_is_the_round_function() -> None:
    # For m = 2 the schedule is the round function applied to (l[i], k[i]) with key i.
    rng = random.Random(2)
    n = 64
    mask = (1 << n) - 1
    key = [rng.getrandbits(n), rng.getrandbits(n)]
    k = speck_key_schedule(key, 128, 128)
    x, y = key[0], key[1]  # (l[0], k[0])
    for i in range(31):
        x = ((((x >> 8) | (x << 56)) & mask) + y & mask) ^ i
        y = (((y << 3) | (y >> 61)) & mask) ^ x
        assert y == k[i + 1]


def test_avalanche() -> None:
    rng = random.Random(3)
    total = 0
    trials = 100
    for _ in range(trials):
        key = [rng.getrandbits(32) for _ in range(4)]
        pt = (rng.getrandbits(32), rng.getrandbits(32))
        bit = rng.randrange(32)
        a = speck_encrypt(pt, key, 64, 128)
        b = speck_encrypt((pt[0] ^ (1 << bit), pt[1]), key, 64, 128)
        total += bin(a[0] ^ b[0]).count("1") + bin(a[1] ^ b[1]).count("1")
    assert 28 < total / trials < 36
