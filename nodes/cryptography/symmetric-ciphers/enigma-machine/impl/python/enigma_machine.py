# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enigma-machine/. The authors are listed in prov/4QX9ZT.jsonl.
"""A simulator of the three rotor Enigma I, with the double step, and Rejewski's cycles.

For study only. Enigma was broken in the 1930s and 1940s, and the code is not
constant time. Do not use it to protect real data; use AES-GCM or
ChaCha20-Poly1305 from libsodium, a FIPS 140 validated module, or the
standard library of your language.

Wirings: the rotors I to V and the reflectors A and B of the Enigma I, as
listed in the Wikipedia article "Enigma rotor details", which cites the
Crypto Museum (cryptomuseum.com). Each string gives the contact that A, B,
C, ... is wired to when the rotor is at position A with ring setting A.
The turnover letter is the letter in the window when the rotor moves its
left neighbour on the next key press.
"""

from math import factorial

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ROTORS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}

REFLECTORS = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
}


def _idx(c: str) -> int:
    return ord(c) - 65


def plugboard_map(pairs: str) -> list[int]:
    """The plugboard as a permutation: swapped pairs, the other letters fixed."""
    p = list(range(26))
    for pair in pairs.upper().split():
        a, b = _idx(pair[0]), _idx(pair[1])
        if a == b or p[a] != a or p[b] != b:
            raise ValueError("each letter may be in at most one cable")
        p[a], p[b] = b, a
    return p


def step(pos: list[int], notches: list[int]) -> list[int]:
    """One key press: the stepping of the left, middle and right rotors.

    pos and notches are [left, middle, right]. The right rotor always steps.
    A rotor at its turnover position moves the rotor to its left. The pawl
    that moves the left rotor also pushes the notch of the middle rotor, so
    a middle rotor at its turnover position steps too: the double step.
    """
    left, middle, right = pos
    if middle == notches[1]:  # the double step: the middle rotor moves itself and the left rotor
        left, middle = (left + 1) % 26, (middle + 1) % 26
    elif right == notches[2]:
        middle = (middle + 1) % 26
    right = (right + 1) % 26
    return [left, middle, right]


def _through(wiring: list[int], c: int, pos: int, ring: int) -> int:
    shift = pos - ring
    return (wiring[(c + shift) % 26] - shift) % 26


class Enigma:
    """Enigma I: three rotors from I to V, a reflector, ring settings and a plugboard."""

    def __init__(self, rotors: tuple[str, str, str], reflector: str = "B", rings: str = "AAA", plugs: str = "") -> None:
        if len(set(rotors)) != 3:
            raise ValueError("the three rotors must be different")
        self.fwd = [[_idx(c) for c in ROTORS[r][0]] for r in rotors]
        self.bwd = []
        for w in self.fwd:
            inv = [0] * 26
            for i, o in enumerate(w):
                inv[o] = i
            self.bwd.append(inv)
        self.notches = [_idx(ROTORS[r][1]) for r in rotors]
        self.reflector = [_idx(c) for c in REFLECTORS[reflector]]
        self.rings = [_idx(c) for c in rings.upper()]
        self.plug = plugboard_map(plugs)

    def letter_map(self, pos: list[int]) -> list[int]:
        """The permutation of the 26 letters for the rotor positions pos, with no stepping."""
        out = []
        for x in range(26):
            y = self.plug[x]  # @line L4
            for r in (2, 1, 0):  # @line L5
                y = _through(self.fwd[r], y, pos[r], self.rings[r])
            y = self.reflector[y]  # @line L6
            for r in (0, 1, 2):  # @line L7
                y = _through(self.bwd[r], y, pos[r], self.rings[r])
            out.append(self.plug[y])  # @line L8
        return out

    def encrypt(self, text: str, start: str) -> str:
        """Encrypt (or decrypt) the letters of text from the rotor start positions start."""
        pos = [_idx(c) for c in start.upper()]  # @line L1
        out = []
        for ch in text.upper():  # @line L2
            if not "A" <= ch <= "Z":
                continue
            pos = step(pos, self.notches)  # @line L3
            out.append(ALPHABET[self.letter_map(pos)[_idx(ch)]])
        return "".join(out)  # @line L9


def positions(start: str, notches_of: tuple[str, str, str], count: int) -> list[str]:
    """The window letters after each of count key presses."""
    notches = [_idx(ROTORS[r][1]) for r in notches_of]
    pos = [_idx(c) for c in start]
    out = []
    for _ in range(count):
        pos = step(pos, notches)
        out.append("".join(ALPHABET[p] for p in pos))
    return out


def plugboard_settings(n: int, cables: int) -> int:
    """The ways to place the given number of cables on n letters: n! / ((n-2c)! c! 2^c)."""
    return factorial(n) // (factorial(n - 2 * cables) * factorial(cables) * 2**cables)


def key_count() -> dict[str, int]:
    """The terms of the key space of the Army Enigma I with 3 of 5 rotors and 10 cables.

    Only the rings of the middle and right rotors change the stepping; the
    left ring is the same as a change of the left start position, so it adds
    no new keys.
    """
    terms = {
        "rotor orders": 5 * 4 * 3,
        "start positions": 26**3,
        "rings": 26**2,
        "plugboard": plugboard_settings(26, 10),
    }
    terms["total"] = terms["rotor orders"] * terms["start positions"] * terms["rings"] * terms["plugboard"]
    return terms


def cycle_type(perm: list[int]) -> list[int]:
    """The lengths of the cycles of perm, sorted from longest to shortest."""
    seen = [False] * len(perm)
    out = []
    for i in range(len(perm)):
        if not seen[i]:
            n, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                n += 1
            out.append(n)
    return sorted(out, reverse=True)


def characteristic(machine: Enigma, start: str) -> list[list[int]]:
    """Rejewski's characteristic: the cycle types of A1A4, A2A5 and A3A6.

    A_i is the letter map at the i-th key press from start. An operator
    encrypted the message key twice, so letters 1 and 4 of an indicator
    were the same key letter under A1 and A4. The product x -> A4(A1(x))
    is known from many indicators of one day.
    """
    maps = []
    pos = [_idx(c) for c in start]
    for _ in range(6):
        pos = step(pos, machine.notches)
        maps.append(machine.letter_map(pos))
    return [cycle_type([maps[i + 3][maps[i][x]] for x in range(26)]) for i in range(3)]


def crib_positions(ciphertext: str, crib: str) -> list[int]:
    """The offsets where the crib may lie under the ciphertext.

    Enigma never encrypts a letter to itself, so an offset where some crib
    letter equals the cipher letter above it is impossible.
    """
    return [
        i
        for i in range(len(ciphertext) - len(crib) + 1)
        if all(a != b for a, b in zip(ciphertext[i : i + len(crib)], crib))
    ]
