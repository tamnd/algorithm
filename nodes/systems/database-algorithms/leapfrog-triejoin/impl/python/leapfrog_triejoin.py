# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leapfrog-triejoin/. The authors are listed in prov/R8QS9W.jsonl.

"""Leapfrog triejoin (Veldhuizen 2014).

Each relation is a lexicographically sorted list of tuples, with its columns
permuted into the global attribute order. A TrieIterator walks this list as if
it were a trie: open() goes down one level, up() goes back, and at one level
key(), next(), seek(x) and at_end() work on the sorted keys of that level.
next() and seek() use binary search, so each costs O(log n).

A leapfrog join intersects the keys of several iterators at one level: the
iterator with the smallest key seeks to the largest key, until all keys agree.
The triejoin binds one attribute per level with a leapfrog join over the
relations that hold the attribute.

stats["calls"] lists, for each leapfrog join, the tuple
(level, moves, number of iterators, fewest distinct keys of an iterator),
where moves counts the calls of seek() and next().
"""

from bisect import bisect_left, bisect_right
from collections.abc import Sequence


class TrieIterator:
    """A trie view of a sorted list of equal-length tuples."""

    def __init__(self, rows: list[tuple]):
        self.rows = rows
        self.d = -1               # depth; -1 is the root
        self.lo, self.hi, self.p = 0, len(rows), 0
        self.saved: list[tuple[int, int, int]] = []

    def _col(self, r: tuple):
        return r[self.d]

    def key(self):
        return self.rows[self.p][self.d]

    def at_end(self) -> bool:
        return self.p >= self.hi

    def next(self) -> None:
        """Move to the first row of the range with a larger key."""
        self.p = bisect_right(self.rows, self.key(), self.p, self.hi, key=self._col)

    def seek(self, x) -> None:
        """Move to the first row at or after the position with key >= x."""
        self.p = bisect_left(self.rows, x, self.p, self.hi, key=self._col)

    def open(self) -> None:
        """Go down: the new range is the rows that share the current key."""
        self.saved.append((self.lo, self.hi, self.p))
        if self.d >= 0:
            self.hi = bisect_right(self.rows, self.key(), self.p, self.hi, key=self._col)
            self.lo = self.p
        self.d += 1
        self.p = self.lo

    def up(self) -> None:
        self.lo, self.hi, self.p = self.saved.pop()
        self.d -= 1

    def distinct_keys(self) -> int:
        return len({r[self.d] for r in self.rows[self.lo:self.hi]})


class Leapfrog:
    """Leapfrog intersection of the current level of several iterators."""

    def __init__(self, its: list[TrieIterator]):
        self.its = list(its)
        self.done = False
        self.key = None
        self.p = 0
        self.moves = 0

    def init(self) -> None:
        if any(it.at_end() for it in self.its):  # @line L8
            self.done = True
            return
        self.its.sort(key=TrieIterator.key)  # @line L9
        self.p = 0
        self.search()

    def search(self) -> None:
        its, m = self.its, len(self.its)
        xmax = its[self.p - 1].key()  # @line L10
        while True:
            x = its[self.p].key()  # @line L11
            if x == xmax:  # @line L12
                self.key = x
                return
            its[self.p].seek(xmax)  # @line L13
            self.moves += 1
            if its[self.p].at_end():
                self.done = True
                return
            xmax = its[self.p].key()  # @line L14
            self.p = (self.p + 1) % m

    def next(self) -> None:
        it = self.its[self.p]
        it.next()  # @line L15
        self.moves += 1
        if it.at_end():
            self.done = True
            return
        self.p = (self.p + 1) % len(self.its)  # @line L16
        self.search()


def leapfrog_triejoin(edges: Sequence[Sequence[str]], rels: Sequence[set[tuple]],
                      order: Sequence[str] | None = None, stats: dict | None = None) -> list[tuple]:
    """Return the natural join as a sorted list of tuples over the attributes in order."""
    if order is None:
        order = sorted({v for e in edges for v in e})
    order = list(order)
    if {v for e in edges for v in e} != set(order):
        raise ValueError("order must list each attribute once")
    k = len(order)
    its = []
    for e, r in zip(edges, rels):
        if len(set(e)) != len(e):
            raise ValueError("an edge lists an attribute twice")
        pos = sorted(range(len(e)), key=lambda j: order.index(e[j]))
        its.append(TrieIterator(sorted(tuple(t[j] for j in pos) for t in r)))
    holders = [[j for j, e in enumerate(edges) if v in e] for v in order]
    calls: list[tuple[int, int, int, int]] = []
    out: list[tuple] = []
    bind = [None] * k

    def level(i: int) -> None:  # @line L1
        if i == k:  # @line L2
            out.append(tuple(bind))
            return
        group = [its[j] for j in holders[i]]
        for it in group:  # @line L3
            it.open()
        fewest = min(it.distinct_keys() for it in group) if stats is not None else 0
        lf = Leapfrog(group)
        lf.init()  # @line L4
        while not lf.done:  # @line L5
            bind[i] = lf.key  # @line L6
            level(i + 1)
            lf.next()  # @line L7
        for it in group:
            it.up()
        calls.append((i, lf.moves, len(group), fewest))

    level(0)
    if stats is not None:
        stats["calls"] = calls
    return out
