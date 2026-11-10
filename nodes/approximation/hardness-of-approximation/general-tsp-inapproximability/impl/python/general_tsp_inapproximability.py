# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/general-tsp-inapproximability/. The authors are listed in prov/BA61NJ.jsonl.
"""The gap reduction from Hamiltonian cycle to general TSP (Sahni and Gonzalez 1976).

For small instances only: the exact solvers try every tour.
"""

from itertools import permutations


def hc_to_tsp(n: int, edges: list[tuple[int, int]], rho: int) -> list[list[int]]:
    """Return the cost matrix: 1 on the edges of the graph, rho*n + 1 on the other pairs."""
    big = rho * n + 1
    adj = {frozenset(e) for e in edges}
    return [[0 if u == v else (1 if frozenset((u, v)) in adj else big) for v in range(n)] for u in range(n)]


def tour_cost(cost: list[list[int]], tour: list[int]) -> int:
    """Return the cost of the closed tour that visits the vertices in the given order."""
    return sum(cost[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))


def optimal_tour_cost(cost: list[list[int]]) -> int:
    """Return OPT by trying each tour that starts at vertex 0."""
    n = len(cost)
    if n == 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in permutations(range(1, n)))


def is_hamiltonian(n: int, edges: list[tuple[int, int]]) -> bool:
    """Decide by brute force whether the graph has a Hamiltonian cycle (n >= 3)."""
    adj = {frozenset(e) for e in edges}
    for p in permutations(range(1, n)):
        cyc = [0, *p]
        if all(frozenset((cyc[i], cyc[(i + 1) % n])) in adj for i in range(n)):
            return True
    return False


def decide_with_approximation(n: int, edges: list[tuple[int, int]], rho: int, approx) -> bool:
    """Decide Hamiltonian cycle with a rho-approximation `approx` for TSP (a function on cost matrices)."""
    return approx(hc_to_tsp(n, edges, rho)) <= rho * n
