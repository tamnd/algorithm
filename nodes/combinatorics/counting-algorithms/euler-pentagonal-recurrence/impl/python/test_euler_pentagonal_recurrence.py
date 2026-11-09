# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-pentagonal-recurrence/. The authors are listed in prov/SBKFAF.jsonl.

import random

from euler_pentagonal_recurrence import partition_number, partition_numbers


def partitions_by_listing(n: int, largest: int | None = None) -> int:
    """Count partitions of n with parts at most largest by listing them (reference only)."""
    if largest is None:
        largest = n
    if n == 0:
        return 1
    return sum(partitions_by_listing(n - k, k) for k in range(1, min(n, largest) + 1))


def partitions_by_table(n: int) -> list[int]:
    """p(0), ..., p(n) by the coin change table over the largest part, O(n^2)."""
    p = [1] + [0] * n
    for k in range(1, n + 1):
        for m in range(k, n + 1):
            p[m] += p[m - k]
    return p


def test_first_values() -> None:
    # OEIS A000041
    assert partition_numbers(15) == [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176]


def test_edges() -> None:
    assert partition_numbers(0) == [1]
    assert partition_numbers(1) == [1, 1]
    assert partition_number(-3) == 0
    assert partition_numbers(5, 1) == [0] * 6


def test_known_values() -> None:
    assert partition_number(100) == 190569292
    assert partition_number(200) == 3972999029388
    assert partition_number(1000) == 24061467864032622473692149727991


def test_against_listing() -> None:
    p = partition_numbers(22)
    for n in range(23):
        assert p[n] == partitions_by_listing(n)


def test_against_table() -> None:
    assert partition_numbers(1500) == partitions_by_table(1500)


def test_random_moduli() -> None:
    rng = random.Random(4171)
    exact = partitions_by_table(600)
    for _ in range(40):
        n = rng.randint(0, 600)
        mod = rng.randint(1, 10**9)
        got = partition_numbers(n, mod)
        assert got == [v % mod for v in exact[: n + 1]]


def test_ramanujan_congruences() -> None:
    p = partition_numbers(700)
    assert all(p[5 * j + 4] % 5 == 0 for j in range(139))
    assert all(p[7 * j + 5] % 7 == 0 for j in range(99))
    assert all(p[11 * j + 6] % 11 == 0 for j in range(63))
