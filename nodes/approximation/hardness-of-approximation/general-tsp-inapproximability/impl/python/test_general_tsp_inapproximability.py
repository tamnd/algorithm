# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/general-tsp-inapproximability/. The authors are listed in prov/BA61NJ.jsonl.

import random
from itertools import combinations, permutations

from general_tsp_inapproximability import (
    decide_with_approximation,
    hc_to_tsp,
    is_hamiltonian,
    optimal_tour_cost,
    tour_cost,
)


def random_graph(rng: random.Random, n: int, p: float) -> list[tuple[int, int]]:
    return [e for e in combinations(range(n), 2) if rng.random() < p]


def test_cycle_and_star() -> None:
    cyc = [(i, (i + 1) % 5) for i in range(5)]
    assert is_hamiltonian(5, cyc)
    assert optimal_tour_cost(hc_to_tsp(5, cyc, 3)) == 5
    star = [(0, i) for i in range(1, 5)]
    assert not is_hamiltonian(5, star)
    # A tour of the star uses at least 3 non-edges: the tour passes the center only once.
    assert optimal_tour_cost(hc_to_tsp(5, star, 3)) == 2 + 3 * 16


def test_gap_on_random_graphs() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(3, 7)
        edges = random_graph(rng, n, rng.choice([0.3, 0.5, 0.7]))
        rho = rng.randint(1, 5)
        cost = hc_to_tsp(n, edges, rho)
        opt = optimal_tour_cost(cost)
        if is_hamiltonian(n, edges):
            assert opt == n
        else:
            assert opt >= (n - 1) + rho * n + 1
            assert opt > rho * n


def test_any_rho_approximation_decides() -> None:
    rng = random.Random(11)
    for _ in range(80):
        n = rng.randint(3, 6)
        edges = random_graph(rng, n, 0.5)
        rho = rng.randint(1, 4)

        def worst_allowed(cost: list[list[int]]) -> int:
            # The worst tour that a rho-approximation may return: the costliest tour of cost <= rho*OPT.
            opt = optimal_tour_cost(cost)
            costs = [tour_cost(cost, [0, *p]) for p in permutations(range(1, n))]
            return max(c for c in costs if c <= rho * opt)

        assert decide_with_approximation(n, edges, rho, worst_allowed) == is_hamiltonian(n, edges)


def test_instance_size() -> None:
    # n vertices give n*(n-1)/2 pairs, and the largest cost rho*n + 1 has O(log(rho*n)) digits.
    for n in range(3, 9):
        for rho in (1, 2, 10, 2**n):
            cost = hc_to_tsp(n, [(0, 1)], rho)
            values = {cost[u][v] for u in range(n) for v in range(n) if u != v}
            assert values <= {1, rho * n + 1}
        # Even rho = 2^n keeps each cost below 2^(n + log n + 1), so the matrix has polynomial size.
        big = hc_to_tsp(n, [(0, 1)], 2**n)[0][2]
        assert big.bit_length() <= n + n.bit_length() + 1
