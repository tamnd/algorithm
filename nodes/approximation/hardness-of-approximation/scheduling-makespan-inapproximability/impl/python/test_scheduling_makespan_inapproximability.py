# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-makespan-inapproximability/. The authors are listed in prov/KVD1F4.jsonl.

import random
from itertools import combinations

from scheduling_makespan_inapproximability import (
    clique_to_prec,
    decides,
    feasible,
    gap_threshold,
    has_clique,
)


def test_gap_thresholds() -> None:
    assert gap_threshold(2) == 1.5
    assert abs(gap_threshold(3) - 4 / 3) < 1e-12
    assert gap_threshold(4) == 1.25
    # An algorithm with ratio rho < (t + 1) / t returns at most floor(rho t) = t when OPT = t.
    for t in range(1, 30):
        rho = gap_threshold(t) - 1e-9
        assert int(rho * t) == t
        assert decides(t, rho, t) and not decides(t, rho, t + 1)


def test_triangle_example() -> None:
    tri = [(0, 1), (1, 2), (0, 2)]
    m, n, arcs = clique_to_prec(3, tri, 3)
    assert n == 3 * m
    assert feasible(3, m, n, arcs)
    path = [(0, 1), (1, 2)]
    m, n, arcs = clique_to_prec(3, path, 3)
    assert not feasible(3, m, n, arcs) and feasible(4, m, n, arcs)


def test_clique_iff_makespan_three() -> None:
    rng = random.Random(10)
    for _ in range(80):
        nv = rng.randint(3, 5)
        edges = [e for e in combinations(range(nv), 2) if rng.random() < 0.6]
        k = rng.randint(2, nv)
        m, n, arcs = clique_to_prec(nv, edges, k)
        assert n == 3 * m
        assert not feasible(2, m, n, arcs)
        assert feasible(3, m, n, arcs) == has_clique(nv, edges, k)
