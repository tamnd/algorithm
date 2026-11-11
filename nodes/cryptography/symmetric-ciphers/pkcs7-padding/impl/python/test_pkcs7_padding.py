# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pkcs7-padding/. The authors are listed in prov/TD8JXS.jsonl.

import itertools
import random

import pytest

from pkcs7_padding import PaddingError, pkcs7_check_masked, pkcs7_pad, pkcs7_unpad, pkcs7_unpad_lenient


def test_rfc5652_rule_examples() -> None:
    # RFC 5652, Section 6.3: pad with k octets of value k, k = b - (len mod b).
    assert pkcs7_pad(b"attack at dawn", 16) == b"attack at dawn\x02\x02"
    assert pkcs7_pad(b"YELLOW SUBMARINE", 16) == b"YELLOW SUBMARINE" + b"\x10" * 16
    assert pkcs7_pad(b"", 16) == b"\x10" * 16
    assert pkcs7_pad(b"ICE ICE BABY", 16) == b"ICE ICE BABY\x04\x04\x04\x04"
    # PKCS #5 (RFC 8018, Section 6.1.1) is the same rule with b = 8.
    assert pkcs7_pad(b"hello", 8) == b"hello\x03\x03\x03"


def test_round_trip_every_length() -> None:
    rng = random.Random(5652)
    for b in (1, 8, 16, 255):
        for n in range(0, 2 * b + 2):
            m = bytes(rng.randrange(256) for _ in range(n))
            x = pkcs7_pad(m, b)
            assert len(x) % b == 0 and 1 <= len(x) - len(m) <= b
            assert pkcs7_unpad(x, b) == m


def test_strict_unpad_rejects() -> None:
    for bad in (
        b"ICE ICE BABY\x05\x05\x05\x05",
        b"ICE ICE BABY\x01\x02\x03\x04",
        b"ICE ICE BABY\x04\x04\x04\x00",
        b"abcdefghijklmno\x11",
        b"",
        b"abc",
    ):
        with pytest.raises(PaddingError):
            pkcs7_unpad(bad, 16)
    assert pkcs7_unpad(b"ICE ICE BABY\x04\x04\x04\x04", 16) == b"ICE ICE BABY"


def test_accepts_exactly_the_image_of_pad() -> None:
    # Exhaustive over b = 3 and all strings of length 3 or 6 over the bytes {0, 1, 2, 3, 65}.
    alphabet = [0, 1, 2, 3, 65]
    for n in (3, 6):
        for t in itertools.product(alphabet, repeat=n):
            x = bytes(t)
            try:
                m = pkcs7_unpad(x, 3)
            except PaddingError:
                assert not pkcs7_check_masked(x, 3)
                continue
            assert pkcs7_pad(m, 3) == x
            assert pkcs7_check_masked(x, 3)


def test_masked_check_agrees_on_random_blocks() -> None:
    rng = random.Random(7)
    for _ in range(3000):
        x = bytes(rng.randrange(256) for _ in range(14)) + bytes([rng.randrange(18)]) * 2
        ok = True
        try:
            pkcs7_unpad(x, 16)
        except PaddingError:
            ok = False
        assert pkcs7_check_masked(x, 16) == ok


def test_lenient_unpad_accepts_garbage() -> None:
    # The lenient version returns a wrong message instead of an error.
    assert pkcs7_unpad_lenient(b"ICE ICE BABY\x01\x02\x03\x04") == b"ICE ICE BABY"
    assert pkcs7_unpad_lenient(b"abc\x40") == b""
    with pytest.raises(PaddingError):
        pkcs7_unpad(b"abc\x40", 4)


def test_probability_random_block_is_valid() -> None:
    # A uniformly random 16-byte block has valid padding with probability sum_{k=1}^{16} 256^-k.
    from fractions import Fraction

    p = sum(Fraction(1, 256**k) for k in range(1, 17))
    assert abs(float(p) - 1 / 255) < 1e-12
    assert float(p) == pytest.approx(0.00392156862745098)
