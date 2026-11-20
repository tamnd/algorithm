# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kwiksort-rank-aggregation/. The authors are listed in prov/BHYQT7.jsonl.

import random
from typing import Optional, Sequence

Ranking = Sequence[int]


def pairwise_counts(profile: Sequence[Ranking], m: int) -> list[list[int]]:
    """Return N with N[a][b] the number of voters who rank a above b."""
    N = [[0] * m for _ in range(m)]
    for r in profile:
        for i, a in enumerate(r):
            for b in r[i + 1:]:
                N[a][b] += 1
    return N


def majority_tournament(profile: Sequence[Ranking], m: int) -> list[list[bool]]:
    """Return T with T[u][v] True when a majority ranks u above v; a tie goes to the smaller index."""
    N = pairwise_counts(profile, m)
    return [[u != v and (N[u][v] > N[v][u] or (N[u][v] == N[v][u] and u < v))
             for v in range(m)] for u in range(m)]


def partition(T: list[list[bool]], V: Sequence[int], p: int) -> tuple[list[int], list[int]]:
    """Split V without p into the candidates that beat p in T and those that p beats."""
    left = [u for u in V if u != p and T[u][p]]  # @line L3
    right = [u for u in V if u != p and T[p][u]]  # @line L4
    return left, right


def kwiksort(T: list[list[bool]], V: Sequence[int], rng: random.Random) -> tuple[int, ...]:
    """Order V by quicksort on the tournament T with uniformly random pivots."""
    out: list[int] = []
    stack = [list(V)]
    while stack:
        W = stack.pop()
        if len(W) <= 1:  # @line L1
            out.extend(W)
            continue
        p = W[rng.randrange(len(W))]  # @line L2
        left, right = partition(T, W, p)
        stack.append(right)  # @line L5
        stack.append([p])
        stack.append(left)
    return tuple(out)


def kemeny_cost(N: list[list[int]], r: Ranking) -> int:
    """Return the sum over voters of the Kendall tau distance to r, from the counts N."""
    return sum(N[r[j]][r[i]] for i in range(len(r)) for j in range(i + 1, len(r)))


def fas_cost(T: list[list[bool]], r: Ranking) -> int:
    """Return the number of arcs of T that point from a lower to a higher place of r."""
    return sum(1 for i in range(len(r)) for j in range(i + 1, len(r)) if T[r[j]][r[i]])


def best_input_ranking(profile: Sequence[Ranking], N: list[list[int]]) -> tuple[int, ...]:
    """Return the ballot with the least Kemeny cost (the first one on ties)."""
    return tuple(min(profile, key=lambda r: kemeny_cost(N, r)))


def kwiksort_aggregate(profile: Sequence[Ranking], m: int,
                       seed: Optional[int] = 0) -> tuple[int, ...]:
    """Return the better, in Kemeny cost, of KwikSort on the majority tournament and the best
    ballot. The ballot wins ties. With no voters, return KwikSort on the empty tournament."""
    rng = random.Random(seed)
    N = pairwise_counts(profile, m)
    T = majority_tournament(profile, m)  # @line L6
    r1 = kwiksort(T, range(m), rng)  # @line L7
    if not profile:
        return r1
    r2 = best_input_ranking(profile, N)  # @line L8
    return r2 if kemeny_cost(N, r2) <= kemeny_cost(N, r1) else r1  # @line L9
