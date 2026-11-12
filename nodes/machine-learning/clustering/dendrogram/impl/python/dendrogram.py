# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dendrogram/. The authors are listed in prov/2GBS7F.jsonl.

import math
from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]


class Dendrogram:
    """A binary merge tree over n leaves 0 .. n-1 with a height at each merge.

    Node n + t is the cluster made by merge t, from the nodes left[n + t] and
    right[n + t] at height[n + t]. Leaves have height 0. The merges are given in
    order; the tree is monotone when the heights do not decrease.
    """

    def __init__(self, n: int, merges: Sequence[tuple[int, int, Number]]) -> None:
        """Build from n - 1 merges (a, b, h); each a and b must be a current root.
        Cost: Theta(n)."""
        if n > 0 and len(merges) != n - 1:
            raise ValueError("a dendrogram on n leaves has n - 1 merges")
        self.n = n
        self.left = [-1] * max(2 * n - 1, 0)
        self.right = [-1] * max(2 * n - 1, 0)
        self.height: list[Number] = [0] * max(2 * n - 1, 0)
        self.size = [1] * n + [0] * max(n - 1, 0)
        self.parent = [-1] * max(2 * n - 1, 0)
        for t, (a, b, h) in enumerate(merges):
            v = n + t
            if not (0 <= a < v and 0 <= b < v) or a == b or self.parent[a] >= 0 or self.parent[b] >= 0:
                raise ValueError(f"merge {t} does not join two current clusters")
            self.left[v], self.right[v], self.height[v] = a, b, h
            self.size[v] = self.size[a] + self.size[b]
            self.parent[a] = self.parent[b] = v

    def is_monotone(self) -> bool:
        """True when no merge is lower than a merge below it."""
        return all(self.height[self.parent[v]] >= self.height[v] for v in range(self.n, 2 * self.n - 2))

    def leaves(self, v: int) -> list[int]:
        """The leaves below node v, left to right. Cost: O(size of v)."""
        out, stack = [], [v]
        while stack:
            u = stack.pop()
            if u < self.n:
                out.append(u)
            else:
                stack += [self.right[u], self.left[u]]
        return out

    def cophenetic(self) -> list[list[Number]]:
        """The n x n matrix of cophenetic distances: the height of the lowest
        common ancestor of each pair. Cost: Theta(n^2)."""
        n = self.n
        c: list[list[Number]] = [[0] * n for _ in range(n)]
        below = [[i] for i in range(n)]  # @line L1
        for t in range(n - 1):  # @line L2
            v = n + t
            a, b = self.left[v], self.right[v]  # @line L3
            for i in below[a]:  # @line L4
                for j in below[b]:
                    c[i][j] = c[j][i] = self.height[v]  # @line L5
            below.append(below[a] + below[b])  # @line L6
        return c  # @line L7

    def cut_k(self, k: int) -> list[int]:
        """Labels of the k clusters left when the last k - 1 merges are undone.
        Clusters are numbered in the order of their smallest leaf. Cost: O(n + k^2)."""
        n = self.n
        if not 1 <= k <= n:
            raise ValueError("k must be between 1 and n")
        roots = [2 * n - 2]  # @line L8
        while len(roots) < k:  # @line L9
            v = max(roots)  # @line L10
            roots.remove(v)  # @line L11
            roots += [self.left[v], self.right[v]]
        return self._labels(roots)  # @line L12

    def cut_height(self, t: Number) -> list[int]:
        """Labels of the clusters of the merges with height at most t, for a
        monotone tree: the maximal nodes of height at most t. Cost: O(n)."""
        n = self.n
        roots, stack = [], [2 * n - 2] if n else []
        while stack:
            v = stack.pop()
            if v < n or self.height[v] <= t:
                roots.append(v)
            else:
                stack += [self.left[v], self.right[v]]
        return self._labels(roots)

    def _labels(self, roots: list[int]) -> list[int]:
        groups = sorted((self.leaves(r) for r in roots), key=min)
        labels = [0] * self.n
        for c, g in enumerate(groups):
            for i in g:
                labels[i] = c
        return labels

    def cophenetic_correlation(self, dist: Sequence[Sequence[Number]]) -> float:
        """Pearson correlation of the input dissimilarities with the cophenetic
        distances over the n(n-1)/2 pairs (Sokal and Rohlf). Cost: Theta(n^2)."""
        c = self.cophenetic()
        xs = [float(dist[i][j]) for i in range(self.n) for j in range(i + 1, self.n)]
        ys = [float(c[i][j]) for i in range(self.n) for j in range(i + 1, self.n)]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs)
        syy = sum((y - my) ** 2 for y in ys)
        return sxy / math.sqrt(sxx * syy)

    def dasgupta_cost(self, w: Sequence[Sequence[Number]]) -> Number:
        """Dasgupta's cost: the sum over internal nodes v of |leaves(v)| times the
        total weight between the leaves of its two children. Cost: Theta(n^2)."""
        total: Number = 0
        for v in range(self.n, 2 * self.n - 1):
            cross = sum(w[i][j] for i in self.leaves(self.left[v]) for j in self.leaves(self.right[v]))
            total += self.size[v] * cross
        return total
