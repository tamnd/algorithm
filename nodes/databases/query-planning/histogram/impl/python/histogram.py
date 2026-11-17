# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram/. The authors are listed in prov/R1T161.jsonl.
"""Histograms for selectivity estimation on an integer column.

A Histogram is a list of buckets (lo, hi, count, distinct): the bucket covers
the integers lo..hi, holds `count` tuples and `distinct` distinct values.
Buckets are sorted and disjoint. Estimates assume that the tuples of a bucket
are spread evenly over the integers lo..hi (for ranges) and over its distinct
values (for equality).

Builders:
  equi_width(values, B)  B ranges of equal width, O(N + B)
  equi_depth(values, B)  B buckets of about N / B tuples each, O(N log N)
  v_optimal(values, B)   minimum total squared error of the frequencies,
                         by dynamic programming, O(n^2 B) for n distinct values
  EndBiased(values, B)   B - 1 singleton buckets for extreme frequencies
All arithmetic is exact (Fraction).
"""

from bisect import bisect_left, bisect_right
from collections import Counter
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Bucket = Tuple[int, int, int, int]  # lo, hi, count, distinct


def sse(prefix: List[Fraction], prefix2: List[Fraction], i: int, j: int) -> Fraction:
    """Sum of squared deviations from the mean of f[i+1..j] (1-based), j > i."""
    s = prefix[j] - prefix[i]
    return prefix2[j] - prefix2[i] - s * s / (j - i)


def v_optimal_partition(f: Sequence[int], B: int) -> Tuple[Fraction, List[Tuple[int, int]]]:
    """Split f[0..n-1] into at most B contiguous groups with the least total
    squared error. Returns (error, groups as half-open index ranges).
    Precondition: n >= 1, B >= 1. Time O(n^2 B), space O(n B)."""
    n = len(f)
    B = min(B, n)
    prefix, prefix2 = [Fraction(0)], [Fraction(0)]
    for x in f:  # @line L1
        prefix.append(prefix[-1] + x)
        prefix2.append(prefix2[-1] + x * x)
    INF = None
    E: List[List] = [[INF] * (B + 1) for _ in range(n + 1)]
    T = [[0] * (B + 1) for _ in range(n + 1)]
    E[0][0] = Fraction(0)  # @line L2
    for b in range(1, B + 1):  # @line L3
        for j in range(b, n + 1):  # @line L4
            best, arg = INF, 0
            for i in range(b - 1, j):  # @line L5
                if E[i][b - 1] is INF:
                    continue
                c = E[i][b - 1] + sse(prefix, prefix2, i, j)  # @line L6
                if best is INF or c < best:  # @line L7
                    best, arg = c, i
            E[j][b], T[j][b] = best, arg  # @line L8
    groups, j = [], n
    for b in range(B, 0, -1):  # @line L9
        i = T[j][b]
        groups.append((i, j))
        j = i
    groups.reverse()
    return E[n][B], groups  # @line L10


class Histogram:
    def __init__(self, buckets: Sequence[Bucket] = ()) -> None:
        self.buckets: List[Bucket] = list(buckets)

    @classmethod
    def equi_width(cls, values: Sequence[int], B: int) -> "Histogram":
        if not values:
            return cls()
        lo, hi = min(values), max(values)
        width = -(-(hi - lo + 1) // B)
        cnt: Counter = Counter()
        dist: Dict[int, set] = {}
        for v in values:
            k = (v - lo) // width
            cnt[k] += 1
            dist.setdefault(k, set()).add(v)
        out = []
        for k in range(B):
            a = lo + k * width
            if a > hi:
                break
            out.append((a, min(hi, a + width - 1), cnt[k], len(dist.get(k, ()))))
        return cls(out)

    @classmethod
    def equi_depth(cls, values: Sequence[int], B: int) -> "Histogram":
        """Consecutive groups of d = ceil(N / B) sorted tuples. A value that
        occurs often can be split between two buckets, so neighbouring
        buckets may share an end value: hi of one bucket <= lo of the next."""
        s = sorted(values)
        if not s:
            return cls()
        d = -(-len(s) // B)
        out: List[Bucket] = []
        for k in range(0, len(s), d):
            part = s[k:k + d]
            out.append((part[0], part[-1], len(part), len(set(part))))
        return cls(out)

    @classmethod
    def v_optimal(cls, values: Sequence[int], B: int) -> "Histogram":
        """Buckets of contiguous distinct values that minimize the sum of the
        squared errors of the frequencies (V-optimal, serial in value order)."""
        freq = sorted(Counter(values).items())
        if not freq:
            return cls()
        _, groups = v_optimal_partition([c for _, c in freq], B)
        out = []
        for i, j in groups:
            part = freq[i:j]
            out.append((part[0][0], part[-1][0], sum(c for _, c in part), j - i))
        return cls(out)

    def check_invariant(self, values: Sequence[int]) -> None:
        """Buckets are sorted, hi of one <= lo of the next, the counts add up
        to N, and each bucket holds every tuple strictly inside its range and
        no tuple outside it."""
        for (lo, hi, c, d) in self.buckets:
            assert lo <= hi and 0 <= d <= c and d <= hi - lo + 1
            inside = sum(1 for v in values if lo < v < hi)
            closed = sum(1 for v in values if lo <= v <= hi)
            assert inside <= c <= closed
        for x, y in zip(self.buckets, self.buckets[1:]):
            assert x[1] <= y[0]
        assert sum(b[2] for b in self.buckets) == len(values)

    def estimate_range(self, a: int, b: int) -> Fraction:
        """Estimated number of tuples with a <= value <= b."""
        total = Fraction(0)
        for lo, hi, c, _ in self.buckets:
            x, y = max(a, lo), min(b, hi)
            if x <= y:
                total += Fraction(c * (y - x + 1), hi - lo + 1)
        return total

    def estimate_eq(self, v: int) -> Fraction:
        """Estimated number of tuples with value = v: count / distinct in
        each bucket whose range holds v (uniform frequency)."""
        return sum((Fraction(c, d) for lo, hi, c, d in self.buckets if lo <= v <= hi and d), Fraction(0))


class EndBiased:
    """Keep the exact frequency of the h most frequent and l least frequent
    values, h + l = B - 1, chosen to minimize the squared error of the rest;
    all other values share one bucket with their average frequency."""

    def __init__(self, values: Sequence[int], B: int) -> None:
        freq = sorted(Counter(values).items(), key=lambda t: (t[1], t[0]))
        n, k = len(freq), min(B - 1, len(freq))
        best = None
        for h in range(k + 1):
            l = k - h
            rest = freq[l:n - h]
            err = Fraction(0)
            if rest:
                m = Fraction(sum(c for _, c in rest), len(rest))
                err = sum((c - m) ** 2 for _, c in rest)
            if best is None or err < best[0]:
                best = (err, h, l)
        _, h, l = best
        self.single: Dict[int, int] = dict(freq[:l] + freq[n - h:])
        rest = freq[l:n - h]
        self.rest_values = {v for v, _ in rest}
        self.rest_avg = Fraction(sum(c for _, c in rest), len(rest)) if rest else Fraction(0)
        self.error = best[0]

    def estimate_eq(self, v: int) -> Fraction:
        if v in self.single:
            return Fraction(self.single[v])
        return self.rest_avg if v in self.rest_values else Fraction(0)


def exact_range(values: Sequence[int], a: int, b: int) -> int:
    s = sorted(values)
    return bisect_right(s, b) - bisect_left(s, a)
