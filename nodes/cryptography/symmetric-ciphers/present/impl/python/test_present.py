# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/present/. The authors are listed in prov/ADV21B.jsonl.

import random

from present import (
    SBOX,
    p_layer,
    p_layer_inv,
    present80_decrypt,
    present80_encrypt,
    round_keys_80,
)

F64 = (1 << 64) - 1
F80 = (1 << 80) - 1

# The test vectors of PRESENT-80 in the appendix of Bogdanov et al. (CHES 2007).
VECTORS = [
    (0, 0, 0x5579C1387B228445),
    (0, F80, 0xE72C46C0F5945049),
    (F64, 0, 0xA112FFC72F68417B),
    (F64, F80, 0x3333DCD3213210D2),
]


def test_paper_vectors() -> None:
    for pt, key, ct in VECTORS:
        assert present80_encrypt(pt, key) == ct
        assert present80_decrypt(ct, key) == pt


def test_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(30):
        pt, key = rng.getrandbits(64), rng.getrandbits(80)
        assert present80_decrypt(present80_encrypt(pt, key), key) == pt


def test_round_keys() -> None:
    rk = round_keys_80(0)
    assert len(rk) == 32
    assert rk[0] == 0 and rk[1] == 0xC000000000000000


def test_p_layer_has_order_three() -> None:
    # P(i) = 16 i mod 63 and 16^3 = 4096 = 1 mod 63, so P applied three times is the identity.
    rng = random.Random(2)
    for _ in range(50):
        x = rng.getrandbits(64)
        assert p_layer(p_layer(p_layer(x))) == x
        assert p_layer_inv(p_layer(x)) == x


def test_sbox_differential_and_linear_bounds() -> None:
    # The design criteria of the paper: each DDT entry is at most 4, a one-bit
    # input difference never gives a one-bit output difference, and each linear
    # bias is at most 1/4 (a LAT count at most 4 away from 8).
    ddt = [[0] * 16 for _ in range(16)]
    for x in range(16):
        for a in range(16):
            ddt[a][SBOX[x] ^ SBOX[x ^ a]] += 1
    assert max(ddt[a][b] for a in range(1, 16) for b in range(16)) == 4
    for a in (1, 2, 4, 8):
        for b in (1, 2, 4, 8):
            assert ddt[a][b] == 0
    for a in range(1, 16):
        for b in range(1, 16):
            count = sum(1 for x in range(16) if bin(a & x).count("1") % 2 == bin(b & SBOX[x]).count("1") % 2)
            assert abs(count - 8) <= 4
