# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luhn-algorithm/. The authors are listed in prov/BC0D59.jsonl.

"""The Luhn algorithm (H. P. Luhn, US patent 2,950,048; ISO/IEC 7812-1).

Count positions from the right, with the check digit at position 1. Every
digit at an even position is doubled, and 9 is taken off a result above 9
(the same as adding the two digits of the product). The number is valid when
the total of all the digits after this step is 0 mod 10.

To make a check digit for a payload, run the same step over the payload with
the doubling on the rightmost payload digit, and choose the digit that brings
the total to 0 mod 10.

Cost: Theta(n) for n digits, O(1) extra space.
"""

DOUBLE = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]  # D(x) = 2x, minus 9 when 2x > 9


def _digits(s: str) -> list[int]:
    if not s or not s.isdigit() or not s.isascii():
        raise ValueError("expected a non-empty string of decimal digits")
    return [ord(c) - 48 for c in s]


def luhn_sum(number: str, double_first: bool) -> int:
    """The Luhn total mod 10, read from the right; double_first doubles the rightmost digit."""
    total = 0  # @line L1
    double = double_first  # @line L2
    for d in reversed(_digits(number)):  # @line L3
        total += DOUBLE[d] if double else d  # @line L4
        double = not double  # @line L5
    return total % 10  # @line L6


def check_digit(payload: str) -> str:
    """The digit c such that payload + c is valid."""
    return str((10 - luhn_sum(payload, True)) % 10)  # @line L7


def is_valid(number: str) -> bool:
    """True when the full number, check digit last, passes the Luhn test."""
    return luhn_sum(number, False) == 0  # @line L8
