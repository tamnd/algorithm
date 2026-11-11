# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-signature/. The authors are listed in prov/PEKVQA.jsonl.
"""Tests for RSASSA-PKCS1-v1_5 with official vectors, the textbook forgery
and the CRT fault attack. All attacks run on local keys."""

import math

import pytest

from rsa_signature import (
    PrivateKey,
    emsa_pkcs1_v15_encode,
    generate_key,
    os2ip,
    rsasp1_crt,
    sign,
    sign_checked,
    textbook_sign,
    textbook_verify,
    verify,
)


def h(s: str) -> bytes:
    return bytes.fromhex(s)


def hi(s: str) -> int:
    return int.from_bytes(bytes.fromhex(s), "big")


# RSA Laboratories, pkcs1v15sign-vectors.txt (PKCS #1 v2.1 test vectors),
# "Example 1: A 1024-bit RSA key pair". The digest is SHA-1.
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
    dp=hi("28 fa 13 93 86 55 be 1f 8a 15 9c ba ca 5a 72 ea 19 0c 30 08 9e 19 cd 27 4a 55 6f 36 c4 f6 e1 9f"
          "55 4b 34 c0 77 79 04 27 bb dd 8d d3 ed e2 44 83 28 f3 85 d8 1b 30 e8 e4 3b 2f ff a0 27 86 19 79"),
    dq=hi("1a 8b 38 f3 98 fa 71 20 49 89 8d 7f b7 9e e0 a7 76 68 79 12 99 cd fa 09 ef c0 e5 07 ac b2 1e d7"
          "43 01 ef 5b fd 48 be 45 5e ae b6 e1 67 82 55 82 75 80 a8 e4 e8 e1 41 51 d1 51 0a 82 a3 f2 e7 29"),
    qinv=hi("27 15 6a ba 41 26 d2 4a 81 f3 a5 28 cb fb 27 f5 68 86 f8 40 a9 f6 e8 6e 17 a4 4b 94 fe 93 19 58"
            "4b 8e 22 fd de 1e 5a 2e 3b d8 aa 5b a8 d8 58 41 94 eb 21 90 ac f8 32 b8 47 f1 3a 3d 24 a7 9f 4d"),
)

# pkcs1v15sign-vectors.txt, "PKCS#1 v1.5 Signature Example 1.17" and "Example 1.18".
VECTORS_EX1 = [
    (
        h("eb 1e 59 35"),
        h("37 0c b9 83 9a e6 07 4f 84 b2 ac d6 e6 f6 b7 92 1b 4b 52 34 63 75 7f 64 46 71 61 40 c4 e6 c0 e7"
          "5b ec 6a d0 19 7e bf a8 6b f4 6d 09 4f 5f 6c d3 6d ca 3a 5c c7 3c 8b bb 70 e2 c7 c9 ab 5d 96 4e"
          "c8 e3 df de 48 1b 4a 1b ef fd 01 b4 ad 15 b3 1a e7 ae bb 9b 70 34 4a 94 11 08 31 65 fd f9 c3 75"
          "4b bb 8b 94 dd 34 bd 48 13 df ad a1 f6 93 7d e4 26 7d 55 97 ca 09 a3 1e 83 d7 f1 a7 9d d1 9b 5e"),
    ),
    (
        h("63 46 b1 53 e8 89 c8 22 82 09 63 00 71 c8 a5 77 83 f3 68 76 0b 8e b9 08 cf c2 b2 76"),
        h("24 79 c9 75 c5 b1 ae 4c 4e 94 0f 47 3a 90 45 b8 bf 5b 0b fc a7 8e c2 9a 38 df be dc 8a 74 9b 7a"
          "26 92 f7 c5 2d 5b c7 c8 31 c7 23 23 72 a0 0f ed 3b 6b 49 e7 60 ec 99 e0 74 ff 2e ea d5 13 4e 83"
          "05 72 5d fa 39 21 2b 84 bd 4b 8d 80 bc 8b c1 7a 51 28 23 a3 be b1 8f c0 8e 45 ed 19 c2 6c 81 77"
          "07 d6 7f b0 58 32 ef 1f 12 a3 3e 90 cd 93 b8 a7 80 31 9e 29 63 ca 25 a2 af 7b 09 ad 8f 59 5c 21"),
    ),
]

# NIST CAVP, SigGen15_186-3.rsp (CAVS 10.1, "SigGen PKCS#1 Ver 1.5"),
# section [mod = 1024], the first entry with SHAAlg = SHA256. Public key only.
NIST_N = hi("a3ecf80ff1804833c36a89a1583f58ef3332476a50a153e73ced17796139636045c131a6b17222ba8848f70150b18dfa"
            "390bfb1670ae982dfbc311fd0ede055564687af3805ca883944bb5ac9ec19b0e0cfbd9a314d70b17080c3d49b50cbf"
            "417062eb41bd639d67a5fb330ec55a0489fee08eeec97ed487c114b20393fe0aef")
NIST_E = 0x1001
NIST_MSG = h("dfce08b64b9ea4014947012670548da4ceeee084dbfe509aac92bf096982b8050153bbdd1c5bd4385226729e9a19773b"
             "05558ce0acdfb74be6fd2fa8bfe36f58a68e89f066f1bd85584f4a27d6e884abf2d727ae683bebd6d295585b1b71dc"
             "c636491bf910a68670c3882fc60c08db7bff3c59f4f95b13c3d721e329657528d9")
NIST_S = h("8D9D30A87DF0C2F6CD651FCAF2B9AC1296287AD3D4B03132E330F08AB701FC197040D0A261F631E7E34478B592551E1F"
           "682395C9E2B54C8CE8B0C72C1B5A79748CC34F9152730A7F67FAE1225A4CE750F1D5D4E288176DF197E7503C88B5BA"
           "ECEF3ABCF2875F111E6D7F7B4DC8AFA2ED3C1D7AD8E7CF45A77F0B1CB178518402")


def test_vector_key_is_consistent() -> None:
    k = EX1
    assert k.p * k.q == k.n
    assert k.dp == k.d % (k.p - 1) and k.dq == k.d % (k.q - 1)
    assert k.qinv * k.q % k.p == 1


@pytest.mark.parametrize("msg,sig", VECTORS_EX1)
def test_pkcs1_vectors_sign_and_verify(msg: bytes, sig: bytes) -> None:
    assert sign(EX1, msg, "sha1") == sig
    assert verify(EX1.n, EX1.e, msg, sig, "sha1")


def test_nist_sha256_verify_vector() -> None:
    assert verify(NIST_N, NIST_E, NIST_MSG, NIST_S, "sha256")
    assert not verify(NIST_N, NIST_E, NIST_MSG + b"\x00", NIST_S, "sha256")
    assert not verify(NIST_N, NIST_E, NIST_MSG, NIST_S, "sha1")


def test_encoding_layout() -> None:
    em = emsa_pkcs1_v15_encode(b"abc", 128, "sha256")
    assert em[:2] == b"\x00\x01" and len(em) == 128
    assert em[2:128 - 52] == b"\xff" * (128 - 54) and em[128 - 52] == 0
    with pytest.raises(ValueError):
        emsa_pkcs1_v15_encode(b"abc", 64, "sha512")  # 64 < 83 + 11


def test_round_trip_and_rejections() -> None:
    key = generate_key(1024, seed=7)
    assert key.n.bit_length() == 1024 and key.e * key.d % math.lcm(key.p - 1, key.q - 1) == 1
    for name in ("sha256", "sha384", "sha512"):
        for msg in (b"", b"hello", bytes(range(200))):
            s = sign(key, msg, name)
            assert verify(key.n, key.e, msg, s, name)
    s = sign(key, b"pay 10", "sha256")
    assert not verify(key.n, key.e, b"pay 11", s)
    for i in range(0, 8 * len(s), 97):
        bad = bytearray(s)
        bad[i // 8] ^= 1 << (i % 8)
        assert not verify(key.n, key.e, b"pay 10", bytes(bad))
    assert not verify(key.n, key.e, b"pay 10", s[1:])
    # Values s >= N are out of range and rejected (L12), even when s mod N verifies.
    assert not verify(key.n, key.e, b"pay 10", key.n.to_bytes(128, "big"))
    if os2ip(s) + key.n < 256**128:
        assert not verify(key.n, key.e, b"pay 10", (os2ip(s) + key.n).to_bytes(128, "big"))


def test_crt_equals_plain_exponentiation() -> None:
    key = generate_key(1024, seed=3)
    for m in (0, 1, 2, key.n - 1, 123456789 ** 7 % key.n):
        assert rsasp1_crt(key, m) == pow(m, key.d, key.n)


def test_textbook_rsa_multiplicative_forgery() -> None:
    key = generate_key(1024, seed=11)
    m1, m2 = 1234567, 7654321
    s1, s2 = textbook_sign(key, m1), textbook_sign(key, m2)
    forged = s1 * s2 % key.n
    assert textbook_verify(key.n, key.e, m1 * m2 % key.n, forged)
    # The same trick fails against PKCS #1 v1.5: the product of two
    # signatures does not verify for any of the messages tried.
    a, b = sign(key, b"m1"), sign(key, b"m2")
    prod = (os2ip(a) * os2ip(b) % key.n).to_bytes(128, "big")
    assert not any(verify(key.n, key.e, msg, prod) for msg in (b"m1", b"m2", b"m1m2", b""))


def test_crt_fault_attack_and_countermeasure() -> None:
    key = generate_key(1024, seed=5)
    msg = b"firmware v2"
    m = os2ip(emsa_pkcs1_v15_encode(msg, 128))
    faulty = rsasp1_crt(key, m, fault=lambda s1: s1 ^ 1)
    # Boneh, DeMillo and Lipton with Lenstra's remark: one faulty signature
    # and the public key reveal the factor q.
    g = math.gcd((pow(faulty, key.e, key.n) - m) % key.n, key.n)
    assert g == key.q
    with pytest.raises(RuntimeError):
        sign_checked(key, msg, fault=lambda s1: s1 ^ 1)
    assert verify(key.n, key.e, msg, sign_checked(key, msg))
