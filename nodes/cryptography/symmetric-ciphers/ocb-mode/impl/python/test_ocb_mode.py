# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ocb-mode/. The authors are listed in prov/0FNP6K.jsonl.

import random

import pytest

from aes import AES
from ocb_mode import INVALID, OcbKey, initial_offset, ocb_decrypt, ocb_encrypt

K = bytes(range(16))
SEQ = bytes(range(40))


def test_aes_fips197_appendix_c1() -> None:
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert AES(K).encrypt_block(pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


# RFC 7253, Appendix A, the 16 (N, A, P, C) tuples: K = 000102...0F, TAGLEN = 128,
# N = BBAA998877665544332211 || i. Lengths of A and P in bytes, with A and P = 00 01 02 ...
RFC7253_APPENDIX_A = [
    (0x00, 0, 0, "785407bfffc8ad9edcc5520ac9111ee6"),
    (0x01, 8, 8, "6820b3657b6f615a5725bda0d3b4eb3a257c9af1f8f03009"),
    (0x02, 8, 0, "81017f8203f081277152fade694a0a00"),
    (0x03, 0, 8, "45dd69f8f5aae72414054cd1f35d82760b2cd00d2f99bfa9"),
    (0x04, 16, 16, "571d535b60b277188be5147170a9a22c3ad7a4ff3835b8c5701c1ccec8fc3358"),
    (0x05, 16, 0, "8cf761b6902ef764462ad86498ca6b97"),
    (0x06, 0, 16, "5ce88ec2e0692706a915c00aeb8b2396f40e1c743f52436bdf06d8fa1eca343d"),
    (
        0x07,
        24,
        24,
        "1ca2207308c87c010756104d8840ce1952f09673a448a122c92c62241051f57356d7f3c90bb0e07f",
    ),
    (0x08, 24, 0, "6dc225a071fc1b9f7c69f93b0f1e10de"),
    (
        0x09,
        0,
        24,
        "221bd0de7fa6fe993eccd769460a0af2d6cded0c395b1c3ce725f32494b9f914d85c0b1eb38357ff",
    ),
    (
        0x0A,
        32,
        32,
        "bd6f6c496201c69296c11efd138a467abd3c707924b964deaffc40319af5a48540fbba186c5553c68ad9f592a79a4240",
    ),
    (0x0B, 32, 0, "fe80690bee8a485d11f32965bc9d2a32"),
    (
        0x0C,
        0,
        32,
        "2942bfc773bda23cabc6acfd9bfd5835bd300f0973792ef46040c53f1432bcdfb5e1dde3bc18a5f840b52e653444d5df",
    ),
    (
        0x0D,
        40,
        40,
        "d5ca91748410c1751ff8a2f618255b68a0a12e093ff454606e59f9c1d0ddc54b"
        "65e8628e568bad7aed07ba06a4a69483a7035490c5769e60",
    ),
    (0x0E, 40, 0, "c5cd9d1850c141e358649994ee701b68"),
    (
        0x0F,
        0,
        40,
        "4412923493c57d5de0d700f753cce0d1d2d95060122e9f15a5ddbfc5787e50b5"
        "cc55ee507bcb084e479ad363ac366b95a98ca5f3000b1479",
    ),
]


@pytest.mark.parametrize("last, alen, plen, c", RFC7253_APPENDIX_A)
def test_rfc7253_appendix_a(last: int, alen: int, plen: int, c: str) -> None:
    cipher = AES(K)
    n = bytes.fromhex("bbaa998877665544332211") + bytes([last])
    assert ocb_encrypt(cipher, n, SEQ[:alen], SEQ[:plen]).hex() == c
    assert ocb_decrypt(cipher, n, SEQ[:alen], bytes.fromhex(c)) == SEQ[:plen]


def test_rfc7253_appendix_a_internal_values() -> None:
    # The internal values that RFC 7253 Appendix A lists for the last tuple (N = ...0F).
    key = OcbKey(AES(K))
    assert f"{key.l_star:032x}" == "c6a13b37878f5b826f4f8162a1c8d879"
    assert f"{key.l_dollar:032x}" == "8d42766f0f1eb704de9f02c54391b075"
    assert f"{key.l_i(0):032x}" == "1a84ecde1e3d6e09bd3e058a8723606d"
    assert f"{key.l_i(1):032x}" == "3509d9bc3c7adc137a7c0b150e46c0da"
    n = bytes.fromhex("bbaa9988776655443322110f")
    assert int.from_bytes(n, "big") & 63 == 15  # bottom
    offset0 = initial_offset(key, n, 128)
    assert f"{offset0:032x}" == "587ef72716eab6dd3219f8092d517d69"
    offset1 = offset0 ^ key.l_i(0)
    offset2 = offset1 ^ key.l_i(1)
    assert f"{offset1:032x}" == "42fa1bf908d7d8d48f27fd83aa721d04"
    assert f"{offset2:032x}" == "77f3c24534ad04c7f55bf696a434ddde"
    assert f"{offset2 ^ key.l_star:032x}" == "b152f972b3225f459a1477f405fc05a7"


def test_rfc7253_appendix_a_taglen_96() -> None:
    cipher = AES(bytes(range(15, -1, -1)))
    n = bytes.fromhex("bbaa9988776655443322110d")
    c = (
        "1792a4e31e0755fb03e31b22116e6c2ddf9efd6e33d536f1a0124b0a55bae884"
        "ed93481529c76b6ad0c515f4d1cdd4fdac4f02aa"
    )
    assert ocb_encrypt(cipher, n, SEQ, SEQ, 96).hex() == c
    assert ocb_decrypt(cipher, n, SEQ, bytes.fromhex(c), 96) == SEQ


@pytest.mark.parametrize(
    "keylen, taglen, output",
    [
        # RFC 7253, Appendix A, the iterated test, one output per parameter set of Section 3.1.
        (128, 128, "67e944d23256c5e0b6c61fa22fdf1ea2"),
        (192, 128, "f673f2c3e7174aae7bae986ca9f29e17"),
        (256, 128, "d90eb8e9c977c88b79dd793d7ffa161c"),
        (128, 96, "77a3d8e73589158d25d01209"),
        (192, 96, "05d56ead2752c86be6932c5e"),
        (256, 96, "5458359ac23b0cba9e6330dd"),
        (128, 64, "192c9b7bd90ba06a"),
        (192, 64, "0066bc6e0ef34e24"),
        (256, 64, "7d4ea5d445501cbe"),
    ],
)
def test_rfc7253_appendix_a_iterated(keylen: int, taglen: int, output: str) -> None:
    cipher = AES(bytes(keylen // 8 - 1) + bytes([taglen]))
    c = b""
    for i in range(128):
        s = bytes(i)
        c += ocb_encrypt(cipher, (3 * i + 1).to_bytes(12, "big"), s, s, taglen)
        c += ocb_encrypt(cipher, (3 * i + 2).to_bytes(12, "big"), b"", s, taglen)
        c += ocb_encrypt(cipher, (3 * i + 3).to_bytes(12, "big"), s, b"", taglen)
    assert len(c) == {128: 22400, 96: 20864, 64: 19328}[taglen]
    assert ocb_encrypt(cipher, (385).to_bytes(12, "big"), c, b"", taglen).hex() == output


def test_round_trips_and_nonce_lengths() -> None:
    rng = random.Random(7)
    cipher = AES(rng.randbytes(16))
    for plen in (0, 1, 15, 16, 17, 31, 32, 33, 100):
        for nlen in (1, 7, 12, 15):
            n, a, p = rng.randbytes(nlen), rng.randbytes(rng.randrange(50)), rng.randbytes(plen)
            for taglen in (64, 96, 128):
                c = ocb_encrypt(cipher, n, a, p, taglen)
                assert len(c) == plen + taglen // 8
                assert ocb_decrypt(cipher, n, a, c, taglen) == p


def test_one_changed_bit_is_rejected() -> None:
    rng = random.Random(8)
    cipher = AES(rng.randbytes(16))
    n, a, p = rng.randbytes(12), rng.randbytes(20), rng.randbytes(37)
    c = ocb_encrypt(cipher, n, a, p)
    for bit in range(len(c) * 8):
        bad = bytearray(c)
        bad[bit // 8] ^= 1 << (bit % 8)
        assert ocb_decrypt(cipher, n, a, bytes(bad)) == INVALID
    for bit in range(len(a) * 8):
        bad_a = bytearray(a)
        bad_a[bit // 8] ^= 1 << (bit % 8)
        assert ocb_decrypt(cipher, n, bytes(bad_a), c) == INVALID
    assert ocb_decrypt(cipher, n[:-1] + bytes([n[-1] ^ 1]), a, c) == INVALID
    assert ocb_decrypt(cipher, n, a, c[:10]) == INVALID


def test_tag_length_is_bound_into_the_nonce() -> None:
    # The ciphertext core depends on TAGLEN, so a 64-bit tag is not a prefix of the 128-bit one.
    cipher = AES(K)
    n = bytes(12)
    c128 = ocb_encrypt(cipher, n, b"", SEQ, 128)
    c64 = ocb_encrypt(cipher, n, b"", SEQ, 64)
    assert c128[:40] != c64[:40]
    assert ocb_decrypt(cipher, n, b"", c128[:-8], 64) == INVALID


def test_nonce_reuse_acts_like_ecb_per_position() -> None:
    rng = random.Random(9)
    cipher = AES(rng.randbytes(16))
    n = rng.randbytes(12)
    x, y, z = rng.randbytes(16), rng.randbytes(16), rng.randbytes(16)
    c1 = ocb_encrypt(cipher, n, b"", x + y)
    c2 = ocb_encrypt(cipher, n, b"", x + z)
    assert c1[:16] == c2[:16]  # equal first blocks are visible
    assert c1[16:32] != c2[16:32]
    c3 = ocb_encrypt(cipher, rng.randbytes(12), b"", x + z)
    assert c1[:16] != c3[:16]  # with a fresh nonce they are not


def test_nonce_reuse_forges_a_new_message() -> None:
    """Two encryptions under one nonce give a valid ciphertext for a third message never encrypted."""
    rng = random.Random(10)
    cipher = AES(rng.randbytes(16))
    n, a = rng.randbytes(12), b"hdr"
    b, s = rng.randbytes(16), b"amount=0100"  # one full block and a partial block
    delta = bytes(x ^ y for x, y in zip(b"amount=0100", b"amount=9999"))
    c1 = ocb_encrypt(cipher, n, a, b + s)
    # Second query, same nonce: change the full block by delta || 0^*, keep the partial block.
    b2 = bytes(x ^ y for x, y in zip(b, delta + bytes(16 - len(delta))))
    c2 = ocb_encrypt(cipher, n, a, b2 + s)
    # The partial block is a stream cipher with a pad fixed by (N, m), and the checksum of
    # (b, s xor delta) equals that of (b2, s). So the tag of query 2 fits the forgery.
    tail = bytes(x ^ y for x, y in zip(c1[16:27], delta))
    forged = c1[:16] + tail + c2[27:]
    assert forged not in (c1, c2)
    assert ocb_decrypt(cipher, n, a, forged) == b + b"amount=9999"
