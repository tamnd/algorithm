# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-heap/. The authors are listed in prov/PYFMNC.jsonl.

from typing import Any, Generic, Iterable, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class WeakHeap(Generic[K]):
    """A min weak heap in an array a with one reverse bit r[i] per node.

    The children of node i are 2i + r[i] (left) and 2i + 1 - r[i] (right).
    The root a[0] has only a right child, a[1]. Weak-heap order: every node
    j > 0 has a key at least the key of its distinguished ancestor.
    """

    def __init__(self, items: Iterable[K] = ()) -> None:
        """Build a weak heap with n - 1 comparisons."""
        self.a: list[K] = list(items)
        self.r: list[int] = [0] * len(self.a)
        self.comparisons = 0
        for j in range(len(self.a) - 1, 0, -1):  # @line L5
            self._join(self.d_ancestor(j), j)  # @line L6

    def __len__(self) -> int:
        return len(self.a)

    def is_empty(self) -> bool:
        """Return True if the heap holds no item."""
        return not self.a

    def d_ancestor(self, j: int) -> int:
        """The distinguished ancestor of j > 0: the parent of the first right child on the way up."""
        while (j & 1) == self.r[j >> 1]:  # @line L1
            j >>= 1
        return j >> 1  # @line L2

    def _join(self, i: int, j: int) -> bool:
        """Join the weak heap rooted at j to i = d_ancestor(j); return True if no swap."""
        self.comparisons += 1
        if self.a[j] < self.a[i]:  # @line L3
            self.a[i], self.a[j] = self.a[j], self.a[i]
            self.r[j] ^= 1  # @line L4
            return False
        return True

    def find_min(self) -> K:
        """Return a smallest key; the heap must not be empty."""
        if not self.a:
            raise IndexError("find_min on an empty heap")
        return self.a[0]

    def _sift_down(self, n: int) -> None:
        """Restore the order of a[0 .. n-1] after a[0] changed."""
        if n < 2:
            return
        x = 1  # @line L7
        while 2 * x + self.r[x] < n:  # @line L8
            x = 2 * x + self.r[x]
        while x > 0:  # @line L9
            self._join(0, x)  # @line L10
            x >>= 1

    def delete_min(self) -> K:
        """Remove and return a smallest key with at most ceil(lg n) comparisons."""
        if not self.a:
            raise IndexError("delete_min on an empty heap")
        top = self.a[0]
        last = self.a.pop()  # @line L11
        self.r.pop()
        if self.a:
            self.a[0] = last
            self._sift_down(len(self.a))  # @line L12
        return top

    def insert(self, x: K) -> None:
        """Add x and sift it up along distinguished ancestors."""
        j = len(self.a)
        self.a.append(x)  # @line L13
        self.r.append(0)
        if j > 0 and j & 1 == 0:
            self.r[j >> 1] = 0  # the parent was a leaf; make j its left child
        while j != 0:  # @line L14
            i = self.d_ancestor(j)
            if self._join(i, j):  # @line L15
                break
            j = i

    def check_invariant(self) -> None:
        """Check weak-heap order for every node."""
        for j in range(1, len(self.a)):
            assert not (self.a[j] < self.a[self.d_ancestor(j)]), f"order at {j}"


def weak_heapsort(items: Iterable[K]) -> tuple[list[K], int]:
    """Sort with Dutton's weak-heapsort; return the sorted list and the comparisons."""
    h = WeakHeap(items)
    a, n = h.a, len(h.a)
    for m in range(n - 1, 0, -1):
        a[0], a[m] = a[m], a[0]
        h._sift_down(m)
    a.reverse()
    return a, h.comparisons
