# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ripemd-160/. The authors are listed in prov/QEE7BH.jsonl.

import hashlib
import math

from ripemd_160 import K_LEFT, K_RIGHT, R_LEFT, R_RIGHT, hash160, ripemd160

# A. Bosselaers, "The hash function RIPEMD-160", https://homes.esat.kuleuven.be/~bosselae/ripemd160.html,
# section "Test vectors", copied by hand. The vector of one million "a" is left out for time.
BOSSELAERS = [
    (b"", "9c1185a5c5e9fc54612808977ee8f548b2258d31"),
    (b"a", "0bdc9d2d256b3ee9daae347be6f4dc835a467ffe"),
    (b"abc", "8eb208f7e05d987a9b044a8e98c6b087f15a0bfc"),
    (b"message digest", "5d0689ef49d2fae572b881b123a85ffa21595f36"),
    (b"abcdefghijklmnopqrstuvwxyz", "f71c27109c692c1b56bbdceb5b9d2865b3708dbc"),
    (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "12a053384a9c0c88e405a06c27dcf49ada62eb2b"),
    (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "b0e20b6e3116640286ed3a87a5713079b21f5189"),
    (b"1234567890" * 8, "9b752e45573d4b39f4dbd3323cab82bf63326bfb"),
]


def test_bosselaers_vectors() -> None:
    for msg, want in BOSSELAERS:
        assert ripemd160(msg).hex() == want, msg


def test_constants_from_roots() -> None:
    for j, p in enumerate((2, 3, 5, 7)):
        assert K_LEFT[j + 1] == math.isqrt(p << 60)  # floor(2^30 * sqrt(p))
        r = round((p << 90) ** (1 / 3))
        while r ** 3 > p << 90:
            r -= 1
        while (r + 1) ** 3 <= p << 90:
            r += 1
        assert K_RIGHT[j] == r  # floor(2^30 * cbrt(p))


def test_word_orders_are_permutations() -> None:
    for t in (R_LEFT, R_RIGHT):
        for r in range(5):
            assert sorted(t[16 * r:16 * r + 16]) == list(range(16))
    # The right line starts with pi(i) = 9i + 5 mod 16.
    assert R_RIGHT[:16] == [(9 * i + 5) % 16 for i in range(16)]


def test_bitcoin_hash160() -> None:
    # BIP 173, "Examples": the public key 0279BE66...F81798 gives the P2WPKH witness program
    # 751e76e8199196d454941c45d1b3a323f1433bd6, which is HASH160 of the key.
    pub = bytes.fromhex("0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")
    got = hash160(pub, lambda b: hashlib.sha256(b).digest())
    assert got.hex() == "751e76e8199196d454941c45d1b3a323f1433bd6"


def test_against_hashlib_if_available() -> None:
    try:
        h = hashlib.new("ripemd160")
    except ValueError:
        return  # some OpenSSL builds do not provide RIPEMD-160
    for n in (0, 1, 55, 56, 64, 100):
        msg = bytes((13 * i) & 255 for i in range(n))
        h = hashlib.new("ripemd160", msg)
        assert ripemd160(msg) == h.digest()
