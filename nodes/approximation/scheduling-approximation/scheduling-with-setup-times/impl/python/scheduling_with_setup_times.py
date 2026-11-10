# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-with-setup-times/. The authors are listed in prov/KEC6PH.jsonl.

"""One machine with sequence-dependent setup times, 1|s_ij|C_max.

The machine starts in state 0. Running job j first costs the setup s0[j];
running job j right after job i costs s[i][j]. The makespan is the sum of all
processing times plus the setups along the order, so the problem is a shortest
Hamiltonian path from state 0 in a directed graph.
"""

from typing import Sequence


def makespan(p: Sequence[int], s0: Sequence[int], s: Sequence[Sequence[int]], order: Sequence[int]) -> int:
    if not order:
        return 0
    total = s0[order[0]] + sum(p[j] for j in order)
    return total + sum(s[a][b] for a, b in zip(order, order[1:]))


def held_karp_setup(p: Sequence[int], s0: Sequence[int], s: Sequence[Sequence[int]]) -> tuple[list[int], int]:
    """Exact dynamic program over subsets, O(2^n n^2) time and O(2^n n) space."""
    n = len(p)
    if len(s0) != n or len(s) != n or any(len(row) != n for row in s):
        raise ValueError("s0 must have n entries and s must be n by n")
    if n == 0:
        return [], 0
    INF = float("inf")
    full = (1 << n) - 1
    # D[S][j]: least total setup to run exactly the jobs of S, ending with job j
    D = [[INF] * n for _ in range(1 << n)]  # @line L1
    parent = [[-1] * n for _ in range(1 << n)]
    for j in range(n):
        D[1 << j][j] = s0[j]  # @line L2
    for S in range(1, 1 << n):  # @line L3
        for j in range(n):
            if not (S >> j) & 1 or D[S][j] == INF:
                continue
            for k in range(n):  # @line L4
                if (S >> k) & 1:
                    continue
                v = D[S][j] + s[j][k]
                T = S | (1 << k)
                if v < D[T][k]:
                    D[T][k] = v
                    parent[T][k] = j
    last = min(range(n), key=lambda j: D[full][j])  # @line L5
    order, S, j = [], full, last
    while j != -1:
        order.append(j)
        S, j = S & ~(1 << j), parent[S][j]
    order.reverse()
    return order, int(D[full][last]) + sum(p)  # @line L6


def nearest_neighbor(p: Sequence[int], s0: Sequence[int], s: Sequence[Sequence[int]]) -> tuple[list[int], int]:
    """Greedy heuristic: always run next the job with the smallest setup. No ratio in general."""
    n = len(p)
    left = set(range(n))
    order: list[int] = []
    cur = None
    while left:
        j = min(left, key=lambda k: (s0[k] if cur is None else s[cur][k], k))
        order.append(j)
        left.remove(j)
        cur = j
    return order, makespan(p, s0, s, order)
