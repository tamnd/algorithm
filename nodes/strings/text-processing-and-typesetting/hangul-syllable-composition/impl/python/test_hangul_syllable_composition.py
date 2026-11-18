# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hangul-syllable-composition/. The authors are listed in prov/QKVWX9.jsonl.

# Oracles: unicodedata.normalize and unicodedata.name. Written against Python 3.14 with
# unicodedata.unidata_version 16.0.0. The 11172 syllables and the modern jamo are in
# Unicode 2.0 and later, so they are assigned in 3.2, and the stability policy fixes their
# decompositions.

import random
import unicodedata

from hangul_syllable_composition import (
    JAMO_SHORT_NAME, NCOUNT, SBASE, SCOUNT, TBASE, compose, decompose, decompose_syllable,
    decomposition_mapping, syllable_name)


def cps(s: str) -> list[int]:
    return [ord(ch) for ch in s]


def text(c: list[int]) -> str:
    return "".join(map(chr, c))


def test_constants_and_check_values() -> None:
    assert NCOUNT == 588 and SCOUNT == 11172
    assert decompose_syllable(0xD55C) == (0x1112, 0x1161, 0x11AB)
    assert syllable_name(0xD55C) == "HANGUL SYLLABLE HAN"
    assert decompose_syllable(0xAC01) == (0x1100, 0x1161, 0x11A8)
    assert decompose_syllable(0xAC00) == (0x1100, 0x1161)
    assert decomposition_mapping(0xAC01) == (0xAC00, 0x11A8)
    assert len(JAMO_SHORT_NAME) == 67


def test_every_syllable() -> None:
    for s in range(SBASE, SBASE + SCOUNT):
        jamo = list(decompose_syllable(s))
        assert compose(jamo) == [s]
        assert jamo == cps(unicodedata.normalize("NFD", chr(s)))
        assert syllable_name(s) == unicodedata.name(chr(s))
        first, second = decomposition_mapping(s)
        if first >= SBASE:  # LVT maps to LV and T; the LV part decomposes again
            assert list(decomposition_mapping(first)) + [second] == jamo
        else:
            assert [first, second] == jamo


def test_all_syllables_are_in_unicode_3_2() -> None:
    assert all(unicodedata.ucd_3_2_0.category(chr(s)) == "Lo" for s in range(SBASE, SBASE + SCOUNT, 97))


def test_random_text_against_nfc_and_nfd() -> None:
    rng = random.Random(1)
    pool = (list(range(0x1100, 0x1113)) + list(range(0x1161, 0x1176)) + list(range(0x11A8, 0x11C3))
            + [0x41, 0x20, SBASE, SBASE + 1, 0xD55C, 0xB2E4])
    for _ in range(4000):
        s = text([rng.choice(pool) for _ in range(rng.randrange(1, 10))])
        assert text(compose(cps(s))) == unicodedata.normalize("NFC", s)
        assert text(decompose(cps(s))) == unicodedata.normalize("NFD", s)


def test_no_composition_cases() -> None:
    # An LVT syllable takes no second trailing consonant, V T without L stays apart, and
    # TBASE (U+11A7) is not a trailing consonant.
    assert compose([0xAC01, 0x11A8]) == [0xAC01, 0x11A8]
    assert compose([0x1161, 0x11A8]) == [0x1161, 0x11A8]
    assert compose([SBASE, TBASE]) == [SBASE, TBASE]
    assert compose([0x1100, 0x1100, 0x1161, 0x11A8]) == [0x1100, 0xAC01]
