# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lhd/. The authors are listed in prov/VC0D27.jsonl.

import random
from collections.abc import Hashable, Iterable
from fractions import Fraction


class LHD:
    """Least hit density of Beckmann, Chen and Cidon (NSDI 2018).

    The cache holds objects of integer sizes up to `capacity` bytes. Time is
    the number of requests. The age of an object is the time since its last
    reference, coarsened into `ages` bins of `coarseness` requests; the last
    bin holds every older age. The class of an object is its number of
    references since it entered the cache, capped at `classes`. For each
    class the policy counts hits and lifetimes (hits plus evictions) by age.
    Every `interval` requests it folds the new counts into the old ones with
    weight `decay` and recomputes, for each class k and age bin a,

        rank[k][a] = sum_{e >= a} H[k][e] / sum_{e >= a} (e - a + 1) * L[k][e],

    which is Eq. 6 of the paper on this discrete grid. The hit density of an
    object is rank / size. On eviction the policy samples `samples` objects
    and evicts the one of least hit density; ties go to the older object.
    """

    def __init__(self, capacity: int, samples: int = 64, classes: int = 4, ages: int = 64,
                 coarseness: int | None = None, interval: int = 1000,
                 decay: Fraction = Fraction(9, 10), seed: int = 0) -> None:
        if capacity < 1 or samples < 1 or classes < 1 or ages < 1 or interval < 1:
            raise ValueError("bad parameter")
        self.capacity = capacity
        self.samples = samples
        self.classes = classes
        self.ages = ages
        self.coarseness = coarseness or max(1, capacity // 4)  # ages up to 16 * capacity
        self.interval = interval
        self.decay = Fraction(decay)
        self.rng = random.Random(seed)
        self.t = 0
        self.used = 0
        self.size: dict[Hashable, int] = {}
        self.last: dict[Hashable, int] = {}
        self.refs: dict[Hashable, int] = {}
        self.keys: list[Hashable] = []
        self.pos: dict[Hashable, int] = {}
        zero = lambda: [[Fraction(0)] * ages for _ in range(classes)]
        self.hits, self.lives = zero(), zero()  # decayed histograms
        self.new_hits = [[0] * ages for _ in range(classes)]
        self.new_lives = [[0] * ages for _ in range(classes)]
        self.rank = zero()
        self.evicted: list[Hashable] = []

    def __contains__(self, x: Hashable) -> bool:
        return x in self.size

    def __len__(self) -> int:
        return len(self.keys)

    def age(self, x: Hashable) -> int:
        return min((self.t - self.last[x]) // self.coarseness, self.ages - 1)

    def cls(self, x: Hashable) -> int:
        return min(self.refs[x], self.classes) - 1

    def density(self, x: Hashable) -> Fraction:
        return self.rank[self.cls(x)][self.age(x)] / self.size[x]

    def access(self, x: Hashable, size: int = 1) -> bool:
        """Serve one request for x of the given size. Return True on a hit."""
        self.evicted = []
        self.t += 1  # @line L1
        if x in self.size:  # @line L2
            k, a = self.cls(x), self.age(x)
            self.new_hits[k][a] += 1  # @line L3
            self.new_lives[k][a] += 1
            self.last[x] = self.t  # @line L4
            self.refs[x] += 1
            hit = True
        elif size > self.capacity:  # @line L5
            hit = False
        else:
            while self.used + size > self.capacity:  # @line L6
                cand = [self.keys[i] for i in self.rng.sample(range(len(self.keys)), min(self.samples, len(self.keys)))]  # @line L7
                v = min(cand, key=lambda y: (self.density(y), self.last[y]))  # @line L8
                self.new_lives[self.cls(v)][self.age(v)] += 1  # @line L9
                self._remove(v)
                self.evicted.append(v)
            self.size[x], self.last[x], self.refs[x] = size, self.t, 1  # @line L10
            self.used += size
            self.pos[x] = len(self.keys)
            self.keys.append(x)
            hit = False
        if self.t % self.interval == 0:  # @line L11
            self.reconfigure()
        return hit

    def reconfigure(self) -> None:
        for k in range(self.classes):
            for a in range(self.ages):  # @line L12
                self.hits[k][a] = self.decay * self.hits[k][a] + self.new_hits[k][a]
                self.lives[k][a] = self.decay * self.lives[k][a] + self.new_lives[k][a]
                self.new_hits[k][a] = self.new_lives[k][a] = 0
            hits_above = lives_above = weighted = Fraction(0)
            for a in range(self.ages - 1, -1, -1):  # @line L13
                hits_above += self.hits[k][a]
                lives_above += self.lives[k][a]
                weighted += lives_above  # sum over e >= a of (e - a + 1) * L[e]
                self.rank[k][a] = hits_above / weighted if weighted else Fraction(0)  # @line L14

    def _remove(self, v: Hashable) -> None:
        i, last = self.pos.pop(v), self.keys.pop()
        if last != v:
            self.keys[i] = last
            self.pos[last] = i
        self.used -= self.size.pop(v)
        del self.last[v], self.refs[v]


def lhd_hits(trace: Iterable[tuple[Hashable, int]], capacity: int, **options) -> list[bool]:
    """Run LHD on (key, size) requests. Return one hit flag per request."""
    cache = LHD(capacity, **options)
    return [cache.access(x, s) for x, s in trace]
