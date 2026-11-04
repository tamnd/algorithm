# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arpa-offline-rmq/. The authors are listed in prov/2G2RRV.jsonl.

from collections.abc import Sequence
from typing import Any


def arpa_offline_rmq(a: Sequence[Any], queries: Sequence[tuple[int, int]]) -> list[int]:
    """Return, for each query (L, R), the position of the leftmost minimum of a[L..R].

    The queries are answered offline in one sweep from left to right with a
    monotonic stack and a union-find forest with path compression.
    """
    n = len(a)
    p = list(range(n))  # @line L1
    by_right: list[list[int]] = [[] for _ in range(n)]  # @line L2
    for k, (lo, hi) in enumerate(queries):
        if not 0 <= lo <= hi < n:
            raise ValueError("query out of range")
        by_right[hi].append(k)
    ans = [0] * len(queries)
    stack: list[int] = []  # @line L3

    def find(x: int) -> int:
        r = x  # @line L11
        while p[r] != r:
            r = p[r]
        while p[x] != r:  # @line L12
            nx = p[x]
            p[x] = r
            x = nx
        return r  # @line L13

    for i in range(n):  # @line L4
        while stack and a[stack[-1]] > a[i]:  # @line L5
            p[stack.pop()] = i  # @line L6
        stack.append(i)  # @line L7
        for k in by_right[i]:  # @line L8
            ans[k] = find(queries[k][0])  # @line L9
    return ans  # @line L10
