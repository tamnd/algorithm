# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ccm-decryption-check/. The authors are listed in prov/PYJ12X.jsonl.

import random

import pytest

from aes import AES
from ccm_decryption_check import (
    INVALID,
    decrypt_parse_first,
    decrypt_release_first,
    decrypt_verify,
    generate_encrypt,
)

SP_KEY = bytes.fromhex("404142434445464748494a4b4c4d4e4f")


def test_aes_fips197_appendix_c1() -> None:
    key = bytes(range(16))
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert AES(key).encrypt_block(pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


@pytest.mark.parametrize(
    "example, n, a, p, tlen, c",
    [
        # NIST SP 800-38C, Appendix C, Examples 1 to 3, run through decryption-verification
        # ("a corresponding example of the decryption-verification process ... is straightforward").
        (1, "10111213141516", "0001020304050607", "20212223", 4, "7162015b4dac255d"),
        (
            2,
            "1011121314151617",
            "000102030405060708090a0b0c0d0e0f",
            "202122232425262728292a2b2c2d2e2f",
            6,
            "d2a1f0e051ea5f62081a7792073d593d1fc64fbfaccd",
        ),
        (
            3,
            "101112131415161718191a1b",
            "000102030405060708090a0b0c0d0e0f10111213",
            "202122232425262728292a2b2c2d2e2f3031323334353637",
            8,
            "e3b201a9f5b71a7a9b1ceaeccd97e70b6176aad9a4428aa5484392fbc1b09951",
        ),
    ],
)
def test_sp800_38c_appendix_c(example: int, n: str, a: str, p: str, tlen: int, c: str) -> None:
    cipher = AES(SP_KEY)
    args = (bytes.fromhex(n), bytes.fromhex(a))
    assert generate_encrypt(cipher, *args, bytes.fromhex(p), tlen).hex() == c, example
    assert decrypt_verify(cipher, *args, bytes.fromhex(c), tlen) == bytes.fromhex(p)


def test_sp800_38c_example_4() -> None:
    cipher = AES(SP_KEY)
    n = bytes.fromhex("101112131415161718191a1b1c")
    a = bytes(range(256)) * 256
    c = bytes.fromhex(
        "69915dad1e84c6376a68c2967e4dab615ae0fd1faec44cc484828529463ccf72" "b4ac6bec93e8598e7f0dadbcea5b"
    )
    assert decrypt_verify(cipher, n, a, c, 14) == bytes(range(0x20, 0x40))


def test_rfc3610_packet_vector_1() -> None:
    # RFC 3610, Section 8, Packet Vector #1: 8 header bytes, M = 8.
    cipher = AES(bytes.fromhex("c0c1c2c3c4c5c6c7c8c9cacbcccdcecf"))
    n = bytes.fromhex("00000003020100a0a1a2a3a4a5")
    c = bytes.fromhex("588c979a61c663d2f066d0c2c0f989806d5f6b61dac38417e8d12cfdf926e0")
    assert decrypt_verify(cipher, n, bytes(range(8)), c, 8) == bytes(range(8, 31))


def test_every_changed_bit_gives_only_invalid() -> None:
    rng = random.Random(6)
    cipher = AES(rng.randbytes(16))
    n, a, p = rng.randbytes(13), b"header", rng.randbytes(37)
    c = generate_encrypt(cipher, n, a, p, 8)
    for bit in range(len(c) * 8):
        bad = bytearray(c)
        bad[bit // 8] ^= 1 << (bit % 8)
        assert decrypt_verify(cipher, n, a, bytes(bad), 8) == INVALID
    assert decrypt_verify(cipher, n, a + b"!", c, 8) == INVALID
    assert decrypt_verify(cipher, n[:-1] + bytes([n[-1] ^ 1]), a, c, 8) == INVALID


def test_step_1_rejects_short_ciphertexts() -> None:
    cipher = AES(SP_KEY)
    n = bytes(13)
    assert decrypt_verify(cipher, n, b"", bytes(8), 8) == INVALID  # Clen = Tlen: no payload
    assert decrypt_verify(cipher, n, b"", bytes(3), 8) == INVALID


def test_step_7_and_step_10_give_the_same_error() -> None:
    cipher = AES(SP_KEY)
    c = generate_encrypt(cipher, bytes(13), b"", b"abc", 8)
    bad_nonce = bytes(14)  # 14 bytes: q = 1, not valid, so step 7 fails
    assert decrypt_verify(cipher, bad_nonce, b"", c, 8) == INVALID
    assert decrypt_verify(cipher, bytes(13), b"", c[:-1] + b"\x00", 8) == INVALID


# ---- What goes wrong without the check. ----


def test_release_before_check_decrypts_any_target_with_one_query() -> None:
    rng = random.Random(2004)
    cipher = AES(rng.randbytes(16))
    n, a = rng.randbytes(13), b"to: bank"
    secret = b"PIN 4071, account 55-0918-2210"
    target = generate_encrypt(cipher, n, a, secret, 8)  # the attacker sees this on the wire
    delta = rng.randbytes(len(secret))
    query = bytes(x ^ y for x, y in zip(target, delta)) + target[len(secret) :]
    leaked, ok = decrypt_release_first(cipher, n, a, query, 8)
    assert not ok  # the tag check fails, but too late
    assert bytes(x ^ y for x, y in zip(leaked, delta)) == secret
    assert decrypt_verify(cipher, n, a, query, 8) == INVALID  # the correct check leaks nothing


def test_parse_before_check_reveals_the_first_byte() -> None:
    rng = random.Random(38)
    for _ in range(5):
        cipher = AES(rng.randbytes(16))
        n = rng.randbytes(13)
        secret = bytes([rng.randrange(256)]) + b" rest of the record"
        target = generate_encrypt(cipher, n, b"", secret, 8)
        found = []
        for d in range(256):  # at most 256 queries
            query = bytes([target[0] ^ d]) + target[1:]
            if decrypt_parse_first(cipher, n, b"", query, 8) != "BAD VERSION":
                found.append(0x01 ^ d)
        assert found == [secret[0]]
        # The correct process answers all 256 queries in the same way, except the unchanged one.
        answers = {decrypt_verify(cipher, n, b"", bytes([target[0] ^ d]) + target[1:], 8) for d in range(1, 256)}
        assert answers == {INVALID}
