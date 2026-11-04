# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/green-filter/. The authors are listed in prov/12PBRG.jsonl.

import random

from green_filter import green_16, green_filter, green_network


def depth(net: list[tuple[int, int]], n: int) -> int:
    level = [0] * n
    for i, j in net:
        level[i] = level[j] = max(level[i], level[j]) + 1
    return max(level, default=0)


def sorts_all_zero_one(net: list[tuple[int, int]], n: int) -> bool:
    """Run all 2^n inputs at once: bit v of wire[k] is item k of input v."""
    full = (1 << (1 << n)) - 1
    wire = []
    for k in range(n):
        block = (1 << (1 << k)) - 1
        pattern = 0
        period = 1 << (k + 1)
        for start in range(0, 1 << n, period):
            pattern |= block << (start + (1 << k))
        wire.append(pattern & full)
    for i, j in net:
        wire[i], wire[j] = wire[i] & wire[j], wire[i] | wire[j]
    return all(wire[k] & ~wire[k + 1] == 0 for k in range(n - 1))


def test_example() -> None:
    a = [3, 8, 13, 12, 10, 2, 7, 15, 6, 0, 4, 5, 11, 9, 1, 14]
    green_filter(a)
    assert a == list(range(16))


def test_size_and_depth() -> None:
    net = green_16()
    assert len(net) == 60
    assert depth(net, 16) == 10
    assert all(i < j for i, j in net)


def test_filter_order() -> None:
    rng = random.Random(16)
    for _ in range(200):
        x = [rng.randint(0, 99) for _ in range(16)]
        for i, j in green_16()[:32]:
            if x[j] < x[i]:
                x[i], x[j] = x[j], x[i]
        for w in range(16):
            for v in range(16):
                if w & v == w:
                    assert x[w] <= x[v]


def test_all_zero_one_inputs() -> None:
    for n in range(1, 17):
        assert sorts_all_zero_one(green_network(n), n)


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [5, 5, 4, 4, 3], list(range(40, 0, -1))):
        b = list(a)
        green_filter(b)
        assert b == sorted(a)


def test_random_against_sorted() -> None:
    rng = random.Random(1969)
    for _ in range(600):
        a = [rng.randint(-40, 40) for _ in range(rng.randint(0, 80))]
        b = list(a)
        green_filter(b)
        assert b == sorted(a)
