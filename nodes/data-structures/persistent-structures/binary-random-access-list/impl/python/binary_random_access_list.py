# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-random-access-list/. The authors are listed in prov/00WGSN.jsonl.

from collections.abc import Iterator
from typing import Generic, Optional, TypeVar, Union

T = TypeVar("T")


class Leaf(Generic[T]):
    __slots__ = ("item",)

    def __init__(self, item: T) -> None:
        self.item = item


class Node(Generic[T]):
    """A complete binary tree with w leaves, w a power of two at least 2."""

    __slots__ = ("w", "left", "right")

    def __init__(self, w: int, left: "Tree[T]", right: "Tree[T]") -> None:
        self.w, self.left, self.right = w, left, right


Tree = Union[Leaf[T], Node[T]]

# A digit is None (Zero) or a tree (One t). The digit list is an immutable
# linked list, least significant digit first: None, or a pair (digit, rest).
Digit = Optional[Tree[T]]
Digits = Optional[tuple[Digit[T], "Digits[T]"]]


def size(t: Tree[T]) -> int:
    return 1 if isinstance(t, Leaf) else t.w


def link(t1: Tree[T], t2: Tree[T]) -> Node[T]:
    """Join two complete trees of the same size; the leaves of t1 come first."""
    return Node(size(t1) + size(t2), t1, t2)


def cons_tree(t: Tree[T], ds: Digits[T]) -> Digits[T]:
    if ds is None:  # @line L2
        return (t, None)
    d, rest = ds
    if d is None:  # @line L3
        return (t, rest)
    u = d  # @line L4
    return (None, cons_tree(link(t, u), rest))  # @line L5


def uncons_tree(ds: Digits[T]) -> tuple[Tree[T], Digits[T]]:
    if ds is None:  # @line L6
        raise IndexError("empty list")
    d, rest = ds
    if d is not None and rest is None:  # @line L7
        return d, None
    if d is not None:  # @line L8
        return d, (None, rest)
    t, rest2 = uncons_tree(rest)  # @line L9
    assert isinstance(t, Node)
    return t.left, (t.right, rest2)  # @line L10


def update_tree(i: int, y: T, t: Tree[T]) -> Tree[T]:
    if isinstance(t, Leaf):  # @line L25
        return Leaf(y)
    half = t.w // 2  # @line L26
    if i < half:  # @line L27
        return Node(t.w, update_tree(i, y, t.left), t.right)
    return Node(t.w, t.left, update_tree(i - half, y, t.right))  # @line L28


def update_digits(i: int, y: T, ds: Digits[T]) -> Digits[T]:
    if ds is None:
        raise IndexError("index out of range")
    d, rest = ds
    if d is None:  # @line L21
        return (None, update_digits(i, y, rest))
    t = d  # @line L22
    if i < size(t):  # @line L23
        return (update_tree(i, y, t), rest)
    return (t, update_digits(i - size(t), y, rest))  # @line L24


class BinaryRandomAccessList(Generic[T]):
    """Okasaki's binary random-access list: a persistent sequence.

    The list of n items is a list of digits of n in binary, least significant
    first; digit k is Zero or One t, where t is a complete binary tree with 2^k
    leaves. cons, head, tail, lookup and update each take O(log n) time in the
    worst case and make O(log n) new nodes. Every method leaves self unchanged.
    """

    __slots__ = ("_ds", "_n")

    def __init__(self) -> None:
        self._ds: Digits[T] = None
        self._n = 0

    @classmethod
    def _of(cls, ds: Digits[T], n: int) -> "BinaryRandomAccessList[T]":
        r: BinaryRandomAccessList[T] = cls.__new__(cls)
        r._ds, r._n = ds, n
        return r

    def __len__(self) -> int:
        return self._n

    def is_empty(self) -> bool:
        return self._ds is None

    def cons(self, x: T) -> "BinaryRandomAccessList[T]":
        """Return the list with x added at the front."""
        return self._of(cons_tree(Leaf(x), self._ds), self._n + 1)  # @line L1

    def head(self) -> T:
        """Return the first item. Raises IndexError on an empty list."""
        t, _ = uncons_tree(self._ds)  # @line L11
        assert isinstance(t, Leaf)
        return t.item

    def tail(self) -> "BinaryRandomAccessList[T]":
        """Return the list without its first item. Raises IndexError on an empty list."""
        _, ds = uncons_tree(self._ds)  # @line L12
        return self._of(ds, self._n - 1)

    def lookup(self, i: int) -> T:
        """Return item i (0-based). Raises IndexError if i is out of range."""
        if i < 0:
            raise IndexError("index out of range")
        ds = self._ds
        while ds is not None:  # @line L13
            d, ds = ds
            if d is not None:  # @line L14
                if i < size(d):  # @line L15
                    t: Tree[T] = d
                    while isinstance(t, Node):  # @line L16
                        half = t.w // 2
                        if i < half:  # @line L17
                            t = t.left
                        else:
                            i, t = i - half, t.right
                    return t.item  # @line L18
                i -= size(d)  # @line L19
        raise IndexError("index out of range")  # @line L20

    def update(self, i: int, y: T) -> "BinaryRandomAccessList[T]":
        """Return the list with item i replaced by y. Raises IndexError if out of range."""
        if not 0 <= i < self._n:
            raise IndexError("index out of range")
        return self._of(update_digits(i, y, self._ds), self._n)

    def __iter__(self) -> Iterator[T]:
        ds = self._ds
        while ds is not None:
            d, ds = ds
            if d is not None:
                stack: list[Tree[T]] = [d]
                while stack:
                    t = stack.pop()
                    if isinstance(t, Leaf):
                        yield t.item
                    else:
                        stack.append(t.right)
                        stack.append(t.left)

    def to_list(self) -> list[T]:
        return list(self)

    def digits(self) -> list[int]:
        """The binary digits of the representation, least significant first."""
        out, ds = [], self._ds
        while ds is not None:
            d, ds = ds
            out.append(0 if d is None else 1)
        return out

    def check_invariant(self) -> None:
        """Digit k is Zero or a complete tree of 2^k leaves; the last digit is One; sizes add to n."""
        ds, k, total, last = self._ds, 0, 0, None
        while ds is not None:
            d, ds = ds
            last = d
            if d is not None:
                _check_complete(d, 1 << k)
                total += 1 << k
            k += 1
        assert self._ds is None or last is not None
        assert total == self._n


def _check_complete(t: Tree[T], w: int) -> None:
    if isinstance(t, Leaf):
        assert w == 1
        return
    assert t.w == w and w >= 2
    _check_complete(t.left, w // 2)
    _check_complete(t.right, w // 2)
