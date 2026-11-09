# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-range-search/. The authors are listed in prov/JZANN9.jsonl.

"""Range search in a binary search tree: report every key in the closed range [lo, hi].

The tree keeps the order rule "left keys < node key <= right keys", so equal keys go right.
RANGE-SEARCH is the pruned in-order traversal of the page, run with an explicit stack so that a
degenerate tree of height n does not overflow the Python stack.

Cost: O(H + k) time, where H is the height of the tree and k the number of reported keys;
O(log n + k) on a balanced tree. Extra space O(H) for the stack.
"""

from typing import Any, List, Optional


class Node:
    """One node of the tree."""

    __slots__ = ("key", "left", "right")

    def __init__(self, key: Any) -> None:
        self.key = key
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None


def insert(root: Optional[Node], key: Any) -> Node:
    """Insert key without balancing (equal keys go right). Returns the root. O(H) time."""
    new = Node(key)
    if root is None:
        return new
    x = root
    while True:
        if key < x.key:
            if x.left is None:
                x.left = new
                return root
            x = x.left
        else:
            if x.right is None:
                x.right = new
                return root
            x = x.right


def build_balanced(keys: List[Any]) -> Optional[Node]:
    """Build a tree of height at most ceil(lg(n + 1)) + (number of equal keys) from any keys.

    The root of a sorted part is the first copy of its middle key, so every key on the left
    is smaller and every key on the right is at least as large. O(n log n) time.
    """
    a = sorted(keys)
    if not a:
        return None
    root_holder: List[Optional[Node]] = [None]
    # Each task: (lo, hi, parent, is_left); lo..hi-1 is a nonempty part of a.
    tasks = [(0, len(a), None, False)]
    while tasks:
        lo, hi, parent, is_left = tasks.pop()
        mid = (lo + hi) // 2
        while mid > lo and a[mid - 1] == a[mid]:
            mid -= 1
        node = Node(a[mid])
        if parent is None:
            root_holder[0] = node
        elif is_left:
            parent.left = node
        else:
            parent.right = node
        if lo < mid:
            tasks.append((lo, mid, node, True))
        if mid + 1 < hi:
            tasks.append((mid + 1, hi, node, False))
    return root_holder[0]


def range_search(root: Optional[Node], lo: Any, hi: Any, stats: Optional[dict] = None) -> List[Any]:
    """Return the keys k with lo <= k <= hi in non-decreasing order.

    Precondition: the tree obeys "left < key <= right". If stats is a dict, stats["visited"]
    receives the number of nodes that the search entered. Time O(H + k).
    """
    out: List[Any] = []
    visited = 0
    # A frame is (node, stage): stage 0 = not yet started, stage 1 = left part done.
    stack: List[tuple] = [(root, 0)]
    while stack:
        x, stage = stack.pop()
        if stage == 0:
            if x is None:  # @line L1
                continue
            visited += 1
            stack.append((x, 1))
            if lo < x.key:  # @line L2
                stack.append((x.left, 0))  # @line L3
        else:
            if lo <= x.key <= hi:  # @line L4
                out.append(x.key)  # @line L5
            if x.key <= hi:  # @line L6
                stack.append((x.right, 0))  # @line L7
    if stats is not None:
        stats["visited"] = visited
    return out


def height(root: Optional[Node]) -> int:
    """Number of nodes on the longest root-to-leaf path (0 for the empty tree)."""
    best = 0
    stack = [(root, 1)]
    while stack:
        x, d = stack.pop()
        if x is not None:
            best = max(best, d)
            stack.append((x.left, d + 1))
            stack.append((x.right, d + 1))
    return best
