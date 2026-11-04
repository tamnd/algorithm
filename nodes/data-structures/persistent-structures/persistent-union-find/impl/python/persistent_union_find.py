# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-union-find/. The authors are listed in prov/ZTTVD6.jsonl.

"""Conchon and Filliatre's persistent union-find.

The parent and rank maps are Baker-style persistent arrays: one shared
Python list plus chains of diffs, with rerooting on each access. Every
version stays valid. Union uses union by rank, and find does path
compression, writing the compressed parent array back into the handle.
That write is a side effect, but it keeps the partition of the handle, so
no caller can see it. All loops are iterative.
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")

_ARR, _DIFF = 0, 1


class PArray(Generic[T]):
    """A fully persistent array with rerooting (Baker's trick).

    Access to the version that owns the shared list costs O(1); access to
    another version costs O(1 + d), d the number of diffs between them.
    """

    __slots__ = ("_kind", "_data", "_idx", "_val", "_next")

    def __init__(self, items: List[T]) -> None:
        """A first version holding ``items`` (the list is taken over)."""
        self._kind = _ARR
        self._data: Optional[List[T]] = items
        self._idx = 0
        self._val: Optional[T] = None
        self._next: "Optional[PArray[T]]" = None

    def _reroot(self) -> List[T]:
        path: List[PArray[T]] = []
        t: PArray[T] = self
        while t._kind == _DIFF:  # @line A1
            path.append(t)
            assert t._next is not None
            t = t._next
        data = t._data
        assert data is not None
        for d in reversed(path):  # @line A2
            nxt = d._next  # @line A3
            assert nxt is not None
            i = d._idx
            nxt._kind, nxt._idx, nxt._val, nxt._next = _DIFF, i, data[i], d  # @line A4
            nxt._data = None
            data[i] = d._val  # type: ignore[assignment]  # @line A5
            d._kind, d._data, d._val, d._next = _ARR, data, None, None  # @line A6
        return data

    def get(self, i: int) -> T:
        """Item i of this version. Cost: O(1 + d)."""
        return self._reroot()[i]  # @line A7

    def set(self, i: int, v: T) -> "PArray[T]":
        """A new version with item i set to v. Cost: O(1 + d)."""
        data = self._reroot()  # @line A8
        old = data[i]
        if old is v or old == v:
            return self
        data[i] = v
        new: PArray[T] = PArray.__new__(PArray)  # @line A9
        new._kind, new._data, new._idx, new._val, new._next = _ARR, data, 0, None, None
        self._kind, self._data, self._idx, self._val, self._next = _DIFF, None, i, old, new  # @line A10
        return new

    def to_list(self) -> List[T]:
        """A copy of this version. Cost: O(n + d)."""
        return list(self._reroot())


class PersistentUnionFind:
    """A version of a partition of {0, ..., n - 1}."""

    __slots__ = ("_rank", "_parent", "_n")

    def __init__(self, n: int, _rank: Optional[PArray[int]] = None,
                 _parent: Optional[PArray[int]] = None) -> None:
        """The partition into n singletons. Cost: Θ(n)."""
        self._n = n
        self._rank = _rank if _rank is not None else PArray([0] * n)
        self._parent = _parent if _parent is not None else PArray(list(range(n)))

    def __len__(self) -> int:
        """Number of elements. Cost: O(1)."""
        return self._n

    def find(self, x: int) -> int:
        """The representative of the set of x. Cost: O(log n + d)."""
        if not 0 <= x < self._n:
            raise IndexError("element out of range")
        f = self._parent  # @line L1
        r = x
        while f.get(r) != r:  # @line L2
            r = f.get(r)
        y = x  # @line L3
        while y != r:  # @line L4
            nxt = f.get(y)
            f = f.set(y, r)
            y = nxt
        self._parent = f  # @line L5
        return r  # @line L6

    def same(self, x: int, y: int) -> bool:
        """Whether x and y are in the same set. Cost: O(log n + d)."""
        return self.find(x) == self.find(y)

    def union(self, x: int, y: int) -> "PersistentUnionFind":
        """A new version with the sets of x and y merged. Cost: O(log n + d)."""
        rx, ry = self.find(x), self.find(y)  # @line L7
        if rx == ry:  # @line L8
            return self
        a, b = self._rank.get(rx), self._rank.get(ry)  # @line L9
        if a > b:  # @line L10
            return PersistentUnionFind(self._n, self._rank, self._parent.set(ry, rx))
        if a < b:  # @line L11
            return PersistentUnionFind(self._n, self._rank, self._parent.set(rx, ry))
        return PersistentUnionFind(  # @line L12
            self._n, self._rank.set(rx, a + 1), self._parent.set(ry, rx))

    def sets(self) -> List[List[int]]:
        """The sets of this version, each sorted, in order of least element."""
        groups: dict = {}
        for x in range(self._n):
            groups.setdefault(self.find(x), []).append(x)
        return sorted(groups.values())

    def check_invariant(self) -> None:
        """Check that parents are in range and that rank strictly grows from
        a non-root to its parent, so there are no cycles. Cost: O(n + d)."""
        par = self._parent.to_list()
        rank = self._rank.to_list()
        assert len(par) == self._n and len(rank) == self._n
        for x in range(self._n):
            p = par[x]
            assert 0 <= p < self._n
            if p != x:
                assert rank[p] > rank[x]
            assert rank[x] < max(1, self._n).bit_length() + 1

