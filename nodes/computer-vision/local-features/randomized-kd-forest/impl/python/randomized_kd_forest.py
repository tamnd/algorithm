# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-kd-forest/. The authors are listed in prov/GS7MJP.jsonl.

"""A randomized k-d forest (Silpa-Anan and Hartley 2008, Muja and Lowe 2009).

Points are tuples of floats of the same dimension d. The forest holds T k-d
trees over the same points. Each internal node splits at the mean of one
dimension, drawn uniformly at random from the D dimensions of largest
variance of its points (D = 5 in FLANN). Points with x[j] < mean go left,
the others go right. A leaf holds at most `leaf_size` points, or any number
of equal points.

FLANN estimates the mean and the variance from the first 100 points of a
node; this code uses all the points of the node, which changes the trees but
not the method.

The search keeps one min-priority queue for all trees, keyed by the squared
distance from the query to the bin of each subtree. A set of seen points
makes sure that each point is checked once, even if it is reached in several
trees. The search stops after `checks` points, or when the next bin is not
closer than the current k-th neighbor; in the second case the answer is
exact. The bin distance replaces the offset of a dimension when the path
crosses a second split on it, so it is a true lower bound.
"""

import heapq
import math
import random
from typing import List, Optional, Sequence, Tuple

Point = Tuple[float, ...]


class Node:
    __slots__ = ("dim", "split", "left", "right", "ids")

    def __init__(self):
        self.dim = -1  # -1 for a leaf
        self.split = 0.0
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.ids: List[int] = []


def sqdist(p: Sequence[float], q: Sequence[float]) -> float:
    return sum((a - b) * (a - b) for a, b in zip(p, q))


class RandomizedKDForest:
    def __init__(self, points: Sequence[Point] = (), trees: int = 4, top_dims: int = 5,
                 leaf_size: int = 1, seed: int = 0, dim: Optional[int] = None):
        if trees < 1 or top_dims < 1 or leaf_size < 1:
            raise ValueError("trees, top_dims and leaf_size must be at least 1")
        self.points: List[Point] = [tuple(p) for p in points]
        self.dim = dim if dim is not None else (len(self.points[0]) if self.points else 0)
        self.top_dims = top_dims
        self.leaf_size = leaf_size
        self.rng = random.Random(seed)
        ids = list(range(len(self.points)))
        self.roots = [self._make(ids) for _ in range(trees)]  # @line L1

    def _make(self, ids: List[int]) -> Node:
        node = Node()
        self._fill(node, ids)
        return node

    def _fill(self, node: Node, ids: List[int]) -> None:
        pts = self.points
        if len(ids) <= self.leaf_size:  # @line L2
            node.dim, node.ids = -1, list(ids)
            return
        n = len(ids)
        mean = [sum(pts[i][j] for i in ids) / n for j in range(self.dim)]  # @line L3
        var = [sum((pts[i][j] - mean[j]) ** 2 for i in ids) / n for j in range(self.dim)]
        order = sorted((j for j in range(self.dim) if var[j] > 0.0), key=lambda j: (-var[j], j))
        if not order:  # all points equal: one leaf
            node.dim, node.ids = -1, list(ids)
            return
        cand = order[: self.top_dims]  # @line L4
        j = cand[self.rng.randrange(len(cand))]  # @line L5
        s = mean[j]
        left = [i for i in ids if pts[i][j] < s]  # @line L6
        right = [i for i in ids if pts[i][j] >= s]
        if not left or not right:  # rounding of the mean; split below the largest value instead
            s = max(pts[i][j] for i in ids)
            left = [i for i in ids if pts[i][j] < s]
            right = [i for i in ids if pts[i][j] >= s]
        node.dim, node.split, node.ids = j, s, []  # @line L7
        node.left, node.right = self._make(left), self._make(right)

    def insert(self, p: Sequence[float]) -> int:
        """Add a point to every tree and return its index."""
        p = tuple(p)
        if not self.points and self.dim == 0:
            self.dim = len(p)
        i = len(self.points)
        self.points.append(p)  # @line L8
        for root in self.roots:  # @line L9
            node = root
            while node.dim >= 0:  # @line L10
                node = node.left if p[node.dim] < node.split else node.right
            node.ids.append(i)  # @line L11
            if len(node.ids) > self.leaf_size:  # @line L12
                self._fill(node, node.ids)
        return i

    def search(self, q: Sequence[float], k: int = 1, checks: float = math.inf
               ) -> Tuple[List[Tuple[float, int]], bool, int]:
        """Return (neighbors, exact, evaluations).

        neighbors: up to k pairs (squared distance, index), sorted.
        exact: True when the search proved that these are the k nearest.
        evaluations: the number of distance computations, at most one per point.
        """
        best: List[Tuple[float, int]] = []  # @line L13
        seen = set()
        checked = 0
        d = self.dim
        count = 0
        queue = []
        for root in self.roots:  # @line L14
            queue.append((0.0, count, root, (0.0,) * d))
            count += 1
        heapq.heapify(queue)
        exact = True
        while queue:  # @line L15
            if checked >= checks:
                exact = False
                break
            b, _, node, off = heapq.heappop(queue)  # @line L16
            if len(best) == k and b >= -best[0][0]:  # @line L17
                break
            while node.dim >= 0:  # @line L18
                delta = q[node.dim] - node.split  # @line L19
                if delta < 0:  # @line L20
                    near, far = node.left, node.right
                else:
                    near, far = node.right, node.left
                old = off[node.dim]  # @line L21
                count += 1
                heapq.heappush(queue, (b - old * old + delta * delta, count, far,
                                       off[: node.dim] + (delta,) + off[node.dim + 1:]))
                node = near  # @line L22
            for i in node.ids:  # @line L23
                if i in seen:
                    continue
                seen.add(i)  # @line L24
                checked += 1
                item = (-sqdist(self.points[i], q), -i)
                if len(best) < k:
                    heapq.heappush(best, item)
                elif item > best[0]:
                    heapq.heapreplace(best, item)
        return sorted((-a, -b) for a, b in best), exact, checked  # @line L25

    def check_invariant(self) -> None:
        """Raise AssertionError if a tree misses a point or breaks a split."""
        n = len(self.points)
        for root in self.roots:
            found: List[int] = []
            stack = [(root, [-math.inf] * self.dim, [math.inf] * self.dim)]
            while stack:
                node, lo, hi = stack.pop()
                if node.dim < 0:
                    assert len(node.ids) <= self.leaf_size or len(set(self.points[i] for i in node.ids)) == 1
                    for i in node.ids:
                        p = self.points[i]
                        assert all(lo[t] <= p[t] < hi[t] for t in range(self.dim))
                    found.extend(node.ids)
                    continue
                j, s = node.dim, node.split
                hl = list(hi)
                hl[j] = min(hi[j], s)
                ll = list(lo)
                ll[j] = max(lo[j], s)
                stack.append((node.left, lo, hl))
                stack.append((node.right, ll, hi))
            assert sorted(found) == list(range(n))


def brute_force(points: Sequence[Point], q: Sequence[float], k: int = 1) -> List[Tuple[float, int]]:
    return sorted((sqdist(p, q), i) for i, p in enumerate(points))[:k]
