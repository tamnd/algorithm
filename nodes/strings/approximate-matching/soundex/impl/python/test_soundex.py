# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soundex/. The authors are listed in prov/8WZ6WZ.jsonl.

import random

import pytest
from soundex import code, soundex


def rules(name: str) -> str:
    """The four rules of the definition, applied one after the other."""
    s = [c for c in name.upper() if "A" <= c <= "Z"]
    keep = []
    for i in range(1, len(s)):
        if s[i] in "AEIOUYHW":
            continue
        j = i - 1
        while j > 0 and s[j] in "HW":
            j -= 1
        if code(s[j]) == code(s[i]):
            continue
        keep.append(code(s[i]))
    return (s[0] + "".join(keep) + "000")[:4]


def test_examples() -> None:
    table = {
        "Robert": "R163", "Rupert": "R163", "Rubin": "R150", "Ashcraft": "A261",
        "Ashcroft": "A261", "Tymczak": "T522", "Pfister": "P236", "Honeyman": "H555",
        "Lee": "L000", "Euler": "E460", "Ellery": "E460", "Gauss": "G200", "Ghosh": "G200",
        "Hilbert": "H416", "Heilbronn": "H416", "Knuth": "K530", "Kant": "K530",
        "Lloyd": "L300", "Ladd": "L300", "Lukasiewicz": "L222", "Lissajous": "L222",
    }
    for name, want in table.items():
        assert soundex(name) == want
        assert rules(name) == want


def test_edges() -> None:
    assert soundex("a") == "A000"
    assert soundex("o'Hara") == "O600"
    assert soundex("  van Dyke ") == soundex("VANDYKE")
    with pytest.raises(ValueError):
        soundex("")
    with pytest.raises(ValueError):
        soundex("123 -")


def test_random_against_rules() -> None:
    rng = random.Random(1918)
    for letters in ("BH", "AEBP", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "HWSCAZ"):
        for _ in range(600):
            name = "".join(rng.choice(letters) for _ in range(rng.randint(1, 12)))
            got = soundex(name)
            assert got == rules(name)
            assert len(got) == 4 and got[0] == name[0] and got[1:].isdigit()
