# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/m-tree/. The authors are listed in prov/GE79TV.jsonl.

import heapq
import itertools
import math
from dataclasses import dataclass, field
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar("T")
Metric = Callable[[T, T], float]


@dataclass
class Entry(Generic[T]):
    obj: T
    radius: float = 0.0  # covering radius; 0 in a leaf
    child: Optional["Node[T]"] = None  # None in a leaf
    dparent: Optional[float] = None  # distance to the routing object of the parent entry; None at the root


@dataclass
class Node(Generic[T]):
    leaf: bool
    entries: list[Entry[T]] = field(default_factory=list)


def _balanced(n: int, dm: list[list[float]], i: int, j: int) -> tuple[list[int], list[int]]:
    """Split range(n) between the promoted entries i and j, taking turns, each its nearest free entry."""
    free = set(range(n)) - {i, j}
    a, b = [i], [j]
    turn = 0
    while free:
        part, p = (a, i) if turn == 0 else (b, j)
        t = min(free, key=lambda t: (dm[t][p], t))
        part.append(t)
        free.remove(t)
        turn ^= 1
    return a, b


class MTree(Generic[T]):
    """An M-tree with node capacity M >= 2, insertion one object at a time, range and k-NN queries.

    A split promotes the pair of entries that minimizes the larger covering radius (mM_RAD),
    with the balanced partition: the two promoted objects take turns picking their nearest
    remaining entry. Every node but the root then holds at least floor((M + 1) / 2) entries.
    evaluations counts metric calls.
    """

    def __init__(self, d: Metric, capacity: int = 4) -> None:
        if capacity < 2:
            raise ValueError("capacity must be at least 2")
        self._d, self.M = d, capacity
        self.root: Node[T] = Node(leaf=True)
        self.evaluations = 0
        self.size = 0

    def dist(self, a: T, b: T) -> float:
        self.evaluations += 1
        return self._d(a, b)

    # ---------- queries ----------

    def range(self, q: T, r: float) -> list[T]:
        """All stored objects x with d(q, x) <= r."""
        out: list[T] = []
        self._range(self.root, q, r, None, out)
        return out

    def _range(self, node: Node[T], q: T, r: float, dqp: Optional[float], out: list[T]) -> None:
        for e in node.entries:  # @line L1
            if dqp is not None and abs(dqp - e.dparent) > r + e.radius:  # @line L2
                continue
            de = self.dist(q, e.obj)  # @line L3
            if node.leaf:  # @line L4
                if de <= r:  # @line L5
                    out.append(e.obj)
            elif de <= r + e.radius:  # @line L6
                self._range(e.child, q, r, de, out)  # @line L7

    def knn(self, q: T, k: int) -> list[tuple[float, T]]:
        """The k nearest stored objects with their distances, nearest first (ties in any order)."""
        if k <= 0:
            return []
        tick = itertools.count()
        best: list[tuple[float, int, T]] = []  # max-heap by negated distance
        tau = math.inf
        pq: list[tuple[float, int, Node[T], Optional[float]]] = [(0.0, next(tick), self.root, None)]
        while pq:  # @line L8
            dmin, _, node, dqp = heapq.heappop(pq)  # @line L9
            if dmin > tau:  # @line L10
                break
            for e in node.entries:  # @line L11
                if dqp is not None and abs(dqp - e.dparent) - e.radius > tau:  # @line L12
                    continue
                de = self.dist(q, e.obj)  # @line L13
                if node.leaf:
                    if de < tau or len(best) < k:  # @line L14
                        heapq.heappush(best, (-de, next(tick), e.obj))
                        if len(best) > k:
                            heapq.heappop(best)
                        if len(best) == k:
                            tau = -best[0][0]
                else:
                    lb = max(de - e.radius, 0.0)
                    if lb <= tau:  # @line L15
                        heapq.heappush(pq, (lb, next(tick), e.child, de))
        return sorted(((-nd, x) for nd, _, x in best), key=lambda t: t[0])  # @line L16

    # ---------- insertion ----------

    def insert(self, x: T) -> None:
        split = self._insert(self.root, x, None, None)
        if split is not None:  # @line L17
            self.root = Node(leaf=False, entries=list(split))
        self.size += 1

    def _insert(self, node: Node[T], x: T, pobj: Optional[T], dxp: Optional[float]):
        """Insert x below node; pobj is the routing object of node (None at the root), dxp = d(x, pobj)."""
        if node.leaf:  # @line L18
            node.entries.append(Entry(x, dparent=dxp))
        else:
            ds = [self.dist(x, e.obj) for e in node.entries]  # @line L19
            inside = [i for i, e in enumerate(node.entries) if ds[i] <= e.radius]
            if inside:  # @line L20
                i = min(inside, key=lambda i: ds[i])
            else:
                i = min(range(len(ds)), key=lambda i: ds[i] - node.entries[i].radius)
                node.entries[i].radius = ds[i]  # @line L21
            e = node.entries[i]
            split = self._insert(e.child, x, e.obj, ds[i])  # @line L22
            if split is not None:
                for s2 in split:
                    s2.dparent = None if pobj is None else self.dist(s2.obj, pobj)
                node.entries[i : i + 1] = list(split)
        if len(node.entries) > self.M:  # @line L23
            return self._split(node)
        return None

    def _split(self, node: Node[T]) -> tuple[Entry[T], Entry[T]]:
        es = node.entries
        n = len(es)
        dm = [[0.0] * n for _ in range(n)]
        for i in range(n):  # @line L24
            for j in range(i + 1, n):
                dm[i][j] = dm[j][i] = self.dist(es[i].obj, es[j].obj)
        best = None
        for i in range(n):  # @line L25
            for j in range(i + 1, n):
                a, b = _balanced(n, dm, i, j)
                ra = max(dm[t][i] + es[t].radius for t in a)
                rb = max(dm[t][j] + es[t].radius for t in b)
                if best is None or max(ra, rb) < best[0]:
                    best = (max(ra, rb), i, j, a, b, ra, rb)
        _, i, j, a, b, ra, rb = best
        out = []
        for p, part, rad in ((i, a, ra), (j, b, rb)):  # @line L26
            child = Node(node.leaf, [es[t] for t in part])
            for t in part:
                es[t].dparent = dm[t][p]
            out.append(Entry(es[p].obj, rad, child))
        return out[0], out[1]  # @line L27
