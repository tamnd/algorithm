# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/russian-peasant-multiplication/. The authors are listed in prov/ANVYVS.jsonl.


def russian_peasant_multiply(x: list[int], y: list[int], w: int = 8) -> list[int]:
    """Product of two nonnegative limb arrays (base 2^w, least significant limb first).

    Halve y and double x until y is zero, and add x to the result whenever y is
    odd. Uses only addition and one-bit shifts. Returns a normalized limb array.
    Cost: O(N) additions and shifts of arrays of O(n) limbs, where N is the
    number of binary digits of y, so O(N (m + n)) limb operations.
    """
    p: list[int] = []  # @line L1
    x, y = _normalize(list(x)), _normalize(list(y))
    while y:  # @line L2: y > 0
        if y[0] & 1:  # @line L3
            p = _add(p, x, w)
        x = _shl1(x, w)  # @line L4
        y = _shr1(y, w)  # @line L5
    return p  # @line L6


def _normalize(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def _add(a: list[int], b: list[int], w: int) -> list[int]:
    """a + b for limb arrays, one carry pass."""
    if len(a) < len(b):
        a, b = b, a
    out, carry, mask = [], 0, (1 << w) - 1
    for i in range(len(a)):
        t = a[i] + (b[i] if i < len(b) else 0) + carry
        out.append(t & mask)
        carry = t >> w
    if carry:
        out.append(carry)
    return out


def _shl1(a: list[int], w: int) -> list[int]:
    """2 a: shift each limb left by one bit and pass the top bit up."""
    out, carry, mask = [], 0, (1 << w) - 1
    for d in a:
        out.append(((d << 1) & mask) | carry)
        carry = d >> (w - 1)
    if carry:
        out.append(carry)
    return out


def _shr1(a: list[int], w: int) -> list[int]:
    """floor(a / 2): shift each limb right by one bit and pass the low bit down."""
    out = [0] * len(a)
    carry = 0
    for i in range(len(a) - 1, -1, -1):
        out[i] = (a[i] >> 1) | (carry << (w - 1))
        carry = a[i] & 1
    return _normalize(out)
