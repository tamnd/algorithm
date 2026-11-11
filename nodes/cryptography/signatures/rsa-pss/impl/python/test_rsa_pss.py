# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-pss/. The authors are listed in prov/CWNPMK.jsonl.
"""Tests for RSASSA-PSS with the RSA Laboratories vectors (pss-vect.txt)."""

import pytest

from rsa_pss import PrivateKey, emsa_pss_encode, emsa_pss_verify, generate_key, sign, verify


def hi(s: str) -> int:
    return int.from_bytes(bytes.fromhex(s), "big")


# pss-vect.txt, "Example 1: A 1024-bit RSA key pair" (the same key as Example 1
# of the PKCS #1 v1.5 vectors). Hash SHA-1, MGF1 with SHA-1, salt of 20 bytes.
EX1 = PrivateKey(
    n=hi("a5 6e 4a 0e 70 10 17 58 9a 51 87 dc 7e a8 41 d1 56 f2 ec 0e 36 ad 52 a4 4d fe b1 e6 1f 7a d9 91"
         "d8 c5 10 56 ff ed b1 62 b4 c0 f2 83 a1 2a 88 a3 94 df f5 26 ab 72 91 cb b3 07 ce ab fc e0 b1 df"
         "d5 cd 95 08 09 6d 5b 2b 8b 6d f5 d6 71 ef 63 77 c0 92 1c b2 3c 27 0a 70 e2 59 8e 6f f8 9d 19 f1"
         "05 ac c2 d3 f0 cb 35 f2 92 80 e1 38 6b 6f 64 c4 ef 22 e1 e1 f2 0d 0c e8 cf fb 22 49 bd 9a 21 37"),
    e=0x010001,
    d=hi("33 a5 04 2a 90 b2 7d 4f 54 51 ca 9b bb d0 b4 47 71 a1 01 af 88 43 40 ae f9 88 5f 2a 4b be 92 e8"
         "94 a7 24 ac 3c 56 8c 8f 97 85 3a d0 7c 02 66 c8 c6 a3 ca 09 29 f1 e8 f1 12 31 88 44 29 fc 4d 9a"
         "e5 5f ee 89 6a 10 ce 70 7c 3e d7 e7 34 e4 47 27 a3 95 74 50 1a 53 26 83 10 9c 2a ba ca ba 28 3c"
         "31 b4 bd 2f 53 c3 ee 37 e3 52 ce e3 4f 9e 50 3b d8 0c 06 22 ad 79 c6 dc ee 88 35 47 c6 a3 b3 25"),
    p=hi("e7 e8 94 27 20 a8 77 51 72 73 a3 56 05 3e a2 a1 bc 0c 94 aa 72 d5 5c 6e 86 29 6b 2d fc 96 79 48"
         "c0 a7 2c bc cc a7 ea cb 35 70 6e 09 a1 df 55 a1 53 5b d9 b3 cc 34 16 0b 3b 6d cd 3e da 8e 64 43"),
    q=hi("b6 9d ca 1c f7 d4 d7 ec 81 e7 5b 90 fc ca 87 4a bc de 12 3f d2 70 01 80 aa 90 47 9b 6e 48 de 8d"
         "67 ed 24 f9 f1 9d 85 ba 27 58 74 f5 42 cd 20 dc 72 3e 69 63 36 4a 1f 94 25 45 2b 26 9a 67 99 fd"),
)

# pss-vect.txt, "PSS Example 1.2".
EX12_MSG = bytes.fromhex("85 13 84 cd fe 81 9c 22 ed 6c 4c cb 30 da eb 5c f0 59 bc 8e 11 66 b7 e3 53 0c 4c 23"
                         "3e 2b 5f 8f 71 a1 cc a5 82 d4 3e cc 72 b1 bc a1 6d fc 70 13 22 6b 9e")
EX12_SALT = bytes.fromhex("ef 28 69 fa 40 c3 46 cb 18 3d ab 3d 7b ff c9 8f d5 6d f4 2d")
EX12_SIG = bytes.fromhex("3e f7 f4 6e 83 1b f9 2b 32 27 41 42 a5 85 ff ce fb dc a7 b3 2a e9 0d 10 fb 0f 0c 72"
                         "99 84 f0 4e f2 9a 9d f0 78 07 75 ce 43 73 9b 97 83 83 90 db 0a 55 05 e6 3d e9 27 02"
                         "8d 9d 29 b2 19 ca 2c 45 17 83 25 58 a5 5d 69 4a 6d 25 b9 da b6 60 03 c4 cc cd 90 78"
                         "02 19 3b e5 17 0d 26 14 7d 37 b9 35 90 24 1b e5 1c 25 05 5f 47 ef 62 75 2c fb e2 14"
                         "18 fa fe 98 c2 2c 4d 4d 47 72 4f db 56 69 e8 43")

# pss-vect.txt, "Example 2: A 1025-bit RSA key pair" (public key) and "PSS Example 2.1".
# With 1025 binary digits, emLen = 128 is one byte shorter than the signature.
EX2_N = hi("01 d4 0c 1b cf 97 a6 8a e7 cd bd 8a 7b f3 e3 4f a1 9d cc a4 ef 75 a4 74 54 37 5f 94 51 4d 88 fe"
           "d0 06 fb 82 9f 84 19 ff 87 d6 31 5d a6 8a 1f f3 a0 93 8e 9a bb 34 64 01 1c 30 3a d9 91 99 cf 0c"
           "7c 7a 8b 47 7d ce 82 9e 88 44 f6 25 b1 15 e5 e9 c4 a5 9c f8 f8 11 3b 68 34 33 6a 2f d2 68 9b 47"
           "2c bb 5e 5c ab e6 74 35 0c 59 b6 c1 7e 17 68 74 fb 42 f8 fc 3d 17 6a 01 7e dc 61 fd 32 6c 4b 33 c9")
EX21_MSG = bytes.fromhex("da ba 03 20 66 26 3f ae db 65 98 48 11 52 78 a5 2c 44 fa a3 a7 6f 37 51 5e d3 36 32"
                         "10 72 c4 0a 9d 9b 53 bc 05 01 40 78 ad f5 20 87 51 46 aa e7 0f f0 60 22 6d cb 7b 1f"
                         "1f c2 7e 93 60")
EX21_SIG = bytes.fromhex("01 4c 5b a5 33 83 28 cc c6 e7 a9 0b f1 c0 ab 3f d6 06 ff 47 96 d3 c1 2e 4b 63 9e d9"
                         "13 6a 5f ec 6c 16 d8 88 4b dd 99 cf dc 52 14 56 b0 74 2b 73 68 68 cf 90 de 09 9a db"
                         "8d 5f fd 1d ef f3 9b a4 00 7a b7 46 ce fd b2 2d 7d f0 e2 25 f5 46 27 dc 65 46 61 31"
                         "72 1b 90 af 44 53 63 a8 35 8b 9f 60 76 42 f7 8f ab 0a b0 f4 3b 71 68 d6 4b ae 70 d8"
                         "82 78 48 d8 ef 1e 42 1c 57 54 dd f4 2c 25 89 b5 b3")


def test_example_1_2_sign_with_given_salt() -> None:
    assert EX1.p * EX1.q == EX1.n
    assert sign(EX1, EX12_MSG, "sha1", salt=EX12_SALT) == EX12_SIG
    assert verify(EX1.n, EX1.e, EX12_MSG, EX12_SIG, "sha1", s_len=20)


def test_example_1_2_changed_salt_or_message() -> None:
    other_salt = bytes([EX12_SALT[0] ^ 1]) + EX12_SALT[1:]
    s2 = sign(EX1, EX12_MSG, "sha1", salt=other_salt)
    assert s2 != EX12_SIG
    assert verify(EX1.n, EX1.e, EX12_MSG, s2, "sha1", s_len=20)  # a new salt gives a new valid signature
    assert not verify(EX1.n, EX1.e, EX12_MSG[:-1], EX12_SIG, "sha1", s_len=20)
    assert not verify(EX1.n, EX1.e, EX12_MSG + b"\x00", EX12_SIG, "sha1", s_len=20)
    assert not verify(EX1.n, EX1.e, EX12_MSG, EX12_SIG, "sha1", s_len=19)
    assert not verify(EX1.n, EX1.e, EX12_MSG, EX12_SIG, "sha256", s_len=20)


def test_example_2_1_verify_1025_bit_modulus() -> None:
    assert EX2_N.bit_length() == 1025 and len(EX21_SIG) == 129
    assert verify(EX2_N, 0x010001, EX21_MSG, EX21_SIG, "sha1", s_len=20)
    bad = bytearray(EX21_SIG)
    bad[64] ^= 0x10
    assert not verify(EX2_N, 0x010001, EX21_MSG, bytes(bad), "sha1", s_len=20)


def test_bit_flips_rejected() -> None:
    for i in range(0, 1024, 61):
        bad = bytearray(EX12_SIG)
        bad[i // 8] ^= 1 << (i % 8)
        assert not verify(EX1.n, EX1.e, EX12_MSG, bytes(bad), "sha1", s_len=20)


def test_sha256_round_trips_and_salt_lengths() -> None:
    key = generate_key(1024, seed=9)
    for s_len in (0, 20, 32, 62):
        for msg in (b"", b"abc", bytes(1000)):
            sig = sign(key, msg, "sha256", s_len=s_len)
            assert verify(key.n, key.e, msg, sig, "sha256", s_len=s_len)
    # Randomized: two signatures on the same message differ, both verify.
    a, b = sign(key, b"m"), sign(key, b"m")
    assert a != b and verify(key.n, key.e, b"m", a) and verify(key.n, key.e, b"m", b)
    # emLen = 128 bytes, hLen = 32: the largest salt is 128 - 32 - 2 = 94 bytes.
    sign(key, b"m", s_len=94)
    with pytest.raises(ValueError):
        sign(key, b"m", s_len=95)


def test_zero_salt_is_deterministic() -> None:
    key = generate_key(1024, seed=9)
    assert sign(key, b"m", s_len=0) == sign(key, b"m", s_len=0)


def test_encoding_structure() -> None:
    em = emsa_pss_encode(b"x", 1023, "sha256", salt=bytes(32))
    assert len(em) == 128 and em[-1] == 0xBC and em[0] < 0x80
    assert emsa_pss_verify(b"x", em, 1023, "sha256", 32)
    bad = bytearray(em)
    bad[0] |= 0x80  # the cleared top bit must stay zero
    assert not emsa_pss_verify(b"x", bytes(bad), 1023, "sha256", 32)
