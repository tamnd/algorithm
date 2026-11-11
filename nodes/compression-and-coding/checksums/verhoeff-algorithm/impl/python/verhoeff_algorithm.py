# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verhoeff-algorithm/. The authors are listed in prov/ZV0WXF.jsonl.

"""The Verhoeff check digit (J. Verhoeff, Error Detecting Decimal Codes, 1969).

The digits 0..9 name the ten elements of the dihedral group D5 (the symmetries
of a regular pentagon). D is its multiplication table, P[i] is the i-th power
of a fixed permutation of the digits, and INV gives the group inverse.

Read the digits from the right, with the check digit at position 0 for
validation. The running value is c <- D[c][P[i mod 8][digit]]. A number is
valid when the final c is 0. To make a check digit, run the same loop over
the payload with positions starting at 1, then take INV[c].

Cost: Theta(n) table lookups for n digits, O(1) extra space.
"""

# Multiplication table of D5: rows 0-4 are the rotations, rows 5-9 the reflections.
D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

# P[i] is the permutation (0 1 5 8 9 4 2 7)(3 6) applied i times.
P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]

INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def _digits(s: str) -> list[int]:
    if not s or not s.isdigit() or not s.isascii():
        raise ValueError("expected a non-empty string of decimal digits")
    return [ord(c) - 48 for c in s]


def verhoeff_state(number: str, start: int) -> int:
    """The running value c after all digits, read from the right with positions from start."""
    c = 0  # @line L1
    for i, d in enumerate(reversed(_digits(number)), start):  # @line L2
        c = D[c][P[i % 8][d]]  # @line L3
    return c  # @line L4


def check_digit(payload: str) -> str:
    """The digit that makes payload + digit valid."""
    return str(INV[verhoeff_state(payload, 1)])  # @line L5


def is_valid(number: str) -> bool:
    """True when the number, check digit last, passes the Verhoeff test."""
    return verhoeff_state(number, 0) == 0  # @line L6
