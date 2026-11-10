# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/misra-gries-summary/. The authors are listed in prov/6P4C0W.jsonl.

from collections.abc import Hashable, Iterable


class MisraGries:
    """The Misra-Gries summary with k - 1 counters (k >= 2).

    After m items, each estimate satisfies f_x - m/k <= estimate(x) <= f_x,
    and more exactly f_x - estimate(x) <= (m - sum of counters) / k.
    Space: at most k - 1 (item, counter) pairs. Update: O(k) worst case,
    O(1) amortized (with O(1) dictionary operations). Query: O(1).
    """

    def __init__(self, k: int) -> None:
        if k < 2:
            raise ValueError("k must be at least 2")
        self.k = k
        self.m = 0
        self.counters: dict[Hashable, int] = {}

    def update(self, x: Hashable) -> None:
        """Process one occurrence of item x."""
        self.m += 1  # @line L1
        c = self.counters
        if x in c:  # @line L2
            c[x] += 1  # @line L2
        elif len(c) < self.k - 1:  # @line L3
            c[x] = 1  # @line L3
        else:
            for y in list(c):  # @line L4
                c[y] -= 1  # @line L5
                if c[y] == 0:  # @line L6
                    del c[y]  # @line L6

    def extend(self, stream: Iterable[Hashable]) -> None:
        for x in stream:
            self.update(x)

    def estimate(self, x: Hashable) -> int:
        """Return the lower estimate of f_x."""
        return self.counters.get(x, 0)  # @line L7

    def merge(self, other: "MisraGries") -> "MisraGries":
        """Return a summary of the concatenation of the two streams.

        Both summaries must have the same k. The result has at most k - 1
        counters and the same error guarantee for the combined length.
        Cost: O(k log k) for the sort.
        """
        if other.k != self.k:
            raise ValueError("the summaries must have the same k")
        out = MisraGries(self.k)
        out.m = self.m + other.m
        combined = dict(self.counters)  # @line L8
        for y, v in other.counters.items():  # @line L8
            combined[y] = combined.get(y, 0) + v  # @line L8
        if len(combined) >= self.k:  # @line L9
            c_k = sorted(combined.values(), reverse=True)[self.k - 1]  # @line L10
            combined = {y: v - c_k for y, v in combined.items() if v > c_k}  # @line L11
        out.counters = combined  # @line L12
        return out

    def heavy_candidates(self) -> list[Hashable]:
        """Items that may occur more than m/k times; it contains every such item."""
        return list(self.counters)
