# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-decay/. The authors are listed in prov/SAPQHG.jsonl.
"""Forward-decayed count, sum, average and max, with landmark moves and merges."""

from typing import Callable, Optional


class ForwardDecayed:
    """Weights g(t_i - L) / g(t - L) for a positive non-decreasing g and a landmark L.

    The numerators are fixed when an item arrives; the divisor g(t - L) is
    applied only at query time.
    """

    def __init__(self, g: Callable, landmark=0) -> None:
        self.g = g
        self.landmark = landmark
        self.nc = 0  # sum of g(t_i - L)
        self.ns = 0  # sum of g(t_i - L) x_i
        self.nmax: Optional[object] = None  # max of g(t_i - L) x_i

    def add(self, t, x=1) -> None:
        if t < self.landmark:
            raise ValueError("items must not be older than the landmark")
        w = self.g(t - self.landmark)
        self.nc += w
        self.ns += w * x
        wx = w * x
        self.nmax = wx if self.nmax is None or wx > self.nmax else self.nmax

    def count(self, t):
        return self.nc / self.g(t - self.landmark)

    def total(self, t):
        return self.ns / self.g(t - self.landmark)

    def max(self, t):
        return None if self.nmax is None else self.nmax / self.g(t - self.landmark)

    def average(self):
        """The decayed average; the divisor cancels, so it does not depend on t."""
        return self.ns / self.nc

    def move_landmark(self, new_landmark, scale) -> None:
        """For g(n) = b^n only: pass scale = b^(L - L') to keep every query unchanged."""
        self.nc *= scale
        self.ns *= scale
        if self.nmax is not None:
            self.nmax *= scale
        self.landmark = new_landmark

    def merge(self, other: "ForwardDecayed") -> "ForwardDecayed":
        """Merge two summaries of disjoint items with the same g and landmark."""
        if other.landmark != self.landmark:
            raise ValueError("move both summaries to one landmark first")
        out = ForwardDecayed(self.g, self.landmark)
        out.nc = self.nc + other.nc
        out.ns = self.ns + other.ns
        maxes = [m for m in (self.nmax, other.nmax) if m is not None]
        out.nmax = max(maxes) if maxes else None
        return out
