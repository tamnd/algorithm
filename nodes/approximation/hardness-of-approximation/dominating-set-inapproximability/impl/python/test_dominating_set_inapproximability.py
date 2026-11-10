# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominating-set-inapproximability/. The authors are listed in prov/W53DKC.jsonl.

import random
from itertools import combinations

from dominating_set_inapproximability import (
    cover_to_ds,
    domination_number,
    ds_to_cover,
    ds_to_sc,
    is_cover,
    is_dominating,
    min_cover,
    sc_to_ds,
)


def random_system(rng: random.Random, n: int, m: int) -> list[frozenset[int]]:
    sets = [frozenset(e for e in range(n) if rng.random() < 0.35) for _ in range(m)]
    # Make the system coverable: put each element into some set.
    sets = [set(s) for s in sets]
    for e in range(n):
        if not any(e in s for s in sets):
            sets[rng.randrange(m)].add(e)
    return [frozenset(s) for s in sets]


def test_example() -> None:
    sets = [frozenset(s) for s in ([0, 1, 2], [2, 3], [3, 4, 5], [0, 3], [1, 4], [5])]
    assert min_cover(6, sets) == 2
    g = sc_to_ds(6, sets)
    assert g[0] == 12 and len(g[1]) == 15 + 13
    assert domination_number(*g) == 2


def test_sc_to_ds_keeps_opt_and_maps_back() -> None:
    rng = random.Random(8)
    for _ in range(120):
        n, m = rng.randint(1, 6), rng.randint(1, 5)
        sets = random_system(rng, n, m)
        nv, edges = sc_to_ds(n, sets)
        assert nv == n + m
        assert len(edges) == m * (m - 1) // 2 + sum(len(s) for s in sets)
        opt = min_cover(n, sets)
        assert domination_number(nv, edges) == opt
        # Every dominating set maps back to a cover that is no larger (beta = 1).
        for size in range(1, nv + 1):
            for dom in combinations(range(nv), size):
                if is_dominating(nv, edges, list(dom)):
                    cov = ds_to_cover(n, sets, list(dom))
                    assert is_cover(n, sets, cov) and len(cov) <= len(dom)


def test_ds_to_sc_keeps_opt_and_maps_back() -> None:
    rng = random.Random(9)
    for _ in range(150):
        n = rng.randint(1, 8)
        edges = [e for e in combinations(range(n), 2) if rng.random() < 0.3]
        u, sets = ds_to_sc(n, edges)
        assert u == n and len(sets) == n
        assert max(len(s) for s in sets) == 1 + max(sum(v in e for e in edges) for v in range(n))
        gamma = domination_number(n, edges)
        assert min_cover(u, sets) == gamma
        for size in range(gamma, min(n, gamma + 1) + 1):
            for c in combinations(range(n), size):
                if is_cover(u, sets, list(c)):
                    assert is_dominating(n, edges, cover_to_ds(list(c)))
