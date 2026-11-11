# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tea/. The authors are listed in prov/1JEH0C.jsonl.

import random

from tea import equivalent_keys, tea_decrypt, tea_decrypt_block, tea_encrypt, tea_encrypt_block

# There are no official TEA test vectors. These published reference values are
# from the Crypto++ file TestVectors/tea.txt, which names its source as
# http://www.cix.co.uk/~klockstone/teavect.htm. Words are big-endian.
VECTORS = [
    ("0000000000000000", "00000000000000000000000000000000", "41ea3a0a94baa940"),
    ("94baa94000000000", "00000000000000000000000041ea3a0a", "4e8e78297d8236d8"),
    ("7d8236d800000000", "000000000000000041ea3a0a4e8e7829", "c88ba95ee7edac02"),
]


def test_reference_values() -> None:
    for pt, key, ct in VECTORS:
        assert tea_encrypt_block(bytes.fromhex(pt), bytes.fromhex(key)).hex() == ct
        assert tea_decrypt_block(bytes.fromhex(ct), bytes.fromhex(key)).hex() == pt


def test_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(200):
        v = (rng.getrandbits(32), rng.getrandbits(32))
        k = (rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32))
        assert tea_decrypt(tea_encrypt(v, k), k) == v


def test_equivalent_keys_give_the_same_ciphertext() -> None:
    rng = random.Random(2)
    for _ in range(200):
        v = (rng.getrandbits(32), rng.getrandbits(32))
        k = (rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32))
        keys = equivalent_keys(k)
        assert len(set(keys)) == 4
        assert len({tea_encrypt(v, kk) for kk in keys}) == 1


def test_one_top_bit_alone_changes_the_ciphertext() -> None:
    # Flipping the top bit of k0 alone is not an equivalence.
    rng = random.Random(3)
    v = (rng.getrandbits(32), rng.getrandbits(32))
    k = (rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32))
    k2 = (k[0] ^ 0x80000000, k[1], k[2], k[3])
    assert tea_encrypt(v, k) != tea_encrypt(v, k2)


def test_avalanche() -> None:
    rng = random.Random(4)
    total = 0
    trials = 200
    for _ in range(trials):
        v = (rng.getrandbits(32), rng.getrandbits(32))
        k = (rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32))
        bit = rng.randrange(64)
        w = (v[0] ^ (1 << bit), v[1]) if bit < 32 else (v[0], v[1] ^ (1 << (bit - 32)))
        a, b = tea_encrypt(v, k), tea_encrypt(w, k)
        total += bin(a[0] ^ b[0]).count("1") + bin(a[1] ^ b[1]).count("1")
    assert 28 < total / trials < 36
