# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simrank/. The authors are listed in prov/G0C81F.jsonl.

import math


def simrank(
    n: int, arcs: list[tuple[int, int]], c: float = 0.8, rounds: int = 10
) -> list[list[float]]:
    """Return the SimRank matrix after the given number of rounds.

    The vertices are 0 .. n-1 and arcs is a list of pairs (u, v) of a directed
    graph; a repeated arc counts as many times as it appears. The similarity of
    two vertices is built from their in-neighbours. The decay factor c is in
    (0, 1). After k rounds every entry is at most the exact SimRank score and
    at least that score minus c ** (k + 1). Each round costs O(n^2 + m^2) time;
    the space is O(n^2).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if not 0.0 < c < 1.0:
        raise ValueError("c must be in (0, 1)")
    if rounds < 0:
        raise ValueError("rounds must be non-negative")
    into: list[list[int]] = [[] for _ in range(n)]
    for u, v in arcs:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("arc endpoint out of range")
        into[v].append(u)
    r = [[1.0 if a == b else 0.0 for b in range(n)] for a in range(n)]  # @line L1
    for _ in range(rounds):  # @line L2
        nxt = [[0.0] * n for _ in range(n)]
        for a in range(n):  # @line L3
            for b in range(n):
                if a == b:  # @line L4
                    nxt[a][b] = 1.0
                elif not into[a] or not into[b]:  # @line L5
                    nxt[a][b] = 0.0
                else:  # @line L6
                    total = 0.0
                    for i in into[a]:
                        row = r[i]
                        for j in into[b]:
                            total += row[j]
                    nxt[a][b] = c * total / (len(into[a]) * len(into[b]))
        r = nxt  # @line L7
    return r  # @line L8


def rounds_for(eps: float, c: float = 0.8) -> int:
    """Return the least k >= 0 with c ** (k + 1) <= eps, for 0 < eps < 1."""
    if not 0.0 < eps < 1.0 or not 0.0 < c < 1.0:
        raise ValueError("eps and c must be in (0, 1)")
    k = max(0, math.ceil(math.log(eps) / math.log(c)) - 1)
    while c ** (k + 1) > eps:
        k += 1
    while k > 0 and c**k <= eps:
        k -= 1
    return k
