# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mvp-tree/. The authors are listed in prov/WR0RGE.jsonl.

import random
from dataclasses import dataclass, field
from typing import Callable, Generic, Optional, Sequence, TypeVar

T = TypeVar("T")
Metric = Callable[[T, T], float]


@dataclass
class Entry(Generic[T]):
    obj: T
    path: list[float]  # distances to the first p vantage points above it
    d1: float = 0.0
    d2: float = 0.0


@dataclass
class Leaf(Generic[T]):
    v1: Optional[T]
    v2: Optional[T]
    entries: list[Entry[T]]


@dataclass
class Internal(Generic[T]):
    v1: T
    v2: Optional[T]
    # children[i][j] with the interval of d(., v1) of group i and of d(., v2) of subgroup j
    ring1: list[tuple[float, float]]
    ring2: list[list[tuple[float, float]]]
    children: list[list[object]] = field(default_factory=list)


def _split(entries: list[Entry[T]], key: Callable[[Entry[T]], float], m: int) -> list[list[Entry[T]]]:
    """Split by rank of key into m groups of sizes as equal as possible (some may be empty)."""
    s = sorted(entries, key=key)
    n = len(s)
    return [s[(i * n) // m : ((i + 1) * n) // m] for i in range(m)]


def _interval(group: list[Entry[T]], key: Callable[[Entry[T]], float]) -> tuple[float, float]:
    if not group:
        return (1.0, 0.0)  # empty interval, never met
    vals = [key(e) for e in group]
    return (min(vals), max(vals))


class MVPTree(Generic[T]):
    """A multi-vantage-point tree with fan-out m*m, leaf capacity k and p path distances per object.

    choose(n) gives the index of the first vantage point among n candidates; the default is random.
    The second vantage point is the object farthest from the first. evaluations counts metric calls.
    """

    def __init__(self, points: Sequence[T], d: Metric, m: int = 2, k: int = 4, p: int = 4, seed: int = 0,
                 choose: Optional[Callable[[int], int]] = None) -> None:
        if m < 2 or k < 1 or p < 0:
            raise ValueError("need m >= 2, k >= 1, p >= 0")
        self._d, self.m, self.k, self.p = d, m, k, p
        self.evaluations = 0
        rng = random.Random(seed)
        self._choose = choose or rng.randrange
        self.root = self._build([Entry(x, []) for x in points])

    def dist(self, a: T, b: T) -> float:
        self.evaluations += 1
        return self._d(a, b)

    def _push(self, e: Entry[T], value: float) -> None:
        if len(e.path) < self.p:
            e.path.append(value)

    def _vantage_points(self, s: list[Entry[T]]) -> tuple[Optional[Entry[T]], Optional[Entry[T]], list[Entry[T]]]:
        """v1 at random; d1 for the others; v2 the farthest from v1; d2 for the rest."""
        if not s:
            return None, None, []
        v1 = s.pop(self._choose(len(s)))
        for e in s:
            e.d1 = self.dist(e.obj, v1.obj)
        if not s:
            return v1, None, []
        j = max(range(len(s)), key=lambda i: s[i].d1)
        v2 = s.pop(j)
        for e in s:
            e.d2 = self.dist(e.obj, v2.obj)
        return v1, v2, s

    def _build(self, s: list[Entry[T]]):
        if len(s) <= self.k + 2:  # @line L1
            v1, v2, rest = self._vantage_points(s)  # @line L2
            return Leaf(v1.obj if v1 else None, v2.obj if v2 else None, rest)
        v1 = s.pop(self._choose(len(s)))  # @line L3
        for e in s:
            e.d1 = self.dist(e.obj, v1.obj)
            self._push(e, e.d1)
        groups = _split(s, lambda e: e.d1, self.m)  # @line L4
        ring1 = [_interval(g, lambda e: e.d1) for g in groups]
        gi = max(range(self.m), key=lambda i: len(groups[i]))
        j = max(range(len(groups[gi])), key=lambda i: groups[gi][i].d1)
        v2 = groups[gi].pop(j)  # @line L5
        ring2: list[list[tuple[float, float]]] = []
        children: list[list[object]] = []
        for g in groups:
            for e in g:
                e.d2 = self.dist(e.obj, v2.obj)
                self._push(e, e.d2)
            sub = _split(g, lambda e: e.d2, self.m)  # @line L6
            ring2.append([_interval(h, lambda e: e.d2) for h in sub])
            children.append([self._build(h) for h in sub])  # @line L7
        return Internal(v1.obj, v2.obj, ring1, ring2, children)

    def range(self, q: T, r: float) -> list[T]:
        """All stored objects x with d(q, x) <= r."""
        out: list[T] = []
        self._range(self.root, q, r, [], out)
        return out

    def _range(self, node, q: T, r: float, qpath: list[float], out: list[T]) -> None:
        if isinstance(node, Leaf):  # @line L8
            if node.v1 is None:
                return
            t1 = self.dist(q, node.v1)  # @line L9
            if t1 <= r:
                out.append(node.v1)
            if node.v2 is None:
                return
            t2 = self.dist(q, node.v2)
            if t2 <= r:
                out.append(node.v2)
            for e in node.entries:  # @line L10
                if abs(t1 - e.d1) > r or abs(t2 - e.d2) > r:  # @line L11
                    continue
                if any(abs(a - b) > r for a, b in zip(qpath, e.path)):  # @line L12
                    continue
                if self.dist(q, e.obj) <= r:  # @line L13
                    out.append(e.obj)
            return
        t1 = self.dist(q, node.v1)  # @line L14
        t2 = self.dist(q, node.v2)
        for t, v in ((t1, node.v1), (t2, node.v2)):
            if t <= r:
                out.append(v)
        path = (qpath + [t1, t2])[: self.p]  # @line L15
        for i in range(self.m):  # @line L16
            lo, hi = node.ring1[i]
            if lo > hi or t1 + r < lo or t1 - r > hi:
                continue
            for j in range(self.m):  # @line L17
                lo2, hi2 = node.ring2[i][j]
                if lo2 > hi2 or t2 + r < lo2 or t2 - r > hi2:
                    continue
                self._range(node.children[i][j], q, r, path, out)  # @line L18
