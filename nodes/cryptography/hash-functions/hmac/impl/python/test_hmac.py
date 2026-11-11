# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmac/. The authors are listed in prov/02765M.jsonl.

import hashlib
import importlib.util
import os
import random
import sysconfig
from types import ModuleType

import pytest


def _load(name: str, path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Our file is named hmac.py, like the standard module, so load both by path.
impl = _load("hmac_impl", os.path.join(os.path.dirname(os.path.abspath(__file__)), "hmac.py"))
std_hmac = _load("std_hmac", os.path.join(sysconfig.get_paths()["stdlib"], "hmac.py"))

hmac_digest = impl.hmac_digest
hmac_truncated = impl.hmac_truncated
hmac_verify = impl.hmac_verify
tags_equal = impl.tags_equal

K6 = "aa" * 131
D6 = b"Test Using Larger Than Block-Size Key - Hash Key First"
D7 = (
    b"This is a test using a larger than block-size key and a larger than block-size data. "
    b"The key needs to be hashed before being used by the HMAC algorithm."
)

# RFC 4231, Section 4.2 to 4.8, Test Cases 1 to 7 (Test Case 5 is in a separate test).
# Each row: case number, key (hex), data, then HMAC-SHA-224, -256, -384, -512.
RFC4231 = [
    (
        1,
        "0b" * 20,
        b"Hi There",
        "896fb1128abbdf196832107cd49df33f47b4b1169912ba4f53684b22",
        "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7",
        "afd03944d84895626b0825f4ab46907f15f9dadbe4101ec682aa034c7cebc59cfaea9ea9076ede7f4af152e8b2fa9cb6",
        "87aa7cdea5ef619d4ff0b4241a1d6cb02379f4e2ce4ec2787ad0b30545e17cde"
        "daa833b7d6b8a702038b274eaea3f4e4be9d914eeb61f1702e696c203a126854",
    ),
    (
        2,
        b"Jefe".hex(),
        b"what do ya want for nothing?",
        "a30e01098bc6dbbf45690f3a7e9e6d0f8bbea2a39e6148008fd05e44",
        "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843",
        "af45d2e376484031617f78d2b58a6b1b9c7ef464f5a01b47e42ec3736322445e8e2240ca5e69e2c78b3239ecfab21649",
        "164b7a7bfcf819e2e395fbe73b56e0a387bd64222e831fd610270cd7ea250554"
        "9758bf75c05a994a6d034f65f8f0e6fdcaeab1a34d4a6b4b636e070a38bce737",
    ),
    (
        3,
        "aa" * 20,
        b"\xdd" * 50,
        "7fb3cb3588c6c1f6ffa9694d7d6ad2649365b0c1f65d69d1ec8333ea",
        "773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe",
        "88062608d3e6ad8a0aa2ace014c8a86f0aa635d947ac9febe83ef4e55966144b2a5ab39dc13814b94e3ab6e101a34f27",
        "fa73b0089d56a284efb0f0756c890be9b1b5dbdd8ee81a3655f83e33b2279d39"
        "bf3e848279a722c806b485a47e67c807b946a337bee8942674278859e13292fb",
    ),
    (
        4,
        "0102030405060708090a0b0c0d0e0f10111213141516171819",
        b"\xcd" * 50,
        "6c11506874013cac6a2abc1bb382627cec6a90d86efc012de7afec5a",
        "82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b",
        "3e8a69b7783c25851933ab6290af6ca77a9981480850009cc5577c6e1f573b4e6801dd23c4a7d679ccf8a386c674cffb",
        "b0ba465637458c6990e5a8c5f61d4af7e576d97ff94b872de76f8050361ee3db"
        "a91ca5c11aa25eb4d679275cc5788063a5f19741120c4f2de2adebeb10a298dd",
    ),
    (
        6,
        K6,
        D6,
        "95e9a0db962095adaebe9b2d6f0dbce2d499f112f2d2b7273fa6870e",
        "60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54",
        "4ece084485813e9088d2c63a041bc5b44f9ef1012a2b588f3cd11f05033ac4c60c2ef6ab4030fe8296248df163f44952",
        "80b24263c7c1a3ebb71493c1dd7be8b49b46d1f41b4aeec1121b013783f8f352"
        "6b56d037e05f2598bd0fd2215d6a1e5295e64f73f63f0aec8b915a985d786598",
    ),
    (
        7,
        K6,
        D7,
        "3a854166ac5d9f023f54d517d0b39dbd946770db9c2b95c9f6f565d1",
        "9b09ffa71b942fcb27635fbcd5b0e944bfdc63644f0713938a7f51535c3a35e2",
        "6617178e941f020d351e2f254e8fd32c602420feb0b8fb9adccebb82461e99c5a678cc31e799176d3860e6110c46523e",
        "e37b6a775dc87dbaa4dfa9f96e5e3ffddebd71f8867289865df5a32d20cdc944"
        "b6022cac3c4982b10d5eeb55c3e4de15134676fb6de0446065c97440fa8c6a58",
    ),
]


@pytest.mark.parametrize("case", RFC4231, ids=lambda c: f"rfc4231-case{c[0]}")
def test_rfc4231(case: tuple[int, str, bytes, str, str, str, str]) -> None:
    _, key_hex, data, t224, t256, t384, t512 = case
    key = bytes.fromhex(key_hex)
    assert hmac_digest(key, data, "sha224").hex() == t224
    assert hmac_digest(key, data, "sha256").hex() == t256
    assert hmac_digest(key, data, "sha384").hex() == t384
    assert hmac_digest(key, data, "sha512").hex() == t512


def test_rfc4231_case5_truncation() -> None:
    # RFC 4231, Section 4.6, Test Case 5: output truncated to 128 bits.
    key = bytes.fromhex("0c" * 20)
    data = b"Test With Truncation"
    assert hmac_truncated(key, data, 16, "sha224").hex() == "0e2aea68a90c8d37c988bcdb9fca6fa8"
    assert hmac_truncated(key, data, 16, "sha256").hex() == "a3b6167473100ee06e0c796c2955552b"
    assert hmac_truncated(key, data, 16, "sha384").hex() == "3abf34c3503b2a23a46efc619baef897"
    assert hmac_truncated(key, data, 16, "sha512").hex() == "415fad6271580a531d4179bc891d87a6"


LONG_KEY_DATA = b"Test Using Larger Than Block-Size Key and Larger Than One Block-Size Data"

# RFC 2202, Section 2 (HMAC-MD5) and Section 3 (HMAC-SHA-1), test cases 1 to 7.
RFC2202 = [
    ("md5", 1, "0b" * 16, b"Hi There", "9294727a3638bb1c13f48ef8158bfc9d"),
    ("md5", 2, b"Jefe".hex(), b"what do ya want for nothing?", "750c783e6ab0b503eaa86e310a5db738"),
    ("md5", 3, "aa" * 16, b"\xdd" * 50, "56be34521d144c88dbb8c733f0e8b3f6"),
    ("md5", 4, "0102030405060708090a0b0c0d0e0f10111213141516171819", b"\xcd" * 50, "697eaf0aca3a3aea3a75164746ffaa79"),
    ("md5", 5, "0c" * 16, b"Test With Truncation", "56461ef2342edc00f9bab995690efd4c"),
    ("md5", 6, "aa" * 80, D6, "6b1ab7fe4bd7bf8f0b62e6ce61b9d0cd"),
    ("md5", 7, "aa" * 80, LONG_KEY_DATA, "6f630fad67cda0ee1fb1f562db3aa53e"),
    ("sha1", 1, "0b" * 20, b"Hi There", "b617318655057264e28bc0b6fb378c8ef146be00"),
    ("sha1", 2, b"Jefe".hex(), b"what do ya want for nothing?", "effcdf6ae5eb2fa2d27416d5f184df9c259a7c79"),
    ("sha1", 3, "aa" * 20, b"\xdd" * 50, "125d7342b9ac11cd91a39af48aa17b4f63f175d3"),
    ("sha1", 4, "0102030405060708090a0b0c0d0e0f10111213141516171819", b"\xcd" * 50, "4c9007f4026250c6bc8414f9bf50c86c2d7235da"),
    ("sha1", 5, "0c" * 20, b"Test With Truncation", "4c1a03424b55e07fe7f27be1d58bb9324a9a5a04"),
    ("sha1", 6, "aa" * 80, D6, "aa4ae5e15272d00e95705637ce8a3b55ed402112"),
    ("sha1", 7, "aa" * 80, LONG_KEY_DATA, "e8e99d0f45237d786d6bbaa7965c7808bbff1a91"),
]


@pytest.mark.parametrize("name, case, key_hex, data, tag", RFC2202)
def test_rfc2202(name: str, case: int, key_hex: str, data: bytes, tag: str) -> None:
    assert hmac_digest(bytes.fromhex(key_hex), data, name).hex() == tag


def test_rfc2202_digest_96() -> None:
    # RFC 2202, test case 5 of Sections 2 and 3: the 96-bit truncations.
    assert hmac_truncated(b"\x0c" * 16, b"Test With Truncation", 12, "md5").hex() == "56461ef2342edc00f9bab995"
    assert hmac_truncated(b"\x0c" * 20, b"Test With Truncation", 12, "sha1").hex() == "4c1a03424b55e07fe7f27be1"


@pytest.mark.parametrize("name", ["md5", "sha1", "sha256", "sha512", "sha3_256", "blake2b"])
def test_matches_stdlib_hmac(name: str) -> None:
    rng = random.Random(2104)
    for klen in [0, 1, 31, 64, 65, 127, 128, 129, 200]:
        key = rng.randbytes(klen)
        msg = rng.randbytes(rng.randrange(0, 300))
        assert hmac_digest(key, msg, name) == std_hmac.new(key, msg, name).digest()


def test_verify_accepts_and_rejects() -> None:
    key, msg = b"k" * 32, b"pay 100 to Bob"
    tag = hmac_digest(key, msg)
    assert hmac_verify(key, msg, tag)
    assert hmac_verify(key, msg, tag[:16])  # a truncated tag
    assert not hmac_verify(b"j" * 32, msg, tag)  # a wrong key fails
    assert not hmac_verify(key, b"pay 900 to Bob", tag)
    for i in range(len(tag)):
        bad = bytearray(tag)
        bad[i] ^= 1
        assert not hmac_verify(key, msg, bytes(bad))
    assert not hmac_verify(key, msg, b"")
    assert not tags_equal(b"ab", b"abc")


def test_key_padding_equivalence() -> None:
    # A short key and the same key with zero bytes appended up to B give the same tag.
    # This is a known property of RFC 2104 key handling, not a weakness of HMAC as a PRF.
    msg = b"m"
    assert hmac_digest(b"key", msg) == hmac_digest(b"key\x00\x00", msg)
    # A long key and its hash give the same tag.
    long_key = b"x" * 100
    assert hmac_digest(long_key, msg) == hmac_digest(hashlib.sha256(long_key).digest(), msg)


def test_avalanche() -> None:
    rng = random.Random(7)
    key = rng.randbytes(32)
    total = 0
    trials = 200
    for _ in range(trials):
        msg = bytearray(rng.randbytes(40))
        a = int.from_bytes(hmac_digest(key, bytes(msg)), "big")
        msg[rng.randrange(40)] ^= 1 << rng.randrange(8)
        b = int.from_bytes(hmac_digest(key, bytes(msg)), "big")
        total += bin(a ^ b).count("1")
    mean = total / trials
    assert 120 < mean < 136  # about half of 256 bits
