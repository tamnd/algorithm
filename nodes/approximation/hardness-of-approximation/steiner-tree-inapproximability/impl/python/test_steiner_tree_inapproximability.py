# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steiner-tree-inapproximability/. The authors are listed in prov/46CJ97.jsonl.

import random
from itertools import combinations

from steiner_tree_inapproximability import (
    is_connected,
    mst_weight,
    steiner_opt,
    tree_to_cover,
    vc_to_steiner,
    vertex_cover_number,
)


def random_connected(rng, n, p):
    while True:
        edges = [e for e in combinations(range(n), 2) if rng.random() < p]
        if len(edges) >= 2 and is_connected(n, edges):
            return edges


def test_examples() -> None:
    # The path 0-1-2-3 has tau = 2, so OPT = 3 + 2 - 1 = 4.
    path = [(0, 1), (1, 2), (2, 3)]
    d, s, t = vc_to_steiner(4, path)
    assert steiner_opt(d, s, t)[0] == 4
    # The triangle has tau = 2, so OPT = 3 + 2 - 1 = 4; terminals alone cost 2 (3 - 1) = 4 as well.
    tri = [(0, 1), (1, 2), (0, 2)]
    d, s, t = vc_to_steiner(3, tri)
    assert steiner_opt(d, s, t)[0] == 4 and mst_weight(d, t) == 4


def test_optimum_formula_and_metric() -> None:
    rng = random.Random(6)
    for _ in range(80):
        n = rng.randint(3, 6)
        edges = random_connected(rng, n, 0.5)
        d, s, t = vc_to_steiner(n, edges)
        r = range(len(d))
        assert all(d[a][b] <= d[a][x] + d[x][b] for a in r for b in r for x in r)
        opt, _ = steiner_opt(d, s, t)
        assert opt == len(edges) + vertex_cover_number(n, edges) - 1


def test_solution_map_has_beta_one() -> None:
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(3, 6)
        edges = random_connected(rng, n, 0.5)
        d, s, t = vc_to_steiner(n, edges)
        m = len(edges)
        for size in range(n + 1):
            for chosen in combinations(s, size):
                cost = mst_weight(d, t + list(chosen))
                cover = tree_to_cover(edges, chosen)
                assert all(u in cover or v in cover for u, v in edges)
                assert len(cover) <= cost - m + 1


def test_alpha_bound_for_bounded_degree() -> None:
    rng = random.Random(8)
    for _ in range(60):
        n = rng.randint(3, 6)
        edges = random_connected(rng, n, 0.6)
        deg = max(sum(v in e for e in edges) for v in range(n))
        tau = vertex_cover_number(n, edges)
        assert len(edges) + tau - 1 <= (deg + 1) * tau
