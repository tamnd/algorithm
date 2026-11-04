# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/odd-even-merge-sort/. The authors are listed in prov/0H3K90.jsonl.

import itertools
import random

from odd_even_merge_sort import odd_even_merge_network, odd_even_merge_sort


def depth(net: list[tuple[int, int]], n: int) -> int:
    level = [0] * n
    for i, j in net:
        level[i] = level[j] = max(level[i], level[j]) + 1
    return max(level, default=0)


def test_example() -> None:
    a = [1, 6, 8, 3, 2, 7, 5, 4]
    odd_even_merge_sort(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3], [5, 5, 4, 4, 3]):
        b = list(a)
        odd_even_merge_sort(b)
        assert b == sorted(a)


def test_size_and_depth() -> None:
    sizes = {2: 1, 4: 5, 8: 19, 16: 63, 32: 191, 64: 543}
    for k in range(1, 7):
        n = 2**k
        net = odd_even_merge_network(n)
        assert len(net) == sizes[n] == n * k * (k - 1) // 4 + n - 1
        assert depth(net, n) == k * (k + 1) // 2
        assert all(i < j for i, j in net)


def test_all_zero_one_inputs() -> None:
    for n in range(1, 13):
        net = odd_even_merge_network(n)
        for bits in itertools.product((0, 1), repeat=n):
            b = list(bits)
            for i, j in net:
                if b[j] < b[i]:
                    b[i], b[j] = b[j], b[i]
            assert b == sorted(bits)


def test_random_against_sorted() -> None:
    rng = random.Random(1968)
    for _ in range(600):
        a = [rng.randint(-40, 40) for _ in range(rng.randint(0, 70))]
        b = list(a)
        odd_even_merge_sort(b)
        assert b == sorted(a)
