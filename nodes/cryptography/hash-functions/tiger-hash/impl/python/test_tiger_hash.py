# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tiger-hash/. The authors are listed in prov/6RCPBE.jsonl.

from tiger_hash import TABLE, pad, tiger, tiger2

S64 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-"

# R. Anderson and E. Biham, Tiger home page, https://www.cs.technion.ac.il/~biham/Reports/Tiger/,
# "Test results" (testresults.html), copied by hand. The page prints the three 64-bit words of
# the result as integers; the digest bytes are each word in little-endian order.
TIGER_PAGE = [
    (b"", "24F0130C63AC9332 16166E76B1BB925F F373DE2D49584E7A"),
    (b"abc", "F258C1E88414AB2A 527AB541FFC5B8BF 935F7B951C132951"),
    (b"Tiger", "9F00F599072300DD 276ABB38C8EB6DEC 37790C116F9D2BDF"),
    (S64, "87FB2A9083851CF7 470D2CF810E6DF9E B586445034A5A386"),
    (b"ABCDEFGHIJKLMNOPQRSTUVWXYZ=abcdefghijklmnopqrstuvwxyz+0123456789",
     "467DB80863EBCE48 8DF1CD1261655DE9 57896565975F9197"),
    (b"Tiger - A Fast New Hash Function, by Ross Anderson and Eli Biham",
     "0C410A042968868A 1671DA5A3FD29A72 5EC1E457D3CDB303"),
    (b"Tiger - A Fast New Hash Function, by Ross Anderson and Eli Biham, "
     b"proceedings of Fast Software Encryption 3, Cambridge.",
     "EBF591D5AFA655CE 7F22894FF87F54AC 89C811B6B0DA3193"),
    (b"Tiger - A Fast New Hash Function, by Ross Anderson and Eli Biham, "
     b"proceedings of Fast Software Encryption 3, Cambridge, 1996.",
     "3D9AEB03D1BD1A63 57B2774DFD6D5B24 DD68151D503974FC"),
    (S64 * 2, "00B83EB4E53440C5 76AC6AAEE0A74858 25FD15E70A59FFE4"),
]


def words_to_bytes(s: str) -> bytes:
    return b"".join(int(w, 16).to_bytes(8, "little") for w in s.split())


def test_tiger_page_vectors() -> None:
    for msg, want in TIGER_PAGE:
        assert tiger(msg) == words_to_bytes(want), msg


def test_empty_digest_bytes() -> None:
    assert tiger(b"").hex() == "3293ac630c13f0245f92bbb1766e16167a4e58492dde73f3"


def test_generated_sboxes() -> None:
    # Words of t1 and t4 as printed in the S-box listing of the reference code.
    assert TABLE[0] == 0x02AAB17CF7E90C5E
    assert TABLE[1] == 0xAC424B03E243A8EC
    assert TABLE[1023] == 0xC3A0396F7363A51F


def test_tiger2_differs_only_in_padding() -> None:
    assert pad(b"abc", 0x01)[3] == 0x01 and pad(b"abc", 0x80)[3] == 0x80
    assert pad(b"abc", 0x01)[4:] == pad(b"abc", 0x80)[4:]
    assert tiger2(b"abc") != tiger(b"abc")
    # A message whose last byte equals the padding is not a problem: the length field differs.
    assert tiger(b"") != tiger(b"\x01")
