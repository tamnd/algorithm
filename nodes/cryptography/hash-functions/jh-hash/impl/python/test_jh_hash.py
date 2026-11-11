# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jh-hash/. The authors are listed in prov/TGYCB3.jsonl.

import random

import pytest

from jh_hash import CONSTANTS, compress, jh, jh256, jh512, linear, pad, permute

# Final-round package jh_20110116.zip from the designer's page, files KAT_MCT/ShortMsgKAT_256.txt
# and KAT_MCT/ShortMsgKAT_512.txt: entries Len = 0, 8, 16, 512 and 1024 (bits).
MSG512 = (
    "E926AE8B0AF6E53176DBFFCC2A6B88C6BD765F939D3D178A9BDE9EF3AA131C61"
    "E31C1E42CDFAF4B4DCDE579A37E150EFBEF5555B4C1CB40439D835A724E2FAE7"
)
MSG1024 = (
    "2B6DB7CED8665EBE9DEB080295218426BDAA7C6DA9ADD2088932CDFFBAA1C141"
    "29BCCDD70F369EFB149285858D2B1D155D14DE2FDB680A8B027284055182A0CA"
    "E275234CC9C92863C1B4AB66F304CF0621CD54565F5BFF461D3B461BD40DF281"
    "98E3732501B4860EADD503D26D6E69338F4E0456E9E9BAF3D827AE685FB1D817"
)
KAT_256 = [
    ("", "46E64619C18BB0A92A5E87185A47EEF83CA747B8FCC8E1412921357E326DF434"),
    ("CC", "7B1191F13A2667830142541BFC5918543D2A434C7692E70C3E5E9BBDDDB7F581"),
    ("41FB", "EF3EEEAE2D2457DB084F2A933647D9E77A476EB4E58569A18AD4BA55754F9034"),
    (MSG512, "9D35C0CC1880A36EBB6CB33B732C0C2ADB4A418B4BF0DF9173B539263653E90B"),
    (MSG1024, "43B7D01D93213874B2AC0792BED8C137E865BA5FA87B20A3151A984F4AF267A6"),
]
KAT_512 = [
    ("", "90ECF2F76F9D2C8017D979AD5AB96B87D58FC8FC4B83060F3F900774FAA2C8FA"
         "BE69C5F4FF1EC2B61D6B316941CEDEE117FB04B1F4C5BC1B919AE841C50EEC4F"),
    ("CC", "277C93806945992A7F10102F28471AF2783FE32003B3F63320810E74F1BC233B"
           "F8669AB4B922DB9EF13FCDCD4D31193B731EEDDE98FC87C129C04A4A1071F66F"),
    ("41FB", "5D80BE996BA553A0C68FD539FF3859CED2D1FA627AFADDE83464A9F67CAB6D66"
             "A32749B5228482A5F4A11332D62974547CB8FF90EBA9DDF03272F873457563F0"),
    (MSG512, "D1DBACB16C6A88BEA992CD34F92D1375F05215037CF989E155D324D6D1E42043"
             "20CF18C1AD6BF11019CDD112BAC3C7CB73E41A94254B8C5AF3DB8245318FFC70"),
    (MSG1024, "9EC6669F30F482A65D93FE7811923B6BDF3A1BDE032502E0B1A064C9D893C035"
              "07576FC4FBC745D458C1402BA76F7D4C4539C4DFED7C058596FA270416865162"),
]


@pytest.mark.parametrize("msg,want", KAT_256)
def test_short_msg_kat_256(msg: str, want: str) -> None:
    assert jh256(bytes.fromhex(msg)) == bytes.fromhex(want)


@pytest.mark.parametrize("msg,want", KAT_512)
def test_short_msg_kat_512(msg: str, want: str) -> None:
    assert jh512(bytes.fromhex(msg)) == bytes.fromhex(want)


def test_round_constants_appendix_a1() -> None:
    # Appendix A.1 of the round 3 specification: C_0, C_1, C_2, C_40 and C_41 of E_8.
    want = {
        0: "6a09e667f3bcc908b2fb1366ea957d3e3adec17512775099da2f590b0667322a",
        1: "bb896bf05955abcd5281828d66e7d99ac4203494f89bf12817deb43288712231",
        2: "1836e76b12d79c55118a1139d2417df52a2021225ff6350063d88e5f1f91631c",
        40: "e449a03eab359e34095f8b4b55cd7ac7c0ec6510f2c4cc79fa6b1fee6b18c59e",
        41: "73bd6978c59f2b219449b36770fb313fbe2da28f6b04275f071a1b193dde2072",
    }
    assert len(CONSTANTS) == 42
    for r, hexval in want.items():
        assert CONSTANTS[r] == int(hexval, 16)


def _gf16_mul(a: int, b: int) -> int:
    r = 0
    for _ in range(4):
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 0b10011  # x^4 + x + 1
    return r


def test_linear_is_the_mds_map_of_section_4_2() -> None:
    # (C, D) = (5 A + 2 B, 2 A + B) in GF(2^4); also check that L is a bijection on pairs.
    seen = set()
    for a in range(16):
        for b in range(16):
            c, d = linear(a, b)
            assert c == _gf16_mul(5, a) ^ _gf16_mul(2, b)
            assert d == _gf16_mul(2, a) ^ b
            seen.add((c, d))
    assert len(seen) == 256


def test_permutation_p8_is_a_bijection() -> None:
    out = permute(list(range(256)))
    assert sorted(out) == list(range(256))
    # pi_8 gives 0, 1, 3, 2, 4, 5, 7, 6, ...; P'_8 keeps the even places first; phi_8 fixes the first half.
    assert out[:4] == [0, 3, 4, 7]
    assert out[128:132] == [2, 1, 6, 5]  # P'_8 puts 1, 2, 5, 6 here and phi_8 swaps the pairs


def test_padding_lengths() -> None:
    # Section 6.1 always adds at least 512 bits, so "abc" needs two blocks.
    assert len(pad(b"")) == 64 and pad(b"")[0] == 0x80
    p = pad(b"abc")
    assert len(p) == 128 and p[3] == 0x80 and p[-16:] == (24).to_bytes(16, "big")
    p = pad(bytes(64))  # a full block still gets a whole block of padding
    assert len(p) == 128 and p[64] == 0x80 and p[-16:] == (512).to_bytes(16, "big")


def test_digest_sizes_have_different_ivs() -> None:
    # The IV holds n, so JH-224 is not the last 224 bits of JH-256.
    assert len(jh(b"abc", 224)) == 28 and len(jh(b"abc", 384)) == 48
    assert jh(b"abc", 224) != jh(b"abc", 256)[-28:]


def test_compression_feed_forward() -> None:
    # F_8 xors the message into the first half before E_8 and into the second half after.
    rng = random.Random(4)
    h = rng.getrandbits(1024)
    assert compress(h, 1) != compress(h, 0)
    assert compress(h, 0) != compress(h ^ 1, 0)


def test_avalanche() -> None:
    rng = random.Random(9)
    total, trials = 0, 8
    for _ in range(trials):
        m = bytearray(rng.randbytes(20))
        a = int.from_bytes(jh256(bytes(m)), "big")
        bit = rng.randrange(160)
        m[bit // 8] ^= 1 << (bit % 8)
        total += bin(a ^ int.from_bytes(jh256(bytes(m)), "big")).count("1")
    assert 108 <= total / trials <= 148


def test_bad_size() -> None:
    with pytest.raises(ValueError):
        jh(b"", 160)
