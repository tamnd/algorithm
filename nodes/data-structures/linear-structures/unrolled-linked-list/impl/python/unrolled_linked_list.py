# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unrolled-linked-list/. The authors are listed in prov/YWD1E5.jsonl.

from typing import Generic, TypeVar

T = TypeVar("T")


class Block(Generic[T]):
    """A node: up to b items in order, and a pointer to the next node."""

    __slots__ = ("items", "next")

    def __init__(self, items: list[T], next: "Block[T] | None" = None) -> None:
        self.items = items
        self.next = next


class UnrolledLinkedList(Generic[T]):
    """A sequence stored as a singly linked list of blocks of at most b items.

    Invariant: the blocks, read in order, hold the sequence; each block holds
    1 to b items; when there are two or more blocks, each holds at least
    h = b // 2 items. With k blocks, get and set cost O(k) = O(1 + n / b)
    steps, insert and delete cost O(n / b + b). Space: O(n + b).
    """

    def __init__(self, b: int = 16) -> None:
        if b < 2:
            raise ValueError("need b >= 2")
        self.b = b
        self.h = b // 2
        self.head: Block[T] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def _find(self, i: int) -> tuple["Block[T] | None", Block[T], int]:
        """Return (pred, v, j): position i is offset j of block v. Needs a block."""
        assert self.head is not None
        pred: Block[T] | None = None
        v = self.head  # @line L1
        while v.next is not None and i >= len(v.items):  # @line L2
            i -= len(v.items)  # @line L3
            pred, v = v, v.next
        return pred, v, i  # @line L4

    def get(self, i: int) -> T:
        """Return the item at position i. Precondition: 0 <= i < n. Cost O(1 + n / b)."""
        if not 0 <= i < self.n:
            raise IndexError("position out of range")
        _, v, j = self._find(i)
        return v.items[j]  # @line L5

    def set(self, i: int, x: T) -> None:
        """Replace the item at position i. Precondition: 0 <= i < n. Cost O(1 + n / b)."""
        if not 0 <= i < self.n:
            raise IndexError("position out of range")
        _, v, j = self._find(i)
        v.items[j] = x

    def insert(self, i: int, x: T) -> None:
        """Insert x so that it gets position i. Precondition: 0 <= i <= n. Cost O(n / b + b)."""
        if not 0 <= i <= self.n:
            raise IndexError("position out of range")
        self.n += 1
        if self.head is None:  # @line L6
            self.head = Block([x])
            return
        _, v, j = self._find(i)  # @line L7
        if len(v.items) == self.b:  # @line L8
            c = self.b - self.h  # v keeps c = ceil(b / 2) items
            w = Block(v.items[c:], v.next)  # @line L9
            del v.items[c:]
            v.next = w
            if j > c:  # @line L10
                v, j = w, j - c
        v.items.insert(j, x)  # @line L11

    def delete(self, i: int) -> T:
        """Remove and return the item at position i. Precondition: 0 <= i < n. Cost O(n / b + b)."""
        if not 0 <= i < self.n:
            raise IndexError("position out of range")
        self.n -= 1
        pred, v, j = self._find(i)  # @line L12
        x = v.items.pop(j)  # @line L13
        if len(v.items) >= self.h or (pred is None and v.next is None):  # @line L14
            if not v.items:
                self.head = None
            return x
        if v.next is not None:  # @line L15
            u, r = v, v.next
        else:
            assert pred is not None
            u, r = pred, v
        if len(u.items) + len(r.items) <= self.b:  # @line L16
            u.items.extend(r.items)
            u.next = r.next
        elif u is v:  # @line L17
            u.items.append(r.items.pop(0))
        else:
            r.items.insert(0, u.items.pop())
        return x  # @line L18

    def append(self, x: T) -> None:
        """Insert x at the end. Cost O(n / b + b)."""
        self.insert(self.n, x)

    def to_list(self) -> list[T]:
        """Return the items in order. Cost O(n + n / b)."""
        out: list[T] = []
        v = self.head
        while v is not None:
            out.extend(v.items)
            v = v.next
        return out

    def blocks(self) -> list[int]:
        """Return the sizes of the blocks in order."""
        out = []
        v = self.head
        while v is not None:
            out.append(len(v.items))
            v = v.next
        return out

    def check_invariant(self) -> None:
        """Check the block sizes and the count of items."""
        sizes = self.blocks()
        assert sum(sizes) == self.n
        assert all(1 <= s <= self.b for s in sizes)
        if len(sizes) >= 2:
            assert all(s >= self.h for s in sizes)
