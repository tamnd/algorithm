# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/advanced-encryption-standard/. The authors are listed in prov/4E36FN.jsonl.

import random

from advanced_encryption_standard import (
    INV_SBOX,
    SBOX,
    add_round_key,
    decrypt_block,
    encrypt_block,
    inv_mix_columns,
    key_expansion,
    mix_columns,
    shift_rows,
    sub_bytes,
)

PT = bytes.fromhex("00112233445566778899aabbccddeeff")


def word(w: list[int]) -> str:
    return bytes(w).hex()


# FIPS 197 (November 26, 2001), Appendix C.1, AES-128 (Nk=4, Nr=10).
def test_fips197_c1() -> None:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    ct = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# FIPS 197 (2001), Appendix C.1: the state after round 1 and the round key of round 1.
def test_fips197_c1_round1() -> None:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    w = key_expansion(key)
    assert "".join(word(x) for x in w[4:8]) == "d6aa74fdd2af72fadaa678f1d6ab76fe"
    s = add_round_key(list(PT), w, 0)
    assert bytes(s).hex() == "00102030405060708090a0b0c0d0e0f0"
    s = sub_bytes(s)
    assert bytes(s).hex() == "63cab7040953d051cd60e0e7ba70e18c"
    s = shift_rows(s)
    assert bytes(s).hex() == "6353e08c0960e104cd70b751bacad0e7"
    s = add_round_key(mix_columns(s), w, 1)
    assert bytes(s).hex() == "89d810e8855ace682d1843d8cb128fe4"


# FIPS 197 (2001), Appendix C.2, AES-192 (Nk=6, Nr=12).
def test_fips197_c2() -> None:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f1011121314151617")
    ct = bytes.fromhex("dda97ca4864cdfe06eaf70a0ec0d7191")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# FIPS 197 (2001), Appendix C.3, AES-256 (Nk=8, Nr=14).
def test_fips197_c3() -> None:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    ct = bytes.fromhex("8ea2b7ca516745bfeafc49904b496089")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# FIPS 197 (2023 update), Appendix A.1, expansion of a 128-bit key: w36 and w40 to w43.
def test_fips197_a1() -> None:
    w = key_expansion(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
    assert len(w) == 44
    assert [word(w[i]) for i in range(4)] == ["2b7e1516", "28aed2a6", "abf71588", "09cf4f3c"]
    assert word(w[36]) == "ac7766f3"
    assert [word(w[i]) for i in range(40, 44)] == ["d014f9a8", "c9ee2589", "e13f0cc8", "b6630ca6"]


# FIPS 197 (2023 update), Appendix A.2, expansion of a 192-bit key: w6 to w8 and w44 to w51.
def test_fips197_a2() -> None:
    w = key_expansion(bytes.fromhex("8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b"))
    assert len(w) == 52
    assert [word(w[i]) for i in (6, 7, 8)] == ["fe0c91f7", "2402f5a5", "ec12068e"]
    assert [word(w[i]) for i in range(44, 52)] == [
        "ca400538", "8fcc5006", "282d166a", "bc3ce7b5",
        "e98ba06f", "448c773c", "8ecc7204", "01002202",
    ]


# FIPS 197 (2023 update), Appendix A.3, expansion of a 256-bit key: w8 and w44 to w47, w54 to w59.
def test_fips197_a3() -> None:
    key = bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4")
    w = key_expansion(key)
    assert len(w) == 60
    assert word(w[8]) == "9ba35411"
    assert [word(w[i]) for i in range(44, 48)] == ["5886ca5d", "2e2f31d7", "7e0af1fa", "27cf73c3"]
    assert [word(w[i]) for i in range(54, 60)] == [
        "9adf6ace", "bd10190d", "fe4890d1", "e6188d0b", "046df344", "706c631e",
    ]


# FIPS 197 (2023 update), Appendix B: input 3243f6a8..., key of Appendix A.1.
def test_fips197_appendix_b() -> None:
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    pt = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
    ct = encrypt_block(key, pt)
    assert ct.hex() == "3925841d02dc09fbdc118597196a0b32"
    assert decrypt_block(key, ct) == pt


# FIPS 197 (2023 update), Section 5.1.1 and Table 4: SBOX({53}) = {ed}, and some other entries.
def test_sbox_entries() -> None:
    assert SBOX[0x53] == 0xED
    assert SBOX[0x00] == 0x63 and SBOX[0x01] == 0x7C and SBOX[0xFF] == 0x16
    assert SBOX[0x10] == 0xCA and SBOX[0xF0] == 0x8C
    assert sorted(SBOX) == list(range(256))
    assert all(INV_SBOX[SBOX[b]] == b for b in range(256))


def test_mix_columns_inverse() -> None:
    rng = random.Random(197)
    for _ in range(200):
        s = [rng.randrange(256) for _ in range(16)]
        assert inv_mix_columns(mix_columns(s)) == s
    # FIPS 197 (2001), Appendix C.1, round 1: s_row -> m_col.
    s_row = list(bytes.fromhex("6353e08c0960e104cd70b751bacad0e7"))
    assert bytes(mix_columns(s_row)).hex() == "5f72641557f5bc92f7be3b291db9f91a"


def test_round_trip() -> None:
    rng = random.Random(2001)
    for n in (16, 24, 32):
        for _ in range(30):
            key = bytes(rng.randrange(256) for _ in range(n))
            pt = bytes(rng.randrange(256) for _ in range(16))
            assert decrypt_block(key, encrypt_block(key, pt)) == pt


def test_avalanche() -> None:
    # Flip one plaintext bit: about half of the 128 output bits change.
    rng = random.Random(4)
    total, trials = 0, 200
    for _ in range(trials):
        key = bytes(rng.randrange(256) for _ in range(16))
        pt = bytes(rng.randrange(256) for _ in range(16))
        bit = rng.randrange(128)
        pt2 = bytearray(pt)
        pt2[bit // 8] ^= 1 << (bit % 8)
        a = int.from_bytes(encrypt_block(key, pt), "big")
        b = int.from_bytes(encrypt_block(key, bytes(pt2)), "big")
        total += bin(a ^ b).count("1")
    assert 60 < total / trials < 68


def test_bad_lengths() -> None:
    for n in (0, 15, 17, 33):
        try:
            key_expansion(bytes(n))
        except ValueError:
            pass
        else:
            raise AssertionError("a bad key length must fail")
