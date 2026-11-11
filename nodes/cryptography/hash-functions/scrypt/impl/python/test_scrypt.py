# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scrypt/. The authors are listed in prov/1CM1NZ.jsonl.

import hashlib

import pytest

from scrypt import block_mix, pbkdf2_sha256_1, ro_mix, ro_mix_low_memory, salsa20_8, scrypt


def h(s: str) -> bytes:
    return bytes.fromhex("".join(s.split()))


# RFC 7914, Section 8 (Test Vectors for Salsa20/8 Core).
SALSA_IN = h("""7e 87 9a 21 4f 3e c9 86 7c a9 40 e6 41 71 8f 26 ba ee 55 5b 8c 61 c1 b5 0d f8 46 11 6d cd 3b 1d
ee 24 f3 19 df 9b 3d 85 14 12 1e 4b 5a c5 aa 32 76 02 1d 29 09 c7 48 29 ed eb c6 8d b8 b8 c2 5e""")
SALSA_OUT = h("""a4 1f 85 9c 66 08 cc 99 3b 81 ca cb 02 0c ef 05 04 4b 21 81 a2 fd 33 7d fd 7b 1c 63 96 68 2f 29
b4 39 31 68 e3 c9 e6 bc fe 6b c5 b7 a0 6d 96 ba e4 24 cc 10 2c 91 74 5c 24 ad 67 3d c7 61 8f 81""")

# RFC 7914, Section 9 (Test Vectors for scryptBlockMix), r = 1, and Section 10 (scryptROMix), r = 1, N = 16.
MIX_IN = h("""f7 ce 0b 65 3d 2d 72 a4 10 8c f5 ab e9 12 ff dd 77 76 16 db bb 27 a7 0e 82 04 f3 ae 2d 0f 6f ad
89 f6 8f 48 11 d1 e8 7b cc 3b d7 40 0a 9f fd 29 09 4f 01 84 63 95 74 f3 9a e5 a1 31 52 17 bc d7
89 49 91 44 72 13 bb 22 6c 25 b5 4d a8 63 70 fb cd 98 43 80 37 46 66 bb 8f fc b5 bf 40 c2 54 b0
67 d2 7c 51 ce 4a d5 fe d8 29 c9 0b 50 5a 57 1b 7f 4d 1c ad 6a 52 3c da 77 0e 67 bc ea af 7e 89""")
BLOCKMIX_OUT = h("""a4 1f 85 9c 66 08 cc 99 3b 81 ca cb 02 0c ef 05 04 4b 21 81 a2 fd 33 7d fd 7b 1c 63 96 68 2f 29
b4 39 31 68 e3 c9 e6 bc fe 6b c5 b7 a0 6d 96 ba e4 24 cc 10 2c 91 74 5c 24 ad 67 3d c7 61 8f 81
20 ed c9 75 32 38 81 a8 05 40 f6 4c 16 2d cd 3c 21 07 7c fe 5f 8d 5f e2 b1 a4 16 8f 95 36 78 b7
7d 3b 3d 80 3b 60 e4 ab 92 09 96 e5 9b 4d 53 b6 5d 2a 22 58 77 d5 ed f5 84 2c b9 f1 4e ef e4 25""")
ROMIX_OUT = h("""79 cc c1 93 62 9d eb ca 04 7f 0b 70 60 4b f6 b6 2c e3 dd 4a 96 26 e3 55 fa fc 61 98 e6 ea 2b 46
d5 84 13 67 3b 99 b0 29 d6 65 c3 57 60 1f b4 26 a0 b2 f4 bb a2 00 ee 9f 0a 43 d1 9b 57 1a 9c 71
ef 11 42 e6 5d 5a 26 6f dd ca 83 2c e5 9f aa 7c ac 0b 9c f1 be 2b ff ca 30 0d 01 ee 38 76 19 c4
ae 12 fd 44 38 f2 03 a0 e4 e1 c4 7e c3 14 86 1f 4e 90 87 cb 33 39 6a 68 73 e8 f9 d2 53 9a 4b 8e""")

# RFC 7914, Section 11, first vector: PBKDF2-HMAC-SHA-256(P="passwd", S="salt", c=1, dkLen=64).
PBKDF2_OUT = h("""55 ac 04 6e 56 e3 08 9f ec 16 91 c2 25 44 b6 05 f9 41 85 21 6d de 04 65 e6 8b 9d 57 c2 0d ac bc
49 ca 9c cc f1 79 b6 45 99 16 64 b3 9d 77 ef 31 7c 71 b8 45 b1 e3 0b d5 09 11 20 41 d3 a1 97 83""")

# RFC 7914, Section 12, first vector: scrypt(P="", S="", N=16, r=1, p=1, dkLen=64).
SCRYPT_1 = h("""77 d6 57 62 38 65 7b 20 3b 19 ca 42 c1 8a 04 97 f1 6b 48 44 e3 07 4a e8 df df fa 3f ed e2 14 42
fc d0 06 9d ed 09 48 f8 32 6a 75 3a 0f c8 1f 17 e8 d3 e0 fb 2e 0d 36 28 cf 35 e2 0c 38 d1 89 06""")


def test_salsa20_8_core() -> None:
    assert salsa20_8(SALSA_IN) == SALSA_OUT


def test_block_mix() -> None:
    assert block_mix(MIX_IN, 1) == BLOCKMIX_OUT


def test_ro_mix() -> None:
    assert ro_mix(MIX_IN, 16, 1) == ROMIX_OUT


def test_pbkdf2_one_iteration() -> None:
    assert pbkdf2_sha256_1(b"passwd", b"salt", 64) == PBKDF2_OUT
    assert pbkdf2_sha256_1(b"passwd", b"salt", 64) == hashlib.pbkdf2_hmac("sha256", b"passwd", b"salt", 1, 64)


def test_scrypt_rfc7914_vector_1() -> None:
    assert scrypt(b"", b"", 16, 1, 1, 64) == SCRYPT_1


def test_first_vector_intermediates_chain_together() -> None:
    # The RFC says the Section 10 input is the first scrypt vector's B, so L1 must produce it.
    assert pbkdf2_sha256_1(b"", b"", 128) == MIX_IN


@pytest.mark.skipif(not hasattr(hashlib, "scrypt"), reason="hashlib.scrypt needs OpenSSL")
@pytest.mark.parametrize("pw,salt,n,r,p,dk", [
    (b"password", b"NaCl", 32, 2, 2, 40),
    (b"pleaseletmein", b"SodiumChloride", 64, 1, 3, 17),
    (b"x" * 100, b"", 8, 3, 1, 64),
])
def test_against_hashlib_scrypt(pw: bytes, salt: bytes, n: int, r: int, p: int, dk: int) -> None:
    assert scrypt(pw, salt, n, r, p, dk) == hashlib.scrypt(pw, salt=salt, n=n, r=r, p=p, dklen=dk)


@pytest.mark.parametrize("k", [1, 2, 4, 16])
def test_low_memory_romix_trade_off(k: int) -> None:
    n = 16
    out, calls = ro_mix_low_memory(MIX_IN, n, 1, k)
    assert out == ROMIX_OUT
    assert calls >= 2 * n
    if k == 1:
        assert calls == 2 * n
    assert calls <= 2 * n + n * (k - 1)


def test_wrong_password_and_parameters_fail() -> None:
    good = scrypt(b"password", b"NaCl", 16, 1, 1, 32)
    assert scrypt(b"passwore", b"NaCl", 16, 1, 1, 32) != good
    assert scrypt(b"password", b"NaCm", 16, 1, 1, 32) != good
    assert scrypt(b"password", b"NaCl", 32, 1, 1, 32) != good
    assert scrypt(b"password", b"NaCl", 16, 2, 1, 32) != good
    assert scrypt(b"password", b"NaCl", 16, 1, 2, 32) != good


def test_avalanche() -> None:
    a = scrypt(b"password", b"NaCl", 16, 1, 1, 64)
    b = scrypt(b"passwore", b"NaCl", 16, 1, 1, 64)
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    assert 200 <= diff <= 312  # about half of 512 bits


def test_bad_parameters() -> None:
    for n in (0, 1, 3, 24):
        with pytest.raises(ValueError):
            scrypt(b"", b"", n, 1, 1, 16)
