# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/damm-algorithm/. The authors are listed in prov/B1H68B.jsonl.

"""The Damm check digit (H. Michael Damm, PhD thesis, Marburg, 2004).

Q is a totally anti-symmetric quasigroup of order 10 with a zero diagonal.
Read the digits from the left with an interim digit c that starts at 0 and
becomes Q[c][d] for each digit d. The check digit of a payload is the final c.
A full number is valid when the final c is 0, because Q[c][c] = 0.

The table is the one printed in the Wikipedia article "Damm algorithm", which
takes it from the thesis (page 111) with the rows reordered to get the zero
diagonal. The tests check every property the method needs.

Cost: Theta(n) table lookups for n digits, O(1) extra space.
"""

Q = [
    [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
    [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
    [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
    [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
    [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
    [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
    [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
    [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
    [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
    [2, 5, 8, 1, 4, 3, 6, 7, 9, 0],
]


def _digits(s: str) -> list[int]:
    if not s or not s.isdigit() or not s.isascii():
        raise ValueError("expected a non-empty string of decimal digits")
    return [ord(c) - 48 for c in s]


def interim(number: str) -> int:
    """The interim digit after all digits of number, read from the left."""
    c = 0  # @line L1
    for d in _digits(number):  # @line L2
        c = Q[c][d]  # @line L3
    return c  # @line L4


def check_digit(payload: str) -> str:
    """The digit that makes payload + digit valid."""
    return str(interim(payload))  # @line L5


def is_valid(number: str) -> bool:
    """True when the number, check digit last, passes the Damm test."""
    return interim(number) == 0  # @line L6
