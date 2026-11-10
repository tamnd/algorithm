# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cooperative-groups/.

import random

import pytest

from cooperative_groups import (cooperative_sum, max_cooperative_blocks, meta_group_size,
                                tile_ranks)


def test_tiled_partition_ranks():
    ranks = tile_ranks(256, 8)
    assert ranks[0] == (0, 0) and ranks[7] == (7, 0) and ranks[8] == (0, 1) and ranks[255] == (7, 31)
    assert meta_group_size(256, 8) == 32 and meta_group_size(256, 32) == 8
    for size in (1, 2, 4, 8, 16, 32):
        r = tile_ranks(128, size)
        assert sorted(set(r)) == sorted((t, g) for g in range(128 // size) for t in range(size))
    with pytest.raises(AssertionError):
        tile_ranks(128, 6)


def test_grid_sync_works_when_all_blocks_are_resident():
    rng = random.Random(16)
    for n in (1, 100, 1000):
        x = [rng.randrange(-100, 100) for _ in range(n)]
        blocks = -(-n // 64)
        for slots in (blocks, blocks + 3, 4 * blocks):
            assert cooperative_sum(x, 64, blocks, slots) == sum(x)


def test_grid_sync_deadlocks_when_the_grid_is_too_large():
    x = list(range(1000))
    blocks = 16
    for slots in (1, 8, 15):
        assert cooperative_sum(x, 64, blocks, slots) is None
    assert cooperative_sum(x, 64, blocks, 16) == sum(x)


def test_page_example_of_the_largest_cooperative_grid():
    assert max_cooperative_blocks(108, 4) == 432
