# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cartesian-tree/. The authors are listed in prov/3X8X1H.jsonl.

from collections import deque


class CartesianTree:
    """The min-Cartesian tree of a sequence, built in O(n) time with a stack.

    Node i is position i of the sequence (0 .. n-1). The tree is a rooted
    binary tree: its inorder is 0, 1, ..., n-1, and every node holds a value
    no smaller than its parent's. Equal values are ordered by position, so the
    leftmost minimum of each range is the root of that range. Missing
    children and the parent of the root are -1; root is -1 for n = 0.
    """

    def __init__(self, values: list) -> None:
        a = list(values)
        n = len(a)
        self.values = a
        self.parent = [-1] * n
        self.left = [-1] * n
        self.right = [-1] * n
        spine: list[int] = []  # @line L1
        for i in range(n):  # @line L2
            last = -1  # @line L3
            while spine and a[spine[-1]] > a[i]:  # @line L4
                last = spine.pop()  # @line L5
            self.left[i] = last  # @line L6
            if last != -1:
                self.parent[last] = i
            if spine:  # @line L7
                self.right[spine[-1]] = i
                self.parent[i] = spine[-1]
            spine.append(i)  # @line L8
        self.root = spine[0] if spine else -1  # @line L9
        self.depth = [0] * n
        if n:
            queue = deque([self.root])
            while queue:
                x = queue.popleft()
                for c in (self.left[x], self.right[x]):
                    if c != -1:
                        self.depth[c] = self.depth[x] + 1
                        queue.append(c)

    def __len__(self) -> int:
        return len(self.values)

    def inorder(self) -> list[int]:
        """The nodes in inorder; equals list(range(n)) for every input."""
        out: list[int] = []
        stack: list[int] = []
        x = self.root
        while x != -1 or stack:
            while x != -1:
                stack.append(x)
                x = self.left[x]
            x = stack.pop()
            out.append(x)
            x = self.right[x]
        return out

    def range_min_index(self, i: int, j: int) -> int:
        """Position of the leftmost minimum of values[i..j], as lca(i, j).

        The lowest common ancestor is found by climbing, in O(h) time for a
        tree of height h; a constant-time LCA structure makes it O(1).
        """
        if not 0 <= i <= j < len(self.values):
            raise IndexError("need 0 <= i <= j < n")
        u, v = i, j
        while self.depth[u] > self.depth[v]:
            u = self.parent[u]
        while self.depth[v] > self.depth[u]:
            v = self.parent[v]
        while u != v:
            u = self.parent[u]
            v = self.parent[v]
        return u
