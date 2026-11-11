# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcm-mode/. The authors are listed in prov/74AABT.jsonl.

import random

import pytest

from aes import AES
from gcm_mode import (
    ONE,
    InvalidTag,
    gcm_decrypt,
    gcm_encrypt,
    gf_inverse,
    gf_mult,
    gf_sqrt,
    ghash,
    hash_subkey,
)

# The common data of Test Cases 3 to 6 and 16 of the GCM specification, Appendix B.
K3 = "feffe9928665731c6d6a8f9467308308"
P3 = (
    "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72"
    "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255"
)
P4 = P3[:-8]  # 60 bytes
A4 = "feedfacedeadbeeffeedfacedeadbeefabaddad2"
IV60 = (
    "9313225df88406e555909c5aff5269aa6a7a9538534f7da1e4c303d2a318a728"
    "c3c0c95156809539fcf0e2429a6b525416aedbf5a0de6a57a637b39b"
)


def test_aes_fips197_appendix_c1() -> None:
    key = bytes(range(16))
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert AES(key).encrypt_block(pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


@pytest.mark.parametrize(
    "case, key, iv, a, p, c, t",
    [
        # McGrew and Viega, The Galois/Counter Mode of Operation (GCM), Appendix B, Test Cases 1 to 6
        # (AES-128), Test Case 7 (AES-192) and Test Case 16 (AES-256).
        (1, "00" * 16, "00" * 12, "", "", "", "58e2fccefa7e3061367f1d57a4e7455a"),
        (2, "00" * 16, "00" * 12, "", "00" * 16, "0388dace60b6a392f328c2b971b2fe78", "ab6e47d42cec13bdf53a67b21257bddf"),
        (
            3,
            K3,
            "cafebabefacedbaddecaf888",
            "",
            P3,
            "42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e"
            "21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091473f5985",
            "4d5c2af327cd64a62cf35abd2ba6fab4",
        ),
        (
            4,
            K3,
            "cafebabefacedbaddecaf888",
            A4,
            P4,
            "42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e"
            "21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091",
            "5bc94fbc3221a5db94fae95ae7121a47",
        ),
        (
            5,
            K3,
            "cafebabefacedbad",
            A4,
            P4,
            "61353b4c2806934a777ff51fa22a4755699b2a714fcdc6f83766e5f97b6c7423"
            "73806900e49f24b22b097544d4896b424989b5e1ebac0f07c23f4598",
            "3612d2e79e3b0785561be14aaca2fccb",
        ),
        (
            6,
            K3,
            IV60,
            A4,
            P4,
            "8ce24998625615b603a033aca13fb894be9112a5c3a211a8ba262a3cca7e2ca7"
            "01e4a9a4fba43c90ccdcb281d48c7c6fd62875d2aca417034c34aee5",
            "619cc5aefffe0bfa462af43c1699d050",
        ),
        (7, "00" * 24, "00" * 12, "", "", "", "cd33b28ac773f74ba00ed1f312572435"),
        (
            16,
            K3 * 2,
            "cafebabefacedbaddecaf888",
            A4,
            P4,
            "522dc1f099567d07f47f37a32a84427d643a8cdcbfe5c0c97598a2bd2555d1aa"
            "8cb08e48590dbb3da7b08b1056828838c5f61e6393ba7a0abcc9f662",
            "76fc6ece0f4e1768cddf8853bb2d551b",
        ),
    ],
)
def test_gcm_spec_appendix_b(case: int, key: str, iv: str, a: str, p: str, c: str, t: str) -> None:
    cipher = AES(bytes.fromhex(key))
    got_c, got_t = gcm_encrypt(cipher, bytes.fromhex(iv), bytes.fromhex(a), bytes.fromhex(p))
    assert (got_c.hex(), got_t.hex()) == (c, t), case
    assert gcm_decrypt(cipher, bytes.fromhex(iv), bytes.fromhex(a), got_c, got_t).hex() == p


def test_intermediate_values_of_test_cases_2_and_3() -> None:
    # Appendix B: H, then X1 = C . H and GHASH(H, A, C) of Test Case 2, and H of Test Case 3.
    h = hash_subkey(AES(bytes(16)))
    assert h == 0x66E94BD4EF8A2C3B884CFA59CA342B2E
    c = bytes.fromhex("0388dace60b6a392f328c2b971b2fe78")
    assert gf_mult(int.from_bytes(c, "big"), h) == 0x5E2EC746917062882C85B0685353DEB7
    lengths = bytes(8) + (128).to_bytes(8, "big")
    assert ghash(h, c + lengths) == 0xF38CBB1AD69223DCC3457AE5B6B0F885
    assert hash_subkey(AES(bytes.fromhex(K3))) == 0xB83B533708BF535D0AA6E52980D53B78


def _reverse128(v: int) -> int:
    return int(f"{v:0128b}"[::-1], 2)


def _poly_mult(a: int, b: int) -> int:
    """Plain polynomial product modulo x^128 + x^7 + x^2 + x + 1, with bit i = coefficient of x^i."""
    z = 0
    for i in range(128):
        if (a >> i) & 1:
            z ^= b << i
    for i in range(254, 127, -1):
        if (z >> i) & 1:
            z ^= ((1 << 128) | 0x87) << (i - 128)
    return z


def test_gcm_bit_order_is_the_reflected_polynomial_basis() -> None:
    # gf_mult is the ordinary product modulo x^128 + x^7 + x^2 + x + 1 once each block is read with
    # its leftmost bit as the coefficient of x^0.
    rng = random.Random(38)
    for _ in range(50):
        x, y = rng.getrandbits(128), rng.getrandbits(128)
        assert _reverse128(gf_mult(x, y)) == _poly_mult(_reverse128(x), _reverse128(y))
    assert _reverse128(ONE) == 1 and _reverse128(0xE1 << 120) == 0x87


def test_field_laws() -> None:
    rng = random.Random(2004)
    for _ in range(10):
        x, y, z = (rng.getrandbits(128) for _ in range(3))
        assert gf_mult(x, ONE) == x
        assert gf_mult(x, y) == gf_mult(y, x)
        assert gf_mult(x, y ^ z) == gf_mult(x, y) ^ gf_mult(x, z)
        if x:
            assert gf_mult(x, gf_inverse(x)) == ONE
        assert gf_sqrt(gf_mult(x, x)) == x


@pytest.mark.parametrize("n", [0, 1, 15, 16, 17, 64])
def test_round_trip(n: int) -> None:
    rng = random.Random(n)
    cipher = AES(rng.randbytes(16))
    iv, a, p = rng.randbytes(12), rng.randbytes(n // 3), rng.randbytes(n)
    c, t = gcm_encrypt(cipher, iv, a, p)
    assert len(c) == n and gcm_decrypt(cipher, iv, a, c, t) == p


def test_one_changed_bit_is_rejected() -> None:
    rng = random.Random(7)
    cipher = AES(rng.randbytes(16))
    iv, a, p = rng.randbytes(12), b"header", rng.randbytes(33)
    c, t = gcm_encrypt(cipher, iv, a, p)
    for name, value in (("iv", iv), ("a", a), ("c", c), ("t", t)):
        for bit in range(len(value) * 8):
            changed = bytearray(value)
            changed[bit // 8] ^= 1 << (bit % 8)
            args = {"iv": iv, "a": a, "c": c, "t": t, name: bytes(changed)}
            with pytest.raises(InvalidTag):
                gcm_decrypt(cipher, args["iv"], args["a"], args["c"], args["t"])


def test_truncated_tag() -> None:
    cipher = AES(bytes(16))
    c, t = gcm_encrypt(cipher, bytes(12), b"", b"abc", tag_len=12)
    assert t == gcm_encrypt(cipher, bytes(12), b"", b"abc")[1][:12]
    assert gcm_decrypt(cipher, bytes(12), b"", c, t) == b"abc"


def nonce_reuse_attack(c1: bytes, t1: bytes, c2: bytes, t2: bytes) -> tuple[int, int]:
    """From two one-block messages with no AAD under one key and one IV, return (H, E_K(J0)).

    For one block, S = C . H^2 xor L . H with the same length block L, so
    T1 xor T2 = (C1 xor C2) . H^2. Divide, then take the square root.
    """
    d_c = int.from_bytes(c1, "big") ^ int.from_bytes(c2, "big")
    d_t = int.from_bytes(t1, "big") ^ int.from_bytes(t2, "big")
    h = gf_sqrt(gf_mult(d_t, gf_inverse(d_c)))
    lengths = bytes(8) + (128).to_bytes(8, "big")
    ek_j0 = int.from_bytes(t1, "big") ^ ghash(h, c1 + lengths)
    return h, ek_j0


def test_nonce_reuse_recovers_h_and_forges() -> None:
    rng = random.Random(2006)
    for _ in range(5):
        cipher = AES(rng.randbytes(16))
        iv = rng.randbytes(12)  # used twice: the mistake
        p1, p2 = b"pay 10 EUR to A.", b"pay 20 EUR to B."
        c1, t1 = gcm_encrypt(cipher, iv, b"", p1)
        c2, t2 = gcm_encrypt(cipher, iv, b"", p2)
        h, ek_j0 = nonce_reuse_attack(c1, t1, c2, t2)
        assert h == hash_subkey(cipher)
        # The known plaintext p1 gives the keystream block; the attacker makes a new message
        # and a new header, and computes the tag with H and E_K(J0) alone.
        keystream = bytes(x ^ y for x, y in zip(p1, c1))
        forged_p, forged_a = b"pay 9999 EUR, E.", b"approved"
        forged_c = bytes(x ^ y for x, y in zip(forged_p, keystream))
        block = forged_a + bytes(8) + forged_c + (8 * len(forged_a)).to_bytes(8, "big") + (128).to_bytes(8, "big")
        forged_t = (ghash(h, block) ^ ek_j0).to_bytes(16, "big")
        assert gcm_decrypt(cipher, iv, forged_a, forged_c, forged_t) == forged_p


def test_fresh_ivs_stop_the_attack() -> None:
    rng = random.Random(9)
    cipher = AES(rng.randbytes(16))
    c1, t1 = gcm_encrypt(cipher, rng.randbytes(12), b"", b"pay 10 EUR to A.")
    c2, t2 = gcm_encrypt(cipher, rng.randbytes(12), b"", b"pay 20 EUR to B.")
    h, _ = nonce_reuse_attack(c1, t1, c2, t2)
    assert h != hash_subkey(cipher)
