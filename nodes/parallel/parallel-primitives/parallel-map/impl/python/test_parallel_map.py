# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-map/. The authors are listed in prov/S8QNJR.jsonl.

import random

from parallel_map import blocked_map, parallel_map

SIZES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 100, 128, 1000]


def ceil_lg(n: int) -> int:
    return (n - 1).bit_length() if n > 0 else 0


def floor_lg(n: int) -> int:
    return n.bit_length() - 1


def test_example() -> None:
    out, work, span = parallel_map(lambda x: x * x, [3, 1, 7, 0, 4])
    assert out == [9, 1, 49, 0, 16]
    assert (work, span) == (5 + 4, 1 + 3)


def test_against_list_comprehension() -> None:
    rng = random.Random(42)
    funcs = [lambda x: x * x, lambda x: -x, str, lambda x: (x % 3, x // 3)]
    for f in funcs:
        for n in SIZES:
            a = [rng.randint(-100, 100) for _ in range(n)]
            assert parallel_map(f, a)[0] == [f(x) for x in a]
            for g in (1, 3, 8, 64):
                assert blocked_map(f, a, g)[0] == [f(x) for x in a]


def test_unit_cost_work_and_span_exact() -> None:
    for n in range(1, 700):
        _, work, span = parallel_map(lambda x: x, list(range(n)))
        assert work == n + (n - 1)
        assert span == ceil_lg(n) + 1


def test_uneven_costs() -> None:
    rng = random.Random(3)
    for n in SIZES[1:]:
        costs = [(rng.randint(1, 50), 0) for _ in range(n)]
        costs = [(w, rng.randint(1, w)) for w, _ in costs]
        _, work, span = parallel_map(lambda x: x, list(range(n)), lambda i: costs[i])
        assert work == (n - 1) + sum(w for w, _ in costs)
        smax = max(s for _, s in costs)
        assert smax + floor_lg(n) <= span <= smax + ceil_lg(n)


def test_grain_reduces_splits() -> None:
    n = 1000
    for g in (1, 10, 100):
        _, splits = blocked_map(lambda x: x, list(range(n)), g)
        # The leaves are ranges of at most g items, each more than g / 2.
        assert n / g - 1 <= splits < 2 * n / g
