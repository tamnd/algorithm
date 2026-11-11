# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eax-mode/. The authors are listed in prov/V9AB4V.jsonl.

import random

import pytest

from aes import AES
from eax_mode import (
    INVALID,
    EaxHeader,
    EaxOnlineEncryptor,
    eax_decrypt,
    eax_encrypt,
    omac,
    omac_t,
)


def test_aes_fips197_appendix_c1() -> None:
    key = bytes(range(16))
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert AES(key).encrypt_block(pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_omac_is_cmac_rfc4493() -> None:
    # RFC 4493, Section 4, Examples 1 and 2 (OMAC with 2L and 4L is AES-CMAC).
    cipher = AES(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
    assert omac(cipher, b"").hex() == "bb1d6929e95937287fa37d129b756746"
    m = bytes.fromhex("6bc1bee22e409f96e93d7e117393172a")
    assert omac(cipher, m).hex() == "070a16b46b4d4144f79bdd9dd04a287c"


# Bellare, Rogaway and Wagner, The EAX Mode of Operation, full version of January 18, 2004,
# Appendix G "Test Vectors" (EAX-AES128 vectors by Jack Lloyd, checked by Brian Gladman).
# Each row: MSG, KEY, NONCE, HEADER, CIPHER (ciphertext followed by the 16-byte tag).
EAX_PAPER_APPENDIX_G = [
    (
        "",
        "233952dee4d5ed5f9b9c6d6ff80ff478",
        "62ec67f9c3a4a407fcb2a8c49031a8b3",
        "6bfb914fd07eae6b",
        "e037830e8389f27b025a2d6527e79d01",
    ),
    (
        "f7fb",
        "91945d3f4dcbee0bf45ef52255f095a4",
        "becaf043b0a23d843194ba972c66debd",
        "fa3bfd4806eb53fa",
        "19dd5c4c9331049d0bdab0277408f67967e5",
    ),
    (
        "1a47cb4933",
        "01f74ad64077f2e704c0f60ada3dd523",
        "70c3db4f0d26368400a10ed05d2bff5e",
        "234a3463c1264ac6",
        "d851d5bae03a59f238a23e39199dc9266626c40f80",
    ),
    (
        "481c9e39b1",
        "d07cf6cbb7f313bdde66b727afd3c5e8",
        "8408dfff3c1a2b1292dc199e46b7d617",
        "33cce2eabff5a79d",
        "632a9d131ad4c168a4225d8e1ff755939974a7bede",
    ),
    (
        "40d0c07da5e4",
        "35b6d0580005bbc12b0587124557d2c2",
        "fdb6b06676eedc5c61d74276e1f8e816",
        "aeb96eaebe2970e9",
        "071dfe16c675cb0677e536f73afe6a14b74ee49844dd",
    ),
    (
        "4de3b35c3fc039245bd1fb7d",
        "bd8e6e11475e60b268784c38c62feb22",
        "6eac5c93072d8e8513f750935e46da1b",
        "d4482d1ca78dce0f",
        "835bb4f15d743e350e728414abb8644fd6ccb86947c5e10590210a4f",
    ),
    (
        "8b0a79306c9ce7ed99dae4f87f8dd61636",
        "7c77d6e813bed5ac98baa417477a2e7d",
        "1a8c98dcd73d38393b2bf1569deefc19",
        "65d2017990d62528",
        "02083e3979da014812f59f11d52630da30137327d10649b0aa6e1c181db617d7f2",
    ),
    (
        "1bda122bce8a8dbaf1877d962b8592dd2d56",
        "5fff20cafab119ca2fc73549e20f5b0d",
        "dde59b97d722156d4d9aff2bc7559826",
        "54b9f04e6a09189a",
        "2ec47b2c4954a489afc7ba4897edcdae8cc33b60450599bd02c96382902aef7f832a",
    ),
    (
        "6cf36720872b8513f6eab1a8a44438d5ef11",
        "a4a4782bcffd3ec5e7ef6d8c34a56123",
        "b781fcf2f75fa5a8de97a9ca48e522ec",
        "899a175897561d7e",
        "0de18fd0fdd91e7af19f1d8ee8733938b1e8e7f6d2231618102fdb7fe55ff1991700",
    ),
    (
        "ca40d7446e545ffaed3bd12a740a659ffbbb3ceab7",
        "8395fcf1e95bebd697bd010bc766aac3",
        "22e7add93cfc6393c57ec0b3c17d6b44",
        "126735fcc320d25a",
        "cb8920f87a6c75cff39627b56e3ed197c552d295a7cfc46afc253b4652b1af3795b124ab6e",
    ),
]


@pytest.mark.parametrize("msg, key, nonce, header, cipher_hex", EAX_PAPER_APPENDIX_G)
def test_eax_paper_appendix_g(msg: str, key: str, nonce: str, header: str, cipher_hex: str) -> None:
    cipher = AES(bytes.fromhex(key))
    n, h, m = bytes.fromhex(nonce), bytes.fromhex(header), bytes.fromhex(msg)
    assert eax_encrypt(cipher, n, h, m).hex() == cipher_hex
    assert eax_decrypt(cipher, n, h, bytes.fromhex(cipher_hex)) == m


def test_first_vector_intermediates() -> None:
    # Vector 1 has an empty message: the tag is N' xor C' xor H' with C' = OMAC^2(empty).
    _, key, nonce, header, cipher_hex = EAX_PAPER_APPENDIX_G[0]
    cipher = AES(bytes.fromhex(key))
    n1 = omac_t(cipher, 0, bytes.fromhex(nonce))
    h1 = omac_t(cipher, 1, bytes.fromhex(header))
    c1 = omac_t(cipher, 2, b"")
    assert bytes(a ^ b ^ c for a, b, c in zip(n1, h1, c1)).hex() == cipher_hex


def test_static_header_is_processed_once() -> None:
    rng = random.Random(1)
    cipher = AES(rng.randbytes(16))
    h = rng.randbytes(100)
    pre = EaxHeader(cipher, h)
    for length in (0, 1, 16, 33):
        n, m = rng.randbytes(16), rng.randbytes(length)
        assert pre.encrypt(n, m) == eax_encrypt(cipher, n, h, m)


def test_online_encryption_does_not_need_the_length() -> None:
    rng = random.Random(2)
    cipher = AES(rng.randbytes(16))
    n, h, m = rng.randbytes(16), b"hdr", rng.randbytes(77)
    enc = EaxOnlineEncryptor(cipher, n, h)
    out = b""
    pos = 0
    for size in (1, 15, 16, 2, 30, 13):  # chunk sizes; the last chunk ends the message
        out += enc.update(m[pos : pos + size])
        pos += size
    assert pos == len(m)
    assert out + enc.finish() == eax_encrypt(cipher, n, h, m)


def test_any_nonce_length_and_round_trips() -> None:
    rng = random.Random(3)
    cipher = AES(rng.randbytes(16))
    for length in (0, 1, 15, 16, 17, 48, 100):
        n = rng.randbytes(rng.choice([0, 1, 12, 16, 40]))
        h, m = rng.randbytes(rng.randrange(40)), rng.randbytes(length)
        for tau in (0, 4, 12, 16):
            ct = eax_encrypt(cipher, n, h, m, tau)
            assert len(ct) == length + tau
            assert eax_decrypt(cipher, n, h, ct, tau) == m


def test_one_changed_bit_is_rejected() -> None:
    rng = random.Random(4)
    cipher = AES(rng.randbytes(16))
    n, h, m = rng.randbytes(16), rng.randbytes(9), rng.randbytes(40)
    ct = eax_encrypt(cipher, n, h, m)
    for bit in range(len(ct) * 8):
        bad = bytearray(ct)
        bad[bit // 8] ^= 1 << (bit % 8)
        assert eax_decrypt(cipher, n, h, bytes(bad)) == INVALID
    for bit in range(len(h) * 8):
        bad_h = bytearray(h)
        bad_h[bit // 8] ^= 1 << (bit % 8)
        assert eax_decrypt(cipher, n, bytes(bad_h), ct) == INVALID
    assert eax_decrypt(cipher, n[:-1] + bytes([n[-1] ^ 1]), h, ct) == INVALID
    assert eax_decrypt(cipher, n, h, ct[:15]) == INVALID  # shorter than the tag


def test_tweaks_separate_nonce_header_and_ciphertext() -> None:
    # Without the tweaks 0, 1, 2, swapping the nonce and the header would keep N' xor H'.
    rng = random.Random(5)
    cipher = AES(rng.randbytes(16))
    x, y = rng.randbytes(16), rng.randbytes(16)
    assert eax_encrypt(cipher, x, y, b"") != eax_encrypt(cipher, y, x, b"")
    assert omac_t(cipher, 0, x) != omac_t(cipher, 1, x) != omac_t(cipher, 2, x)


class CountingAES(AES):
    calls = 0

    def encrypt_block(self, block: bytes) -> bytes:
        CountingAES.calls += 1
        return super().encrypt_block(block)


def test_rejection_costs_about_half_of_decryption() -> None:
    cipher = CountingAES(bytes(16))
    n, h, m = bytes(16), b"", bytes(16 * 40)
    ct = eax_encrypt(cipher, n, h, m)
    CountingAES.calls = 0
    assert eax_decrypt(cipher, n, h, ct) == m
    full = CountingAES.calls
    CountingAES.calls = 0
    assert eax_decrypt(cipher, n, h, ct[:-1] + bytes([ct[-1] ^ 1])) == INVALID
    rejected = CountingAES.calls
    assert full - rejected == 40  # the CTR pass is skipped on rejection
    assert rejected < 0.6 * full


def test_nonce_reuse_leaks_the_xor_of_plaintexts() -> None:
    rng = random.Random(6)
    cipher = AES(rng.randbytes(16))
    n, h = rng.randbytes(16), b""
    p1, p2 = b"attack at dawn, gate 3", b"retreat at six, gate 9"
    c1 = eax_encrypt(cipher, n, h, p1)[: len(p1)]
    c2 = eax_encrypt(cipher, n, h, p2)[: len(p2)]
    assert bytes(a ^ b for a, b in zip(c1, c2)) == bytes(a ^ b for a, b in zip(p1, p2))
    # With a new nonce the XOR of ciphertexts says nothing of this kind.
    c3 = eax_encrypt(cipher, rng.randbytes(16), h, p2)[: len(p2)]
    assert bytes(a ^ b for a, b in zip(c1, c3)) != bytes(a ^ b for a, b in zip(p1, p2))
