# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-save-addition/. The authors are listed in prov/KMMETW.jsonl.

"""Carry-save addition on digit lists in base beta, least significant digit first.

csa reduces three numbers to two with no carry propagation: each output digit
depends only on the three input digits in the same position. A sum of many
numbers is kept as a pair (S, C) and resolved by one ordinary addition at the end.
"""


def csa(x: list[int], y: list[int], z: list[int], base: int) -> tuple[list[int], list[int]]:
    """Return (s, c) with x + y + z = s + c, all of the same length as the inputs.

    The inputs must have the same length and digits in [0, base); the top
    digit of each must be small enough that the sum fits, which the callers
    ensure by padding with zeros.
    """
    n = len(x)
    s = [0] * n
    c = [0] * n
    for i in range(n):  # @line L1: every position at once, in a circuit
        t = x[i] + y[i] + z[i]  # @line L1
        s[i] = t % base  # @line L2
        if i + 1 < n:
            c[i + 1] = t // base  # @line L2: the carry goes to the next position, not further
        elif t >= base:
            raise OverflowError("the sum does not fit; pad the operands")
    c[0] = 0  # @line L3
    return s, c  # @line L4


def propagate_add(x: list[int], y: list[int], base: int) -> list[int]:
    """An ordinary carry-propagate addition, used once at the end."""
    out, carry = [], 0
    for u, v in zip(x, y):
        t = u + v + carry
        out.append(t % base)
        carry = t // base
    if carry:
        raise OverflowError("the sum does not fit")
    return out


def carry_save_sum(numbers: list[list[int]], base: int) -> tuple[list[int], int]:
    """Add m numbers of equal length with a chain of carry-save adders.

    Returns the digits of the sum and the number of csa steps, m - 2 for m >= 2.
    The operands must be padded so that the total fits.
    """
    n = len(numbers[0])
    zero = [0] * n
    big_s, big_c = numbers[0], zero  # @line L5
    if len(numbers) == 1:
        return propagate_add(big_s, big_c, base), 0
    big_c = numbers[1]
    steps = 0
    for x in numbers[2:]:  # @line L6
        big_s, big_c = csa(big_s, big_c, x, base)  # @line L6
        steps += 1
    return propagate_add(big_s, big_c, base), steps  # @line L7


def carry_save_tree(numbers: list[list[int]], base: int) -> tuple[list[int], int]:
    """Add m numbers with levels of parallel carry-save adders (a Wallace tree).

    Each level groups the numbers in threes and replaces every group by two.
    Returns the digits of the sum and the number of levels.
    """
    level = list(numbers)
    levels = 0
    while len(level) > 2:
        nxt = []
        full = len(level) - len(level) % 3
        for j in range(0, full, 3):
            s, c = csa(level[j], level[j + 1], level[j + 2], base)
            nxt += [s, c]
        nxt += level[full:]
        level = nxt
        levels += 1
    if len(level) == 1:
        level.append([0] * len(level[0]))
    return propagate_add(level[0], level[1], base), levels


def to_digits(x: int, n: int, base: int) -> list[int]:
    out = []
    for _ in range(n):
        x, r = divmod(x, base)
        out.append(r)
    if x:
        raise OverflowError("the number does not fit in n digits")
    return out


def from_digits(d: list[int], base: int) -> int:
    v = 0
    for digit in reversed(d):
        v = v * base + digit
    return v


def width_for(m: int, n: int, base: int) -> int:
    """Digits enough for the sum of m numbers of n digits."""
    w, cap = n, base ** n
    while (cap - 1) * m >= base ** w:
        w += 1
    return w
