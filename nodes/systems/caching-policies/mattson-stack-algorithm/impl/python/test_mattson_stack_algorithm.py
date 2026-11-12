# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mattson-stack-algorithm/. The authors are listed in prov/CPEY4J.jsonl.

import heapq
import random
from collections import OrderedDict

from mattson_stack_algorithm import hit_curve, miss_ratio_curve, stack_distances


def lru_hits(seq, k):
    cache, hits = OrderedDict(), 0
    for x in seq:
        if x in cache:
            hits += 1
            cache.move_to_end(x)
        else:
            if len(cache) == k:
                cache.popitem(last=False)
            cache[x] = True
    return hits


def min_hits(seq, k):
    """One simulation of Belady's MIN with a cache of size k."""
    n = len(seq)
    nxt, last = [n] * n, {}
    for t in range(n - 1, -1, -1):
        nxt[t] = last.get(seq[t], n)
        last[seq[t]] = t
    key, heap, hits = {}, [], 0
    for t, x in enumerate(seq):
        if x in key:
            hits += 1
        elif len(key) == k:
            while True:
                neg, _, y = heapq.heappop(heap)
                if key.get(y) == -neg:
                    break
            del key[y]
        key[x] = nxt[t]
        heapq.heappush(heap, (-nxt[t], t, x))
    return hits


def test_example() -> None:
    s = ["a", "b", "c", "a", "d", "b", "a", "c", "d", "a"]
    assert stack_distances(s) == [None, None, None, 3, None, 4, 3, 4, 4, 3]
    assert hit_curve(stack_distances(s), 5) == [0, 0, 0, 3, 6, 6]
    assert stack_distances(s, "opt") == [None, None, None, 2, None, 3, 2, 4, 3, 2]
    assert hit_curve(stack_distances(s, "opt"), 5) == [0, 0, 3, 5, 6, 6]
    for k in range(1, 6):
        assert hit_curve(stack_distances(s), 5)[k] == lru_hits(s, k)
        assert hit_curve(stack_distances(s, "opt"), 5)[k] == min_hits(s, k)


def test_classic_sequence() -> None:
    s = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    n = len(s)
    assert [n - h for h in hit_curve(stack_distances(s), 5)[1:]] == [12, 12, 10, 8, 5]
    assert [n - h for h in hit_curve(stack_distances(s, "opt"), 5)[1:]] == [12, 9, 7, 6, 5]


def test_one_pass_equals_one_simulation_per_size() -> None:
    rng = random.Random(2024)
    for _ in range(300):
        pages = rng.randrange(1, 9)
        seq = [rng.randrange(pages) for _ in range(rng.randrange(60))]
        kmax = pages + 1
        lru_curve = hit_curve(stack_distances(seq, "lru"), kmax)
        opt_curve = hit_curve(stack_distances(seq, "opt"), kmax)
        for k in range(1, kmax + 1):
            assert lru_curve[k] == lru_hits(seq, k)
            assert opt_curve[k] == min_hits(seq, k)


def test_skewed_trace() -> None:
    rng = random.Random(99)
    weights = [1.0 / (i + 1) for i in range(30)]
    seq = rng.choices(range(30), weights=weights, k=2000)
    curve = hit_curve(stack_distances(seq), 30)
    for k in (1, 2, 5, 10, 20, 30):
        assert curve[k] == lru_hits(seq, k)


def test_distance_none_only_on_first_use() -> None:
    rng = random.Random(1)
    seq = [rng.randrange(10) for _ in range(200)]
    seen = set()
    for x, d in zip(seq, stack_distances(seq)):
        assert (d is None) == (x not in seen)
        seen.add(x)


def test_miss_ratio_curve() -> None:
    s = [1, 2, 1, 2]
    assert miss_ratio_curve(s, 2) == [1.0, 0.5]
    assert miss_ratio_curve([], 3) == [0.0, 0.0, 0.0]
