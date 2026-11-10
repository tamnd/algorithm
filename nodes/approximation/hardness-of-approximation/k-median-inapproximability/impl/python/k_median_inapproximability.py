# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-median-inapproximability/. The authors are listed in prov/C8XWBD.jsonl.
"""The reduction from maximum coverage to k-median with facilities and clients.

Facility j is the set S_j and client e is the element e. The distance is 1 when e is in S_j, 3 when it
is not, and 2 between two facilities or two clients. For small instances only: the solvers try all choices.
"""

from itertools import combinations


def coverage_to_k_median(n: int, sets: list[frozenset[int]]) -> list[list[int]]:
    """The distance matrix on the points 0 .. m-1 (facilities) and m .. m+n-1 (clients)."""
    m = len(sets)
    size = m + n
    d = [[0] * size for _ in range(size)]
    for p in range(size):
        for q in range(size):
            if p == q:
                continue
            if (p < m) == (q < m):
                d[p][q] = 2
            else:
                j, e = (p, q - m) if p < m else (q, p - m)
                d[p][q] = 1 if e in sets[j] else 3
    return d


def is_metric(d: list[list[int]]) -> bool:
    r = range(len(d))
    return all(d[p][q] == d[q][p] for p in r for q in r) and all(
        d[p][q] <= d[p][x] + d[x][q] for p in r for q in r for x in r
    )


def k_median_cost(d: list[list[int]], facilities: list[int], clients: list[int], open_: tuple[int, ...]) -> int:
    return sum(min(d[c][f] for f in open_) for c in clients)


def k_median_opt(d: list[list[int]], facilities: list[int], clients: list[int], k: int) -> int:
    return min(k_median_cost(d, facilities, clients, c) for c in combinations(facilities, k))


def max_coverage_opt(n: int, sets: list[frozenset[int]], k: int) -> int:
    return max(len(frozenset().union(*(sets[j] for j in c))) for c in combinations(range(len(sets)), k))
