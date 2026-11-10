# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plru-replacement/. The authors are listed in prov/1SHFPZ.jsonl.

import random

from plru_replacement import TreePLRU, plru_replacement


def lru_misses(requests, ways):
    cache, misses = [], 0
    for x in requests:
        if x in cache:
            cache.remove(x)
        else:
            misses += 1
            if len(cache) == ways:
                cache.pop(0)
        cache.append(x)
    return misses


def timestamp_plru(requests, ways):
    """Independent model: at each node, go to the half whose latest access is older."""
    lines = [None] * ways
    last = [-1] * ways
    misses = 0
    for t, x in enumerate(requests):
        if x in lines:
            w = lines.index(x)
        else:
            misses += 1
            if None in lines:
                w = lines.index(None)
            else:
                lo, hi = 0, ways
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if max(last[lo:mid]) <= max(last[mid:hi]):
                        hi = mid
                    else:
                        lo = mid
                w = lo
            lines[w] = x
        last[w] = t
    return misses, lines


def test_dissertation_example() -> None:
    # Reineke (2008), Section 2.2.6: lines a, b, c, d with bits 1, 1, 0.
    c = TreePLRU(4)
    c.lines = ["a", "b", "c", "d"]
    c.bits = [0, 1, 1, 0]
    assert c.access("d") == (True, None)
    assert c.bits[1:] == [0, 1, 0]
    assert c.access("e") == (False, "b")
    assert c.lines == ["a", "e", "c", "d"]
    assert c.bits[1:] == [1, 0, 0]


def test_matches_timestamp_model() -> None:
    rng = random.Random(42)
    for _ in range(300):
        ways = rng.choice([1, 2, 4, 8])
        u = rng.randint(1, 2 * ways + 2)
        requests = [rng.randrange(u) for _ in range(rng.randint(0, 60))]
        misses, _ = plru_replacement(requests, ways)
        c = TreePLRU(ways)
        for x in requests:
            c.access(x)
        assert (misses, c.lines) == timestamp_plru(requests, ways)


def test_two_ways_is_lru() -> None:
    rng = random.Random(2)
    for _ in range(200):
        requests = [rng.randrange(5) for _ in range(rng.randint(0, 40))]
        assert plru_replacement(requests, 2)[0] == lru_misses(requests, 2)


def test_most_recent_blocks_stay() -> None:
    # The log2(A) + 1 most recently used distinct blocks are always in the set.
    rng = random.Random(3)
    for ways, keep in ((2, 2), (4, 3), (8, 4), (16, 5)):
        c = TreePLRU(ways)
        recent = []
        for _ in range(3000):
            x = rng.randrange(2 * ways + 3)
            c.access(x)
            if x in recent:
                recent.remove(x)
            recent.insert(0, x)
            assert all(y in c.lines for y in recent[:keep])


def test_stale_block_survives() -> None:
    # After a, b, c, d, e, the block e is never requested again but is never evicted,
    # while the working set a, b, c, d keeps missing. LRU with 4 ways stops missing.
    prefix, period = list("abcde"), list("abcabd")
    for reps in (10, 100):
        requests = prefix + period * reps
        misses, log = plru_replacement(requests, 4)
        assert misses == 6 + 2 * reps
        assert all(evicted != "e" for _, _, evicted in log)
        assert lru_misses(requests, 4) == 9


def test_edges() -> None:
    assert plru_replacement([], 4) == (0, [])
    assert plru_replacement(["x", "x"], 1)[0] == 1
    for bad in (0, 3, 6):
        try:
            TreePLRU(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("the number of ways must be a power of two")
