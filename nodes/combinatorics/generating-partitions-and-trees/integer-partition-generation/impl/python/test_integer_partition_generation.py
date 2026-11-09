# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integer-partition-generation/. The authors are listed in prov/E69C97.jsonl.

import random

from integer_partition_generation import partitions, step_counts


def partition_counts(limit: int) -> list[int]:
    """p(0..limit) by the standard counting table over the largest allowed part."""
    p = [1] + [0] * limit
    for part in range(1, limit + 1):
        for total in range(part, limit + 1):
            p[total] += p[total - part]
    return p


def brute_force(n: int) -> set[tuple[int, ...]]:
    """All partitions of n, from all multisets of parts, with an explicit stack."""
    out = set()
    stack = [((), n, n)]
    while stack:
        prefix, rest, cap = stack.pop()
        if rest == 0:
            out.add(prefix)
            continue
        for j in range(1, min(rest, cap) + 1):
            stack.append((prefix + (j,), rest - j, j))
    return out


P = partition_counts(60)


def test_example() -> None:
    assert list(partitions(5)) == [(5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)]
    assert list(partitions(6))[:5] == [(6,), (5, 1), (4, 2), (4, 1, 1), (3, 3)]


def test_edges() -> None:
    assert list(partitions(0)) == [()]
    assert list(partitions(1)) == [(1,)]
    assert list(partitions(2)) == [(2,), (1, 1)]
    assert list(partitions(3)) == [(3,), (2, 1), (1, 1, 1)]
    try:
        list(partitions(-1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative n must raise")


def test_against_brute_force() -> None:
    for n in range(0, 19):
        got = list(partitions(n))
        assert len(got) == P[n]
        assert len(set(got)) == len(got)
        assert set(got) == brute_force(n)


def test_reverse_lexicographic_order() -> None:
    for n in range(0, 26):
        got = list(partitions(n))
        for lam in got:
            assert sum(lam) == n
            assert all(lam[i] >= lam[i + 1] for i in range(len(lam) - 1))
            assert all(x >= 1 for x in lam)
        assert all(got[i] > got[i + 1] for i in range(len(got) - 1))


def test_counts_for_larger_n() -> None:
    for n in (30, 40, 45):
        assert sum(1 for _ in partitions(n)) == P[n]


def test_step_counts() -> None:
    for n in range(2, 46):
        fast, general, inner = step_counts(n)
        assert fast == P[n - 2]
        assert fast + general == P[n] - 1
        assert inner < P[n]
    assert step_counts(6) == (5, 5, 1)
    assert step_counts(0) == (0, 0, 0)
    assert step_counts(1) == (0, 0, 0)


def test_inner_loop_count_is_the_bijection_count() -> None:
    rng = random.Random(7)
    for n in rng.sample(range(2, 30), 10):
        target = 0
        for lam in partitions(n):
            big = [x for x in lam if x > 1]
            if big and min(big) + 1 in lam:
                target += 1
        assert step_counts(n)[2] == target
