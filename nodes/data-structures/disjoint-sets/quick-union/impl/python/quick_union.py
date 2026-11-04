# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-union/. The authors are listed in prov/TPV99M.jsonl.


class QuickUnion:
    """Union-find on the elements 0 to n - 1 as a forest of parent pointers.

    find walks from an element to its root. union links the root of the
    first argument under the root of the second. Both cost time in
    proportion to the depth of the elements, which is O(n) in the worst case.
    """

    def __init__(self, n: int) -> None:
        if n < 0:
            raise ValueError("n must be non-negative")
        self.parent: list[int] = list(range(n))  # @line L1
        self.count = n  # @line L2

    def __len__(self) -> int:
        return len(self.parent)

    def find(self, p: int) -> int:
        """Return the root of the tree of p."""
        parent = self.parent
        if not 0 <= p < len(parent):
            raise IndexError("element out of range")
        while p != parent[p]:  # @line L3
            p = parent[p]  # @line L4
        return p  # @line L5

    def union(self, p: int, q: int) -> bool:
        """Merge the sets of p and q. Return False if they were already one set."""
        i, j = self.find(p), self.find(q)  # @line L6
        if i == j:  # @line L7
            return False
        self.parent[i] = j  # @line L8
        self.count -= 1  # @line L9
        return True

    def connected(self, p: int, q: int) -> bool:
        """Return True if p and q are in the same set."""
        return self.find(p) == self.find(q)

    def depth(self, p: int) -> int:
        """Return the number of edges from p to its root."""
        d = 0
        while p != self.parent[p]:
            p = self.parent[p]
            d += 1
        return d

    def check_invariant(self) -> None:
        """Check that the parent pointers form a forest with count roots."""
        n = len(self.parent)
        roots = 0
        for x in range(n):
            assert 0 <= self.parent[x] < n
            if self.parent[x] == x:
                roots += 1
            steps, y = 0, x
            while y != self.parent[y]:
                y = self.parent[y]
                steps += 1
                assert steps < n
        assert roots == self.count
