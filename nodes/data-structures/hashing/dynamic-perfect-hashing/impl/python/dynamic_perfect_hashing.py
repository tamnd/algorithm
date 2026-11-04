# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-perfect-hashing/. The authors are listed in prov/F7B69T.jsonl.

import random

P61 = (1 << 61) - 1  # a Mersenne prime
SIGMA = 512  # the bound of line L8: total second-level slots at most SIGMA * M
SIGMA0 = 64  # the bound of line L22


def h_ab(a: int, b: int, p: int, m: int, x: int) -> int:
    """The Carter-Wegman hash ((a x + b) mod p) mod m."""
    return ((a * x + b) % p) % m


class DynamicPerfectHash:
    """A dynamic two-level perfect hash table for integer keys in [0, p).

    Search reads one slot: O(1) time in the worst case. Insert and delete
    take O(1) expected amortized time. The space is O(n + 1) words in every
    state. The random choices come from rng, so a test can fix them.
    """

    def __init__(self, rng: random.Random | None = None, p: int = P61) -> None:
        self.rng = rng if rng is not None else random.Random()
        self.p = p
        self.rehash_all(set())

    # ----------------------------------------------------------- search
    def search(self, x: int) -> bool:
        j = h_ab(self.a, self.b, self.p, self.M, x)  # @line L14
        a_j, b_j = self.params[j]
        return self.tables[j][h_ab(a_j, b_j, self.p, len(self.tables[j]), x)] == x  # @line L15

    # ----------------------------------------------------------- updates
    def insert(self, x: int) -> None:
        if not 0 <= x < self.p:
            raise ValueError("key out of range")
        if self.search(x):  # @line L1
            return
        self.u += 1  # @line L2
        if self.u > (self.M + 1) // 2:  # @line L3
            self.rehash_all(self.keys() | {x})
            return
        j = h_ab(self.a, self.b, self.p, self.M, x)  # @line L4
        self.buckets[j].add(x)
        self.c[j] += 1
        t = self.tables[j]
        i = self._slot(j, x)
        if self.c[j] <= self.L[j] and t[i] is None:  # @line L5
            t[i] = x
            return
        if self.c[j] > self.L[j] and len(self.buckets[j]) > self.L[j] / 2:  # @line L6
            self.space += 6 * self.L[j] ** 2  # 2 (2L)^2 - 2 L^2
            self.L[j] *= 2  # @line L7
            if self.space > SIGMA * self.M:  # @line L8
                self.rehash_all(self.keys())
                return
        self.rebuild_bucket(j)  # @line L9

    def delete(self, x: int) -> None:
        if not 0 <= x < self.p or not self.search(x):  # @line L10
            return
        self.u += 1  # @line L11
        if self.u > (self.M + 1) // 2:  # @line L12
            self.rehash_all(self.keys() - {x})
            return
        j = h_ab(self.a, self.b, self.p, self.M, x)  # @line L13
        self.tables[j][self._slot(j, x)] = None
        self.buckets[j].discard(x)

    # ----------------------------------------------------------- rebuilds
    def _slot(self, j: int, x: int) -> int:
        a_j, b_j = self.params[j]
        return h_ab(a_j, b_j, self.p, len(self.tables[j]), x)

    def rebuild_bucket(self, j: int) -> None:
        size = 2 * self.L[j] ** 2
        if len(self.tables[j]) != size:  # @line L16
            self.tables[j] = [None] * size
        else:
            t = self.tables[j]
            for y in self.buckets[j]:  # by (D2) only these slots can be in use
                t[self._slot(j, y)] = None
        t = self.tables[j]
        keys = list(self.buckets[j])
        while True:
            a_j, b_j = self.rng.randrange(1, self.p), self.rng.randrange(self.p)  # @line L17
            slots = [h_ab(a_j, b_j, self.p, size, x) for x in keys]
            if len(set(slots)) == len(slots):  # @line L18
                break
        self.params[j] = (a_j, b_j)
        for x, i in zip(keys, slots):  # @line L19
            t[i] = x
        self.c[j] = len(keys)

    def rehash_all(self, s: set[int]) -> None:
        self.M = max(len(s), 1)  # @line L20
        self.u = 0
        while True:
            self.a, self.b = self.rng.randrange(1, self.p), self.rng.randrange(self.p)  # @line L21
            self.buckets = [set() for _ in range(self.M)]
            for x in s:
                self.buckets[h_ab(self.a, self.b, self.p, self.M, x)].add(x)
            if sum(8 * max(len(b), 1) ** 2 for b in self.buckets) <= SIGMA0 * self.M:  # @line L22
                break
        self.L = [2 * max(len(b), 1) for b in self.buckets]  # @line L23
        self.space = sum(2 * l * l for l in self.L)  # kept equal to the sum of line L8
        self.c = [0] * self.M
        self.params = [(1, 0)] * self.M
        self.tables: list[list[int | None]] = [[] for _ in range(self.M)]
        for j in range(self.M):
            self.rebuild_bucket(j)

    # ----------------------------------------------------------- helpers
    def keys(self) -> set[int]:
        out: set[int] = set()
        for b in self.buckets:
            out |= b
        return out

    def __len__(self) -> int:
        return sum(len(b) for b in self.buckets)

    def check_invariant(self) -> None:
        """Assert (D1) to (D5) of the page."""
        n = len(self)
        assert len(self.buckets) == self.M == len(self.tables) == len(self.L)
        for j, b in enumerate(self.buckets):
            assert all(h_ab(self.a, self.b, self.p, self.M, x) == j for x in b)  # (D1)
            t = self.tables[j]
            assert len(t) == 2 * self.L[j] ** 2
            stored = [x for x in t if x is not None]
            assert sorted(stored) == sorted(b)  # (D2)
            assert all(t[self._slot(j, x)] == x for x in b)
            assert len(b) <= self.c[j] <= self.L[j]  # (D3)
        assert sum(len(t) for t in self.tables) == self.space <= SIGMA * self.M  # (D4)
        assert self.u <= (self.M + 1) // 2  # (D5)
        assert self.M <= 2 * n + 1
