# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ternary-search/. The authors are listed in prov/R8SB5Q.jsonl.

import math
import random

from ternary_search import ternary_search_int, ternary_search_max


def test_example_int() -> None:
    f = [2, 5, 9, 14, 20, 23, 21, 18, 11, 8, 4, 1]
    assert ternary_search_int(lambda i: f[i], 0, len(f) - 1) == 5


def test_example_real() -> None:
    x = ternary_search_max(lambda t: -(t - 2) ** 2, 0.0, 5.0)
    assert abs(x - 2.0) < 1e-9


def test_edges_int() -> None:
    assert ternary_search_int(lambda i: 0, 7, 7) == 7
    assert ternary_search_int(lambda i: i, 0, 1) == 1
    assert ternary_search_int(lambda i: -i, 0, 1) == 0
    assert ternary_search_int(lambda i: i, -5, 9) == 9
    assert ternary_search_int(lambda i: -i, -5, 9) == -5


def test_every_mode_and_evaluation_bound() -> None:
    for n in range(1, 120):
        for m in range(n):
            calls = [0]

            def f(i: int) -> int:
                calls[0] += 1
                return -abs(i - m)

            assert ternary_search_int(f, 0, n - 1) == m
            if n >= 2:
                assert calls[0] <= 2 * math.ceil(math.log(n, 1.5))


def test_random_unimodal_sequences() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(1, 60)
        m = rng.randrange(n)
        left = sorted(rng.sample(range(1000), m))
        right = sorted(rng.sample(range(1000), n - m - 1), reverse=True)
        top = 1000 + rng.randrange(10)
        f = left + [top] + right
        assert ternary_search_int(lambda i: f[i], 0, n - 1) == m


def test_real_interval_length() -> None:
    for c in (0.0, 0.3, 1.7, 4.999):
        x = ternary_search_max(lambda t: -abs(t - c), 0.0, 5.0, steps=60)
        assert abs(x - c) <= 5.0 * (2 / 3) ** 60
