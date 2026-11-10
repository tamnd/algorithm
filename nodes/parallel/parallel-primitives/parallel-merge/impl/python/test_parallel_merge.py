# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-merge/. The authors are listed in prov/GDEWS9.jsonl.

import heapq
import math
import random

from parallel_merge import p_merge, p_merge_sort


def ceil_lg(x: int) -> int:
    return 0 if x <= 1 else (x - 1).bit_length()


def span_upper(n: int) -> float:
    """The span bound proved on the page: (floor(log_{4/3} N) + 1)(ceil(lg(N + 1)) + 2) + 1."""
    levels = 0 if n == 0 else math.floor(math.log(n, 4 / 3) + 1e-9) + 1
    return levels * (ceil_lg(n + 1) + 2) + 1


def work_upper(n: int) -> float:
    """The work bound proved on the page: 10 N + 1 - lg(N + 1)."""
    return 10 * n + 1 - math.log2(n + 1)


def merge(x: list[int], y: list[int]):
    t = x + y
    out = [None] * len(t)
    cost = p_merge(t, 0, len(x), len(x), len(t), out, 0)
    return out, cost


def test_example() -> None:
    out, cost = merge([1, 3, 5, 7, 9, 11], [2, 4, 4, 8, 10, 12, 14])
    assert out == [1, 2, 3, 4, 4, 5, 7, 8, 9, 10, 11, 12, 14]
    assert cost.work <= work_upper(13) and cost.span <= span_upper(13)


def test_edges() -> None:
    assert merge([], [])[0] == []
    assert merge([1], [])[0] == [1]
    assert merge([], [1])[0] == [1]
    assert merge([2, 2, 2], [2, 2])[0] == [2] * 5


def test_random_against_heapq() -> None:
    rng = random.Random(27)
    for _ in range(800):
        m, n = rng.randint(0, 70), rng.randint(0, 70)
        hi = rng.choice([3, 20, 1000])
        x = sorted(rng.randint(0, hi) for _ in range(m))
        y = sorted(rng.randint(0, hi) for _ in range(n))
        out, cost = merge(x, y)
        assert out == list(heapq.merge(x, y))
        assert m + n <= cost.work <= work_upper(m + n)
        assert cost.span <= span_upper(m + n)


def test_span_is_theta_log_squared() -> None:
    # on interleaved inputs the span is at least x (x + 1) / 2 with x = lg(N + 1)
    for big in list(range(1, 200)) + [2**k + d for k in range(8, 14) for d in (-1, 0, 1)]:
        x = list(range(0, big, 2))
        y = list(range(1, big, 2))
        for first, second in ((x, y), (y, x)):
            out, cost = merge(first, second)
            assert out == list(range(big))
            lg = math.log2(big + 1)
            assert lg * (lg + 1) / 2 <= cost.span <= span_upper(big)
            assert big <= cost.work <= work_upper(big)


def test_merge_sort() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(0, 100)
        a = [rng.randint(0, 50) for _ in range(n)]
        b = [None] * n
        cost = p_merge_sort(a, 0, n, b, 0)
        assert b == sorted(a)
        # each of the ceil(lg n) levels adds one merge of at most n items and one unit
        assert cost.span <= ceil_lg(n) * (span_upper(n) + 1) + 1


def test_merge_sort_span_is_theta_log_cubed() -> None:
    # the bit reversal permutation makes every merge interleaved
    for big_l in range(1, 11):
        n = 2**big_l
        a = [int(format(i, f"0{big_l}b")[::-1], 2) for i in range(n)]
        b = [None] * n
        cost = p_merge_sort(a, 0, n, b, 0)
        assert b == list(range(n))
        assert big_l * (big_l + 1) * (big_l + 2) / 6 <= cost.span <= big_l * (span_upper(n) + 1) + 1
