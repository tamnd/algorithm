# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-histogram/. The authors are listed in prov/DG02CV.jsonl.

import random
from collections import Counter

from parallel_histogram import histogram, span_formula, work_formula


def oracle(x: list[int], k: int) -> list[int]:
    c = Counter(x)
    return [c[j] for j in range(k)]


def test_example() -> None:
    x = [2, 0, 1, 2, 2, 3, 0, 2, 1, 3]
    h, cost = histogram(x, 4, 4)
    assert h == [2, 2, 4, 2]
    assert (cost.work, cost.span) == (50, 15)


def test_edges() -> None:
    assert histogram([], 3, 1)[0] == [0, 0, 0]
    assert histogram([], 3, 5)[0] == [0, 0, 0]
    assert histogram([0], 1, 1)[0] == [1]
    assert histogram([1, 1, 1], 2, 10)[0] == [0, 3]


def test_random_against_counter() -> None:
    rng = random.Random(4)
    for _ in range(800):
        n = rng.randint(0, 300)
        k = rng.randint(1, 40)
        p = rng.randint(1, 50)
        skew = rng.random() < 0.3
        x = [min(k - 1, int(rng.expovariate(1.0))) if skew else rng.randrange(k) for _ in range(n)]
        h, cost = histogram(x, k, p)
        assert h == oracle(x, k)
        assert cost.work == work_formula(n, k, p)
        assert cost.span == span_formula(n, k, p)


def test_trade_off() -> None:
    # with p = ceil(n / k) blocks the work is at most 4n + 3k and the span is O(k + log n log k)
    rng = random.Random(8)
    for n, k in ((4096, 16), (4096, 256), (10000, 10)):
        p = -(-n // k)
        x = [rng.randrange(k) for _ in range(n)]
        h, cost = histogram(x, k, p)
        assert h == oracle(x, k)
        assert cost.work <= 4 * n + 3 * k
        assert cost.span <= 2 * k + (n.bit_length()) * (k.bit_length() + 2)
