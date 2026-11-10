# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-center-inapproximability/. The authors are listed in prov/5WNEVK.jsonl.
"""The gap reduction from dominating set to k-center (Hsu and Nemhauser 1979).

For small instances only: the exact solvers try every set of k centers.
"""

from itertools import combinations


def ds_to_k_center(n: int, edges: list[tuple[int, int]], far: int = 2) -> list[list[int]]:
    """Distance 0 on the diagonal, 1 on the edges, `far` on the other pairs."""
    adj = {frozenset(e) for e in edges}
    return [[0 if u == v else (1 if frozenset((u, v)) in adj else far) for v in range(n)] for u in range(n)]


def is_metric(d: list[list[int]]) -> bool:
    n = len(d)
    return all(d[u][w] <= d[u][v] + d[v][w] for u in range(n) for v in range(n) for w in range(n))


def radius(d: list[list[int]], centers) -> int:
    """The largest distance from a point to its nearest center."""
    return max(min(d[v][c] for c in centers) for v in range(len(d)))


def k_center_opt(d: list[list[int]], k: int) -> int:
    """OPT of k-center by trying every set of min(k, n) centers."""
    n = len(d)
    return min(radius(d, c) for c in combinations(range(n), min(k, n)))


def domination_number(n: int, edges: list[tuple[int, int]]) -> int:
    """The least size of a dominating set, by brute force."""
    nbr = [{v} for v in range(n)]
    for u, v in edges:
        nbr[u].add(v)
        nbr[v].add(u)
    for size in range(1, n + 1):
        for s in combinations(range(n), size):
            if set().union(*(nbr[v] for v in s)) == set(range(n)):
                return size
    return n


def farthest_first(d: list[list[int]], k: int) -> list[int]:
    """Gonzalez's farthest-first traversal, started at point 0."""
    centers = [0]
    while len(centers) < min(k, len(d)):
        far = max(range(len(d)), key=lambda v: min(d[v][c] for c in centers))
        centers.append(far)
    return centers
