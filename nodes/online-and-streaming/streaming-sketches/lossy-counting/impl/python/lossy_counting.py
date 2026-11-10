# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossy-counting/. The authors are listed in prov/1P92W2.jsonl.

from collections.abc import Hashable, Iterable
from fractions import Fraction


class LossyCounting:
    """Lossy counting of Manku and Motwani with bucket width w.

    With w = ceil(1/eps), after N items each entry (f, delta) satisfies
    f <= f_x <= f + delta, every item without an entry has f_x <= N // w,
    and so f_x - estimate(x) <= N // w <= eps * N. After the pruning at the
    end of bucket B there are at most w * H_B entries (H_B the harmonic
    number). Entries are grouped by the key f + delta, so the pruning removes
    one group and each update takes O(1) amortized expected time.
    """

    def __init__(self, eps: Fraction | float | None = None, w: int | None = None) -> None:
        if w is None:
            if eps is None or not 0 < eps <= 1:
                raise ValueError("give eps in (0, 1] or a bucket width w >= 1")
            w = -int(-1 // Fraction(eps))  # ceil(1/eps), exact for a Fraction
        if w < 1:
            raise ValueError("w must be at least 1")
        self.w = w
        self.n = 0
        self.f: dict[Hashable, int] = {}
        self.delta: dict[Hashable, int] = {}
        self._by_key: dict[int, set[Hashable]] = {}

    def _move(self, x: Hashable, old: int | None, new: int) -> None:
        if old is not None:
            s = self._by_key[old]
            s.discard(x)
            if not s:
                del self._by_key[old]
        self._by_key.setdefault(new, set()).add(x)

    def update(self, x: Hashable) -> None:
        """Process one occurrence of item x."""
        self.n += 1  # @line L1
        b = -(-self.n // self.w)  # @line L2
        if x in self.f:  # @line L3
            key = self.f[x] + self.delta[x]
            self.f[x] += 1  # @line L3
            self._move(x, key, key + 1)
        else:
            self.f[x] = 1  # @line L4
            self.delta[x] = b - 1  # @line L4
            self._move(x, None, b)
        if self.n % self.w == 0:  # @line L5
            # Every key is at least b here, so the keys <= b are exactly key b.
            for y in self._by_key.pop(b, ()):  # @line L6
                del self.f[y]  # @line L6
                del self.delta[y]

    def extend(self, stream: Iterable[Hashable]) -> None:
        for x in stream:
            self.update(x)

    def estimate(self, x: Hashable) -> int:
        """A lower estimate of f_x, low by at most N // w."""
        return self.f.get(x, 0)  # @line L7

    def upper(self, x: Hashable) -> int:
        """An upper estimate of f_x: f + delta for an entry, else the bound N // w."""
        if x in self.f:
            return self.f[x] + self.delta[x]
        return self.n // self.w

    def report(self, s: Fraction | float) -> list[Hashable]:
        """Items with f >= (s - 1/w) N, with 1/w playing the role of eps.

        For a support s > 1/w, this list holds every item with f_x >= s N
        and no item with f_x < (s - 1/w) N.
        """
        t = (Fraction(s) - Fraction(1, self.w)) * self.n
        return [x for x, c in self.f.items() if c >= t]  # @line L8

    def __len__(self) -> int:
        return len(self.f)
