# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learned-index/. The authors are listed in prov/935TPJ.jsonl.

"""A two-stage recursive model index (RMI) over a sorted array of distinct keys.

Stage 1 is one linear model fitted by least squares to (key, position) over
all keys; it routes a key to one of M stage-2 models. Each stage-2 model is a
linear model fitted by least squares to the keys routed to it. Each stage-2
model stores the smallest and largest error, position minus prediction, over
its own keys. A lookup predicts a position and runs a binary search only in
the window [prediction + err_lo, prediction + err_hi].

All arithmetic is exact (Fraction), so the stored bounds hold exactly.
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple

Line = Tuple[Fraction, Fraction]   # (slope, intercept)


def fit_line(xs: Sequence[int], ys: Sequence[int]) -> Line:
    """Exact least squares line y = a x + b. Constant x gives slope 0."""
    n = len(xs)
    if n == 0:
        return Fraction(0), Fraction(0)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    den = n * sxx - sx * sx
    a = Fraction(n * sxy - sx * sy, den) if den != 0 else Fraction(0)
    b = Fraction(sy) / n - a * Fraction(sx) / n
    return a, b


def _floor(q: Fraction) -> int:
    return q.numerator // q.denominator


class RMI:
    def __init__(self, keys: Sequence[int], m: int) -> None:
        if m < 1:
            raise ValueError("need at least one stage-2 model")
        k = list(keys)
        if any(k[i] >= k[i + 1] for i in range(len(k) - 1)):
            raise ValueError("keys must be sorted and distinct")
        self.keys = k
        self.n = len(k)
        self.m = m
        pos = list(range(self.n))
        self.root = fit_line(k, pos)                                      # @line L1
        parts: List[List[int]] = [[] for _ in range(m)]
        for i, key in enumerate(k):
            parts[self.route(key)].append(i)                              # @line L2
        self.models: List[Optional[Line]] = []
        self.err: List[Tuple[int, int]] = []
        for part in parts:                                                # @line L3
            if not part:
                self.models.append(None)
                self.err.append((0, -1))
                continue
            line = fit_line([k[i] for i in part], part)                   # @line L3
            errs = [i - self._predict(line, k[i]) for i in part]          # @line L4
            self.models.append(line)
            self.err.append((min(errs), max(errs)))                       # @line L4

    @staticmethod
    def _predict(line: Line, key: int) -> int:
        a, b = line
        return _floor(a * key + b)

    def route(self, key: int) -> int:
        """Stage 1: the index of the stage-2 model for key."""
        if self.n == 0:
            return 0
        a, b = self.root
        j = _floor(self.m * (a * key + b) / self.n)                       # @line L5
        return max(0, min(self.m - 1, j))                                 # @line L5

    def window(self, key: int) -> Optional[Tuple[int, int]]:
        """The search window [lo, hi] for key, or None if its model is empty."""
        j = self.route(key)
        line = self.models[j]
        if line is None:                                                  # @line L6
            return None                                                   # @line L6
        p = self._predict(line, key)                                      # @line L7
        lo_e, hi_e = self.err[j]
        lo = max(0, p + lo_e)                                             # @line L8
        hi = min(self.n - 1, p + hi_e)                                    # @line L8
        return lo, hi

    def lookup(self, key: int) -> Optional[int]:
        """The position of key in the sorted array, or None if absent."""
        w = self.window(key)
        if w is None:
            return None
        lo, hi = w
        while lo <= hi:                                                   # @line L9
            mid = (lo + hi) // 2                                          # @line L9
            if self.keys[mid] < key:                                      # @line L9
                lo = mid + 1                                              # @line L9
            elif self.keys[mid] > key:                                    # @line L9
                hi = mid - 1                                              # @line L9
            else:
                return mid                                                # @line L10
        return None                                                       # @line L10

    def max_window(self) -> int:
        return max((hi - lo + 1 for lo, hi in self.err), default=0)
