# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fks-perfect-hashing/. The authors are listed in prov/VWBFM0.jsonl.

import random
from dataclasses import dataclass, field

P61 = (1 << 61) - 1  # a Mersenne prime


def h_ab(a: int, b: int, p: int, m: int, x: int) -> int:
    """The Carter-Wegman hash ((a x + b) mod p) mod m."""
    return ((a * x + b) % p) % m


@dataclass
class FKSTable:
    """A two-level perfect hash table for a fixed set of keys."""

    p: int
    m: int
    a: int
    b: int
    sizes: list[int] = field(default_factory=list)  # m_j for each bucket
    params: list[tuple[int, int]] = field(default_factory=list)  # (a_j, b_j)
    slots: list[list[int | None]] = field(default_factory=list)  # T_j

    def first(self, x: int) -> int:
        return h_ab(self.a, self.b, self.p, self.m, x)

    def second(self, j: int, x: int) -> int:
        a_j, b_j = self.params[j]
        return h_ab(a_j, b_j, self.p, self.sizes[j], x)


def fks_build(keys: list[int], rng: random.Random | None = None, p: int = P61) -> FKSTable:
    """Build an FKS table for the distinct keys, each in [0, p), p prime.

    Las Vegas: the result is always correct; the expected time is O(n), and
    the second level has at most 4n slots. Raises ValueError on a duplicate
    key or a key out of range.
    """
    rng = rng if rng is not None else random.Random()
    n = len(keys)
    if len(set(keys)) != n:
        raise ValueError("duplicate key")
    if any(not 0 <= x < p for x in keys):
        raise ValueError("key out of range")
    m = max(n, 1)  # @line L1
    while True:  # @line L2
        a, b = rng.randrange(1, p), rng.randrange(p)  # @line L3
        buckets: list[list[int]] = [[] for _ in range(m)]
        for x in keys:
            buckets[h_ab(a, b, p, m, x)].append(x)  # @line L4
        if sum(len(s) ** 2 for s in buckets) <= 4 * n:  # @line L5
            break
    t = FKSTable(p, m, a, b)
    for s in buckets:  # @line L6
        m_j = len(s) ** 2  # @line L7
        slots: list[int | None] = [None] * m_j
        a_j, b_j = 1, 0
        if m_j > 0:  # @line L8
            while True:
                a_j, b_j = rng.randrange(1, p), rng.randrange(p)  # @line L9
                if _place(s, slots, a_j, b_j, p, m_j):  # @line L10
                    break  # @line L11: _place has stored each key
        t.sizes.append(m_j)
        t.params.append((a_j, b_j))
        t.slots.append(slots)
    return t


def _place(s: list[int], slots: list[int | None], a: int, b: int, p: int, m: int) -> bool:
    """Write the keys of s into slots by h_{a,b,m}; on a collision undo and return False."""
    used: list[int] = []
    for x in s:
        i = h_ab(a, b, p, m, x)
        if slots[i] is not None:
            for k in used:
                slots[k] = None
            return False
        slots[i] = x
        used.append(i)
    return True


def fks_search(t: FKSTable, x: int) -> bool:
    """Return True if x is a key of the table. O(1) time in the worst case."""
    j = t.first(x)  # @line L12
    if t.sizes[j] == 0:  # @line L13
        return False
    return t.slots[j][t.second(j, x)] == x  # @line L14
