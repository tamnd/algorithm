# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ripple-carry-adder/. The authors are listed in prov/0BHM0W.jsonl.


def full_adder(a: int, b: int, c: int) -> tuple[int, int]:
    """One full adder cell on bits: returns (sum, carry out) with a + b + c = sum + 2 carry."""
    p = a ^ b
    return p ^ c, (a & b) | (c & p)


def ripple_carry_add(a: list[int], b: list[int], c_in: int = 0) -> list[int]:
    """Sum of two n-bit words, least significant bit first, as n + 1 bits.

    The circuit is a chain of n full adders. Each stage uses the gates
    p = a XOR b, g = a AND b, s = p XOR c, c' = g OR (p AND c): 5 gates, so 5n gates,
    and the carry passes through 2 gates per stage, so the depth is 2n + 1.
    """
    if len(a) != len(b):
        raise ValueError("operands must have the same width")
    n = len(a)
    s = [0] * (n + 1)
    c = c_in  # @line L1
    for i in range(n):  # @line L2
        p = a[i] ^ b[i]  # @line L3
        g = a[i] & b[i]  # @line L4
        s[i] = p ^ c  # @line L5
        c = g | (p & c)  # @line L6
    s[n] = c  # @line L7
    return s  # @line L8


def ripple_carry_add_limbs(a: list[int], b: list[int], w: int = 8, c_in: int = 0) -> list[int]:
    """The same chain in radix 2^w: each cell adds two limbs and a carry bit.

    This is the multiprecision addition of the word RAM (Knuth's Algorithm A).
    """
    if len(a) != len(b):
        raise ValueError("operands must have the same length")
    mask = (1 << w) - 1
    s = [0] * (len(a) + 1)
    c = c_in
    for i in range(len(a)):
        t = a[i] + b[i] + c
        s[i] = t & mask
        c = t >> w
    s[len(a)] = c
    return s


def add_signed(a: list[int], b: list[int]) -> tuple[list[int], int]:
    """Two's complement addition of n-bit words: the n-bit sum and the overflow flag.

    The overflow flag is the XOR of the carry into and the carry out of the top stage.
    """
    n = len(a)
    if n != len(b) or n == 0:
        raise ValueError("operands must have the same positive width")
    c = 0
    s = [0] * n
    c_top_in = 0
    for i in range(n):
        if i == n - 1:
            c_top_in = c
        s[i], c = full_adder(a[i], b[i], c)
    return s, c_top_in ^ c


def subtract(a: list[int], b: list[int]) -> tuple[list[int], int]:
    """a - b modulo 2^n by a + NOT b + 1; returns the n-bit difference and the carry out.

    The carry out is 1 exactly when a >= b as unsigned numbers (no borrow).
    """
    s = ripple_carry_add(a, [1 - x for x in b], 1)
    return s[:-1], s[-1]


def carry_chain_length(a: list[int], b: list[int]) -> int:
    """The longest run of stages through which one carry propagates (the settling time).

    A carry is generated at stage i (a_i = b_i = 1) and travels while p_j = 1.
    """
    longest = run = 0
    active = False
    for x, y in zip(a, b):
        if x & y:
            active, run = True, 1
        elif x ^ y and active:
            run += 1
        else:
            active, run = False, 0
        longest = max(longest, run)
    return longest
