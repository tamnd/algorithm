# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enigma-machine/. The authors are listed in prov/4QX9ZT.jsonl.

import itertools
import random
from collections import Counter

import pytest

from enigma_machine import (
    ALPHABET,
    REFLECTORS,
    ROTORS,
    Enigma,
    characteristic,
    crib_positions,
    key_count,
    plugboard_map,
    plugboard_settings,
    positions,
)

# No official test vectors exist for the Enigma. The two vectors below are
# widely published and are used to check simulators.
# 1. Wikipedia, "Enigma rotor details": rotors I, II, III, reflector B,
#    rings AAA, start AAA, no plugs; AAAAA encrypts to BDZGO.
# 2. The example of the 1930 German instruction manual for the Enigma
#    (rotors II, I, III, reflector A, rings XMV, start ABL, plugs AM FI NV
#    PS TU WZ), as reproduced on simulator and museum sites.
MANUAL_PLAIN = "FEINDLIQEINFANTERIEKOLONNEBEOBAQTETXANFANGSUEDAUSGANGBAERWALDEXENDEDREIKMOSTWAERTSNEUSTADT"
MANUAL_CIPHER = (
    "GCDSEAHUGWTQGRKVLFGXUCALXVYMIGMMNMFDXTGNVHVRMMEVOUYFZSLRHDRRXFJWCFHUHMUNZEFRDISIKBGPMYVXUZ"
)


def test_published_examples() -> None:
    assert Enigma(("I", "II", "III"), "B", "AAA").encrypt("AAAAA", "AAA") == "BDZGO"
    manual = Enigma(("II", "I", "III"), "A", "XMV", "AM FI NV PS TU WZ")
    assert manual.encrypt(MANUAL_PLAIN, "ABL") == MANUAL_CIPHER
    assert manual.encrypt(MANUAL_CIPHER, "ABL") == MANUAL_PLAIN


def test_wirings() -> None:
    for wiring, notch in ROTORS.values():
        assert sorted(wiring) == list(ALPHABET) and notch in ALPHABET
    for wiring in REFLECTORS.values():
        r = [ord(c) - 65 for c in wiring]
        assert all(r[r[x]] == x and r[x] != x for x in range(26))  # an involution with no fixed point


def test_double_step() -> None:
    # Rotor II turns over at E, rotor III at V. The middle rotor steps at
    # ADU -> ADV -> AEW, and then again at AEW -> BFX, together with the left.
    assert positions("ADU", ("I", "II", "III"), 4) == ["ADV", "AEW", "BFX", "BFY"]
    # Away from the turnover of the middle rotor, it is a plain odometer.
    assert positions("AAU", ("I", "II", "III"), 3) == ["AAV", "ABW", "ABX"]
    # The double step makes the period 26 * 25 * 26 = 16900, not 26^3.
    seq = positions("AAA", ("I", "II", "III"), 17000)
    assert seq.index("AAA") + 1 == 16900


def test_edge_cases() -> None:
    e = Enigma(("I", "II", "III"))
    assert e.encrypt("", "AAA") == ""
    assert e.encrypt("a a!", "AAA") == e.encrypt("AA", "AAA")
    with pytest.raises(ValueError):
        Enigma(("I", "I", "III"))
    with pytest.raises(ValueError):
        plugboard_map("AB AC")


def _rotate(w: list[int], s: int) -> list[int]:
    return [(w[(x + s) % 26] - s) % 26 for x in range(26)]


def _compose(*perms: list[int]) -> list[int]:
    """The permutation that applies perms[0] first, then perms[1], and so on."""
    out = list(range(26))
    for p in perms:
        out = [p[y] for y in out]
    return out


def _inverse(p: list[int]) -> list[int]:
    inv = [0] * 26
    for i, y in enumerate(p):
        inv[y] = i
    return inv


def oracle_encrypt(rotors, reflector, rings, plugs, start, text) -> str:
    """An independent statement: compose the permutations, step by the three pawls."""
    w = [[ord(c) - 65 for c in ROTORS[r][0]] for r in rotors]
    turn = [ord(ROTORS[r][1]) - 65 for r in rotors]
    u = [ord(c) - 65 for c in REFLECTORS[reflector]]
    ring = [ord(c) - 65 for c in rings]
    s = plugboard_map(plugs)
    pos = [ord(c) - 65 for c in start]
    out = []
    for ch in text:
        # Pawl 3 always pushes the right rotor; pawl 2 engages a notch of the
        # right rotor or the notch of the middle rotor itself; pawl 1 engages
        # the notch of the middle rotor.
        moves = [pos[1] == turn[1], pos[2] == turn[2] or pos[1] == turn[1], True]
        pos = [(p + m) % 26 for p, m in zip(pos, moves)]
        r = [_rotate(w[i], pos[i] - ring[i]) for i in range(3)]
        e = _compose(s, r[2], r[1], r[0], u, _inverse(r[0]), _inverse(r[1]), _inverse(r[2]), s)
        out.append(ALPHABET[e[ord(ch) - 65]])
    return "".join(out)


def random_setting(rng: random.Random):
    rotors = tuple(rng.sample(sorted(ROTORS), 3))
    letters = rng.sample(ALPHABET, 20)
    plugs = " ".join(letters[2 * i] + letters[2 * i + 1] for i in range(rng.randrange(11)))
    rings = "".join(rng.choice(ALPHABET) for _ in range(3))
    start = "".join(rng.choice(ALPHABET) for _ in range(3))
    return rotors, rng.choice("AB"), rings, plugs, start


def test_against_oracle_and_involution() -> None:
    rng = random.Random(12)
    for _ in range(500):
        rotors, refl, rings, plugs, start = random_setting(rng)
        text = "".join(rng.choice(ALPHABET) for _ in range(rng.randrange(1, 40)))
        m = Enigma(rotors, refl, rings, plugs)
        c = m.encrypt(text, start)
        assert c == oracle_encrypt(rotors, refl, rings, plugs, start, text)
        assert m.encrypt(c, start) == text  # decryption is encryption
        assert all(a != b for a, b in zip(text, c))  # no letter maps to itself


def test_letter_maps_are_fixed_point_free_involutions() -> None:
    rng = random.Random(13)
    for _ in range(100):
        rotors, refl, rings, plugs, _ = random_setting(rng)
        m = Enigma(rotors, refl, rings, plugs)
        e = m.letter_map([rng.randrange(26) for _ in range(3)])
        assert all(e[e[x]] == x and e[x] != x for x in range(26))


def test_left_ring_is_redundant() -> None:
    rng = random.Random(14)
    text = "".join(rng.choice(ALPHABET) for _ in range(300))
    a = Enigma(("III", "I", "V"), "B", "AKD").encrypt(text, "AQS")
    b = Enigma(("III", "I", "V"), "B", "HKD").encrypt(text, "HQS")
    assert a == b  # shifting the left ring and the left start together changes nothing


def test_key_count() -> None:
    # Small cases of the plugboard formula against an enumeration of matchings.
    for n, c in [(4, 1), (4, 2), (6, 2), (6, 3), (8, 3)]:
        found = set()
        for pairs in itertools.combinations(itertools.combinations(range(n), 2), c):
            flat = [x for p in pairs for x in p]
            if len(set(flat)) == 2 * c:
                found.add(frozenset(pairs))
        assert plugboard_settings(n, c) == len(found)
    k = key_count()
    assert k["rotor orders"] == 60
    assert k["start positions"] == 17576
    assert k["rings"] == 676
    assert k["plugboard"] == 150738274937250
    assert k["total"] == 60 * 17576 * 676 * 150738274937250 == 107458687327250619360000
    assert 60 * 17576 * k["plugboard"] == 158962555217826360000  # without the rings
    assert max(range(14), key=lambda c: plugboard_settings(26, c)) == 11  # 11 cables would give the most


def test_crib_placement() -> None:
    m = Enigma(("II", "V", "I"), "B", "FKQ", "AQ BJ CE DM FT GL HZ IU KR NO")
    plain = "ANXOBERKOMMANDOXWETTERBERICHTXHEUTEKLARXWINDAUSWEST"
    c = m.encrypt(plain, "RTW")
    found = crib_positions(c, "WETTERBERICHT")
    assert plain.index("WETTERBERICHT") == 16 and 16 in found
    assert len(found) == 21 and len(c) - 13 + 1 == 39  # 18 of 39 offsets are ruled out


def test_rejewski_characteristic() -> None:
    rng = random.Random(15)
    for _ in range(50):
        rotors, refl, rings, plugs, start = random_setting(rng)
        with_plugs = characteristic(Enigma(rotors, refl, rings, plugs), start)
        without = characteristic(Enigma(rotors, refl, rings, ""), start)
        assert with_plugs == without  # the plugboard does not change the cycle type
        for lengths in with_plugs:
            assert sum(lengths) == 26
            assert all(v % 2 == 0 for v in Counter(lengths).values())  # cycles come in pairs
