# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-stack/. The authors are listed in prov/A69Z23.jsonl.

from typing import Generic, TypeVar

T = TypeVar("T")


class ExternalStack(Generic[T]):
    """A stack whose bottom part lives on a simulated disk in blocks of B items.

    Memory holds a buffer of at most 2B items: the top of the stack. A push
    into a full buffer first writes its B oldest items as one block; a pop
    from an empty buffer first reads the last block back. After each block
    transfer the buffer holds exactly B items, so any n operations make at
    most n / B transfers. `reads` and `writes` count the block transfers.
    """

    def __init__(self, block_size: int) -> None:
        if block_size < 1:
            raise ValueError("the block size must be at least 1")
        self.B = block_size
        self.buf: list[T] = []
        self.disk: list[list[T]] = []
        self.reads = 0
        self.writes = 0

    def push(self, x: T) -> None:
        """Put x on top of the stack."""
        if len(self.buf) == 2 * self.B:  # @line L1
            self.disk.append(self.buf[: self.B])  # @line L2
            self.writes += 1
            del self.buf[: self.B]  # @line L3
        self.buf.append(x)  # @line L4

    def pop(self) -> T:
        """Remove and return the top item. Raise IndexError if empty."""
        if not self.buf:  # @line L5
            if not self.disk:  # @line L6
                raise IndexError("pop from an empty stack")
            self.buf = self.disk.pop()  # @line L7
            self.reads += 1
        return self.buf.pop()  # @line L8

    def top(self) -> T:
        """Return the top item without removing it."""
        x = self.pop()
        self.buf.append(x)
        return x

    def __len__(self) -> int:
        return len(self.buf) + self.B * len(self.disk)

    def items(self) -> list[T]:
        """Return the items from the bottom to the top, without I/O counts."""
        return [x for blk in self.disk for x in blk] + self.buf

    def check_invariant(self) -> None:
        """Raise AssertionError if a representation rule fails."""
        assert len(self.buf) <= 2 * self.B
        assert all(len(blk) == self.B for blk in self.disk)
