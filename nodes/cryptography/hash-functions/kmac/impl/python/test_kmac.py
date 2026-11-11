# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kmac/. The authors are listed in prov/J3VNX8.jsonl.

import hashlib
import random

import pytest

from kmac import (
    bytepad,
    cshake,
    encode_string,
    kmac128,
    kmac256,
    kmacxof128,
    left_encode,
    right_encode,
    sha3_256,
    shake128,
    shake256,
)

KEY = bytes(range(0x40, 0x60))  # 40 41 ... 5F, the key of all six KMAC samples
DATA4 = bytes(range(4))  # 00 01 02 03
DATA200 = bytes(range(200))  # 00 01 ... C7 (1600 bits)
TAG = b"My Tagged Application"


# NIST, SP 800-185 example values, KMAC_samples.pdf, Samples #1 to #6.
@pytest.mark.parametrize(
    "sample, fn, data, out_bits, s, expected",
    [
        (1, kmac128, DATA4, 256, b"", "e5780b0d3ea6f7d3a429c5706aa43a00fadbd7d49628839e3187243f456ee14e"),
        (2, kmac128, DATA4, 256, TAG, "3b1fba963cd8b0b59e8c1a6d71888b7143651af8ba0a7070c0979e2811324aa5"),
        (3, kmac128, DATA200, 256, TAG, "1f5b4e6cca02209e0dcb5ca635b89a15e271ecc760071dfd805faa38f9729230"),
        (
            4,
            kmac256,
            DATA4,
            512,
            TAG,
            "20c570c31346f703c9ac36c61c03cb64c3970d0cfc787e9b79599d273a68d2f7"
            "f69d4cc3de9d104a351689f27cf6f5951f0103f33f4f24871024d9c27773a8dd",
        ),
        (
            5,
            kmac256,
            DATA200,
            512,
            b"",
            "75358cf39e41494e949707927cee0af20a3ff553904c86b08f21cc414bcfd691"
            "589d27cf5e15369cbbff8b9a4c2eb17800855d0235ff635da82533ec6b759b69",
        ),
        (
            6,
            kmac256,
            DATA200,
            512,
            TAG,
            "b58618f71f92e1d56c1b8c55ddd7cd188b97b4ca4d99831eb2699a837da2e4d9"
            "70fbacfde50033aea585f1a2708510c32d07880801bd182898fe476876fc8965",
        ),
    ],
)
def test_kmac_nist_samples(sample: int, fn, data: bytes, out_bits: int, s: bytes, expected: str) -> None:  # type: ignore[no-untyped-def]
    assert fn(KEY, data, out_bits // 8, s).hex() == expected


def test_cshake_nist_samples() -> None:
    # NIST, SP 800-185 example values, cSHAKE_samples.pdf, Samples #1 and #2 (cSHAKE128, N empty).
    s = b"Email Signature"
    assert cshake(DATA4, 32, b"", s, 168).hex() == "c1c36925b6409a04f1b504fcbca9d82b4017277cb5ed2b2065fc1d3814d5aaf5"
    assert cshake(DATA200, 32, b"", s, 168).hex() == "c5221d50e4f822d96a2e8881a961420f294b7b24fe3d2094baed2c6524cc166b"


def test_encodings_sp800_185() -> None:
    # SP 800-185, Section 2.3: left_encode(0) = 01 00, right_encode(0) = 00 01.
    assert left_encode(0) == b"\x01\x00"
    assert right_encode(0) == b"\x00\x01"
    assert left_encode(168) == b"\x01\xa8"
    assert right_encode(256) == b"\x01\x00\x02"
    assert encode_string(b"") == b"\x01\x00"
    assert encode_string(b"KMAC") == b"\x01\x20KMAC"
    # The "Encoded K" line of KMAC_samples.pdf, Sample #1, starts 02 01 00 40 41.
    assert encode_string(KEY)[:5].hex() == "0201004041"
    padded = bytepad(encode_string(KEY), 168)
    assert len(padded) == 168 and padded[:5].hex() == "01a8020100"


def test_shake_and_sha3_match_hashlib() -> None:
    rng = random.Random(202)
    for n in [0, 1, 135, 136, 137, 167, 168, 169, 400]:
        x = rng.randbytes(n)
        assert shake128(x, 200) == hashlib.shake_128(x).digest(200)
        assert shake256(x, 200) == hashlib.shake_256(x).digest(200)
        assert sha3_256(x) == hashlib.sha3_256(x).digest()


def test_wrong_key_and_customization() -> None:
    t = kmac128(KEY, b"msg", 32)
    assert kmac128(KEY, b"msg", 32) == t
    assert kmac128(KEY[:-1] + b"\x00", b"msg", 32) != t
    assert kmac128(KEY, b"msg", 32, b"other") != t
    assert kmac128(KEY, b"msh", 32) != t


def test_output_length_is_bound_in_but_not_for_xof() -> None:
    # KMAC with L = 256 is not a prefix of KMAC with L = 512, because L is in the input.
    a = kmac128(KEY, b"m", 32)
    b = kmac128(KEY, b"m", 64)
    assert b[:32] != a
    # KMACXOF128 uses right_encode(0), so shorter outputs are prefixes of longer ones.
    c = kmacxof128(KEY, b"m", 32)
    d = kmacxof128(KEY, b"m", 64)
    assert d[:32] == c
    assert c != a


def test_avalanche() -> None:
    rng = random.Random(9)
    total, trials = 0, 60
    for _ in range(trials):
        m = bytearray(rng.randbytes(16))
        a = int.from_bytes(kmac128(KEY, bytes(m), 32), "big")
        m[rng.randrange(16)] ^= 1 << rng.randrange(8)
        b = int.from_bytes(kmac128(KEY, bytes(m), 32), "big")
        total += bin(a ^ b).count("1")
    assert 116 < total / trials < 140
