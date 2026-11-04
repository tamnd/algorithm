# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fully-persistent-array/. The authors are listed in prov/MX556Y.jsonl.

"""A fully persistent array by path copying over a balanced binary tree.

Version t is the root roots[t].  A read walks from the root to a leaf, and a
write copies the nodes on that path, so both take O(log n) time and a write
adds O(log n) nodes.  No node is ever changed after it is built.
"""

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class _Leaf:
    __slots__ = ("value",)

    def __init__(self, value: Any) -> None:
        self.value = value


class _Node:
    __slots__ = ("left", "right")

    def __init__(self, left: Any, right: Any) -> None:
        self.left = left
        self.right = right


def _build(a: Sequence[Any], lo: int, hi: int) -> Any:
    if hi - lo == 1:  # @line L1
        return _Leaf(a[lo])
    mid = (lo + hi) // 2  # @line L2
    return _Node(_build(a, lo, mid), _build(a, mid, hi))  # @line L3


def _get(v: Any, n: int, i: int) -> Any:
    lo, hi = 0, n  # @line L4
    while hi - lo > 1:  # @line L5
        mid = (lo + hi) // 2  # @line L6
        if i < mid:  # @line L7
            v, hi = v.left, mid
        else:
            v, lo = v.right, mid
    return v.value  # @line L8


def _set(v: Any, lo: int, hi: int, i: int, x: Any) -> Any:
    if hi - lo == 1:  # @line L9
        return _Leaf(x)
    mid = (lo + hi) // 2  # @line L10
    if i < mid:  # @line L11
        return _Node(_set(v.left, lo, mid, i, x), v.right)
    return _Node(v.left, _set(v.right, mid, hi, i, x))  # @line L12


class FullyPersistentArray(Generic[T]):
    """An array of fixed length n whose versions are numbered 0, 1, 2, ...

    Version 0 is the initial array.  set(t, i, x) makes a new version from
    version t, for any existing t, and returns its number.
    """

    __slots__ = ("_n", "_roots", "_nodes")

    def __init__(self, initial: Sequence[T]) -> None:
        self._n = len(initial)
        root = _build(initial, 0, self._n) if self._n else None
        self._roots: list[Any] = [root]
        self._nodes = 2 * self._n - 1 if self._n else 0

    def __len__(self) -> int:
        return self._n

    def versions(self) -> int:
        return len(self._roots)

    def _check(self, t: int, i: int) -> None:
        if not 0 <= t < len(self._roots):
            raise IndexError("no such version")
        if not 0 <= i < self._n:
            raise IndexError("index out of range")

    def get(self, t: int, i: int) -> T:
        self._check(t, i)
        return _get(self._roots[t], self._n, i)

    def set(self, t: int, i: int, x: T) -> int:
        self._check(t, i)
        self._roots.append(_set(self._roots[t], 0, self._n, i, x))  # @line L13
        self._nodes += _path_length(self._n, i)
        return len(self._roots) - 1

    def to_list(self, t: int) -> list[T]:
        if not 0 <= t < len(self._roots):
            raise IndexError("no such version")
        out: list[T] = []

        def walk(v: Any) -> None:
            if isinstance(v, _Leaf):
                out.append(v.value)
            else:
                walk(v.left)
                walk(v.right)

        if self._n:
            walk(self._roots[t])
        return out

    def node_count(self) -> int:
        """The number of nodes built so far, over all versions."""
        return self._nodes


def _path_length(n: int, i: int) -> int:
    """The number of nodes on the path from the root to leaf i."""
    lo, hi, k = 0, n, 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if i < mid:
            hi = mid
        else:
            lo = mid
        k += 1
    return k
