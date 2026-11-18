# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefix-b-tree/. The authors are listed in prov/AJZDXP.jsonl.

"""Prefix B-tree (Bayer and Unterauer 1977) on string keys.

A B+ tree: the keys are in the leaves, and the inner nodes hold separators.
A separator s between a left node and a right node satisfies
left keys < s <= right keys. Two ideas of the paper are used:

* simple prefix B-tree: a leaf split puts the shortest separator between the
  two halves into the parent, and the split point is chosen inside a split
  interval of 2 d + 1 positions so that this separator is short;
* prefix B-tree: every key in a node lies between the two fences of the node
  (the separators that bound it in its parent, or the fences of the parent),
  so all keys of the node start with the common prefix of the fences. The
  node stores its keys and separators without that prefix.

Capacity is counted in entries to keep the code short; real systems count
bytes, which is where short separators pay off.
"""

from bisect import bisect_left, bisect_right, insort
from typing import Iterator, List, Optional, Tuple


def shortest_separator(a: str, b: str) -> str:
    """SHORTEST-SEPARATOR: the shortest s with a < s <= b, for a < b."""
    if not a < b:
        raise ValueError("need a < b")
    i = 0                                                    # @line L1
    while i < len(a) and a[i] == b[i]:                       # @line L2
        i += 1                                               # @line L2
    return b[: i + 1]                                        # @line L3


def common_prefix(low: Optional[str], high: Optional[str]) -> str:
    """The prefix that every key in [low, high) has. An open end gives ''."""
    if low is None or high is None:
        return ""
    i = 0
    while i < len(low) and i < len(high) and low[i] == high[i]:
        i += 1
    return low[:i]


class Node:
    """A node with fences [low, high). keys holds suffixes after the prefix.

    In a leaf, keys are the stored keys. In an inner node, keys are the
    separators, and len(children) == len(keys) + 1.
    """

    def __init__(self, leaf: bool, low: Optional[str], high: Optional[str]):
        self.leaf = leaf
        self.low = low
        self.high = high
        self.prefix = common_prefix(low, high)
        self.keys: List[str] = []
        self.children: List["Node"] = []

    def full_keys(self) -> List[str]:
        return [self.prefix + s for s in self.keys]

    def set_fences(self, low: Optional[str], high: Optional[str]) -> None:
        """Change the fences and store the keys again without the new prefix."""
        full = self.full_keys()
        self.low, self.high = low, high
        self.prefix = common_prefix(low, high)
        self.keys = [k[len(self.prefix):] for k in full]


class PrefixBTree:
    def __init__(self, capacity: int = 4, d: int = 1):
        """capacity: the largest number of keys or separators in a node.

        d: the half width of the split interval (d = 0 splits in the middle).
        """
        if capacity < 3:
            raise ValueError("capacity must be at least 3")
        self.capacity = capacity
        self.d = d
        self.root = Node(True, None, None)

    # ----- search -----

    def _child_index(self, v: Node, k: str) -> int:
        # k lies in [v.low, v.high), so it starts with v.prefix.
        return bisect_right(v.keys, k[len(v.prefix):])      # @line L6

    def _leaf_for(self, k: str) -> Tuple[Node, List[Tuple[Node, int]]]:
        v = self.root                                        # @line L4
        path = []
        while not v.leaf:                                    # @line L5
            j = self._child_index(v, k)                      # @line L6
            path.append((v, j))
            v = v.children[j]                                # @line L7
        return v, path

    def contains(self, k: str) -> bool:
        """SEARCH."""
        v, _ = self._leaf_for(k)
        s = k[len(v.prefix):]
        i = bisect_left(v.keys, s)
        return i < len(v.keys) and v.keys[i] == s            # @line L8

    # ----- insert -----

    def insert(self, k: str) -> bool:
        """Insert k; return False if it was already there."""
        if not isinstance(k, str):
            raise TypeError("keys are strings")
        v, path = self._leaf_for(k)
        s = k[len(v.prefix):]
        i = bisect_left(v.keys, s)
        if i < len(v.keys) and v.keys[i] == s:
            return False
        v.keys.insert(i, s)
        while len(v.keys) > self.capacity:
            parent = path.pop()[0] if path else None
            if v.leaf:
                sep, right = self._split_leaf(v)
            else:
                sep, right = self._split_inner(v)
            if parent is None:
                root = Node(False, None, None)
                root.keys = [sep]
                root.children = [v, right]
                self.root = root
                break
            j = parent.children.index(v)
            parent.keys.insert(j, sep[len(parent.prefix):])  # @line L13
            parent.children.insert(j + 1, right)            # @line L13
            v = parent
        return True

    def _choose(self, n: int, sep_of) -> int:
        """The split index j in the split interval with the shortest separator."""
        c = (n + 1) // 2                                     # @line L9
        lo, hi = max(1, c - self.d), min(n - 1, c + self.d)
        best = None
        for j in range(lo, hi + 1):                          # @line L10
            key = (len(sep_of(j)), abs(j - c), j)
            if best is None or key < best:
                best = key
        return best[2]

    def _split_leaf(self, v: Node) -> Tuple[str, Node]:
        full = v.full_keys()
        n = len(full)
        j = self._choose(n, lambda t: shortest_separator(full[t - 1], full[t]))  # @line L10
        sep = shortest_separator(full[j - 1], full[j])       # @line L11
        right = Node(True, sep, v.high)                      # @line L12
        right.keys = [x[len(right.prefix):] for x in full[j:]]  # @line L14
        v.keys = [x[len(v.prefix):] for x in full[:j]]       # @line L12
        v.set_fences(v.low, sep)                             # @line L14
        return sep, right

    def _split_inner(self, v: Node) -> Tuple[str, Node]:
        full = v.full_keys()
        n = len(full)
        # Separator t moves up; the left node keeps full[:t] and the right full[t+1:].
        t = self._choose(n - 1, lambda u: full[u]) if n > 2 else 1
        sep = full[t]
        right = Node(False, sep, v.high)
        right.keys = [x[len(right.prefix):] for x in full[t + 1:]]
        right.children = v.children[t + 1:]
        v.keys = [x[len(v.prefix):] for x in full[:t]]
        v.children = v.children[: t + 1]
        v.set_fences(v.low, sep)
        self._refence(v)
        self._refence(right)
        return sep, right

    def _refence(self, v: Node) -> None:
        """Give each child of v the fences that v now implies."""
        bounds = [v.low] + v.full_keys() + [v.high]
        for i, c in enumerate(v.children):
            c.set_fences(bounds[i], bounds[i + 1])

    # ----- scans and checks -----

    def range(self, lo: str, hi: str) -> List[str]:
        """All keys k with lo <= k <= hi, in order."""
        out: List[str] = []
        self._collect(self.root, lo, hi, out)
        return out

    def _collect(self, v: Node, lo: str, hi: str, out: List[str]) -> None:
        if v.high is not None and v.high <= lo:
            return
        if v.low is not None and v.low > hi:
            return
        if v.leaf:
            out.extend(k for k in v.full_keys() if lo <= k <= hi)
            return
        for c in v.children:
            self._collect(c, lo, hi, out)

    def keys(self) -> List[str]:
        out: List[str] = []
        self._all(self.root, out)
        return out

    def _all(self, v: Node, out: List[str]) -> None:
        if v.leaf:
            out.extend(v.full_keys())
        else:
            for c in v.children:
                self._all(c, out)

    def height(self) -> int:
        h, v = 1, self.root
        while not v.leaf:
            h, v = h + 1, v.children[0]
        return h

    def stored_chars(self) -> Tuple[int, int]:
        """(characters of separators as stored, characters of the full separators)."""
        stored = full = 0
        stack = [self.root]
        while stack:
            v = stack.pop()
            if not v.leaf:
                stored += sum(len(s) for s in v.keys)
                full += sum(len(s) for s in v.full_keys())
                stack.extend(v.children)
        return stored, full

    def check(self) -> None:
        """Raise AssertionError if an invariant of the page fails."""
        depths = set()
        self._check(self.root, None, None, 1, depths)
        assert len(depths) == 1, "leaves at different depths"

    def _check(self, v: Node, low, high, depth, depths) -> None:
        assert v.low == low and v.high == high, "wrong fences"
        assert v.prefix == common_prefix(low, high)
        full = v.full_keys()
        assert full == sorted(full) and len(set(full)) == len(full)
        assert len(full) <= self.capacity
        for k in full:
            assert low is None or low <= k
            assert high is None or k < high
        if v.leaf:
            depths.add(depth)
            return
        assert len(v.children) == len(v.keys) + 1
        bounds = [low] + full + [high]
        for i, c in enumerate(v.children):
            self._check(c, bounds[i], bounds[i + 1], depth + 1, depths)
