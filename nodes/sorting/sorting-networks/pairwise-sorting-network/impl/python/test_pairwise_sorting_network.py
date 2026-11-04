# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pairwise-sorting-network/. The authors are listed in prov/Y3SNG1.jsonl.

import itertools
import random

from pairwise_sorting_network import pairwise_network, pairwise_sorting_network


def depth(net: list[tuple[int, int]], n: int) -> int:
    level = [0] * n
    for i, j in net:
        level[i] = level[j] = max(level[i], level[j]) + 1
    return max(level, default=0)


def test_example() -> None:
    a = [1, 6, 8, 3, 2, 7, 5, 4]
    pairwise_sorting_network(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3], [5, 5, 4, 4, 3]):
        b = list(a)
        pairwise_sorting_network(b)
        assert b == sorted(a)


def test_size_and_depth_match_batcher() -> None:
    for k in range(1, 7):
        n = 2**k
        net = pairwise_network(n)
        assert len(net) == n * k * (k - 1) // 4 + n - 1
        assert depth(net, n) == k * (k + 1) // 2
        assert all(i < j for i, j in net)


def test_all_zero_one_inputs() -> None:
    for n in range(1, 13):
        net = pairwise_network(n)
        for bits in itertools.product((0, 1), repeat=n):
            b = list(bits)
            for i, j in net:
                if b[j] < b[i]:
                    b[i], b[j] = b[j], b[i]
            assert b == sorted(bits)


def test_random_against_sorted() -> None:
    rng = random.Random(1992)
    for _ in range(600):
        a = [rng.randint(-40, 40) for _ in range(rng.randint(0, 70))]
        b = list(a)
        pairwise_sorting_network(b)
        assert b == sorted(a)
