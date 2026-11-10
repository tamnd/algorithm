# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-marking/. The authors are listed in prov/6JHBAR.jsonl.

import random
from collections.abc import Hashable, Sequence
from fractions import Fraction


class RandomizedMarking:
    """An online randomized marking cache of size k.

    The array unmarked holds the cached pages not yet requested in the current
    phase, and pos maps each of them to its index, so a removal is a swap with
    the last element. Cost per request: O(1) expected time, plus O(k) at the
    start of a phase, which a phase pays with its at least k requests.
    """

    def __init__(self, k: int, rng: random.Random) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k
        self.rng = rng
        self.cache: set[Hashable] = set()  # @line L1
        self.unmarked: list[Hashable] = []
        self.pos: dict[Hashable, int] = {}
        self.faults = 0

    def _remove_unmarked(self, q: Hashable) -> None:
        i = self.pos.pop(q)
        last = self.unmarked.pop()
        if last != q:
            self.unmarked[i] = last
            self.pos[last] = i

    def request(self, p: Hashable) -> Hashable | None:
        """Serve a request for p. Return the evicted page, or None."""
        victim = None
        if p not in self.cache:  # @line L4
            self.faults += 1  # @line L5
            if len(self.cache) == self.k:  # @line L6
                if not self.unmarked:  # @line L7
                    self.unmarked = list(self.cache)
                    self.pos = {q: i for i, q in enumerate(self.unmarked)}
                victim = self.unmarked[self.rng.randrange(len(self.unmarked))]  # @line L8
                self._remove_unmarked(victim)  # @line L9
                self.cache.remove(victim)
            self.cache.add(p)  # @line L10
        elif p in self.pos:  # @line L11
            self._remove_unmarked(p)
        return victim


def randomized_marking(sigma: Sequence[Hashable], k: int, rng: random.Random) -> int:
    """Return the faults of one run of randomized marking on sigma.

    Precondition: k >= 1 and the pages are hashable. The cache starts empty.
    Cost: O(n) expected time and O(k) space, with n = len(sigma).
    """
    cache = RandomizedMarking(k, rng)
    for p in sigma:  # @line L2
        cache.request(p)  # @line L3
    return cache.faults  # @line L12


def expected_faults_exact(sigma: Sequence[Hashable], k: int) -> Fraction:
    """Return the exact expected number of faults, over all random choices.

    The state is the pair (cache, unmarked cached pages) with its probability.
    Cost: exponential in k in the worst case; for small inputs only.
    """
    states: dict[tuple[frozenset, frozenset], Fraction] = {(frozenset(), frozenset()): Fraction(1)}
    total = Fraction(0)
    for p in sigma:
        new: dict[tuple[frozenset, frozenset], Fraction] = {}
        for (c, u), pr in states.items():
            if p in c:
                outs = [((c, u - {p}), pr)]
            else:
                total += pr
                if len(c) < k:
                    outs = [((c | {p}, u), pr)]
                else:
                    if not u:
                        u = c
                    outs = [((c - {q} | {p}, u - {q}), pr / len(u)) for q in u]
            for s, q in outs:
                new[s] = new.get(s, Fraction(0)) + q
        states = new
    return total
