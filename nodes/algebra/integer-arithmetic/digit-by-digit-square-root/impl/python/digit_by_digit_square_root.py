# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/digit-by-digit-square-root/. The authors are listed in prov/SH6MP2.jsonl.


def digit_sqrt(a: list[int], base: int) -> tuple[list[int], int]:
    """Integer square root of a number given as base-`base` digits.

    Precondition: base >= 2 and 0 <= a[i] < base, digits least significant
    first (an empty list is 0). Returns (root digits, remainder) with
    root = isqrt(A), remainder = A - root^2 and 0 <= remainder <= 2 * root;
    the root has ceil(len(a) / 2) digits, least significant first. The
    remainder r and the partial root q are Python ints of O(n) digits. Cost:
    n steps for a root of n digits, each with O(log base) trial products of
    an O(n)-digit number by one digit, so Theta(n^2) digit operations for a
    fixed base.
    """
    if base < 2 or any(not 0 <= v < base for v in a):
        raise ValueError("digits must lie in 0 .. base - 1")
    digits = list(a)
    if len(digits) % 2:
        digits.append(0)
    n = len(digits) // 2
    q, r = 0, 0  # @line L1
    root: list[int] = []
    for k in range(n - 1, -1, -1):  # @line L2
        r = r * base * base + digits[2 * k + 1] * base + digits[2 * k]  # @line L3
        lo, hi = 0, base - 1  # @line L4: largest x with (2 q base + x) x <= r
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if (2 * q * base + mid) * mid <= r:
                lo = mid
            else:
                hi = mid - 1
        x = lo
        r -= (2 * q * base + x) * x  # @line L5
        q = q * base + x  # @line L6
        root.append(x)
    root.reverse()
    return root, r  # @line L7


def to_digits(x: int, base: int) -> list[int]:
    """The digits of x >= 0 in the given base, least significant first."""
    out: list[int] = []
    while x:
        x, d = divmod(x, base)
        out.append(d)
    return out


def from_digits(digits: list[int], base: int) -> int:
    """The value of a digit list, least significant first."""
    value = 0
    for d in reversed(digits):
        value = value * base + d
    return value
