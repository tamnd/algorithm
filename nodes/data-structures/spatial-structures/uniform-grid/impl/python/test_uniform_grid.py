# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-grid/. The authors are listed in prov/F5M3BP.jsonl.

import math
import random

import pytest

from uniform_grid import UniformGrid

PAGE = [(1.0, 1.0), (2.5, 1.5), (3.5, 3.2), (6.2, 0.5), (6.8, 1.6), (4.1, 5.0), (0.4, 4.4), (5.6, 5.9)]


def test_page_example() -> None:
    g = UniformGrid(0.0, 0.0, 2.0, 4, 3)
    for p in PAGE:
        g.insert(p)
        g.check_invariant()
    assert g.cell_of((3.5, 3.2)) == (1, 1)
    assert sorted(g.radius_query((3.0, 2.0), 2.0)) == [(2.5, 1.5), (3.5, 3.2)]
    pairs = sorted(tuple(sorted(pq)) for pq in g.close_pairs())
    assert pairs == [
        ((1.0, 1.0), (2.5, 1.5)),
        ((2.5, 1.5), (3.5, 3.2)),
        ((3.5, 3.2), (4.1, 5.0)),
        ((4.1, 5.0), (5.6, 5.9)),
        ((6.2, 0.5), (6.8, 1.6)),
    ]
    assert g.delete((2.5, 1.5))
    assert not g.delete((2.5, 1.5))
    g.check_invariant()
    assert g.radius_query((3.0, 2.0), 2.0) == [(3.5, 3.2)]
    assert len(g) == 7


def test_edges() -> None:
    g = UniformGrid(0.0, 0.0, 1.0, 1, 1)
    assert g.radius_query((0.5, 0.5), 10.0) == []
    assert g.close_pairs() == []
    with pytest.raises(ValueError):
        g.insert((1.0, 0.5))  # the cells are half-open
    with pytest.raises(ValueError):
        UniformGrid(0.0, 0.0, 0.0, 1, 1)
    g.insert((0.0, 0.0))
    g.insert((0.0, 0.0))
    assert len(g.radius_query((0.0, 0.0), 0.0)) == 2
    assert len(g.close_pairs()) == 1
    assert g.radius_query((0.0, 0.0), -1.0) == []
    # a query far outside the grid still works
    assert g.radius_query((100.0, 100.0), 1.0) == []


def test_all_in_one_cell() -> None:
    g = UniformGrid(0.0, 0.0, 10.0, 3, 3)
    for k in range(20):
        g.insert((1.0 + k * 0.01, 1.0))
    assert len(g.close_pairs()) == 190


def test_random_against_brute_force() -> None:
    rng = random.Random(17)
    for _ in range(600):
        h = rng.choice([0.5, 1.0, 2.5])
        nx, ny = rng.randint(1, 6), rng.randint(1, 6)
        g = UniformGrid(-1.0, 2.0, h, nx, ny)
        model: list[tuple[float, float]] = []
        for _ in range(rng.randint(0, 25)):
            if model and rng.random() < 0.3:
                p = rng.choice(model)
                model.remove(p)
                assert g.delete(p)
            else:
                p = (round(rng.uniform(-1.0, -1.0 + nx * h - 1e-9), 2), round(rng.uniform(2.0, 2.0 + ny * h - 1e-9), 2))
                if p[0] >= -1.0 + nx * h or p[1] >= 2.0 + ny * h:
                    continue
                g.insert(p)
                model.append(p)
        g.check_invariant()
        q = (rng.uniform(-3, 2 + nx * h), rng.uniform(0, 4 + ny * h))
        r = rng.uniform(0, 3)
        want = sorted(p for p in model if math.dist(p, q) <= r)
        assert sorted(g.radius_query(q, r)) == want
        want_pairs = sorted(
            tuple(sorted((model[a], model[b])))
            for a in range(len(model))
            for b in range(a + 1, len(model))
            if (model[a][0] - model[b][0]) ** 2 + (model[a][1] - model[b][1]) ** 2 <= h * h
        )
        assert sorted(tuple(sorted(pq)) for pq in g.close_pairs()) == want_pairs
