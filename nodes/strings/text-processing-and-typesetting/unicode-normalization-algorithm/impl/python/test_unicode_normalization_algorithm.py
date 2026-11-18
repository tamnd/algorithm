# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-normalization-algorithm/. The authors are listed in prov/ZG8A1R.jsonl.

# Oracle: unicodedata.normalize. Written against Python 3.14, unicodedata.unidata_version
# 16.0.0. Random tests use only characters assigned in Unicode 3.2, whose decompositions and
# ccc values the stability policy fixes.

import random
import unicodedata

from unicode_normalization_algorithm import (
    COMPOSITION_EXCLUSIONS, PRIMARY, canonical_order, canonically_equivalent, ccc, full_composition_exclusions,
    mapping, normalize)

FORMS = ("NFC", "NFD", "NFKC", "NFKD")

# NormalizationTest-16.0.0.txt (Date: 2024-04-30, 21:48:23 GMT),
# https://www.unicode.org/Public/16.0.0/ucd/NormalizationTest.txt. The fields c1;c2;c3;c4;c5;
# of the first 25 data lines after "@Part0 # Specific cases" and the first 10 after
# "@Part1 # Character by character test", without the comments.
PART0 = """\
1E0A;1E0A;0044 0307;1E0A;0044 0307;
1E0C;1E0C;0044 0323;1E0C;0044 0323;
1E0A 0323;1E0C 0307;0044 0323 0307;1E0C 0307;0044 0323 0307;
1E0C 0307;1E0C 0307;0044 0323 0307;1E0C 0307;0044 0323 0307;
0044 0307 0323;1E0C 0307;0044 0323 0307;1E0C 0307;0044 0323 0307;
0044 0323 0307;1E0C 0307;0044 0323 0307;1E0C 0307;0044 0323 0307;
1E0A 031B;1E0A 031B;0044 031B 0307;1E0A 031B;0044 031B 0307;
1E0C 031B;1E0C 031B;0044 031B 0323;1E0C 031B;0044 031B 0323;
1E0A 031B 0323;1E0C 031B 0307;0044 031B 0323 0307;1E0C 031B 0307;0044 031B 0323 0307;
1E0C 031B 0307;1E0C 031B 0307;0044 031B 0323 0307;1E0C 031B 0307;0044 031B 0323 0307;
0044 031B 0307 0323;1E0C 031B 0307;0044 031B 0323 0307;1E0C 031B 0307;0044 031B 0323 0307;
0044 031B 0323 0307;1E0C 031B 0307;0044 031B 0323 0307;1E0C 031B 0307;0044 031B 0323 0307;
00C8;00C8;0045 0300;00C8;0045 0300;
0112;0112;0045 0304;0112;0045 0304;
0045 0300;00C8;0045 0300;00C8;0045 0300;
0045 0304;0112;0045 0304;0112;0045 0304;
1E14;1E14;0045 0304 0300;1E14;0045 0304 0300;
0112 0300;1E14;0045 0304 0300;1E14;0045 0304 0300;
1E14 0304;1E14 0304;0045 0304 0300 0304;1E14 0304;0045 0304 0300 0304;
0045 0304 0300;1E14;0045 0304 0300;1E14;0045 0304 0300;
0045 0300 0304;00C8 0304;0045 0300 0304;00C8 0304;0045 0300 0304;
05B8 05B9 05B1 0591 05C3 05B0 05AC 059F;05B1 05B8 05B9 0591 05C3 05B0 05AC 059F;05B1 05B8 05B9 0591 05C3 05B0 05AC 059F;05B1 05B8 05B9 0591 05C3 05B0 05AC 059F;05B1 05B8 05B9 0591 05C3 05B0 05AC 059F;
0592 05B7 05BC 05A5 05B0 05C0 05C4 05AD;05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4;05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4;05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4;05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4;
1100 AC00 11A8;1100 AC01;1100 1100 1161 11A8;1100 AC01;1100 1100 1161 11A8;
1100 AC00 11A8 11A8;1100 AC01 11A8;1100 1100 1161 11A8 11A8;1100 AC01 11A8;1100 1100 1161 11A8 11A8;
"""
PART1 = """\
00A0;00A0;00A0;0020;0020;
00A8;00A8;00A8;0020 0308;0020 0308;
00AA;00AA;00AA;0061;0061;
00AF;00AF;00AF;0020 0304;0020 0304;
00B2;00B2;00B2;0032;0032;
00B3;00B3;00B3;0033;0033;
00B4;00B4;00B4;0020 0301;0020 0301;
00B5;00B5;00B5;03BC;03BC;
00B8;00B8;00B8;0020 0327;0020 0327;
00B9;00B9;00B9;0031;0031;
"""


def parse(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        fields = line.split("#", 1)[0].split(";")[:5]
        rows.append(["".join(chr(int(x, 16)) for x in f.split()) for f in fields])
    return rows


def hexs(s: str) -> str:
    return " ".join("%04X" % ord(ch) for ch in s)


def test_conformance_lines() -> None:
    # The invariants of the header of NormalizationTest.txt (conformance clause UAX15-C3).
    rows = parse(PART0) + parse(PART1)
    assert len(rows) == 35
    nfc = lambda s: normalize("NFC", s)  # noqa: E731
    nfd = lambda s: normalize("NFD", s)  # noqa: E731
    nfkc = lambda s: normalize("NFKC", s)  # noqa: E731
    nfkd = lambda s: normalize("NFKD", s)  # noqa: E731
    for c1, c2, c3, c4, c5 in rows:
        assert c2 == nfc(c1) == nfc(c2) == nfc(c3)
        assert c4 == nfc(c4) == nfc(c5)
        assert c3 == nfd(c1) == nfd(c2) == nfd(c3)
        assert c5 == nfd(c4) == nfd(c5)
        assert c4 == nfkc(c1) == nfkc(c2) == nfkc(c3) == nfkc(c4) == nfkc(c5)
        assert c5 == nfkd(c1) == nfkd(c2) == nfkd(c3) == nfkd(c4) == nfkd(c5)


def test_check_values() -> None:
    cases = {
        "ḍ̇": ("1E0D 0307", "0064 0323 0307", "1E0D 0307", "0064 0323 0307"),
        "Å": ("00C5", "0041 030A", "00C5", "0041 030A"),
        "ﬁ": ("FB01", "FB01", "0066 0069", "0066 0069"),
        "Å": ("00C5", "0041 030A", "00C5", "0041 030A"),
        "ẛ̣": ("1E9B 0323", "017F 0323 0307", "1E69", "0073 0323 0307"),
    }
    for s, want in cases.items():
        assert tuple(hexs(normalize(f, s)) for f in FORMS) == want
    assert [ccc(c) for c in (0x0323, 0x0307, 0x0301, 0x031B)] == [220, 230, 230, 216]


def test_starters_never_move_and_order_is_stable() -> None:
    d = [0x0061, 0x0301, 0x0323, 0x0062, 0x0308, 0x0301, 0x0327]
    canonical_order(d)
    assert d == [0x0061, 0x0323, 0x0301, 0x0062, 0x0327, 0x0308, 0x0301]


def test_not_closed_under_concatenation() -> None:
    x, y = "a", "́"
    assert normalize("NFC", x) == x and normalize("NFC", y) == y
    assert normalize("NFC", x + y) == "á" != x + y


def test_exclusion_table() -> None:
    assert len(COMPOSITION_EXCLUSIONS) == 81
    for c in COMPOSITION_EXCLUSIONS:
        m = mapping(c, False)
        assert m is not None and len(m) == 2
        assert unicodedata.normalize("NFC", "".join(map(chr, m))) != chr(c)
        assert c not in PRIMARY.values()
    full = full_composition_exclusions()
    singletons = [c for c in full if (m := mapping(c, False)) is not None and len(m) == 1]
    assert len(singletons) == 1035
    assert sorted(full - COMPOSITION_EXCLUSIONS - set(singletons)) == [0x0344, 0x0F73, 0x0F75, 0x0F81]


def pool_3_2() -> list[str]:
    rng = random.Random(7)
    marks = [chr(c) for c in range(0x0300, 0x0370) if unicodedata.ucd_3_2_0.category(chr(c)) == "Mn"]
    decomposable = [chr(c) for c in range(0x00A0, 0x3400) if unicodedata.ucd_3_2_0.category(chr(c)) != "Cn"
                    and unicodedata.decomposition(chr(c))]
    hangul = [chr(c) for c in list(range(0x1100, 0x1113)) + list(range(0x1161, 0x1176)) + list(range(0x11A8, 0x11C3))]
    hangul += [chr(rng.randrange(0xAC00, 0xD7A4)) for _ in range(30)]
    plain = list("aeiouACEOUnsdk ")
    return plain + marks + rng.sample(decomposable, 400) + hangul + [chr(c) for c in COMPOSITION_EXCLUSIONS]


def test_random_strings_against_unicodedata() -> None:
    pool = pool_3_2()
    assert all(unicodedata.ucd_3_2_0.category(ch) != "Cn" for ch in pool)
    rng = random.Random(8)
    for _ in range(3000):
        s = "".join(rng.choice(pool) for _ in range(rng.randrange(1, 9)))
        for f in FORMS:
            assert normalize(f, s) == unicodedata.normalize(f, s), (f, hexs(s))


def test_each_decomposable_3_2_character() -> None:
    for c in range(0x00A0, 0x10000):
        ch = chr(c)
        if unicodedata.ucd_3_2_0.category(ch) == "Cn" or not unicodedata.decomposition(ch):
            continue
        for f in FORMS:
            assert normalize(f, ch) == unicodedata.normalize(f, ch), (f, "%04X" % c)


def test_canonical_equivalence() -> None:
    assert canonically_equivalent("Å", "Å")
    assert canonically_equivalent("q̣̇", "q̣̇")
    assert not canonically_equivalent("ﬁ", "fi")
