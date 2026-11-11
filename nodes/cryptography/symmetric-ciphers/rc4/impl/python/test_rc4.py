# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rc4/. The authors are listed in prov/F9NPHX.jsonl.

import random

from rc4 import rc4_crypt, rc4_keystream, rc4_ksa


def h(s: str) -> bytes:
    return bytes.fromhex(s.replace(" ", ""))


# RFC 6229, Section 2 (Test Vectors for RC4), copied by hand.
RFC6229 = [
    ("0102030405", 0, "b2 39 63 05 f0 3d c0 27 cc c3 52 4a 0a 11 18 a8"),
    ("0102030405", 16, "69 82 94 4f 18 fc 82 d5 89 c4 03 a4 7a 0d 09 19"),
    ("0102030405", 240, "28 cb 11 32 c9 6c e2 86 42 1d ca ad b8 b6 9e ae"),
    ("0102030405", 4096, "ff 25 b5 89 95 99 67 07 e5 1f bd f0 8b 34 d8 75"),
    ("0102030405060708090a0b0c0d0e0f10", 0, "9a c7 cc 9a 60 9d 1e f7 b2 93 28 99 cd e4 1b 97"),
    ("0102030405060708090a0b0c0d0e0f10", 16, "52 48 c4 95 90 14 12 6a 6e 8a 84 f1 1d 1a 9e 1c"),
    ("0102030405060708090a0b0c0d0e0f10", 240, "06 59 02 e4 b6 20 f6 cc 36 c8 58 9f 66 43 2f 2b"),
    ("ebb46227c6cc8b37641910833222772a", 0, "72 0c 94 b6 3e df 44 e1 31 d9 50 ca 21 1a 5a 30"),
]


def test_rfc6229_vectors() -> None:
    for key, off, want in RFC6229:
        ks = rc4_keystream(h(key), off + 16)
        assert ks[off:] == h(want)


def test_ksa_is_a_permutation() -> None:
    rng = random.Random(1)
    for _ in range(20):
        key = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 33)))
        assert sorted(rc4_ksa(key)) == list(range(256))


def test_decrypt_inverts_encrypt() -> None:
    rng = random.Random(2)
    for _ in range(20):
        key = bytes(rng.randrange(256) for _ in range(16))
        msg = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 100)))
        assert rc4_crypt(key, rc4_crypt(key, msg)) == msg


def test_second_byte_bias() -> None:
    # Mantin and Shamir (FSE 2001): Pr[Z2 = 0] is about 2/256 over random keys.
    # Sample of 20000 random 16-byte keys. Stated tolerance: the measured rate
    # must lie in [1.5/256, 2.5/256]. A uniform byte gives 1/256, outside it.
    rng = random.Random(3)
    n = 20000
    zeros2 = zeros1 = 0
    for _ in range(n):
        key = bytes(rng.randrange(256) for _ in range(16))
        z = rc4_keystream(key, 2)
        zeros1 += z[0] == 0
        zeros2 += z[1] == 0
    p2 = zeros2 / n
    assert 1.5 / 256 <= p2 <= 2.5 / 256
    # The first byte has no such bias: its zero rate is near 1/256.
    assert zeros1 / n < 1.5 / 256


def test_two_time_pad() -> None:
    # Reuse of one key: the XOR of the ciphertexts is the XOR of the plaintexts.
    key = h("0102030405060708090a0b0c0d0e0f10")
    m1 = b"attack at dawn, bring the maps"
    m2 = b"retreat at six, burn the notes"
    c1, c2 = rc4_crypt(key, m1), rc4_crypt(key, m2)
    x = bytes(a ^ b for a, b in zip(c1, c2))
    assert x == bytes(a ^ b for a, b in zip(m1, m2))
    # Who knows m1 recovers m2 without the key.
    assert bytes(a ^ b for a, b in zip(x, m1)) == m2


def test_bit_flip_malleability() -> None:
    key = h("0102030405")
    m = b"PAY 100 TO BOB"
    c = bytearray(rc4_crypt(key, m))
    # Change "1" to "9" in place: flip the bits of ord("1") ^ ord("9").
    c[4] ^= ord("1") ^ ord("9")
    assert rc4_crypt(key, bytes(c)) == b"PAY 900 TO BOB"
