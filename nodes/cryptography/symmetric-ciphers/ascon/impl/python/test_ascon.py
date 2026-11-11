# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ascon/. The authors are listed in prov/F7H5VG.jsonl.

import random

from ascon import ascon_aead128_decrypt, ascon_aead128_encrypt, ascon_p

KEY = bytes(range(16))
NONCE = bytes(range(16, 32))

# Known-answer tests for Ascon-AEAD128 (SP 800-232) from the designers' reference
# code ascon-c, file LWC_AEAD_KAT_128_128.txt. Key 000102...0F, nonce 101112...1F.
# Each entry: (Count, plaintext, associated data, ciphertext followed by the tag).
KAT = [
    (1, "", "", "4F9C278211BEC9316BF68F46EE8B2EC6"),
    (2, "", "30", "CCCB674FE18A09A285D6AB11B35675C0"),
    (3, "", "3031", "F65B191550C4DF9CFDD4460EBBCCA782"),
    (34, "20", "", "E8DD576ABA1CD3E6FC704DE02AEDB79588"),
    (35, "20", "30", "962B8016836C75A7D86866588CA245D886"),
    (
        545,
        "202122232425262728292A2B2C2D2E2F",
        "303132333435363738393A3B3C3D3E3F",
        "6373EBB28BE97C9BAC090CF399C13EF13ABFC0D209E8F4844C90814D13F32C59",
    ),
    (
        765,
        "202122232425262728292A2B2C2D2E2F30313233343536",
        "3031323334",
        "3076658CBA8BF3BB6DCCAA2F1255EE2E7DB6C1FA9B1D1E94271131B6D127FDC87A7F6F826F2663",
    ),
]

# SP 800-232 Table 6: the S-box as a table, x0 being the most significant bit of x.
SBOX = [
    0x04, 0x0B, 0x1F, 0x14, 0x1A, 0x15, 0x09, 0x02, 0x1B, 0x05, 0x08, 0x12, 0x1D, 0x03, 0x06, 0x1C,
    0x1E, 0x13, 0x07, 0x0E, 0x00, 0x0D, 0x11, 0x18, 0x10, 0x0C, 0x01, 0x19, 0x16, 0x0A, 0x0F, 0x17,
]


def test_known_answers() -> None:
    for _, pt, ad, expected in KAT:
        p, a = bytes.fromhex(pt), bytes.fromhex(ad)
        c, t = ascon_aead128_encrypt(KEY, NONCE, a, p)
        assert (c + t).hex().upper() == expected
        assert ascon_aead128_decrypt(KEY, NONCE, a, c, t) == p


def test_bitsliced_sbox_matches_the_table() -> None:
    # Apply the bitsliced instructions of ascon_p to single bits (one slice) and
    # compare with the table for all 32 inputs.
    mask = (1 << 64) - 1
    for x in range(32):
        bits = [(x >> (4 - i)) & 1 for i in range(5)]
        x0, x1, x2, x3, x4 = bits
        x0 ^= x4
        x4 ^= x3
        x2 ^= x1
        t = [(~x0 & x1), (~x1 & x2), (~x2 & x3), (~x3 & x4), (~x4 & x0)]
        x0 ^= t[1]
        x1 ^= t[2]
        x2 ^= t[3]
        x3 ^= t[4]
        x4 ^= t[0]
        x1 ^= x0
        x0 ^= x4
        x3 ^= x2
        x2 = ~x2
        y = [v & 1 & mask for v in (x0, x1, x2, x3, x4)]
        assert sum(b << (4 - i) for i, b in enumerate(y)) == SBOX[x]


def test_permutation_is_deterministic_and_mixes() -> None:
    rng = random.Random(1)
    s = [rng.getrandbits(64) for _ in range(5)]
    a, b = list(s), list(s)
    b[0] ^= 1
    ascon_p(a, 12)
    ascon_p(b, 12)
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    assert 120 < diff < 200


def test_round_trip_and_forgery_rejected() -> None:
    rng = random.Random(2)
    for _ in range(40):
        key, nonce = rng.randbytes(16), rng.randbytes(16)
        ad, pt = rng.randbytes(rng.randrange(40)), rng.randbytes(rng.randrange(50))
        c, t = ascon_aead128_encrypt(key, nonce, ad, pt)
        assert len(c) == len(pt)
        assert ascon_aead128_decrypt(key, nonce, ad, c, t) == pt
        bad_t = bytes([t[0] ^ 1]) + t[1:]
        assert ascon_aead128_decrypt(key, nonce, ad, c, bad_t) is None
        if c:
            j = rng.randrange(len(c))
            bad_c = c[:j] + bytes([c[j] ^ 0x80]) + c[j + 1:]
            assert ascon_aead128_decrypt(key, nonce, ad, bad_c, t) is None
        assert ascon_aead128_decrypt(key, nonce, ad + b"x", c, t) is None


def test_empty_ad_differs_from_one_padding_block() -> None:
    # Empty associated data skips absorption, so it differs from AD = one zero byte.
    c1, t1 = ascon_aead128_encrypt(KEY, NONCE, b"", b"hello")
    c2, t2 = ascon_aead128_encrypt(KEY, NONCE, b"\x00", b"hello")
    assert t1 != t2
