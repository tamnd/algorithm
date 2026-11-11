# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ccm-mode/. The authors are listed in prov/0AFYD8.jsonl.

import random

import pytest

from aes import AES
from ccm_mode import (
    InvalidTag,
    cbc_mac_tag,
    ccm_decrypt,
    ccm_encrypt,
    counter_block,
    encode_ad_length,
    format_blocks,
)

RFC_KEY = "c0c1c2c3c4c5c6c7c8c9cacbcccdcecf"
SP_KEY = "404142434445464748494a4b4c4d4e4f"


def test_aes_fips197_appendix_c1() -> None:
    key = bytes(range(16))
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert AES(key).encrypt_block(pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


@pytest.mark.parametrize(
    "vector, key, nonce, packet, header_len, m_len, output",
    [
        # RFC 3610, Section 8, Packet Vectors #1 to #4 (M = 8), #7 (M = 10) and #13 (another key).
        (
            1,
            RFC_KEY,
            "00000003020100a0a1a2a3a4a5",
            "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e",
            8,
            8,
            "0001020304050607588c979a61c663d2f066d0c2c0f989806d5f6b61dac38417e8d12cfdf926e0",
        ),
        (
            2,
            RFC_KEY,
            "00000004030201a0a1a2a3a4a5",
            "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
            8,
            8,
            "000102030405060772c91a36e135f8cf291ca894085c87e3cc15c439c9e43a3ba091d56e10400916",
        ),
        (
            3,
            RFC_KEY,
            "00000005040302a0a1a2a3a4a5",
            "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20",
            8,
            8,
            "000102030405060751b1e5f44a197d1da46b0f8e2d282ae871e838bb64da8596574adaa76fbd9fb0c5",
        ),
        (
            4,
            RFC_KEY,
            "00000006050403a0a1a2a3a4a5",
            "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e",
            12,
            8,
            "000102030405060708090a0ba28c6865939a9a79faaa5c4c2a9d4a91cdac8c96c861b9c9e61ef1",
        ),
        (
            7,
            RFC_KEY,
            "00000009080706a0a1a2a3a4a5",
            "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e",
            8,
            10,
            "00010203040506070135d1b2c95f41d5d1d4fec185d166b8094e999dfed96c048c56602c97acbb7490",
        ),
        (
            13,
            "d7828d13b2b0bdc325a76236df93cc6b",
            "00412b4ea9cdbe3c9696766cfa",
            "0be1a88bace018b108e8cf97d820ea258460e96ad9cf5289054d895ceac47c",
            8,
            8,
            "0be1a88bace018b14cb97f86a2a4689a877947ab8091ef5386a6ffbdd080f8e78cf7cb0cddd7b3",
        ),
    ],
)
def test_rfc3610_section_8(vector: int, key: str, nonce: str, packet: str, header_len: int, m_len: int, output: str) -> None:
    cipher = AES(bytes.fromhex(key))
    pkt, n = bytes.fromhex(packet), bytes.fromhex(nonce)
    a, p = pkt[:header_len], pkt[header_len:]
    cu = ccm_encrypt(cipher, n, a, p, m_len)
    assert (a + cu).hex() == output, vector
    assert ccm_decrypt(cipher, n, a, cu, m_len) == p


def test_rfc3610_packet_vector_1_intermediates() -> None:
    cipher = AES(bytes.fromhex(RFC_KEY))
    n = bytes.fromhex("00000003020100a0a1a2a3a4a5")
    pkt = bytes(range(31))
    blocks = format_blocks(n, pkt[:8], pkt[8:], 8, 2)
    assert blocks[:16].hex() == "59000000030201" + "00a0a1a2a3a4a5" + "0017"  # "CBC IV in"
    assert cbc_mac_tag(cipher, blocks, 8).hex() == "2dc697e411ca83a8"  # "CBC-MAC"
    assert counter_block(n, 1, 2).hex() == "0100000003020100a0a1a2a3a4a50001"  # "CTR Start"


@pytest.mark.parametrize(
    "example, nonce, a, p, m_len, c",
    [
        # NIST SP 800-38C, Appendix C, Examples 1 to 3.
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
def test_sp800_38c_appendix_c(example: int, nonce: str, a: str, p: str, m_len: int, c: str) -> None:
    cipher = AES(bytes.fromhex(SP_KEY))
    out = ccm_encrypt(cipher, bytes.fromhex(nonce), bytes.fromhex(a), bytes.fromhex(p), m_len)
    assert out.hex() == c, example


def test_sp800_38c_example_4_long_associated_data() -> None:
    # Appendix C.4: 65536 bytes of A (the bytes 00 to ff repeated), so l(a) uses 0xff 0xfe and 4 bytes.
    cipher = AES(bytes.fromhex(SP_KEY))
    n = bytes.fromhex("101112131415161718191a1b1c")
    a = bytes(range(256)) * 256
    p = bytes(range(0x20, 0x40))
    assert format_blocks(n, a, p, 14, 2)[:32].hex() == "71101112131415161718191a1b1c0020" "fffe0001000000010203040506070809"
    out = ccm_encrypt(cipher, n, a, p, 14)
    assert out.hex() == (
        "69915dad1e84c6376a68c2967e4dab615ae0fd1faec44cc484828529463ccf72" "b4ac6bec93e8598e7f0dadbcea5b"
    )


def test_ad_length_encoding() -> None:
    assert encode_ad_length(1).hex() == "0001"
    assert encode_ad_length(0xFEFF).hex() == "feff"
    assert encode_ad_length(0xFF00).hex() == "fffe0000ff00"
    assert encode_ad_length(1 << 32).hex() == "ffff0000000100000000"


def test_counter_blocks_never_equal_b0() -> None:
    # B_0 has M' >= 1 in bits 3 to 5 of its flags; every A_i has zeros there.
    n = bytes(13)
    for m_len in (4, 8, 16):
        b0 = format_blocks(n, b"", b"", m_len, 2)[:16]
        assert all(counter_block(n, i, 2) != b0 for i in range(1000))


@pytest.mark.parametrize("n", [0, 1, 16, 17, 40])
def test_round_trip(n: int) -> None:
    rng = random.Random(n)
    cipher = AES(rng.randbytes(16))
    nonce, a, p = rng.randbytes(12), rng.randbytes(n % 5), rng.randbytes(n)
    assert ccm_decrypt(cipher, nonce, a, ccm_encrypt(cipher, nonce, a, p, 12), 12) == p


def test_one_changed_bit_is_rejected() -> None:
    rng = random.Random(3610)
    cipher = AES(rng.randbytes(16))
    nonce, a, p = rng.randbytes(13), b"hdr", rng.randbytes(20)
    cu = ccm_encrypt(cipher, nonce, a, p, 8)
    for bit in range(len(cu) * 8):
        bad = bytearray(cu)
        bad[bit // 8] ^= 1 << (bit % 8)
        with pytest.raises(InvalidTag):
            ccm_decrypt(cipher, nonce, a, bytes(bad), 8)
    for bit in range(24):
        bad_a = bytearray(a)
        bad_a[bit // 8] ^= 1 << (bit % 8)
        with pytest.raises(InvalidTag):
            ccm_decrypt(cipher, nonce, bytes(bad_a), cu, 8)


def test_not_online_the_first_block_needs_the_length() -> None:
    # B_0 holds l(m), so the CBC-MAC cannot start before the length of the message is known.
    n = bytes(13)
    assert format_blocks(n, b"", b"x" * 16, 16, 2)[:16] != format_blocks(n, b"", b"x" * 32, 16, 2)[:16]


def test_bad_parameters() -> None:
    cipher = AES(bytes(16))
    with pytest.raises(ValueError):
        ccm_encrypt(cipher, bytes(13), b"", b"", 5)  # odd tag length
    with pytest.raises(ValueError):
        ccm_encrypt(cipher, bytes(14), b"", b"")  # L = 1 is reserved
    with pytest.raises(ValueError):
        ccm_encrypt(cipher, bytes(13), b"", bytes(1 << 16))  # too long for L = 2
