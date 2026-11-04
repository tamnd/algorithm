# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-segment-tree/. The authors are listed in prov/6P1XHV.jsonl.


class DynamicSegmentTree:
    """Range sums over A[0..U-1] of integers, all zero at the start.

    Nodes are made only on the paths of updates. update and query take
    O(log U) time; after m updates the tree has at most 1 + m*ceil(lg U)
    nodes. Node 0 means "absent" and node 1 is the root.
    """

    def __init__(self, universe: int) -> None:
        """Make the tree of U = universe zeros; requires universe >= 1."""
        if universe < 1:
            raise ValueError("universe must be at least 1")
        self.universe = universe
        self.val = [0, 0]
        self.left = [0, 0]
        self.right = [0, 0]

    def _new_node(self) -> int:
        self.val.append(0)
        self.left.append(0)
        self.right.append(0)
        return len(self.val) - 1

    def node_count(self) -> int:
        """The number of created nodes, the root included."""
        return len(self.val) - 1

    def update(self, i: int, x: int) -> None:
        """Set A[i] += x, for 0 <= i < U, in O(log U) time."""
        if not 0 <= i < self.universe:
            raise IndexError("index out of range")
        v, lo, hi = 1, 0, self.universe  # @line L1
        while True:  # @line L2
            self.val[v] += x  # @line L3
            if hi - lo == 1:  # @line L4
                return
            mid = (lo + hi) // 2  # @line L5
            if i < mid:  # @line L6
                if self.left[v] == 0:  # @line L7
                    c = self._new_node()
                    self.left[v] = c
                v, hi = self.left[v], mid  # @line L8
            else:  # @line L9
                if self.right[v] == 0:  # @line L10
                    c = self._new_node()
                    self.right[v] = c
                v, lo = self.right[v], mid  # @line L11

    def query(self, l: int, r: int) -> int:
        """Return A[l] + ... + A[r-1] for 0 <= l <= r <= U, in O(log U) time."""
        if not 0 <= l <= r <= self.universe:
            raise IndexError("range out of bounds")
        total = 0
        stack = [(1, 0, self.universe)]
        while stack:
            v, lo, hi = stack.pop()
            if v == 0 or r <= lo or hi <= l:  # @line L12
                continue
            if l <= lo and hi <= r:  # @line L13
                total += self.val[v]
                continue
            mid = (lo + hi) // 2  # @line L14
            stack.append((self.right[v], mid, hi))  # @line L15
            stack.append((self.left[v], lo, mid))
        return total

    def check_invariant(self) -> None:
        """Check that each inner node holds the sum of its children and
        that each node is reached exactly once from the root."""
        seen = [False] * len(self.val)
        stack = [(1, 0, self.universe)]
        while stack:
            v, lo, hi = stack.pop()
            assert not seen[v], "node reached twice"
            seen[v] = True
            if hi - lo == 1:
                assert self.left[v] == 0 and self.right[v] == 0, "leaf with children"
                continue
            mid = (lo + hi) // 2
            s = 0
            for c, a, b in ((self.left[v], lo, mid), (self.right[v], mid, hi)):
                if c != 0:
                    s += self.val[c]
                    stack.append((c, a, b))
            if self.left[v] or self.right[v]:
                assert self.val[v] == s, "inner sum differs from the children"
        assert all(seen[1:]), "unreachable node"
