# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-linked-list/. The authors are listed in prov/GE847R.jsonl.

from typing import Generic, TypeVar

T = TypeVar("T")


class XorLinkedList(Generic[T]):
    """A doubly linked list that keeps one link field per node: prev XOR next.

    Memory is simulated by the arrays key and np, indexed by integer
    addresses. Address 0 is nil and is never given to a node. For the nodes
    x_1, ..., x_n in list order, np[x_i] = x_(i-1) XOR x_(i+1), where x_0 and
    x_(n+1) are 0. push_front, push_back, pop_front, pop_back and reverse
    cost O(1); to_list costs Theta(n). Space: n keys and n link words.
    """

    def __init__(self) -> None:
        self.key: list[T | None] = [None]  # cell 0 is nil
        self.np: list[int] = [0]
        self.free: list[int] = []  # freed addresses, reused first
        self.head = 0
        self.tail = 0
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def _allocate(self, k: T) -> int:
        if self.free:
            x = self.free.pop()
            self.key[x] = k
        else:
            x = len(self.key)
            self.key.append(k)
            self.np.append(0)
        return x

    def push_front(self, k: T) -> int:
        """Insert k at the front and return the address of its node. Cost O(1)."""
        x = self._allocate(k)  # @line L1
        self.np[x] = self.head  # @line L2: 0 XOR head
        if self.head != 0:  # @line L3
            self.np[self.head] ^= x
        else:
            self.tail = x  # @line L4
        self.head = x  # @line L5
        self.size += 1
        return x

    def pop_front(self) -> T:
        """Remove and return the front key. Precondition: the list is not empty. Cost O(1)."""
        if self.head == 0:
            raise IndexError("pop from an empty list")
        x = self.head  # @line L6
        nxt = self.np[x]
        if nxt != 0:  # @line L7
            self.np[nxt] ^= x
        else:
            self.tail = 0  # @line L8
        self.head = nxt  # @line L9
        k = self.key[x]  # @line L10
        self.key[x] = None
        self.np[x] = 0
        self.free.append(x)
        self.size -= 1
        return k  # type: ignore[return-value]

    def to_list(self) -> list[T]:
        """Return the keys from the front to the back. Cost Theta(n)."""
        out: list[T] = []
        prev, cur = 0, self.head  # @line L11
        while cur != 0:  # @line L12
            out.append(self.key[cur])  # type: ignore[arg-type]  # @line L13
            nxt = self.np[cur] ^ prev  # @line L14
            prev, cur = cur, nxt  # @line L15
        return out

    def reverse(self) -> None:
        """Reverse the list by swapping head and tail. Cost O(1)."""
        self.head, self.tail = self.tail, self.head

    def push_back(self, k: T) -> int:
        """Insert k at the back and return the address of its node. Cost O(1)."""
        self.reverse()
        x = self.push_front(k)
        self.reverse()
        return x

    def pop_back(self) -> T:
        """Remove and return the back key. Precondition: the list is not empty. Cost O(1)."""
        self.reverse()
        try:
            return self.pop_front()
        finally:
            self.reverse()

    def insert_between(self, p: int, q: int, k: T) -> int:
        """Insert k between the adjacent nodes p and q (p before q). Cost O(1)."""
        x = self._allocate(k)
        self.np[x] = p ^ q
        self.np[p] ^= q ^ x
        self.np[q] ^= p ^ x
        self.size += 1
        return x

    def check_invariant(self) -> None:
        """Check np[x_i] = x_(i-1) XOR x_(i+1) for each node, and the ends and the size."""
        order: list[int] = []
        prev, cur = 0, self.head
        while cur != 0:
            order.append(cur)
            prev, cur = cur, self.np[cur] ^ prev
            assert len(order) <= len(self.key), "cycle"
        assert len(order) == self.size
        assert (self.tail == order[-1]) if order else (self.head == 0 and self.tail == 0)
        ext = [0, *order, 0]
        for i in range(1, len(ext) - 1):
            assert self.np[ext[i]] == ext[i - 1] ^ ext[i + 1]
