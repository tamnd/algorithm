# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperbolic-caching/. The authors are listed in prov/NR35XD.jsonl.

import random
from collections.abc import Hashable, Iterable
from fractions import Fraction


class HyperbolicCache:
    """Hyperbolic caching of Blankstein, Sen and Freedman (USENIX ATC 2017).

    Item i has priority p_i = cost_i * n_i / (t - t_i), where n_i counts the
    requests to i since it entered the cache, t_i is the time it entered and
    t is the current time. The clock is an explicit integer that grows by one
    on every request. On a miss with a full cache, the policy samples
    `samples` distinct cached items uniformly at random, as Redis does, and
    evicts the one of least priority. Ties go to the item that entered first.
    With cost 1 for every item this is the basic policy of Fig. 1.
    """

    def __init__(self, c: int, samples: int = 64, seed: int = 0) -> None:
        if c < 1 or samples < 1:
            raise ValueError("need c >= 1 and samples >= 1")
        self.c = c
        self.samples = samples
        self.rng = random.Random(seed)
        self.t = 0
        self.n: dict[Hashable, int] = {}
        self.t_in: dict[Hashable, int] = {}
        self.cost: dict[Hashable, Fraction] = {}
        self.keys: list[Hashable] = []  # for O(1) uniform sampling
        self.pos: dict[Hashable, int] = {}
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.n

    def __len__(self) -> int:
        return len(self.keys)

    def priority(self, x: Hashable) -> Fraction:
        return self.cost[x] * Fraction(self.n[x], self.t - self.t_in[x])

    def sample(self) -> list[Hashable]:
        k = min(self.samples, len(self.keys))
        return [self.keys[i] for i in self.rng.sample(range(len(self.keys)), k)]

    def access(self, x: Hashable, cost: Fraction | int = 1) -> bool:
        """Serve one request. Return True on a hit."""
        self.evicted = None
        self.t += 1  # @line L1
        if x in self.n:  # @line L2
            self.n[x] += 1  # @line L3
            return True
        if len(self.keys) == self.c:  # @line L4
            cand = self.sample()  # @line L5
            v = min(cand, key=lambda y: (self.priority(y), self.t_in[y]))  # @line L6
            self._remove(v)  # @line L7
            self.evicted = v
        self.n[x] = 1  # @line L8
        self.t_in[x] = self.t
        self.cost[x] = Fraction(cost)
        self.pos[x] = len(self.keys)
        self.keys.append(x)
        return False  # @line L9

    def _remove(self, v: Hashable) -> None:
        i, last = self.pos.pop(v), self.keys.pop()
        if last != v:
            self.keys[i] = last
            self.pos[last] = i
        del self.n[v], self.t_in[v], self.cost[v]


def hyperbolic_hits(trace: Iterable[Hashable], c: int, samples: int = 64, seed: int = 0) -> list[bool]:
    """Run hyperbolic caching with c items and unit costs. Return one hit flag per request."""
    cache = HyperbolicCache(c, samples, seed)
    return [cache.access(x) for x in trace]
