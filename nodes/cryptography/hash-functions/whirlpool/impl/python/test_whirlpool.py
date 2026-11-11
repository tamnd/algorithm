# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whirlpool/. The authors are listed in prov/C0V92H.jsonl.

from whirlpool import S, gmul, pad, whirlpool

# The ISO/IEC 10118-3 test vectors for Whirlpool ("" up to the 32-byte "abcdbcde...ijk"), as
# reproduced in Botan, src/tests/data/hash/whirlpool.vec, section [Whirlpool], first 8 entries.
# The reference distribution of the designers (whirlpool.zip, iso-test-vectors.txt) could not be fetched.
ISO = [
    (b"", "19FA61D75522A4669B44E39C1D2E1726C530232130D407F89AFEE0964997F7A7"
          "3E83BE698B288FEBCF88E3E03C4F0757EA8964E59B63D93708B138CC42A66EB3"),
    (b"a", "8ACA2602792AEC6F11A67206531FB7D7F0DFF59413145E6973C45001D0087B42"
           "D11BC645413AEFF63A42391A39145A591A92200D560195E53B478584FDAE231A"),
    (b"abc", "4E2448A4C6F486BB16B6562C73B4020BF3043E3A731BCE721AE1B303D97E6D4C"
             "7181EEBDB6C57E277D0E34957114CBD6C797FC9D95D8B582D225292076D4EEF5"),
    (b"message digest", "378C84A4126E2DC6E56DCC7458377AAC838D00032230F53CE1F5700C0FFB4D3B"
                        "8421557659EF55C106B4B52AC5A4AAA692ED920052838F3362E86DBD37A8903E"),
    (b"abcdefghijklmnopqrstuvwxyz",
     "F1D754662636FFE92C82EBB9212A484A8D38631EAD4238F5442EE13B8054E41B"
     "08BF2A9251C30B6A0B8AAE86177AB4A6F68F673E7207865D5D9819A3DBA4EB3B"),
    (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
     "DC37E008CF9EE69BF11F00ED9ABA26901DD7C28CDEC066CC6AF42E40F82F3A1E"
     "08EBA26629129D8FB7CB57211B9281A65517CC879D7B962142C65F5A7AF01467"),
    (b"1234567890" * 8,
     "466EF18BABB0154D25B9D38A6414F5C08784372BCCB204D6549C4AFADB601429"
     "4D5BD8DF2A6C44E538CD047B2681A51A2C60481E88C5A20B2C2A80CF3A9A083B"),
    (b"abcdbcdecdefdefgefghfghighijhijk",
     "2A987EA40F917061F5D6F0A0E4644F488A7A5A52DEEE656207C562F988E95C69"
     "16BDC8031BC5BE1B7B947639FE050B56939BAAA0ADFF9AE6745B7B181C3BE3FD"),
]


def test_iso_vectors() -> None:
    for msg, want in ISO:
        assert whirlpool(msg).hex().upper() == want, msg


def test_sbox() -> None:
    # The first row of the S-box table in the specification: 18 23 c6 e8 87 b8 01 4f.
    assert S[:8] == [0x18, 0x23, 0xC6, 0xE8, 0x87, 0xB8, 0x01, 0x4F]
    assert sorted(S) == list(range(256))


def test_field() -> None:
    assert gmul(0x80, 0x02) == 0x1D  # x^8 = x^4 + x^3 + x^2 + 1
    for a in range(1, 256, 17):
        assert any(gmul(a, b) == 1 for b in range(1, 256))


def test_padding() -> None:
    for n in (0, 31, 32, 33, 63, 64):
        p = pad(b"q" * n)
        assert len(p) % 64 == 0 and p[n] == 0x80
        assert int.from_bytes(p[-32:], "big") == 8 * n
    assert len(pad(b"q" * 31)) == 64 and len(pad(b"q" * 32)) == 128
