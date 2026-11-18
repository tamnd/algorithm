# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-case-folding/. The authors are listed in prov/GS7516.jsonl.

# The oracle is str.casefold, which is full case folding on the Unicode version of
# unicodedata.unidata_version (16.0.0 when these tests were written). The oracle tests use
# only characters assigned in Unicode 3.2, so a newer Python cannot change the result.

import random
import unicodedata

from unicode_case_folding import (
    CASE_FOLDING,
    canonical_caseless_key,
    canonical_caseless_match,
    default_caseless_match,
    to_casefold,
)


def in_3_2(c: str) -> bool:
    return unicodedata.ucd_3_2_0.category(c) != "Cn"


def test_check_values():
    assert to_casefold("ß") == "ss"
    assert to_casefold("ẞ") == "ss"
    assert to_casefold("ﬃ") == "ffi"
    assert to_casefold("İ") == "i̇"
    assert to_casefold("ς") == "σ"
    assert to_casefold("Ǆ") == "ǆ"
    assert to_casefold("ǅ") == "ǆ"


def test_against_str_casefold_on_table():
    checked = 0
    for c in CASE_FOLDING:
        if in_3_2(c):
            assert to_casefold(c) == c.casefold(), hex(ord(c))
            checked += 1
    assert checked >= 50


def test_random_strings_against_str_casefold():
    rng = random.Random(20240910)
    pool = [c for c in CASE_FOLDING if in_3_2(c)] + list("abcxyz éά")
    for _ in range(500):
        s = "".join(rng.choice(pool) for _ in range(rng.randint(0, 12)))
        assert to_casefold(s) == s.casefold()


def test_simple_folding_keeps_length():
    assert to_casefold("ẞ", full=False) == "ß"
    assert to_casefold("ß", full=False) == "ß"
    assert to_casefold("ᾼ", full=False) == "ᾳ"
    assert to_casefold("ﬅ", full=False) == "ﬆ"
    rng = random.Random(7)
    pool = list(CASE_FOLDING) + list("abc")
    for _ in range(300):
        s = "".join(rng.choice(pool) for _ in range(rng.randint(0, 10)))
        assert len(to_casefold(s, full=False)) == len(s)


def test_full_folding_changes_length():
    assert len("ΐ") == 1 and len(to_casefold("ΐ")) == 3
    assert to_casefold("Straße") == "strasse"


def test_turkic_option():
    assert to_casefold("I") == "i"
    assert to_casefold("I", turkic=True) == "ı"
    assert to_casefold("İ", turkic=True) == "i"
    assert not default_caseless_match("I", "ı")
    assert default_caseless_match("I", "ı", turkic=True)


def test_idempotent():
    for c in CASE_FOLDING:
        for full in (True, False):
            f = to_casefold(c, full=full)
            assert to_casefold(f, full=full) == f


def test_sign_characters():
    assert to_casefold("K") == "k"
    assert to_casefold("Ω") == "ω"
    assert to_casefold("Å") == "å"
    assert to_casefold("µ") == "μ"


def test_default_match_misses_decomposed_forms():
    assert not default_caseless_match("Å", "Å")
    assert canonical_caseless_match("Å", "Å")
    assert canonical_caseless_match("Å", "å")


def test_ypogegrammeni_needs_nfd_first():
    x = "ᾴ"
    y = "ᾴ"
    assert unicodedata.normalize("NFD", x) == unicodedata.normalize("NFD", y)
    folded_then_nfd_x = unicodedata.normalize("NFD", to_casefold(x))
    folded_then_nfd_y = unicodedata.normalize("NFD", to_casefold(y))
    assert folded_then_nfd_x != folded_then_nfd_y
    assert canonical_caseless_key(x) == "άι"
    assert canonical_caseless_match(x, y)


def test_folding_does_not_preserve_nfc():
    s = "ΐ"
    assert unicodedata.normalize("NFC", s) == s
    f = to_casefold(s)
    assert f == "ΐ"
    assert unicodedata.normalize("NFC", f) != f
