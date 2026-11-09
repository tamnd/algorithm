# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree-nearest-neighbor-search/. The authors are listed in prov/GXNZ91.jsonl.

from fractions import Fraction
from typing import Optional, Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, ...]


class Node:
    __slots__ = ("point", "axis", "left", "right")

    def __init__(self, point: Point, axis: int, left: "Optional[Node]", right: "Optional[Node]") -> None:
        self.point = point
        self.axis = axis
        self.left = left
        self.right = right


def dist2(p: Sequence[Number], q: Sequence[Number]) -> Number:
    """Squared Euclidean distance; exact for int and Fraction coordinates."""
    return sum((a - b) * (a - b) for a, b in zip(p, q))


def build(points: list[Point], depth: int = 0) -> Optional[Node]:
    """Build a kd-tree by splitting at the median of the axis depth mod d.

    Left subtree points have coordinate <= the node's, right subtree points >=. Duplicates are kept.
    Cost: O(n log^2 n) time with a sort per level, depth about lg n.
    """
    if not points:
        return None
    d = len(points[0])
    axis = depth % d
    pts = sorted(points, key=lambda p: p[axis])
    m = len(pts) // 2
    return Node(pts[m], axis, build(pts[:m], depth + 1), build(pts[m + 1:], depth + 1))


def nearest(root: Optional[Node], q: Point, stats: Optional[list[int]] = None) -> Optional[tuple[Number, Point]]:
    """Return (squared distance, point) for a nearest point of the tree to q, or None if the tree is empty.

    Every test compares squared distances exactly. If stats is a one-element list, the number of
    visited nodes is added to stats[0]. Cost: O(n) worst case, O(log n) expected on well-spread data;
    recursion depth equals the tree height.
    """
    # best = [d2, point]; d2 = None stands for infinity.
    best: list = [None, None]  # @line L1

    def nn(node: Optional[Node]) -> None:
        if node is None:  # @line L4
            return
        if stats is not None:
            stats[0] += 1
        p, a = node.point, node.axis  # @line L5
        d = dist2(q, p)
        if best[0] is None or d < best[0]:  # @line L6
            best[0], best[1] = d, p
        diff = q[a] - p[a]  # @line L7
        if diff < 0:  # @line L8
            near, far = node.left, node.right
        else:
            near, far = node.right, node.left
        nn(near)  # @line L9
        if best[0] is None or diff * diff < best[0]:  # @line L10
            nn(far)
        return

    nn(root)  # @line L2
    if best[1] is None:
        return None
    return best[0], best[1]  # @line L3
