# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slink/. The authors are listed in prov/5KYFGE.jsonl.

import math
from fractions import Fraction
from typing import Callable, Union

Number = Union[int, float, Fraction]
Merge = tuple[int, int, Number, int]


def slink(n: int, dist: Callable[[int, int], Number]) -> tuple[list[int], list[Number]]:
    """Sibson's SLINK: the pointer representation of the single-linkage hierarchy.

    dist(i, j) gives the dissimilarity of points i and j; it is called once for
    each pair i < j. Returns (pi, lam): lam[i] is the height at which point i
    first joins a point with a larger index, and pi[i] is the largest index in
    the cluster that it then joins. For the last point pi = n - 1 and lam = inf.
    Cost: Theta(n^2) time and Theta(n) memory.
    """
    pi = [0] * n
    lam: list[Number] = [math.inf] * n
    m: list[Number] = [math.inf] * n
    for i in range(n):  # @line L1
        pi[i] = i  # @line L2
        lam[i] = math.inf
        for j in range(i):  # @line L3
            m[j] = dist(j, i)
        for j in range(i):  # @line L4
            if lam[j] >= m[j]:  # @line L5
                m[pi[j]] = min(m[pi[j]], lam[j])  # @line L6
                lam[j] = m[j]  # @line L7
                pi[j] = i
            else:
                m[pi[j]] = min(m[pi[j]], m[j])  # @line L8
        for j in range(i):  # @line L9
            if lam[j] >= lam[pi[j]]:
                pi[j] = i  # @line L10
    return pi, lam


def pointer_to_merges(pi: list[int], lam: list[Number]) -> list[Merge]:
    """Turn a pointer representation into merges (a, b, h, size) sorted by height.

    Point j is joined to the cluster of pi[j] at height lam[j], in the order of
    increasing lam[j]. Leaves are 0 .. n-1 and merge t makes cluster n + t.
    Cost: O(n log n) time.
    """
    n = len(pi)
    parent = list(range(n))
    cluster = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    merges: list[Merge] = []
    for j in sorted(range(n - 1), key=lambda t: (lam[t], t)):
        ru, rv = find(j), find(pi[j])
        a, b = sorted((cluster[ru], cluster[rv]))
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        merges.append((a, b, lam[j], size[ru]))
        cluster[ru] = n + len(merges) - 1
    return merges
