# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-star/. The authors are listed in prov/83VY7T.jsonl.

from collections.abc import Iterable


def _prefix_counts(n: int, keys: Iterable[int]) -> list[int]:
    """p[i] = the number of keys less than i, for i in 0 .. n."""
    p = [0] * (n + 1)
    for k in keys:
        p[k + 1] += 1
    for i in range(1, n + 1):
        p[i] += p[i - 1]
    return p


class ForwardStar:
    """A static directed network: arcs sorted by tail, named 0 .. m - 1.

    point[i] is the name of the first arc out of i; trace[rpoint[j]:rpoint[j + 1]]
    lists the names of the arcs into j. Building takes Theta(n + m) time,
    out_arcs and in_arcs take time linear in their output, degrees O(1).
    Parallel arcs and self-loops are allowed.
    """

    def __init__(self, n: int, arcs: Iterable[tuple[int, int, float]]) -> None:
        if n < 0:
            raise ValueError("n must be at least 0")
        given = list(arcs)
        for t, h, _ in given:
            if not (0 <= t < n and 0 <= h < n):
                raise IndexError("vertex out of range")
        self.n, self.m = n, len(given)
        start = _prefix_counts(n, (t for t, _, _ in given))
        pos = start[:n]
        order: list[tuple[int, int, float]] = [(0, 0, 0)] * self.m
        for a in given:  # stable counting sort by tail
            order[pos[a[0]]] = a  # @line L1
            pos[a[0]] += 1
        self.tail = [t for t, _, _ in order]
        self.head = [h for _, h, _ in order]
        self.cost = [c for _, _, c in order]
        self.flow: list[float] = [0] * self.m
        self.point = start  # @line L2
        self.rpoint = _prefix_counts(n, self.head)  # @line L3
        rpos = self.rpoint[:n]  # @line L4
        self.trace = [0] * self.m
        for e in range(self.m):  # @line L5
            j = self.head[e]  # @line L6
            self.trace[rpos[j]] = e
            rpos[j] += 1

    def _check(self, i: int) -> None:
        if not 0 <= i < self.n:
            raise IndexError("vertex out of range")

    def out_arcs(self, i: int) -> list[int]:
        self._check(i)
        return list(range(self.point[i], self.point[i + 1]))  # @line L7

    def in_arcs(self, j: int) -> list[int]:
        self._check(j)
        return [self.trace[k] for k in range(self.rpoint[j], self.rpoint[j + 1])]  # @line L8

    def out_degree(self, i: int) -> int:
        self._check(i)
        return self.point[i + 1] - self.point[i]  # @line L9

    def in_degree(self, j: int) -> int:
        self._check(j)
        return self.rpoint[j + 1] - self.rpoint[j]  # @line L10

    def arcs(self) -> list[tuple[int, int, float]]:
        return list(zip(self.tail, self.head, self.cost))

    def check_invariant(self) -> None:
        n, m = self.n, self.m
        assert self.point[0] == 0 and self.point[n] == m
        assert self.rpoint[0] == 0 and self.rpoint[n] == m
        for i in range(n):
            assert self.point[i] <= self.point[i + 1]
            assert self.rpoint[i] <= self.rpoint[i + 1]
            for e in range(self.point[i], self.point[i + 1]):
                assert self.tail[e] == i
            seg = self.trace[self.rpoint[i] : self.rpoint[i + 1]]
            assert all(seg[k] < seg[k + 1] for k in range(len(seg) - 1))
            assert all(self.head[e] == i for e in seg)
        assert sorted(self.trace) == list(range(m))
