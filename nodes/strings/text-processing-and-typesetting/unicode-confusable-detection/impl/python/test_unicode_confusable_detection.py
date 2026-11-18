# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-confusable-detection/. The authors are listed in prov/N2QXMJ.jsonl.
# NFD and the bidi classes come from unicodedata (unidata_version 16.0.0 with Python 3.14).
# The tests use only characters that are assigned in Unicode 3.2.
import random

import pytest

from unicode_confusable_detection import (PROTOTYPES, classify, confusable, internal_skeleton,
                                          is_default_ignorable, parse_confusables,
                                          resolved_script_set, skeleton)


def test_parse_confusables_line():
    t = parse_confusables("0430 ;\t0061 ;\tMA\t# ( а → a ) CYRILLIC SMALL LETTER A → LATIN SMALL LETTER A\t# \n")
    assert t == {"а": "a"}
    assert PROTOTYPES["m"] == "rn"
    assert PROTOTYPES["1"] == "l" and PROTOTYPES["I"] == "l" and PROTOTYPES["|"] == "l"
    assert PROTOTYPES["0"] == "O" and PROTOTYPES["о"] == "o"


def test_four_steps_of_internal_skeleton():
    # Step 1, NFD: U+00E9 and U+0065 U+0301 give the same skeleton.
    assert internal_skeleton("é") == internal_skeleton("é") == "é"
    # Step 2: default ignorable code points are removed.
    assert internal_skeleton("pay­pal") == internal_skeleton("pay​pal") == "paypal"
    # Step 3: the prototypes. U+0430 CYRILLIC SMALL LETTER A becomes U+0061.
    assert internal_skeleton("pаypаl") == "paypal"
    assert internal_skeleton("m") == "rn"
    # Step 4: NFD again. U+0131 DOTLESS I becomes i, and i + U+0307 stays decomposed.
    assert internal_skeleton("ı̇") == "i̇"
    assert internal_skeleton("ı̇") == internal_skeleton("i̇")


def test_confusable_pairs():
    must = [("paypal", "pаypаl"), ("paypal", "paypa1"), ("paypal", "paypaI"), ("rn", "m"),
            ("сор", "cop"), ("Ο0", "OO"), ("a-b", "a‐b"), ("pay​pal", "paypal"),
            ("é", "é")]
    for x, y in must:
        assert confusable(x, y), (x, y)
    must_not = [("paypal", "paypai"), ("cat", "cot"), ("e", "é"), ("rm", "rn"), ("O", "o"),
                ("a b", "ab")]
    for x, y in must_not:
        assert not confusable(x, y), (x, y)


def test_classes_of_confusables():
    assert classify("rn", "m") == "single-script"
    assert classify("paypa1", "paypal") == "single-script"  # U+0031 is Common
    assert classify("сор", "cop") == "whole-script"  # Cyrillic and Latin
    assert classify("pаypаl", "paypal") == "mixed-script"  # the first string mixes scripts
    assert classify("cat", "dog") is None


def test_resolved_script_sets():
    assert resolved_script_set("abc") == frozenset({"Latin"})
    assert resolved_script_set("123") is None  # Common only: all scripts
    assert resolved_script_set("a1") == frozenset({"Latin"})
    assert resolved_script_set("pаypаl") == frozenset()
    assert resolved_script_set("сор") == frozenset({"Cyrillic"})


def test_skeleton_rejects_text_that_needs_bidi_reordering():
    for x in ["אb", "aا", "1١", "a‮b", "a‏b", "a\u0001"]:
        with pytest.raises(ValueError):
            skeleton(x)
    assert internal_skeleton("a‏b") == "ab"


def test_skeleton_is_idempotent_and_ignores_dicp():
    rng = random.Random(39)
    alphabet = "aceilmnoprxy01I|-`" + "аеорсху" + "ΑΟ" + "é"
    ignorables = ["­", "​", "⁠", "﻿", "͏"]
    for _ in range(400):
        x = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
        s = skeleton(x)
        assert skeleton(s) == s
        y = list(x)
        for _ in range(rng.randint(0, 3)):
            y.insert(rng.randint(0, len(y)), rng.choice(ignorables))
        assert skeleton("".join(y)) == s
        assert not any(is_default_ignorable(c) for c in s)


def _reference_skeleton(x):
    """A second implementation of the four steps, from the raw lines and code point lists."""
    import unicodedata
    ignorable = set(range(0x200B, 0x2010)) | {0x00AD, 0x034F, 0x2060, 0x2061, 0x2062, 0x2063,
                                              0x2064, 0xFEFF} | set(range(0xFE00, 0xFE10))
    x = [c for c in unicodedata.normalize("NFD", x) if ord(c) not in ignorable]
    out = []
    for c in x:
        out.append(PROTOTYPES[c] if c in PROTOTYPES else c)
    return unicodedata.normalize("NFD", "".join(out))


def test_against_reference_on_random_strings():
    rng = random.Random(2024)
    alphabet = "abcdeilmnorIO01|" + "аеіјорсху" + "ΑΒΟοι" + "­​﻿́" + "ñåé"
    for _ in range(400):
        x = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 10)))
        assert internal_skeleton(x) == _reference_skeleton(x)


def test_confusable_is_an_equivalence():
    rng = random.Random(7)
    alphabet = "aolI1m" + "ао" + "rn"
    words = ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 3))) for _ in range(60)]
    for x in words:
        assert confusable(x, x)
        for y in words:
            assert confusable(x, y) == confusable(y, x)
            if confusable(x, y):
                for z in words:
                    if confusable(y, z):
                        assert confusable(x, z)
