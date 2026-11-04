# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-find/. The authors are listed in prov/E7GCG2.jsonl.


class QuickFind:
    """Union-find on the elements 0 to n - 1 with a name stored at each element.

    find and connected take O(1) time. A union of two different sets scans
    the whole array and renames one set, so it takes Theta(n) time.
    """

    def __init__(self, n: int) -> None:
        if n < 0:
            raise ValueError("n must be non-negative")
        self.id: list[int] = list(range(n))  # @line L1
        self.count = n  # @line L2

    def __len__(self) -> int:
        return len(self.id)

    def find(self, p: int) -> int:
        """Return the name of the set of p."""
        return self.id[p]  # @line L3

    def union(self, p: int, q: int) -> bool:
        """Merge the sets of p and q. Return False if they were already one set."""
        ids = self.id
        a, b = ids[p], ids[q]  # @line L4
        if a == b:  # @line L5
            return False
        for i in range(len(ids)):  # @line L6
            if ids[i] == a:  # @line L7
                ids[i] = b
        self.count -= 1  # @line L8
        return True

    def connected(self, p: int, q: int) -> bool:
        """Return True if p and q are in the same set."""
        return self.id[p] == self.id[q]

    def check_invariant(self) -> None:
        """Check that each name is a member of its own set and that count matches."""
        names = set(self.id)
        for name in names:
            assert 0 <= name < len(self.id)
            assert self.id[name] == name
        assert len(names) == self.count
