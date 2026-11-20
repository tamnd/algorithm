# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/su-rental-harmony-algorithm/. The authors are listed in prov/QR1JRG.jsonl.

import random
from fractions import Fraction
from itertools import permutations, product
from math import comb

import pytest

from su_rental_harmony_algorithm import (
    Labeler,
    boundary_doors,
    cell_in_region,
    count_cells,
    envy,
    fully_labeled_cells,
    owner,
    pivot,
    prices,
    su_rental_harmony,
    vertices,
)

F = Fraction


def cost_chooser(costs):
    """Tenant i pays costs[i][j] * p_j in its own eyes and picks the least (ties: smallest room).

    A free room costs 0, so the tenants are miserly, and the choice is a
    continuous preference.
    """

    def choose(i, p):
        return min(range(len(p)), key=lambda j: (costs[i][j] * p[j], j))

    return choose


def value_chooser(vals):
    """Miserly by rule: a free room if there is one, else the best value minus price."""

    def choose(i, p):
        free = [j for j in range(len(p)) if p[j] == 0]
        if free:
            return max(free, key=lambda j: (vals[i][j], -j))
        return max(range(len(p)), key=lambda j: (vals[i][j] - p[j], -j))

    return choose


def check_output(n, rent, grid, choose, rooms, price, questions):
    assert sorted(rooms) == list(range(n))
    assert all(x >= 0 for x in price) and sum(price) == rent
    assert questions <= comb(grid + n - 1, n - 1)


def test_page_example() -> None:
    w = [[2, 1, 1], [1, 2, 1], [1, 1, 1]]
    costs = [[F(1, x) for x in row] for row in w]
    choose = cost_chooser(costs)
    rooms, price, questions, steps = su_rental_harmony(3, F(900), 6, choose)
    assert rooms == [0, 1, 2]
    assert price == [400, 250, 250]
    assert (questions, steps) == (11, 8)
    assert envy(costs, rooms, price) == 0
    assert len(boundary_doors(3, 6, Labeler(3, 900, 6, choose))) == 1
    assert count_cells(3, 6) == 36


def test_envy_bound_on_cost_tenants() -> None:
    rng = random.Random(17)
    for n, grid in [(2, 2), (2, 9), (3, 3), (3, 10), (4, 4), (4, 9)]:
        for _ in range(6):
            costs = [[rng.randint(1, 5) for _ in range(n)] for _ in range(n)]
            rent = F(rng.randint(1, 1000))
            choose = cost_chooser(costs)
            rooms, price, questions, steps = su_rental_harmony(n, rent, grid, choose)
            check_output(n, rent, grid, choose, rooms, price, questions)
            # vertex prices of one cell differ by at most rent / grid per room
            for i, r in enumerate(rooms):
                for j in range(n):
                    extra = costs[i][r] * price[r] - costs[i][j] * price[j]
                    assert extra <= (costs[i][r] + costs[i][j]) * rent / grid


def test_cell_is_fully_labeled_and_count_is_odd() -> None:
    rng = random.Random(4)
    for n, grid in [(2, 7), (3, 6), (3, 8), (4, 5)]:
        for trial in range(5):
            if trial % 2:
                vals = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
                choose = value_chooser(vals)
            else:
                choose = cost_chooser([[rng.randint(1, 4) for _ in range(n)] for _ in range(n)])
            rooms, price, questions, steps = su_rental_harmony(n, 60, grid, choose)
            check_output(n, 60, grid, choose, rooms, price, questions)
            cells = fully_labeled_cells(n, 60, grid, choose)
            assert len(cells) % 2 == 1
            assert steps <= count_cells(n, grid)
            # the answer comes from one of the brute force cells: the owner of
            # each vertex chose the room it is given
            ok = False
            for cell in cells:
                vs = vertices(cell)
                if all(choose(owner(v, n), prices(v, n, F(60), grid)) == rooms[owner(v, n)] for v in vs):
                    ok = True
            assert ok


def all_boundary_doors(n, grid, label):
    """Brute force over every cell of the region and every facet."""
    found = set()
    for b in product(range(grid + 1), repeat=n - 1):
        for pi in permutations(range(n - 1)):
            cell = (b, pi)
            if not cell_in_region(cell, grid):
                continue
            vs = vertices(cell)
            for t in range(n):
                facet = frozenset(v for k, v in enumerate(vs) if k != t)
                if {label(v) for v in facet} == set(range(n - 1)) and not cell_in_region(pivot(cell, t)[0], grid):
                    found.add(facet)
    return found


def test_boundary_doors_against_brute_force() -> None:
    rng = random.Random(9)
    for n, grid in [(2, 5), (3, 3), (3, 5), (3, 8), (4, 4), (4, 6)]:
        for _ in range(6):
            choose = cost_chooser([[rng.randint(1, 6) for _ in range(n)] for _ in range(n)])
            label = Labeler(n, 1, grid, choose)
            near = {
                frozenset(v for k, v in enumerate(vertices(cell)) if k != t)
                for cell, t in boundary_doors(n, grid, label)
            }
            every = all_boundary_doors(n, grid, label)
            assert near == every
            assert len(every) % 2 == 1
            if n <= 3:
                assert len(every) == 1


def test_owners_distinct_in_each_cell() -> None:
    for n, grid in [(3, 4), (4, 4)]:
        for b in product(range(grid + 1), repeat=n - 1):
            for pi in permutations(range(n - 1)):
                assert len({owner(v, n) for v in vertices((b, pi))}) == n


def test_cell_count_is_grid_power() -> None:
    assert count_cells(2, 7) == 7
    assert count_cells(3, 5) == 25
    assert count_cells(4, 4) == 64


def test_rejects_small_grid() -> None:
    with pytest.raises(ValueError):
        su_rental_harmony(3, 10, 2, cost_chooser([[1] * 3] * 3))
