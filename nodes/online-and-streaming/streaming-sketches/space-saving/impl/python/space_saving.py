# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-saving/. The authors are listed in prov/3PR4D2.jsonl.

from collections.abc import Hashable, Iterable


class SpaceSaving:
    """The Space-Saving summary with k counters (k >= 1).

    After m items, with mu = min_count() (0 while fewer than k items are
    monitored), every item x satisfies f_x <= estimate(x) <= f_x + mu and
    mu <= m / k. Monitored items also keep err[x], and count[x] - err[x] is a
    lower bound of f_x. The counters are kept in buckets of equal value (the
    Stream-Summary idea), so an update takes O(1) expected time.
    """

    def __init__(self, k: int) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k
        self.m = 0
        self.count: dict[Hashable, int] = {}
        self.err: dict[Hashable, int] = {}
        self._buckets: dict[int, set[Hashable]] = {}
        self._min = 0
        self._floor = 0  # the value of unmonitored items in a merged summary
        self.delta_bound = 0  # the proved bound on estimate(x) - f_x
        self._merged = False

    # bucket helpers
    def _bucket_add(self, x: Hashable, c: int) -> None:
        self._buckets.setdefault(c, set()).add(x)

    def _bucket_remove(self, x: Hashable, c: int) -> None:
        b = self._buckets[c]
        b.discard(x)
        if not b:
            del self._buckets[c]

    def min_count(self) -> int:
        """mu: the smallest counter when k items are monitored, else the floor."""
        if len(self.count) < self.k:
            return self._floor
        while self._min not in self._buckets:
            self._min += 1
        return self._min

    def update(self, x: Hashable) -> None:
        """Process one occurrence of item x."""
        if self._merged:
            raise ValueError("a merged summary supports queries and merges only")
        self.m += 1  # @line L1
        if x in self.count:  # @line L2
            c = self.count[x]
            self._bucket_remove(x, c)
            self.count[x] = c + 1  # @line L3
            self._bucket_add(x, c + 1)
        elif len(self.count) < self.k:  # @line L4
            self.count[x] = 1  # @line L5
            self.err[x] = 0  # @line L5
            self._bucket_add(x, 1)
            self._min = 1  # the new counter is the smallest one
        else:
            mu = self.min_count()  # @line L6
            y = next(iter(self._buckets[mu]))  # @line L6
            self._bucket_remove(y, mu)
            del self.count[y]  # @line L7
            del self.err[y]  # @line L7
            self.count[x] = mu + 1  # @line L8
            self.err[x] = mu  # @line L8
            self._bucket_add(x, mu + 1)
        self.delta_bound = self.min_count()

    def extend(self, stream: Iterable[Hashable]) -> None:
        for x in stream:
            self.update(x)

    def estimate(self, x: Hashable) -> int:
        """An upper estimate of f_x."""
        if x in self.count:  # @line L9
            return self.count[x]  # @line L9
        return self.min_count()  # @line L10

    def guaranteed(self, x: Hashable) -> int:
        """A lower bound of f_x: count[x] - err[x] for a monitored item, else 0."""
        if x in self.count:
            return self.count[x] - self.err[x]
        return 0

    def top(self, j: int) -> list[tuple[Hashable, int]]:
        """The j monitored items with the largest counters, largest first."""
        return sorted(self.count.items(), key=lambda t: -t[1])[:j]

    def to_misra_gries(self) -> dict[Hashable, int]:
        """The Misra-Gries summary with k - 1 counters of the same stream.

        For a summary built by updates, this is max(count[x] - mu, 0) for each
        monitored x (the isomorphism of Agarwal et al. 2012). For a merged
        summary, it is the stored Misra-Gries part.
        """
        if self._merged:
            return {x: c - self._floor for x, c in self.count.items()}
        mu = self.min_count()
        return {x: c - mu for x, c in self.count.items() if c > mu}

    def merge(self, other: "SpaceSaving") -> "SpaceSaving":
        """Return a summary of the concatenation of the two streams.

        Both summaries are mapped to Misra-Gries summaries, these are merged,
        and D = (m - sum of the merged counters) // k is added back. Then
        f_x <= estimate(x) <= f_x + D and D <= m / k. The result supports
        queries and further merges. Cost: O(k log k).
        """
        if other.k != self.k:
            raise ValueError("the summaries must have the same k")
        k = self.k
        combined = self.to_misra_gries()
        for y, v in other.to_misra_gries().items():
            combined[y] = combined.get(y, 0) + v
        if len(combined) >= k:
            c_k = sorted(combined.values(), reverse=True)[k - 1]
            combined = {y: v - c_k for y, v in combined.items() if v > c_k}
        out = SpaceSaving(k)
        out._merged = True
        out.m = self.m + other.m
        d = (out.m - sum(combined.values())) // k
        for x, v in combined.items():
            out.count[x] = v + d
            out.err[x] = d
            out._bucket_add(x, v + d)
        out._floor = d
        out.delta_bound = d
        return out
