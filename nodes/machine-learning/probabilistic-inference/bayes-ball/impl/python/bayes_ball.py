# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-ball/. The authors are listed in prov/FBZXXF.jsonl.

"""Bayes-Ball (Shachter 1998) on a DAG with the nodes 0 .. n - 1.

The edges (u, v) mean u -> v. J is the set of query nodes and K the set of
observed (evidence) nodes. The ball starts at each node of J as if it came
from a child. Each node has a visited flag and two marks, top and bottom.
"""

from collections import deque
from dataclasses import dataclass

FROM_CHILD = 0
FROM_PARENT = 1


@dataclass
class BallResult:
    visited: set[int]
    top: set[int]
    bottom: set[int]
    observed: set[int]

    def irrelevant(self, n: int) -> set[int]:
        """The nodes not marked on the bottom: d-separated from J given K, or in K."""
        return set(range(n)) - self.bottom

    def requisite_probability(self) -> set[int]:
        """The nodes marked on top: their conditional tables may be needed for P(J | K)."""
        return set(self.top)

    def requisite_observation(self) -> set[int]:
        """The observed nodes that the ball visits."""
        return self.visited & self.observed


def bayes_ball(n: int, edges: list[tuple[int, int]], J: set[int], K: set[int],
               functional: frozenset[int] = frozenset()) -> BallResult:
    parents: list[list[int]] = [[] for _ in range(n)]
    children: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        parents[v].append(u)
        children[u].append(v)
    visited: set[int] = set()  # @line L1
    top: set[int] = set()
    bottom: set[int] = set()
    schedule = deque((j, FROM_CHILD) for j in sorted(J))
    while schedule:  # @line L2
        j, came = schedule.popleft()  # @line L3
        visited.add(j)
        if came == FROM_CHILD and j not in K:  # @line L4
            if j not in top:  # @line L5
                top.add(j)
                schedule.extend((p, FROM_CHILD) for p in parents[j])
            if j not in functional and j not in bottom:  # @line L6
                bottom.add(j)
                schedule.extend((c, FROM_PARENT) for c in children[j])
        elif came == FROM_PARENT:  # @line L7
            if j in K and j not in top:  # @line L8
                top.add(j)
                schedule.extend((p, FROM_CHILD) for p in parents[j])
            if j not in K and j not in bottom:  # @line L9
                bottom.add(j)
                schedule.extend((c, FROM_PARENT) for c in children[j])
    return BallResult(visited, top, bottom, set(K))  # @line L10


def d_separated(n: int, edges: list[tuple[int, int]], xs: set[int], ys: set[int], zs: set[int]) -> bool:
    """Decide whether xs and ys are d-separated given zs (disjoint sets)."""
    if xs & ys or xs & zs or ys & zs:
        raise ValueError("the sets X, Y and Z must be disjoint")
    return not (bayes_ball(n, edges, xs, zs).bottom & ys)
