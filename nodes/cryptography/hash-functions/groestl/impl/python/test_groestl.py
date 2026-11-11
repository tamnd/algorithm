# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/groestl/. The authors are listed in prov/AE3QKK.jsonl.

import random

import pytest

from groestl import SBOX, compress, groestl, groestl256, groestl512, pad, permutation

# Final-round submission package Groestl.zip (January 2011), files KAT_MCT/ShortMsgKAT_256.txt
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
    ("", "1A52D11D550039BE16107F9C58DB9EBCC417F16F736ADB2502567119F0083467"),
    ("CC", "15E2671F0EAF66C0DE3093AB7B1E39DC68F945D7002FC5DFD52D60527E7228D1"),
    ("41FB", "846F1C22FC62B770DE1782EF33414AA5BAA44B690EBFB7D1BDCCA8D2AC59C929"),
    (MSG512, "5ADEBBFDF6FD6178892B39A97A32B29FB605F97E1E5C3BBCF624A0E9CD72D145"),
    (MSG1024, "B8A871928FCC39AB286E5A768B0AE61DDBD765FBC55C2DD2F3D10477D362A08F"),
]
KAT_512 = [
    ("", "6D3AD29D279110EEF3ADBD66DE2A0345A77BAEDE1557F5D099FCE0C03D6DC2BA"
         "8E6D4A6633DFBD66053C20FAA87D1A11F39A7FBE4A6C2F009801370308FC4AD8"),
    ("CC", "B23EEEB675C272C6E37A6EE9AB4DC505C9D6A10020F6BED3948205D04CDD1E90"
           "B06E494D186EF4F19266D7DA200C89DC009E2B1A538CDEA199E773FC076F802E"),
    (MSG512, "E8EEDDEF7104F8EE0A93C4BE5028DB073B7AC44B73787B3ADCAFDB8AADE084C1"
             "9550EBB1D968E2B26B9F99BA48D5686E1D7658725F6934A845CB5EE475B8B7F0"),
    (MSG1024, "FF410B511135DBC0B8644C28EFA3EC632326FEB98E50EDC6390C441610D7C514"
              "ACDF0A61A0BF01AA9DC1F55D92E085248EBA1C24EE23978B4986AF41C13A6176"),
]


@pytest.mark.parametrize("msg,want", KAT_256)
def test_short_msg_kat_256(msg: str, want: str) -> None:
    assert groestl256(bytes.fromhex(msg)) == bytes.fromhex(want)


@pytest.mark.parametrize("msg,want", KAT_512)
def test_short_msg_kat_512(msg: str, want: str) -> None:
    assert groestl512(bytes.fromhex(msg)) == bytes.fromhex(want)


def test_intermediate_values_abc() -> None:
    # KAT_MCT/IntermediateValues_1BlockMsg_256.txt, input "abc". The file prints the state as a
    # matrix; the bytes below are its columns 0 and 7 after "P(h+m) + Q(m) + h =".
    trace: list[bytes] = []
    digest = groestl(b"abc", 256, trace)
    assert len(trace) == 1
    assert trace[0][0:8] == bytes.fromhex("037699027b7f61a2")
    assert trace[0][56:64] == bytes.fromhex("469e9321ca217d9a")
    assert digest == bytes.fromhex("f3c1bb19c048801326a7efbcf16e3d7887446249829c379e1840d1a3a1e7d4d2")


def test_sbox_matches_appendix_b() -> None:
    # Table 4 of the specification: first row and some other entries.
    assert SBOX[:16] == [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
                         0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76]
    assert SBOX[0x53] == 0xED and SBOX[0xFF] == 0x16 and SBOX[0x80] == 0xCD


def test_padding_is_one_block_count_suffix() -> None:
    p = pad(b"abc", 64)
    assert len(p) == 64 and p[3] == 0x80 and p[-8:] == (1).to_bytes(8, "big")
    p = pad(bytes(56), 64)  # 448 + 65 > 512: needs a second block
    assert len(p) == 128 and p[-8:] == (2).to_bytes(8, "big")


def test_p_and_q_are_different_permutations() -> None:
    rng = random.Random(2)
    s = list(rng.randbytes(64))
    assert permutation("P", s) != permutation("Q", s)
    outs = {bytes(permutation("P", list(rng.randbytes(64)))) for _ in range(30)}
    assert len(outs) == 30


def test_truncation_is_not_a_prefix_of_a_longer_digest() -> None:
    # The IV holds n, so Groestl-224 is not Groestl-256 cut short.
    assert groestl(b"abc", 224) != groestl(b"abc", 256)[-28:]
    assert groestl(b"abc", 224) != groestl(b"abc", 256)[:28]


def test_compression_feed_forward() -> None:
    # f(h, m) = P(h xor m) xor Q(m) xor h: changing h with m fixed changes the output.
    h, m = bytes(64), bytes(range(64))
    assert compress(h, m) != compress(b"\x01" + bytes(63), m)


def test_avalanche() -> None:
    rng = random.Random(9)
    total, trials = 0, 12
    for _ in range(trials):
        m = bytearray(rng.randbytes(20))
        a = int.from_bytes(groestl256(bytes(m)), "big")
        bit = rng.randrange(160)
        m[bit // 8] ^= 1 << (bit % 8)
        total += bin(a ^ int.from_bytes(groestl256(bytes(m)), "big")).count("1")
    assert 112 <= total / trials <= 144


def test_bad_size() -> None:
    with pytest.raises(ValueError):
        groestl(b"", 12)
