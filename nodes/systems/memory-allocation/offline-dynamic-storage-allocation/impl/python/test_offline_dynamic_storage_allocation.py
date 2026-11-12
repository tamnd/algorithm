# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-dynamic-storage-allocation/. The authors are listed in prov/CVDZH6.jsonl.

import random
from itertools import product

from offline_dynamic_storage_allocation import (
    cost,
    first_fit_by_start,
    is_feasible,
    load,
    opt,
)

# The first-fit trap of the page: four unit items, two of them leave early,
# then an item of size 2 arrives.
TRAP = [(0, 5, 1), (1, 9, 1), (2, 5, 1), (3, 9, 1), (6, 9, 2)]


def random_items(rng: random.Random, n: int, hmax: int) -> list:
    items = []
    for _ in range(n):
        a = rng.randrange(8)
        items.append((a, a + rng.randint(1, 6), rng.randint(1, hmax)))
    return items


def brute_opt(items: list) -> int:
    top = sum(h for _, _, h in items)
    best = top
    for x in product(range(top), repeat=len(items)):
        if cost(items, list(x)) < best and is_feasible(items, list(x)):
            best = cost(items, list(x))
    return best


def test_trap() -> None:
    x = first_fit_by_start(TRAP)
    assert x == [0, 1, 2, 3, 4]
    assert cost(TRAP, x) == 6
    assert load(TRAP) == 4
    best, y = opt(TRAP)
    assert best == 4 and is_feasible(TRAP, y)


def test_edges() -> None:
    assert load([]) == 0
    assert opt([]) == (0, [])
    assert first_fit_by_start([(0, 1, 5)]) == [0]
    assert load([(0, 1, 2), (1, 2, 3)]) == 3
    assert opt([(0, 1, 2), (1, 2, 3)])[0] == 3


def test_opt_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(150):
        items = random_items(rng, rng.randint(1, 3), 3)
        assert opt(items)[0] == brute_opt(items)


def test_order_of_bounds() -> None:
    rng = random.Random(5)
    for _ in range(500):
        items = random_items(rng, rng.randint(1, 5), 4)
        lo = load(items)
        best, y = opt(items)
        x = first_fit_by_start(items)
        assert is_feasible(items, y) and is_feasible(items, x)
        assert lo <= best <= cost(items, x)


def test_unit_sizes_first_fit_is_optimal() -> None:
    rng = random.Random(9)
    for _ in range(300):
        items = random_items(rng, rng.randint(1, 8), 1)
        assert cost(items, first_fit_by_start(items)) == load(items)
