# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/booth-multiplication/. The authors are listed in prov/B6TGDA.jsonl.

"""Booth's multiplication of n-bit two's complement integers.

Registers are fixed-width bit patterns held in Python ints in [0, 2^width).
booth_multiply is the sequential radix-2 algorithm with the registers A, Q and
the extra bit q_{-1}; booth4_multiply sums the radix-4 recoded partial products.
"""


def to_unsigned(x: int, width: int) -> int:
    """The width-bit two's complement pattern of x."""
    return x & ((1 << width) - 1)


def to_signed(u: int, width: int) -> int:
    """The value of a width-bit two's complement pattern."""
    return u - (1 << width) if u >> (width - 1) & 1 else u


def _check(x: int, y: int, n: int) -> None:
    if n < 1:
        raise ValueError("n must be at least 1")
    lo, hi = -(1 << (n - 1)), (1 << (n - 1)) - 1
    if not (lo <= x <= hi and lo <= y <= hi):
        raise ValueError("operands must be n-bit two's complement integers")


def booth_multiply(x: int, y: int, n: int) -> tuple[int, int]:
    """Return (x * y, number of additions and subtractions) by radix-2 Booth.

    Precondition: x and y are n-bit two's complement integers, n >= 1.
    A has n + 1 bits so that A - x cannot overflow; (A, Q) holds 2n + 1 bits
    and the product is their low 2n bits read as a two's complement number.
    Cost: n steps, each one add or subtract of n + 1 bits and a shift.
    """
    _check(x, y, n)
    wa = n + 1
    mask_a = (1 << wa) - 1
    xa = to_unsigned(x, wa)
    a, q, q_1 = 0, to_unsigned(y, n), 0  # @line L1
    ops = 0
    for _ in range(n):  # @line L2
        q0 = q & 1
        if (q0, q_1) == (1, 0):  # @line L3
            a = (a - xa) & mask_a
            ops += 1
        elif (q0, q_1) == (0, 1):  # @line L4
            a = (a + xa) & mask_a
            ops += 1
        q_1 = q0  # @line L5
        q = (q >> 1) | ((a & 1) << (n - 1))
        a = (a >> 1) | (a & (1 << (wa - 1)))  # arithmetic shift keeps the sign
    product = (a << n) | q  # @line L6
    return to_signed(product & ((1 << (2 * n)) - 1), 2 * n), ops


def booth2_digits(y: int, n: int) -> list[int]:
    """Radix-2 Booth digits y_{i-1} - y_i, i = 0..n-1, of an n-bit y."""
    u = to_unsigned(y, n)
    bits = [(u >> i) & 1 for i in range(n)]
    return [(bits[i - 1] if i else 0) - bits[i] for i in range(n)]


def booth4_digits(y: int, n: int) -> list[int]:
    """Radix-4 Booth digits y_{2j-1} + y_{2j} - 2 y_{2j+1}, in {-2..2}.

    The pattern is sign-extended to an even number of bits first.
    """
    m = n + (n & 1)
    u = to_unsigned(y, m)
    bits = [(u >> i) & 1 for i in range(m)]
    digits = []
    for j in range(m // 2):  # @line L7
        low = bits[2 * j - 1] if j else 0
        digits.append(low + bits[2 * j] - 2 * bits[2 * j + 1])
    return digits


def booth4_multiply(x: int, y: int, n: int) -> tuple[int, int]:
    """Return (x * y, number of nonzero partial products) by radix-4 Booth.

    Each partial product q_j * x is 0, +-x or +-2x: a shift and a negation
    in 2n-bit two's complement, added with a 2n-bit adder.
    """
    _check(x, y, n)
    width = 2 * n + 2
    mask = (1 << width) - 1
    acc = 0
    nonzero = 0
    for j, q in enumerate(booth4_digits(y, n)):  # @line L8
        if q == 0:
            continue
        nonzero += 1
        mag = to_unsigned(x << (abs(q) - 1), width)
        term = (-mag) & mask if q < 0 else mag
        acc = (acc + (term << (2 * j))) & mask
    return to_signed(acc, width), nonzero  # @line L9
