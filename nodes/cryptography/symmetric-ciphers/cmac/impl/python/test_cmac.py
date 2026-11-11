# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cmac/. The authors are listed in prov/57R39D.jsonl.

import random

import pytest

from aes import AES
from cmac import cmac, cmac_verify, dbl, subkeys

KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
MSG64 = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def test_aes_fips197_appendix_c1() -> None:
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_rfc4493_section4_subkeys() -> None:
    # RFC 4493, Section 4, "Subkey Generation".
    a = AES(KEY)
    assert a.encrypt_block(bytes(16)).hex() == "7df76b0c1ab899b33e42f047b91b546f"
    k1, k2 = subkeys(a)
    assert k1.hex() == "fbeed618357133667c85e08f7236a8de"
    assert k2.hex() == "f7ddac306ae266ccf90bc11ee46d513b"


@pytest.mark.parametrize(
    "mlen, tag",
    [
        (0, "bb1d6929e95937287fa37d129b756746"),  # RFC 4493, Section 4, Example 1
        (16, "070a16b46b4d4144f79bdd9dd04a287c"),  # Example 2
        (40, "dfa66747de9ae63030ca32611497c827"),  # Example 3
        (64, "51f0bebf7e3b9d92fc49741779363cfe"),  # Example 4
    ],
)
def test_rfc4493_section4_examples(mlen: int, tag: str) -> None:
    a = AES(KEY)
    assert cmac(a, MSG64[:mlen]).hex() == tag
    assert cmac_verify(a, MSG64[:mlen], bytes.fromhex(tag))


def test_doubling_reduces_with_0x87() -> None:
    assert dbl(bytes(15) + b"\x01") == bytes(15) + b"\x02"
    assert dbl(b"\x80" + bytes(15)) == bytes(15) + b"\x87"
    # dbl is multiplication by x, so it is linear over GF(2).
    rng = random.Random(4493)
    for _ in range(100):
        u, v = rng.randbytes(16), rng.randbytes(16)
        assert dbl(xor(u, v)) == xor(dbl(u), dbl(v))


def test_truncated_tags_and_one_changed_bit() -> None:
    a = AES(KEY)
    t = cmac(a, MSG64[:40])
    assert cmac(a, MSG64[:40], 8) == t[:8]
    assert cmac_verify(a, MSG64[:40], t[:8])
    for bit in range(0, 320, 7):
        m = bytearray(MSG64[:40])
        m[bit // 8] ^= 1 << (bit % 8)
        assert not cmac_verify(a, bytes(m), t)
    for bit in range(128):
        t2 = bytearray(t)
        t2[bit // 8] ^= 1 << (bit % 8)
        assert not cmac_verify(a, MSG64[:40], bytes(t2))


def test_padding_is_unambiguous() -> None:
    # A partial block m and the full block m || 80 00 .. 00 get different tags, because K1 != K2.
    a = AES(KEY)
    m = b"fifteen bytes.."
    assert len(m) == 15
    assert cmac(a, m) != cmac(a, m + b"\x80")
    assert cmac(a, b"") != cmac(a, b"\x80" + bytes(15))


def test_cbc_mac_splice_fails_against_cmac() -> None:
    # The variable-length forgery of plain CBC-MAC does not work: the last block is masked with K1.
    a = AES(KEY)
    m1, m2 = b"pay 10 EUR to A.", b"pay 99 EUR to E."
    t1, t2 = cmac(a, m1), cmac(a, m2)
    assert not cmac_verify(a, m1 + xor(m2, t1), t2)


def test_cmac_is_cbc_mac_with_a_masked_last_block() -> None:
    # For whole blocks, CMAC(M) is the CBC-MAC of M with the last block XORed with K1.
    a = AES(KEY)
    k1, _ = subkeys(a)
    c = bytes(16)
    blocks = [MSG64[i : i + 16] for i in range(0, 64, 16)]
    blocks[-1] = xor(blocks[-1], k1)
    for blk in blocks:
        c = a.encrypt_block(xor(c, blk))
    assert c == cmac(a, MSG64)


def test_bad_tag_length() -> None:
    a = AES(KEY)
    with pytest.raises(ValueError):
        cmac(a, b"x", 0)
    with pytest.raises(ValueError):
        cmac(a, b"x", 17)
