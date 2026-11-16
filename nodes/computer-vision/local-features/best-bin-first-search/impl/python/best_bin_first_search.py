# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-bin-first-search/. The authors are listed in prov/THZZ2G.jsonl.

"""Best bin first (BBF) search in a k-d tree (Beis and Lowe 1997).

Points are tuples of floats of the same dimension d. The tree is the
standard k-d tree of Beis and Lowe: each internal node splits on the
dimension of greatest variance of its points, at the median point. A leaf
holds at most `leaf_size` points (1 in the paper).

The search keeps a min-priority queue of subtrees that it has not explored.
The key of a subtree is the squared distance from the query to its bin (the
box of points that the subtree can hold), so the queue gives the bins in
order of increasing distance. The search stops after it has examined
`max_leaves` leaves, which makes it approximate, or when the next bin is
not closer than the current k-th neighbor, which makes the answer exact.

The bin distance is kept with one offset per dimension: the signed distance
from the query to the last split on that dimension that the path crossed to
the far side. The squared distance to the bin is the sum of the squared
offsets, and one crossing changes one term (Arya and Mount 1993).
"""

import heapq
import math
from typing import List, Optional, Sequence, Tuple

Point = Tuple[float, ...]


class Node:
    __slots__ = ("dim", "split", "left", "right", "ids")

    def __init__(self, dim=-1, split=0.0, left=None, right=None, ids=None):
        self.dim = dim  # split dimension, -1 for a leaf
        self.split = split  # left points have x[dim] <= split, right points x[dim] >= split
        self.left = left
        self.right = right
        self.ids = ids  # point indices of a leaf


def _variance(points: Sequence[Point], ids: Sequence[int], d: int) -> float:
    m = sum(points[i][d] for i in ids) / len(ids)
    return sum((points[i][d] - m) ** 2 for i in ids) / len(ids)


def build(points: Sequence[Point], leaf_size: int = 1) -> Optional[Node]:
    """Build the k-d tree of Beis and Lowe: split at the median on the dimension of greatest variance."""
    if not points:
        return None
    dim = len(points[0])

    def make(ids: List[int]) -> Node:
        if len(ids) <= leaf_size:
            return Node(ids=ids)
        var = [_variance(points, ids, d) for d in range(dim)]
        best = max(range(dim), key=lambda d: (var[d], -d))
        if var[best] == 0.0:  # all points equal: one leaf
            return Node(ids=ids)
        ids = sorted(ids, key=lambda i: (points[i][best], i))
        mid = len(ids) // 2
        split = points[ids[mid]][best]
        return Node(best, split, make(ids[:mid]), make(ids[mid:]))

    return make(list(range(len(points))))


def sqdist(p: Sequence[float], q: Sequence[float]) -> float:
    return sum((a - b) * (a - b) for a, b in zip(p, q))


def bbf_search(
    root: Optional[Node],
    points: Sequence[Point],
    q: Sequence[float],
    k: int = 1,
    max_leaves: float = math.inf,
    log: Optional[list] = None,
) -> Tuple[List[Tuple[float, int]], bool]:
    """Return (neighbors, exact).

    neighbors is the list of up to k pairs (squared distance, index), sorted.
    exact is True when the search proved that the list is the true k nearest.
    If log is a list, the search appends (bin distance, leaf ids) for each leaf.
    """
    best: List[Tuple[float, int]] = []  # max-heap by (-dist, -index)  # @line L1
    checked = 0
    if root is None:
        return [], True
    d = len(q)
    count = 0
    queue = [(0.0, count, root, (0.0,) * d)]  # @line L2
    exact = True
    while queue:  # @line L3
        if checked >= max_leaves:
            exact = False
            break
        b, _, node, off = heapq.heappop(queue)  # @line L4
        if len(best) == k and b >= -best[0][0]:  # @line L5
            break
        while node.dim >= 0:  # @line L6
            delta = q[node.dim] - node.split  # @line L7
            if delta < 0:  # @line L8
                near, far = node.left, node.right
            else:
                near, far = node.right, node.left
            old = off[node.dim]  # @line L9
            far_off = off[: node.dim] + (delta,) + off[node.dim + 1:]
            count += 1
            heapq.heappush(queue, (b - old * old + delta * delta, count, far, far_off))  # @line L10
            node = near  # @line L11
        if log is not None:
            log.append((b, list(node.ids)))
        for i in node.ids:  # @line L12
            dist = sqdist(points[i], q)
            item = (-dist, -i)
            if len(best) < k:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)
        checked += 1  # @line L13
    return sorted((-nd, -ni) for nd, ni in best), exact  # @line L14


def brute_force(points: Sequence[Point], q: Sequence[float], k: int = 1) -> List[Tuple[float, int]]:
    """The k nearest points by a full scan, ties broken by the smaller index."""
    return sorted((sqdist(p, q), i) for i, p in enumerate(points))[:k]
