# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-karp-equivalence/. The authors are listed in prov/R0H62M.jsonl.

from collections.abc import Sequence


class DisjointSet:
    """Union by size and path halving; m operations on n elements take O(m alpha(n)) time."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        x, y = self.find(x), self.find(y)
        if x == y:
            return
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.parent[y] = x
        self.size[x] += self.size[y]


def hopcroft_karp_equivalent(
    delta1: Sequence[Sequence[int]],
    start1: int,
    finals1: set[int] | frozenset[int],
    delta2: Sequence[Sequence[int]],
    start2: int,
    finals2: set[int] | frozenset[int],
) -> tuple[bool, tuple[int, ...] | None]:
    """Decide whether two complete DFAs over symbols 0..sigma-1 accept the same language.

    Returns (True, None) if they do, and (False, w) with w a string accepted by exactly
    one of them otherwise. With n = n1 + n2 states the time is O(sigma n alpha(n)), and
    |w| <= n - 2.
    """
    n1 = len(delta1)
    sigma = len(delta1[0]) if delta1 else 0
    ds = DisjointSet(n1 + len(delta2))  # @line L1
    # each pushed pair stores (state of M1, state of M2, index of its parent pair, symbol)
    pairs: list[tuple[int, int, int, int]] = [(start1, start2, -1, -1)]
    ds.union(start1, n1 + start2)  # @line L2
    stack = [0]
    while stack:  # @line L3
        i = stack.pop()  # @line L4
        p, r, _, _ = pairs[i]
        if (p in finals1) != (r in finals2):  # @line L5
            word = []
            while pairs[i][2] >= 0:
                word.append(pairs[i][3])
                i = pairs[i][2]
            return False, tuple(reversed(word))
        for a in range(sigma):  # @line L6
            p2, r2 = delta1[p][a], delta2[r][a]  # @line L7
            if ds.find(p2) != ds.find(n1 + r2):  # @line L8
                ds.union(p2, n1 + r2)  # @line L9
                pairs.append((p2, r2, i, a))
                stack.append(len(pairs) - 1)
    return True, None  # @line L10
