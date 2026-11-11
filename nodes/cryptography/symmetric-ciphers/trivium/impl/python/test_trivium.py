# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trivium/. The authors are listed in prov/RVXXYX.jsonl.

import random

from trivium import trivium_crypt, trivium_keystream

# eSTREAM test vectors for Trivium (verified.test-vectors), the first 16 bytes
# of stream[0..63]. Set 1 vector 0, Set 2 vector 0 and Set 6 vector 0.
VECTORS = [
    ("80000000000000000000", "00000000000000000000", "38EB86FF730D7A9CAF8DF13A4420540D"),
    ("00000000000000000000", "00000000000000000000", "FBE0BF265859051B517A2E4E239FC97F"),
    ("0053A6F94C9FF24598EB", "0D74DB42A91077DE45AC", "F4CD954A717F26A7D6930830C4E7CF08"),
]


def test_estream_vectors() -> None:
    for key, iv, ks in VECTORS:
        assert trivium_keystream(bytes.fromhex(key), bytes.fromhex(iv), 16).hex().upper() == ks


def test_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(5):
        key, iv = rng.randbytes(10), rng.randbytes(10)
        msg = rng.randbytes(rng.randrange(1, 40))
        assert trivium_crypt(key, iv, trivium_crypt(key, iv, msg)) == msg


def test_iv_changes_keystream() -> None:
    key = bytes(10)
    a = trivium_keystream(key, bytes(10), 16)
    b = trivium_keystream(key, bytes([1]) + bytes(9), 16)
    assert a != b
    # About half of the 128 bits differ.
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    assert 40 < diff < 88


def test_two_time_pad() -> None:
    key, iv = bytes(range(10)), bytes(range(10, 20))
    m1, m2 = b"attack at dawn!!", b"retreat at nine!"
    c1, c2 = trivium_crypt(key, iv, m1), trivium_crypt(key, iv, m2)
    assert bytes(a ^ b for a, b in zip(c1, c2)) == bytes(a ^ b for a, b in zip(m1, m2))
