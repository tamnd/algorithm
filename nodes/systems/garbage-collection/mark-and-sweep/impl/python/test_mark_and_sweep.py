# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mark-and-sweep/. The authors are listed in prov/MNBT5P.jsonl.

import random

import pytest

from mark_and_sweep import Heap


def reachable(fields: list[list[int | None]], roots: list[int | None]) -> set[int]:
    """Oracle: breadth-first search from the roots, independent of the collector."""
    seen = {r for r in roots if r is not None}
    queue = list(seen)
    i = 0
    while i < len(queue):
        for y in fields[queue[i]]:
            if y is not None and y not in seen:
                seen.add(y)
                queue.append(y)
        i += 1
    return seen


def example_heap() -> Heap:
    h = Heap(8, 2)
    for _ in range(8):
        h.allocate()
    links = {0: [1, 2], 1: [3, None], 2: [1, 0], 3: [None, None], 4: [6, 7], 5: [None, 5], 6: [4, None], 7: [None, None]}
    for a, f in links.items():
        h.fields[a] = list(f)
    h.roots = [0, 5]
    return h


def test_example() -> None:
    h = example_heap()
    assert h.free is None
    assert h.collect() == 3
    assert h.free_cells() == [4, 6, 7]
    assert h.fields[0] == [1, 2] and h.fields[2] == [1, 0] and h.fields[5] == [None, 5]
    assert h.marked == [False] * 8


def test_edges() -> None:
    h = Heap(0)
    assert h.collect() == 0
    with pytest.raises(MemoryError):
        h.allocate()
    h = Heap(3, 1)
    assert h.free_cells() == [0, 1, 2]
    assert h.collect() == 3
    h.roots = [h.allocate(), h.allocate(), h.allocate()]
    with pytest.raises(MemoryError):
        h.allocate()
    h.roots[1] = None
    assert h.allocate() == 1


def test_allocate_collects_garbage_cycle() -> None:
    h = Heap(4, 1)
    a, b = h.allocate(), h.allocate()
    h.fields[a][0], h.fields[b][0] = b, a
    h.roots = [h.allocate()]
    h.allocate()
    assert h.free is None
    got = h.allocate()
    assert got in (a, b) and h.collections == 1


def random_run(rng: random.Random, n: int, k: int, steps: int) -> None:
    h = Heap(n, k)
    h.roots = [None] * rng.randint(1, 3)
    for _ in range(steps):
        live = sorted(reachable(h.fields, h.roots))
        op = rng.random()
        if op < 0.35:
            before = reachable(h.fields, h.roots)
            try:
                a = h.allocate()
            except MemoryError:
                assert len(before) == n
                continue
            assert a not in before
            assert h.fields[a] == [None] * k
            h.roots[rng.randrange(len(h.roots))] = a
        elif op < 0.75 and live:
            x = rng.choice(live)
            h.fields[x][rng.randrange(k)] = rng.choice(live + [None])
        elif op < 0.9:
            h.roots[rng.randrange(len(h.roots))] = rng.choice(live + [None])
        else:
            want = reachable(h.fields, h.roots)
            snapshot = {a: list(h.fields[a]) for a in want}
            freed = h.collect()
            free = h.free_cells()
            assert len(free) == len(set(free)) == freed
            assert set(free) == set(range(n)) - want
            assert all(h.fields[a] == snapshot[a] for a in want)
            assert not any(h.marked)


def test_random_graphs_with_cycles() -> None:
    rng = random.Random(1960)
    for _ in range(600):
        random_run(rng, rng.randint(1, 12), rng.randint(1, 3), 40)
