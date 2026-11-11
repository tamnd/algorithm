# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xtea/. The authors are listed in prov/07Z3SA.jsonl.

import random

from xtea import xtea_decrypt, xtea_decrypt_block, xtea_encrypt, xtea_encrypt_block

# There are no official XTEA test vectors. These published reference values are
# from the Crypto++ file TestVectors/tea.txt, which names its source as
# http://www.cix.co.uk/~klockstone/teavect.htm. Words are big-endian, and the
# file's "Rounds" field counts cycles.
VECTORS = [
    (1, "0000000000000000", "00000000000000000000000000000000", "000000009e3779b9"),
    (2, "9e3779b900000000", "00000000000000000000000000000000", "ec01a1deaaa0256d"),
    (32, "af20a390547571aa", "27f917b1c1da899360e2acaaa6eb923d", "d26428af0a202283"),
]


def test_reference_values() -> None:
    for cycles, pt, key, ct in VECTORS:
        assert xtea_encrypt_block(bytes.fromhex(pt), bytes.fromhex(key), cycles).hex() == ct
        assert xtea_decrypt_block(bytes.fromhex(ct), bytes.fromhex(key), cycles).hex() == pt


def test_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(200):
        v = (rng.getrandbits(32), rng.getrandbits(32))
        k = (rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32))
        assert xtea_decrypt(xtea_encrypt(v, k), k) == v


def test_tea_equivalent_keys_do_not_carry_over() -> None:
    # Flipping the top bits of k0 and k1 is an equivalence for TEA, not for XTEA.
    rng = random.Random(2)
    t = 0x80000000
    same = 0
    for _ in range(100):
        v = (rng.getrandbits(32), rng.getrandbits(32))
        k = (rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32))
        k2 = (k[0] ^ t, k[1] ^ t, k[2], k[3])
        same += xtea_encrypt(v, k) == xtea_encrypt(v, k2)
    assert same == 0


def test_avalanche() -> None:
    rng = random.Random(3)
    total = 0
    trials = 200
    for _ in range(trials):
        v = (rng.getrandbits(32), rng.getrandbits(32))
        k = (rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32))
        bit = rng.randrange(64)
        w = (v[0] ^ (1 << bit), v[1]) if bit < 32 else (v[0], v[1] ^ (1 << (bit - 32)))
        a, b = xtea_encrypt(v, k), xtea_encrypt(w, k)
        total += bin(a[0] ^ b[0]).count("1") + bin(a[1] ^ b[1]).count("1")
    assert 28 < total / trials < 36
