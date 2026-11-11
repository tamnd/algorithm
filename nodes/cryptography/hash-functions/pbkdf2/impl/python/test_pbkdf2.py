# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pbkdf2/. The authors are listed in prov/G2X3X9.jsonl.

import hashlib
import random

import pytest

from pbkdf2 import _HmacKey, pbkdf2, verify


@pytest.mark.parametrize(
    "p, s, c, dk_len, dk",
    [
        # RFC 6070, Section 2 (PBKDF2 HMAC-SHA1 Test Vectors). The vector with
        # c = 16777216 is left out because it takes minutes in pure Python.
        (b"password", b"salt", 1, 20, "0c60c80f961f0e71f3a9b524af6012062fe037a6"),
        (b"password", b"salt", 2, 20, "ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957"),
        (b"password", b"salt", 4096, 20, "4b007901b765489abead49d926f721d065a429c1"),
        (
            b"passwordPASSWORDpassword",
            b"saltSALTsaltSALTsaltSALTsaltSALTsalt",
            4096,
            25,
            "3d2eec4fe41c849b80c8d83662c0e44a8b291a964cf2f07038",
        ),
        (b"pass\0word", b"sa\0lt", 4096, 16, "56fa6aa75548099dcc37d7f03425e0c3"),
    ],
)
def test_rfc6070_sha1(p: bytes, s: bytes, c: int, dk_len: int, dk: str) -> None:
    assert pbkdf2(p, s, c, dk_len, "sha1").hex() == dk


@pytest.mark.parametrize(
    "p, s, c, dk",
    [
        # RFC 7914, Section 11 (Test Vectors for PBKDF2 with HMAC-SHA-256), dkLen = 64.
        (
            b"passwd",
            b"salt",
            1,
            "55ac046e56e3089fec1691c22544b605f94185216dde0465e68b9d57c20dacbc"
            "49ca9cccf179b645991664b39d77ef317c71b845b1e30bd509112041d3a19783",
        ),
        (
            b"Password",
            b"NaCl",
            80000,
            "4ddcd8f60b98be21830cee5ef22701f9641a4418d04c0414aeff08876b34ab56"
            "a1d425a1225833549adb841b51c9b3176a272bdebba1d078478f62b397f33c8d",
        ),
    ],
)
def test_rfc7914_sha256(p: bytes, s: bytes, c: int, dk: str) -> None:
    assert pbkdf2(p, s, c, 64, "sha256").hex() == dk


def test_against_hashlib() -> None:
    # Second check only: the stdlib pbkdf2_hmac.
    rng = random.Random(1)
    for name in ("sha1", "sha256", "sha512", "sha3_256"):
        for _ in range(4):
            p = rng.randbytes(rng.randrange(0, 200))  # also longer than one block
            s = rng.randbytes(rng.randrange(0, 40))
            c = rng.randrange(1, 50)
            n = rng.randrange(1, 150)  # several blocks T_i
            assert pbkdf2(p, s, c, n, name) == hashlib.pbkdf2_hmac(name, p, s, c, n)


def test_hmac_against_stdlib() -> None:
    import hmac as std_hmac

    k, m = b"key" * 30, b"message"
    assert _HmacKey(k, "sha256").mac(m) == std_hmac.new(k, m, "sha256").digest()


def test_verify_and_wrong_password() -> None:
    stored = pbkdf2(b"correct horse", b"NaCl", 100, 32)
    assert verify(b"correct horse", b"NaCl", 100, stored)
    assert not verify(b"correct horsf", b"NaCl", 100, stored)
    assert not verify(b"correct horse", b"NaCm", 100, stored)  # wrong salt
    assert not verify(b"correct horse", b"NaCl", 101, stored)  # wrong count


def test_prefix_property() -> None:
    # Output blocks are independent, so a shorter key is a prefix of a longer one.
    assert pbkdf2(b"pw", b"s", 5, 80)[:30] == pbkdf2(b"pw", b"s", 5, 30)


def test_long_password_equals_its_hash() -> None:
    # HMAC hashes keys longer than the block size, so these two passwords collide.
    long_pw = b"x" * 100
    short_pw = hashlib.sha256(long_pw).digest()
    assert pbkdf2(long_pw, b"salt", 3, 32) == pbkdf2(short_pw, b"salt", 3, 32)


def test_avalanche() -> None:
    rng = random.Random(2)
    total, trials = 0, 100
    for _ in range(trials):
        p = bytearray(rng.randbytes(10))
        a = int.from_bytes(pbkdf2(bytes(p), b"salt", 2, 32), "big")
        p[rng.randrange(10)] ^= 1 << rng.randrange(8)
        b = int.from_bytes(pbkdf2(bytes(p), b"salt", 2, 32), "big")
        total += bin(a ^ b).count("1")
    assert 118 < total / trials < 138  # about 128 of 256 bits
