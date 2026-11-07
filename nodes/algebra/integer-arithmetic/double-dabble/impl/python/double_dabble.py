# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-dabble/. The authors are listed in prov/8H3YQ9.jsonl.


def decimal_digits_for(n: int) -> int:
    """The number of decimal digits of 2^n - 1, enough for any n-bit number."""
    return max(1, len(str((1 << n) - 1)))


def double_dabble(bits: list[int]) -> list[int]:
    """Convert a binary number to BCD digits by shift and add 3.

    Precondition: bits holds n >= 0 entries in {0, 1}, the most significant
    bit first. Returns d = decimal_digits_for(n) BCD digits, the least
    significant digit first, each in 0..9. Cost: n * d digit steps, each a
    compare, an add of 3 and a shift of a 4-bit digit, so Theta(n^2).
    """
    n = len(bits)
    d = decimal_digits_for(n)
    digits = [0] * d  # @line L1
    for bit in bits:  # @line L2
        for i in range(d):  # @line L3
            if digits[i] >= 5:  # @line L4
                digits[i] += 3
        carry = bit  # @line L5
        for i in range(d):  # @line L6
            t = 2 * digits[i] + carry  # @line L7
            digits[i], carry = t & 15, t >> 4  # @line L8
        if carry:
            raise AssertionError("the BCD register overflowed")
    return digits  # @line L9


def to_bcd(x: int, n: int) -> int:
    """The packed BCD form of 0 <= x < 2^n: four bits per decimal digit."""
    bits = [(x >> k) & 1 for k in range(n - 1, -1, -1)]
    digits = double_dabble(bits)
    return sum(dig << (4 * i) for i, dig in enumerate(digits))
