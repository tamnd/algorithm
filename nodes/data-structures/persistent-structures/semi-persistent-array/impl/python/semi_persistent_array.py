# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-persistent-array/. The authors are listed in prov/07TV6Q.jsonl.

"""A semi-persistent array: one shared array plus a chain of diffs.

The valid versions form a path v0 -> v1 -> ... -> vk, where vk (the newest)
holds the real array and each older vi is a diff "vi equals v(i+1) except
that a[idx] = val". Reads of any valid version walk the diffs toward vk.
An update of an older version vi first rolls the array back to vi, which
makes v(i+1), ..., vk invalid, and then writes. All loops are iterative.
"""

from typing import Generic, List, Optional, Sequence, TypeVar

T = TypeVar("T")

_ARR, _DIFF, _DEAD = 0, 1, 2


class _Store(Generic[T]):
    __slots__ = ("a", "root", "current", "length")

    def __init__(self, items: Sequence[T]) -> None:
        self.a: List[T] = list(items)
        self.root: "Optional[SemiPersistentArray[T]]" = None
        self.current: "Optional[SemiPersistentArray[T]]" = None
        self.length = 1  # number of valid versions


class SemiPersistentArray(Generic[T]):
    """A handle to one version. Only versions on the path from the first
    version to the newest one are valid; using another raises ValueError.
    """

    __slots__ = ("_store", "_kind", "_idx", "_val", "_next")

    def __init__(self, items: Sequence[T]) -> None:
        """The first version, holding ``items``. Cost: Θ(n)."""
        store: _Store[T] = _Store(items)
        self._store = store
        self._kind = _ARR
        self._idx = 0
        self._val: Optional[T] = None
        self._next: "Optional[SemiPersistentArray[T]]" = None
        store.root = self
        store.current = self

    def __len__(self) -> int:
        """Number of slots. Cost: O(1)."""
        return len(self._store.a)

    def is_valid(self) -> bool:
        """Whether this version can still be used. Cost: O(1)."""
        return self._kind != _DEAD

    def _check(self, i: int) -> None:
        if self._kind == _DEAD:
            raise ValueError("this version is no longer valid")
        if not 0 <= i < len(self._store.a):
            raise IndexError("index out of range")

    def get(self, i: int) -> T:
        """Item i of this version. Cost: Θ(1 + d), d the distance to the newest."""
        self._check(i)  # @line L1
        t: SemiPersistentArray[T] = self  # @line L2
        while t._kind == _DIFF:  # @line L3
            if t._idx == i:  # @line L4
                return t._val  # type: ignore[return-value]
            assert t._next is not None
            t = t._next  # @line L5
        return self._store.a[i]  # @line L6

    def _reroot(self) -> None:
        if self._kind == _DEAD:  # @line L11
            raise ValueError("this version is no longer valid")
        path: List[SemiPersistentArray[T]] = []
        t: SemiPersistentArray[T] = self
        while t._kind == _DIFF:  # @line L12
            path.append(t)
            assert t._next is not None
            t = t._next
        a = self._store.a
        for d in reversed(path):  # @line L13
            a[d._idx] = d._val  # type: ignore[assignment]
        for d in path[1:]:  # @line L14
            d._kind = _DEAD
            d._next = None
            d._val = None
        if path:
            t._kind = _DEAD
            self._store.length -= len(path)
        self._kind = _ARR  # @line L15
        self._next = None
        self._val = None
        self._store.current = self

    def set(self, i: int, x: T) -> "SemiPersistentArray[T]":
        """A new version equal to this one with item i set to x.

        Versions made after this one become invalid. Cost: Θ(1 + d).
        """
        self._check(i)
        self._reroot()  # @line L7
        store = self._store
        w: SemiPersistentArray[T] = SemiPersistentArray.__new__(SemiPersistentArray)  # @line L8
        w._store, w._kind, w._idx, w._val, w._next = store, _ARR, 0, None, None
        self._kind, self._idx, self._val, self._next = _DIFF, i, store.a[i], w  # @line L9
        store.a[i] = x  # @line L10
        store.current = w
        store.length += 1
        return w

    def to_list(self) -> List[T]:
        """All items of this version. Cost: Θ(n + d)."""
        if self._kind == _DEAD:
            raise ValueError("this version is no longer valid")
        out = list(self._store.a)
        path: List[SemiPersistentArray[T]] = []
        t: SemiPersistentArray[T] = self
        while t._kind == _DIFF:
            path.append(t)
            assert t._next is not None
            t = t._next
        for d in reversed(path):
            out[d._idx] = d._val  # type: ignore[assignment]
        return out

    def check_invariant(self) -> None:
        """Check that the valid versions form one path of diffs ending at the
        version that owns the array, and that this version is on it (or dead).
        Cost: Θ(k) for k valid versions.
        """
        store = self._store
        t = store.root
        assert t is not None
        count = 1
        on_path = t is self
        while t._kind == _DIFF:
            assert t._next is not None and 0 <= t._idx < len(store.a)
            t = t._next
            count += 1
            on_path = on_path or t is self
        assert t._kind == _ARR and t is store.current
        assert count == store.length
        assert on_path or self._kind == _DEAD
