# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schorr-waite-marking/. The authors are listed in prov/AGATQM.jsonl.

import itertools
import random

from schorr_waite_marking import BinaryHeap, mark_all, schorr_waite_mark


def reachable(left: list[int | None], right: list[int | None], roots: list[int | None]) -> set[int]:
    """Oracle: breadth-first search with a set and a queue."""
    seen = {r for r in roots if r is not None}
    queue = list(seen)
    i = 0
    while i < len(queue):
        x = queue[i]
        for y in (left[x], right[x]):
            if y is not None and y not in seen:
                seen.add(y)
                queue.append(y)
        i += 1
    return seen


def check(left: list[int | None], right: list[int | None], roots: list[int | None]) -> None:
    h = BinaryHeap(left, right)
    mark_all(h, roots)
    want = reachable(left, right, roots)
    assert {a for a in range(len(left)) if h.mark[a]} == want
    assert h.left == left and h.right == right
    assert h.steps == 3 * len(want) + len(roots)


def test_example() -> None:
    left = [1, 3, 4, None, 0, None]
    right = [2, 2, None, 3, None, 4]
    h = BinaryHeap(left, right)
    schorr_waite_mark(h, 0)
    assert h.mark == [True, True, True, True, True, False]
    assert h.left == left and h.right == right
    assert h.steps == 16


def test_edges() -> None:
    check([], [], [])
    check([None], [None], [None])
    check([None], [None], [0])
    check([0], [0], [0])
    check([1, None], [None, 0], [1, 0, 1])


def test_long_list_needs_no_stack() -> None:
    n = 50000
    left = [i + 1 for i in range(n - 1)] + [None]
    right = [None] * n
    check(left, right, [0])


def test_all_graphs_up_to_three_cells() -> None:
    for n in range(1, 4):
        values = [None, *range(n)]
        for fields in itertools.product(values, repeat=2 * n):
            left, right = list(fields[:n]), list(fields[n:])
            for k in range(n + 1):
                for roots in itertools.combinations(range(n), k):
                    check(left, right, list(roots))


def test_all_graphs_of_four_cells_from_cell_zero() -> None:
    values = [None, 0, 1, 2, 3]
    for fields in itertools.product(values, repeat=8):
        check(list(fields[:4]), list(fields[4:]), [0])


def test_random_larger_graphs() -> None:
    rng = random.Random(1967)
    for _ in range(600):
        n = rng.randint(1, 40)
        left = [rng.choice([None, rng.randrange(n)]) for _ in range(n)]
        right = [rng.choice([None, rng.randrange(n)]) for _ in range(n)]
        roots = [rng.choice([None, rng.randrange(n)]) for _ in range(rng.randint(0, 4))]
        check(left, right, roots)
