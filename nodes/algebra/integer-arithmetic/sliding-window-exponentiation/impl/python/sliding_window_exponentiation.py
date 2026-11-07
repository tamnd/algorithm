# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-exponentiation/. The authors are listed in prov/YXZZ39.jsonl.

"""Left-to-right sliding-window exponentiation in any monoid.

power(x, e, k, mul) computes x^e with the odd powers x, x^3, ..., x^(2^k - 1)
precomputed, and the exponent read from the top in windows of at most k binary
digits that start and end with a 1. Squarings of the identity are skipped, so
the counts are those of the addition chain that the method builds.

For integers the products go through limb arrays (radix 2^w, schoolbook), so
the tests can check limb code against Python's int.
"""

from typing import Callable, TypeVar

T = TypeVar("T")


class Counter:
    def __init__(self) -> None:
        self.squarings = 0
        self.products = 0

    @property
    def total(self) -> int:
        return self.squarings + self.products


def windows(e: int, k: int) -> list[tuple[int, int]]:
    """The decomposition of e >= 1, from the top, as (value, length) pairs.

    A pair with value 0 and length 1 is a single zero digit; any other pair is
    a window of `length` <= k digits whose first and last digits are 1.
    """
    if e < 1 or k < 1:
        raise ValueError("need e >= 1 and k >= 1")
    out = []
    i = e.bit_length() - 1
    while i >= 0:
        if (e >> i) & 1 == 0:
            out.append((0, 1))
            i -= 1
            continue
        j = max(i - k + 1, 0)
        while (e >> j) & 1 == 0:  # the window must end with a 1
            j += 1
        out.append(((e >> j) & ((1 << (i - j + 1)) - 1), i - j + 1))
        i = j - 1
    return out


def power(x: T, e: int, k: int, mul: Callable[[T, T], T], one: T, cnt: Counter | None = None) -> T:
    """x^e for e >= 0 in the monoid given by mul and one, with window width k."""
    if k < 1:
        raise ValueError("k must be at least 1")
    if e == 0:
        return one
    cnt = cnt if cnt is not None else Counter()
    table = {1: x}  # @line L1: the odd powers x, x^3, ..., x^(2^k - 1)
    if k > 1 and e > 1:
        x2 = mul(x, x)
        cnt.squarings += 1
        top = min((1 << k) - 1, e)
        for u in range(3, top + 1, 2):
            table[u] = mul(table[u - 2], x2)
            cnt.products += 1
    y = None  # @line L2: y = 1, kept symbolic so that 1 * 1 is not counted
    for u, length in windows(e, k):  # @line L3: the windows from the top
        for _ in range(length):  # @line L4: shift: y <- y^(2^length)
            if y is not None:
                y = mul(y, y)
                cnt.squarings += 1
        if u:  # @line L5: add the window: y <- y * x^u
            if y is None:
                y = table[u]
            else:
                y = mul(y, table[u])
                cnt.products += 1
    return y  # @line L6


def fixed_window_power(x: T, e: int, k: int, mul: Callable[[T, T], T], one: T, cnt: Counter | None = None) -> T:
    """The 2^k-ary method: all powers x^0 .. x^(2^k - 1), windows at fixed positions."""
    if e == 0:
        return one
    cnt = cnt if cnt is not None else Counter()
    table = [one, x]
    for u in range(2, min(1 << k, e + 1)):
        table.append(mul(table[-1], x))
        if u == 2:
            cnt.squarings += 1
        else:
            cnt.products += 1
    digits = []
    while e:
        digits.append(e & ((1 << k) - 1))
        e >>= k
    y = None
    for d in reversed(digits):
        if y is not None:
            for _ in range(k):
                y = mul(y, y)
                cnt.squarings += 1
        if d:
            if y is None:
                y = table[d]
            else:
                y = mul(y, table[d])
                cnt.products += 1
        elif y is None:
            raise AssertionError("the top digit is nonzero")
    return y


def best_width(t: int) -> int:
    """The k minimizing the expected count t - 1 + t / (k + 1) + 2^(k - 1)."""
    return min(range(1, 16), key=lambda k: t / (k + 1) + 2 ** (k - 1))


# Integers as limb arrays in radix 2^w.


def to_limbs(x: int, w: int) -> list[int]:
    out = []
    while x:
        out.append(x & ((1 << w) - 1))
        x >>= w
    return out


def from_limbs(d: list[int], w: int) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def limb_mul(a: list[int], b: list[int], w: int) -> list[int]:
    """Schoolbook product of limb arrays, without leading zero limbs."""
    if not a or not b:
        return []
    mask = (1 << w) - 1
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j, y in enumerate(b):
            s = c[i + j] + x * y + carry
            c[i + j] = s & mask
            carry = s >> w
        c[i + len(b)] = carry
    while c and c[-1] == 0:
        c.pop()
    return c


def power_limbs(a: list[int], e: int, k: int, w: int = 8, cnt: Counter | None = None) -> list[int]:
    """a^e for a limb array a in radix 2^w."""
    return power(a, e, k, lambda p, q: limb_mul(p, q, w), [1], cnt)


def modpow_limbs(a: list[int], e: int, m: list[int], k: int, w: int = 8, cnt: Counter | None = None) -> list[int]:
    """a^e mod m: limb products, each reduced modulo m (the reduction uses Python's %)."""
    M = from_limbs(m, w)
    if M < 1:
        raise ZeroDivisionError("modulus must be positive")

    def mulmod(p: list[int], q: list[int]) -> list[int]:
        return to_limbs(from_limbs(limb_mul(p, q, w), w) % M, w)

    one = to_limbs(1 % M, w)
    x = to_limbs(from_limbs(a, w) % M, w)
    return power(x, e, k, mulmod, one, cnt)
