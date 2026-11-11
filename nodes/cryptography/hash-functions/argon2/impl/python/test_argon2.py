# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/argon2/. The authors are listed in prov/3Y7XXB.jsonl.

import hashlib

import pytest

from argon2 import ARGON2D, ARGON2I, ARGON2ID, argon2, blake2b, h_prime, pre_hash


def h(s: str) -> bytes:
    return bytes.fromhex("".join(s.split()))


# RFC 9106, Section 5: the common inputs of the three test vectors.
P, S, K, X = b"\x01" * 32, b"\x02" * 16, b"\x03" * 8, b"\x04" * 12
T_COST, M_COST, LANES, TAG = 3, 32, 4, 32

VECTORS = {
    # Section 5.1 (Argon2d), 5.2 (Argon2i), 5.3 (Argon2id): pre-hashing digest, blocks, tag.
    ARGON2D: (
        """b8 81 97 91 a0 35 96 60 bb 77 09 c8 5f a4 8f 04 d5 d8 2c 05 c5 f2 15 cc db 88 54 91 71 7c f7 57
        08 2c 28 b9 51 be 38 14 10 b5 fc 2e b7 27 40 33 b9 fd c7 ae 67 2b ca ac 5d 17 90 97 a4 af 31 09""",
        [("db2fea6b2c6f5c8a", "6a6c49d2cb75d5b6"), ("d3801200410f8c0d", "2dbfff23f31b5883"),
         ("5f047b575c5ff4d2", "c341b3ca45c10da5")],
        "51 2b 39 1b 6f 11 62 97 53 71 d3 09 19 73 42 94 f8 68 e3 be 39 84 f3 c1 a1 3a 4d b9 fa be 4a cb",
    ),
    ARGON2I: (
        """c4 60 65 81 52 76 a0 b3 e7 31 73 1c 90 2f 1f d8 0c f7 76 90 7f bb 7b 6a 5c a7 2e 7b 56 01 1f ee
        ca 44 6c 86 dd 75 b9 46 9a 5e 68 79 de c4 b7 2d 08 63 fb 93 9b 98 2e 5f 39 7c c7 d1 64 fd da a9""",
        [("f8f9e84545db08f6", "c570f2ab2a86cf00"), ("b2e4ddfcf76dc85a", "421b3c6e9555b79d"),
         ("af2a8bd8482c2f11", "71e436f035f30ed0")],
        "c8 14 d9 d1 dc 7f 37 aa 13 f0 d7 7f 24 94 bd a1 c8 de 6b 01 6d d3 88 d2 99 52 a4 c4 67 2b 6c e8",
    ),
    ARGON2ID: (
        """28 89 de 48 7e b4 2a e5 00 c0 00 7e d9 25 2f 10 69 ea de c4 0d 57 65 b4 85 de 6d c2 43 7a 67 b8
        54 6a 2f 0a cc 1a 08 82 db 8f cf 74 71 4b 47 2e 94 df 42 1a 5d a1 11 2f fa 11 43 43 70 a1 e9 97""",
        [("6b2e09f10671bd43", "81f88b28683ea8e5"), ("3653ec9d01583df9", "a55222a93754c692"),
         ("942363968ce597a4", "0b012846a40f346a")],
        "0d 64 0d f5 8d 78 76 6c 08 c0 37 a3 4a 8b 53 c9 d0 1e f0 45 2d 75 b6 5e b5 25 20 e9 6b 01 e6 59",
    ),
}


def test_blake2b_rfc7693_appendix_a() -> None:
    want = h("""BA 80 A5 3F 98 1C 4D 0D 6A 27 97 B6 9F 12 F6 E9 4C 21 2F 14 68 5A C4 B7 4B 12 BB 6F DB FF A2 D1
    7D 87 C5 39 2A AB 79 2D C2 52 D5 DE 45 33 CC 95 18 D3 8A A8 DB F1 92 5A B9 23 86 ED D4 00 99 23""")
    assert blake2b(b"abc") == want


@pytest.mark.parametrize("n,nn", [(0, 64), (1, 32), (127, 64), (128, 16), (129, 64), (300, 7)])
def test_blake2b_against_hashlib(n: int, nn: int) -> None:
    data = bytes(range(256))[:n] if n <= 256 else bytes(i % 251 for i in range(n))
    assert blake2b(data, nn) == hashlib.blake2b(data, digest_size=nn).digest()


@pytest.mark.parametrize("y", [ARGON2D, ARGON2I, ARGON2ID])
def test_rfc9106_pre_hash(y: int) -> None:
    assert pre_hash(P, S, T_COST, M_COST, LANES, TAG, y, K, X) == h(VECTORS[y][0])


@pytest.mark.parametrize("y", [ARGON2D, ARGON2I, ARGON2ID])
def test_rfc9106_blocks_and_tag(y: int) -> None:
    trace: list = []
    tag = argon2(P, S, T_COST, M_COST, LANES, TAG, y, K, X, trace)
    for (first, last), (w_first, w_last) in zip(trace, VECTORS[y][1]):
        assert first[0] == int(w_first, 16)  # Block 0000 [  0] after the pass
        assert last[-1] == int(w_last, 16)  # Block 0031 [127] after the pass
    assert tag == h(VECTORS[y][2])


def test_h_prime_lengths_and_prefix() -> None:
    a = b"input"
    for t in (4, 32, 64, 65, 100, 1024):
        assert len(h_prime(a, t)) == t
    # For T > 64, the output starts with the first half of BLAKE2b-512(LE32(T) || A).
    assert h_prime(a, 100)[:32] == hashlib.blake2b((100).to_bytes(4, "little") + a).digest()[:32]


def test_wrong_inputs_change_the_tag() -> None:
    base = argon2(b"password", b"somesalt", 1, 8, 1, 16)
    assert argon2(b"passwore", b"somesalt", 1, 8, 1, 16) != base
    assert argon2(b"password", b"somesalu", 1, 8, 1, 16) != base
    assert argon2(b"password", b"somesalt", 2, 8, 1, 16) != base
    assert argon2(b"password", b"somesalt", 1, 16, 1, 16) != base
    assert argon2(b"password", b"somesalt", 1, 8, 1, 16, ARGON2I) != base
    assert argon2(b"password", b"somesalt", 1, 8, 1, 16, secret=b"pepper") != base
    assert argon2(b"password", b"somesalt", 1, 8, 1, 16) == base


def test_avalanche() -> None:
    a = argon2(b"password", b"somesalt", 1, 8, 1, 64)
    b = argon2(b"passwore", b"somesalt", 1, 8, 1, 64)
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    assert 200 <= diff <= 312  # about half of 512 bits


def test_bad_parameters() -> None:
    with pytest.raises(ValueError):
        argon2(b"p", b"s", 1, 7, 1, 32)  # m < 8p
    with pytest.raises(ValueError):
        argon2(b"p", b"s", 0, 8, 1, 32)  # t = 0
    with pytest.raises(ValueError):
        argon2(b"p", b"s", 1, 8, 1, 3)  # tag shorter than 4 bytes
