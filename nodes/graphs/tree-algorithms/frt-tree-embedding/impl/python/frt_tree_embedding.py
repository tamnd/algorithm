# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frt-tree-embedding/. The authors are listed in prov/CF4M1Y.jsonl.

import random


class FrtTree:
    """A random dominating tree metric for a finite metric, after Fakcharoenphol, Rao and Talwar.

    The input is an n x n distance matrix (n >= 1) of a metric on the points
    0 .. n-1: symmetric, zero exactly on the diagonal, and obeying the triangle
    inequality. The tree is rooted, its edges are weighted, and its leaves are
    the points: tree node leaf[x] holds point x. Nodes are numbered 0 .. N-1
    in order of creation, with the root as node 0. Tree distances are never
    smaller than the input distances, and their expectation over the random
    choices is at most 16 H_n times larger, where H_n is the n-th harmonic
    number. Building takes O(n^2 log(Delta / dmin)) time.
    """

    def __init__(
        self,
        dist: list[list[float]],
        seed: int | None = None,
        perm: list[int] | None = None,
        beta: float | None = None,
    ) -> None:
        n = len(dist)
        if n < 1 or any(len(row) != n for row in dist):
            raise ValueError("the distance matrix must be square and non-empty")
        for i in range(n):
            if dist[i][i] != 0:
                raise ValueError("the diagonal must be zero")
            for j in range(i + 1, n):
                if dist[i][j] != dist[j][i] or dist[i][j] <= 0:
                    raise ValueError("distances must be symmetric and positive off the diagonal")
        rng = random.Random(seed)
        # @line L1
        dmin = min((dist[i][j] for i in range(n) for j in range(i + 1, n)), default=1.0)
        dmax = max((dist[i][j] for i in range(n) for j in range(i + 1, n)), default=1.0)
        top = 0
        if n > 1:  # the smallest top >= 1 with 2^top * dmin >= dmax
            top = 1
            while 2.0**top * dmin < dmax:
                top += 1
        if perm is None:  # @line L2
            perm = list(range(n))
            rng.shuffle(perm)
        elif sorted(perm) != list(range(n)):
            raise ValueError("perm must be a permutation of 0 .. n-1")
        if beta is None:
            beta = rng.uniform(1.0, 2.0)
        elif not 1.0 <= beta < 2.0:
            raise ValueError("beta must lie in [1, 2)")
        self.n = n
        self.top = top
        self.perm = list(perm)
        self.beta = beta
        self.scale = dmin
        self.parent = [-1]  # @line L3
        self.weight = [0.0]  # weight of the edge to the parent, in input units
        self.level = [top]
        self.members: list[list[int]] = [list(range(n))]
        node = [0] * n
        for i in range(top - 1, -1, -1):  # @line L4
            radius = beta * 2.0 ** (i - 1) * dmin  # @line L5
            children: dict[tuple[int, int], int] = {}
            new_node = [0] * n
            for x in range(n):
                row = dist[x]
                c = next(w for w in perm if row[w] <= radius)  # @line L6
                key = (node[x], c)  # @line L7
                if key not in children:
                    children[key] = len(self.parent)
                    self.parent.append(node[x])
                    self.weight.append(2.0 ** (i + 1) * dmin)
                    self.level.append(i)
                    self.members.append([])
                new_node[x] = children[key]  # @line L8
                self.members[new_node[x]].append(x)
            node = new_node
        self.leaf = node  # @line L9

    def tree_distance(self, u: int, v: int) -> float:
        """Return the distance between the leaves of points u and v in the tree."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("point out of range")
        a, b = self.leaf[u], self.leaf[v]
        total = 0.0
        while a != b:  # all leaves are at level 0, so a and b stay level
            total += self.weight[a] + self.weight[b]
            a, b = self.parent[a], self.parent[b]
        return total
