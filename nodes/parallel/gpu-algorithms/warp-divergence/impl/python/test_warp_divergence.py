# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-divergence/.

import random

from warp_divergence import branch, kernel_issues, loop, tree_reduction_issues, warp_issues


def test_divergent_branch_costs_the_sum_of_the_paths():
    for a in range(0, 5):
        for b in range(0, 5):
            issued, lanes = kernel_issues(32, branch(lambda i: i % 2 == 0, a, b))
            assert issued == 2 + a + b
            assert lanes == 32 * 2 + 16 * a + 16 * b


def test_warp_uniform_branch_costs_one_path():
    issued, _ = kernel_issues(128, branch(lambda i: (i // 32) % 2 == 0, 3, 5))
    assert issued == 2 * (2 + 3) + 2 * (2 + 5)


def test_masks_of_a_branch():
    traces = [branch(lambda i: i < 8, 1, 1)(i) for i in range(32)]
    _, _, masks = warp_issues(traces)
    assert masks[("then", 0)] == 0xFF and masks[("else", 0)] == 0xFFFFFF00
    assert masks["after"] == 0xFFFFFFFF


def test_loop_costs_the_largest_trip_count():
    rng = random.Random(12)
    for _ in range(50):
        trips = [rng.randrange(0, 20) for _ in range(32)]
        issued, lanes = kernel_issues(32, loop(lambda i: trips[i], body_len=2))
        assert issued == 3 * max(trips) + 1
        assert lanes == 3 * sum(trips) + 32


def test_sorting_work_by_trip_count_cuts_issues():
    rng = random.Random(13)
    trips = [rng.randrange(1, 64) for _ in range(1024)]
    plain, lanes1 = kernel_issues(1024, loop(lambda i: trips[i]))
    order = sorted(trips)
    bucketed, lanes2 = kernel_issues(1024, loop(lambda i: order[i]))
    assert lanes1 == lanes2
    assert bucketed < plain
    assert bucketed == sum(2 * max(order[w * 32:(w + 1) * 32]) + 1 for w in range(32))


def test_tree_reduction_layouts():
    assert tree_reduction_issues(256, interleaved=True) == (47, 255)
    assert tree_reduction_issues(256, interleaved=False) == (12, 255)
    for T in (32, 64, 128, 512, 1024):
        a, n1 = tree_reduction_issues(T, True)
        b, n2 = tree_reduction_issues(T, False)
        assert n1 == n2 == T - 1 and b <= a
