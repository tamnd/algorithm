# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belady-algorithm/. The authors are listed in prov/6CTF08.jsonl.

import random
from collections.abc import Hashable, Sequence

from belady_algorithm import belady, next_requests


def brute_opt(sigma: Sequence[Hashable], k: int) -> int:
    """Least number of faults over all demand paging schedules, by search over caches."""
    states: dict[frozenset, int] = {frozenset(): 0}
    for p in sigma:
        new: dict[frozenset, int] = {}
        for c, f in states.items():
            if p in c:
                outs = [(c, f)]
            elif len(c) < k:
                outs = [(c | {p}, f + 1)]
            else:
                outs = [((c - {q}) | {p}, f + 1) for q in c]
            for c2, f2 in outs:
                if f2 < new.get(c2, f2 + 1):
                    new[c2] = f2
        states = new
    return min(states.values())


def lru_caches(sigma: Sequence[Hashable], k: int) -> tuple[int, list[frozenset]]:
    order: list[Hashable] = []
    faults, caches = 0, []
    for p in sigma:
        if p in order:
            order.remove(p)
        else:
            faults += 1
            if len(order) == k:
                order.pop(0)
        order.append(p)
        caches.append(frozenset(order))
    return faults, caches


def fifo_caches(sigma: Sequence[Hashable], k: int) -> tuple[int, list[frozenset]]:
    queue: list[Hashable] = []
    faults, caches = 0, []
    for p in sigma:
        if p not in queue:
            faults += 1
            if len(queue) == k:
                queue.pop(0)
            queue.append(p)
        caches.append(frozenset(queue))
    return faults, caches


def belady_caches(sigma: Sequence[Hashable], k: int) -> list[frozenset]:
    _, evicted = belady(sigma, k)
    cache: set[Hashable] = set()
    caches = []
    for p, q in zip(sigma, evicted):
        if q is not None:
            cache.remove(q)
        cache.add(p)
        assert len(cache) <= k
        caches.append(frozenset(cache))
    return caches


def test_example() -> None:
    sigma = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3]
    faults, evicted = belady(sigma, 3)
    assert faults == 6
    assert [q for q in evicted if q is not None] == [3, 4, 5]
    assert evicted[3] == 3 and evicted[6] == 4 and evicted[9] == 5
    assert lru_caches(sigma, 3)[0] == 8
    assert fifo_caches(sigma, 3)[0] == 8


def test_edges() -> None:
    assert belady([], 1) == (0, [])
    assert belady([7], 1) == (1, [None])
    assert belady([1, 1, 1], 1) == (1, [None, None, None])
    assert belady([1, 2, 1, 2], 1)[0] == 4
    assert belady([1, 2, 3, 1, 2, 3], 5)[0] == 3
    assert belady(["a", "b", "a", "c", "b"], 2)[0] == 3
    assert next_requests([1, 2, 1, 1]) == [2, 4, 3, 4]


def test_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(600):
        k = rng.randint(1, 4)
        pages = rng.randint(1, k + 3)
        sigma = [rng.randrange(pages) for _ in range(rng.randint(0, 12))]
        faults, evicted = belady(sigma, k)
        assert faults == brute_opt(sigma, k)
        caches = belady_caches(sigma, k)
        assert all(sigma[t] in caches[t] for t in range(len(sigma)))


def test_lru_fifo_within_k_times_opt() -> None:
    rng = random.Random(2)
    for _ in range(500):
        k = rng.randint(1, 5)
        pages = rng.randint(1, 2 * k + 2)
        sigma = [rng.randrange(pages) for _ in range(rng.randint(0, 60))]
        opt = belady(sigma, k)[0]
        assert lru_caches(sigma, k)[0] <= k * opt
        assert fifo_caches(sigma, k)[0] <= k * opt


def test_belady_anomaly_for_fifo() -> None:
    sigma = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    f3, c3 = fifo_caches(sigma, 3)
    f4, c4 = fifo_caches(sigma, 4)
    assert (f3, f4) == (9, 10)
    assert [t + 1 for t in range(len(sigma)) if not c3[t] <= c4[t]] == [7, 8, 11]
    assert belady(sigma, 3)[0] == 7 and belady(sigma, 4)[0] == 6
    assert lru_caches(sigma, 3)[0] == 10 and lru_caches(sigma, 4)[0] == 8


def test_inclusion_property() -> None:
    rng = random.Random(3)
    for _ in range(500):
        pages = rng.randint(1, 8)
        sigma = [rng.randrange(pages) for _ in range(rng.randint(0, 40))]
        for k in range(1, 6):
            small, big = lru_caches(sigma, k)[1], lru_caches(sigma, k + 1)[1]
            assert all(a <= b for a, b in zip(small, big))
            small, big = belady_caches(sigma, k), belady_caches(sigma, k + 1)
            assert all(a <= b for a, b in zip(small, big))


def test_large_input() -> None:
    rng = random.Random(4)
    sigma = [rng.randrange(500) for _ in range(100000)]
    faults, _ = belady(sigma, 100)
    assert 500 <= faults <= len(sigma)
    prefix = sigma[:20000]
    assert belady(prefix, 100)[0] <= lru_caches(prefix, 100)[0]
