# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bin-packing-inapproximability/. The authors are listed in prov/9SGJ55.jsonl.

import random

from bin_packing_inapproximability import (
    first_fit_decreasing,
    has_partition,
    opt_bins,
    partition_to_bin_packing,
)


def test_examples() -> None:
    assert has_partition([3, 1, 1, 2, 2, 1])
    assert opt_bins(*partition_to_bin_packing([3, 1, 1, 2, 2, 1])) == 2
    assert not has_partition([2, 2, 3, 5])
    assert opt_bins(*partition_to_bin_packing([2, 2, 3, 5])) == 3
    assert opt_bins(*partition_to_bin_packing([5, 6, 7, 8, 9, 11])) == 2
    assert first_fit_decreasing(*partition_to_bin_packing([5, 6, 7, 8, 9, 11])) == 3


def test_gap_two_versus_three() -> None:
    rng = random.Random(2)
    for _ in range(400):
        a = [rng.randint(1, 12) for _ in range(rng.randint(2, 8))]
        cap, sizes = partition_to_bin_packing(a)
        opt = opt_bins(cap, sizes)
        if has_partition(a):
            assert opt == 2
        else:
            assert opt >= 3
        assert opt >= 2
        # Any absolute ratio rho < 3/2 gives at most floor(2 * rho) = 2 bins on yes-instances.
        assert (opt <= 2) == has_partition(a)


def test_padding_gives_k_versus_k_plus_one() -> None:
    rng = random.Random(4)
    for _ in range(150):
        a = [rng.randint(1, 9) for _ in range(rng.randint(2, 6))]
        k = rng.randint(2, 5)
        cap, sizes = partition_to_bin_packing(a, k)
        assert opt_bins(cap, sizes) == (k if has_partition(a) else k + 1)


def test_instance_size() -> None:
    rng = random.Random(6)
    for _ in range(100):
        a = [rng.randint(1, 30) for _ in range(rng.randint(2, 9))]
        k = rng.randint(2, 6)
        cap, sizes = partition_to_bin_packing(a, k)
        assert len(sizes) <= len(a) + k - 2 or len(sizes) == k + 1
        assert max(sizes) <= cap <= max(sum(a), 1)
