# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-tree/. The authors are listed in prov/4YYHCQ.jsonl.

"""A binary decision tree with axis-aligned tests "x[j] <= theta".

Nodes live in parallel arrays and are named by integer ids. Node 0 is the
root. A node is a leaf when its left child is -1. Removed nodes keep their
ids but are no longer reachable from the root.
"""

from typing import Any, Sequence


class DecisionTree:
    """A tree whose internal nodes test one feature and whose leaves hold values."""

    def __init__(self, value: Any = None) -> None:
        """Make a tree with one leaf, the root, that predicts `value`."""
        self.feature: list[int] = [-1]
        self.threshold: list[Any] = [None]
        self.left: list[int] = [-1]
        self.right: list[int] = [-1]
        self.parent: list[int] = [-1]
        self.value: list[Any] = [value]
        self.alive: list[bool] = [True]
        self._leaves = 1
        self._internal = 0

    def is_leaf(self, v: int) -> bool:
        return self.left[v] == -1

    def predict(self, x: Sequence[Any]) -> Any:
        """Return the value of the leaf whose cell holds x. Cost: O(depth) tests."""
        return self.value[self.leaf_of(x)]

    def leaf_of(self, x: Sequence[Any]) -> int:
        """Return the id of the leaf reached by x. Cost: O(depth) tests."""
        v = 0  # @line L1
        while self.left[v] != -1:  # @line L2
            if x[self.feature[v]] <= self.threshold[v]:  # @line L3
                v = self.left[v]  # @line L3
            else:
                v = self.right[v]  # @line L4
        return v  # @line L5

    def _new_leaf(self, parent: int, value: Any) -> int:
        self.feature.append(-1)
        self.threshold.append(None)
        self.left.append(-1)
        self.right.append(-1)
        self.parent.append(parent)
        self.value.append(value)
        self.alive.append(True)
        return len(self.value) - 1

    def split_leaf(self, v: int, j: int, theta: Any, a: Any, b: Any) -> tuple[int, int]:
        """Make leaf v test x[j] <= theta, with new leaves a (true) and b (false).

        Returns the ids of the two new leaves. Cost: O(1).
        """
        if not self.alive[v] or not self.is_leaf(v):
            raise ValueError("split_leaf needs a live leaf")
        self.feature[v], self.threshold[v] = j, theta  # @line L6
        self.left[v] = self._new_leaf(v, a)  # @line L7
        self.right[v] = self._new_leaf(v, b)  # @line L8
        self.value[v] = None
        self._leaves += 1
        self._internal += 1
        return self.left[v], self.right[v]

    def prune(self, v: int, c: Any) -> None:
        """Replace the subtree at the live node v by one leaf with value c.

        Cost: O(size of the removed subtree), with an explicit stack.
        """
        if not self.alive[v]:
            raise ValueError("prune needs a live node")
        stack = [v]
        while stack:  # @line L9
            u = stack.pop()
            if self.left[u] == -1:
                self._leaves -= 1
            else:
                self._internal -= 1
                stack += [self.left[u], self.right[u]]
            if u != v:
                self.alive[u] = False
        self.feature[v], self.threshold[v] = -1, None
        self.left[v] = self.right[v] = -1  # @line L10
        self.value[v] = c
        self._leaves += 1

    def n_leaves(self) -> int:
        return self._leaves

    def size(self) -> int:
        """The number of nodes, internal and leaves."""
        return self._leaves + self._internal

    def depth(self) -> int:
        """The largest number of tests on a root-to-leaf path. Cost: O(size)."""
        best, stack = 0, [(0, 0)]
        while stack:
            u, dep = stack.pop()
            if self.left[u] == -1:
                best = max(best, dep)
            else:
                stack += [(self.left[u], dep + 1), (self.right[u], dep + 1)]
        return best

    def leaves(self) -> list[int]:
        """The ids of the live leaves, left to right."""
        out, stack = [], [0]
        while stack:
            u = stack.pop()
            if self.left[u] == -1:
                out.append(u)
            else:
                stack += [self.right[u], self.left[u]]
        return out

    def cell(self, v: int) -> dict[int, list[Any]]:
        """The box of node v: for each tested feature j, bounds [lo, hi] meaning lo < x[j] <= hi.

        A bound None means no limit. Cost: O(depth).
        """
        box: dict[int, list[Any]] = {}
        u = v
        while self.parent[u] != -1:
            p = self.parent[u]
            j, t = self.feature[p], self.threshold[p]
            lo, hi = box.setdefault(j, [None, None])
            if u == self.left[p]:
                if hi is None or t < hi:
                    box[j][1] = t
            elif lo is None or t > lo:
                box[j][0] = t
            u = p
        return box

    def check_invariant(self) -> None:
        """Each internal node has two live children whose parent is it; counts agree."""
        leaves = internal = 0
        stack = [0]
        while stack:
            u = stack.pop()
            assert self.alive[u]
            if self.left[u] == -1:
                assert self.right[u] == -1
                leaves += 1
            else:
                internal += 1
                for c in (self.left[u], self.right[u]):
                    assert c != -1 and self.parent[c] == u
                    stack.append(c)
        assert leaves == self._leaves and internal == self._internal
        assert leaves == internal + 1
