# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thread-block-and-grid/.

import random

from thread_block_and_grid import (global_xyz, grid_for, grid_stride_indices, idle_lanes,
                                   linear_block, linear_thread, threads_of, valid_launch,
                                   warps_per_block)


def test_linear_rank_is_a_bijection_with_x_fastest():
    for block in ((32, 1, 1), (16, 8, 1), (8, 4, 2), (5, 3, 7)):
        ranks = [linear_thread(t, block) for _, t in threads_of((1, 1, 1), block)]
        assert ranks == list(range(block[0] * block[1] * block[2]))
    assert linear_thread((1, 0, 0), (16, 16, 1)) == 1
    assert linear_thread((0, 1, 0), (16, 16, 1)) == 16
    assert linear_block((2, 1, 0), (4, 3, 1)) == 6


def test_2d_grid_covers_a_matrix_once_with_a_guard():
    rng = random.Random(6)
    for _ in range(20):
        width, height = rng.randrange(1, 70), rng.randrange(1, 70)
        block = rng.choice([(16, 16, 1), (32, 8, 1), (8, 8, 1)])
        grid = grid_for((width, height, 1), block)
        seen = {}
        for b, t in threads_of(grid, block):
            col, row, _ = global_xyz(b, t, block)
            if col < width and row < height:
                seen[(row, col)] = seen.get((row, col), 0) + 1
        assert len(seen) == width * height and set(seen.values()) == {1}


def test_page_example_of_a_2d_grid():
    assert grid_for((1000, 600, 1), (16, 16, 1)) == (63, 38, 1)
    assert 63 * 38 * 256 - 1000 * 600 == 12864


def test_grid_stride_loop_covers_each_index_once():
    for n in (0, 1, 31, 32, 1000, 4097):
        for grid_x, block_x in ((1, 32), (3, 64), (8, 128), (100, 256)):
            visits = grid_stride_indices(n, grid_x, block_x)
            flat = sorted(i for v in visits.values() for i in v)
            assert flat == list(range(n))
            stride = grid_x * block_x
            assert max(len(v) for v in visits.values()) == -(-n // stride)


def test_launch_limits():
    assert valid_launch((2**31 - 1, 1, 1), (1024, 1, 1))
    assert not valid_launch((2**31, 1, 1), (1024, 1, 1))
    assert not valid_launch((1, 65536, 1), (32, 1, 1))
    assert not valid_launch((1, 1, 1), (1, 1, 65))
    assert not valid_launch((1, 1, 1), (32, 32, 2))
    assert valid_launch((1, 1, 1), (16, 16, 4))


def test_warps_and_idle_lanes():
    assert warps_per_block((256, 1, 1)) == 8 and idle_lanes((256, 1, 1)) == 0
    assert warps_per_block((100, 1, 1)) == 4 and idle_lanes((100, 1, 1)) == 28
    assert warps_per_block((10, 10, 1)) == 4
