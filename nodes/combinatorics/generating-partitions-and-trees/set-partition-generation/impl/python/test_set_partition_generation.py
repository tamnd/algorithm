# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-partition-generation/. The authors are listed in prov/8CRTRG.jsonl.

import random

from set_partition_generation import scan_steps, set_partitions, to_blocks


def stirling_table(limit: int) -> list[list[int]]:
    """S(n, k) for 0 <= k <= n <= limit by S(n, k) = k S(n-1, k) + S(n-1, k-1)."""
    s = [[0] * (limit + 1) for _ in range(limit + 1)]
    s[0][0] = 1
    for n in range(1, limit + 1):
        for k in range(1, n + 1):
            s[n][k] = k * s[n - 1][k] + s[n - 1][k - 1]
    return s


def bell_numbers(limit: int) -> list[int]:
    s = stirling_table(limit)
    return [sum(row) for row in s]


def brute_force(n: int) -> set[tuple[tuple[int, ...], ...]]:
    """All partitions of {1..n}, by inserting each element into a block or a new block, with an explicit stack."""
    out = set()
    stack: list[tuple[int, tuple[tuple[int, ...], ...]]] = [(0, ())]
    while stack:
        i, blocks = stack.pop()
        if i == n:
            out.add(tuple(sorted(blocks)))
            continue
        e = i + 1
        stack.append((e, blocks + ((e,),)))
        for t in range(len(blocks)):
            stack.append((e, blocks[:t] + (blocks[t] + (e,),) + blocks[t + 1 :]))
    return out


def is_rgs(a: tuple[int, ...]) -> bool:
    top = -1
    for v in a:
        if v < 0 or v > top + 1:
            return False
        top = max(top, v)
    return not a or a[0] == 0


def test_edge_cases():
    assert list(set_partitions(0)) == [()]
    assert list(set_partitions(1)) == [(0,)]
    assert list(set_partitions(2)) == [(0, 0), (0, 1)]
    assert scan_steps(0) == 0 and scan_steps(1) == 0
    assert to_blocks(()) == []
    try:
        list(set_partitions(-1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative n must raise ValueError")


def test_small_list():
    got = ["".join(map(str, a)) for a in set_partitions(4)]
    assert got == [
        "0000", "0001", "0010", "0011", "0012", "0100", "0101", "0102",
        "0110", "0111", "0112", "0120", "0121", "0122", "0123",
    ]
    assert to_blocks((0, 1, 1, 0)) == [[1, 4], [2, 3]]
    assert to_blocks((0, 1, 0, 2, 1)) == [[1, 3], [2, 5], [4]]


def test_matches_brute_force():
    for n in range(0, 9):
        got = list(set_partitions(n))
        assert len(got) == len(set(got))
        assert all(is_rgs(a) for a in got)
        assert {tuple(tuple(b) for b in to_blocks(a)) for a in got} == brute_force(n)


def test_counts_bell_and_stirling():
    limit = 10
    s = stirling_table(limit)
    bell = bell_numbers(limit)
    assert bell[:11] == [1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975]
    for n in range(0, limit + 1):
        by_blocks = [0] * (n + 1)
        count = 0
        for a in set_partitions(n):
            count += 1
            by_blocks[max(a) + 1 if a else 0] += 1
        assert count == bell[n]
        assert by_blocks == s[n][: n + 1]


def test_lexicographic_order():
    for n in range(0, 10):
        got = list(set_partitions(n))
        assert got == sorted(got)
        if n >= 1:
            assert got[0] == (0,) * n
            assert got[-1] == tuple(range(n))


def test_rank_formula_random():
    rng = random.Random(8023)
    for n in range(1, 10):
        got = list(set_partitions(n))
        memo: dict[tuple[int, int], int] = {}

        def completions(r: int, blocks: int) -> int:
            if r == 0:
                return 1
            key = (r, blocks)
            if key not in memo:
                memo[key] = blocks * completions(r - 1, blocks) + completions(r - 1, blocks + 1)
            return memo[key]

        for _ in range(30):
            idx = rng.randrange(len(got))
            a = got[idx]
            rank, top = 0, 0
            for i in range(1, n):
                rank += a[i] * completions(n - 1 - i, top + 1)
                top = max(top, a[i])
            assert rank == idx


def test_scan_total_is_less_than_bell():
    bell = bell_numbers(11)
    for n in range(1, 12):
        total = scan_steps(n)
        assert total == sum(bell[1:n])
        if n >= 2:
            assert total < bell[n]
