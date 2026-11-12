# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-garbage-collection/. The authors are listed in prov/02511Y.jsonl.

import random

import pytest

from parallel_garbage_collection import Marker, binary_tree, linked_list, random_heap, reachable


@pytest.mark.parametrize("workers", [1, 2, 3, 4, 8])
def test_marked_set_is_the_reachable_set(workers: int) -> None:
    rng = random.Random(workers)
    for _ in range(40):
        n = rng.randrange(1, 120)
        heap = random_heap(n, rng.randrange(1, 4), rng)
        roots = [rng.randrange(n) for _ in range(rng.randrange(0, 5))]
        m = Marker(heap, roots, workers, random.Random(rng.random()))
        marked = m.run()
        live = reachable(heap, roots)
        assert {x for x in range(n) if marked[x]} == live
        assert sum(m.scanned) == len(live)  # each live cell is scanned exactly once


def test_tree_is_balanced_by_stealing() -> None:
    heap = binary_tree(10)  # 1023 cells, depth 10
    rounds = {}
    for p in (1, 2, 4, 8):
        m = Marker(heap, [0], p, random.Random(1))
        m.run()
        rounds[p] = m.rounds
        assert m.rounds >= max(-(-1023 // p), 10)  # work and span bounds
        assert max(m.scanned) - min(m.scanned) <= 8
    assert rounds == {1: 1025, 2: 516, 4: 270, 8: 167}


def test_without_stealing_one_worker_does_everything() -> None:
    m = Marker(binary_tree(10), [0], 4, random.Random(1), steal=False)
    m.run()
    assert m.scanned == [1023, 0, 0, 0] and m.rounds == 1025


def test_a_list_has_no_parallelism() -> None:
    heap = linked_list(200)
    for p in (1, 4):
        m = Marker(heap, [0], p, random.Random(1))
        m.run()
        assert sum(m.scanned) == 200 and m.rounds >= 200
    assert m.rounds == 822  # stealing the only gray cell makes it slower


def test_workers_stop_only_when_all_work_is_gone() -> None:
    # Marker.run asserts after every round that a stopped worker implies empty deques.
    for seed in range(30):
        rng = random.Random(seed)
        heap = random_heap(60, 2, rng, nil=0.1)
        m = Marker(heap, [0, 1, 2], 5, rng)
        m.run()
        assert all(m.done) and m.active == 0
