# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-padding/. The authors are listed in prov/YE2JDS.jsonl.

import itertools

import pytest

from aes import AES
from block_padding import (
    cbc_cs3_decrypt,
    cbc_cs3_encrypt,
    pad_iso7816,
    pad_pkcs7,
    pad_x923,
    pad_zero,
    unpad_iso7816,
    unpad_pkcs7,
    unpad_x923,
    unpad_zero,
)

SCHEMES = [(pad_pkcs7, unpad_pkcs7), (pad_iso7816, unpad_iso7816), (pad_x923, unpad_x923)]


def test_aes_fips197_appendix_c() -> None:
    # FIPS 197, Appendix C.1 (AES-128).
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_worked_example_block_size_8() -> None:
    m = b"hello"
    assert pad_pkcs7(m, 8).hex() == "68656c6c6f030303"
    assert pad_iso7816(m, 8).hex() == "68656c6c6f800000"
    assert pad_x923(m, 8).hex() == "68656c6c6f000003"
    assert pad_zero(m, 8).hex() == "68656c6c6f000000"
    full = b"abcdefgh"
    assert pad_pkcs7(full, 8) == full + b"\x08" * 8
    assert pad_iso7816(full, 8) == full + b"\x80" + bytes(7)
    assert pad_x923(full, 8) == full + bytes(7) + b"\x08"
    assert pad_zero(full, 8) == full


def test_unambiguous_schemes_round_trip_on_all_short_messages() -> None:
    # Every message of length 0..5 over the alphabet {00, 01, 80} with b = 4: pad is injective.
    alphabet = [0x00, 0x01, 0x80]
    for pad, unpad in SCHEMES:
        seen = set()
        for n in range(6):
            for t in itertools.product(alphabet, repeat=n):
                m = bytes(t)
                x = pad(m, 4)
                assert len(x) % 4 == 0 and len(m) < len(x) <= len(m) + 4
                assert unpad(x, 4) == m
                seen.add(x)
        assert len(seen) == sum(3**n for n in range(6))


def test_zero_padding_is_ambiguous() -> None:
    assert pad_zero(b"hello", 8) == pad_zero(b"hello\x00", 8)
    assert unpad_zero(pad_zero(b"hello\x00", 8)) != b"hello\x00"


def test_strict_unpadding_rejects_bad_padding() -> None:
    with pytest.raises(ValueError):
        unpad_pkcs7(b"abcde\x02\x03\x03", 8)
    with pytest.raises(ValueError):
        unpad_pkcs7(b"abcdefg\x00", 8)
    with pytest.raises(ValueError):
        unpad_iso7816(bytes(8), 8)
    with pytest.raises(ValueError):
        unpad_x923(b"abcde\x01\x00\x03", 8)
    with pytest.raises(ValueError):
        unpad_x923(b"abcdefg\x09", 8)


def test_rfc3962_cbc_cts_vectors() -> None:
    # RFC 3962, Appendix B: AES-128 CBC with ciphertext stealing, all-zero IV.
    # Kerberos CTS swaps the last two blocks always, which is variant CS3.
    a = AES(bytes.fromhex("636869636b656e207465726979616b69"))
    iv = bytes(16)
    p = b"I would like the General Gau's Chicken, please,"
    cases = [
        (17, "c6353568f2bf8cb4d8a580362da7ff7f97"),
        (31, "fc00783e0efdb2c1d445d4c8eff7ed2297687268d6ecccc0c07b25e25ecfe5"),
        (32, "39312523a78662d5be7fcbcc98ebf5a897687268d6ecccc0c07b25e25ecfe584"),
        (47, "97687268d6ecccc0c07b25e25ecfe584b3fffd940c16a18c1b5549d2f838029e39312523a78662d5be7fcbcc98ebf5"),
    ]
    for n, ct in cases:
        c = cbc_cs3_encrypt(a, iv, p[:n])
        assert c.hex() == ct
        assert cbc_cs3_decrypt(a, iv, c) == p[:n]


def test_cts_round_trip_keeps_length() -> None:
    a = AES(bytes(range(16)))
    iv = bytes(range(16, 32))
    for n in range(16, 70):
        p = bytes((7 * i + 3) % 256 for i in range(n))
        c = cbc_cs3_encrypt(a, iv, p)
        assert len(c) == n
        assert cbc_cs3_decrypt(a, iv, c) == p
    with pytest.raises(ValueError):
        cbc_cs3_encrypt(a, iv, b"short")
