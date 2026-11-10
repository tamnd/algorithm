# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sticky-sampling/. The authors are listed in prov/VTF6WC.jsonl.

import math
import random
from collections.abc import Hashable, Iterable


class StickySampling:
    """Sticky sampling of Manku and Motwani, with an exact change of rate.

    Parameters: support s, error eps < s, failure probability delta, and a
    random.Random. With t = (1/eps) ln(1/(s delta)), the sampling rate r is 1
    for the first 2t items, 2 for the next 2t, 4 for the next 4t, and so on.
    At any time, the table has the same distribution as if each occurrence
    had been sampled with probability 1/r from the start, and an entry
    counts the occurrences from its first sampled one. So estimates are never
    too large, report(...) meets the guarantee with probability >= 1 - delta,
    and the expected number of entries is at most N / r <= 2t.

    With paper_rule=True, the change of rate tosses fair coins as in the
    paper. Then the table is not in the state above after the second change,
    and the expected number of entries can be larger than 2t.
    """

    def __init__(
        self,
        s: float,
        eps: float,
        delta: float,
        rng: random.Random,
        paper_rule: bool = False,
    ) -> None:
        if not (0 < eps < s < 1 and 0 < delta < 1):
            raise ValueError("need 0 < eps < s < 1 and 0 < delta < 1")
        self.s, self.eps, self.delta = s, eps, delta
        self.t = math.log(1 / (s * delta)) / eps
        self.rng = rng
        self.paper_rule = paper_rule
        self.n = 0
        self.r = 1
        self.f: dict[Hashable, int] = {}

    def _geometric_failures(self, p: float, limit: int) -> int:
        """The number of failures before the first success, each try with
        success probability p, cut at limit."""
        if p >= 1:
            return 0
        u = self.rng.random()
        k = int(math.log(1.0 - u) / math.log(1.0 - p))
        return min(k, limit)

    def _change_rate(self) -> None:
        new_r = 2 * self.r
        for x in list(self.f):  # @line L6
            c = self.f[x]
            if self.paper_rule:
                while c > 0 and self.rng.random() < 0.5:  # tails: one less
                    c -= 1
            elif self.rng.random() >= 0.5:  # @line L7
                # The first counted occurrence is not sampled at the new rate,
                # and each later one is sampled with probability 1/new_r.
                c -= 1 + self._geometric_failures(1 / new_r, c - 1)  # @line L8
            if c == 0:  # @line L9
                del self.f[x]  # @line L9
            else:
                self.f[x] = c
        self.r = new_r

    def update(self, x: Hashable) -> None:
        """Process one occurrence of item x."""
        self.n += 1  # @line L1
        while self.n > 2 * self.r * self.t:  # @line L2
            self._change_rate()  # @line L3
        if x in self.f:  # @line L4
            self.f[x] += 1  # @line L4
        elif self.rng.random() < 1 / self.r:  # @line L5
            self.f[x] = 1  # @line L5

    def extend(self, stream: Iterable[Hashable]) -> None:
        for x in stream:
            self.update(x)

    def estimate(self, x: Hashable) -> int:
        """A lower estimate of f_x."""
        return self.f.get(x, 0)  # @line L10

    def report(self) -> list[Hashable]:
        """The entries with f >= (s - eps) N."""
        threshold = (self.s - self.eps) * self.n
        return [x for x, c in self.f.items() if c >= threshold]  # @line L11

    def __len__(self) -> int:
        return len(self.f)
