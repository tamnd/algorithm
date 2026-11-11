# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simon-cipher/. The authors are listed in prov/D973ES.jsonl.

import random

from simon_cipher import PARAMS, Z, simon_decrypt, simon_encrypt, simon_key_schedule

# Test vectors from the appendix of Beaulieu et al., ePrint 2013/404.
# Each entry: (block bits, key bits, key words k[m-1]..k[0], plaintext (x, y), ciphertext (x, y)).
VECTORS = [
    (32, 64, [0x1918, 0x1110, 0x0908, 0x0100], (0x6565, 0x6877), (0xC69B, 0xE9BB)),
    (48, 72, [0x121110, 0x0A0908, 0x020100], (0x612067, 0x6E696C), (0xDAE5AC, 0x292CAC)),
    (48, 96, [0x1A1918, 0x121110, 0x0A0908, 0x020100], (0x726963, 0x20646E), (0x6E06A5, 0xACF156)),
    (
        64,
        128,
        [0x1B1A1918, 0x13121110, 0x0B0A0908, 0x03020100],
        (0x656B696C, 0x20646E75),
        (0x44C8FC20, 0xB9DFA07A),
    ),
    (
        128,
        128,
        [0x0F0E0D0C0B0A0908, 0x0706050403020100],
        (0x6373656420737265, 0x6C6C657661727420),
        (0x49681B1E1E54FE3F, 0x65AA832AF84E0BBC),
    ),
    (
        128,
        256,
        [0x1F1E1D1C1B1A1918, 0x1716151413121110, 0x0F0E0D0C0B0A0908, 0x0706050403020100],
        (0x74206E69206D6F6F, 0x6D69732061207369),
        (0x8D2B5579AFC8A3A0, 0x3BF72A87EFE7B868),
    ),
]


def test_paper_vectors() -> None:
    # Together these use the five sequences z0, z1, z2, z3 and z4.
    for bb, kb, key, pt, ct in VECTORS:
        assert simon_encrypt(pt, key, bb, kb) == ct
        assert simon_decrypt(ct, key, bb, kb) == pt


def test_round_trip_all_parameter_sets() -> None:
    rng = random.Random(1)
    for (bb, kb), (n, m, rounds, _) in PARAMS.items():
        for _ in range(5):
            key = [rng.getrandbits(n) for _ in range(m)]
            pt = (rng.getrandbits(n), rng.getrandbits(n))
            assert simon_decrypt(simon_encrypt(pt, key, bb, kb), key, bb, kb) == pt
            assert len(simon_key_schedule(key, bb, kb)) == rounds


def test_first_round_keys_are_the_key_words() -> None:
    key = [0x1B1A1918, 0x13121110, 0x0B0A0908, 0x03020100]
    assert simon_key_schedule(key, 64, 128)[:4] == [0x03020100, 0x0B0A0908, 0x13121110, 0x1B1A1918]


def test_z_sequences_of_period_31() -> None:
    # z0 and z1 repeat with period 31; z2, z3 and z4 have period 62.
    for j, z in enumerate(Z):
        assert len(z) == 62
        assert (z[:31] == z[31:]) == (j < 2)
