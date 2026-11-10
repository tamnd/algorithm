# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-center-inapproximability/. The authors are listed in prov/5WNEVK.jsonl.

import random
from itertools import combinations

from k_center_inapproximability import (
    domination_number,
    ds_to_k_center,
    farthest_first,
    is_metric,
    k_center_opt,
    radius,
)

PETERSEN = [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]


def random_graph(rng: random.Random, n: int, p: float) -> list[tuple[int, int]]:
    return [e for e in combinations(range(n), 2) if rng.random() < p]


def test_examples() -> None:
    path = [(0, 1), (1, 2), (2, 3), (3, 4)]
    assert domination_number(5, path) == 2
    d = ds_to_k_center(5, path)
    assert k_center_opt(d, 2) == 1 and k_center_opt(d, 1) == 2
    assert domination_number(10, PETERSEN) == 3
    d = ds_to_k_center(10, PETERSEN)
    assert k_center_opt(d, 2) == 2 and k_center_opt(d, 3) == 1


def test_gap_completeness_and_soundness() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = random_graph(rng, n, rng.choice([0.2, 0.4, 0.6]))
        d = ds_to_k_center(n, edges)
        assert is_metric(d)
        gamma = domination_number(n, edges)
        assert k_center_opt(d, n) == 0
        for k in range(1, n):
            opt = k_center_opt(d, k)
            assert opt == (1 if gamma <= k else 2)
            # Every set of k centers has radius at most 2, so a ratio below 2 must find radius 1.
            assert radius(d, farthest_first(d, k)) <= 2


def test_without_triangle_inequality() -> None:
    rng = random.Random(5)
    for _ in range(100):
        n = rng.randint(2, 7)
        edges = random_graph(rng, n, 0.4)
        far = rng.randint(3, 50)
        d = ds_to_k_center(n, edges, far)
        gamma = domination_number(n, edges)
        for k in range(1, n):
            assert k_center_opt(d, k) == (1 if gamma <= k else far)


def test_instance_size() -> None:
    for n in range(1, 9):
        d = ds_to_k_center(n, [(0, n - 1)] if n > 1 else [])
        assert len(d) == n and all(len(row) == n for row in d)
        assert {d[u][v] for u in range(n) for v in range(n) if u != v} <= {1, 2}
