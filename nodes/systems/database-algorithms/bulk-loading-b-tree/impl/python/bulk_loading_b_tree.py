# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bulk-loading-b-tree/. The authors are listed in prov/BKKK4M.jsonl.

"""Bulk loading of a B+ tree of order d, bottom up.

Each node other than the root holds d to 2d keys: a leaf holds d to 2d
entries, an internal node d to 2d separators, so d + 1 to 2d + 1 children.
BULK-LOAD sorts the entries, packs them into leaves to a fill factor, links
the leaves, and builds each index level from the level below. It writes each
node once. The sort here is Python's sorted, which stands for an external
merge sort when the entries do not fit in memory.

For comparison, `insert` is the classic one-at-a-time B+ tree insertion with
splits, and counts the nodes it touches.
"""

from bisect import bisect_right
from fractions import Fraction
from typing import Any, Iterable, List, Optional, Sequence, Tuple


class Node:
    __slots__ = ("leaf", "keys", "values", "children", "next", "low")

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.keys: List[Any] = []          # entries (leaf) or separators (internal)
        self.values: List[Any] = []        # leaf only
        self.children: List["Node"] = []   # internal only
        self.next: Optional["Node"] = None  # leaf chain
        self.low: Any = None               # smallest key in the subtree


def _clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))


def pack(items: Sequence[Any], t: int, lo: int, hi: int) -> List[List[Any]]:
    """Cut items into groups of t; repair a short last group. lo <= t <= hi."""
    groups = [list(items[i:i + t]) for i in range(0, len(items), t)]   # @line L10
    if len(groups) >= 2 and len(groups[-1]) < lo:                      # @line L11
        m = groups[-2] + groups[-1]                                    # @line L12
        del groups[-2:]                                                # @line L12
        if len(m) <= hi:                                               # @line L13
            groups.append(m)                                           # @line L13
        else:
            half = len(m) // 2                                         # @line L14
            groups.extend([m[:half], m[half:]])                        # @line L14
    return groups                                                      # @line L15


class BPlusTree:
    def __init__(self, d: int) -> None:
        if d < 1:
            raise ValueError("order d must be at least 1")
        self.d = d
        self.root: Optional[Node] = None
        self.node_accesses = 0     # nodes read or written by insert

    # ------------------------------------------------------------ bulk load

    @classmethod
    def bulk_load(cls, entries: Iterable[Tuple[Any, Any]], d: int,
                  fill: Fraction = Fraction(1)) -> "BPlusTree":
        """Build a tree from (key, value) pairs with distinct keys.

        Cost: one sort, then O(n) time; it creates at most L + (L + d - 2) / d
        nodes for L leaves, each once.
        """
        if not 0 < fill <= 1:
            raise ValueError("fill must be in (0, 1]")
        tree = cls(d)
        e = sorted(entries, key=lambda kv: kv[0])                          # @line L1
        for i in range(1, len(e)):
            if e[i - 1][0] == e[i][0]:
                raise ValueError("keys must be distinct")
        t = _clamp(int(fill * 2 * d), d, 2 * d)                            # @line L2
        level: List[Node] = []
        for g in pack(e, t, d, 2 * d):                                     # @line L3
            leaf = Node(True)
            leaf.keys = [k for k, _ in g]
            leaf.values = [v for _, v in g]
            leaf.low = leaf.keys[0]
            if level:
                level[-1].next = leaf
            level.append(leaf)
        if not level:                                                      # @line L4
            return tree                                                    # @line L4
        u = _clamp(int(fill * (2 * d + 1)), d + 1, 2 * d + 1)              # @line L5
        while len(level) > 1:                                              # @line L6
            parents = []
            for g in pack(level, u, d + 1, 2 * d + 1):                     # @line L7
                node = Node(False)                                         # @line L8
                node.children = g                                          # @line L8
                node.keys = [c.low for c in g[1:]]                         # @line L8
                node.low = g[0].low
                parents.append(node)
            level = parents
        tree.root = level[0]                                               # @line L9
        return tree

    # ------------------------------------------------------------ queries

    def search(self, key: Any) -> Any:
        node = self.root
        if node is None:
            return None
        while not node.leaf:
            node = node.children[bisect_right(node.keys, key)]
        i = bisect_right(node.keys, key) - 1
        return node.values[i] if i >= 0 and node.keys[i] == key else None

    def items(self) -> List[Tuple[Any, Any]]:
        """All entries in key order, by the leaf chain."""
        node = self.root
        if node is None:
            return []
        while not node.leaf:
            node = node.children[0]
        out = []
        while node is not None:
            out.extend(zip(node.keys, node.values))
            node = node.next
        return out

    def levels(self) -> List[List[Node]]:
        if self.root is None:
            return []
        out, level = [], [self.root]
        while level:
            out.append(level)
            level = [c for n in level for c in n.children]
        return out

    # ------------------------------------------------------------ insert

    def insert(self, key: Any, value: Any) -> None:
        """Insert one entry top down with splits (the method bulk loading replaces)."""
        d = self.d
        if self.root is None:
            self.root = Node(True)
        path, node = [], self.root
        while not node.leaf:
            self.node_accesses += 1
            path.append(node)
            node = node.children[bisect_right(node.keys, key)]
        self.node_accesses += 1
        i = bisect_right(node.keys, key)
        if i > 0 and node.keys[i - 1] == key:
            node.values[i - 1] = value
            return
        node.keys.insert(i, key)
        node.values.insert(i, value)
        split: Optional[Tuple[Any, Node]] = None
        if len(node.keys) > 2 * d:
            right = Node(True)
            right.keys, node.keys = node.keys[d:], node.keys[:d]
            right.values, node.values = node.values[d:], node.values[:d]
            right.next, node.next = node.next, right
            self.node_accesses += 1
            split = (right.keys[0], right)
        while split is not None and path:
            parent = path.pop()
            sep, right_node = split
            j = bisect_right(parent.keys, sep)
            parent.keys.insert(j, sep)
            parent.children.insert(j + 1, right_node)
            split = None
            if len(parent.keys) > 2 * d:
                right = Node(False)
                up = parent.keys[d]
                right.keys, parent.keys = parent.keys[d + 1:], parent.keys[:d]
                right.children, parent.children = parent.children[d + 1:], parent.children[:d + 1]
                self.node_accesses += 1
                split = (up, right)
        if split is not None:
            new_root = Node(False)
            new_root.keys = [split[0]]
            new_root.children = [self.root, split[1]]
            self.root = new_root
            self.node_accesses += 1

    # ------------------------------------------------------------ invariant

    def check_invariant(self) -> None:
        """All leaves at one depth, keys in order, separators bound subtrees, fill bounds."""
        d = self.d
        if self.root is None:
            return
        leaf_depths = set()
        stack = [(self.root, 0, None, None)]
        while stack:
            node, depth, lo, hi = stack.pop()
            assert node.keys == sorted(node.keys)
            assert len(set(node.keys)) == len(node.keys)
            for k in node.keys:
                assert lo is None or k >= lo
                assert hi is None or k < hi
            is_root = node is self.root
            if node.leaf:
                leaf_depths.add(depth)
                assert len(node.keys) == len(node.values)
                assert len(node.keys) <= 2 * d
                assert is_root or len(node.keys) >= d
            else:
                assert len(node.children) == len(node.keys) + 1
                assert len(node.keys) <= 2 * d
                assert len(node.keys) >= (1 if is_root else d)
                bounds = [lo] + node.keys + [hi]
                for i, c in enumerate(node.children):
                    stack.append((c, depth + 1, bounds[i], bounds[i + 1]))
        assert len(leaf_depths) == 1
        # the leaf chain visits all leaves left to right
        leaves = self.levels()[-1]
        for a, b in zip(leaves, leaves[1:]):
            assert a.next is b
        assert leaves[-1].next is None
