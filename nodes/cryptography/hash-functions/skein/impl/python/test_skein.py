# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skein/. The authors are listed in prov/WAM1AS.jsonl.

import random

import pytest

from skein import T_PRS, initial_chaining_value, skein, skein256, skein512, skein1024, threefish_encrypt


def h(s: str) -> bytes:
    return bytes.fromhex(s.replace(" ", "").replace("\n", ""))


# The Skein Hash Function Family, version 1.3, Appendix C: messages FF, then FF FE FD ... downwards.
MSG1 = bytes([0xFF])
MSG32 = bytes(range(0xFF, 0xFF - 32, -1))
MSG64 = bytes(range(0xFF, 0xFF - 64, -1))
MSG128 = bytes(range(0xFF, -1, -1))[:128]

VECTORS = [
    # Appendix C.1, Skein-256-256
    (32, 256, MSG1, "0B 98 DC D1 98 EA 0E 50 A7 A2 44 C4 44 E2 5C 23 DA 30 C1 0F C9 A1 F2 70 A6 63 7F 1F 34 E6 7E D2"),
    (32, 256, MSG32, "8D 0F A4 EF 77 7F D7 59 DF D4 04 4E 6F 6A 5A C3 C7 74 AE C9 43 DC FC 07 92 7B 72 3B 5D BF 40 8B"),
    (32, 256, MSG64, "DF 28 E9 16 63 0D 0B 44 C4 A8 49 DC 9A 02 F0 7A 07 CB 30 F7 32 31 82 56 B1 5D 86 5A C4 AE 16 2F"),
    # Appendix C.2, Skein-512-512
    (64, 512, MSG1,
     "71 B7 BC E6 FE 64 52 22 7B 9C ED 60 14 24 9E 5B F9 A9 75 4C 3A D6 18 CC C4 E0 AA E1 6B 31 6C C8"
     "CA 69 8D 86 43 07 ED 3E 80 B6 EF 15 70 81 2A C5 27 2D C4 09 B5 A0 12 DF 2A 57 91 02 F3 40 61 7A"),
    (64, 512, MSG64,
     "45 86 3B A3 BE 0C 4D FC 27 E7 5D 35 84 96 F4 AC 9A 73 6A 50 5D 93 13 B4 2B 2F 5E AD A7 9F C1 7F"
     "63 86 1E 94 7A FB 1D 05 6A A1 99 57 5A D3 F8 C9 A3 CC 17 80 B5 E5 FA 4C AE 05 0E 98 98 76 62 5B"),
    (64, 512, MSG128,
     "91 CC A5 10 C2 63 C4 DD D0 10 53 0A 33 07 33 09 62 86 31 F3 08 74 7E 1B CB AA 90 E4 51 CA B9 2E"
     "51 88 08 7A F4 18 87 73 A3 32 30 3E 66 67 A7 A2 10 85 6F 74 21 39 00 00 71 F4 8E 8B A2 A5 AD B7"),
    # Appendix C.3, Skein-1024-1024
    (128, 1024, MSG1,
     "E6 2C 05 80 2E A0 15 24 07 CD D8 78 7F DA 9E 35 70 3D E8 62 A4 FB C1 19 CF F8 59 0A FE 79 25 0B"
     "CC C8 B3 FA F1 BD 24 22 AB 5C 0D 26 3F B2 F8 AF B3 F7 96 F0 48 00 03 81 53 1B 6F 00 D8 51 61 BC"
     "0F FF 4B EF 24 86 B1 EB CD 37 73 FA BF 50 AD 4A D5 63 9A F9 04 0E 3F 29 C6 C9 31 30 1B F7 98 32"
     "E9 DA 09 85 7E 83 1E 82 EF 8B 46 91 C2 35 65 65 15 D4 37 D2 BD A3 3B CE C0 01 C6 7F FD E1 5B A8"),
    (128, 1024, MSG128,
     "1F 3E 02 C4 6F B8 0A 3F CD 2D FB BC 7C 17 38 00 B4 0C 60 C2 35 4A F5 51 18 9E BF 43 3C 3D 85 F9"
     "FF 18 03 E6 D9 20 49 31 79 ED 7A E7 FC E6 9C 35 81 A5 A2 F8 2D 3E 0C 7A 29 55 74 D0 CD 7D 21 7C"
     "48 4D 2F 63 13 D5 9A 77 18 EA D0 7D 07 29 C2 48 51 D7 E7 D2 49 1B 90 2D 48 91 94 E6 B7 D3 69 DB"
     "0A B7 AA 10 6F 0E E0 A3 9A 42 EF C5 4F 18 D9 37 76 08 09 85 F9 07 57 4F 99 5E C6 A3 71 53 A5 78"),
]

# Appendix C.3, third vector: the 256 bytes FF FE ... 01 00.
MSG256 = bytes(range(0xFF, -1, -1))
SKEIN1024_256 = (
    "84 2A 53 C9 9C 12 B0 CF 80 CF 69 49 1B E5 E2 F7 51 5D E8 73 3B 6E A9 42 2D FD 67 66 65 B5 FA 42"
    "FF B3 A9 C4 8C 21 77 77 95 08 48 CE CD B4 8F 64 0F 81 FB 92 BE F6 F8 8F 7A 85 C1 F7 CD 14 46 C9"
    "16 1C 0A FE 8F 25 AE 44 4F 40 D3 68 00 81 C3 5A A4 3F 64 0F D5 FA 3C 3C 03 0B CC 06 AB AC 01 D0"
    "98 BC C9 84 EB D8 32 27 12 92 1E 00 B1 BA 07 D6 D0 1F 26 90 70 50 25 5E F2 C8 E2 4F 71 6C 52 A5"
)


@pytest.mark.parametrize("nb,no,msg,want", VECTORS)
def test_appendix_c_vectors(nb: int, no: int, msg: bytes, want: str) -> None:
    assert skein(nb, no, msg) == h(want)


def test_appendix_c3_third_vector() -> None:
    assert len(MSG256) == 256 and MSG256[-1] == 0
    assert skein1024(MSG256) == h(SKEIN1024_256)


# Appendix B: the precomputed initial chaining values G0 for simple hashing.
@pytest.mark.parametrize("nb,no,want", [
    (32, 256, [0xFC9DA860D048B449, 0x2FCA66479FA7D833, 0xB33BC3896656840F, 0x6A54E920FDE8DA69]),  # B.4
    (32, 128, [0xE1111906964D7260, 0x883DAAA77C8D811C, 0x10080DF491960F7A, 0xCCF7DDE5B45BC1C2]),  # B.1
    (64, 512, [0x4903ADFF749C51CE, 0x0D95DE399746DF03, 0x8FD1934127C79BCE, 0x9A255629FF352CB1,
               0x5DB62599DF6CA7B0, 0xEABE394CA9D5C3F4, 0x991112C71A75B523, 0xAE18A40B660FCC33]),  # B.10
    (64, 256, [0xCCD044A12FDB3E13, 0xE83590301A79A9EB, 0x55AEA0614F816E6F, 0x2A2767A4AE9B94DB,
               0xEC06025E74DD7683, 0xE7A436CDC4746251, 0xC36FBAF9393AD185, 0x3EEDBA1833EDFC13]),  # B.8
    (128, 1024, [0xD593DA0741E72355, 0x15B5E511AC73E00C, 0x5180E5AEBAF2C4F0, 0x03BD41D3FCBCAFAF,
                 0x1CAEC6FD1983A898, 0x6E510B8BCDD0589F, 0x77E2BDFDC6394ADA, 0xC11E1DB524DCB0A3,
                 0xD6D14AF9C6329AB5, 0x6A9B0BFC6EB67E0D, 0x9243C60DCCFF1332, 0x1A1F1DDE743F02D4,
                 0x0996753C10ED0BB8, 0x6572DD22F2B4969A, 0x61FD3062D00A579A, 0x1DE0536E8682E539]),  # B.13
])
def test_appendix_b_initial_chaining_values(nb: int, no: int, want: list[int]) -> None:
    assert initial_chaining_value(nb, no) == want


def test_output_size_changes_whole_digest() -> None:
    # No is in the configuration block, so Skein-512-256 is not a prefix of Skein-512-512.
    assert skein512(b"abc", 256) != skein512(b"abc", 512)[:32]
    assert len(skein512(b"abc", 1024)) == 128  # any output size from one state


def test_mac_wrong_key_fails() -> None:
    key = bytes(range(32))
    tag = skein512(b"message", 256, key=key)
    assert skein512(b"message", 256, key=key) == tag
    assert skein512(b"message", 256, key=bytes(31) + b"\x01") != tag
    assert skein512(b"message", 256) != tag  # unkeyed differs


def test_personalization_separates() -> None:
    a = skein(64, 256, b"m", extra=((T_PRS, b"app one"),))
    b = skein(64, 256, b"m", extra=((T_PRS, b"app two"),))
    assert a != b != skein512(b"m", 256)


def test_zero_padding_is_not_ambiguous() -> None:
    # UBI pads with zero bytes, but the Position field holds the true length.
    assert skein256(b"") != skein256(b"\x00")
    assert skein256(b"\x00" * 31) != skein256(b"\x00" * 32)


def test_threefish_is_a_permutation_sample() -> None:
    rng = random.Random(3)
    key, tweak = rng.randbytes(64), rng.randbytes(16)
    outs = {threefish_encrypt(key, tweak, rng.randbytes(64)) for _ in range(50)}
    assert len(outs) == 50


def test_avalanche() -> None:
    rng = random.Random(5)
    total = 0
    trials = 30
    for _ in range(trials):
        m = bytearray(rng.randbytes(40))
        a = int.from_bytes(skein512(bytes(m), 256), "big")
        bit = rng.randrange(320)
        m[bit // 8] ^= 1 << (bit % 8)
        total += bin(a ^ int.from_bytes(skein512(bytes(m), 256), "big")).count("1")
    assert 118 <= total / trials <= 138  # about 128 of 256 bits


def test_bad_parameters() -> None:
    with pytest.raises(ValueError):
        skein(48, 256, b"")
    with pytest.raises(ValueError):
        skein(64, 12, b"")
