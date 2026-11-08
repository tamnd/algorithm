# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/halton-sequence/. The authors are listed in prov/MKABDE.jsonl.

"""The van der Corput radical inverse and the Halton sequence, with exact rational output."""

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple

FIRST_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71)


def radical_inverse_int(i: int, b: int) -> Tuple[int, int]:
    """Return (numerator, denominator) of phi_b(i), the base-b digits of i mirrored about the point.

    The denominator is b^L where L is the number of base-b digits of i (1 for i = 0).
    """
    if b < 2:
        raise ValueError("need a base b >= 2")
    if i < 0:
        raise ValueError("need an index i >= 0")
    num, den, n = 0, 1, i
    while n > 0:  # @line L3
        num = num * b + n % b  # @line L4
        n //= b  # @line L5
        den *= b  # @line L5
    return num, max(den, 1)


def radical_inverse(i: int, b: int) -> Fraction:
    """phi_b(i) as an exact fraction."""
    num, den = radical_inverse_int(i, b)
    return Fraction(num, den)


def radical_inverse_float(i: int, b: int) -> float:
    """phi_b(i) as a float, accumulated digit by digit as in the pseudocode."""
    x, f, n = 0.0, 1.0 / b, i  # @line L2
    while n > 0:  # @line L3
        x += f * (n % b)  # @line L4
        n //= b  # @line L5
        f /= b  # @line L5
    return x  # @line L6


def halton(i: int, bases: Sequence[int] = (2, 3)) -> Tuple[Fraction, ...]:
    """The i-th Halton point (phi_(b_1)(i), ..., phi_(b_d)(i)) for pairwise coprime bases."""
    return tuple(radical_inverse(i, b) for b in bases)  # @line L1 @line L7


def halton_points(n: int, bases: Sequence[int] = (2, 3), start: int = 0) -> List[Tuple[Fraction, ...]]:
    """Points start, ..., start + n - 1 of the Halton sequence."""
    return [halton(i, bases) for i in range(start, start + n)]


class HaltonStream:
    """Incremental Halton generator: one base-b counter per coordinate, O(1) amortized digit updates.

    Coordinates are kept as exact integers over b^L, where L grows as needed.
    """

    def __init__(self, bases: Sequence[int] = (2, 3), start: int = 0) -> None:
        for b in bases:
            if b < 2:
                raise ValueError("need bases >= 2")
        self.bases = tuple(bases)
        self.index = start
        self.digits: List[List[int]] = []
        for b in self.bases:
            ds, n = [], start
            while n > 0:
                ds.append(n % b)
                n //= b
            self.digits.append(ds)

    def _value(self, k: int) -> Fraction:
        b, ds = self.bases[k], self.digits[k]
        num = 0
        for d in ds:
            num = num * b + d
        return Fraction(num, b ** len(ds)) if ds else Fraction(0)

    def next(self) -> Tuple[Fraction, ...]:
        point = tuple(self._value(k) for k in range(len(self.bases)))
        self.index += 1
        for k, b in enumerate(self.bases):
            ds = self.digits[k]
            j = 0
            while j < len(ds) and ds[j] == b - 1:
                ds[j] = 0
                j += 1
            if j == len(ds):
                ds.append(1)
            else:
                ds[j] += 1
        return point


def scrambled_radical_inverse(i: int, b: int, perms: Sequence[Sequence[int]]) -> Fraction:
    """Digit-permuted radical inverse: digit j of i is replaced by perms[j][digit] before mirroring.

    Each permutation must fix 0, so that the infinitely many leading zero digits stay zero.
    """
    num, den, n, j = 0, 1, i, 0
    while n > 0:
        p = perms[j]
        num = num * b + p[n % b]
        n //= b
        den *= b
        j += 1
    return Fraction(num, den)


def star_discrepancy_1d(xs: Sequence[Fraction]) -> Fraction:
    """Exact star discrepancy of points in [0, 1): 1/(2N) + max |x_(i) - (2i - 1)/(2N)| (Niederreiter, Theorem 2.6)."""
    n = len(xs)
    ys = sorted(xs)
    return Fraction(1, 2 * n) + max(abs(y - Fraction(2 * i + 1, 2 * n)) for i, y in enumerate(ys))


def star_discrepancy_2d(points: Sequence[Tuple[Fraction, Fraction]]) -> Fraction:
    """Exact star discrepancy of a 2D point set by checking all critical boxes [0, y)."""
    n = len(points)
    xs = sorted(set(p[0] for p in points) | {Fraction(1)})
    ys = sorted(set(p[1] for p in points) | {Fraction(1)})
    best = Fraction(0)
    for a in xs:
        col = sorted(p[1] for p in points if p[0] < a)
        col_closed = sorted(p[1] for p in points if p[0] <= a)
        for c in ys:
            vol = a * c
            open_count = sum(1 for y in col if y < c)
            closed_count = sum(1 for y in col_closed if y <= c)
            best = max(best, vol - Fraction(open_count, n), Fraction(closed_count, n) - vol)
    return best


def discrepancy_bound(n: int, bases: Sequence[int]) -> Fraction:
    """The bound (d + prod_k ((b_k - 1) L_k + 1)) / N with b_k^L_k >= N proved on the page."""
    prod = 1
    for b in bases:
        L = 0
        while b ** L < n:
            L += 1
        prod *= (b - 1) * L + 1
    return Fraction(len(bases) + prod, n)


def count_in_box(points: Sequence[Tuple[Fraction, ...]], lows: Sequence[Fraction], highs: Sequence[Fraction]) -> int:
    return sum(1 for p in points if all(lo <= x < hi for x, lo, hi in zip(p, lows, highs)))
