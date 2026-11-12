# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-associative-cache/. The authors are listed in prov/Q5H7VX.jsonl.

import random
from collections import OrderedDict

import pytest

from set_associative_cache import SetAssociativeCache, run


def lru_blocks(capacity, blocks):
    """A fully associative LRU cache of blocks, as a reference."""
    cache, out = OrderedDict(), []
    for b in blocks:
        if b in cache:
            cache.move_to_end(b)
            out.append(True)
        else:
            if len(cache) == capacity:
                cache.popitem(last=False)
            cache[b] = True
            out.append(False)
    return out


def per_set_lru(sets, ways, blocks):
    """A separate LRU cache of W blocks for each set, chosen by block mod S."""
    caches = [OrderedDict() for _ in range(sets)]
    out = []
    for b in blocks:
        c = caches[b % sets]
        if b in c:
            c.move_to_end(b)
            out.append(True)
        else:
            if len(c) == ways:
                c.popitem(last=False)
            c[b] = True
            out.append(False)
    return out


def test_split_into_tag_index_offset() -> None:
    c = SetAssociativeCache(sets=64, ways=4, block=64)
    address = (0x1234 << 12) | (37 << 6) | 9
    assert c.split(address) == (0x1234, 37, 9)


def test_one_set_is_fully_associative_lru() -> None:
    rng = random.Random(1)
    for ways in (1, 2, 3, 8):
        blocks = [rng.randrange(20) for _ in range(2000)]
        c = SetAssociativeCache(sets=1, ways=ways, block=16)
        assert run(c, [16 * b + rng.randrange(16) for b in blocks]) == lru_blocks(ways, blocks)


def test_each_set_is_its_own_lru_cache() -> None:
    rng = random.Random(2)
    blocks = [rng.randrange(64) for _ in range(5000)]
    c = SetAssociativeCache(sets=8, ways=4, block=32)
    assert run(c, [32 * b for b in blocks]) == per_set_lru(8, 4, blocks)


def test_conflict_misses_in_a_direct_mapped_cache() -> None:
    # 8 sets of 1 way, 16-byte blocks: addresses 0 and 128 are blocks 0 and 8, both in set 0
    trace = [0, 128] * 10
    direct = SetAssociativeCache(sets=8, ways=1, block=16)
    assert run(direct, trace).count(True) == 0  # every access misses
    two_way = SetAssociativeCache(sets=4, ways=2, block=16)
    assert run(two_way, trace).count(True) == 18  # same 8 blocks of space, only 2 cold misses
    full = SetAssociativeCache(sets=1, ways=8, block=16)
    assert run(full, trace).count(True) == 18


def test_plru_with_two_ways_is_lru() -> None:
    rng = random.Random(3)
    blocks = [rng.randrange(40) for _ in range(5000)]
    a = SetAssociativeCache(sets=4, ways=2, block=8, policy="plru")
    b = SetAssociativeCache(sets=4, ways=2, block=8, policy="lru")
    addrs = [8 * x for x in blocks]
    assert run(a, addrs) == run(b, addrs)


def test_plru_differs_from_lru_with_four_ways() -> None:
    # one set of 4 ways holding blocks 0 1 2 3 in ways 0 1 2 3; then touch 2 and 0.
    # LRU evicts block 1, the oldest. In the tree, the use of 0 points the root to the
    # right pair, and the use of 2 points that pair to way 3, so PLRU evicts block 3.
    seq = [0, 1, 2, 3, 2, 0, 4]
    lru = SetAssociativeCache(sets=1, ways=4, block=1, policy="lru")
    plru = SetAssociativeCache(sets=1, ways=4, block=1, policy="plru")
    run(lru, seq)
    run(plru, seq)
    assert lru.contents() == {0, 2, 3, 4}
    assert plru.contents() == {0, 1, 2, 4}
    assert lru.access(1) is False and plru.access(1) is True


def test_at_most_w_lines_per_set_and_random_is_seeded() -> None:
    rng = random.Random(4)
    trace = [rng.randrange(1 << 16) for _ in range(5000)]
    a = SetAssociativeCache(sets=16, ways=4, block=64, policy="random", rng=random.Random(9))
    b = SetAssociativeCache(sets=16, ways=4, block=64, policy="random", rng=random.Random(9))
    assert run(a, trace) == run(b, trace)
    assert len(a.contents()) <= 64
    for s, line in enumerate(a.tags):
        tags = [t for t in line if t is not None]
        assert len(tags) == len(set(tags)) <= 4
    assert a.contents() <= {x >> 6 for x in trace}
    assert a.hits + a.misses == len(trace)


def test_rejects_bad_shapes() -> None:
    with pytest.raises(ValueError):
        SetAssociativeCache(sets=6, ways=2)
    with pytest.raises(ValueError):
        SetAssociativeCache(sets=4, ways=3, policy="plru")
    with pytest.raises(ValueError):
        SetAssociativeCache(sets=4, ways=2, policy="random")
