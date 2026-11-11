# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasiski-examination/. The authors are listed in prov/ZTGXR5.jsonl.
"""Kasiski examination: the period of a periodic polyalphabetic cipher from repeats.

For study only. It is an attack on classical ciphers such as the Vigenere
cipher. Do not use those ciphers to protect real data; use AES-GCM or
ChaCha20-Poly1305 from libsodium, a FIPS 140 validated module, or the
standard library of your language.
"""

import math


def letters(text: str) -> str:
    """Keep the letters A to Z of text, in upper case."""
    return "".join(c for c in text.upper() if "A" <= c <= "Z")


def repeats(ciphertext: str, length: int = 3) -> dict[str, list[int]]:
    """Each substring of the given length that occurs at least twice, with its start positions."""
    c = letters(ciphertext)
    pos: dict[str, list[int]] = {}
    for i in range(len(c) - length + 1):  # @line L1
        pos.setdefault(c[i : i + length], []).append(i)  # @line L2
    return {s: p for s, p in pos.items() if len(p) >= 2}


def kasiski_distances(ciphertext: str, length: int = 3) -> list[int]:
    """The distances between consecutive occurrences of each repeated substring."""
    out = []
    for p in repeats(ciphertext, length).values():
        out.extend(b - a for a, b in zip(p, p[1:]))  # @line L3
    return sorted(out)


def factor_counts(distances: list[int], max_period: int = 20) -> dict[int, int]:
    """For each m in 2..max_period, the number of distances that m divides."""
    return {m: sum(d % m == 0 for d in distances) for m in range(2, max_period + 1)}  # @line L4


def kasiski_period(ciphertext: str, length: int = 3, max_period: int = 20) -> int | None:
    """The period m in 2..max_period that divides the most distances beyond chance.

    A distance from a true repeat is a multiple of the period; a false hit
    is a random number, which m divides with a chance of about 1/m. So the
    score of m is count(m) - N/m for N distances, and the best score wins
    (the smaller m on a tie). Returns None when there is no repeat.
    """
    d = kasiski_distances(ciphertext, length)
    if not d:
        return None
    counts = factor_counts(d, max_period)
    return max(counts, key=lambda m: (counts[m] - len(d) / m, -m))  # @line L5


def gcd_of_distances(distances: list[int]) -> int:
    """The gcd of all distances; one false hit can make it 1."""
    return math.gcd(*distances) if distances else 0
