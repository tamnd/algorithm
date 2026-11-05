# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rp-tree/. The authors are listed in prov/58J4K4.jsonl.

import heapq
import math
import random
from typing import Sequence


class _Node:
    __slots__ = ("v", "t", "left", "right", "items")

    def __init__(self, v=None, t=0.0, left=None, right=None, items=None):
        self.v, self.t, self.left, self.right, self.items = v, t, left, right, items


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


class RPTree:
    """Random projection tree with median splits along random unit directions.

    points: a sequence of equal-length vectors; leaf_size: the largest leaf n0; directions: optional list of
    directions used in the preorder of node creation (for examples), else Gaussian directions from seed.
    """

    def __init__(self, points: Sequence[Sequence[float]], leaf_size: int = 8, seed: int = 0, directions=None):
        if leaf_size < 1:
            raise ValueError("leaf_size must be at least 1")
        self.points = [tuple(map(float, p)) for p in points]
        self.leaf_size = leaf_size
        self._rng = random.Random(seed)
        self._dirs = list(directions) if directions is not None else None
        self.evaluations = 0
        self.root = self._build(list(range(len(self.points))))

    def _direction(self) -> tuple[float, ...]:
        dim = len(self.points[0])
        if self._dirs:
            v = tuple(map(float, self._dirs.pop(0)))
        else:
            v = tuple(self._rng.gauss(0.0, 1.0) for _ in range(dim))
        norm = math.sqrt(_dot(v, v))
        return tuple(x / norm for x in v)

    def _build(self, idx: list[int]) -> _Node:
        if len(idx) <= self.leaf_size:  # @line L1
            return _Node(items=idx)
        v = self._direction()  # @line L2
        proj = sorted(_dot(v, self.points[i]) for i in idx)
        t = proj[(len(idx) - 1) // 2]  # @line L3
        left = [i for i in idx if _dot(v, self.points[i]) <= t]  # @line L4
        right = [i for i in idx if _dot(v, self.points[i]) > t]
        if not right:  # @line L5
            return _Node(items=idx)
        return _Node(v, t, self._build(left), self._build(right))  # @line L6

    def leaves(self) -> list[list[int]]:
        out, stack = [], [self.root]
        while stack:
            node = stack.pop()
            if node.items is not None:
                out.append(node.items)
            else:
                stack += [node.right, node.left]
        return out

    def depth(self, node=None) -> int:
        node = self.root if node is None else node
        if node.items is not None:
            return 0
        return 1 + max(self.depth(node.left), self.depth(node.right))

    def leaf_of(self, q: Sequence[float]) -> list[int]:
        """The leaf that a defeatist search for q reaches."""
        node = self.root
        while node.items is None:
            node = node.left if _dot(node.v, q) - node.t <= 0 else node.right
        return node.items

    def query(self, q: Sequence[float], k: int = 1) -> list[tuple[float, int]]:
        """The k nearest points to q, exactly, as sorted (distance, index) pairs."""
        self.evaluations = 0
        heap: list[tuple[float, int]] = []  # max-heap of (-dist, -idx)
        if k <= 0 or not self.points:
            return []

        def worst() -> tuple[float, int]:
            return (-heap[0][0], -heap[0][1])

        def visit(node: _Node) -> None:
            if node.items is not None:  # @line L7
                for i in node.items:
                    self.evaluations += 1
                    item = (math.dist(q, self.points[i]), i)
                    if len(heap) < k:
                        heapq.heappush(heap, (-item[0], -item[1]))
                    elif item < worst():
                        heapq.heapreplace(heap, (-item[0], -item[1]))
                return
            g = _dot(node.v, q) - node.t  # @line L8
            near, far = (node.left, node.right) if g <= 0 else (node.right, node.left)  # @line L9
            visit(near)  # @line L10
            if len(heap) < k or abs(g) <= worst()[0] * (1 + 1e-12) + 1e-12:  # @line L11
                visit(far)

        visit(self.root)
        return sorted((-a, -b) for a, b in heap)
