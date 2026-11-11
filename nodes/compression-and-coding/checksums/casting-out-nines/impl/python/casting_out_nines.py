# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/casting-out-nines/. The authors are listed in prov/SXWWDF.jsonl.

"""Casting out nines and casting out elevens: checks on hand arithmetic.

Since 10 = 1 mod 9, a number is congruent mod 9 to the sum of its decimal
digits. The "excess of nines" of a number is that sum with all nines cast
out: a value in 0..8. A sum or product is checked by doing the same
operation on the excesses of the operands and comparing with the excess of
the claimed result. A mismatch proves an error. A match does not prove that
the result is right: every error that changes the result by a multiple of 9
is missed, and that includes any transposition of its digits.

Since 10 = -1 mod 11, the alternating sum of the digits, from the right,
gives the number mod 11. Casting out elevens catches the adjacent
transpositions of different digits that casting out nines misses. The two
checks together miss exactly the errors that are multiples of 99.

The code works on the decimal digits only. It never takes x % 9 of the
number itself.

Cost: Theta(n) digit additions for n digits, O(1) extra space.
"""


def _digits(x: int) -> list[int]:
    if x < 0:
        raise ValueError("expected a non-negative integer")
    return [ord(c) - 48 for c in str(x)]


def excess9(x: int) -> int:
    """The excess of nines of x: its digit sum with nines cast out, in 0..8."""
    r = 0  # @line L1
    for d in _digits(x):  # @line L2
        r += d  # @line L3
        if r >= 9:  # @line L4
            r -= 9
    return r  # @line L5


def check_addition(a: int, b: int, claimed: int) -> bool:
    """False proves claimed != a + b. True means the check found no error."""
    return excess9(excess9(a) + excess9(b)) == excess9(claimed)  # @line L6


def check_multiplication(a: int, b: int, claimed: int) -> bool:
    """False proves claimed != a * b. True means the check found no error."""
    return excess9(excess9(a) * excess9(b)) == excess9(claimed)  # @line L7


def excess11(x: int) -> int:
    """x mod 11 from the alternating digit sum, read from the right."""
    r = 0
    for i, d in enumerate(reversed(_digits(x))):
        r = (r + d) % 11 if i % 2 == 0 else (r - d) % 11
    return r


def check_addition11(a: int, b: int, claimed: int) -> bool:
    return (excess11(a) + excess11(b)) % 11 == excess11(claimed)


def check_multiplication11(a: int, b: int, claimed: int) -> bool:
    return (excess11(a) * excess11(b)) % 11 == excess11(claimed)
