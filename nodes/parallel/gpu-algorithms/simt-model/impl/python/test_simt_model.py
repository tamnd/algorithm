# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simt-model/.

import random

from simt_model import (WARP_SIZE, Thread, branch_kernel, launch, reverse_in_block, vec_add,
                        warp_cost)


def test_vector_add_matches_sequential_sum():
    rng = random.Random(1)
    for n in (0, 1, 31, 32, 33, 64, 100, 257):
        for block in (32, 64, 128):
            a = [rng.randrange(-1000, 1000) for _ in range(n)]
            b = [rng.randrange(-1000, 1000) for _ in range(n)]
            c, _ = vec_add(a, b, block)
            assert c == [x + y for x, y in zip(a, b)]


def test_cost_is_counted_per_warp_instruction():
    # Each warp issues index and compare; a warp with at least one lane in range also issues
    # two loads, the add and the store. A partly full warp costs as much as a full one.
    for n in (1, 31, 32, 33, 63, 64, 65, 200):
        for block in (32, 64, 96):
            _, records = vec_add([0] * n, [0] * n, block)
            blocks = (n + block - 1) // block
            warps = blocks * ((block + WARP_SIZE - 1) // WARP_SIZE)
            active_warps = (n + WARP_SIZE - 1) // WARP_SIZE
            issued, lanes = warp_cost(records)
            assert issued == 2 * warps + 4 * active_warps
            assert lanes == 2 * blocks * block + 4 * n


def test_page_example_33_items_in_one_block_of_64():
    _, records = vec_add([0] * 33, [0] * 33, 64)
    assert warp_cost(records) == (12, 260)


def test_threads_map_to_warps_with_x_fastest():
    t = Thread((0, 0, 0), (5, 3, 0), (16, 4, 1), (1, 1, 1), [], {})
    assert t.tid == 5 + 3 * 16 and t.warp == 1 and t.lane == 21
    t = Thread((0, 0, 0), (7, 1, 2), (8, 4, 2), (1, 1, 1), [], {})
    assert t.tid == 7 + 1 * 8 + 2 * 32 and t.warp == 2 and t.lane == 15


def test_barrier_orders_the_two_phases():
    rng = random.Random(2)
    for n in (2, 5, 32, 33, 100):
        x = [rng.randrange(10**6) for _ in range(n)]
        assert reverse_in_block(x, sync=True) == x[::-1]
        assert reverse_in_block(x, sync=False) != x[::-1]


def test_divergent_branch_issues_both_paths():
    for split in (0, 1, 16, 31, 32):
        records = launch(branch_kernel, (1, 1, 1), (32, 1, 1), {}, args=(split,))
        issued, lanes = warp_cost(records)
        then_runs = 0 < split
        else_runs = split < 32
        assert issued == 2 + 2 * then_runs + 1 * else_runs
        assert lanes == 32 * 2 + 2 * split + (32 - split)
