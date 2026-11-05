# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-matrix/. The authors are listed in prov/QTKKXV.jsonl.

import itertools
import random

import pytest

from laplacian_matrix import Laplacian, components, spanning_tree_count


def example() -> Laplacian:
    lap = Laplacian(4)
    for u, v in [(0, 1), (0, 2), (1, 2), (2, 3)]:
        lap.add_edge(u, v)
    return lap


def test_example() -> None:
    lap = example()
    assert lap.dense() == [[2, -1, -1, 0], [-1, 2, -1, 0],
                           [-1, -1, 3, -1], [0, 0, -1, 1]]
    assert lap.multiply([1, 1, 1, 1]) == [0, 0, 0, 0]
    assert lap.multiply([1, 0, 0, 0]) == [2, -1, -1, 0]
    assert lap.quadratic_form([1, 1, 0, 0]) == 2
    assert lap.quadratic_form([0, 0, 0, 1]) == 1
    assert components(lap) == 1
    assert spanning_tree_count(lap) == 3


def test_matrix_tree() -> None:
    for n in range(1, 7):
        k = Laplacian(n)
        for u, v in itertools.combinations(range(n), 2):
            k.add_edge(u, v)
        assert spanning_tree_count(k) == n ** (n - 2) if n >= 2 else 1
    for n in range(3, 9):
        c = Laplacian(n)
        for i in range(n):
            c.add_edge(i, (i + 1) % n)
        assert spanning_tree_count(c) == n


def test_components_and_rejects() -> None:
    lap = Laplacian(5)
    lap.add_edge(0, 1)
    lap.add_edge(2, 3)
    assert components(lap) == 3
    assert spanning_tree_count(lap) == 0
    with pytest.raises(ValueError):
        lap.add_edge(4, 4)
    with pytest.raises(ValueError):
        lap.add_edge(0, 4, 0)


def test_parallel_edges_add() -> None:
    lap = Laplacian(2)
    lap.add_edge(0, 1, 2)
    lap.add_edge(0, 1, 3)
    assert lap.entry(0, 1) == -5 and lap.entry(0, 0) == 5
    assert spanning_tree_count(lap) == 5


def test_random_against_dense() -> None:
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(1, 8)
        lap = Laplacian(n)
        for _ in range(rng.randint(0, 12)):
            u, v = rng.sample(range(n), 2) if n >= 2 else (0, 0)
            if u != v:
                lap.add_edge(u, v, rng.randint(1, 4))
        a = lap.dense()
        x = [rng.randint(-5, 5) for _ in range(n)]
        y = [sum(a[i][j] * x[j] for j in range(n)) for i in range(n)]
        assert lap.multiply(x) == y
        assert lap.quadratic_form(x) == sum(x[i] * y[i] for i in range(n))
        assert lap.quadratic_form(x) >= 0
        assert all(sum(row) == 0 for row in a)
        assert all(lap.entry(i, j) == a[i][j] for i in range(n) for j in range(n))
