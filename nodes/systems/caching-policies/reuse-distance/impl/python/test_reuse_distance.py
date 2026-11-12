# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reuse-distance/. The authors are listed in prov/30G9RA.jsonl.

import random
from collections import OrderedDict

from reuse_distance import lru_hits_from_distances, reuse_distances, reuse_distances_naive, reuse_times

EXAMPLE = ["a", "b", "c", "b", "b", "a", "d", "c", "a"]


def lru_stack_depths(seq):
    """0-based depth of each request in the LRU stack just before it, or None if absent."""
    stack, out = [], []
    for x in seq:
        if x in stack:
            out.append(stack.index(x))
            stack.remove(x)
        else:
            out.append(None)
        stack.insert(0, x)
    return out


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


def test_example() -> None:
    assert reuse_distances(EXAMPLE) == [None, None, None, 1, 0, 2, None, 3, 2]
    assert reuse_times(EXAMPLE) == [None, None, None, 2, 1, 5, None, 5, 3]


def test_fast_equals_naive_and_lru_depth() -> None:
    rng = random.Random(31)
    for _ in range(300):
        seq = [rng.randrange(rng.randrange(1, 12)) for _ in range(rng.randrange(80))]
        d = reuse_distances(seq)
        assert d == reuse_distances_naive(seq)
        assert d == lru_stack_depths(seq)


def test_distance_at_most_time_minus_one() -> None:
    rng = random.Random(32)
    seq = [rng.randrange(15) for _ in range(500)]
    for d, r in zip(reuse_distances(seq), reuse_times(seq)):
        assert (d is None) == (r is None)
        if d is not None:
            assert 0 <= d <= r - 1


def test_lru_hits_from_histogram() -> None:
    rng = random.Random(33)
    for _ in range(100):
        seq = [rng.randrange(10) for _ in range(rng.randrange(100))]
        d = reuse_distances(seq)
        for k in range(1, 12):
            assert lru_hits_from_distances(d, k) == lru_hits(seq, k)
